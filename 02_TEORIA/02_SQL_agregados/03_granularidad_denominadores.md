# 2.3 Granularidad y denominadores: el número correcto para la pregunta correcta

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisito: [2.2 GROUP BY y HAVING](02_group_by_having.md).

## Para qué sirve

La mayoría de los indicadores son un cociente: ventas por pedido, visitas realizadas sobre visitas planificadas, pedidos sobre visitas. Si divides entre el número equivocado, el resultado parece razonable y es incorrecto. Esta lección te da el hábito de preguntar, antes de escribir el cociente: **¿qué cuento arriba y qué cuento abajo, y qué representa cada fila que estoy contando?**

## Términos nuevos

- **Numerador**: el número de arriba de una fracción (lo que quieres medir: visitas realizadas).
- **Denominador**: el número de abajo (el universo contra el que lo comparas: visitas planificadas).
- **Granularidad** (ya la conoces): qué representa una fila. Cambiar de tabla o de `GROUP BY` cambia la granularidad.
- **División entera**: cuando ambos números son enteros, SQLite descarta los decimales: `7 / 2` da 3 y `11 / 14` da 0. Para evitarlo, multiplica por `1.0` o por `100.0` antes de dividir.
- **NULLIF(a, b)**: devuelve NULL si `a` es igual a `b`, y `a` en caso contrario. Se usa como `NULLIF(denominador, 0)` para evitar divisiones entre cero.
- **Promedio de promedios**: calcular el promedio de varios porcentajes o promedios de grupos de distinto tamaño. Casi nunca es correcto.

## Ejemplo paso a paso

**1. Dos promedios que parecen el mismo.** En `venta_lineas` una fila es una *línea*, no una venta. Comparemos:

```sql
SELECT SUM(cantidad * precio_unitario) / COUNT(DISTINCT venta_id) AS importe_por_venta,
       AVG(cantidad * precio_unitario) AS importe_por_linea
FROM venta_lineas;
```

```resultado
importe_por_venta | importe_por_linea
170.09375 | 69.78205128205128
```

- **Importe por venta** (llamado a veces *ticket promedio*): total vendido dividido entre el número de ventas distintas. Responde "¿cuánto gasta una venta típica?".
- **Importe por línea**: promedio de cada renglón de venta. Responde "¿cuánto vale un renglón típico?". Es mucho menor, porque cada venta tiene varias líneas.

Los dos son correctos; responden preguntas distintas. Si el gerente pide el "ticket promedio" y entregas el segundo número, te equivocaste sin ningún error de sintaxis. (Aquí aún entran las ventas anuladas, porque `venta_lineas` no tiene el estado; para excluirlas necesitarás un JOIN con `ventas`, que verás en el capítulo 3.)

**2. Un porcentaje bien construido.** Cumplimiento de visitas = visitas realizadas / visitas planificadas:

```sql
SELECT SUM(realizada) AS realizadas,
       SUM(planificada) AS planificadas,
       100.0 * SUM(realizada) / SUM(planificada) AS cumplimiento_pct
FROM visitas_ej;
```

```resultado
realizadas | planificadas | cumplimiento_pct
11 | 14 | 78.57142857142857
```

A mano: 11 realizadas de 14 planificadas → 11 / 14 = 0,7857 → 78,57 %. Fíjate en que conservamos el numerador y el denominador **por separado** en el resultado: así quien lea el reporte puede verificar el porcentaje.

**3. La trampa de la división entera.**

```sql
SELECT SUM(realizada) / SUM(planificada) AS sin_decimales,
       1.0 * SUM(realizada) / SUM(planificada) AS con_decimales
FROM visitas_ej;
```

```resultado
sin_decimales | con_decimales
0 | 0.7857142857142857
```

La primera da 0 porque 11 / 14 entre enteros se trunca. La segunda da 0,7857. Regla: **multiplica por `1.0` (o `100.0`) antes de dividir**, no después.

**4. Efectividad: otro denominador.** De las visitas realizadas, ¿en cuántas se tomó pedido?

```sql
SELECT SUM(pedido_tomado) AS pedidos,
       SUM(realizada) AS realizadas,
       100.0 * SUM(pedido_tomado) / SUM(realizada) AS efectividad_pct
FROM visitas_ej;
```

```resultado
pedidos | realizadas | efectividad_pct
7 | 11 | 63.63636363636363
```

El denominador cambió: ya no son las *planificadas*, sino las *realizadas*, porque no puedes tomar pedido si no hiciste la visita. Elegir el denominador es decidir **qué pregunta responde el indicador**: cumplimiento y efectividad usan los mismos datos y dicen cosas distintas.

**5. El promedio de promedios.** Mira el cumplimiento por día:

```sql
SELECT fecha, SUM(planificada) AS planificadas,
       100.0 * SUM(realizada) / SUM(planificada) AS cumplimiento_pct
FROM visitas_ej
GROUP BY fecha
ORDER BY fecha;
```

```resultado
fecha | planificadas | cumplimiento_pct
2026-09-01 | 4 | 75.0
2026-09-02 | 3 | 66.66666666666667
2026-09-03 | 3 | 100.0
2026-09-04 | 3 | 66.66666666666667
2026-09-05 | 1 | 100.0
```

Los cinco porcentajes diarios son 75, 66,67, 100, 66,67 y 100. Su promedio simple es (75 + 66,67 + 100 + 66,67 + 100) / 5 ≈ 81,67 %, **pero el cumplimiento real del período es 78,57 %**. La diferencia aparece porque los días tienen distinta cantidad de visitas (el 1 de septiembre tuvo 4 y el 5 solo 1) y el promedio simple da el mismo peso al día de 1 visita que al de 4. Para combinar grupos, **suma numeradores y denominadores y divide al final**.

**6. Evitar la división entre cero.**

```sql
SELECT 100.0 * SUM(realizada) / NULLIF(SUM(planificada), 0) AS cumplimiento_pct
FROM visitas_ej
WHERE fecha = '2030-01-01';
```

```resultado
cumplimiento_pct
NULL
```

No hay visitas en esa fecha: el denominador sería 0. `NULLIF(…, 0)` lo convierte en NULL y el resultado es NULL, que significa «no se puede calcular». Es distinto de «0 %», que diría que había visitas planificadas y no se hizo ninguna. Presenta ese vacío como «sin datos», no como cero.

Ejemplo comercial: el jefe pregunta el «ticket promedio de la ruta R02». Respuesta correcta: ventas en Bs de la ruta R02 ÷ número de ventas de R02. Respuestas incorrectas típicas: promediar líneas (paso 1) o promediar los tickets de cada vendedor (paso 5).

## Un control que siempre debes hacer

Después de calcular un indicador por grupos, comprueba tres cosas:

1. **Cantidad de grupos**: ¿salió el número que esperabas (3 rutas, 5 días)?
2. **Suma de numeradores y denominadores**: ¿dan los totales de la tabla completa?
3. **Unidad**: ¿es Bs, unidades, porcentaje, días?

Si alguno no cuadra, revisa primero los filtros y la granularidad; luego la sintaxis.

## Errores comunes

- **Dividir entre enteros** y obtener 0 o redondeos extraños.
- **Promediar porcentajes** de grupos de distinto tamaño.
- **Usar el denominador equivocado** (planificadas en lugar de realizadas).
- **Promediar sobre el detalle** (`AVG` sobre líneas) cuando la pregunta es por venta, por cliente o por visita.
- **Mostrar el porcentaje sin su numerador y denominador**: nadie puede verificarlo.
- **Convertir un NULL en 0 %** cuando en realidad «no hay datos».
- **Redondear antes de dividir o de sumar**: redondea solo al presentar.

## Para comprobar que entendiste

1. ¿Por qué el importe por línea es menor que el importe por venta?
2. ¿Cuánto da `7 / 2` en SQLite? ¿Y `7 / 2.0`?
3. ¿Por qué es incorrecto promediar los cinco porcentajes diarios?
4. ¿Qué hace `NULLIF(x, 0)`?

<details><summary>Respuestas</summary>

1. Porque una venta tiene varias líneas; el total se reparte entre más renglones.
2. `3` y `3.5`.
3. Porque los días tienen distinta cantidad de visitas; hay que sumar numeradores y denominadores y dividir al final.
4. Devuelve NULL cuando `x` es 0; así evita dividir entre cero.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Calcula en una sola consulta el cumplimiento de visitas (`realizada` sobre `planificada`) **por fecha** y comprueba a mano el de la fecha `2026-09-02`.
2. Calcula la efectividad (`pedido_tomado` sobre `realizada`) del total de `visitas_ej` y explica en una frase por qué el denominador es diferente al del cumplimiento.
3. Calcula el importe total por unidad vendida (importe total ÷ unidades) de `venta_lineas` y escribe qué significa ese número.

Cómo saber que está bien: la 1 devuelve 5 filas; el 2 de septiembre hay 3 visitas planificadas y 2 realizadas (66,67 %); en la 2 el resultado es aproximadamente 63,64 %.

<details><summary>Comprobación de las consultas 2 y 3</summary>

```sql
SELECT 100.0 * SUM(pedido_tomado) / SUM(realizada) AS efectividad_pct FROM visitas_ej;
```

```resultado
efectividad_pct
63.63636363636363
```

```sql
SELECT SUM(cantidad * precio_unitario) / SUM(cantidad) AS precio_medio_por_unidad FROM venta_lineas;
```

```resultado
precio_medio_por_unidad
7.476648351648351
```

Es el precio promedio ponderado: cada precio pesa según las unidades que se vendieron a ese precio.

</details>

## Después, en los ejercicios

Los indicadores de N1 a N4 y las series G de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) piden porcentajes y promedios. Antes de cada uno escribe «numerador = ___, denominador = ___, unidad = ___» y al terminar haz los tres controles de esta lección. Para el contexto de negocio de cada indicador, mira el [capítulo 6 (KPIs)](../06_KPIs.md).

Siguiente: [2.4 Redondeo, texto y fechas](04_redondeo_texto_fechas.md).
