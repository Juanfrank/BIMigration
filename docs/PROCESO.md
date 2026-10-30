# Proceso de extracción

Documentación de `scripts/` y del flujo completo de [SKILL.md](../SKILL.md).

## Requisitos

- Python 3.10 o superior, con `Pillow` (`pip install pillow`).
- Para `.pbix` con modelo embebido, el `Model.bim` se obtiene con [pbi-tools](https://pbi.tools) (no está automatizado aquí).

## Pipeline

Los resultados van a `processed/<Archivo>/` dentro del repo.

```
run_skill.py
 ├─ copia el archivo, .Report/.SemanticModel, capturas y Model.bim a processed/<Archivo>/source/
 ├─ extract_report.py   -> output/datos/report.json
 ├─ extract_model.py    -> output/datos/model.json        (solo si hay Model.bim)
 ├─ annotate_captures.py-> output/<captura> - numerada.png
 │                         output/datos/numbering.json
 └─ build_markdown.py   -> output/<Archivo> - <Página>.md
                           output/resources/             (solo recursos de capturas)
```

## extract_report.py

Lee un `.pbip` (formato PBIR) o un `.pbix` (`Report/Layout`).

- **Visual:** tipo, posición, tamaño, grupo padre, título, texto (textbox), pozos de campos y filtros.
- **Pozos:** los nombres de pozo son los de Power BI tal como aparecen en `query.queryState` (PBIR) o `projections` (pbix): por ejemplo `Data`, `Values`, `Rows`, `Columns`, `Category`, `Y`, `Y2`.
- **Campo:** `column`, `measure`, `hierarchy_level`, `aggregation` (con su función) o `arithmetic` (con sus dos lados y el operador). Cada campo lleva su nombre visible (`displayName`).
- **Filtros:** de visual, de página y de informe. Cada filtro conserva tipo, origen (`howCreated`) y condición en texto. Las expresiones de fecha se conservan con su unidad numérica (ver limitaciones).
- **Redacción (por defecto):** `scripts/redact.py` quita hosts, IPs, credenciales y cadenas de conexión de todas las salidas (`report.json`, `model.json`, `numbering.json`, el `.md`) y de los archivos de texto copiados al repo (`definition.pbir`, `.dax`, `.pbip`). Los visuales de terceros (`CustomVisuals/`, `StaticResources/`) no se tocan. `--raw` desactiva la redacción; úselo solo en local.
- **Model.bim:** no se copia al repo (contiene expresiones M con servidores). Se lee desde su ubicación original. Con `--raw` sí se copia.
- **Capturas:** no se redactan. Revise que no muestren servidores o credenciales antes de versionarlas.
- **Modelo:** en PBIP, `definition.pbir` indica si el modelo es `byConnection`, `byPath` o ninguno. En PBIX, indica si `DataModel` está embebido.
- **Medidas de extensión:** `definition/reportExtensions.json`, con su DAX.

## extract_model.py

Lee `Model.bim` (TMSL JSON) y produce tablas, columnas (con marca de calculada), medidas, relaciones y orígenes. Para relaciones, si `fromCardinality` o `toCardinality` no vienen en el archivo, usa los valores por defecto del esquema y los marca como `(defecto)`.

## annotate_captures.py

- **Tarjetas múltiples:** un `card` o `cardVisual` con varios campos se divide en partes iguales a lo ancho; cada campo recibe su número y, en el .md, solo muestra su campo.
- **Numeración:** solo visuales con al menos un campo que no estén ocultos, ni por sí mismos ni por estar dentro de un grupo oculto (los ocultos se descartan también de la lista de recursos de cada captura). Orden: banda de 30 px en Y, luego X. Los visuales dentro de un grupo suman la posición del grupo.
- **Calibración:** con dos o más anclas, ajusta una transformación lineal por eje (mínimos cuadrados). Sin anclas, usa `ancho_captura / ancho_página` sin desplazamiento y lo deja escrito en `numbering.json`.
- **Salida:** dibuja un distintivo rojo con el número en la esquina superior izquierda de cada visual numerado que cae dentro de la captura. `numbering.json` guarda la numeración de toda la página y, por captura, los visuales dentro del marco (incluidos los no numerados, para recursos).
- **Escenarios:** el estado guardado de la página es el escenario `Default`. Cada bookmark de la página es otro escenario (su `displayName`). Cada captura declara el suyo con `--scenario "captura=escenario"`; sin declararlo, es `Default`. El script no detecta el escenario desde la imagen: lo indica quien ejecuta, tras mirar la captura.
- **Numeración única:** cubre los visuales visibles en algún escenario usado por las capturas. Un visual conserva su número entre capturas; lo que cambia entre escenarios es qué badges se dibujan.
- **Visibilidad:** un visual está oculto en un escenario si él o cualquier grupo padre lo está. Los overrides de un bookmark solo aplican a los visuales objetivo cuando `applyOnlyToTargetVisuals` es verdadero.
- **Posición absoluta:** suma toda la cadena de grupos padre, no solo el inmediato.
- **Superposiciones:** un badge queda tapado si un visual visible de mayor z cubre su esquina superior izquierda en ese escenario. Se reporta por escenario (`scenarios.<nombre>.covered`). Es geométrico: no ve el contenido real de la captura.
- **Contornos:** `<captura> - contornos.png` dibuja el contorno de cada visual visible en el escenario de la captura. Sirve para comparar con la captura real y ver si el escenario declarado coincide.

## build_markdown.py

Genera el .md. Solo incluye los visuales numerados dentro de las capturas. Ver [FORMATO.md](FORMATO.md).

## Limitaciones conocidas

- **Un .pbix sin visuales no prueba el camino de visuales de PBIX.** La única muestra local (`123.pbix`) tiene una página vacía. El análisis de visuales de `.pbix` está escrito pero no verificado con un reporte real.
- **Modelo:** solo se lee `Model.bim`. Los modelos en formato TMDL no se leen; conviértalos antes (por ejemplo, con Tabular Editor o pbi-tools).
- **Modelos remotos:** sin `Model.bim`, los apéndices A, B y C indican que requieren el modelo.
- **Unidades de fecha:** `TimeUnit` se escribe como número sin traducir. La tabla de equivalencias no está verificada contra Power BI, así que el .md no la usa.
- **Calibración automática:** sin anclas, la numeración sobre la captura puede estar desplazada. Dos anclas bastan para la mayoría de los casos.
- **Numeración:** es por orden de lectura, no la asignada a mano en capturas anteriores. Si una captura ya fue numerada a mano, los números no coincidirán.
- **Escenarios:** solo se modela la visibilidad que fijan los bookmarks (`visualContainerGroups` y `visualContainers.display`). Otros cambios de un bookmark (filtros, páginas, selección) no se reproducen; el .md los omite.
- **Acciones de botón:** no se leen. La relación entre un botón y el bookmark que activa se conoce solo por el bookmark en sí.
- **Coincidencia de escenario:** la identifica quien ejecuta mirando la captura y los contornos. Un escenario mal declarado produce badges en lugar equivocado sin error.
- **Filtros de visual:** se listan todos los del visual. Algunos, sin condición (por ejemplo, filtros "Advanced" vacíos), aparecen con "—".
