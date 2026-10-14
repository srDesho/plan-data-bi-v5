# Capítulo 3 — JOIN: conectar tablas y controlar multiplicaciones

Aquí aprendes a combinar tablas (tiendas con ventas, ventas con su detalle) y, sobre todo, a **no equivocarte sin darte cuenta**: un JOIN mal planteado no da error, devuelve cifras infladas. Todos los ejemplos usan la mini-base inventada de `04_DATASETS/mini_base/` ([README](../04_DATASETS/mini_base/README.md)).

**Tiempo total estimado:** unas 3 h 35 min de primera vez (4 lecciones). Recomendado: dos sesiones; la lección 3.4 conviene leerla con calma y repetirla una semana después.

**Antes de empezar:** capítulos 1 y 2, en especial GROUP BY y la lección de granularidad (2.3).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 3.1 | [Claves, relaciones y cardinalidad](03_SQL_joins/01_claves_relaciones.md) | clave primaria y foránea, 1:N, N:M, tabla puente, comprobar unicidad | refuerzo | 45 min |
| 3.2 | [INNER JOIN](03_SQL_joins/02_inner_join.md) | ON, alias, unir tres tablas, producto cartesiano, controles de filas y totales | núcleo · D09 | 60 min |
| 3.3 | [LEFT JOIN y los que no aparecen](03_SQL_joins/03_left_join_ausentes.md) | conservar todo lo de la izquierda, anti-join, `COUNT(columna)`, filtro en ON o WHERE | núcleo · D11 | 55 min |
| 3.4 | [Cuando el JOIN duplica](03_SQL_joins/04_duplicacion_por_join.md) | duplicación, doble conteo, agregar antes de unir, tres controles | núcleo · D11 | 55 min |

## Idea central del capítulo

El JOIN combina filas que cumplen una condición; no sabe cuál era tu intención de negocio. Antes de unir di en voz alta: «una fila de A corresponde a ___ filas de B». Después de unir, comprueba tres cosas: **filas antes y después**, **claves huérfanas** (con LEFT JOIN + IS NULL) y **un total conocido** calculado por otro camino.

No unas por nombres de negocio. No uses `DISTINCT` para ocultar un JOIN incorrecto: primero explica por qué aparecen duplicados. Esta misma regla se aplica en Pandas ([capítulo 10](10_Pandas_transformaciones.md)), en Excel y en Power BI.

## Ejercicios autónomos de este capítulo

Series J (J1–J6) y E (E1–E8), N8 y N9 en [`03_EJERCICIOS/SQL/`](../03_EJERCICIOS/SQL/INDICE.md). El proyecto SQL exige una nota sobre la cardinalidad de cada unión. Las microprácticas de las lecciones no son ejercicios evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 4 — Subconsultas, ventanas, fechas e índices](04_SQL_CTE_ventanas.md).
