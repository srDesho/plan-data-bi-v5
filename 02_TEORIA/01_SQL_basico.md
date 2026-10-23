# Capítulo 1 — SQL desde cero: una pregunta, una tabla y un resultado

Este capítulo te enseña a leer una tabla y a pedirle datos con `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT` y `LIKE`, sin saber nada de bases de datos. Todos los ejemplos usan la **mini-base inventada** de `04_DATASETS/mini_base/` ([README](../04_DATASETS/mini_base/README.md)), no los datos de los ejercicios.

**Tiempo total estimado:** unos 5 h de primera vez (lectura y micropráctica de las 7 lecciones). No lo hagas de una sola vez: una o dos lecciones por sesión y después los ejercicios.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 1.1 | [Tablas, filas, columnas y tipos](01_SQL_basico/01_tablas_filas_columnas.md) | base de datos, tabla, fila, columna, clave primaria, granularidad, NULL | NÚCLEO · D01 | 45 min |
| 1.2 | [SELECT, FROM, alias](01_SQL_basico/02_select_from_alias.md) | elegir columnas, alias, columnas calculadas | NÚCLEO · D01–D02 | 53 min |
| 1.3 | [WHERE y operadores](01_SQL_basico/03_where_operadores.md) | condiciones, AND/OR/NOT, IN, BETWEEN, paréntesis | NÚCLEO · D02 | 56 min |
| 1.4 | [NULL](01_SQL_basico/04_null.md) | IS NULL, lógica de tres valores, filas que se pierden | NÚCLEO · D02 | 40 min |
| 1.5 | [ORDER BY y LIMIT](01_SQL_basico/05_order_limit.md) | orden, desempates, Top N, OFFSET | NÚCLEO · D03 | 40 min |
| 1.6 | [DISTINCT y LIKE](01_SQL_basico/06_distinct_like.md) | valores únicos, patrones, datos sucios | NÚCLEO · D02–D03 | 47 min |
| 1.7 | [Del requerimiento a la consulta](01_SQL_basico/07_del_requerimiento_a_la_consulta.md) | método de cinco preguntas, verificación | COMPLEMENTARIA | 40 min |

## Cómo estudiar este capítulo

1. Lee la lección con la mini-base a mano (`python herramientas/ejecutar_sql.py --db 04_DATASETS/mini_base/mini_base.db --consulta "SELECT * FROM tiendas LIMIT 3;"`).
2. **Escribe** cada ejemplo tú mismo en lugar de copiarlo; cambia un valor y predice el resultado antes de ejecutar.
3. Haz la micropráctica sin mirar la comprobación. Después compárala.
4. Cuando termines la lección 1.2 ya puedes abrir los primeros ejercicios.

## Ejercicios autónomos de este capítulo

Serie S (S1–S10) en [`03_EJERCICIOS/SQL/`](../03_EJERCICIOS/SQL/INDICE.md). Las microprácticas de las lecciones **no** son ejercicios evaluables: no tienen corrector ni cuentan para el progreso; sirven para que llegues listo al ejercicio.

## Si te trabas

- Un error de sintaxis casi siempre está en una coma, una comilla o un punto y coma. Lee el mensaje completo.
- Si el resultado "parece bien" pero no cuadra, revisa primero filtros (¿estado? ¿NULL?) y luego granularidad.
- Términos: [glosario](GLOSARIO.md). Fuentes oficiales: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 2 — Agregar sin perder el significado](02_SQL_agregados.md).
