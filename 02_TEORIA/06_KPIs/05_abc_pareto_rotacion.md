# 6.5 ABC, Pareto y rotación de inventario

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [6.1](01_que_es_un_kpi.md), [4.3 Funciones de ventana](../04_SQL_CTE_ventanas/03_ventanas.md) y [10.2 groupby](../10_Pandas_transformaciones/02_groupby_agg.md).

## Para qué sirve

Dos preguntas de administración de catálogo y de stock: *¿qué pocos productos (o clientes) concentran la mayor parte de la venta?* y *¿qué tan rápido se mueve el inventario?* La primera se responde con una clasificación **ABC** y el análisis de **Pareto**; la segunda, con la **rotación**. Sirven para decidir en qué poner atención, dónde reponer más seguido y qué productos revisar.

## Términos nuevos

- **Análisis de Pareto**: la observación de que una minoría de elementos suele explicar la mayoría del resultado (la «regla 80/20» es una aproximación, **no una ley**). Describe concentración; no obliga a que sea exactamente 80/20.
- **Clasificación ABC**: separar los elementos en clases según su aporte acumulado: **A** (los que más aportan), **B** (intermedios) y **C** (los que menos aportan).
- **Participación**: el porcentaje que aporta cada elemento del total.
- **Participación acumulada**: la suma de las participaciones, de mayor a menor aporte.
- **Convención de borde**: la regla escrita que decide en qué clase cae el elemento que **cruza** un umbral. Aquí: se mira la participación acumulada **antes** de sumar al elemento; si esa acumulada anterior es menor que 80 %, el elemento es A.
- **Rotación de inventario**: salidas del período (unidades) / stock promedio del período (unidades).
- **Stock promedio**: aproximación `(stock inicial + stock final) / 2`.
- **Días de inventario**: `días del período / rotación`; cuántos días alcanza el stock al ritmo de salida actual.

## Ejemplo paso a paso

**1. Aporte de cada artículo.** Importe entregado por artículo, con su participación y la acumulada (de mayor a menor):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")

lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "estado"]], on="venta_id", validate="m:1")
base = base[base["estado"] == "entregado"]

por_articulo = (
    base.groupby("articulo_id", as_index=False)["importe"].sum()
    .merge(articulos[["articulo_id", "nombre"]], on="articulo_id", validate="1:1")
    .sort_values(["importe", "articulo_id"], ascending=[False, True])
    .reset_index(drop=True)
)
total = por_articulo["importe"].sum()
por_articulo["pct"] = por_articulo["importe"] / total * 100
por_articulo["acumulado_pct"] = por_articulo["pct"].cumsum()
print(por_articulo[["nombre", "importe", "pct", "acumulado_pct"]].round(1))
print(total)
```

```salida
           nombre  importe   pct  acumulado_pct
0         Agua 2L    450.0  19.3           19.3
1         Jugo 1L    324.0  13.9           33.2
2       Yogurt 1L    288.0  12.3           45.5
3      Gaseosa 2L    276.0  11.8           57.4
4        Leche 1L    240.0  10.3           67.7
5      Papas 100g    217.5   9.3           77.0
6        Galletas    216.0   9.3           86.2
7  Detergente 1kg    126.0   5.4           91.6
8           Jabón    105.0   4.5           96.1
9        Maní 80g     90.0   3.9          100.0
2332.5
```

Pasos: agregar por artículo → ordenar de mayor a menor (con desempate por id) → participación = importe / total → acumulado con `cumsum()`. Control: el total es 2 332,5 (el de la ficha de 6.1) y el acumulado termina en 100 %.

**2. Clasificar con la convención explícita.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "estado"]], on="venta_id", validate="m:1")
base = base[base["estado"] == "entregado"]
t = (
    base.groupby("articulo_id", as_index=False)["importe"].sum()
    .merge(articulos[["articulo_id", "nombre"]], on="articulo_id", validate="1:1")
    .sort_values(["importe", "articulo_id"], ascending=[False, True])
    .reset_index(drop=True)
)
t["pct"] = t["importe"] / t["importe"].sum() * 100
t["acumulado_antes"] = t["pct"].cumsum() - t["pct"]


def clase(acumulado_antes):
    if acumulado_antes < 80:
        return "A"
    if acumulado_antes < 95:
        return "B"
    return "C"


t["clase"] = t["acumulado_antes"].apply(clase)
print(t[["nombre", "pct", "acumulado_antes", "clase"]].round(1))
print(t.groupby("clase")["pct"].agg(["count", "sum"]).round(1))
```

```salida
           nombre   pct  acumulado_antes clase
0         Agua 2L  19.3              0.0     A
1         Jugo 1L  13.9             19.3     A
2       Yogurt 1L  12.3             33.2     A
3      Gaseosa 2L  11.8             45.5     A
4        Leche 1L  10.3             57.4     A
5      Papas 100g   9.3             67.7     A
6        Galletas   9.3             77.0     A
7  Detergente 1kg   5.4             86.2     B
8           Jabón   4.5             91.6     B
9        Maní 80g   3.9             96.1     C
       count   sum
clase             
A          7  86.2
B          2   9.9
C          1   3.9
```

Con la convención «acumulado **antes** < 80 % es A», el artículo que **cruza** el 80 % queda en A (porque antes de sumarlo aún no se había llegado). La tabla final muestra cuántos artículos hay en cada clase y qué porcentaje de la venta aportan. **Otra convención** (por ejemplo, «acumulado incluyendo al elemento ≤ 80 %») daría clases distintas para los elementos del borde: no es mejor ni peor, pero **debe escribirse y usarse siempre igual**.

**3. Leer la concentración (Pareto).** En la tabla de grupos se ve, por ejemplo, cuántos artículos (de 10) explican cerca del 80 % de la venta. Eso es lo que describe Pareto: **concentración**. Si fueran 3 de 10, la concentración es alta; si fueran 8 de 10, es baja. Aquí, 7 de los 10 artículos aportan el 86,2 % de la venta: una concentración moderada, lejos del «20/80». No hace falta que salga «20 % de los productos → 80 % de la venta»; esa frase es una aproximación histórica.

**4. ABC en SQL con ventanas.**

```sql
WITH por_articulo AS (
    SELECT a.nombre, SUM(l.cantidad * l.precio_unitario) AS importe
    FROM venta_lineas AS l
    INNER JOIN ventas AS v ON v.venta_id = l.venta_id
    INNER JOIN articulos AS a ON a.articulo_id = l.articulo_id
    WHERE v.estado = 'entregado'
    GROUP BY a.articulo_id, a.nombre
),
acumulado AS (
    SELECT nombre,
           importe,
           100.0 * SUM(importe) OVER (ORDER BY importe DESC, nombre ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)
               / SUM(importe) OVER () AS acumulado_antes
    FROM por_articulo
)
SELECT nombre,
       importe,
       ROUND(COALESCE(acumulado_antes, 0), 1) AS acumulado_antes_pct,
       CASE WHEN COALESCE(acumulado_antes, 0) < 80 THEN 'A'
            WHEN COALESCE(acumulado_antes, 0) < 95 THEN 'B'
            ELSE 'C' END AS clase
FROM acumulado
ORDER BY importe DESC, nombre;
```

```resultado
nombre | importe | acumulado_antes_pct | clase
Agua 2L | 450.0 | 0.0 | A
Jugo 1L | 324.0 | 19.3 | A
Yogurt 1L | 288.0 | 33.2 | A
Gaseosa 2L | 276.0 | 45.5 | A
Leche 1L | 240.0 | 57.4 | A
Papas 100g | 217.5 | 67.7 | A
Galletas | 216.0 | 77.0 | A
Detergente 1kg | 126.0 | 86.2 | B
Jabón | 105.0 | 91.6 | B
Maní 80g | 90.0 | 96.1 | C
```

El marco `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` suma todas las filas **anteriores** sin incluir la actual: es el «acumulado antes». Para el primer artículo no hay anteriores (NULL), por eso `COALESCE(..., 0)`. El resultado coincide con la clasificación en Python.

**5. Rotación de inventario.** La mini-base no tiene inventario; construimos un ejemplo pequeño e inventado del mes de septiembre (30 días):

```python
import pandas as pd

inventario = pd.DataFrame({
    "articulo": ["Agua 2L", "Jugo 1L", "Detergente 1kg"],
    "stock_inicial": [120, 60, 40],
    "stock_final": [60, 50, 38],
    "salidas": [180, 40, 6],
})
inventario["stock_promedio"] = (inventario["stock_inicial"] + inventario["stock_final"]) / 2
inventario["rotacion"] = (inventario["salidas"] / inventario["stock_promedio"]).round(2)
inventario["dias_inventario"] = (30 / inventario["rotacion"]).round(1)
print(inventario)
```

```salida
         articulo  stock_inicial  ...  rotacion  dias_inventario
0         Agua 2L            120  ...      2.00             15.0
1         Jugo 1L             60  ...      0.73             41.1
2  Detergente 1kg             40  ...      0.15            200.0

[3 rows x 7 columns]
```

- **Agua 2L**: stock promedio 90; salidas 180 → rotación 2,0 (el stock se renovó 2 veces en el mes) → alcanza para 15 días.
- **Jugo 1L**: promedio 55; salidas 40 → 0,73 → 41,1 días.
- **Detergente 1kg**: promedio 39; salidas 6 → 0,15 → 200 días: **producto de movimiento muy lento**.

**Cuidados:** el stock promedio `(inicial + final) / 2` es una aproximación (ignora lo que pasó dentro del mes); se mide en **unidades**, no en Bs, y las salidas y el stock deben ser del mismo período y de los mismos artículos. Una rotación alta no es siempre buena: puede indicar quiebres de stock (no hay para vender). Y una rotación baja puede ser un producto de nicho que debe estar disponible.

**6. Casos límite de la rotación.**

```python
def rotacion(salidas, stock_inicial, stock_final):
    promedio = (stock_inicial + stock_final) / 2
    if promedio == 0:
        return None
    return salidas / promedio


print(rotacion(180, 120, 60))
print(rotacion(0, 10, 10))
print(rotacion(5, 0, 0))
```

```salida
2.0
0.0
None
```

Con stock promedio 0 la rotación no está definida (`None`): puede ser un producto sin stock que igual tuvo salidas (error de registro) o un producto dado de baja. Con salidas 0 la rotación es 0: sin movimiento.

Ejemplo comercial: la clasificación ABC de artículos define la frecuencia de conteo físico (los A se cuentan cada semana, los C cada trimestre), y la rotación decide qué productos reponer más seguido o promocionar para liquidar.

## Errores comunes

- **Clasificar sin ordenar de mayor a menor** o sin desempate.
- **No declarar la convención de borde** del umbral.
- **Creer que debe salir exactamente 80/20.**
- **Mezclar el ABC por ventas con el ABC por variedad de SKU**: son clasificaciones distintas.
- **Calcular la rotación con Bs** en lugar de unidades.
- **Usar un stock promedio de otro período.**
- **Ignorar el stock cero** o el producto sin movimiento.
- **Interpretar una rotación alta como siempre buena.**

## Para comprobar que entendiste

1. ¿Qué mide la participación acumulada y por qué se ordena de mayor a menor?
2. ¿Qué diferencia hay entre «acumulado antes» y «acumulado incluyendo al elemento»?
3. Si salidas = 60 y stock promedio = 30, ¿cuál es la rotación y los días de inventario en 30 días?
4. ¿Qué indica una rotación muy baja?

<details><summary>Respuestas</summary>

1. La suma de los aportes de los elementos más importantes hasta el actual; se ordena de mayor a menor para ver cuántos explican la mayor parte.
2. «Antes» no suma al elemento actual: el que cruza el umbral queda en la clase superior; «incluyendo» sí lo suma y puede dejarlo en la clase siguiente.
3. 2,0; 15 días.
4. Que el producto se mueve lento y mantiene mucho stock respecto a su salida.

</details>

## Micropráctica

1. Clasifica en ABC las **categorías** (Bebidas, Snacks, Limpieza, Lácteos) de las ventas entregadas, con la convención «acumulado antes < 80 → A; < 95 → B; resto C».
2. Calcula la rotación y los días de inventario de dos artículos inventados con sus datos de stock.
3. Explica en una frase por qué dos analistas pueden obtener clasificaciones ABC distintas con los mismos datos.

Cómo saber que está bien: Bebidas queda en A y representa el 45 % de la venta.

<details><summary>Comprobación de la parte 1</summary>

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas[["venta_id", "estado"]], on="venta_id", validate="m:1").merge(articulos[["articulo_id", "categoria"]], on="articulo_id", validate="m:1")
base = base[base["estado"] == "entregado"]
t = base.groupby("categoria", as_index=False)["importe"].sum().sort_values(["importe", "categoria"], ascending=[False, True]).reset_index(drop=True)
t["pct"] = t["importe"] / t["importe"].sum() * 100
t["acumulado_antes"] = t["pct"].cumsum() - t["pct"]
t["clase"] = ["A" if a < 80 else "B" if a < 95 else "C" for a in t["acumulado_antes"]]
print(t.round(1))
```

```salida
  categoria  importe   pct  acumulado_antes clase
0   Bebidas   1050.0  45.0              0.0     A
1   Lácteos    528.0  22.6             45.0     A
2    Snacks    523.5  22.4             67.7     A
3  Limpieza    231.0   9.9             90.1     B
```

</details>

## Después, en los ejercicios

El ABC se practica en V4 y N10 y la rotación en N11 de [SQL](../../03_EJERCICIOS/SQL/INDICE.md); en cada uno, lee la convención de borde del enunciado y respétala. Siguiente: [6.6 Interpretar, recomendar y qué hacer cuando faltan datos](06_interpretar_y_recomendar.md).
