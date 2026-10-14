# 10.1 Columnas nuevas y transformaciones

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: capítulo 9 completo (sobre todo 9.4 y 9.6).

## Para qué sirve

Los datos crudos casi nunca traen lo que necesitas: el importe de cada línea, el mes de una venta, una etiqueta «grande/pequeña», el estado normalizado. Crear **columnas calculadas** de forma vectorizada (sin bucles) es el trabajo cotidiano de la transformación en un ETL, y es donde nacen muchos errores silenciosos si no se verifica una fila a mano.

## Términos nuevos

- **Transformación**: cualquier cambio que se aplica a los datos para dejarlos en la forma que necesitas (nueva columna, texto normalizado, tipo convertido).
- **Columna derivada** (o calculada): una columna que se obtiene a partir de otras.
- **Operación vectorizada**: la que se aplica a la columna entera de una vez, sin recorrer fila por fila.
- **`np.where(condición, a, b)`**: devuelve `a` donde la condición es verdadera y `b` donde es falsa; es el `CASE WHEN` más simple.
- **`map`**: reemplaza cada valor de una columna usando un diccionario de equivalencias.
- **`apply`**: ejecuta una función Python sobre cada elemento (o fila). Es flexible pero **lenta**; se usa solo si no hay una operación vectorizada.
- **`assign`**: crea columnas nuevas y devuelve una tabla nueva, sin tocar la original.
- **Alineación por índice**: cuando operas dos Series, Pandas empareja los valores por su **etiqueta de índice**, no por su posición.

## Ejemplo paso a paso

**1. Una columna calculada.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
print(lineas[["linea_id", "cantidad", "precio_unitario", "importe"]].head(3))
print(lineas["importe"].sum())
```

```salida
   linea_id  cantidad  precio_unitario  importe
0         1        10              6.0     60.0
1         2         6              7.5     45.0
2         3         4              8.0     32.0
2721.5
```

`lineas["importe"] = ...` crea una columna nueva calculando la multiplicación fila por fila, de una vez. **Verifica una fila a mano**: línea 1 = 10 × 6,0 = 60 ✓. Y compara el total contra una cifra conocida (el SQL de la lección 2.1 da 2 721,5 para todas las líneas).

**2. Condicional con `np.where`** (el `CASE WHEN` de dos ramas):

```python
import numpy as np
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
articulos["tamano_precio"] = np.where(articulos["precio"] >= 8, "alto", "bajo")
print(articulos[["nombre", "precio", "tamano_precio"]].head(4))
print(articulos["tamano_precio"].value_counts().to_dict())
```

```salida
       nombre  precio tamano_precio
0     Agua 2L     6.0          bajo
1     Jugo 1L     9.0          alto
2  Gaseosa 2L    11.5          alto
3  Papas 100g     7.5          bajo
{'bajo': 5, 'alto': 5}
```

`np.where(precio >= 8, "alto", "bajo")` pone `"alto"` donde se cumple y `"bajo"` donde no. Para más de dos ramas, `pd.cut` (rangos) o `np.select`:

```python
import numpy as np
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
condiciones = [articulos["precio"] < 6, articulos["precio"] <= 10]
etiquetas = ["económico", "medio"]
articulos["segmento"] = np.select(condiciones, etiquetas, default="alto")
print(articulos["segmento"].value_counts().to_dict())
```

```salida
{'medio': 4, 'alto': 3, 'económico': 3}
```

`np.select` evalúa las condiciones **en orden** (la primera verdadera gana, igual que `CASE`). Coincide con la clasificación de la lección 2.5: 3 económicos, 4 medios y 3 altos.

**3. Reemplazar valores con un diccionario (`map`).**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
nombre_ruta = {"R01": "Norte-1", "R02": "Centro-2", "R03": "Sur-3"}
tiendas["nombre_ruta"] = tiendas["ruta"].map(nombre_ruta)
print(tiendas[["tienda_id", "ruta", "nombre_ruta"]].head(3))
print(tiendas["nombre_ruta"].isna().sum())
```

```salida
   tienda_id ruta nombre_ruta
0          1  R01     Norte-1
1          2  R01     Norte-1
2          3  R02    Centro-2
0
```

`map(diccionario)` busca cada valor en el diccionario. Un valor que no esté (por ejemplo, una ruta `R09`) queda **`NaN`**, y eso es una señal de alarma: por eso se cuenta `isna().sum()` después. Un 0 indica que todas las rutas estaban en el diccionario.

**4. Texto: normalizar y extraer.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
tiendas["nombre_limpio"] = tiendas["nombre"].str.strip().str.title()
tiendas["primera_palabra"] = tiendas["nombre_limpio"].str.split().str[0]
print(tiendas.loc[tiendas["tienda_id"].isin([4, 5]), ["nombre_limpio", "primera_palabra"]])
```

```salida
             nombre_limpio primera_palabra
3  Minimarket Sol Naciente      Minimarket
4        Kiosco La Esquina          Kiosco
```

Los métodos `.str` operan sobre cada texto de la columna y se pueden encadenar. `str.split().str[0]` parte cada nombre en palabras y toma la primera. Observa la tienda 5: sin el `strip()` previo, la primera «palabra» habría sido un texto vacío.

**5. Columnas de fecha.**

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas["fecha"] = pd.to_datetime(ventas["fecha"], format="%Y-%m-%d")
ventas["mes"] = ventas["fecha"].dt.to_period("M").astype(str)
ventas["es_fin_de_semana"] = ventas["fecha"].dt.dayofweek >= 5
print(ventas[["fecha", "mes", "es_fin_de_semana"]].head(3))
print(ventas["es_fin_de_semana"].sum())
```

```salida
       fecha      mes  es_fin_de_semana
0 2026-08-03  2026-08             False
1 2026-08-05  2026-08             False
2 2026-08-07  2026-08             False
0
```

`dt.dayofweek` da 0 para lunes hasta 6 para domingo; `>= 5` marca sábado y domingo. Sumar el booleano cuenta cuántas ventas fueron en fin de semana (aquí 0: ninguna venta de la mini-base cayó en sábado o domingo).

**6. `assign`: encadenar transformaciones sin tocar la original.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
resultado = lineas.assign(
    importe=lambda d: d["cantidad"] * d["precio_unitario"],
    es_grande=lambda d: d["cantidad"] * d["precio_unitario"] >= 100,
)
print(list(lineas.columns))
print(list(resultado.columns))
print(resultado["es_grande"].sum())
```

```salida
['linea_id', 'venta_id', 'articulo_id', 'cantidad', 'precio_unitario']
['linea_id', 'venta_id', 'articulo_id', 'cantidad', 'precio_unitario', 'importe', 'es_grande']
5
```

`assign` devuelve una tabla **nueva** con las columnas agregadas; `lineas` queda intacta (importante para conservar el dato crudo, como en la lección 8.2). Cada `lambda d: ...` recibe la tabla y calcula la columna.

**7. `apply`: la herramienta de último recurso.**

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")


def etiqueta(precio):
    if precio >= 12:
        return "premium"
    return "normal"


articulos["clase"] = articulos["precio"].apply(etiqueta)
print(articulos["clase"].value_counts().to_dict())
```

```salida
{'normal': 8, 'premium': 2}
```

`apply(función)` llama a tu función una vez por elemento. Funciona, pero con millones de filas es mucho más lento que `np.where`. Úsalo cuando la lógica es demasiado compleja para expresarla de forma vectorizada.

**8. La trampa de la alineación por índice.** Al operar dos Series, Pandas empareja por **etiqueta**, no por posición:

```python
import pandas as pd

a = pd.Series([10, 20, 30], index=[0, 1, 2])
b = pd.Series([1, 2, 3], index=[1, 2, 3])
print((a + b).tolist())
```

```salida
[nan, 21.0, 32.0, nan]
```

Sumaron etiquetas coincidentes: la etiqueta 1 (20 + 1), la 2 (30 + 2); las etiquetas 0 y 3 no tienen pareja y dan **`NaN`**. Esto pasa típicamente después de filtrar o reordenar una tabla (el índice conserva las etiquetas viejas). Para operar por posición, usa `.values` o reinicia el índice con `reset_index(drop=True)`. Una columna `NaN` inesperada tras una operación suele ser esto.

Ejemplo comercial: el reporte necesita `importe`, `mes`, `segmento_cliente` y `es_anulada`. Las cuatro son columnas derivadas; después de crearlas verificas una fila a mano y un total contra el SQL.

## Errores comunes

- **No verificar una fila calculada a mano.**
- **Usar `apply` con una función lenta** cuando existe una operación vectorizada.
- **`map` con un diccionario incompleto** y no revisar los `NaN` resultantes.
- **Modificar un subconjunto sin `.copy()`** y perder el cambio.
- **Operar Series con índices distintos** y obtener `NaN` por alineación.
- **Mezclar tipos** (restar texto de número).
- **Sobrescribir la columna original** y perder el dato crudo.

## Para comprobar que entendiste

1. ¿Qué hace `np.where(precio >= 8, "alto", "bajo")`?
2. ¿Qué pasa con los valores que no están en el diccionario de `map`?
3. ¿Qué es la alineación por índice y cuándo da `NaN`?
4. ¿Por qué se prefiere `assign` o una columna nueva en lugar de sobrescribir la original?

<details><summary>Respuestas</summary>

1. Pone «alto» donde el precio es 8 o más y «bajo» donde no.
2. Quedan `NaN`.
3. Pandas empareja los valores por etiqueta de índice; las etiquetas sin pareja dan `NaN`.
4. Para conservar el dato crudo y poder repetir o auditar la transformación.

</details>

## Micropráctica

Con `venta_lineas.csv` y `articulos.csv`:

1. Crea `importe` y `es_bebida` (usando la categoría; necesitarás traerla: para esta práctica usa los `articulo_id` 1, 2 y 3 como bebidas con `isin`).
2. Crea una columna `tramo` con `np.select` que clasifique el importe en `bajo` (< 50), `medio` (50–99) y `alto` (≥ 100).
3. Cuenta cuántas líneas hay en cada tramo y compara que la suma sea 39.
4. Verifica a mano el tramo de la línea 4 (8 × 11,5).

Cómo saber que está bien: la suma de tramos es 39; la línea 4 tiene importe 92, es «medio».

<details><summary>Comprobación de las partes 2 y 3</summary>

```python
import numpy as np
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
lineas["tramo"] = np.select([lineas["importe"] < 50, lineas["importe"] < 100], ["bajo", "medio"], default="alto")
print(lineas["tramo"].value_counts().to_dict(), lineas["tramo"].value_counts().sum())
print(lineas.loc[lineas["linea_id"] == 4, ["importe", "tramo"]].values.tolist())
```

```salida
{'medio': 22, 'bajo': 12, 'alto': 5} 39
[[92.0, 'medio']]
```

</details>

## Después, en los ejercicios

Las columnas derivadas son el centro de P21–P28 en [Python](../../03_EJERCICIOS/Python/) y del paso de transformación (Silver) del mini-ETL. Siguiente: [10.2 groupby y agregaciones](02_groupby_agg.md).
