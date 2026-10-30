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


def _partition_source(part):
    src = part.get("source", {})
    return join_text(src.get("expression")), src.get("type")


def iter_objects(model):
    """Recorre tablas, columnas, medidas, jerarquías, particiones, relaciones y expresiones compartidas."""
    for obj in _raw_objects(model):
        for key in ("expression", "description", "display_folder", "format_string", "source_column"):
            obj[key] = join_text(obj[key])
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
