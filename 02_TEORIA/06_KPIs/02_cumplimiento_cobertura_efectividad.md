# 6.2 Cumplimiento, cobertura y efectividad

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [6.1 Qué es un KPI](01_que_es_un_kpi.md) y [3.4 Cuando el JOIN duplica](../03_SQL_joins/04_duplicacion_por_join.md).

## Para qué sirve

Los cuatro indicadores más repetidos de una distribuidora comparan **lo logrado contra lo esperado**: ¿cumplimos la meta de venta? ¿hicimos las visitas que planificamos? ¿visitamos a los clientes que debíamos? ¿en cuántas visitas conseguimos pedido? Parecen simples porque son cocientes, pero cada uno tiene un numerador y un denominador diferentes, y mezclarlos es un error muy común.

## Términos nuevos

- **Cumplimiento de presupuesto (o de meta)**: ventas reales / meta × 100, en el mismo período y a la misma granularidad que la meta (aquí, ruta y mes).
- **Cobertura de ejecución** (o cumplimiento de visitas): visitas realizadas / visitas planificadas × 100.
- **Cobertura de clientes**: clientes **únicos** visitados / clientes **únicos** planificados × 100. No cuenta visitas, cuenta clientes distintos.
- **Efectividad comercial**: visitas realizadas que lograron pedido / visitas realizadas × 100.
- **Brecha**: lo que falta para llegar a la meta (meta − real), en las mismas unidades.
- **Meta aditiva solo a su nivel**: una meta por ruta y mes se puede sumar entre rutas del mismo mes, pero no se puede repartir ni multiplicar a un nivel más detallado (lección 3.4).

## Ejemplo paso a paso

Datos de la mini-base: ventas entregadas, la tabla `metas` (meta en Bs por ruta y mes) y `visitas` (una fila por visita planificada, con `realizada` y `pedido_tomado` en 0 o 1).

**1. Cumplimiento de la meta por ruta y mes.**

```sql
SELECT m.mes,
       m.ruta,
       m.meta_bs,
       ROUND(COALESCE(v.vendido_bs, 0), 2) AS vendido_bs,
       ROUND(100.0 * COALESCE(v.vendido_bs, 0) / m.meta_bs, 1) AS cumplimiento_pct,
       ROUND(m.meta_bs - COALESCE(v.vendido_bs, 0), 2) AS brecha_bs
FROM metas AS m
LEFT JOIN (
    SELECT strftime('%Y-%m', ve.fecha) AS mes, t.ruta, SUM(l.cantidad * l.precio_unitario) AS vendido_bs
    FROM venta_lineas AS l
    INNER JOIN ventas AS ve ON ve.venta_id = l.venta_id
    INNER JOIN tiendas AS t ON t.tienda_id = ve.tienda_id
    WHERE ve.estado = 'entregado'
    GROUP BY mes, t.ruta
) AS v ON v.mes = m.mes AND v.ruta = m.ruta
ORDER BY m.mes, m.ruta;
```

```resultado
mes | ruta | meta_bs | vendido_bs | cumplimiento_pct | brecha_bs
2026-08 | R01 | 450.0 | 465.0 | 103.3 | -15.0
2026-08 | R02 | 280.0 | 131.0 | 46.8 | 149.0
2026-08 | R03 | 320.0 | 397.5 | 124.2 | -77.5
2026-09 | R01 | 600.0 | 800.0 | 133.3 | -200.0
2026-09 | R02 | 450.0 | 379.0 | 84.2 | 71.0
2026-09 | R03 | 300.0 | 160.0 | 53.3 | 140.0
```

Cómo se arma, paso por paso:

1. La subconsulta lleva las ventas entregadas a **una fila por (mes, ruta)**, la misma granularidad que `metas`.
2. Se une con `LEFT JOIN` desde `metas` para no perder una meta sin ventas (si no vendió nada, `COALESCE(..., 0)` pone cero, que aquí **sí** es correcto: «vendió cero»).
3. El cumplimiento es `vendido / meta × 100` y la brecha, `meta − vendido`.

Lectura: en septiembre la ruta R01 superó su meta (133,3 %), R02 llegó al 84,2 % y R03 al 53,3 %. El 133,3 % no significa «mejor ruta» sin más: la meta de R01 podría ser baja; el cumplimiento mide contra una meta, no el tamaño de la venta.

**2. El total nacional: no promedies porcentajes.**

```python
import pandas as pd

metas = pd.DataFrame({"ruta": ["R01", "R02", "R03"], "meta": [600.0, 450.0, 300.0], "vendido": [800.0, 379.0, 160.0]})
metas["cumplimiento"] = metas["vendido"] / metas["meta"] * 100

promedio_simple = metas["cumplimiento"].mean()
cumplimiento_total = metas["vendido"].sum() / metas["meta"].sum() * 100
print(round(promedio_simple, 1), round(cumplimiento_total, 1))
```

```salida
90.3 99.2
```

El promedio simple de los tres porcentajes da 90,3 %; el cumplimiento correcto del total es **vendido total / meta total = 1 339 / 1 350 = 99,2 %**. Difieren porque las rutas tienen metas de distinto tamaño (lección 2.3). La regla: **para un cumplimiento global, suma numeradores y denominadores y divide al final**.

**3. Cobertura de ejecución (visitas).**

```sql
SELECT COUNT(*) AS planificadas,
       SUM(realizada) AS realizadas,
       ROUND(100.0 * SUM(realizada) / COUNT(*), 1) AS cobertura_ejecucion_pct
FROM visitas_ej;
```

```resultado
planificadas | realizadas | cobertura_ejecucion_pct
14 | 11 | 78.6
```

11 de las 14 visitas planificadas se realizaron: 78,6 %. Es una medida de **cumplimiento del plan de visitas**, no de ventas.

**4. Cobertura de clientes (únicos, no visitas).**

```sql
SELECT COUNT(DISTINCT tienda_id) AS clientes_planificados,
       COUNT(DISTINCT CASE WHEN realizada = 1 THEN tienda_id END) AS clientes_visitados,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN realizada = 1 THEN tienda_id END) / COUNT(DISTINCT tienda_id), 1) AS cobertura_clientes_pct
FROM visitas_ej;
```

```resultado
clientes_planificados | clientes_visitados | cobertura_clientes_pct
10 | 7 | 70.0
```

De 10 tiendas planificadas se visitó al menos una vez a 7: 70 %. Observa el contraste con la cobertura de ejecución (78,6 %): una tienda visitada tres veces cuenta tres veces en las visitas y una vez en los clientes. `COUNT(DISTINCT CASE WHEN ... THEN tienda_id END)` cuenta tiendas distintas solo entre las filas que cumplen la condición (el `CASE` devuelve NULL en las demás y `COUNT` los ignora). Una cobertura de clientes baja con ejecución alta indica que se visita **repetidamente a pocos clientes**.

**5. Efectividad comercial.**

```sql
SELECT SUM(realizada) AS visitas_realizadas,
       SUM(CASE WHEN realizada = 1 AND pedido_tomado = 1 THEN 1 ELSE 0 END) AS con_pedido,
       ROUND(100.0 * SUM(CASE WHEN realizada = 1 AND pedido_tomado = 1 THEN 1 ELSE 0 END) / SUM(realizada), 1) AS efectividad_pct
FROM visitas_ej;
```

```resultado
visitas_realizadas | con_pedido | efectividad_pct
11 | 7 | 63.6
```

7 de 11 visitas realizadas terminaron en pedido: 63,6 %. El denominador son las **visitas realizadas**, no las planificadas: no puedes tomar pedido en una visita que no hiciste. Si usaras las planificadas, mezclarías el cumplimiento del plan con la efectividad del vendedor.

**6. Los cuatro indicadores en una tabla comparativa.**

| Indicador | Numerador | Denominador | Mide |
|---|---|---|---|
| Cumplimiento de meta | ventas reales (Bs) | meta (Bs) | si se alcanzó el objetivo de venta |
| Cobertura de ejecución | visitas realizadas | visitas planificadas | si se cumplió el plan de visitas |
| Cobertura de clientes | clientes únicos visitados | clientes únicos planificados | cuánta de la cartera se tocó |
| Efectividad | visitas con pedido | visitas realizadas | qué tan bien se convierte una visita |

**7. Leerlos juntos.** Un cumplimiento de meta del 53 % (R03) no dice **por qué**. Cruzando los demás: si la cobertura de ejecución fue baja, el problema probablemente es operativo (no se visita); si fue alta con efectividad baja, es de conversión (se visita pero no se vende); si la meta era demasiado alta, es de planificación. **Un indicador señala dónde mirar; no demuestra la causa.**

Ejemplo comercial: la ruta R03 cumplió el 53,3 % de su meta de septiembre. Antes de concluir «el vendedor falló», revisas visitas realizadas, clientes cubiertos, efectividad y si la meta era comparable con la de otras rutas.

## Errores comunes

- **Multiplicar la meta al unirla con un detalle más fino** (lección 3.4).
- **Promediar los porcentajes de las rutas** para dar un total.
- **Tomar una meta ausente como cero** (cumplimiento infinito o 0 %): una meta ausente es «sin dato».
- **Contar visitas en lugar de clientes únicos** para la cobertura de clientes.
- **Usar las visitas planificadas como denominador** de la efectividad.
- **Comparar un mes parcial con una meta de mes completo.**
- **Concluir una causa** a partir de un solo indicador.

## Para comprobar que entendiste

1. ¿Cuál es el denominador de la efectividad y por qué?
2. ¿Por qué el cumplimiento global no es el promedio de los cumplimientos por ruta?
3. ¿Qué diferencia hay entre cobertura de ejecución y cobertura de clientes?
4. ¿Qué haces si la meta de una ruta no existe en `metas`?

<details><summary>Respuestas</summary>

1. Las visitas realizadas, porque solo en una visita hecha se puede tomar pedido.
2. Porque las rutas tienen metas de distinto tamaño; hay que dividir ventas totales entre metas totales.
3. La de ejecución cuenta visitas; la de clientes cuenta clientes distintos visitados.
4. La trato como «sin dato» y no como cero, y lo informo.

</details>

## Micropráctica

1. Calcula el cumplimiento de las metas de **agosto** por ruta con Python o SQL.
2. Calcula el cumplimiento global de agosto (suma de ventas entre suma de metas) y compáralo con el promedio de los tres porcentajes.
3. Calcula la efectividad **por fecha** de las visitas y di en qué fecha fue más alta.

Cómo saber que está bien: en agosto R01 llega a 103,3 %, R02 a 46,8 % y R03 a 124,2 %.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
base = base[(base["estado"] == "entregado") & (base["fecha"].str.startswith("2026-08"))]
vendido = base.groupby("ruta", as_index=False)["importe"].sum()

agosto = metas[metas["mes"] == "2026-08"].merge(vendido, on="ruta", validate="1:1")
agosto["cumplimiento_pct"] = (agosto["importe"] / agosto["meta_bs"] * 100).round(1)
print(agosto[["ruta", "meta_bs", "importe", "cumplimiento_pct"]])
print(round(agosto["importe"].sum() / agosto["meta_bs"].sum() * 100, 1), round(agosto["cumplimiento_pct"].mean(), 1))
```

```salida
  ruta  meta_bs  importe  cumplimiento_pct
0  R01    450.0    465.0             103.3
1  R02    280.0    131.0              46.8
2  R03    320.0    397.5             124.2
94.6 91.4
```

</details>

## Después, en los ejercicios

Estos cuatro indicadores corresponden a los ejercicios N1–N4 de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) (con sus propios datos). Completa la ficha (6.1) y escribe el numerador y el denominador antes de cada consulta. Siguiente: [6.3 Ticket, drop size, frecuencia y clientes activos](03_ticket_frecuencia_activos.md).
