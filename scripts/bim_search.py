#!/usr/bin/env python3
"""Busca objetos, expresiones y dependencias en un .bim sin volver a leer el JSON en cada consulta.

Uso:
    python bim_search.py search "texto" [--in all|name|desc|expr] [--kind K] [--table T]
                          [--regex RX] [-i] [--limit N] [--json]
    python bim_search.py show "Tabla[Objeto]" [--kind K] [--json]
    python bim_search.py refs "Objeto" [--table T] [--uses] [--json]
    python bim_search.py stats

Opciones comunes:
    --bim RUTA   archivo .bim. Si se omite, se usa el último que se consultó.
    --rebuild    reconstruye el índice aunque el archivo no haya cambiado.

El índice se crea la primera vez que se consulta un .bim y se guarda en la caché del usuario
(~/.cache/bim-search, o $XDG_CACHE_HOME). Se identifica por el hash del archivo: si el .bim cambia,
se reconstruye solo. Nada se escribe dentro del repo.

Búsqueda de texto: FTS5 con prefijos y sin tildes; varias palabras se combinan con AND.
--regex filtra en Python sobre los objetos que ya pasaron el filtro de texto y de tipo.
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bim_core import extract_refs, iter_objects, load_bim, sha256_file  # noqa: E402

SCHEMA_VERSION = "1"
CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "bim-search"
LAST_FILE = CACHE_DIR / "last.json"
FIELD_COLUMNS = {"name": "name", "desc": "description", "expr": "expression"}
SNIPPET_LEN = 140


# ------------------------------------------------------------ índice ----

def db_path_for(bim, sha):
    return CACHE_DIR / f"{Path(bim).stem}.{sha[:12]}.sqlite"


def build_index(bim, sha, db_path):
    tmp = db_path.with_suffix(".tmp")
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(tmp)
    con.executescript("""
        CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE objects(id INTEGER PRIMARY KEY, kind TEXT, tbl TEXT, name TEXT, data_type TEXT,
            description TEXT, display_folder TEXT, format_string TEXT, hidden INTEGER,
            source_column TEXT, expression TEXT, extra TEXT);
        CREATE INDEX ix_objects_kind ON objects(kind);
        CREATE INDEX ix_objects_tbl ON objects(tbl);
        CREATE INDEX ix_objects_name ON objects(name);
        CREATE TABLE refs(src INTEGER, ref_tbl TEXT, ref_name TEXT);
        CREATE INDEX ix_refs_name ON refs(ref_name);
        CREATE INDEX ix_refs_src ON refs(src);
        CREATE VIRTUAL TABLE fts USING fts5(name, tbl, description, expression,
            tokenize = 'unicode61 remove_diacritics 2');
    """)
    model = load_bim(bim)
    kinds = {}
    for i, obj in enumerate(iter_objects(model), start=1):
        kinds[obj["kind"]] = kinds.get(obj["kind"], 0) + 1
        con.execute("INSERT INTO objects VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            i, obj["kind"], obj["table"], obj["name"], obj["data_type"], obj["description"],
            obj["display_folder"], obj["format_string"], int(bool(obj["hidden"])), obj["source_column"],
            obj["expression"], json.dumps(obj["extra"], ensure_ascii=False)))
        con.execute("INSERT INTO fts(rowid, name, tbl, description, expression) VALUES (?,?,?,?,?)",
                    (i, obj["name"], obj["table"], obj["description"], obj["expression"]))
        refs = extract_refs(obj)
        if obj["kind"] == "relationship":
            refs = [(obj["table"], obj["extra"]["from_column"]), (obj["extra"]["to_table"], obj["extra"]["to_column"])]
        con.executemany("INSERT INTO refs VALUES (?,?,?)", [(i, t, n) for t, n in refs])
    con.executemany("INSERT INTO meta VALUES (?,?)", [
        ("schema", SCHEMA_VERSION), ("sha256", sha), ("source", str(Path(bim).resolve())),
        ("model_name", str(model.get("name", "")) or Path(bim).stem),
        ("built_at", time.strftime("%Y-%m-%d %H:%M:%S")), ("kinds", json.dumps(kinds))])
    con.commit()
    con.close()
    if db_path.exists():
        db_path.unlink()
    tmp.rename(db_path)


def ensure_index(bim, rebuild=False):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    sha = sha256_file(bim)
    db = db_path_for(bim, sha)
    if rebuild or not db.exists():
        t0 = time.time()
        build_index(bim, sha, db)
        print(f"# índice creado en {time.time() - t0:.1f} s: {db}", file=sys.stderr)
    LAST_FILE.write_text(json.dumps({"bim": str(Path(bim).resolve())}), encoding="utf-8")
    return sqlite3.connect(f"file:{db}?mode=ro", uri=True)


def resolve_bim(arg):
    if arg:
        return arg
    if LAST_FILE.exists():
        return json.loads(LAST_FILE.read_text(encoding="utf-8"))["bim"]
    raise SystemExit("Falta --bim: no hay un .bim consultado antes.")


# ---------------------------------------------------------- utilidades ----

def fold(text):
    """Minúsculas y sin tildes, para comparar como lo hace FTS."""
    return "".join(c for c in unicodedata.normalize("NFKD", text or "") if not unicodedata.combining(c)).lower()


def snippet(text, needles, regex=None):
    """Primera línea de text que contiene algún término (o que casa con la regex), recortada."""
    if not text:
        return ""
    for line in text.splitlines():
        hit = regex.search(line) if regex else any(n in fold(line) for n in needles)
        if hit:
            line = line.strip()
            return line if len(line) <= SNIPPET_LEN else line[:SNIPPET_LEN - 1] + "…"
    first = text.strip().splitlines()[0] if text.strip() else ""
    return first[:SNIPPET_LEN]


def fts_query(text, field):
    tokens = re.findall(r"\w+", text)
    if not tokens:
        return None
    body = " ".join(f'"{t}"*' for t in tokens)
    return body if field == "all" else f"{FIELD_COLUMNS[field]} : ({body})"


def fmt_row(r, snip=""):
    kind, tbl, name = r["kind"], r["tbl"] or "", r["name"] or ""
    return f"{kind:<18} {tbl[:28]:<28} {name[:40]:<40} {snip}"


def emit(rows, as_json):
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(row["line"])
        print(f"# {len(rows)} resultado(s)", file=sys.stderr)


def row_dict(row):
    keys = ("id", "kind", "tbl", "name", "data_type", "description", "display_folder", "format_string",
            "hidden", "source_column", "expression", "extra")
    return dict(zip(keys, row))


# ------------------------------------------------------------ comandos ----

def cmd_search(con, args):
    where, params = ["1=1"], []
    if args.kind:
        where.append("o.kind = ?")
        params.append(args.kind)
    if args.table:
        where.append("o.tbl = ?")
        params.append(args.table)
    regex = re.compile(args.regex, re.IGNORECASE if args.i else 0) if args.regex else None
    needles = [fold(t) for t in re.findall(r"\w+", args.text or "")]

    if args.text:
        match = fts_query(args.text, args.in_)
        sql = (f"SELECT o.id, o.kind, o.tbl, o.name, o.data_type, o.description, o.display_folder, o.format_string, "
               f"o.hidden, o.source_column, o.expression, o.extra FROM fts JOIN objects o ON o.id = fts.rowid "
               f"WHERE fts MATCH ? AND {' AND '.join(where)} ORDER BY bm25(fts) LIMIT ?")
        rows = con.execute(sql, [match, *params, args.limit * 5 if regex else args.limit]).fetchall()
    else:
        sql = (f"SELECT o.id, o.kind, o.tbl, o.name, o.data_type, o.description, o.display_folder, o.format_string, "
               f"o.hidden, o.source_column, o.expression, o.extra FROM objects o WHERE {' AND '.join(where)} "
               f"ORDER BY o.kind, o.tbl, o.name")
        rows = con.execute(sql, params).fetchall()

    out = []
    for raw in rows:
        r = row_dict(raw)
        fields = {"name": r["name"] or "", "desc": r["description"] or "", "expr": r["expression"] or ""}
        if regex:
            selected = [fields[f] for f in FIELD_COLUMNS if args.in_ in ("all", f)]
            hit = next((regex.search(s) for s in selected if regex.search(s)), None)
            if not hit:
                continue
        snip = snippet(r["expression"] or r["description"] or "", needles, regex)
        r["line"] = fmt_row(r, snip)
        out.append(r)
        if len(out) >= args.limit:
            break
    emit(out, args.json)


def find_objects(con, target, kind=None, table=None):
    if "[" in target and target.endswith("]"):
        table_part, name = target[:-1].rsplit("[", 1)
        table = table_part.strip("'").replace("''", "'") or table
        target = name
    where, params = ["name = ?"], [target]
    if kind:
        where.append("kind = ?")
        params.append(kind)
    if table:
        where.append("tbl = ?")
        params.append(table)
    rows = con.execute(f"SELECT id, kind, tbl, name, data_type, description, display_folder, format_string, hidden, "
                       f"source_column, expression, extra FROM objects WHERE {' AND '.join(where)} "
                       f"ORDER BY kind, tbl", params).fetchall()
    return [row_dict(r) for r in rows]


def cmd_show(con, args):
    found = find_objects(con, args.target, args.kind)
    if not found:
        raise SystemExit(f"No existe '{args.target}'")
    if len(found) > 1 and not args.json:
        print("Hay varias coincidencias; use --kind o Tabla[Objeto]:", file=sys.stderr)
        for r in found:
            print(fmt_row(r), file=sys.stderr)
        raise SystemExit(2)
    out = []
    for r in found:
        used = con.execute("SELECT COUNT(DISTINCT src) FROM refs WHERE ref_name = ? AND (ref_tbl IS NULL OR ref_tbl = ?)",
                           (r["name"], r["tbl"])).fetchone()[0]
        uses = [{"tbl": t, "name": n} for t, n in con.execute(
            "SELECT DISTINCT ref_tbl, ref_name FROM refs WHERE src = ?", (r["id"],))]
        r["used_by_count"] = used
        r["uses"] = uses
        out.append(r)
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    for r in out:
        print(f"{r['kind']}  {r['tbl'] or ''}[{r['name']}]")
        for label, key in (("Tipo", "data_type"), ("Carpeta", "display_folder"), ("Formato", "format_string"),
                           ("Descripción", "description"), ("Columna origen", "source_column")):
            if r.get(key):
                print(f"{label}: {r[key]}")
        extra = json.loads(r["extra"] or "{}")
        if extra:
            print("Datos: " + ", ".join(f"{k}={v}" for k, v in extra.items() if v not in (None, [], "")))
        print(f"Usado por: {r['used_by_count']} objeto(s)")
        if r["uses"]:
            print("Usa: " + ", ".join(f"{u['tbl'] + '[' + u['name'] + ']' if u['tbl'] else '[' + u['name'] + ']'}"
                                      for u in r["uses"]))
        if r["expression"]:
            print("-" * 60)
            print(r["expression"])
        print()


def cmd_refs(con, args):
    targets = find_objects(con, args.target, None, args.table)
    if not targets:
        raise SystemExit(f"No existe '{args.target}'")
    if args.uses:
        out = []
        for t in targets:
            for tbl, name in con.execute("SELECT DISTINCT ref_tbl, ref_name FROM refs WHERE src = ?", (t["id"],)):
                hit = find_objects(con, f"'{tbl}'[{name}]" if tbl else name)
                kinds = ", ".join(sorted({h["kind"] for h in hit})) or "sin resolver"
                out.append({"from": f"{t['kind']} {t['tbl'] or ''}[{t['name']}]", "tbl": tbl, "name": name,
                            "resolved_as": kinds})
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return
        for o in out:
            print(f"{o['from']}  →  {o['tbl'] + '[' if o['tbl'] else '['}{o['name']}]  ({o['resolved_as']})")
        print(f"# {len(out)} referencia(s)", file=sys.stderr)
        return

    out = []
    seen = set()
    for t in targets:
        sql = ("SELECT DISTINCT o.id, o.kind, o.tbl, o.name, o.data_type, o.description, o.display_folder, "
               "o.format_string, o.hidden, o.source_column, o.expression, o.extra, r.ref_tbl "
               "FROM refs r JOIN objects o ON o.id = r.src WHERE r.ref_name = ? AND (r.ref_tbl IS NULL OR r.ref_tbl = ?)")
        for row in con.execute(sql, (t["name"], t["tbl"])):
            r = row_dict(row[:12])
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            note = "" if row[12] else "  (referencia sin tabla: posible coincidencia)"
            r["line"] = fmt_row(r) + note
            out.append(r)
    emit(out, args.json)


def cmd_stats(con, args):
    meta = dict(con.execute("SELECT key, value FROM meta"))
    kinds = json.loads(meta["kinds"])
    stats = {
        "modelo": meta.get("model_name"), "origen": meta.get("source"), "índice": meta.get("built_at"),
        "objetos": dict(sorted(kinds.items())),
        "medidas_por_tabla": con.execute("SELECT tbl, COUNT(*) c FROM objects WHERE kind='measure' "
                                         "GROUP BY tbl ORDER BY c DESC LIMIT 10").fetchall(),
        "referencias_sin_resolver": con.execute(
            "SELECT COUNT(DISTINCT r.ref_name) FROM refs r WHERE r.ref_tbl IS NULL AND r.ref_name NOT IN "
            "(SELECT name FROM objects WHERE kind IN ('measure','column','calculated_column'))").fetchone()[0],
        "medidas_sin_referencias": con.execute(
            "SELECT COUNT(*) FROM objects o WHERE kind='measure' AND NOT EXISTS "
            "(SELECT 1 FROM refs r WHERE r.src=o.id) AND hidden=0").fetchone()[0],
    }
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
    for k, v in stats.items():
        if isinstance(v, dict):
            print(f"{k}:")
            for kk, vv in v.items():
                print(f"  {kk:<22} {vv}")
        elif isinstance(v, list):
            print(f"{k}:")
            for tbl, c in v:
                print(f"  {tbl:<40} {c}")
        else:
            print(f"{k}: {v}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bim", help="archivo .bim (por defecto, el último consultado)")
    ap.add_argument("--rebuild", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="buscar por texto o regex")
    s.add_argument("text", nargs="?", help="palabras a buscar (todas deben aparecer)")
    s.add_argument("--in", dest="in_", choices=["all", "name", "desc", "expr"], default="all")
    s.add_argument("--kind", help="table, column, calculated_column, measure, partition, relationship, ...")
    s.add_argument("--table", help="tabla propietaria exacta")
    s.add_argument("--regex", help="expresión regular adicional (Python)")
    s.add_argument("-i", action="store_true", help="regex sin distinguir mayúsculas")
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--json", action="store_true")

    sh = sub.add_parser("show", help="ver un objeto completo")
    sh.add_argument("target", help="Objeto o 'Tabla[Objeto]'")
    sh.add_argument("--kind")
    sh.add_argument("--json", action="store_true")

    rf = sub.add_parser("refs", help="quién usa un objeto (o qué usa, con --uses)")
    rf.add_argument("target")
    rf.add_argument("--table")
    rf.add_argument("--uses", action="store_true")
    rf.add_argument("--json", action="store_true")

    st = sub.add_parser("stats", help="resumen del modelo")
    st.add_argument("--json", action="store_true")

    args = ap.parse_args()
    if args.cmd == "search" and not args.text and not args.kind and not args.table and not args.regex:
        ap.error("search necesita texto, --kind, --table o --regex")
    bim = resolve_bim(args.bim)
    con = ensure_index(bim, args.rebuild)
    {"search": cmd_search, "show": cmd_show, "refs": cmd_refs, "stats": cmd_stats}[args.cmd](con, args)


if __name__ == "__main__":
    main()
