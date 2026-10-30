# Formato del .md generado

Un archivo por página: `output/<Archivo> - <Página>.md`.

## Encabezado

- Archivo fuente y tipo (`pbip` o `pbix`).
- Estado del modelo: incluido (con la ruta del `Model.bim`) o pendiente por modo `byConnection`/`none`.
- Capturas usadas, con el escenario de cada una, y fecha de generación.

## 1. Numeración

Tabla con Nº, tipo de visual, título, ID del visual (8 caracteres) y capturas donde aparece.

## 2. Visuales y pozos de campos

Un bloque por visual numerado:

- **Pozos:** pozo, campo (`Tabla.Propiedad`), tipo (Medida, Columna, Nivel de jerarquía, Agregación, Aritmética), nombre visible y propiedad.
- **Filtros del visual:** campo, tipo de filtro (Categorical, Advanced, RelativeDate, TopN…), condición en texto y origen (User, Visual, etc.).

## 3. Filtros de página e informe

Solo si existen. Ámbito, campo, tipo y condición.

## 4. Escenarios y superposiciones

Un bloque por escenario usado por las capturas (Default y cada bookmark usado):

- **Capturas:** las que muestran ese escenario.
- **Visuales visibles (Nº):** números de la sección 1 visibles en el escenario.
- **Muestra / Oculta (Nº):** en un bookmark, qué números aparecen y desaparecen respecto al estado guardado.
- **Cambios en visuales sin numeración:** visuales sin campos (formas, textos) cuya visibilidad cambia.
- **Badge tapado por:** tabla de números cuyo badge queda cubierto por un visual de mayor z en ese escenario. Si no hay ninguno, lo indica.

## Apéndice A. Medidas y columnas calculadas

Columnas: tabla, nombre, origen (Medida del modelo, Medida de extensión, Columna calculada), descripción, DAX, formato, carpeta de visualización, oculta, y los números de los visuales que la usan. Si una medida cita otra en su DAX, la segunda aparece con "dependencia" o con los números de visual que la usan.

Sin `Model.bim`, esta sección dice que requiere el modelo y solo incluye las medidas de extensión que estén en el propio archivo.

## Apéndice B. Relaciones

Incluye una relación si se cumple una de estas condiciones:

- Sus dos extremos son tablas que usan los visuales numerados (campos y filtros).
- Una medida de la página la activa con `USERELATIONSHIP` o `CROSSFILTER`. Las medidas de la página incluyen las que citan en su DAX (en cadena).

Columnas: nombre, lado origen, lado destino, cardinalidad (con `(defecto)` cuando el archivo no la declara), filtro cruzado, si está activa y qué medidas la activan. La activación compara tabla y columna de ambos extremos en los argumentos de la llamada, no solo el nombre de la columna.

## Apéndice C. Orígenes de datos

Orígenes del modelo (nombre, tipo, detalles de conexión, autenticación) y particiones de las tablas usadas (modo, tipo y expresión de origen).

## Recursos externos

Imágenes y otros recursos que aparecen en una captura: ID del visual, tipo, nombre del recurso y ruta dentro de `output/`. Si no se encuentra el archivo, la fila lo dice.
