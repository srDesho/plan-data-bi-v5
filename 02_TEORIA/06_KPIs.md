# Capítulo 6 — KPIs empresariales: definición antes de fórmula

Una **métrica** es una medida; un **KPI** es una medida elegida para seguir un objetivo y orientar una decisión. Este capítulo conserva los 13 indicadores del curso (ventas, crecimiento, cumplimiento, cobertura, efectividad, productividad, ticket y drop size, frecuencia, recencia y activos, ABC/Pareto, rotación, variaciones) pero los explica **de cero**: cada uno con su ficha (población, período, unidad, granularidad, numerador, denominador y criterio de acción), su cálculo en Python y en SQL, su interpretación, sus errores comunes y lo que **no** se puede concluir. Todos los datos son inventados (la mini-base de `04_DATASETS/mini_base/`) y distintos de los de los ejercicios.

**Tiempo total estimado de primera vez:** unas 5 h 46 min (6 lecciones). El capítulo se puede leer después de SQL (capítulos 1–4) y se aplica en SQL, Pandas, Excel y Power BI.

**Antes de empezar:** capítulos 1 a 4 (sobre todo 2.3 y 4.4). Para los ejemplos en Python hacen falta los capítulos 9 y 10; si todavía no los has estudiado, usa los de SQL.

## Lecciones

| # | Lección | KPI que cubre | Tipo | Tiempo |
|---|---|---|---|---|
| 6.1 | [Qué es un KPI y la ficha de definición](06_KPIs/01_que_es_un_kpi.md) | KPI 01 · ventas entregadas frente a netas | núcleo · D12 | 56 min |
| 6.2 | [Cumplimiento, cobertura y efectividad](06_KPIs/02_cumplimiento_cobertura_efectividad.md) | KPI 03–06 | núcleo · D25 | 60 min |
| 6.3 | [Ticket, drop size, frecuencia y activos](06_KPIs/03_ticket_frecuencia_activos.md) | KPI 08–10 | refuerzo | 60 min |
| 6.4 | [Productividad, crecimiento y variaciones](06_KPIs/04_productividad_variaciones.md) | KPI 02, 07 y 13 | núcleo · D31 | 55 min |
| 6.5 | [ABC, Pareto y rotación](06_KPIs/05_abc_pareto_rotacion.md) | KPI 11–12 | núcleo · D19 | 60 min |
| 6.6 | [Interpretar, recomendar y cuando faltan datos](06_KPIs/06_interpretar_y_recomendar.md) | todos | núcleo · D39 | 55 min |

## Ideas centrales

- Un KPI sin ficha es una discusión esperando ocurrir: declara qué entra, qué sale, el período, el numerador y el denominador.
- No uses un nombre más grande que lo que mides (no llames «neta» a una venta sin descuentos).
- Los porcentajes de grupos de distinto tamaño no se promedian: suma numeradores y denominadores.
- Una meta se suma solo a su nivel; una meta ausente es «sin dato», no cero.
- Ningún indicador demuestra por sí mismo una causa.
- Todo informe cierra con interpretación, recomendación y límites.

## Ejercicios autónomos de este capítulo

Los indicadores se practican en los ejercicios J2, J4, K1, N1–N5, N7, N9–N12, V1, V2 y V4 de [`03_EJERCICIOS/SQL/`](../03_EJERCICIOS/SQL/INDICE.md) (con sus propios contratos y datos) y en los casos de [`03_EJERCICIOS/Casos/`](../03_EJERCICIOS/Casos/). Las microprácticas de las lecciones no son evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 7 — Python básico](07_Python_basico.md).
