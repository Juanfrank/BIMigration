# Búsqueda en modelos .bim

Herramientas para leer y consultar modelos Power BI en formato TMSL (`Model.bim`). Son la base para los siguientes ejercicios sobre modelos.

## Archivos

- `scripts/bim_core.py`: biblioteca de lectura. Carga el `.bim`, recorre los objetos y extrae referencias DAX. Sin dependencias fuera de la biblioteca estándar.
- `scripts/bim_search.py`: CLI sobre un índice SQLite con FTS5. Se construye la primera vez que se consulta un `.bim` y se reutiliza.

## Uso

```bash
python scripts/bim_search.py --bim Model.bim stats
python scripts/bim_search.py --bim Model.bim search "audiencias programadas" --kind measure
python scripts/bim_search.py search --regex "Penal_vw\w+" --in expr -i --limit 20
python scripts/bim_search.py show "vwSGJAudienciasBO[Audiencias Programadas]"
python scripts/bim_search.py refs "Audiencias Programadas" --table vwSGJAudienciasBO
python scripts/bim_search.py refs "Audiencias Programadas" --uses
python scripts/bim_search.py search "Sql.Databases" --in expr --json
```

Tras la primera consulta, `--bim` puede omitirse: se usa el último archivo consultado.

### Comandos

| Comando | Qué hace |
|---|---|
| `search "texto"` | Busca palabras (AND, prefijos, sin tildes) en nombre, descripción y expresión. `--in name\|desc\|expr\|all`. |
| `search --regex RX` | Filtra con una expresión regular de Python. `-i` ignora mayúsculas. Combinable con texto. |
| `search --kind K --table T` | Filtra por tipo de objeto o tabla propietaria. |
| `show "Tabla[Objeto]"` | Ficha del objeto: tipo, carpeta, descripción, qué usa, cuántos objetos lo usan y su expresión completa. |
| `refs "Objeto"` | Qué objetos lo usan. Con `--uses`, qué usa el objeto. |
| `stats` | Conteo por tipo, medidas por tabla y referencias sin resolver. |

Tipos de objeto: `table`, `column`, `calculated_column`, `measure`, `hierarchy`, `partition`, `relationship`, `shared_expression`.

### Índice

- Se guarda en `~/.cache/bim-search` (o `$XDG_CACHE_HOME`), con el nombre del archivo y los primeros 12 caracteres de su SHA-256. Si el `.bim` cambia, se reconstruye solo.
- `--rebuild` fuerza la reconstrucción.
- Nada se escribe dentro del repo.

## Biblioteca (`bim_core.py`)

```python
import sys; sys.path.insert(0, "scripts")
from bim_core import load_bim, iter_objects, extract_refs

model = load_bim("Model.bim")
for obj in iter_objects(model):
    if obj["kind"] == "measure" and "Programadas" in (obj["name"] or ""):
        print(obj["table"], obj["name"], extract_refs(obj))
```

Cada objeto es un diccionario con `kind`, `table`, `name`, `expression`, `data_type`, `description`, `display_folder`, `format_string`, `hidden`, `source_column` y `extra` (datos propios del tipo, por ejemplo cardinalidad de una relación o modo de partición).

`extract_refs` devuelve `[(tabla o None, nombre)]`. Una referencia sin tabla (`[Medida]`) aparece con `None`.

## Validación de DAX

`scripts/dax_check.py` revisa las medidas y columnas calculadas de un `.bim`:

```bash
python scripts/dax_check.py --bim Model.bim          # 0 = sin problemas, 1 = hay problemas
python scripts/dax_check.py --expr "CALCULATE([x], T[c])"
```

Detecta cadenas, nombres y comentarios sin cerrar, paréntesis o llaves sin pareja, `*/` sueltos, comas finales y comentarios que quedan después de limpiar. También comprueba que la limpieza no cambie el código vivo: los tokens antes y después deben ser iguales.

No es un formateador ni valida funciones o columnas. Un formateador en línea (daxformatter.com) enviaría el DAX del modelo a un servicio externo, por lo que no se usa aquí.

Los comentarios de bloque `/* */` se anidan: un `/*` dentro de otro bloque no cierra el exterior. Es la intención visible de las dos medidas que comentan un bloque con sub-comentarios (`Juez Estado Fallo`, `Juez En Mora Prueba`). Las reglas no anidadas de DAX darían un `*/` sobrante; si el motor de Power BI no admite anidamiento, esas dos medidas ya fallan en el original.

## Redacción

Por defecto, `bim_search.py` redacta su salida (texto y JSON): hosts en orígenes M (`Sql.Databases("...")`), IPs, cadenas de conexión, credenciales y URLs `powerbi://`. `--raw` desactiva la redacción para uso local.

El índice de la caché **no** se redacta, porque la búsqueda necesita el texto real. No lo copie fuera de su equipo. Vive en `~/.cache/bim-search`, fuera del repo.

La redacción se define en `scripts/redact.py`; sus pruebas están en `scripts/test_redact.py`:

```bash
python -m unittest scripts/test_redact.py
```

## Decisiones

- **Índice en SQLite y no solo lectura del JSON.** Cada consulta de Python ya cuesta parsear el archivo (≈0.1 s con un modelo de 5 MB). El índice permite búsquedas por texto, dependencias en ambas direcciones y varias consultas sin volver a leer el archivo.
- **Referencias extraídas al indexar.** Las dependencias se guardan en una tabla, así que `refs` y `--uses` no reanalizan el DAX.
- **Comentarios y cadenas DAX se ignoran** al extraer referencias, para no contar `"[texto]"` o `-- [nota]` como dependencias.
- **Relaciones cuentan como dependencia** de sus dos columnas.

## Límites conocidos

- **Referencias sin tabla.** `[Medida]` se asocia por nombre. Si dos tablas tienen una medida con el mismo nombre, `refs` lo marca como «posible coincidencia».
- **Nombres de columnas idénticos en varias tablas.** `refs` con `--table` intenta resolverlo, pero las referencias sin tabla pueden aparecer de más.
- **Expresiones M.** Se indexan como texto. Las dependencias entre consultas M (por ejemplo, un paso que usa otra tabla) no se extraen.
- **Solo `Model.bim`.** Los modelos en TMDL no se leen; conviértalos antes (Tabular Editor o pbi-tools).
- **Redacción por patrón.** Un nombre de servidor escrito sin patrón de origen ni de clave de conexión (por ejemplo, en una descripción) no se detecta. Revise la salida antes de versionarla.
