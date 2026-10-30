#!/usr/bin/env python3
"""Normaliza un modelo tabular (Model.bim / TMSL JSON) a un JSON con tablas, columnas,
medidas, relaciones y orígenes de datos.

Uso:
    python extract_model.py <Model.bim> --out model.json

Un modelo remoto (conexión en vivo) no tiene Model.bim local: en ese caso este script
no se ejecuta y el documento final lo indica como pendiente.
"""
import argparse
import json
import sys


def text(value):
    """Las expresiones en BIM pueden venir como lista de líneas o como cadena."""
    if value is None:
        return None
    if isinstance(value, list):
        return "\n".join(value)
    return value


def load_model(path):
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    return data.get("model", data)


def parse_columns(table):
    cols = []
    for c in table.get("columns", []):
        cols.append({
            "name": c.get("name"),
            "data_type": c.get("dataType"),
            "is_calculated": "expression" in c,
            "expression": text(c.get("expression")),
            "source_column": c.get("sourceColumn"),
            "description": c.get("description"),
            "format_string": c.get("formatString"),
            "display_folder": c.get("displayFolder"),
            "is_hidden": c.get("isHidden", False),
            "summarize_by": c.get("summarizeBy"),
        })
    return cols


def parse_measures(table):
    out = []
    for m in table.get("measures", []):
        out.append({
            "table": table.get("name"),
            "name": m.get("name"),
            "expression": text(m.get("expression")),
            "description": m.get("description"),
            "format_string": m.get("formatString"),
            "display_folder": m.get("displayFolder"),
            "is_hidden": m.get("isHidden", False),
        })
    return out


def parse_partitions(table):
    out = []
    for p in table.get("partitions", []):
        src = p.get("source", {})
        out.append({
            "name": p.get("name"),
            "mode": p.get("mode"),
            "source_type": src.get("type"),
            "source_expression": text(src.get("expression")),
        })
    return out


def parse_relationships(model):
    rels = []
    for r in model.get("relationships", []):
        rels.append({
            "name": r.get("name"),
            "from_table": r.get("fromTable"),
            "from_column": r.get("fromColumn"),
            "to_table": r.get("toTable"),
            "to_column": r.get("toColumn"),
            # Valores por defecto del esquema TMSL cuando la propiedad no aparece.
            "from_cardinality": r.get("fromCardinality", "many"),
            "to_cardinality": r.get("toCardinality", "one"),
            "cross_filtering_behavior": r.get("crossFilteringBehavior", "oneDirection"),
            "is_active": r.get("isActive", True),
            "security_filtering_behavior": r.get("securityFilteringBehavior"),
            "from_cardinality_is_default": "fromCardinality" not in r,
            "to_cardinality_is_default": "toCardinality" not in r,
        })
    return rels


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bim", help="Ruta a Model.bim")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    model = load_model(args.bim)
    tables, columns, measures = [], [], []
    for t in model.get("tables", []):
        tables.append({"name": t.get("name"), "is_hidden": t.get("isHidden", False),
                       "description": t.get("description"), "partitions": parse_partitions(t)})
        columns += [dict(c, table=t.get("name")) for c in parse_columns(t)]
        measures += parse_measures(t)
    out = {
        "source": {"type": "bim", "path": args.bim},
        "tables": tables,
        "columns": columns,
        "measures": measures,
        "relationships": parse_relationships(model),
        "data_sources": [{"name": d.get("name"), "type": d.get("type"),
                          "connection_details": d.get("connectionDetails"),
                          "credential_type": (d.get("credential") or {}).get("AuthenticationKind")}
                         for d in model.get("dataSources", [])],
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Tablas: {len(tables)}  Columnas: {len(columns)}  Medidas: {len(measures)}  "
          f"Relaciones: {len(out['relationships'])}  -> {args.out}")


if __name__ == "__main__":
    main()
