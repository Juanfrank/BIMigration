#!/usr/bin/env python3
"""Orquesta la extracción completa para un .pbip o .pbix y deja el resultado en el repo.

Uso:
    python scripts/run_skill.py --source ruta/Archivo.pbip --page "Nombre" \
        --captures ruta/captura1.png [ruta/captura2.png ...] \
        [--model ruta/Model.bim] [--anchor "ID=px,py" ...] [--scenario "captura=escenario" ...] [--raw]

Redacción (por defecto activa): los archivos de texto copiados al repo y todas las salidas JSON y Markdown
pasan por scripts/redact.py (hosts, IPs, cadenas de conexión, credenciales). El Model.bim no se copia al repo.
--raw desactiva la redacción y copia el Model.bim: úsalo solo en local, nunca para versionar.
Las capturas (imágenes) no se redactan: revise que no muestren servidores o credenciales.

Estructura resultante (en processed/ dentro del repo):
    processed/<Archivo>/
      source/      archivo .pbip/.pbix (y carpetas .Report / .SemanticModel), capturas
      output/      capturas numeradas y de contornos, <Archivo> - <Página>.md, resources/, datos/ (JSON intermedios)

Códigos de salida:
    0  listo
    2  falta --page: el script imprime las páginas disponibles para preguntar al usuario
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redact import add_raw_arg, redact_tree  # noqa: E402

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCRIPTS)
PY = sys.executable


def run(args):
    res = subprocess.run([PY] + args, capture_output=True, text=True, encoding="utf-8")
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        sys.exit(res.returncode)
    return res


def stage_source(src, source_dir):
    """Copia el archivo y sus dependencias locales al repo, conservando rutas relativas."""
    os.makedirs(source_dir, exist_ok=True)
    dest = os.path.join(source_dir, os.path.basename(src))
    if os.path.abspath(dest) != os.path.abspath(src):
        shutil.copy2(src, dest)
    if src.lower().endswith(".pbip"):
        base = os.path.dirname(os.path.abspath(src))
        with open(src, encoding="utf-8-sig") as f:
            data = json.load(f)
        for art in data.get("artifacts", []):
            for kind in ("report", "semanticModel"):
                rel = art.get(kind, {}).get("path")
                if rel and os.path.isdir(os.path.join(base, rel)):
                    target = os.path.join(source_dir, rel)
                    if not os.path.exists(target):
                        shutil.copytree(os.path.join(base, rel), target)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help="Archivo .pbip o .pbix")
    ap.add_argument("--page", help="Nombre de la página a procesar")
    ap.add_argument("--captures", nargs="+", required=True, help="Capturas de la(s) página(s)")
    ap.add_argument("--model", help="Model.bim del modelo fuente (si el reporte no lo trae en local)")
    ap.add_argument("--anchor", action="append", help="ID_VISUAL=px,py para calibrar la captura")
    ap.add_argument("--scenario", action="append",
                    help="captura=escenario: estado en que está la captura (Default o nombre de un bookmark)")
    ap.add_argument("--repo-root", default=REPO)
    add_raw_arg(ap)
    args = ap.parse_args()
    raw = ["--raw"] if args.raw else []

    stem = os.path.splitext(os.path.basename(args.source))[0]
    root = os.path.join(args.repo_root, "processed", stem)
    source_dir = os.path.join(root, "source")
    output_dir = os.path.join(root, "output")
    data_dir = os.path.join(output_dir, "datos")
    for d in (source_dir, output_dir, data_dir):
        os.makedirs(d, exist_ok=True)

    src_file = stage_source(args.source, source_dir)
    if not args.raw:
        changed = redact_tree(source_dir)
        if changed:
            print(f"Redactado en la copia del repo: {', '.join(changed)}")
    cap_dir = os.path.join(source_dir, "captures")
    os.makedirs(cap_dir, exist_ok=True)
    caps = []
    for c in args.captures:
        dst = os.path.join(cap_dir, os.path.basename(c))
        if os.path.abspath(dst) != os.path.abspath(c):
            shutil.copy2(c, dst)
        caps.append(dst)

    # El Model.bim contiene expresiones M con servidores: no se copia al repo salvo con --raw.
    model_src = None
    if args.model:
        if args.raw:
            model_src = os.path.join(source_dir, "Model.bim")
            if os.path.abspath(args.model) != os.path.abspath(model_src):
                shutil.copy2(args.model, model_src)
        else:
            model_src = os.path.abspath(args.model)
            print("Model.bim: se lee desde su ubicación original y no se copia al repo (sin --raw).")

    report_json = os.path.join(data_dir, "report.json")
    run([os.path.join(SCRIPTS, "extract_report.py"), src_file, "--out", report_json, *raw])

    if not args.page:
        run_page_list = [os.path.join(SCRIPTS, "annotate_captures.py"), "--report", report_json,
                         "--capture", caps[0], "--out-dir", data_dir, "--numbering-out", os.devnull]
        res = subprocess.run([PY] + run_page_list, capture_output=True, text=True, encoding="utf-8")
        sys.stdout.write(res.stderr or res.stdout)
        print("\nFalta --page. Pregunte al usuario en qué página están las capturas.")
        sys.exit(2)

    model_json = None
    if model_src:
        model_json = os.path.join(data_dir, "model.json")
        run([os.path.join(SCRIPTS, "extract_model.py"), model_src, "--out", model_json, *raw])

    numbering_json = os.path.join(data_dir, "numbering.json")
    ann_cmd = [os.path.join(SCRIPTS, "annotate_captures.py"), "--report", report_json, "--page", args.page,
               "--capture", *caps, "--out-dir", output_dir, "--numbering-out", numbering_json, *raw]
    for a in args.anchor or []:
        ann_cmd += ["--anchor", a]
    for sc in args.scenario or []:
        ann_cmd += ["--scenario", sc]
    run(ann_cmd)

    with open(numbering_json, encoding="utf-8") as f:
        page_name = json.load(f)["page"]
    out_md = os.path.join(output_dir, f"{stem} - {page_name}.md")
    md_cmd = [os.path.join(SCRIPTS, "build_markdown.py"), "--report", report_json, "--numbering", numbering_json,
              "--out-md", out_md, "--out-dir", output_dir, *raw]
    if model_json:
        md_cmd += ["--model", model_json]
    run(md_cmd)
    print(f"\nListo. Salida en: {output_dir}")


if __name__ == "__main__":
    main()
