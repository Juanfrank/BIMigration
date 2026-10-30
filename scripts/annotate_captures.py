#!/usr/bin/env python3
"""Numera los visuales de una página de Power BI y dibuja la numeración sobre capturas.

Uso:
    python annotate_captures.py --report report.json --page "Nombre de página" \
        --capture captura1.png [captura2.png ...] --out-dir output/ \
        [--anchor "ID_VISUAL=px,py" ...]

Reglas de numeración (fijas, independientes de las capturas):
  - Solo visuales con al menos un campo (medida o columna) en algún pozo.
  - Se omiten formas, textos, imágenes y grupos.
  - Orden de lectura: por banda de altura (30 px) y luego de izquierda a derecha.
  - Los visuales dentro de un grupo se desplazan por la posición del grupo.

Calibración captura <-> página:
  - Con dos o más --anchor (ID del visual y píxel de su esquina superior izquierda en la
    captura) se ajusta una transformación lineal por eje.
  - Sin anclas se usa la escala ancho_captura / ancho_página, sin desplazamiento. Es
    aproximado: la salida indica que la calibración es automática.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BADGE_FONT_PATHS = ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
GROUP_TYPES = {None, "group", "visualGroup"}
# Tarjetas con varios campos: cada campo es una tarjeta con su propio número.
MULTI_CARD_TYPES = {"card", "cardVisual", "multiRowCard"}


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


def absolute_positions(page):
    """Devuelve visuales con coordenadas absolutas (sumando la posición del grupo padre)."""
    by_id = {v["id"]: v for v in page["visuals"]}
    result = []
    for v in page["visuals"]:
        ax, ay = v["x"], v["y"]
        parent = by_id.get(v.get("parent_group"))
        if parent:
            ax += parent["x"]
            ay += parent["y"]
        result.append(dict(v, abs_x=ax, abs_y=ay))
    return result


def is_numberable(v):
    return (not v["is_hidden"]) and bool(v["wells"]) and v["visual_type"] not in GROUP_TYPES


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


def draw_badge(draw, font, x, y, text):
    w = 10 + 7 * len(text)
    h = 18
    x0, y0 = x - 2, y - 2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=5, fill=(220, 20, 20), outline=(255, 255, 255))
    draw.text((x0 + w / 2, y0 + h / 2), text, font=font, fill=(255, 255, 255), anchor="mm")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True, help="report.json de extract_report.py")
    ap.add_argument("--page", help="Nombre (o id) de la página")
    ap.add_argument("--capture", nargs="+", required=True, help="Capturas de la página")
    ap.add_argument("--anchor", action="append", help="ID_VISUAL=px,py (repetible, mínimo 2 para calibrar)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--numbering-out", required=True, help="JSON con la numeración de la página")
    args = ap.parse_args()

    with open(args.report, encoding="utf-8") as f:
        report = json.load(f)
    page = find_page(report, args.page)
    visuals = absolute_positions(page)
    numbered = number_visuals(visuals)
    anchors = parse_anchors(args.anchor, visuals)

    os.makedirs(args.out_dir, exist_ok=True)
    font = pick_font(12)
    numbering = {"page": page["name"], "page_id": page["id"], "page_size": [page.get("width"), page.get("height")],
                 "visuals": [], "captures": []}
    for v in numbered:
        numbering["visuals"].append({
            "number": v["number"], "id": v["id"], "visual_type": v["visual_type"], "title": v["title"],
            "abs_x": v["abs_x"], "abs_y": v["abs_y"], "width": v["width"], "height": v["height"],
            "parent_group": v["parent_group"], "sub_refs": v["sub_refs"],
        })

    for cap in args.capture:
        img = Image.open(cap).convert("RGB")
        t = build_transform(anchors, page, *img.size)
        draw = ImageDraw.Draw(img)
        drawn, inside = [], []
        for v in visuals:
            px = t["sx"] * v["abs_x"] + t["bx"]
            py = t["sy"] * v["abs_y"] + t["by"]
            if 0 <= px < img.size[0] and 0 <= py < img.size[1] and v["id"] not in inside:
                inside.append(v["id"])
        for v in numbered:
            px = t["sx"] * v["abs_x"] + t["bx"]
            py = t["sy"] * v["abs_y"] + t["by"]
            if 0 <= px < img.size[0] and 0 <= py < img.size[1]:
                draw_badge(draw, font, round(px), round(py), str(v["number"]))
                drawn.append(v["number"])
        name = os.path.splitext(os.path.basename(cap))[0]
        out_img = os.path.join(args.out_dir, f"{name} - numerada.png")
        img.save(out_img)
        numbering["captures"].append({"file": os.path.basename(cap), "output": os.path.basename(out_img),
                                      "transform": t, "drawn_numbers": drawn, "visuals_in_capture": inside})
        print(f"{os.path.basename(cap)}: {len(drawn)} visuales numerados ({t['mode']}) -> {out_img}")

    with open(args.numbering_out, "w", encoding="utf-8") as f:
        json.dump(numbering, f, ensure_ascii=False, indent=2)
    print(f"Visuales numerados en la página: {len(numbered)}  -> {args.numbering_out}")


if __name__ == "__main__":
    main()
