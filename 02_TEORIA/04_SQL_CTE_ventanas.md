# Capítulo 4 — Subconsultas, CTE, ventanas, fechas e índices

Con los capítulos 1–3 ya puedes filtrar, agrupar y unir. Este capítulo te da las herramientas para cálculos de **varios pasos**: subconsultas y CTE, funciones de ventana (puestos, acumulados, mes anterior) y la construcción de indicadores con fecha de corte. Cierra con una primera mirada a cómo saber si una consulta es lenta. Todos los ejemplos usan la mini-base de `04_DATASETS/mini_base/` ([README](../04_DATASETS/mini_base/README.md)).

**Tiempo total estimado:** unas 3 h 35 min de primera vez (4 lecciones). La lección 4.3 (ventanas) es la más exigente: léela en una sesión propia.

**Antes de empezar:** capítulos 1–3, sobre todo GROUP BY, LEFT JOIN y los controles de 3.4.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 4.1 | [Subconsultas](04_SQL_CTE_ventanas/01_subconsultas.md) | escalar, de lista, en FROM, EXISTS, la trampa de NOT IN con NULL | NÚCLEO · D18 | 50 min |
| 4.2 | [CTE con WITH](04_SQL_CTE_ventanas/02_cte.md) | dividir en pasos con nombre, depurar paso a paso | NÚCLEO · D18 | 45 min |
| 4.3 | [Funciones de ventana](04_SQL_CTE_ventanas/03_ventanas.md) | OVER, PARTITION BY, ROW_NUMBER/RANK/DENSE_RANK, acumulados, LAG | NÚCLEO · D18 | 65 min |
| 4.4 | [SQL para indicadores, fechas y rendimiento](04_SQL_CTE_ventanas/04_sql_kpis_fechas_rendimiento.md) | fecha de corte, activos/inactivos, crecimiento, EXPLAIN QUERY PLAN, notas de SQL Server | COMPLEMENTARIA | 55 min |

## Idea central del capítulo

Una subconsulta o una CTE no son magia: son pasos. Escribe cada paso con su granularidad («una fila por venta», «una fila por ruta») y verifícalo por separado. Una función de ventana **no colapsa** filas; una condición sobre una ventana se filtra en una consulta externa. Un indicador siempre lleva su definición escrita y su fecha de corte.

Una CTE no es una tabla guardada y no mejora el rendimiento por sí sola. Los ejemplos de SQL Server son referencia conceptual: en este curso no se ejecutaron en SQL Server.

## Ejercicios autónomos de este capítulo

K1–K6, V1–V5, X1–X8, N5–N7, N13 y N15 en [`03_EJERCICIOS/SQL/`](../03_EJERCICIOS/SQL/INDICE.md). Las microprácticas de las lecciones no son ejercicios evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 5 — Calidad de datos y ETL](05_calidad_ETL.md).
