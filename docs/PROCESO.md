# Proceso de extracción

Documentación de `scripts/` y del flujo completo de [SKILL.md](../SKILL.md).

## Requisitos

- Python 3.10 o superior, con `Pillow` (`pip install pillow`).
- Para `.pbix` con modelo embebido, el `Model.bim` se obtiene con [pbi-tools](https://pbi.tools) (no está automatizado aquí).

## Pipeline

```
run_skill.py
 ├─ copia el archivo, .Report/.SemanticModel, capturas y Model.bim a <Archivo>/source/
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
- **Modelo:** en PBIP, `definition.pbir` indica si el modelo es `byConnection`, `byPath` o ninguno. En PBIX, indica si `DataModel` está embebido.
- **Medidas de extensión:** `definition/reportExtensions.json`, con su DAX.

## extract_model.py

Lee `Model.bim` (TMSL JSON) y produce tablas, columnas (con marca de calculada), medidas, relaciones y orígenes. Para relaciones, si `fromCardinality` o `toCardinality` no vienen en el archivo, usa los valores por defecto del esquema y los marca como `(defecto)`.

## annotate_captures.py

- **Numeración:** solo visuales no ocultos con al menos un campo. Orden: banda de 30 px en Y, luego X. Los visuales dentro de un grupo suman la posición del grupo.
- **Calibración:** con dos o más anclas, ajusta una transformación lineal por eje (mínimos cuadrados). Sin anclas, usa `ancho_captura / ancho_página` sin desplazamiento y lo deja escrito en `numbering.json`.
- **Salida:** dibuja un distintivo rojo con el número en la esquina superior izquierda de cada visual numerado que cae dentro de la captura. `numbering.json` guarda la numeración de toda la página y, por captura, los visuales dentro del marco (incluidos los no numerados, para recursos).

## build_markdown.py

Genera el .md. Solo incluye los visuales numerados dentro de las capturas. Ver [FORMATO.md](FORMATO.md).

## Limitaciones conocidas

- **Un .pbix sin visuales no prueba el camino de visuales de PBIX.** La única muestra local (`123.pbix`) tiene una página vacía. El análisis de visuales de `.pbix` está escrito pero no verificado con un reporte real.
- **Modelo:** solo se lee `Model.bim`. Los modelos en formato TMDL no se leen; conviértalos antes (por ejemplo, con Tabular Editor o pbi-tools).
- **Modelos remotos:** sin `Model.bim`, los apéndices A, B y C indican que requieren el modelo.
- **Unidades de fecha:** `TimeUnit` se escribe como número sin traducir. La tabla de equivalencias no está verificada contra Power BI, así que el .md no la usa.
- **Calibración automática:** sin anclas, la numeración sobre la captura puede estar desplazada. Dos anclas bastan para la mayoría de los casos.
- **Numeración:** es por orden de lectura, no la asignada a mano en capturas anteriores. Si una captura ya fue numerada a mano, los números no coincidirán.
- **Filtros de visual:** se listan todos los del visual. Algunos, sin condición (por ejemplo, filtros "Advanced" vacíos), aparecen con "—".
