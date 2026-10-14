# 10.2 groupby y agregaciones

> Tiempo estimado: 60 min (lectura 20 + práctica 40). Prerrequisitos: [10.1 Columnas nuevas](01_columnas_nuevas.md) y [2.2 GROUP BY en SQL](../02_SQL_agregados/02_group_by_having.md).

## Para qué sirve

`groupby` es el `GROUP BY` de Pandas: divide la tabla en grupos, calcula algo en cada uno y junta los resultados. Con él construyes casi todas las tablas de resumen de un reporte (ventas por ruta, pedidos por mes, clientes por tipo). Como en SQL, el error clásico es agrupar a la granularidad equivocada o contar sin darte cuenta de qué estás contando.

## Términos nuevos

- **`groupby`**: divide la tabla en grupos según una o más columnas.
- **Agregación** (`agg`): la función que resume cada grupo (suma, promedio, conteo).
- **Agregación con nombre** (*named aggregation*): `agg(nombre=("columna", "función"))`; define el nombre de la columna resultante.
- **`size()`**: cuenta las filas de cada grupo (como `COUNT(*)`).
- **`count()`**: cuenta los valores **no vacíos** de cada columna (como `COUNT(columna)`).
- **`nunique()`**: cuenta los valores distintos (como `COUNT(DISTINCT ...)`).
- **`reset_index()`**: convierte las claves del grupo (que quedan en el índice) en columnas normales.
- **`transform`**: calcula una agregación por grupo pero devuelve un resultado **del tamaño original** (una fila por fila de entrada); sirve para porcentajes del grupo.
- **Tabla dinámica** (`pivot_table`): resumen con una variable en filas y otra en columnas.

## Ejemplo paso a paso

Preparamos el importe por línea y traemos el estado y la fecha de la venta:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "tienda_id", "estado"]], on="venta_id", how="left", validate="m:1")
print(len(lineas), len(base))
print(base[["linea_id", "venta_id", "tienda_id", "estado", "importe"]].head(3))
```

```salida
39 39
   linea_id  venta_id  tienda_id     estado  importe
0         1         1          1  entregado     60.0
1         2         1          1  entregado     45.0
2         3         1          1  entregado     32.0
```

Control: 39 líneas antes y después de unir (la unión es muchos a uno: cada línea tiene una sola venta). Ahora a agrupar.

**1. Un conteo por grupo.**

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
print(ventas.groupby("estado").size())
```

```salida
estado
anulado       2
entregado    14
dtype: int64
```

`groupby("estado").size()` cuenta las filas de cada estado: 14 entregadas y 2 anuladas, lo mismo que el SQL de la lección 2.2.

**2. Sumar por grupo.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "tienda_id", "estado"]], on="venta_id", how="left", validate="m:1")

entregadas = base[base["estado"] == "entregado"]
print(entregadas.groupby("tienda_id")["importe"].sum().head(4))
print(entregadas["importe"].sum())
```

```salida
tienda_id
1    544.0
2    348.0
3    345.0
4    165.0
Name: importe, dtype: float64
2332.5
```

Primero se filtra (`estado == "entregado"`), luego se agrupa y se suma. El segundo número es el total sin agrupar (2 332,5, el mismo del SQL de 3.2). **El control de siempre: los grupos deben sumar el total.**

**3. Varias agregaciones con nombre.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", how="left", validate="m:1")
base = base.merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", how="left", validate="m:1")
base = base[base["estado"] == "entregado"]

por_ruta = (
    base.groupby("ruta")
    .agg(
        importe_bs=("importe", "sum"),
        lineas=("linea_id", "size"),
        ventas=("venta_id", "nunique"),
        unidades=("cantidad", "sum"),
    )
    .reset_index()
)
por_ruta["ticket_bs"] = (por_ruta["importe_bs"] / por_ruta["ventas"]).round(2)
print(por_ruta)
print(por_ruta["importe_bs"].sum(), por_ruta["ventas"].sum())
```

```salida
  ruta  importe_bs  lineas  ventas  unidades  ticket_bs
0  R01      1265.0      19       7       176     180.71
1  R02       510.0      10       4        80     127.50
2  R03       557.5       7       3        67     185.83
2332.5 14
```

Cada argumento de `agg` es `nombre_resultado=("columna", "función")`. Observa tres cosas:

1. `lineas` usa `size` (filas), `ventas` usa `nunique` de `venta_id` (ventas **distintas**). Después de unir con el detalle, contar ventas con `size` contaría líneas (error de la lección 3.4).
2. Se **conservan numerador y denominador** (`importe_bs`, `ventas`) y el ticket se calcula **después** dividiendo, nunca promediando.
3. `reset_index()` convierte la ruta (que estaba en el índice) en una columna. Control: importes suman 2 332,5 y las ventas, 14.

**4. `size` frente a `count` frente a `nunique`.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
r = tiendas.groupby("ruta").agg(
    filas=("tienda_id", "size"),
    con_zona=("zona", "count"),
    zonas_distintas=("zona", "nunique"),
)
print(r)
```

```salida
      filas  con_zona  zonas_distintas
ruta                                  
R01       4         4                3
R02       4         3                2
R03       4         3                3
```

Es la misma diferencia de SQL: `size` cuenta todas las filas del grupo, `count("zona")` solo las que tienen zona (las `NaN` no cuentan), y `nunique` cuenta los valores distintos no vacíos.

**5. Agrupar por dos columnas.**

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
r = ventas.groupby(["vendedor_id", "estado"]).size().reset_index(name="ventas")
print(r)
```

```salida
   vendedor_id     estado  ventas
0            1  entregado       7
1            2    anulado       1
2            2  entregado       4
3            3    anulado       1
4            3  entregado       3
```

El resultado tiene una fila por cada combinación (vendedor, estado) que existe, igual que en SQL.

**6. Los vacíos en las claves de agrupación.** Por defecto `groupby` **descarta** las filas cuya clave es `NaN`. Mira:

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas.groupby("zona").size().sum())
print(tiendas.groupby("zona", dropna=False).size().sum())
```

```salida
10
12
```

Sin `dropna=False` los grupos suman 10 (¡faltan las 2 tiendas sin zona!); con `dropna=False` suman 12. Es un error **silencioso**: tu resumen por zona no incluye dos tiendas y nadie lo nota si no compara con el total. Control: la suma de los grupos debe igualar las filas de la tabla.

**7. Porcentaje del grupo con `transform`.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
lineas["importe_venta"] = lineas.groupby("venta_id")["importe"].transform("sum")
lineas["pct_de_su_venta"] = (lineas["importe"] / lineas["importe_venta"] * 100).round(1)
print(lineas.loc[lineas["venta_id"] == 1, ["linea_id", "importe", "importe_venta", "pct_de_su_venta"]])
```

```salida
   linea_id  importe  importe_venta  pct_de_su_venta
0         1     60.0          137.0             43.8
1         2     45.0          137.0             32.8
2         3     32.0          137.0             23.4
```

`transform("sum")` calcula el total de cada venta pero lo repite en cada una de sus líneas, conservando el tamaño original; así puedes dividir cada línea entre el total de su venta. Es el equivalente de `SUM(...) OVER (PARTITION BY venta_id)` de la lección 4.3. Los porcentajes de la venta 1 suman 100.

**8. Tabla dinámica.**

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tabla = pd.pivot_table(ventas, index="vendedor_id", columns="estado", values="venta_id", aggfunc="count", fill_value=0)
print(tabla)
```

```salida
estado       anulado  entregado
vendedor_id                    
1                  0          7
2                  1          4
3                  1          3
```

`pivot_table` pone una variable en filas (vendedor), otra en columnas (estado) y cuenta en cada celda; `fill_value=0` pone cero donde no hay ventas (aquí es un cero legítimo: «ninguna venta anulada»). Es el equivalente de una tabla dinámica de Excel y de `SUM(CASE WHEN ...)` en SQL.

Ejemplo comercial: «ventas, ventas distintas y ticket por ruta» es el `agg` del punto 3. Con la columna `ventas` conservada, otro analista puede recalcular el ticket nacional como suma de importes entre suma de ventas, no como promedio de tickets.

## Errores comunes

- **`size()` cuando querías contar entidades distintas** después de unir con un detalle.
- **No usar `reset_index()`** y trabajar con claves escondidas en el índice.
- **Promediar promedios** en lugar de sumar numerador y denominador.
- **Perder grupos con clave vacía** por no usar `dropna=False`.
- **No comprobar que los grupos suman el total.**
- **Agrupar antes de filtrar** (o filtrar después) cambiando el significado.
- **Olvidar que `count()` ignora los vacíos.**

## Para comprobar que entendiste

1. ¿En qué se diferencian `size()` y `count()`?
2. ¿Qué hace `reset_index()` después de un `groupby`?
3. ¿Por qué el ticket se calcula después de agregar importe y ventas?
4. ¿Qué pasa por defecto con las filas cuya clave de grupo es `NaN`?

<details><summary>Respuestas</summary>

1. `size` cuenta todas las filas del grupo; `count` solo las no vacías de cada columna.
2. Convierte las claves del grupo (índice) en columnas normales.
3. Porque promediar tickets de grupos de distinto tamaño da un resultado incorrecto; hay que dividir totales.
4. Se descartan del resultado.

</details>

## Micropráctica

Con las líneas entregadas unidas a artículos (necesitas `articulos.csv`):

1. Importe, unidades y ventas distintas por **categoría de artículo**.
2. Verifica que el importe total por categoría suma 2 332,5.
3. Calcula el porcentaje que representa cada categoría del total.
4. Compara tus cifras con el SQL de la lección 3.2 (importe por categoría).

Cómo saber que está bien: Bebidas es la categoría con más importe (1 050).

<details><summary>Comprobación de las partes 1 a 3</summary>

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "estado"]], on="venta_id", validate="m:1")
base = base.merge(articulos[["articulo_id", "categoria"]], on="articulo_id", validate="m:1")
base = base[base["estado"] == "entregado"]

r = base.groupby("categoria").agg(
    importe_bs=("importe", "sum"),
    unidades=("cantidad", "sum"),
    ventas=("venta_id", "nunique"),
).reset_index()
r["pct"] = (r["importe_bs"] / r["importe_bs"].sum() * 100).round(1)
print(r.sort_values("importe_bs", ascending=False))
print(r["importe_bs"].sum())
```

```salida
  categoria  importe_bs  unidades  ventas   pct
0   Bebidas      1050.0       135      10  45.0
2   Lácteos       528.0        54       6  22.6
3    Snacks       523.5        95       8  22.4
1  Limpieza       231.0        39       3   9.9
2332.5
```

</details>

## Después, en los ejercicios

`groupby` es la base de P17–P20 y de las tablas Gold de los ejercicios P21–P28 en [Python](../../03_EJERCICIOS/Python/); en cada una compara con el SQL equivalente (G1 y G5 son buenos puentes). Siguiente: [10.3 merge y cardinalidad](03_merge_cardinalidad.md).
