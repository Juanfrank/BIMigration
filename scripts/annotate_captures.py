#!/usr/bin/env python3
"""Numera los visuales de una página de Power BI y dibuja la numeración sobre capturas.

Uso:
    python annotate_captures.py --report report.json --page "Nombre de página" \
        --capture captura1.png [captura2.png ...] \
        [--scenario "captura1.png=Default" "captura2.png=MenuA" ...] \
        --out-dir output/ --numbering-out datos/numbering.json \
        [--anchor "ID_VISUAL=px,py" ...]

Escenarios:
  - "Default" es el estado guardado de la página.
  - Cada bookmark del reporte que afecta a la página es un escenario, con su displayName.
  - Cada captura declara su escenario con --scenario (por nombre de archivo); sin declarar, es "Default".

Reglas de numeración (fijas, independientes de las capturas):
  - Solo visuales con al menos un campo (medida o columna) en algún pozo.
  - Se omiten formas, textos, imágenes y grupos.
  - Un visual cuenta como oculto en un escenario si él o cualquier grupo padre está oculto en ese escenario.
  - La numeración es única para la página: cubre los visuales visibles en algún escenario usado por las
    capturas, así que un mismo visual conserva su número entre capturas.
  - Orden de lectura: por banda de altura (30 px) y luego de izquierda a derecha.
  - La posición absoluta suma la posición de toda la cadena de grupos padre.

Superposiciones:
  - Un badge queda tapado si, en el escenario de su captura, un visual de mayor z cubre su esquina superior izquierda.
  - Se reporta por escenario en numbering.json y en el .md.

Calibración captura <-> página:
  - Con dos o más --anchor (ID del visual y píxel de su esquina superior izquierda en la captura) se ajusta
    una transformación lineal por eje.
  - Sin anclas se usa la escala ancho_captura / ancho_página, sin desplazamiento. Es aproximado.

Salida por captura:
  - "<captura> - numerada.png": badges de los visuales visibles en su escenario.
  - "<captura> - contornos.png": contornos de todos los visuales visibles en su escenario, para comparar
    con la captura real y detectar superposiciones o escenarios que no coinciden.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from redact import add_raw_arg, redact_value

BADGE_FONT_PATHS = ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
GROUP_TYPES = {None, "group", "visualGroup"}
# Tarjetas con varios campos: cada campo es una tarjeta con su propio número.
MULTI_CARD_TYPES = {"card", "cardVisual", "multiRowCard"}
DEFAULT_SCENARIO = "Default"


def pick_font(size=12):
    for path in BADGE_FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def find_page(report, name):
    pages = report["pages"]
    if name is None:
        names = "\n".join(f"  - {p['name']}" for p in pages)
        raise SystemExit(f"Falta --page. Páginas disponibles:\n{names}")
    for p in pages:
        if p["name"] == name or p["id"] == name:
            return p
    matches = [p for p in pages if p["name"] and p["name"].lower() == name.lower()]
    if matches:
        return matches[0]
    raise SystemExit(f"No existe la página '{name}'")


# ----------------------------------------------------------- escenarios ----

def scenarios_of(page):
    """{nombre: escenario}: 'Default' y un escenario por cada bookmark de la página."""
    scen = {DEFAULT_SCENARIO: {"display_name": DEFAULT_SCENARIO, "overrides": {}, "targets": None}}
    for bm in page.get("bookmarks", []):
        scen[bm["display_name"]] = bm
    return scen


def effectively_hidden(vid, own, parents):
    """Oculto si el visual o cualquiera de sus grupos padre está oculto (own: {id: oculto})."""
    seen = set()
    while vid is not None and vid not in seen:
        if own.get(vid):
            return True
        seen.add(vid)
        vid = parents.get(vid)
    return False


def hidden_in(page, scenario):
    """Visibilidad efectiva de cada visual en un escenario, aplicando los overrides del bookmark."""
    own = {v["id"]: v["is_hidden"] for v in page["visuals"]}
    targets = scenario.get("targets")
    for vid, hidden in scenario.get("overrides", {}).items():
        if vid in own and (targets is None or vid in targets):
            own[vid] = hidden
    parents = {v["id"]: v.get("parent_group") for v in page["visuals"]}
    return {vid: effectively_hidden(vid, own, parents) for vid in own}


# ----------------------------------------------------------- posiciones ----

def absolute_items(page):
    """Visuales con coordenadas absolutas (suma de toda la cadena de grupos padre)."""
    by_id = {v["id"]: v for v in page["visuals"]}
    items = []
    for v in page["visuals"]:
        x, y = v["x"], v["y"]
        pid, seen = v.get("parent_group"), set()
        while pid in by_id and pid not in seen:
            seen.add(pid)
            parent = by_id[pid]
            x += parent["x"]
            y += parent["y"]
            pid = parent.get("parent_group")
        items.append(dict(v, abs_x=x, abs_y=y))
    return items


def is_numberable(v):
    return bool(v["wells"]) and v["visual_type"] not in GROUP_TYPES


def expand_multi_cards(visuals):
    """Cada campo de una tarjeta múltiple ocupa una porción igual del ancho del visual."""
    items = []
    for v in visuals:
        if not is_numberable(v):
            continue
        refs = [fi["query_ref"] for items_ in v["wells"].values() for fi in items_ if fi.get("query_ref")]
        if v["visual_type"] in MULTI_CARD_TYPES and len(refs) > 1:
            w = v["width"] / len(refs)
            for i, ref in enumerate(refs):
                items.append(dict(v, abs_x=v["abs_x"] + i * w, width=w, sub_refs=[ref]))
        else:
            items.append(dict(v, sub_refs=None))
    return items


def number_visuals(visuals):
    cands = expand_multi_cards(visuals)
    cands.sort(key=lambda v: (round(v["abs_y"] / 30), v["abs_x"]))
    for n, v in enumerate(cands, start=1):
        v["number"] = n
    return cands


def parse_anchors(raw, visuals):
    anchors = []
    for item in raw or []:
        vid, coords = item.split("=")
        px, py = (float(c) for c in coords.split(","))
        matches = [v for v in visuals if v["id"].startswith(vid)]
        if not matches:
            raise SystemExit(f"Ancla: no existe un visual que empiece por '{vid}'")
        anchors.append((matches[0], px, py))
    return anchors


def fit_axis(pairs, default_scale, default_offset=0.0):
    """pairs: [(coord_pagina, coord_captura)] -> (escala, desplazamiento) por mínimos cuadrados."""
    if len(pairs) < 2:
        return default_scale, default_offset
    us = [u for u, _ in pairs]
    ps = [p for _, p in pairs]
    mu, mp = sum(us) / len(us), sum(ps) / len(ps)
    var = sum((u - mu) ** 2 for u in us)
    if var == 0:
        return default_scale, default_offset
    a = sum((u - mu) * (p - mp) for u, p in pairs) / var
    return a, mp - a * mu


def build_transform(anchors, page, img_w, img_h):
    page_w = page.get("width") or img_w
    default_sx = img_w / page_w
    if not anchors:
        return {"mode": "automatica", "sx": default_sx, "bx": 0.0, "sy": default_sx, "by": 0.0}
    sx, bx = fit_axis([(v["abs_x"], px) for v, px, _ in anchors], default_sx)
    sy, by = fit_axis([(v["abs_y"], py) for v, _, py in anchors], default_sx)
    return {"mode": f"calibrada ({len(anchors)} anclas)", "sx": sx, "bx": bx, "sy": sy, "by": by}


# ---------------------------------------------------------- superposición ----

def contains(v, x, y):
    return v["abs_x"] <= x < v["abs_x"] + v["width"] and v["abs_y"] <= y < v["abs_y"] + v["height"]


def covering_visuals(badge, visible_items):
    """Visuales visibles de mayor z que cubren la esquina superior izquierda del badge."""
    px, py = badge["abs_x"] + 1, badge["abs_y"] + 1
    return [v for v in visible_items
            if v["id"] != badge["id"] and (v.get("z") or 0) > (badge.get("z") or 0) and contains(v, px, py)]


def describe(v):
    return {"id": v["id"][:8], "visual_type": v["visual_type"], "title": v["title"] or v.get("text") or None}


# ------------------------------------------------------------- dibujo ----

def draw_badge(draw, font, x, y, text):
    w = 10 + 7 * len(text)
    h = 18
    x0, y0 = x - 2, y - 2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=5, fill=(220, 20, 20), outline=(255, 255, 255))
    draw.text((x0 + w / 2, y0 + h / 2), text, font=font, fill=(255, 255, 255), anchor="mm")


def to_capture(t, x, y):
    return t["sx"] * x + t["bx"], t["sy"] * y + t["by"]


def draw_outlines(img, t, visible_items):
    draw = ImageDraw.Draw(img)
    for v in visible_items:
        x0, y0 = to_capture(t, v["abs_x"], v["abs_y"])
        x1, y1 = to_capture(t, v["abs_x"] + v["width"], v["abs_y"] + v["height"])
        draw.rectangle([x0, y0, x1, y1], outline=(0, 200, 255), width=2)


# -------------------------------------------------------------- main ----

def parse_scenario_args(raw, scen_all):
    assign = {}
    for item in raw or []:
        cap, sep, name = item.rpartition("=")
        if not sep:
            raise SystemExit(f"--scenario debe ser 'captura=escenario': {item}")
        if name not in scen_all:
            raise SystemExit(f"No existe el escenario '{name}'. Disponibles: {', '.join(scen_all)}")
        assign[os.path.basename(cap)] = name
    return assign


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True, help="report.json de extract_report.py")
    ap.add_argument("--page", help="Nombre (o id) de la página")
    ap.add_argument("--capture", nargs="+", required=True, help="Capturas de la página")
    ap.add_argument("--scenario", action="append", help="captura=escenario (repetible; por defecto, Default)")
    ap.add_argument("--anchor", action="append", help="ID_VISUAL=px,py (repetible, mínimo 2 para calibrar)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--numbering-out", required=True, help="JSON con la numeración de la página")
    add_raw_arg(ap)
    args = ap.parse_args()

    with open(args.report, encoding="utf-8") as f:
        report = json.load(f)
    page = find_page(report, args.page)
    scen_all = scenarios_of(page)
    assign = parse_scenario_args(args.scenario, scen_all)
    cap_scen = {cap: assign.get(os.path.basename(cap), DEFAULT_SCENARIO) for cap in args.capture}
    used = list(dict.fromkeys(cap_scen.values()))
    shown = list(dict.fromkeys([DEFAULT_SCENARIO] + used))

    hidden = {name: hidden_in(page, scen_all[name]) for name in shown}
    union_hidden = {vid: all(hidden[s][vid] for s in used) for vid in hidden[DEFAULT_SCENARIO]}
    items = absolute_items(page)
    numbered = number_visuals([v for v in items if not union_hidden[v["id"]]])
    anchors = parse_anchors(args.anchor, items)

    os.makedirs(args.out_dir, exist_ok=True)
    font = pick_font(12)
    numbering = {"page": page["name"], "page_id": page["id"], "page_size": [page.get("width"), page.get("height")],
                 "visuals": [], "scenarios": {}, "captures": []}
    for v in numbered:
        numbering["visuals"].append({
            "number": v["number"], "id": v["id"], "visual_type": v["visual_type"], "title": v["title"],
            "abs_x": v["abs_x"], "abs_y": v["abs_y"], "width": v["width"], "height": v["height"],
            "parent_group": v["parent_group"], "sub_refs": v["sub_refs"],
        })

    default_numbers = {c["number"] for c in numbered if not hidden[DEFAULT_SCENARIO][c["id"]]}
    for name in shown:
        vis_s = [v for v in items if not hidden[name][v["id"]] and v["visual_type"] not in GROUP_TYPES]
        numbers = {c["number"] for c in numbered if not hidden[name][c["id"]]}
        covered = []
        for c in numbered:
            if hidden[name][c["id"]]:
                continue
            above = covering_visuals(c, vis_s)
            if above:
                covered.append({"number": c["number"], "covered_by": [describe(v) for v in above]})
        others = [v for v in items if v["visual_type"] not in GROUP_TYPES and not is_numberable(v)
                  and hidden[name][v["id"]] != hidden[DEFAULT_SCENARIO][v["id"]]]
        numbering["scenarios"][name] = {
            "bookmark": None if name == DEFAULT_SCENARIO else scen_all[name]["name"],
            "visible_numbers": sorted(numbers),
            "shows": sorted(numbers - default_numbers),
            "hides": sorted(default_numbers - numbers),
            "covered": covered,
            "other_changes": [describe(v) for v in others],
        }

    for cap in args.capture:
        name = cap_scen[cap]
        img = Image.open(cap).convert("RGB")
        t = build_transform(anchors, page, *img.size)
        vis_s = [v for v in items if not hidden[name][v["id"]] and v["visual_type"] not in GROUP_TYPES]
        inside = []
        for v in vis_s:
            px, py = to_capture(t, v["abs_x"], v["abs_y"])
            if 0 <= px < img.size[0] and 0 <= py < img.size[1]:
                inside.append(v["id"])

        drawn = []
        badges = ImageDraw.Draw(img)
        for c in numbered:
            if hidden[name][c["id"]]:
                continue
            px, py = to_capture(t, c["abs_x"], c["abs_y"])
            if 0 <= px < img.size[0] and 0 <= py < img.size[1]:
                draw_badge(badges, font, round(px), round(py), str(c["number"]))
                drawn.append(c["number"])

        stem = os.path.splitext(os.path.basename(cap))[0]
        out_img = os.path.join(args.out_dir, f"{stem} - numerada.png")
        img.save(out_img)

        outline = Image.open(cap).convert("RGB")
        draw_outlines(outline, t, vis_s)
        out_outline = os.path.join(args.out_dir, f"{stem} - contornos.png")
        outline.save(out_outline)

        numbering["captures"].append({
            "file": os.path.basename(cap), "scenario": name, "output": os.path.basename(out_img),
            "outline_output": os.path.basename(out_outline), "transform": t,
            "drawn_numbers": drawn, "visuals_in_capture": inside,
        })
        print(f"{os.path.basename(cap)} [{name}]: {len(drawn)} visuales numerados ({t['mode']}) -> {out_img}")
        print(f"  contornos: {out_outline}")

    if not args.raw:
        numbering = redact_value(numbering)
    with open(args.numbering_out, "w", encoding="utf-8") as f:
        json.dump(numbering, f, ensure_ascii=False, indent=2)
    print(f"Escenarios: {', '.join(shown)}  ·  visuales numerados en la página: {len(numbered)}")
    print(f"Numeración -> {args.numbering_out}")


if __name__ == "__main__":
    main()
