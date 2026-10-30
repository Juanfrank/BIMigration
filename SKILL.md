---
name: bi-report-spec
description: Extrae la especificación de una página de un reporte Power BI (.pbip o .pbix) a partir del archivo y de capturas de esa página. Numera los visuales sobre las capturas y genera un .md con pozos de campos, filtros, medidas/columnas (DAX), relaciones, orígenes de datos y recursos externos. Úsala cuando el usuario pida documentar, replicar o inventariar los visuales de una página de Power BI.
---

# bi-report-spec

Convierte un reporte Power BI en documentación reproducible. Usa scripts para todo lo mecánico; tu trabajo es reunir las entradas, pedir lo que falte y comunicar qué se generó y qué quedó pendiente.

Detalles del proceso, reglas de numeración y limitaciones: [docs/PROCESO.md](docs/PROCESO.md). Formato del .md: [docs/FORMATO.md](docs/FORMATO.md).

## Entradas

| Entrada | Obligatoria | Notas |
|---|---|---|
| Archivo `.pbip` (con su carpeta `.Report` y, si existe, `.SemanticModel`) o `.pbix` | Sí | |
| Una o más capturas de la(s) página(s) | Sí | PNG o JPG. |
| Nombre de la página | Sí | Si el usuario no la dice, el script la lista y debes preguntarla. |
| `Model.bim` del modelo | Solo si el reporte no trae el modelo en local | Un reporte con `byConnection` (modelo remoto) lo necesita para los apéndices de medidas, relaciones y orígenes. |
| Escenario de cada captura | No, pero necesario si la captura no está en el estado guardado | Estado en que se tomó la captura: `Default` o el nombre de un bookmark de la página (p. ej., un panel abierto desde un botón). |
| Dos o más anclas de calibración | No, pero recomendadas | Pares `ID_VISUAL=px,py` con la esquina superior izquierda de un visual en la captura. Sin anclas, la numeración sobre la captura es aproximada. |

## Procedimiento

1. **Confirma las entradas.** Si falta la página, ejecuta el script una vez: devuelve código de salida `2` y lista las páginas. Pregunta al usuario cuál es.
2. **Modelo.** Si `definition.pbir` tiene `byConnection` y el usuario no aporta `Model.bim`, pregunta si lo aporta o si prefiere omitirlo. Si omite, los apéndices A, B y C dirán que requieren el modelo; no los elimines.
3. **Ejecuta:**

   ```bash
   python scripts/run_skill.py --source "<ruta>/Archivo.pbip" --page "<Página>" --captures "<captura1.png>" "<captura2.png>" --anchor "<ID_VISUAL>=<px>,<py>" --anchor "<ID_VISUAL>=<px>,<py>" --model "<Model.bim>"
   ```

   Omite `--anchor` y `--model` si no aplican.

4. **Escenarios.** Mira cada captura y decide en qué estado está: el guardado (`Default`) o un bookmark (`MenuA`, `MenuC`…). Lista los bookmarks con `numbering.json` (`scenarios`). Pásalo como `--scenario "captura.png=Escenario"` en la ejecución. El script no lo detecta solo.
5. **Revisa la salida.** Abre la captura numerada y su `- contornos.png`. Compara: cada badge debe caer sobre su visual, y los contornos deben coincidir con lo que muestra la captura (paneles abiertos, visuales ocultos). Si no coincide, cambia el escenario declarado; si los números no caen donde deben, pide al usuario dos anclas y vuelve a ejecutar.
6. **Informa.** Indica la carpeta generada, los escenarios usados, cuántos visuales se numeraron en cada captura, qué badges quedan tapados por otro visual y qué secciones quedaron pendientes (modelo, recursos no encontrados).

## Salida

Por archivo analizado, dentro de `processed/` en la raíz del repo:

```
processed/<Archivo>/
  source/    archivo, carpetas .Report/.SemanticModel, capturas originales, Model.bim (si se dio)
  output/    capturas numeradas, "<Archivo> - <Página>.md", resources/, datos/ (JSON intermedios)
```

## Reglas que no debes cambiar

- La numeración la fija el script por página, no por captura. Un mismo visual tiene siempre el mismo número.
- Solo se numeran visuales con campos (medidas o columnas). Formas, textos, imágenes y grupos se omiten.
- No inventes DAX, descripciones ni relaciones. Si un dato no está en el archivo o en el `Model.bim`, el .md lo dice.
- Los recursos externos (imágenes, SVG, shapes) se copian a `output/resources/` solo si están en una captura.
- No subas al repo ni hagas commit sin que el usuario lo pida.
- La redacción (`scripts/redact.py`) está activa por defecto en todas las salidas y en la copia de fuentes. No uses `--raw` para algo que vaya a versionarse. El `Model.bim` no se copia al repo.
- Las capturas no se redactan: revise que no muestren servidores o credenciales.
