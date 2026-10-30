#!/usr/bin/env python3
"""Valida la estructura de expresiones DAX y que la limpieza de comentarios no cambie el código vivo.

No es un formateador ni un analizador semántico: no sabe si una función existe ni si las columnas
son válidas. Sí detecta:
  - cadenas "...", nombres 'x' y bloques /* ... */ sin cerrar
  - paréntesis y llaves sin pareja, o cerrados en orden incorrecto
  - comentarios que quedan después de limpiar (// -- /* */)
  - */ suelto
  - comas finales antes de ) o }
  - código vivo distinto antes y después de limpiar (ningún token debe perderse ni aparecer)

Uso:
    python scripts/dax_check.py --bim Model.bim [--json]        # revisa medidas y columnas calculadas
    python scripts/dax_check.py --expr "CALCULATE([x], T[c])"   # revisa una expresión suelta

Salida: código 0 si no hay problemas, 1 si los hay.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bim_core import iter_objects, load_bim, strip_dax_comments  # noqa: E402

OPERATORS = set("+-*/^&=<>|,.;:")


class DaxSyntaxError(Exception):
    pass


def tokenize(expr):
    """Tokens de código DAX, sin espacios. Los comentarios salen como tokens ('comment', texto).

    Errores: DaxSyntaxError con descripción. Mantiene el orden de (), {} y los literales.
    """
    tokens = []
    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
        elif c in ('"', "'"):
            j = i + 1
            while True:
                if j >= n:
                    raise DaxSyntaxError(f"{'cadena' if c == '\"' else 'nombre'} sin cerrar desde la posición {i}")
                if expr[j] == c:
                    if j + 1 < n and expr[j + 1] == c:
                        j += 2
                        continue
                    break
                j += 1
            tokens.append(("str" if c == '"' else "qname", expr[i:j + 1]))
            i = j + 1
        elif c == "[":
            j = expr.find("]", i)
            if j < 0:
                raise DaxSyntaxError(f"columna o medida [ sin cerrar desde la posición {i}")
            tokens.append(("bracket", expr[i:j + 1]))
            i = j + 1
        elif expr.startswith("//", i) or expr.startswith("--", i):
            j = expr.find("\n", i)
            j = n if j < 0 else j
            tokens.append(("comment", expr[i:j]))
            i = j
        elif expr.startswith("/*", i):
            depth, j = 1, i + 2
            while j < n and depth:
                if expr.startswith("/*", j):
                    depth, j = depth + 1, j + 2
                elif expr.startswith("*/", j):
                    depth, j = depth - 1, j + 2
                else:
                    j += 1
            if depth:
                raise DaxSyntaxError(f"comentario /* sin cerrar desde la posición {i}")
            tokens.append(("comment", expr[i:j]))
            i = j
        elif expr.startswith("*/", i):
            raise DaxSyntaxError(f"*/ sin apertura en la posición {i}")
        elif c.isalnum() or c == "_" or c == "#":
            j = i + 1
            while j < n and (expr[j].isalnum() or expr[j] in "_#.") :
                j += 1
            tokens.append(("word", expr[i:j]))
            i = j
        else:
            tokens.append(("op", c))
            i += 1
    return tokens


def structure_problems(expr):
    """Problemas de estructura de una expresión ya tokenizada. Lista de textos; vacía si no hay."""
    problems = []
    try:
        tokens = tokenize(expr)
    except DaxSyntaxError as e:
        return [str(e)]
    stack = []
    pairs = {")": "(", "}": "{"}
    for kind, text in tokens:
        if kind == "comment":
            problems.append(f"comentario sin limpiar: {text[:40]!r}")
        elif kind == "op" and text in "({":
            stack.append(text)
        elif kind == "op" and text in pairs:
            if not stack or stack[-1] != pairs[text]:
                problems.append(f"'{text}' sin apertura correspondiente")
                stack = []
            else:
                stack.pop()
    if stack:
        problems.append(f"'{stack[-1]}' sin cerrar")
    for (k1, t1), (k2, t2) in zip(tokens, tokens[1:]):
        if k1 == "op" and t1 == "," and k2 == "op" and t2 in ")}":
            problems.append("coma final antes de ')' o '}'")
    if tokens and tokens[-1][0] == "op" and tokens[-1][1] in "+-*/&|=<>,":
        problems.append(f"la expresión termina en operador '{tokens[-1][1]}'")
    return problems


def live_tokens(expr):
    """Tokens de código vivo: sin comentarios, sin espacios."""
    return [tok for tok in tokenize(expr) if tok[0] != "comment"]


def check_expression(expr):
    """Revisa una expresión original: estructura de la versión limpia y que el código vivo no cambie."""
    problems = []
    if not expr or not expr.strip():
        return problems
    try:
        original = live_tokens(expr)
    except DaxSyntaxError as e:
        return [f"original: {e}"]
    cleaned = strip_dax_comments(expr)
    problems += [f"limpia: {p}" for p in structure_problems(cleaned)]
    try:
        after = live_tokens(cleaned)
    except DaxSyntaxError as e:
        problems.append(f"limpia: {e}")
        return problems
    if original != after:
        diff_at = next((i for i, (a, b) in enumerate(zip(original, after)) if a != b), min(len(original), len(after)))
        problems.append(f"el código vivo cambió al limpiar (token {diff_at}: "
                        f"{original[diff_at:diff_at + 1]} → {after[diff_at:diff_at + 1]})")
    return problems


def check_model(bim_path):
    model = load_bim(bim_path)
    report = []
    checked = 0
    for obj in iter_objects(model):
        if obj["kind"] not in ("measure", "calculated_column"):
            continue
        raw_expr = None
        # iter_objects ya limpia; para revisar el original se vuelve a leer el objeto crudo.
        raw_expr = _raw_expression(model, obj)
        checked += 1
        problems = check_expression(raw_expr)
        if problems:
            report.append({"kind": obj["kind"], "table": obj["table"], "name": obj["name"], "problems": problems})
    return checked, report


def _raw_expression(model, obj):
    for t in model.get("tables", []):
        if t.get("name") != obj["table"]:
            continue
        if obj["kind"] == "measure":
            for m in t.get("measures", []):
                if m.get("name") == obj["name"]:
                    return _join(m.get("expression"))
        else:
            for c in t.get("columns", []):
                if c.get("name") == obj["name"] and c.get("type") == "calculated":
                    return _join(c.get("expression"))
    return None


def _join(value):
    if value is None:
        return None
    return "\n".join(value) if isinstance(value, list) else value


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bim")
    ap.add_argument("--expr")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.expr is not None:
        problems = check_expression(args.expr)
        print("\n".join(problems) if problems else "OK")
        sys.exit(1 if problems else 0)
    if not args.bim:
        ap.error("indique --bim o --expr")
    checked, report = check_model(args.bim)
    if args.json:
        print(json.dumps({"revisadas": checked, "con_problemas": report}, ensure_ascii=False, indent=2))
    else:
        print(f"Revisadas: {checked} medidas y columnas calculadas. Con problemas: {len(report)}")
        for r in report:
            print(f"- {r['kind']} {r['table']}[{r['name']}]")
            for p in r["problems"]:
                print(f"    {p}")
    sys.exit(1 if report else 0)


if __name__ == "__main__":
    main()
