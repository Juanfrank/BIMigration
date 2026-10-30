#!/usr/bin/env python3
"""Núcleo para leer modelos Power BI en formato .bim (TMSL) y producir filas de objetos.

Uso como biblioteca (base para otros scripts):
    from bim_core import load_bim, iter_objects, extract_refs
    model = load_bim("Model.bim")
    for obj in iter_objects(model):
        ...   # obj es un dict con kind, table, name, expression, ...

Filas que produce iter_objects (claves comunes; las que no aplican quedan en None):
    kind           table | column | calculated_column | measure | partition | hierarchy
                   | relationship | shared_expression
    table, name    tabla propietaria y nombre del objeto
    expression     DAX (medidas y columnas calculadas), M (particiones y expresiones compartidas)
                   o "Origen.Col -> Destino.Col" (relaciones)
    data_type, description, display_folder, format_string, hidden, source_column
    extra          dict con datos específicos (cardinalidad, modo de partición, etc.)

extract_refs(obj) devuelve las referencias DAX de un objeto como [(tabla o None, nombre)].
Tabla None significa referencia sin calificar, por ejemplo [Medida].
"""
import hashlib
import json
import re

# 'Tabla con espacios'[Col] o Tabla[Col]. El nombre de tabla no puede contener corchetes.
QUALIFIED = re.compile(r"(?:'((?:[^']|'')+)'|([A-Za-z_][\w\.]*))\[([^\[\]]+)\]")
# [Medida] sin tabla. Se aplica al texto sin las referencias calificadas.
BARE = re.compile(r"\[([^\[\]]+)\]")
# Cadenas DAX ("...") y comentarios de línea (// y --) que no deben generar referencias.
DAX_STRING = re.compile(r'"(?:[^"]|"")*"')
DAX_COMMENT = re.compile(r"//[^\n]*|--[^\n]*")


def strip_dax_comments(expr):
    """Quita los comentarios DAX (// y -- hasta fin de línea, y /* ... */) de una expresión.

    No toca lo que va dentro de cadenas "...", nombres de tabla 'x' ni nombres de columna [x]:
    ahí // o -- son texto. Las líneas que quedan vacías se reducen a una sola.
    """
    if not expr:
        return expr
    out = []
    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c in ('"', "'"):
            j = i + 1
            while j < n:
                if expr[j] == c:
                    if j + 1 < n and expr[j + 1] == c:
                        j += 2
                        continue
                    break
                j += 1
            out.append(expr[i:j + 1])
            i = j + 1
        elif c == "[":
            j = expr.find("]", i)
            j = n - 1 if j < 0 else j
            out.append(expr[i:j + 1])
            i = j + 1
        elif expr.startswith("//", i) or expr.startswith("--", i):
            j = expr.find("\n", i)
            i = n if j < 0 else j
        elif expr.startswith("/*", i):
            j = expr.find("*/", i + 2)
            out.append(" ")
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    lines = [line.rstrip() for line in "".join(out).split("\n")]
    collapsed = []
    for line in lines:
        if line == "" and collapsed and collapsed[-1] == "":
            continue
        collapsed.append(line)
    return "\n".join(collapsed).strip("\n")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_bim(path):
    """Devuelve el objeto 'model' del .bim (acepta también el documento completo o el modelo suelto)."""
    with open(path, encoding="utf-8-sig") as f:
        doc = json.load(f)
    return doc.get("model", doc)


def join_text(value):
    """TMSL guarda expresiones como lista de líneas o como cadena."""
    if value is None:
        return None
    if isinstance(value, list):
        return "\n".join(value)
    return str(value)


NAV_ITEM = re.compile(r'\[\s*Schema\s*=\s*"([^"]+)"\s*,\s*Item\s*=\s*"([^"]+)"\s*\]')
CTE_NAME = re.compile(r"(\w+)\s+AS\s*\(", re.IGNORECASE)
FROM_JOIN = re.compile(r"\b(?:FROM|JOIN)\s+((?:\[[^\]]+\]|\w+)(?:\s*\.\s*(?:\[[^\]]+\]|\w+)){0,2})", re.IGNORECASE)
NAME_PART = re.compile(r"\[([^\]]+)\]|(\w+)")


STRING_LITERAL = re.compile(r'"((?:[^"]|"")*)"')
SQL_HINT = re.compile(r"\bSELECT\b.*\bFROM\b", re.IGNORECASE | re.DOTALL)
REFERENCE = re.compile(r"^\s*let\s+\w+\s*=\s*([A-Za-z_]\w*)\s*(?:,|\bin\b)", re.IGNORECASE)


SQL_DATABASE = re.compile(r'\bSql\.Database\s*\(\s*"[^"]*"\s*,\s*"([^"]+)"', re.IGNORECASE)
NAV_BASE = re.compile(r"(\w+)\s*\{\s*\[\s*Schema\s*=", re.IGNORECASE)
NATIVE_BASE = re.compile(r"Value\.NativeQuery\s*\(\s*(\w+)", re.IGNORECASE)


def _database_of(expr, var):
    """Nombre de la base de una variable M de la forma: var = Origen{[Name="base"]}[Data]."""
    m = re.search(r'\b' + re.escape(var) + r'\s*=\s*\w+\s*\{\s*\[\s*Name\s*=\s*"([^"]+)"', expr)
    return m.group(1) if m else None


def _sql_objects(sql, database):
    """Tablas y vistas de los FROM y JOIN de un texto SQL. No devuelve el texto.

    Un nombre de tres partes (base.esquema.tabla) indica su propia base; si no, se usa database.
    """
    text = sql.replace('""', '"').replace("#(lf)", "\n").replace("#(tab)", " ")
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    text = re.sub(r"--[^\n]*", " ", text)
    ctes = {c.lower() for c in CTE_NAME.findall(text)}
    objects = []
    for m in FROM_JOIN.finditer(text):
        parts = [a or b for a, b in NAME_PART.findall(m.group(1))]
        if len(parts) == 1 and parts[0].lower() in ctes:
            continue
        obj = {"database": parts[0] if len(parts) == 3 else database,
               "schema": parts[-2] if len(parts) >= 2 else None, "name": parts[-1]}
        if obj not in objects:
            objects.append(obj)
    return objects


def parse_m_source(expr):
    """Origen de una expresión M de partición: base de datos, esquema y tabla o vista, sin texto de la consulta.

    kind:    navigation   (Schema/Item de un origen SQL)
             native_query (SQL en Query= o en cualquier literal con SELECT ... FROM)
             reference    (la consulta toma otra tabla del modelo como origen)
             file         (Excel, CSV o JSON; la ruta no se devuelve)
             embedded     (datos escritos en la propia expresión)
             None         (sin origen reconocible)
    objects: [{"database": str|None, "schema": str|None, "name": str}]
    """
    if not expr:
        return {"kind": None, "objects": []}
    nav = NAV_ITEM.search(expr)
    if nav:
        base = NAV_BASE.search(expr)
        database = _database_of(expr, base.group(1)) if base else None
        return {"kind": "navigation",
                "objects": [{"database": database, "schema": nav.group(1), "name": nav.group(2)}]}
    sql_literals = [m.group(1) for m in STRING_LITERAL.finditer(expr) if SQL_HINT.search(m.group(1))]
    if sql_literals:
        database = None
        sql_db = SQL_DATABASE.search(expr)
        if sql_db:
            database = sql_db.group(1)
        else:
            native = NATIVE_BASE.search(expr)
            database = _database_of(expr, native.group(1)) if native else None
        objects = []
        for literal in sql_literals:
            for obj in _sql_objects(literal, database):
                if obj not in objects:
                    objects.append(obj)
        return {"kind": "native_query", "objects": objects}
    ref = REFERENCE.search(expr)
    if ref:
        return {"kind": "reference", "objects": [{"database": None, "schema": None, "name": ref.group(1)}]}
    if re.search(r"\bTable\.FromRows\b|#table\(", expr):
        return {"kind": "embedded", "objects": []}
    if re.search(r"\b(Excel\.Workbook|Csv\.Document|Json\.Document|File\.Contents|SharePoint\.Files)\b", expr):
        # Solo se indica el tipo de archivo: la ruta o la URL no se publican.
        return {"kind": "file", "objects": []}
    return {"kind": None, "objects": []}


def _partition_source(part):
    src = part.get("source", {})
    return join_text(src.get("expression")), src.get("type")


def iter_objects(model):
    """Recorre tablas, columnas, medidas, jerarquías, particiones, relaciones y expresiones compartidas."""
    for obj in _raw_objects(model):
        for key in ("expression", "description", "display_folder", "format_string", "source_column"):
            obj[key] = join_text(obj[key])
        if obj["kind"] in ("measure", "calculated_column"):
            obj["expression"] = strip_dax_comments(obj["expression"])
        yield obj


def _raw_objects(model):
    for t in model.get("tables", []):
        tname = t.get("name")
        yield {"kind": "table", "table": None, "name": tname, "expression": None,
               "data_type": None, "description": t.get("description"), "display_folder": None,
               "format_string": None, "hidden": t.get("isHidden", False), "source_column": None,
               "extra": {"columns": len(t.get("columns", [])), "measures": len(t.get("measures", []))}}

        for c in t.get("columns", []):
            calc = c.get("type") == "calculated"
            yield {"kind": "calculated_column" if calc else "column", "table": tname, "name": c.get("name"),
                   "expression": join_text(c.get("expression")) if calc else None,
                   "data_type": c.get("dataType"), "description": c.get("description"),
                   "display_folder": c.get("displayFolder"), "format_string": c.get("formatString"),
                   "hidden": c.get("isHidden", False), "source_column": c.get("sourceColumn"),
                   "extra": {"is_key": c.get("isKey", False), "summarize_by": c.get("summarizeBy")}}

        for m in t.get("measures", []):
            yield {"kind": "measure", "table": tname, "name": m.get("name"),
                   "expression": join_text(m.get("expression")), "data_type": None,
                   "description": m.get("description"), "display_folder": m.get("displayFolder"),
                   "format_string": m.get("formatString"), "hidden": m.get("isHidden", False),
                   "source_column": None, "extra": {}}

        for h in t.get("hierarchies", []):
            yield {"kind": "hierarchy", "table": tname, "name": h.get("name"), "expression": None,
                   "data_type": None, "description": h.get("description"), "display_folder": h.get("displayFolder"),
                   "format_string": None, "hidden": h.get("isHidden", False), "source_column": None,
                   "extra": {"levels": [lv.get("column") for lv in h.get("levels", [])]}}

        for p in t.get("partitions", []):
            expr, src_type = _partition_source(p)
            yield {"kind": "partition", "table": tname, "name": p.get("name"), "expression": expr,
                   "data_type": None, "description": p.get("description"), "display_folder": None,
                   "format_string": None, "hidden": False, "source_column": None,
                   "extra": {"mode": p.get("mode"), "source_type": src_type}}

    for r in model.get("relationships", []):
        frm = f"{r.get('fromTable')}[{r.get('fromColumn')}]"
        to = f"{r.get('toTable')}[{r.get('toColumn')}]"
        yield {"kind": "relationship", "table": r.get("fromTable"), "name": r.get("name"),
               "expression": f"{frm} -> {to}", "data_type": None, "description": None,
               "display_folder": None, "format_string": None, "hidden": False, "source_column": None,
               "extra": {"to_table": r.get("toTable"), "from_column": r.get("fromColumn"),
                         "to_column": r.get("toColumn"), "cardinality": r.get("fromCardinality"),
                         "to_cardinality": r.get("toCardinality"),
                         "cross_filter": r.get("crossFilteringBehavior"), "active": r.get("isActive", True)}}

    for e in model.get("expressions", []):
        yield {"kind": "shared_expression", "table": None, "name": e.get("name"),
               "expression": join_text(e.get("expression")), "data_type": None,
               "description": e.get("description"), "display_folder": None, "format_string": None,
               "hidden": False, "source_column": None, "extra": {"kind": e.get("kind")}}


def extract_refs(obj):
    """Referencias DAX de un objeto: [(tabla o None, nombre)]. Solo medidas y columnas calculadas."""
    if obj["kind"] not in ("measure", "calculated_column") or not obj["expression"]:
        return []
    text = DAX_COMMENT.sub(" ", DAX_STRING.sub('""', obj["expression"]))
    refs = []
    for m in QUALIFIED.finditer(text):
        table = m.group(1).replace("''", "'") if m.group(1) else m.group(2)
        refs.append((table, m.group(3)))
    rest = QUALIFIED.sub(" ", text)
    for m in BARE.finditer(rest):
        refs.append((None, m.group(1)))
    return refs
