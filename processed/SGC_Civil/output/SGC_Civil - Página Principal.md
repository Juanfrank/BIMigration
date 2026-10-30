# Página Principal: especificación de visuales

- Fuente: `SGC_Civil.pbip` (pbip)
- Modelo: Modo 'byConnection': no hay Model.bim local. Las secciones de modelo están pendientes.
- Capturas: 1.png
- Generado: 2026-10-30 01:18

## 1. Numeración

| Nº | Tipo | Título | ID visual | Capturas |
|---|---|---|---|---|
| 1 | azureMap | Mapa por Edificación | b1d432f4 | 1.png |
| 2 | cardVisual | Indicadores | 5638dd3f | 1.png |
| 3 | cardVisual | Indicadores | 5638dd3f | 1.png |
| 4 | cardVisual | Indicadores | 5638dd3f | 1.png |
| 5 | cardVisual | Indicadores | 5638dd3f | 1.png |
| 6 | cardVisual | Indicadores | 5638dd3f | 1.png |
| 7 | cardVisual | Indicadores | 5638dd3f | 1.png |
| 8 | slicer | Tipo Procedimiento | 7a39605b | 1.png |
| 9 | shapeMap | Mapa por Departamento Judicial | 7ccd466c | 1.png |
| 10 | TornadoChart1452517688218 | Asuntos más frecuentes | acfd0346 | 1.png |
| 11 | donutChart | Entrada | 4e5e8a90 | 1.png |
| 12 | advancedSlicerVisual | Año | ee601ddc | 1.png |
| 13 | advancedSlicerVisual | Semestre | 3e01e760 | 1.png |
| 14 | advancedSlicerVisual | Trim | 5cc80a9f | 1.png |
| 15 | advancedSlicerVisual | Asunto | 64dd690c | 1.png |
| 16 | slicer | Fechas | e38387e0 | 1.png |
| 17 | donutChart | Audiencias Transcurridas | 536bc030 | 1.png |
| 18 | slicer | Departamento / Distrito Judicial | 700b384b | 1.png |
| 19 | pivotTable | — | bbe15e97 | 1.png |
| 20 | slicer | Categoría | bc4a8ea0 | 1.png |
| 21 | slicer | Tipo Tribunal | ad3e6b34 | 1.png |
| 22 | slicer | Tribunal | 3cd11780 | 1.png |
| 23 | annotatedBarByQueryOn10945130E24B4D6AAD5741C12ECB533D | Duración según Intervalos | d0783a5c | 1.png |

## 2. Visuales y pozos de campos

### Nº 1: azureMap · Mapa por Edificación

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Size | vwSGJEntradaExpedientesBO.Entrada Trámites | Medida | — | Entrada Trámites |
| Tooltips | AGG3(Edificios.Edificio) | Agregación (Columna) | Edificio | Edificio |
| X | Edificios.Y | Columna | — | Y |
| Y | Edificios.X | Columna | — | X |

### Nº 2: cardVisual · Indicadores

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJEntradaExpedientesBO.Entrada Trámites | Medida | Entrada | Entrada Trámites |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJAudienciasBO.% Celebradas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.% Solución Trámites | Advanced | — | — |
| vwSGJAudienciasBO.Audiencias Transcurridas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Duración Cerrados | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Juez En Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | — |

### Nº 3: cardVisual · Indicadores

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJEntradaExpedientesBO.Salida Trámites | Medida | Salida | Salida Trámites |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJAudienciasBO.% Celebradas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.% Solución Trámites | Advanced | — | — |
| vwSGJAudienciasBO.Audiencias Transcurridas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Duración Cerrados | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Juez En Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | — |

### Nº 4: cardVisual · Indicadores

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJEntradaExpedientesBO.% Solución Trámites | Medida | % Solución | % Solución Trámites |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJAudienciasBO.% Celebradas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.% Solución Trámites | Advanced | — | — |
| vwSGJAudienciasBO.Audiencias Transcurridas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Duración Cerrados | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Juez En Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | — |

### Nº 5: cardVisual · Indicadores

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJAudienciasBO.Audiencias Transcurridas | Medida | — | Audiencias Transcurridas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJAudienciasBO.% Celebradas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.% Solución Trámites | Advanced | — | — |
| vwSGJAudienciasBO.Audiencias Transcurridas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Duración Cerrados | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Juez En Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | — |

### Nº 6: cardVisual · Indicadores

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJAudienciasBO.% Celebradas | Medida | — | % Celebradas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJAudienciasBO.% Celebradas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.% Solución Trámites | Advanced | — | — |
| vwSGJAudienciasBO.Audiencias Transcurridas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Duración Cerrados | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Juez En Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | — |

### Nº 7: cardVisual · Indicadores

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJEntradaExpedientesBO.Duración Cerrados | Medida | — | Duración Cerrados |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJAudienciasBO.% Celebradas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.% Solución Trámites | Advanced | — | — |
| vwSGJAudienciasBO.Audiencias Transcurridas | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Duración Cerrados | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | — |
| vwSGJEntradaExpedientesBO.Juez En Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | — |

### Nº 8: slicer · Tipo Procedimiento

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | vwSGJTipoProcedimiento.Tipo Procedimiento | Columna | — | Tipo Procedimiento |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJTipoProcedimiento.Tipo Procedimiento | Categorical | NOT (IN null) | — |

### Nº 9: shapeMap · Mapa por Departamento Judicial

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Category | vwRelacionTribunalSUSEC.cod_departamento_judicial | Columna | Cód. | cod_departamento_judicial |
| Value | vwSGJEntradaExpedientesBO.% Solución Trámites | Medida | — | % Solución Trámites |

### Nº 10: TornadoChart1452517688218 · Asuntos más frecuentes

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Category | vwSGJAsuntos.Asunto | Columna | — | Asunto |
| Values | vwSGJEntradaExpedientesBO.Entrada Trámites | Medida | Entrada | Entrada Trámites |
| Values | vwSGJEntradaExpedientesBO.Salida Trámites | Medida | Salida | Salida Trámites |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJTipoProcedimiento.Tipo Procedimiento | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Juez Salida | Advanced | — | User |

### Nº 11: donutChart · Entrada

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Category | vwSGJTipoProcedimiento.Tipo Procedimiento | Columna | — | Tipo Procedimiento |
| Y | vwSGJEntradaExpedientesBO.Entrada Trámites | Medida | — | Entrada Trámites |

### Nº 12: advancedSlicerVisual · Año

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas.Año | Columna | — | Año |

### Nº 13: advancedSlicerVisual · Semestre

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas.Semestre | Columna | — | Semestre |

### Nº 14: advancedSlicerVisual · Trim

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas.Trim. | Columna | — | Trim. |

### Nº 15: advancedSlicerVisual · Asunto

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Tooltips | vwSGJEntradaExpedientesBO.Registros | Medida | — | Registros |
| Values | vwSGJAsuntos.Asunto (origen) | Columna | — | Asunto (origen) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.Registros | Advanced | NOT (Comparison(kind=0) vwSGJEntradaExpedientesBO.Registros ? null) | — |

### Nº 16: slicer · Fechas

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas.Fechas | Columna | — | Fechas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Dim_Tipo_Tribunal.Tipo Tribunal (groups) | Categorical | NOT (IN null) | User |

### Nº 17: donutChart · Audiencias Transcurridas

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Category | vwSGJTipoResultados.Tipo Resultado (grupo2) | Columna | Tipo Resultado | Tipo Resultado (grupo2) |
| Y | vwSGJAudienciasBO.Audiencias Transcurridas con Resultado | Medida | — | Audiencias Transcurridas con Resultado |

### Nº 18: slicer · Departamento / Distrito Judicial

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | dvwTribunalesBO.DepartamentoJudicial | Columna | — | DepartamentoJudicial |
| Values | dvwTribunalesBO.Distrito Judicial | Columna | — | Distrito Judicial |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.Registros | Advanced | NOT (Comparison(kind=0) vwSGJEntradaExpedientesBO.Registros ? null) | User |

### Nº 19: pivotTable

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Rows | dvwTribunalesBO.DepartamentoJudicial | Columna | Departamento Judicial | DepartamentoJudicial |
| Rows | dvwTribunalesBO.Distrito Judicial | Columna | — | Distrito Judicial |
| Rows | Dim_Tipo_Tribunal.Tipo Tribunal (groups) | Columna | Tipo Tribunal | Tipo Tribunal (groups) |
| Rows | dvwSalasBO.NombreCorto | Columna | Sala | NombreCorto |
| Values | vwSGJEntradaExpedientesBO.Entrada Trámites | Medida | Entrada | Entrada Trámites |
| Values | vwSGJEntradaExpedientesBO.Entrada Trámites por Día | Medida | — | Entrada Trámites por Día |
| Values | vwSGJEntradaExpedientesBO.Salida Trámites | Medida | Salida | Salida Trámites |
| Values | vwSGJEntradaExpedientesBO.% Solución Trámites | Medida | % Sol. | % Solución Trámites |
| Values | vwSGJEntradaExpedientesBO.Mediana en Sala | Medida | Duración | Mediana en Sala |

### Nº 20: slicer · Categoría

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Dim_Instancia.Categoría | Columna | — | Categoría |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Dim_Instancia.Categoría | Categorical | — | — |
| vwSGJEntradaExpedientesBO.Registros | Advanced | NOT (Comparison(kind=0) vwSGJEntradaExpedientesBO.Registros ? null) | User |

### Nº 21: slicer · Tipo Tribunal

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Dim_Tipo_Tribunal.Tipo Tribunal (groups) | Columna | — | Tipo Tribunal (groups) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Dim_Tipo_Tribunal.Tipo Tribunal (groups) | Categorical | NOT (IN null) | — |

### Nº 22: slicer · Tribunal

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | dvwTribunalesBO.Tribunal | Columna | — | Tribunal |
| Values | dvwSalasBO.NombreCorto | Columna | — | NombreCorto |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.Registros | Advanced | NOT (Comparison(kind=0) vwSGJEntradaExpedientesBO.Registros ? null) | User |

### Nº 23: annotatedBarByQueryOn10945130E24B4D6AAD5741C12ECB533D · Duración según Intervalos

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| measure | vwSGJEntradaExpedientesBO.Duración Sorteo | Medida | Sorteo | Duración Sorteo |
| measure | vwSGJAudienciasBO.Intervalo Entrada Fijación | Medida | Entrada - Fijación | Intervalo Entrada Fijación |
| measure | vwSGJAudienciasBO.Intervalo Fijación 1ra. | Medida | Fijación - 1ra. Aud. | Intervalo Fijación 1ra. |
| measure | vwSGJAudienciasBO.Intervalo Primera Ultima Audiencia | Medida | Instrucción | Intervalo Primera Ultima Audiencia |
| measure | vwSGJEntradaExpedientesBO.Duración EstadoFallo-Salida AVG | Medida | Fallo | Duración EstadoFallo-Salida AVG |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJTipoProcedimiento.Tipo Procedimiento | Categorical | IN 'CONTENCIOSO', 'GRACIOSO' | User |

## 3. Filtros de página e informe

| Ámbito | Campo | Tipo | Condición |
|---|---|---|---|
| Informe | Fechas.Fechas | Advanced | Comparison(kind=2) Fechas.Fechas ? DateSpan(datetime'2021-06-14T00:00:00', unidad=5) |
| Informe | dvwTribunalesBO.DepartamentoJudicial | Categorical | NOT (IN null) |
| Informe | Dim_Tipo_Tribunal.Materia Tribunal | Categorical | IN 'CIVIL' |
| Informe | Dim_Instancia.Categoría | Categorical | NOT (IN 'JUZGADOS DE PAZ') |

## Apéndice A. Medidas y columnas calculadas

Requiere definición del modelo (Model.bim). No se puede completar esta sección.

## Apéndice B. Relaciones

Requiere definición del modelo (Model.bim). No se puede completar esta sección.

## Apéndice C. Orígenes de datos

Requiere definición del modelo (Model.bim). No se puede completar esta sección.

## Recursos externos

| ID visual | Tipo | Referencia en el visual | Archivo en output/ |
|---|---|---|---|
| b1d432f4 | azureMap | DEPJ_BI582906550240508.geojson | resources/DEPJ_BI582906550240508.geojson |
| 7ccd466c | shapeMap | DEPJ_BI659385776850175.json | resources/DEPJ_BI659385776850175.json |
| ab3a3935 | image | LOGO_NUEVO_PJ-0445749737862337536.png | resources/LOGO_NUEVO_PJ-0445749737862337536.png |
| 4063d690 | actionButton | pngegg_W5231039035730467.png | resources/pngegg_W5231039035730467.png |
