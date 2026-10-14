# 6.3 Ticket medio, drop size, frecuencia y clientes activos

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [6.1](01_que_es_un_kpi.md), [4.4 SQL para indicadores](../04_SQL_CTE_ventanas/04_sql_kpis_fechas_rendimiento.md) y [2.3 Denominadores](../02_SQL_agregados/03_granularidad_denominadores.md).

## Para qué sirve

Estos cuatro indicadores describen **cómo compran los clientes**: cuánto compran cada vez (ticket y tamaño de entrega), cada cuánto compran (frecuencia y recencia) y si siguen comprando (activos e inactivos). Un gerente los usa para decidir a quién visitar, qué clientes reactivar y si una promoción cambió el comportamiento. Todos dependen de una definición escrita y de una fecha de corte fija.

## Términos nuevos

- **Ticket medio**: importe total / número de documentos de venta. Responde «¿cuánto gasta una venta típica?».
- **Drop size** (tamaño de la entrega): lo que se entrega en cada parada del reparto. Puede medirse en Bs o en unidades por entrega; en esta mini-base, una venta entregada equivale a una entrega.
- **Frecuencia de compra**: cuántas veces compra un cliente en un período; como indicador agregado, ventas entregadas / clientes compradores únicos.
- **Recencia**: días transcurridos desde la última compra hasta la fecha de corte (ya vista).
- **Cliente activo**: aquel que cumple la regla de actividad escrita en la ficha (por ejemplo, «compró en los últimos 30 días hasta el corte»).
- **Cliente inactivo**: tuvo compras pero ya no cumple la regla de actividad.
- **Cliente sin compras**: nunca compró en los datos; no es lo mismo que inactivo.
- **Ventana de actividad**: el número de días de la regla (30, 60...). Cambiarla cambia el número de activos.

## Ejemplo paso a paso

Usamos solo ventas **entregadas** (la ficha de 6.1) y la fecha de corte `2026-09-30`.

**1. Ticket medio y drop size.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1")
base = base[base["estado"] == "entregado"]

por_venta = base.groupby("venta_id").agg(importe=("importe", "sum"), unidades=("cantidad", "sum"))
print(len(por_venta))
print(round(por_venta["importe"].sum() / len(por_venta), 2))
print(round(por_venta["unidades"].mean(), 2))
print(round(por_venta["importe"].median(), 2))
```

```salida
14
166.61
23.07
156.5
```

- 14 entregas.
- **Ticket medio** = 2 332,5 / 14 = **166,61 Bs** por entrega.
- **Drop size en unidades** = unidades promedio por entrega: **23,07**.
- La **mediana** del importe por entrega es 156,5: menor que la media porque hay entregas grandes (lección 11.3).

Primero se agrega al nivel de la venta (una fila por entrega) y **recién entonces** se promedia; promediar las líneas daría el importe medio por línea (lección 2.3), un número distinto.

**2. Frecuencia de compra.**

```sql
SELECT COUNT(*) AS entregas,
       COUNT(DISTINCT tienda_id) AS clientes_compradores,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT tienda_id), 2) AS frecuencia
FROM ventas
WHERE estado = 'entregado';
```

```resultado
entregas | clientes_compradores | frecuencia
14 | 9 | 1.56
```

14 entregas a 9 clientes distintos: **1,56 compras por cliente** en el período. Un indicador agregado así oculta la dispersión: veamos cuántas compras tiene cada cliente.

```sql
SELECT tienda_id, COUNT(*) AS compras
FROM ventas
WHERE estado = 'entregado'
GROUP BY tienda_id
ORDER BY compras DESC, tienda_id;
```

```resultado
tienda_id | compras
1 | 3
3 | 3
2 | 2
4 | 1
5 | 1
6 | 1
7 | 1
9 | 1
10 | 1
```

Dos clientes (las tiendas 1 y 3) compraron 3 veces; las demás, 1 o 2. La frecuencia promedio de 1,56 describe mal a un cliente concreto. (Medir el **intervalo entre compras** de cada cliente es otro indicador distinto: no lo mezcles con este.)

**3. Recencia y clasificación de clientes.** Regla de la ficha: *activo = última compra entregada hasta 30 días antes del corte (inclusive); inactivo = última compra más antigua; sin compras = nunca compró.*

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")

corte = pd.Timestamp("2026-09-30")
entregadas = ventas[ventas["estado"] == "entregado"].copy()
entregadas["fecha"] = pd.to_datetime(entregadas["fecha"])

ultima = entregadas.groupby("tienda_id", as_index=False)["fecha"].max().rename(columns={"fecha": "ultima_compra"})
clientes = tiendas[["tienda_id", "nombre"]].merge(ultima, on="tienda_id", how="left", validate="1:1")
clientes["recencia_dias"] = (corte - clientes["ultima_compra"]).dt.days


def clasificar(dias, ventana):
    if pd.isna(dias):
        return "sin compras"
    return "activo" if dias <= ventana else "inactivo"


clientes["estado_30"] = clientes["recencia_dias"].apply(clasificar, ventana=30)
clientes["estado_45"] = clientes["recencia_dias"].apply(clasificar, ventana=45)
print(clientes["estado_30"].value_counts().to_dict())
print(clientes["estado_45"].value_counts().to_dict())
print(len(clientes))
```

```salida
{'activo': 7, 'sin compras': 3, 'inactivo': 2}
{'activo': 9, 'sin compras': 3}
12
```

El resultado cambia con la regla: con **30 días** hay 7 activos, 2 inactivos y 3 sin compras; con **45 días** hay 9 activos, 0 inactivos y 3 sin compras (las tiendas 5 y 6 compraron hace 40 y 33 días). Los totales siempre suman 12 clientes. Por eso la ventana va **escrita en la ficha**, y cada reporte dice cuál usó.

**4. Los pasos que no se pueden saltar.**

1. Fecha de corte **fija** (no `hoy`).
2. Considerar solo las compras que la ficha define (aquí, entregadas).
3. `how="left"` desde la lista completa de clientes, para no perder a los que nunca compraron.
4. Tratar el «sin compras» como categoría propia: su recencia es `NaN`, no 0.
5. Comprobar que las categorías suman el total de clientes.

**5. Actividad por mes (clientes activos mensuales).**

```sql
SELECT strftime('%Y-%m', fecha) AS mes,
       COUNT(DISTINCT tienda_id) AS clientes_con_compra,
       COUNT(*) AS entregas
FROM ventas
WHERE estado = 'entregado'
GROUP BY mes
ORDER BY mes;
```

```resultado
mes | clientes_con_compra | entregas
2026-08 | 5 | 6
2026-09 | 7 | 8
```

«Activo mensual» = tuvo al menos una compra en el mes. En agosto compraron 5 clientes y en septiembre 7. Un cliente puede ser activo en septiembre y haber estado inactivo en agosto (reactivación). Esta definición es diferente de la ventana de 30 días: son dos indicadores y cada uno necesita su ficha.

Ejemplo comercial: la lista de «clientes inactivos» (hasta 60 días sin compra) se entrega a los vendedores para visitas de reactivación. Si en la ficha dice 60 y el reporte del mes pasado usaba 30, los números no son comparables.

## Errores comunes

- **Calcular el ticket promediando líneas** en lugar de ventas.
- **Usar el promedio de la frecuencia** como si describiera a cada cliente.
- **Usar la fecha de hoy** como corte.
- **Convertir «sin compras» en 0 días** (parecería el cliente más activo).
- **Cambiar la ventana de actividad** entre reportes sin avisar.
- **Perder clientes sin compras** por usar INNER JOIN.
- **Confundir cliente inactivo con cliente que nunca compró.**

## Para comprobar que entendiste

1. ¿Cuál es el denominador del ticket medio?
2. ¿Por qué la frecuencia promedio puede engañar?
3. ¿Qué pasa con la clasificación si la ventana pasa de 30 a 45 días?
4. ¿Cómo se trata a un cliente que nunca compró?

<details><summary>Respuestas</summary>

1. El número de ventas (documentos) distintas, no de líneas.
2. Porque oculta la dispersión: pocos clientes compran mucho y otros una sola vez.
3. Algunos inactivos pasan a activos (aquí, las tiendas 5 y 6).
4. Como «sin compras», categoría aparte; su recencia está vacía.

</details>

## Micropráctica

1. Calcula el ticket medio y el drop size en unidades de **septiembre** solamente.
2. Cuenta cuántos clientes están activos con una ventana de 15 días y cuántos son inactivos.
3. Escribe la ficha del KPI «Clientes activos (ventana 15 días)».

Cómo saber que está bien: en septiembre hay 8 entregas.

<details><summary>Comprobación de la parte 1</summary>

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1")
base = base[(base["estado"] == "entregado") & (base["fecha"].str.startswith("2026-09"))]
por_venta = base.groupby("venta_id").agg(importe=("importe", "sum"), unidades=("cantidad", "sum"))
print(len(por_venta), round(por_venta["importe"].mean(), 2), round(por_venta["unidades"].mean(), 2))
```

```salida
8 167.38 23.25
```

</details>

## Después, en los ejercicios

Estos indicadores se practican en K1, N7, N9, N12, V1 y V2 de [SQL](../../03_EJERCICIOS/SQL/INDICE.md). En cada uno escribe primero la regla de actividad y la fecha de corte. Siguiente: [6.4 Productividad, crecimiento y variaciones](04_productividad_variaciones.md).
