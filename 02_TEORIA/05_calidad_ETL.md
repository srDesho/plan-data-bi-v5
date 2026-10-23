# Capítulo 5 — Calidad de datos y ETL: un proceso que puedas defender

ETL significa extraer, transformar y cargar. Este capítulo te enseña a diseñar un proceso de datos **que puedas explicar y repetir**: las capas Bronze, Silver y Gold, el contrato de datos que se escribe antes de programar, el tratamiento de duplicados y rechazos con su ecuación de auditoría, las cargas repetibles con registro y la organización del código en cuatro funciones. Los ejemplos usan datos inventados y no revelan las soluciones de los ejercicios ni de la evaluación final.

**Tiempo total estimado de primera vez:** unas 4 h 35 min (5 lecciones). Se lee mejor después del capítulo 10 (Pandas): allí se implementan los controles que aquí se diseñan.

**Antes de empezar:** capítulos 8, 9 y 10; en especial 8.5 (excepciones), 9.5 (nulos y duplicados), 10.3 (merge) y 10.5 (controles).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 5.1 | [ETL, ELT y capas Bronze, Silver y Gold](05_calidad_ETL/01_etl_elt_medallon.md) | el mapa de un proyecto de datos; la ecuación de auditoría | NÚCLEO · D22 | 50 min |
| 5.2 | [El contrato de datos](05_calidad_ETL/02_contrato_de_datos.md) | escribir las reglas antes de programar; detener frente a rechazar | NÚCLEO · D23 | 50 min |
| 5.3 | [Rechazos, duplicados y reconciliación](05_calidad_ETL/03_rechazos_y_reconciliacion.md) | exactos frente a conflictos, imputación con condición, centavos, cuadre de valor | NÚCLEO · D24 | 55 min |
| 5.4 | [Cargas repetibles, registro y reproducibilidad](05_calidad_ETL/04_cargas_registro_reproducibilidad.md) | idempotencia, carga atómica, `logging`, parámetros | NÚCLEO · D24 | 55 min |
| 5.5 | [Estructura de un ETL en funciones](05_calidad_ETL/05_estructura_etl_funciones.md) | extraer, transformar, validar, cargar y un `main` corto | NÚCLEO · D23 | 65 min |

## Ideas centrales

- Bronze conserva lo que llegó; Silver, lo válido con tipos y claves; los rechazos explican lo que no pasó; Gold alimenta el reporte.
- Si no puedes decidir, para tres filas escritas a mano, cuáles pasan y cuáles se rechazan, todavía no estás listo para programar el pipeline.
- Error de **estructura** → detener; error de **fila** → rechazar con motivo.
- `filas Bronze = duplicados exactos + rechazados + filas Silver`, y además se cuadra el **valor** entre capas: el número de filas correcto por sí solo no detecta importes multiplicados.
- Ante un conflicto de clave no se conserva «la primera»: se detiene o se envía a revisión.
- Una segunda ejecución debe producir iguales filas y totales, no duplicarlos. Publica en un archivo temporal y reemplaza el destino solo si todo pasó; en Windows cierra la conexión SQLite antes (`closing`).
- Un registro (log) con etapa, conteos y motivos; nunca claves ni datos privados.

## Ejercicios autónomos de este capítulo

El proyecto ETL en etapas ([`05_PROYECTOS/`](../05_PROYECTOS/)), el mini-ETL ME01–ME04 ([`03_EJERCICIOS/Puente/`](../03_EJERCICIOS/Puente/)), P21–P30 y los casos C04 y C06. La referencia validada de los ejercicios está separada de las actividades: no la abras antes de terminar tu intento. Las microprácticas de las lecciones no son evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 6 — KPIs](06_KPIs.md).
