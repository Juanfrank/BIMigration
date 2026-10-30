# Formato del .md generado

Un archivo por página: `output/<Archivo> - <Página>.md`.

## Encabezado

- Archivo fuente y tipo (`pbip` o `pbix`).
- Estado del modelo: incluido (con la ruta del `Model.bim`) o pendiente por modo `byConnection`/`none`.
- Capturas usadas y fecha de generación.

## 1. Numeración

Tabla con Nº, tipo de visual, título, ID del visual (8 caracteres) y capturas donde aparece.

## 2. Visuales y pozos de campos

Un bloque por visual numerado:

- **Pozos:** pozo, campo (`Tabla.Propiedad`), tipo (Medida, Columna, Nivel de jerarquía, Agregación, Aritmética), nombre visible y propiedad.
- **Filtros del visual:** campo, tipo de filtro (Categorical, Advanced, RelativeDate, TopN…), condición en texto y origen (User, Visual, etc.).

## 3. Filtros de página e informe

Solo si existen. Ámbito, campo, tipo y condición.

## Apéndice A. Medidas y columnas calculadas

Columnas: tabla, nombre, origen (Medida del modelo, Medida de extensión, Columna calculada), descripción, DAX, formato, carpeta de visualización, oculta, y los números de los visuales que la usan. Si una medida cita otra en su DAX, la segunda aparece con "dependencia" o con los números de visual que la usan.

Sin `Model.bim`, esta sección dice que requiere el modelo y solo incluye las medidas de extensión que estén en el propio archivo.

## Apéndice B. Relaciones

Columnas: nombre, lado origen, lado destino, cardinalidad (con `(defecto)` cuando el archivo no la declara), filtro cruzado, si está activa y qué medidas la activan. La activación por medida se detecta cuando el DAX de la medida cita ambas columnas dentro de `USERELATIONSHIP` o `CROSSFILTER`; es una coincidencia textual.

## Apéndice C. Orígenes de datos

Orígenes del modelo (nombre, tipo, detalles de conexión, autenticación) y particiones de las tablas usadas (modo, tipo y expresión de origen).

## Recursos externos

Imágenes y otros recursos que aparecen en una captura: ID del visual, tipo, nombre del recurso y ruta dentro de `output/`. Si no se encuentra el archivo, la fila lo dice.
