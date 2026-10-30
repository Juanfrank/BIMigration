#!/usr/bin/env python3
"""Lee la definición de un reporte Power BI (.pbip o .pbix) y la vuelca a un JSON normalizado.

Uso:
    python extract_report.py <archivo.pbip | archivo.pbix> --out report.json

El JSON resultante contiene páginas, visuales (con sus pozos de campos), filtros
(de visual, página e informe), medidas de extensión del reporte y recursos externos.
No interpreta nada: solo traduce la estructura guardada por Power BI.
"""
import argparse
import json
import os
import sys
import zipfile

from redact import add_raw_arg, redact_value

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".bmp", ".emf", ".wmf", ".webp")


def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def load_json_text(text):
    return json.loads(text) if isinstance(text, str) else text


# ---------------------------------------------------------------- campos ----

def field_info(f):
    """Convierte un campo de projection / Select / filtro en un dict plano."""
    if not isinstance(f, dict):
        return {"kind": "unknown", "raw": str(f)[:200]}
    if "ScopedEval" in f:
        inner = field_info(f["ScopedEval"]["Expression"])
        inner["scoped_eval"] = True
        return inner
    if "Column" in f or "Measure" in f:
        kind = "column" if "Column" in f else "measure"
        body = f["Column"] if kind == "column" else f["Measure"]
        src = body["Expression"].get("SourceRef", {})
        return {"kind": kind, "entity": src.get("Entity"), "source_alias": src.get("Source"),
                "property": body.get("Property")}
    if "HierarchyLevel" in f:
        h = f["HierarchyLevel"]
        hier = h["Expression"]["Hierarchy"]
        src = hier["Expression"]["SourceRef"]
        return {"kind": "hierarchy_level", "entity": src.get("Entity"), "source_alias": src.get("Source"),
                "hierarchy": hier.get("Hierarchy"), "property": h.get("Level")}
    if "Aggregation" in f:
        a = f["Aggregation"]
        inner = field_info(a["Expression"])
        inner["aggregation_function"] = a.get("Function")
        inner["base_kind"] = inner.get("kind")
        inner["kind"] = "aggregation"
        return inner
    if "Arithmetic" in f:
        a = f["Arithmetic"]
        return {"kind": "arithmetic", "operator": a.get("Operator"),
                "left": field_info(a.get("Left")), "right": field_info(a.get("Right"))}
    return {"kind": "unknown", "raw": json.dumps(f, ensure_ascii=False)[:200]}


def remap_aliases(fi, alias_map):
    """En pbix, las entidades se referencian por alias de FROM; las traduce a nombre de tabla."""
    if not isinstance(fi, dict):
        return fi
    if fi.get("source_alias") in alias_map:
        fi["entity"] = alias_map[fi["source_alias"]]
    for key in ("left", "right"):
        if key in fi:
            remap_aliases(fi[key], alias_map)
    return fi


def expr_text(e, alias_map=None):
    """Texto legible y sin interpretar de una expresión de filtro."""
    alias_map = alias_map or {}
    if isinstance(e, list):
        return "[" + ", ".join(expr_text(x, alias_map) for x in e) + "]"
    if not isinstance(e, dict):
        return str(e)
    if "Literal" in e:
        return str(e["Literal"].get("Value"))
    if "Now" in e:
        return "Now()"
    if "DateAdd" in e:
        d = e["DateAdd"]
        return f"DateAdd({expr_text(d['Expression'], alias_map)}, {d.get('Amount')}, unidad={d.get('TimeUnit')})"
    if "DateSpan" in e:
        d = e["DateSpan"]
        return f"DateSpan({expr_text(d['Expression'], alias_map)}, unidad={d.get('TimeUnit')})"
    if "Column" in e or "Measure" in e or "HierarchyLevel" in e or "Aggregation" in e or "Arithmetic" in e:
        fi = remap_aliases(field_info(e), alias_map)
        return label(fi)
    return json.dumps(e, ensure_ascii=False)[:160]


def condition_text(c, alias_map=None):
    alias_map = alias_map or {}
    if not isinstance(c, dict):
        return str(c)
    if "Not" in c:
        return "NOT (" + condition_text(c["Not"]["Expression"], alias_map) + ")"
    if "In" in c:
        vals = c["In"].get("Values", [])
        flat = [expr_text(v[0], alias_map) if isinstance(v, list) and v else expr_text(v, alias_map) for v in vals]
        return "IN " + ", ".join(flat)
    if "Comparison" in c:
        cmp_ = c["Comparison"]
        return f"Comparison(kind={cmp_.get('ComparisonKind')}) {expr_text(cmp_.get('Left'), alias_map)} ? {expr_text(cmp_.get('Right'), alias_map)}"
    if "Between" in c:
        b = c["Between"]
        return f"BETWEEN {expr_text(b.get('LowerBound'), alias_map)} Y {expr_text(b.get('UpperBound'), alias_map)}"
    if "Contains" in c:
        k = c["Contains"]
        return f"CONTAINS {expr_text(k.get('Right'), alias_map)}"
    if "StartsWith" in c:
        k = c["StartsWith"]
        return f"STARTSWITH {expr_text(k.get('Right'), alias_map)}"
    return json.dumps(c, ensure_ascii=False)[:200]


def label(fi):
    """Nombre legible de un campo: Tabla.Propiedad, Tabla[Jerarquía].Nivel, Agg(...), (A op B)."""
    if not isinstance(fi, dict):
        return str(fi)
    k = fi.get("kind")
    if k in ("column", "measure"):
        return f"{fi.get('entity')}.{fi.get('property')}"
    if k == "hierarchy_level":
        return f"{fi.get('entity')}[{fi.get('hierarchy')}].{fi.get('property')}"
    if k == "aggregation":
        return f"AGG{fi.get('aggregation_function')}({fi.get('entity')}.{fi.get('property')})"
    if k == "arithmetic":
        return f"({label(fi.get('left'))} op{fi.get('operator')} {label(fi.get('right'))})"
    return fi.get("raw", "?")


def parse_filter(f):
    field = f.get("field") or f.get("expression") or {}
    flt = f.get("filter") or {}
    alias_map = {x.get("Name"): x.get("Entity") for x in flt.get("From", [])}
    where = flt.get("Where") or []
    conditions = [condition_text(w.get("Condition", {}), alias_map) for w in where if "Condition" in w]
    return {
        "name": f.get("name"),
        "type": f.get("type"),
        "field": field_info(field),
        "field_label": label(field_info(field)),
        "how_created": f.get("howCreated"),
        "is_locked": f.get("isLockedInViewMode", False),
        "is_hidden": f.get("isHiddenInViewMode", False),
        "conditions": conditions,
    }


def parse_filters(raw):
    raw = load_json_text(raw) if raw else []
    return [parse_filter(f) for f in raw or []]


# ----------------------------------------------------------- resources ----

def find_resource_refs(obj, found=None):
    """Busca en cualquier valor de texto del visual referencias a imágenes o recursos."""
    found = set() if found is None else found
    if isinstance(obj, dict):
        if "ItemName" in obj:
            found.add(str(obj["ItemName"]))
        for v in obj.values():
            find_resource_refs(v, found)
    elif isinstance(obj, list):
        for v in obj:
            find_resource_refs(v, found)
    elif isinstance(obj, str):
        low = obj.lower()
        if low.endswith(IMAGE_EXT):
            found.add(obj)
    return found


def visual_title(v):
    try:
        t = v["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"]
        return t.strip("'")
    except (KeyError, IndexError, TypeError):
        return ""


def textbox_text(v):
    try:
        paras = v["objects"]["general"][0]["properties"]["paragraphs"]
        return " | ".join("".join(r.get("value", "") for r in p.get("textRuns", [])) for p in paras)
    except (KeyError, IndexError, TypeError):
        return ""


def new_visual(vid, visual_type, x, y, w, h, z, parent, hidden, title, text, wells, filters, resources, raw_objects_keys):
    return {
        "id": vid, "visual_type": visual_type, "x": x, "y": y, "width": w, "height": h, "z": z,
        "parent_group": parent, "is_hidden": hidden, "title": title, "text": text,
        "wells": wells, "filters": filters, "resource_refs": sorted(resources),
        "object_keys": raw_objects_keys,
    }


# --------------------------------------------------------------- PBIP ----

def find_report_folder(pbip_path):
    data = load_json(pbip_path)
    base = os.path.dirname(os.path.abspath(pbip_path))
    for art in data.get("artifacts", []):
        rep = art.get("report", {}).get("path")
        if rep:
            return os.path.join(base, rep)
    raise SystemExit("No se encontró la carpeta .Report en el archivo .pbip")


def parse_pbip(pbip_path):
    report_folder = find_report_folder(pbip_path)
    definition = os.path.join(report_folder, "definition")
    pbir = load_json(os.path.join(report_folder, "definition.pbir"))
    dataset = pbir.get("datasetReference", {})
    if "byConnection" in dataset:
        model = {"mode": "byConnection", "connection": dataset["byConnection"].get("connectionString")}
    elif "byPath" in dataset:
        model = {"mode": "byPath", "path": dataset["byPath"].get("path")}
    else:
        model = {"mode": "none"}
    sm_dirs = [d for d in os.listdir(os.path.dirname(report_folder))
               if d.endswith(".SemanticModel") and os.path.isdir(os.path.join(os.path.dirname(report_folder), d))]
    if sm_dirs:
        model["semantic_model_folder"] = sm_dirs[0]

    pages_meta = load_json(os.path.join(definition, "pages", "pages.json"))
    order = pages_meta.get("pageOrder", [])
    bookmarks = parse_bookmarks(definition)
    pages = []
    for pid in order:
        pdir = os.path.join(definition, "pages", pid)
        page = load_json(os.path.join(pdir, "page.json"))
        visuals = []
        vroot = os.path.join(pdir, "visuals")
        if os.path.isdir(vroot):
            for vid in os.listdir(vroot):
                vj = os.path.join(vroot, vid, "visual.json")
                if os.path.exists(vj):
                    visuals.append(parse_pbip_visual(load_json(vj), vid))
        pages.append({
            "id": pid, "name": page.get("displayName"), "width": page.get("width"), "height": page.get("height"),
            "filters": parse_filters(page.get("filterConfig", {}).get("filters")),
            "visuals": visuals,
            "bookmarks": [b for b in bookmarks if b["page_id"] == pid],
        })
    report_json = load_json(os.path.join(definition, "report.json"))
    ext = []
    ext_path = os.path.join(definition, "reportExtensions.json")
    if os.path.exists(ext_path):
        for e in load_json(ext_path).get("entities", []):
            for m in e.get("measures", []):
                ext.append({"entity": e.get("name"), "name": m.get("name"), "expression": m.get("expression"),
                            "format_string": m.get("formatString"), "display_folder": m.get("displayFolder"),
                            "description": m.get("description"), "data_type": m.get("dataType")})
    return {
        "source": {"type": "pbip", "path": os.path.abspath(pbip_path), "report_folder": report_folder},
        "model": model,
        "report_filters": parse_filters(report_json.get("filterConfig", {}).get("filters")),
        "extension_measures": ext,
        "pages": pages,
        "resource_dirs": {
            "registered": os.path.join(report_folder, "StaticResources", "RegisteredResources"),
            "shared": os.path.join(report_folder, "StaticResources", "SharedResources"),
        },
    }


def flatten_group_states(nodes, out):
    """Aplana el árbol visualContainerGroups de un bookmark a {id: oculto}."""
    for gid, node in (nodes or {}).items():
        if "isHidden" in node:
            out[gid] = node["isHidden"]
        flatten_group_states(node.get("children"), out)
    return out


def parse_bookmarks(definition):
    """Bookmarks del informe: por cada página que afectan, qué visuales y grupos fijan ocultos o visibles.

    El estado por defecto de la página no está aquí: es el de visual.json y page.json.
    """
    bdir = os.path.join(definition, "bookmarks")
    index_path = os.path.join(bdir, "bookmarks.json")
    if not os.path.exists(index_path):
        return []
    result = []
    for item in load_json(index_path).get("items", []):
        path = os.path.join(bdir, f"{item['name']}.bookmark.json")
        if not os.path.exists(path):
            continue
        bm = load_json(path)
        opts = bm.get("options", {})
        targets = opts.get("targetVisualNames") if opts.get("applyOnlyToTargetVisuals") else None
        for pid, sec in bm.get("explorationState", {}).get("sections", {}).items():
            overrides = flatten_group_states(sec.get("visualContainerGroups"), {})
            for vid, vc in sec.get("visualContainers", {}).items():
                display = vc.get("singleVisual", {}).get("display") or vc.get("display") or {}
                if display.get("mode") in ("hidden", "visible"):
                    overrides[vid] = display["mode"] == "hidden"
            result.append({"name": item["name"], "display_name": bm.get("displayName") or item["name"],
                           "page_id": pid, "targets": targets, "overrides": overrides})
    return result


def parse_pbip_visual(vj, vid):
    v = vj.get("visual", {})
    pos = vj.get("position", {})
    wells = {}
    for well, wv in v.get("query", {}).get("queryState", {}).items():
        items = []
        for p in wv.get("projections", []):
            fi = field_info(p.get("field"))
            fi["query_ref"] = p.get("queryRef")
            fi["display_name"] = p.get("displayName")
            fi["label"] = label(fi)
            items.append(fi)
        if items:
            wells[well] = items
    res = find_resource_refs(v.get("objects", {}))
    return new_visual(
        vid, v.get("visualType"), pos.get("x", 0), pos.get("y", 0), pos.get("width", 0), pos.get("height", 0),
        pos.get("z"), vj.get("parentGroupName"), vj.get("isHidden", False), visual_title(v),
        textbox_text(v) if v.get("visualType") == "textbox" else "", wells,
        parse_filters(vj.get("filterConfig", {}).get("filters")), res, sorted(v.get("objects", {}).keys()))


# --------------------------------------------------------------- PBIX ----

def read_layout(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        if "Report/Layout" not in z.namelist():
            raise SystemExit("El .pbix no contiene Report/Layout (¿formato PBIR nuevo? use la carpeta .pbip)")
        raw = z.read("Report/Layout")
    for enc in ("utf-16", "utf-8-sig"):
        try:
            return json.loads(raw.decode(enc))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    raise SystemExit("No se pudo decodificar Report/Layout")


def parse_pbix(pbix_path):
    layout = read_layout(pbix_path)
    with zipfile.ZipFile(pbix_path) as z:
        has_model = "DataModel" in z.namelist()
    pages = []
    for i, sec in enumerate(layout.get("sections", [])):
        visuals = []
        for j, vc in enumerate(sec.get("visualContainers", [])):
            cfg = load_json_text(vc.get("config")) or {}
            sv = cfg.get("singleVisual", {})
            proto = sv.get("prototypeQuery", {})
            alias_map = {f.get("Name"): f.get("Entity") for f in proto.get("From", [])}
            select_map = {}
            for item in proto.get("Select", []):
                select_map[item.get("Name")] = remap_aliases(field_info(item), alias_map)
            wells = {}
            for well, items in (sv.get("projections") or {}).items():
                out = []
                for p in items:
                    fi = dict(select_map.get(p.get("queryRef"), {"kind": "unknown", "raw": p.get("queryRef")}))
                    fi["query_ref"] = p.get("queryRef")
                    fi["label"] = label(fi)
                    out.append(fi)
                if out:
                    wells[well] = out
            vobj = sv.get("vcObjects", {}) or sv.get("objects", {})
            title = ""
            try:
                title = vobj["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"].strip("'")
            except (KeyError, IndexError, TypeError):
                pass
            text = ""
            if sv.get("visualType") == "textbox":
                text = textbox_text({"objects": sv.get("objects", {})})
            res = find_resource_refs(sv.get("objects", {}))
            visuals.append(new_visual(
                f"{i}-{j}-{cfg.get('name', '')}", sv.get("visualType"), vc.get("x", 0), vc.get("y", 0),
                vc.get("width", 0), vc.get("height", 0), vc.get("z"), None, False, title, text, wells,
                parse_filters(vc.get("filters")), res, sorted(sv.get("objects", {}).keys())))
        pages.append({
            "id": str(i), "name": sec.get("displayName"), "width": sec.get("width"), "height": sec.get("height"),
            "filters": parse_filters(sec.get("filters")), "visuals": visuals,
        })
    return {
        "source": {"type": "pbix", "path": os.path.abspath(pbix_path)},
        "model": {"mode": "embedded" if has_model else "none",
                  "note": "El modelo va embebido en DataModel; extráigalo con pbi-tools para obtener Model.bim"},
        "report_filters": parse_filters(layout.get("filters")),
        "extension_measures": [],
        "pages": pages,
        "resource_dirs": {},
    }


# ---------------------------------------------------------------- main ----

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="Archivo .pbip o .pbix")
    ap.add_argument("--out", required=True, help="JSON de salida")
    add_raw_arg(ap)
    args = ap.parse_args()
    ext = os.path.splitext(args.source)[1].lower()
    if ext == ".pbip":
        data = parse_pbip(args.source)
    elif ext == ".pbix":
        data = parse_pbix(args.source)
    else:
        sys.exit("Extensión no soportada: use .pbip o .pbix")
    if not args.raw:
        data = redact_value(data)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Páginas: {len(data['pages'])}  ->  {args.out}")
    for p in data["pages"]:
        n = sum(1 for v in p["visuals"] if v["wells"])
        print(f"  - {p['name']}: {len(p['visuals'])} visuales, {n} con campos")


if __name__ == "__main__":
    main()
