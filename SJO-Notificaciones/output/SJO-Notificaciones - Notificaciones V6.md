# Notificaciones V6: especificación de visuales

- Fuente: `SJO-Notificaciones.pbip` (pbip)
- Modelo: Modo 'byConnection': no hay Model.bim local. Las secciones de modelo están pendientes.
- Capturas: 1.png
- Generado: 2026-10-29 21:06

## 1. Numeración

| Nº | Tipo | Título | ID visual | Capturas |
|---|---|---|---|---|
| 1 | InforiverFilterF39DAE8D57A743EF89F5C3809DEE2B69 | — | 08f4e37c | 1.png |
| 2 | advancedSlicerVisual | — | 4985da4b | 1.png |
| 3 | advancedSlicerVisual | — | 3411f057 | 1.png |
| 4 | card | Fecha de actualización | 95671549 | 1.png |
| 5 | advancedSlicerVisual | — | 90c7f51b | 1.png |
| 6 | cardVisual | — | 3bce1c7c | 1.png |
| 7 | cardVisual | — | e24114a7 | 1.png |
| 8 | cardVisual | — | 6114b10a | 1.png |
| 9 | cardVisual | — | 5e46eef5 | 1.png |
| 10 | cardVisual | — | 7ed117ae | 1.png |
| 11 | cardVisual | — | d968887b | 1.png |
| 12 | cardVisual | — | 1c48aef5 | 1.png |
| 13 | slicer | Unidades de Notificación | b0731946 | 1.png |
| 14 | slicer | — | 8cebc024 | 1.png |
| 15 | tableEx | WIP-Pendiente de preparar (bandeja) | 78052e68 | 1.png |
| 16 | tableEx | ENTRADA | 37839220 | 1.png |
| 17 | slicer | — | bb9e0fbe | 1.png |
| 18 | card | WIP-Pendiente de preparar (bandeja) | caac1260 | 1.png |
| 19 | slicer | — | d49536e1 | 1.png |
| 20 | pivotTable | SALIDA | bdef301e | 1.png |
| 21 | card | WIP-Pendiente de preparar (bandeja) | ae411559 | 1.png |
| 22 | card | WIP-Pendiente de preparar (bandeja) | 39233a1e | 1.png |
| 23 | card | WIP-Pendiente de preparar (bandeja) | 67daee63 | 1.png |
| 24 | card | WIP-Pendiente de preparar (bandeja) | d332edc0 | 1.png |
| 25 | card | WIP-Pendiente de preparar (bandeja) | cf157400 | 1.png |
| 26 | card | WIP-Pendiente de preparar (bandeja) | be0a5484 | 1.png |
| 27 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | f75ae06a | 1.png |
| 28 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 34faf656 | 1.png |
| 29 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | c4d0aa60 | 1.png |
| 30 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 735c58ab | 1.png |
| 31 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 76dc1c81 | 1.png |
| 32 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | f3c89b7d | 1.png |
| 33 | card | WIP-Pendiente de preparar (bandeja) | dc65746a | 1.png |
| 34 | card | WIP-Pendiente de preparar (bandeja) | 1d479bd0 | 1.png |
| 35 | card | WIP-Pendiente de preparar (bandeja) | 9ed753e7 | 1.png |
| 36 | card | WIP-Pendiente de preparar (bandeja) | 007a0675 | 1.png |
| 37 | card | WIP-Pendiente de preparar (bandeja) | 1c9a5f60 | 1.png |
| 38 | card | WIP-Pendiente de preparar (bandeja) | 33340b41 | 1.png |
| 39 | card | WIP-Pendiente de preparar (bandeja) | 9b678146 | 1.png |
| 40 | card | WIP-Pendiente de preparar (bandeja) | eea9f12e | 1.png |
| 41 | card | WIP-Pendiente de preparar (bandeja) | 458633c4 | 1.png |
| 42 | card | WIP-Pendiente de preparar (bandeja) | 6eeb4760 | 1.png |
| 43 | pivotTable | SALIDA | 544fb243 | 1.png |
| 44 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 5aee69f7 | 1.png |
| 45 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | b0f38c02 | 1.png |
| 46 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 8708123d | 1.png |
| 47 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 2cc43c81 | 1.png |
| 48 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 76f8ad18 | 1.png |
| 49 | cardVisual | TIEMPOS Y EFICIENCIA DEL PROCESO | 958210f6 | 1.png |
| 50 | card | WIP-Pendiente de preparar (bandeja) | 5733e401 | 1.png |

## 2. Visuales y pozos de campos

### Nº 1: InforiverFilterF39DAE8D57A743EF89F5C3809DEE2B69

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| column | Fechas.Fechas | Columna | — | Fechas |

### Nº 2: advancedSlicerVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas.Año | Columna | — | Año |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Etapas.Etapa | Categorical | NOT (IN null) | User |
| Fechas.Año | Advanced | Comparison(kind=2) Fechas.Año ? 2023L | — |

### Nº 3: advancedSlicerVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas.Trim. | Columna | — | Trim. |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Etapas.Etapa | Categorical | NOT (IN null) | User |

### Nº 4: card · Fecha de actualización

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Refresh.FActualizacion | Medida | Fecha de actualización | FActualizacion |

### Nº 5: advancedSlicerVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Fechas[Fechas Hierarchy].MesN | Nivel de jerarquía | — | MesN |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Etapas.Etapa | Categorical | NOT (IN null) | User |
| Tipo Falloo Salida.TipoFallo | Advanced | — | User |

### Nº 6: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Lead Time Solicitud Citación | Medida | Dias Antelacion Solicitud Citaciones | Lead Time Solicitud Citación |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Lead Time Solicitud Citación | Advanced | — | — |

### Nº 7: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Lead Time Solicitud Notificación | Medida | Dias solicitud Notificaciones despues de firmar | Lead Time Solicitud Notificación |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Lead Time Solicitud Notificación | Advanced | — | — |

### Nº 8: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | Requerimientos Solicitados | Notificaciones Solicitadas |
| Data | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Cargadas | Medida | Requerimientos Completados | Notificaciones Cargadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |

### Nº 9: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Medida | % Solución TOTAL | % Notificaciones Cargadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Advanced | — | — |

### Nº 10: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | vwSGJAudienciasBO.% Audiencias Aplazadas por Motivo de Notificacion | Medida | % Audiencias Aplazadas por Not. (Nacional) | % Audiencias Aplazadas por Motivo de Notificacion |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(DateAdd(Now(), -1, unidad=0), 1, unidad=0), -3, unidad=2), unidad=0) Y DateSpan(DateAdd(Now(), -1, unidad=0), unidad=0) | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Fuera de Plazo | Advanced | — | User |
| vwSGJAudienciasBO.% Audiencias Aplazadas por Motivo de Notificacion | Advanced | — | — |

### Nº 11: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Fuera de Plazo | Medida | % Citaciones Fuera de Plazo | % Notificaciones Fuera de Plazo |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Fuera de Plazo | Advanced | — | — |

### Nº 12: cardVisual

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Recibidas (> 1 Traslado) | Medida | % Domicilio desconocido | % Notificaciones Recibidas (> 1 Traslado) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| vwSGJEntradaExpedientesBO.% Solución (Entrada) | Advanced | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Dim_Instancia.Categoría | Categorical | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | — | User |
| vwSGJProductos.Duración Firma (desde Carga) | Advanced | — | User |
| vwSGJProductos.Duración Firma | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Entrada Trámites | Advanced | — | User |
| vwSGJEstatus.Estatus | Categorical | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salas sin Mora % | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Salida Trámites | Advanced | — | User |
| vwSGJEntradaExpedientesBO.Total Salas | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Recibidas (> 1 Traslado) | Advanced | — | — |

### Nº 13: slicer · Unidades de Notificación

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | dvwSalasNotificaciones.Sala | Columna | UN | Sala |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Etapas.Etapa | Categorical | NOT (IN null) | User |
| Tipo Falloo Salida.TipoFallo | Advanced | — | User |
| dvwTribunalesBO.DepartamentoJudicial | Categorical | NOT (IN null) | User |
| dvwSalasNotificaciones.Sala | Advanced | CONTAINS 'noti' | — |

### Nº 14: slicer

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | vwSGJAsuntos.Asunto | Columna | — | Asunto |

### Nº 15: tableEx · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Estatus Solicitud.Estatus Solicitud | Columna | Desperdicios | Estatus Solicitud |
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida |   | Notificaciones Solicitadas |
| Values | (Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas op3 Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas) | Aritmética |    | — |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 12L, 116L, 103L | — |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 16: tableEx · ENTRADA

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | Entrada Prom. por Dia | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Fechas[Fechas Hierarchy].Año | Advanced | — | User |
| vwSGJAsuntos.Asunto (origen) | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Fechas[Fechas Hierarchy].Dia | Advanced | — | User |
| Statistical Functions.Label ESP | Categorical | IN 'Diario Laboral AVG' | User |
| Fechas[Fechas Hierarchy].MesN | Advanced | — | User |
| dvwSalasNotificaciones.Sala | Categorical | — | User |
| Fechas[Fechas Hierarchy].Semana | Advanced | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| dvwTribunalesBO.Tribunal | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Advanced | — | — |

### Nº 17: slicer

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Edificios.Edificio | Columna | — | Edificio |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Edificios.Edificio | Categorical | NOT (IN null) | — |

### Nº 18: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 116L, 103L, 12L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 19: slicer

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Dim_Tipo_Tribunal.Materia Tribunal | Columna | — | Materia Tribunal |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Edificios.Edificio | Categorical | NOT (IN null) | User |
| Dim_Tipo_Tribunal.Materia Tribunal | Categorical | NOT (IN null) | — |

### Nº 20: pivotTable · SALIDA

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Rows | penal_vwViasNotificacionCitacion_ccn.Via | Columna | — | Via |
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | Solicitadas | Notificaciones Solicitadas |
| Values | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Medida | % Solución  | % Notificaciones Cargadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | — | User |

### Nº 21: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 95L, 125L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Advanced | — | — |

### Nº 22: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 4L, 107L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 23: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 108L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 24: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 97L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 25: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 96L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 26: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 106L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 27: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Notificación (Carga) | Medida | — | Duración Notificación (Carga) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Notificación (Carga) | Advanced | — | — |

### Nº 28: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Solicitud - Asignacion | Medida | Preparacion Asignacion  | Duración Solicitud - Asignacion |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Solicitud - Asignacion | Advanced | — | — |

### Nº 29: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Medida | — | Duración Entrega - Recepción |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | — |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |

### Nº 30: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Medida | — | Duración Recepción - Carga |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(Now(), -90, unidad=1), unidad=1) Y DateSpan(DateAdd(Now(), -1, unidad=1), unidad=1) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | — |

### Nº 31: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Medida | — | % Notificaciones Cargadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Advanced | — | — |

### Nº 32: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Recibidas (> 1 Traslado) | Medida | — | % Notificaciones Recibidas (> 1 Traslado) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Recibidas (> 1 Traslado) | Advanced | — | — |

### Nº 33: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 4L, 107L, 95L, 108L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 34: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Fuera de Plazo | Medida | — | % Notificaciones Fuera de Plazo |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 4L, 107L, 95L, 108L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 35: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Fuera de Plazo | Medida | — | % Notificaciones Fuera de Plazo |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 97L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 36: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Fuera de Plazo | Medida | — | % Notificaciones Fuera de Plazo |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 96L, 118L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Citación', 'Notificación de Citación y Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 37: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 95L, 125L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 38: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 4L, 107L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |

### Nº 39: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 108L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 40: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 97L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 41: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 96L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 42: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 106L | — |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

### Nº 43: pivotTable · SALIDA

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Rows | penal_vwMediosNotificaciones_ccn.MedioNotificacion | Columna | Medio | MedioNotificacion |
| Values | (Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Cargadas op3 Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Cargadas) | Aritmética | % | — |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | — | User |

### Nº 44: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Notificación (Carga) | Medida | — | Duración Notificación (Carga) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Notificación (Carga) | Advanced | — | — |

### Nº 45: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Medida | — | % Notificaciones Cargadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Cargadas | Advanced | — | — |

### Nº 46: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Solicitud - Asignacion | Medida | Preparacion Asignacion  | Duración Solicitud - Asignacion |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Solicitud - Asignacion | Advanced | — | — |

### Nº 47: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Medida | — | Duración Entrega - Recepción |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | — |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |

### Nº 48: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Medida | — | Duración Recepción - Carga |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(Now(), -30, unidad=1), unidad=1) Y DateSpan(DateAdd(Now(), -1, unidad=1), unidad=1) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | — |

### Nº 49: cardVisual · TIEMPOS Y EFICIENCIA DEL PROCESO

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Data | Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Recibidas (> 1 Traslado) | Medida | — | % Notificaciones Recibidas (> 1 Traslado) |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Penal_vwSolicitudesNotificaciones_ccn.Duración Entrega - Recepción | Advanced | — | User |
| Time Intelligence.Label ESP | Categorical | — | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Fechas.Fechas | RelativeDate | BETWEEN DateSpan(DateAdd(DateAdd(Now(), 1, unidad=0), -90, unidad=0), unidad=0) Y DateSpan(Now(), unidad=0) | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.Duración Recepción - Carga | Advanced | — | User |
| Penal_vwSolicitudesNotificaciones_ccn.% Notificaciones Recibidas (> 1 Traslado) | Advanced | — | — |

### Nº 50: card · WIP-Pendiente de preparar (bandeja)

| Pozo | Campo | Tipo | Nombre visible | Propiedad |
|---|---|---|---|---|
| Values | Penal_vwSolicitudesNotificaciones_ccn.Notificaciones Solicitadas | Medida | — | Notificaciones Solicitadas |

Filtros del visual:

| Campo | Tipo | Condición | Origen |
|---|---|---|---|
| Estatus Solicitud.Estatus Solicitud | Categorical | IN 4L, 68L, 107L, 95L, 125L, 132L, 108L | User |
| Penal_vwTipoRequerimiento_ccn.TipoRequerimiento | Categorical | IN 'Notificación de Documento' | User |
| Penal_vwTipoRequerimiento_ccn.IdTipoRequerimiento | Advanced | — | User |

## 3. Filtros de página e informe

| Ámbito | Campo | Tipo | Condición |
|---|---|---|---|
| Informe | Fechas.Año | Advanced | Comparison(kind=2) Fechas.Año ? 2022L |
| Informe | Dim_Tipo_Tribunal.Materia Tribunal | Categorical | — |

## Apéndice A. Medidas y columnas calculadas

Requiere definición del modelo (Model.bim). No se puede completar esta sección.

## Apéndice B. Relaciones

Requiere definición del modelo (Model.bim). No se puede completar esta sección.

## Apéndice C. Orígenes de datos

Requiere definición del modelo (Model.bim). No se puede completar esta sección.

## Recursos externos

| ID visual | Tipo | Referencia en el visual | Archivo en output/ |
|---|---|---|---|
| 3d5538e0 | image | VSM_NOTIFICACION_v24481773487694414.png | resources/VSM_NOTIFICACION_v24481773487694414.png |
| d067dff1 | image | Notificaciones9366700892286483.png | resources/Notificaciones9366700892286483.png |
| f5c0b78d | image | Logo_Poder_Judicial6505735048255952.png | resources/Logo_Poder_Judicial6505735048255952.png |
