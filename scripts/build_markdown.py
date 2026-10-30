#!/usr/bin/env python3
"""Genera el .md de especificación de una página a partir de los JSON de extracción.

Uso:
    python build_markdown.py --report report.json --numbering numbering.json \
        [--model model.json] --out-md "output/Pagina.md" --out-dir output/

Secciones: numeración, visuales por pozo, filtros, Apéndice A (medidas y columnas),
Apéndice B (relaciones), Apéndice C (orígenes de datos), recursos externos.
Las secciones que dependen del modelo indican que falta el Model.bim si no se proporcionó.
Solo se incluye lo que aparece en los visuales numerados; el texto es factual, sin interpretación.
"""
import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime

from redact import add_raw_arg, redact_text

TOKEN = re.compile(r"\[([^\[\]]+)\]")
KIND_NAMES = {"measure": "Medida", "column": "Columna", "hierarchy_level": "Nivel de jerarquía",
              "aggregation": "Agregación", "arithmetic": "Aritmética", "unknown": "Desconocido"}


def esc(value):
    """Escapa barras verticales para tablas Markdown y normaliza saltos de línea."""
    if value is None or value == "":
        return "—"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def field_kind(fi):
    base = fi.get("base_kind") or fi.get("kind")
    return KIND_NAMES.get(fi.get("kind"), fi.get("kind")) + (f" ({KIND_NAMES.get(base, base)})" if fi.get("kind") == "aggregation" else "")


def referenced_fields(visuals):
    """Lista de (tabla, nombre, tipo) de todos los campos usados en los visuales numerados."""
    refs = set()

    def walk(fi):
        if not isinstance(fi, dict):
            return
        if fi.get("kind") in ("column", "measure", "hierarchy_level", "aggregation") and fi.get("entity"):
            kind = fi.get("base_kind", fi.get("kind"))
            refs.add((fi["entity"], fi.get("property"), "measure" if kind == "measure" else "column"))
        for key in ("left", "right"):
            walk(fi.get(key))

    for v in visuals:
        for items in v["wells"].values():
            for fi in items:
                walk(fi)
        for flt in v["filters"]:
            walk(flt["field"])
    return refs


def referenced_measure_names(visuals_fields):
    return {(t, n) for t, n, k in visuals_fields if k == "measure"}


def build_appendix_a(refs, model, ext_measures, used_by):
    """Medidas y columnas calculadas referenciadas, más las medidas que citan en su DAX."""
    rows, seen = [], set()
    measures = {(m["table"], m["name"]): m for m in (model or {}).get("measures", [])}
    by_name = {}
    for m in (model or {}).get("measures", []):
        by_name.setdefault(m["name"], []).append(m)
    columns = {(c["table"], c["name"]): c for c in (model or {}).get("columns", [])}
    ext = {(e["entity"], e["name"]): e for e in ext_measures}

    def add_measure(key, m, origin):
        if key in seen:
            return
        seen.add(key)
        rows.append([key[0], key[1], origin, m.get("description"), m.get("expression"), m.get("format_string"),
                     m.get("display_folder"), "Sí" if m.get("is_hidden") else "No", used_by.get(key, "dependencia")])

    for table_name, name, kind in sorted(refs, key=lambda r: (r[0] or "", r[1] or "")):
        if kind == "measure":
            if (table_name, name) in measures:
                add_measure((table_name, name), measures[(table_name, name)], "Medida del modelo")
            elif (table_name, name) in ext:
                add_measure((table_name, name), ext[(table_name, name)], "Medida de extensión (reporte)")
        else:
            c = columns.get((table_name, name))
            if c and c.get("is_calculated"):
                key = (table_name, name)
                if key not in seen:
                    seen.add(key)
                    rows.append([table_name, name, "Columna calculada", c.get("description"), c.get("expression"),
                                 c.get("format_string"), c.get("display_folder"),
                                 "Sí" if c.get("is_hidden") else "No", used_by.get(key, "")])
    # Dependencias: medidas citadas dentro de las expresiones ya incluidas.
    queue = [r[4] for r in rows if r[4] and r[4] != "—"]
    while queue:
        expr = queue.pop()
        for tok in TOKEN.findall(expr or ""):
            for m in by_name.get(tok, []):
                key = (m["table"], m["name"])
                if key not in seen:
                    add_measure(key, m, "Medida del modelo")
                    queue.append(m.get("expression"))
    return rows


def relationship_activation(rel, model):
    """Medidas cuyo DAX cita ambas columnas de la relación dentro de USERELATIONSHIP o CROSSFILTER."""
    hits = []
    for m in (model or {}).get("measures", []):
        expr = m.get("expression") or ""
        if ("USERELATIONSHIP(" not in expr and "CROSSFILTER(" not in expr):
            continue
        if f"[{rel['from_column']}]" in expr and f"[{rel['to_column']}]" in expr:
            hits.append(f"{m['table']}[{m['name']}]")
    return hits


def build_appendix_b(refs_tables, model):
    if not model:
        return None
    rows = []
    for r in model.get("relationships", []):
        if r["from_table"] not in refs_tables and r["to_table"] not in refs_tables:
            continue
        card = f"{r['from_cardinality']}{' (defecto)' if r['from_cardinality_is_default'] else ''} : " \
               f"{r['to_cardinality']}{' (defecto)' if r['to_cardinality_is_default'] else ''}"
        active = "Sí" if r["is_active"] else "No"
        activated_by = relationship_activation(r, model)
        rows.append([r["name"], f"{r['from_table']}[{r['from_column']}]", f"{r['to_table']}[{r['to_column']}]",
                     card, r["cross_filtering_behavior"], active,
                     ", ".join(activated_by) if activated_by else ("No se activa por medida" if r["is_active"] else "Ninguna medida citada")])
    return rows


def build_appendix_c(refs_tables, model):
    if not model:
        return None
    lines = []
    for ds in model.get("data_sources", []):
        lines.append([ds["name"], ds["type"], json.dumps(ds.get("connection_details"), ensure_ascii=False),
                      ds.get("credential_type")])
    part_rows = []
    for t in model.get("tables", []):
        if t["name"] not in refs_tables:
            continue
        for p in t.get("partitions", []):
            part_rows.append([t["name"], p["name"], p["mode"], p["source_type"], p["source_expression"]])
    return lines, part_rows


def copy_resources(report, numbered, out_dir):
    res_dir = os.path.join(out_dir, "resources")
    if os.path.isdir(res_dir):
        shutil.rmtree(res_dir)
    rows = []
    for v in numbered:
        for ref in v["resource_refs"]:
            base = os.path.basename(ref.replace("\\", "/"))
            dest = None
            src = report["source"]
            if src["type"] == "pbip":
                for root_dir in report.get("resource_dirs", {}).values():
                    for dirpath, _, files in os.walk(root_dir):
                        for fn in files:
                            if fn.lower() == base.lower() and dest is None:
                                os.makedirs(res_dir, exist_ok=True)
                                dest = os.path.join(res_dir, fn)
                                shutil.copy2(os.path.join(dirpath, fn), dest)
            elif src["type"] == "pbix":
                with zipfile.ZipFile(src["path"]) as z:
                    for name in z.namelist():
                        if name.startswith("Report/StaticResources") and os.path.basename(name).lower() == base.lower():
                            os.makedirs(res_dir, exist_ok=True)
                            dest = os.path.join(res_dir, os.path.basename(name))
                            with open(dest, "wb") as f:
                                f.write(z.read(name))
                            break
            rows.append([v["id"][:8], v["visual_type"], ref, os.path.relpath(dest, out_dir).replace("\\", "/") if dest else "No encontrado"])
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True)
    ap.add_argument("--numbering", required=True)
    ap.add_argument("--model", help="model.json de extract_model.py (opcional)")
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-dir", required=True, help="Carpeta output/ (recursos externos)")
    add_raw_arg(ap)
    args = ap.parse_args()

    report = json.load(open(args.report, encoding="utf-8"))
    numbering = json.load(open(args.numbering, encoding="utf-8"))
    model = json.load(open(args.model, encoding="utf-8")) if args.model else None
    page = next(p for p in report["pages"] if p["id"] == numbering["page_id"])
    by_id = {v["id"]: v for v in page["visuals"]}
    drawn_any = {n for c in numbering["captures"] for n in c["drawn_numbers"]}
    visuals = []
    for n in numbering["visuals"]:
        if n["number"] not in drawn_any:
            continue
        v = dict(by_id[n["id"]], number=n["number"])
        if n.get("sub_refs"):
            # Tarjeta múltiple: solo el campo de esta tarjeta.
            v["wells"] = {w: [fi for fi in items_ if fi.get("query_ref") in n["sub_refs"]]
                          for w, items_ in v["wells"].items()}
            v["wells"] = {w: items_ for w, items_ in v["wells"].items() if items_}
        visuals.append(v)

    used_by = {}
    for v in visuals:
        for items in v["wells"].values():
            for fi in items:
                _mark_used(fi, v["number"], used_by)

    refs = referenced_fields(visuals)
    refs_tables = {t for t, _, _ in refs if t}
    ext = report.get("extension_measures", [])
    model_status = "Incluido (" + args.model + ")" if model else (
        f"Modo '{report['model']['mode']}': no hay Model.bim local. Las secciones de modelo están pendientes."
        if report["model"]["mode"] == "byConnection" else
        f"Modo '{report['model']['mode']}': falta el Model.bim. Las secciones de modelo están pendientes.")

    lines = []
    lines.append(f"# {page['name']}: especificación de visuales")
    lines.append("")
    lines.append(f"- Fuente: `{os.path.basename(report['source']['path'])}` ({report['source']['type']})")
    lines.append(f"- Modelo: {model_status}")
    lines.append(f"- Capturas: {', '.join(c['file'] + ' (' + c['scenario'] + ')' for c in numbering['captures'])}")
    lines.append(f"- Generado: {datetime.now():%Y-%m-%d %H:%M}")
    lines.append("")
    lines.append("## 1. Numeración")
    lines.append("")
    lines.append(table(["Nº", "Tipo", "Título", "ID visual", "Capturas"],
                       [[v["number"], v["visual_type"], v["title"] or v.get("text") or "—", v["id"][:8],
                         ", ".join(c["file"] for c in numbering["captures"] if v["number"] in c["drawn_numbers"])]
                        for v in visuals]))
    lines.append("")
    lines.append("## 2. Visuales y pozos de campos")
    for v in visuals:
        lines.append("")
        lines.append(f"### Nº {v['number']}: {v['visual_type']}" + (f" · {v['title']}" if v["title"] else ""))
        lines.append("")
        rows = []
        for well, items in v["wells"].items():
            for fi in items:
                rows.append([well, fi.get("label"), field_kind(fi), fi.get("display_name") or "—",
                             fi.get("property") if fi.get("kind") != "arithmetic" else "—"])
        lines.append(table(["Pozo", "Campo", "Tipo", "Nombre visible", "Propiedad"], rows))
        if v["filters"]:
            lines.append("")
            lines.append("Filtros del visual:")
            lines.append("")
            lines.append(table(["Campo", "Tipo", "Condición", "Origen"],
                               [[f["field_label"], f["type"], "; ".join(f["conditions"]) or "—", f["how_created"]]
                                for f in v["filters"]]))
    if page["filters"] or report["report_filters"]:
        lines.append("")
        lines.append("## 3. Filtros de página e informe")
        lines.append("")
        lines.append(table(["Ámbito", "Campo", "Tipo", "Condición"],
                           [["Página"] + [f["field_label"], f["type"], "; ".join(f["conditions"]) or "—"] for f in page["filters"]]
                           + [["Informe"] + [f["field_label"], f["type"], "; ".join(f["conditions"]) or "—"] for f in report["report_filters"]]))

    lines.append("")
    lines.append("## 4. Escenarios y superposiciones")
    lines.append("")
    lines.append("Estado guardado (Default) y cada bookmark que afecta a esta página. Los números son los de la sección 1; "
                 "«muestra» y «oculta» se comparan contra el estado guardado.")
    for name, sc in numbering.get("scenarios", {}).items():
        caps = [c["file"] for c in numbering["captures"] if c["scenario"] == name]
        title = f"### {name}" + (" (bookmark)" if sc["bookmark"] else " (estado guardado)")
        lines.append("")
        lines.append(title)
        lines.append("")
        lines.append(f"- Capturas: {', '.join(caps) if caps else 'ninguna'}")
        lines.append(f"- Visuales visibles (Nº): {', '.join(map(str, sc['visible_numbers'])) or '—'}")
        if sc["bookmark"]:
            lines.append(f"- Muestra (Nº): {', '.join(map(str, sc['shows'])) or '—'}")
            lines.append(f"- Oculta (Nº): {', '.join(map(str, sc['hides'])) or '—'}")
        if sc["other_changes"]:
            others = "; ".join(f"{o['visual_type']}" + (f" · {o['title']}" if o["title"] else "") for o in sc["other_changes"])
            lines.append(f"- Cambios en visuales sin numeración: {others}")
        if sc["covered"]:
            lines.append("")
            lines.append(table(["Nº", "Badge tapado por"],
                               [[c["number"], "; ".join(f"{b['visual_type']}" + (f" · {b['title']}" if b["title"] else "")
                                                       for b in c["covered_by"])] for c in sc["covered"]]))
        else:
            lines.append("- Superposiciones: ningún badge queda tapado por otro visual.")

    lines.append("")
    lines.append("## Apéndice A. Medidas y columnas calculadas")
    lines.append("")
    if model:
        rows = build_appendix_a(refs, model, ext, used_by)
        lines.append(table(["Tabla", "Nombre", "Origen", "Descripción", "DAX", "Formato", "Carpeta", "Oculta", "Usada por"], rows)
                     if rows else "No hay medidas ni columnas calculadas en los visuales numerados.")
    else:
        lines.append("Requiere definición del modelo (Model.bim). No se puede completar esta sección.")
        ext_rows = [[e["entity"], e["name"], "Medida de extensión (reporte)", e.get("description"), e.get("expression"),
                     e.get("format_string"), e.get("display_folder"), "No", used_by.get((e["entity"], e["name"]), "")]
                    for e in ext if (e["entity"], e["name"]) in {(t, n) for t, n, k in refs if k == "measure"}]
        if ext_rows:
            lines.append("")
            lines.append("Medidas de extensión del reporte, incluidas porque están en el propio archivo:")
            lines.append("")
            lines.append(table(["Tabla", "Nombre", "Origen", "Descripción", "DAX", "Formato", "Carpeta", "Oculta", "Usada por"], ext_rows))

    lines.append("")
    lines.append("## Apéndice B. Relaciones")
    lines.append("")
    rel_rows = build_appendix_b(refs_tables, model)
    if rel_rows is None:
        lines.append("Requiere definición del modelo (Model.bim). No se puede completar esta sección.")
    elif rel_rows:
        lines.append(table(["Nombre", "Desde", "Hasta", "Cardinalidad (desde : hasta)", "Filtro cruzado", "Activa", "Activada por medida"], rel_rows))
    else:
        lines.append("No hay relaciones que involucren las tablas de los visuales numerados.")

    lines.append("")
    lines.append("## Apéndice C. Orígenes de datos")
    lines.append("")
    src = build_appendix_c(refs_tables, model)
    if src is None:
        lines.append("Requiere definición del modelo (Model.bim). No se puede completar esta sección.")
    else:
        ds_rows, part_rows = src
        lines.append(table(["Origen", "Tipo", "Detalles de conexión", "Autenticación"], ds_rows) if ds_rows else "El modelo no define orígenes de datos.")
        if part_rows:
            lines.append("")
            lines.append(table(["Tabla", "Partición", "Modo", "Tipo de origen", "Expresión de origen"], part_rows))

    lines.append("")
    lines.append("## Recursos externos")
    lines.append("")
    os.makedirs(args.out_dir, exist_ok=True)
    captured_ids = {i for c in numbering["captures"] for i in c["visuals_in_capture"]}
    captured = [v for v in page["visuals"] if v["id"] in captured_ids]
    res_rows = copy_resources(report, captured, args.out_dir)
    lines.append(table(["ID visual", "Tipo", "Referencia en el visual", "Archivo en output/"], res_rows) if res_rows
                 else "No hay recursos externos en los visuales numerados.")
    lines.append("")

    os.makedirs(os.path.dirname(os.path.abspath(args.out_md)), exist_ok=True)
    text = "\n".join(lines)
    if not args.raw:
        text = redact_text(text)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Markdown: {args.out_md}  ({len(visuals)} visuales)")


def _mark_used(fi, number, used_by):
    if not isinstance(fi, dict):
        return
    if fi.get("entity") and fi.get("property"):
        key = (fi["entity"], fi["property"])
        nums = set(filter(None, used_by.get(key, "").split(", "))) | {str(number)}
        used_by[key] = ", ".join(sorted(nums, key=int))
    for k in ("left", "right"):
        _mark_used(fi.get(k), number, used_by)


if __name__ == "__main__":
    main()
