# Capítulo 2 — Agregar sin perder el significado

Aquí pasas de "listar filas" a "responder cuánto, cuántos y cuál": contar, sumar, promediar y agrupar, y sobre todo **elegir el número correcto** para la pregunta. Todos los ejemplos usan la mini-base inventada de `04_DATASETS/mini_base/` ([README](../04_DATASETS/mini_base/README.md)).

**Tiempo total estimado:** unas 4 h 20 min de primera vez (5 lecciones). Hazlo en tres sesiones como mucho, intercaladas con ejercicios.

**Antes de empezar:** haber hecho el [capítulo 1](01_SQL_basico.md), sobre todo NULL, filtros y ORDER BY.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 2.1 | [Funciones de agregación](02_SQL_agregados/01_funciones_agregadas.md) | COUNT, SUM, AVG, MIN, MAX; cómo tratan los NULL | NÚCLEO · D04 | 50 min |
| 2.2 | [GROUP BY y HAVING](02_SQL_agregados/02_group_by_having.md) | una cifra por grupo, WHERE frente a HAVING, el grupo NULL | NÚCLEO · D05 | 55 min |
| 2.3 | [Granularidad y denominadores](02_SQL_agregados/03_granularidad_denominadores.md) | numerador/denominador, división entera, promedio de promedios, NULLIF, controles | NÚCLEO · D05 | 55 min |
| 2.4 | [Redondeo, texto y fechas](02_SQL_agregados/04_redondeo_texto_fechas.md) | ROUND, TRIM, `\|\|`, SUBSTR, strftime, julianday | NÚCLEO · D04–D11 | 50 min |
| 2.5 | [CASE y COALESCE](02_SQL_agregados/05_case_coalesce.md) | clasificar, conteo condicional, etiquetar faltantes | NÚCLEO · D17 | 50 min |

## Idea central del capítulo

Una consulta puede ser válida y responder la pregunta incorrecta. Antes de entregar, haz tres controles: **cantidad de grupos** esperada, **suma de las partes = total** y **unidad de medida**. Si algo no cuadra, revisa primero los filtros (estado, NULL) y la granularidad; solo después la sintaxis.

Un ejemplo típico: si sumas todo el detalle de ventas, estás sumando también lo que pertenece a ventas anuladas. Para quedarte solo con las entregadas necesitas unir el detalle con la cabecera de la venta, lo que se aprende en el [capítulo 3](03_SQL_joins.md).

## Ejercicios autónomos de este capítulo

Serie G (G1–G8) y N2 en [`03_EJERCICIOS/SQL/`](../03_EJERCICIOS/SQL/INDICE.md). Cuando un ejercicio use un porcentaje, vuelve a la lección 2.3. Guarda para cada uno una tabla y dos frases: **qué mide** y **qué no puedes concluir**.

Las microprácticas de las lecciones no son ejercicios evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 3 — JOIN](03_SQL_joins.md).
