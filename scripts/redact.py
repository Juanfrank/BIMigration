#!/usr/bin/env python3
"""Redacción de hosts, credenciales y cadenas de conexión antes de que un resultado llegue al repo o a la salida.

Lo usan todos los scripts del skill. Por defecto redactan; cada script acepta --raw para uso local.

Qué se redacta (en cualquier cadena de texto, a cualquier profundidad):
  - Primer argumento de orígenes M: Sql.Database(s)("host"), Oracle.Database, PostgreSQL.Database, etc.
  - Claves de conexión: Server=, Data Source=, Host=, Address=, Password=, Pwd=, User ID=, UID=.
  - Credenciales en URLs: https://usuario:clave@host
  - Endpoints powerbi://workspace/dataset
  - Direcciones IPv4 en cualquier texto.
  - Claves de objeto que contienen datos de conexión o secretos (connectionString, password, token...):
    el valor completo se sustituye.

Qué NO detecta: nombres de host sin patrón de origen ni de clave de conexión (p. ej., un nombre de
servidor escrito suelto en una descripción). Revise la salida antes de versionarla.

Los reemplazos no contienen comillas ni barras invertidas, así que un texto JSON sigue siendo JSON válido.
"""
import re

PLACEHOLDER = {"host": "<REDACTED:host>", "ip": "<REDACTED:ip>", "secret": "<REDACTED>",
               "user": "<REDACTED:user>"}

# Llamadas de origen en M: el primer argumento es el servidor.
M_SOURCE = re.compile(
    r'(\b(?:Sql\.Databases?|Oracle\.Database|PostgreSQL\.Database|MySQL\.Database|AnalysisServices\.Database\w*|'
    r'Odbc\.DataSource|Odbc\.Query|Teradata\.Database|Cube\.Databases?|SapHana\.Database|Snowflake\.Databases?)'
    r'\s*\(\s*)"[^"]*"',
    re.IGNORECASE)
# Valores entre comillas en registros M y cadenas de conexión: Sql.Database(srv, bd, [UserName="u"])
M_QUOTED_SECRET = re.compile(
    r'((?:\b|\[)(?:Password|Pwd|UserName|UserId|User|UID|Secret|Token|ApiKey|Credential)\s*=\s*)"[^"]*"',
    re.IGNORECASE)
M_QUOTED_HOST = re.compile(r'((?:\b|\[)(?:Server|Data\s+Source|Host|Address)\s*=\s*)"[^"]*"', re.IGNORECASE)
# Valores sin comillas en cadenas de conexión (ADO/ODBC): Server=...; Data Source=...
CONN_HOST = re.compile(r"((?:Server|Data\s+Source|Host|Address|Addr|Network\s+Address)\s*=\s*)(?!\")[^;\"\n]+",
                       re.IGNORECASE)
CONN_USER = re.compile(r"((?:User\s+ID|UID|User\s+Name|User)\s*=\s*)(?!\")[^;\"\n]+", re.IGNORECASE)
CONN_PASS = re.compile(r"((?:Password|Pwd)\s*=\s*)(?!\")[^;\"\n]*", re.IGNORECASE)
# usuario:clave@host en URLs
URL_USERINFO = re.compile(r"(\b[a-z][a-z0-9+.-]*://)[^/\s:@\"]+:[^/\s@\"]+@", re.IGNORECASE)
POWERBI_URL = re.compile(r"\bpowerbi://[^\s\"\\;]+", re.IGNORECASE)
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

# Claves que, con su valor completo, son datos de conexión o secretos.
SENSITIVE_KEY = re.compile(
    r"^(connection|connectionstring|connection_details|connectiondetails|connectiondetail|"
    r"password|pwd|secret|token|apikey|api_key|credential|credentials)$",
    re.IGNORECASE)


def redact_text(text):
    if not isinstance(text, str) or not text:
        return text
    text = M_SOURCE.sub(lambda m: f'{m.group(1)}"{PLACEHOLDER["host"]}"', text)
    text = M_QUOTED_SECRET.sub(lambda m: f'{m.group(1)}"{PLACEHOLDER["secret"]}"', text)
    text = M_QUOTED_HOST.sub(lambda m: f'{m.group(1)}"{PLACEHOLDER["host"]}"', text)
    text = CONN_HOST.sub(lambda m: m.group(1) + PLACEHOLDER["host"], text)
    text = CONN_USER.sub(lambda m: m.group(1) + PLACEHOLDER["user"], text)
    text = CONN_PASS.sub(lambda m: m.group(1) + PLACEHOLDER["secret"], text)
    text = URL_USERINFO.sub(lambda m: m.group(1) + PLACEHOLDER["user"] + "@", text)
    text = POWERBI_URL.sub(PLACEHOLDER["host"], text)
    text = IPV4.sub(PLACEHOLDER["ip"], text)
    return text


def redact_value(value):
    """Aplica la redacción a un objeto JSON completo (dict, list, str...). Devuelve una copia."""
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if isinstance(k, str) and SENSITIVE_KEY.match(k) and v not in (None, "", [], {}):
                out[k] = PLACEHOLDER["secret"]
            else:
                out[k] = redact_value(v)
        return out
    if isinstance(value, list):
        return [redact_value(v) for v in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_file(path, json_mode=False):
    """Redacta un archivo de texto en su lugar. Solo escribe si el contenido cambia. Devuelve True si cambió.

    En JSON se redacta primero el texto (conserva el formato original). Se acepta solo si, parseado, es
    igual a la redacción estructural del documento; si no, el documento se reserializa.
    """
    import json
    with open(path, encoding="utf-8-sig", errors="surrogateescape") as f:
        original = f.read()
    new = redact_text(original)
    if json_mode:
        try:
            expected = redact_value(json.loads(original))
        except json.JSONDecodeError:
            expected = None
        if expected is not None:
            try:
                same = json.loads(new) == expected
            except json.JSONDecodeError:
                same = False
            if not same:
                new = json.dumps(expected, ensure_ascii=False, indent=2)
    if new == original:
        return False
    with open(path, "w", encoding="utf-8", newline="", errors="surrogateescape") as f:
        f.write(new)
    return True


TEXT_SUFFIXES = {".json", ".pbir", ".pbip", ".bim", ".tmdl", ".dax", ".md", ".txt", ".xml", ".csv", ".m", ".pq"}


# Código y temas de visuales de terceros: no son contenido del reporte y se dejan intactos.
VENDOR_DIRS = {"CustomVisuals", "StaticResources"}


def redact_tree(root):
    """Redacta en su lugar los archivos de texto del reporte bajo root (sin tocar CustomVisuals ni
    StaticResources). Devuelve la lista de archivos cambiados."""
    import os
    changed = []
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in VENDOR_DIRS]
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_SUFFIXES:
                continue
            path = os.path.join(dirpath, name)
            if redact_file(path, json_mode=ext in (".json", ".pbir", ".pbip")):
                changed.append(os.path.relpath(path, root))
    return changed


def add_raw_arg(ap):
    ap.add_argument("--raw", action="store_true",
                    help="Sin redacción (uso local). Por defecto se redactan hosts, IPs y cadenas de conexión.")


class RedactingStream:
    """Envuelve un flujo de texto (stdout o stderr) y redacta cada línea al escribirla.

    Acumula el texto hasta el salto de línea, para que un dato partido entre dos escrituras
    también se redacte. Úselo cuando la salida la produce un print() que no conviene tocar uno a uno.
    """

    def __init__(self, stream):
        self._stream = stream
        self._buf = ""

    def write(self, text):
        self._buf += text
        *lines, self._buf = self._buf.split("\n")
        for line in lines:
            self._stream.write(redact_text(line) + "\n")
        return len(text)

    def flush(self):
        if self._buf:
            self._stream.write(redact_text(self._buf))
            self._buf = ""
        self._stream.flush()

    def __getattr__(self, name):
        return getattr(self._stream, name)
