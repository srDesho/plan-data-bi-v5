# 6.1 Qué es un KPI: la ficha de definición y las ventas entregadas

> Tiempo estimado: 56 min (lectura 31 + práctica 25). Prerrequisitos: [2.3 Granularidad y denominadores](../02_SQL_agregados/03_granularidad_denominadores.md) y [3.2 INNER JOIN](../03_SQL_joins/02_inner_join.md).

<!-- TEORIA:PREPARACION:INICIO -->
<a id="preparacion-an07"></a>

## Base inicial de KPI · 6 min

Antes de AN07, lee estas definiciones y escribe una predicción. Esta base forma parte de la lectura de 6.1; el desarrollo completo de [6.2 Cumplimiento, cobertura y efectividad](02_cumplimiento_cobertura_efectividad.md) sigue en D25.

| KPI | Qué compara | Fracción para el mismo periodo |
|---|---|---|
| Cumplimiento de ventas | lo vendido frente a la meta de ventas | ventas / meta × 100 |
| Cobertura de ejecución | las visitas realizadas dentro de la agenda planificada frente a las que estaban planificadas | visitas planificadas que se realizaron / visitas planificadas × 100 |
| Efectividad | las visitas realizadas que terminaron con pedido frente a todas las realizadas | visitas realizadas con pedido / visitas realizadas × 100 |

Un pedido tomado no demuestra que la venta se haya entregado; declara qué estado cuenta como venta. Si el denominador es cero, el porcentaje no es calculable: no lo conviertas en 0 %.

**Ejemplo guiado independiente.** Una agenda de prueba tiene 6 visitas planificadas; se realizan 3 de ellas y 2 de esas 3 terminan con pedido. Su cobertura es 3/6 = 50 % y su efectividad es 2/3 ≈ 66,7 %. Esas cifras no dicen cuánto dinero se vendió. Para medir cumplimiento se necesitan las ventas y su meta: Bs 90 de ventas frente a una meta de Bs 100 representan 90 %.

**Predice antes de pasar a AN07.** Si esa agenda cambia a 8 visitas planificadas, pero siguen realizándose 3 y tomando pedido en 2, ¿cuál de los dos indicadores de visitas cambia y cuál permanece igual? Escribe qué denominador justifica tu predicción; no necesitas calcular otro porcentaje.

El encabezado de esta lección incluye esta sección de 6 min. Si ya la estudiaste en D12, quedan 25 min de lectura del desarrollo; no vuelvas a sumar esta sección. La práctica de 25 min se contabiliza por separado según la guía.
<!-- TEORIA:PREPARACION:FIN -->

<a id="desarrollo"></a>

## Para qué sirve

«¿Cómo vamos en ventas?» tiene diez respuestas posibles según qué se cuente, en qué período y contra qué. Un indicador clave sin definición es una discusión esperando ocurrir: dos áreas calculan «ventas» distinto y ambas tienen razón. La **ficha de definición** de un KPI es el documento mínimo que evita esa discusión, y es lo primero que haces antes de escribir una consulta de indicadores.

## Términos nuevos

- **Métrica**: una medida numérica de algo (cantidad de pedidos, importe vendido).
- **KPI** (*Key Performance Indicator*, indicador clave de desempeño): una métrica elegida para **seguir un objetivo** y orientar una decisión. Toda métrica puede ser un KPI si está ligada a una meta y a una acción.
- **Ficha del KPI**: la definición escrita con nombre, objetivo de negocio, población, período, unidad, granularidad, numerador, denominador, fuente, regla de exclusiones y criterio de acción.
- **Numerador / denominador** (ya vistos en 2.3): lo que mides y el universo contra el que lo comparas.
- **Población** (de un KPI): el conjunto de unidades sobre el que se mide (todas las ventas, los clientes activos de una ruta). Se estudia a fondo en la lección 11.1.
- **Granularidad** (ya vista): qué representa una fila de los datos y del resultado.
- **Venta bruta / venta neta / venta entregada**: la bruta es el total facturado o pedido; la **neta** descuenta devoluciones y descuentos; la **entregada** solo cuenta lo que efectivamente se entregó.
- **Criterio de acción**: lo que se hará según el valor del KPI (por ejemplo, «si el cumplimiento baja de 80 %, se revisa la ruta»). Sin criterio, un KPI es solo un número.
- **Fecha de corte**: el momento hasta el cual se miden los datos (ya vista en 4.4).

## Ejemplo paso a paso

**1. Un mismo dato, tres «ventas».** Con la mini-base inventada, el importe de todas las líneas, el de las líneas de ventas entregadas y el de las anuladas:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "estado"]], on="venta_id", how="left", validate="m:1")

print("todas las líneas:", base["importe"].sum())
print("entregadas:", base.loc[base["estado"] == "entregado", "importe"].sum())
print("anuladas:", base.loc[base["estado"] == "anulado", "importe"].sum())
```

```salida
todas las líneas: 2721.5
entregadas: 2332.5
anuladas: 389.0
```

Tres cifras para la misma pregunta «¿cuánto vendimos?»: 2 721,5 (todo lo registrado), 2 332,5 (lo entregado) y 389 (lo anulado). Si la ficha dice «**ventas entregadas**», la respuesta es 2 332,5, y las anuladas no cuentan. La diferencia entre las cifras es exactamente lo que genera las discusiones.

**2. La ficha del KPI «Ventas entregadas».**

| Campo | Contenido |
|---|---|
| Nombre | Ventas entregadas |
| Objetivo de negocio | medir lo efectivamente vendido y entregado al cliente |
| Población | todas las ventas de la mini-base |
| Período | agosto y septiembre de 2026 |
| Unidad | bolivianos (Bs) |
| Granularidad de origen | línea de venta |
| Fórmula | suma de `cantidad × precio_unitario` de las líneas cuya venta está en estado `entregado` |
| Exclusiones | ventas anuladas; no hay descuentos ni devoluciones en esta base |
| Fuente | `ventas` + `venta_lineas` |
| Fecha contable | `ventas.fecha` (fecha de la venta) |
| Criterio de acción | comparar contra la meta de cada ruta (lección 6.2) |

Con esta ficha, otra persona calcula el mismo número sin preguntarte nada.

**3. No etiquetes lo que no es.** La mini-base no tiene descuentos ni devoluciones, así que **no puedes llamar «ventas netas» a esa cifra**. Una fórmula completa sería `ventas netas = venta bruta − descuentos − devoluciones`; por ejemplo, `1 000 − 50 − 100 = 850 Bs`:

```python
bruta, descuentos, devoluciones = 1000, 50, 100
neta = bruta - descuentos - devoluciones
print(neta)
```

```salida
850
```

Lo honesto es llamar a la cifra de la mini-base «**ventas entregadas**» y anotar que no se descontaron devoluciones por falta de datos. Un nombre más grande que la definición es una forma de engañar sin querer.

**4. Un KPI en SQL, desde la ficha.** El mismo número en SQL, con el JOIN y el filtro de la ficha:

```sql
SELECT ROUND(SUM(l.cantidad * l.precio_unitario), 2) AS ventas_entregadas_bs
FROM venta_lineas AS l
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
WHERE v.estado = 'entregado';
```

```resultado
ventas_entregadas_bs
2332.5
```

Coincide con el cálculo en Python: 2 332,5. **Dos caminos distintos, el mismo número, es la mejor prueba.**

**5. Por mes, con la fecha contable de la ficha.**

```sql
SELECT strftime('%Y-%m', v.fecha) AS mes,
       COUNT(DISTINCT v.venta_id) AS ventas,
       ROUND(SUM(l.cantidad * l.precio_unitario), 2) AS ventas_entregadas_bs
FROM venta_lineas AS l
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
WHERE v.estado = 'entregado'
GROUP BY mes
ORDER BY mes;
```

```resultado
mes | ventas | ventas_entregadas_bs
2026-08 | 6 | 993.5
2026-09 | 8 | 1339.0
```

Control: 6 + 8 = 14 ventas y 993,5 + 1 339 = 2 332,5. Si un mes se compara con otro, ambos deben estar completos y tener los mismos criterios.

**6. Las seis preguntas antes de calcular cualquier KPI.**

1. ¿Qué decisión o meta sirve este número?
2. ¿Qué entra y qué se excluye? (estados, devoluciones, tipos de cliente)
3. ¿Cuál es la fecha que define el período (venta, entrega, factura)?
4. ¿Cuál es la granularidad de los datos y del resultado?
5. ¿Cuál es el numerador y cuál el denominador (si es un cociente)?
6. ¿Qué haré si el valor sube o baja? (criterio de acción)

Ejemplo comercial: el gerente dice «las ventas de septiembre cayeron». Antes de calcular, preguntas: ¿ventas pedidas, entregadas o facturadas? ¿incluyen anuladas? ¿septiembre completo o hasta el día 20? Esas preguntas, respondidas, son la ficha.

## Errores comunes

- **Calcular antes de definir.**
- **Mezclar pedido tomado, facturación y entrega** sin decirlo.
- **Incluir ventas anuladas** o excluir las devoluciones sin avisar.
- **Dar a una cifra un nombre más ambicioso** que lo que realmente mide («neta» sin descuentos).
- **Cambiar la definición entre reportes** sin comunicarlo.
- **Usar un KPI sin criterio de acción.**
- **Comparar períodos incompletos con períodos completos.**

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre una métrica y un KPI?
2. ¿Qué campos mínimos tiene una ficha de KPI?
3. ¿Por qué en la mini-base no se puede hablar de «ventas netas»?
4. ¿Qué dos caminos usamos para verificar las ventas entregadas?

<details><summary>Respuestas</summary>

1. Un KPI es una métrica elegida para seguir un objetivo y decidir una acción.
2. Nombre, objetivo, población, período, unidad, granularidad, fórmula (numerador/denominador), exclusiones, fuente, fecha contable y criterio de acción.
3. Porque no hay datos de descuentos ni devoluciones.
4. Python (merge + suma) y SQL (JOIN + SUM); ambos dan 2 332,5.

</details>

## Micropráctica

1. Escribe la ficha completa del KPI «Unidades entregadas» para la mini-base.
2. Calcúlalo en Python y en SQL y comprueba que coinciden.
3. Redacta la frase que explicaría al gerente la diferencia entre «unidades pedidas» y «unidades entregadas».

Cómo saber que está bien: tus dos cálculos coinciden y tu ficha tiene criterio de acción.

<details><summary>Comprobación de la parte 2 (SQL)</summary>

```sql
SELECT SUM(l.cantidad) AS unidades_entregadas
FROM venta_lineas AS l
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
WHERE v.estado = 'entregado';
```

```resultado
unidades_entregadas
323
```

</details>

## Después, en los ejercicios

El primer indicador de los ejercicios SQL (ventas entregadas, serie J) y los contratos de [`03_EJERCICIOS/SQL/CONTRATOS.md`](../../03_EJERCICIOS/SQL/CONTRATOS.md) funcionan como fichas. Antes de escribir cada consulta, completa la ficha en tu cuaderno. Siguiente: [6.2 Cumplimiento, cobertura y efectividad](02_cumplimiento_cobertura_efectividad.md).
