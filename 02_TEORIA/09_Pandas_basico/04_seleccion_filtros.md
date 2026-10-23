# 9.4 Seleccionar, filtrar y ordenar

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [9.2 Series y DataFrame](02_series_dataframe_csv.md) y [7.6 Booleanos](../07_Python_basico/06_booleanos_comparaciones_none.md).

## Para qué sirve

Es el `SELECT … WHERE … ORDER BY` de Pandas: elegir columnas, quedarse con las filas que cumplen una condición y ordenar. Si ya sabes SQL (capítulos 1 a 4), esta lección es una traducción; si algo se parece pero se comporta distinto (el `&` en lugar de `AND`, los paréntesis obligatorios), conviene saberlo antes de que cause un resultado incorrecto.

## Términos nuevos

- **Selección de columnas**: elegir cuáles columnas ver: `df[["a", "b"]]`.
- **`loc`**: selecciona por **etiquetas** del índice y por máscaras booleanas. `df.loc[filas, columnas]`.
- **`iloc`**: selecciona por **posición** numérica (0, 1, 2...).
- **Máscara booleana**: una Series de `True`/`False` del mismo largo que la tabla; elige las filas donde es `True`.
- **`&`, `|`, `~`**: «y», «o» y «no» entre máscaras. Cada condición va **entre paréntesis**.
- **`isin`**: pregunta si el valor está en una lista (equivale a `IN` de SQL).
- **`copy()`**: crea una tabla independiente. Se usa antes de modificar un subconjunto para evitar efectos inesperados.
- **`sort_values`**: ordena la tabla por una o más columnas.

## Ejemplo paso a paso

**1. Columnas.** Una columna da una Series; una lista de columnas, un DataFrame:

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas["nombre"].head(2))
print(tiendas[["nombre", "zona"]].head(2))
```

```salida
0    Tienda La Palma
1     Kiosco El Faro
Name: nombre, dtype: object
            nombre    zona
0  Tienda La Palma   Norte
1   Kiosco El Faro  Centro
```

Los corchetes dobles `[["nombre", "zona"]]` son una lista dentro de los corchetes: eso devuelve una tabla. Es el equivalente de `SELECT nombre, zona`.

**2. Filtrar filas con una condición.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
mascara = tiendas["ruta"] == "R01"
print(mascara.head(4).tolist())
print(tiendas.loc[mascara, ["tienda_id", "nombre", "ruta"]])
```

```salida
[True, True, False, False]
   tienda_id           nombre ruta
0          1  Tienda La Palma  R01
1          2   Kiosco El Faro  R01
6          7  Tienda Don Pepe  R01
9         10      Kiosco Luna  R01
```

`tiendas["ruta"] == "R01"` produce una Series de verdaderos y falsos (una por fila). Dentro de `loc[máscara, columnas]` se queda con las filas verdaderas y las columnas pedidas. Es `WHERE ruta = 'R01'`.

**3. Varias condiciones: `&`, `|` y paréntesis.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
condicion = (tiendas["ruta"] == "R01") & (tiendas["tipo"] == "Kiosco")
print(tiendas.loc[condicion, ["tienda_id", "nombre"]])

condicion_o = (tiendas["ruta"] == "R03") | (tiendas["zona"] == "Centro")
print(len(tiendas.loc[condicion_o]))
```

```salida
   tienda_id          nombre
1          2  Kiosco El Faro
9         10     Kiosco Luna
7
```

Dos reglas que no se negocian:

1. Usa **`&` y `|`**, no `and`/`or` (esos fallan con series).
2. **Cada condición entre paréntesis**: por la precedencia de operadores, `a == 1 & b == 2` se evalúa mal y da error.

**4. `isin`, `between` y negación.**

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
print(articulos.loc[articulos["categoria"].isin(["Bebidas", "Lácteos"]), "nombre"].tolist())
print(articulos.loc[articulos["precio"].between(6, 9), "nombre"].tolist())
print(articulos.loc[~articulos["categoria"].isin(["Bebidas"]), "nombre"].tolist())
```

```salida
['Agua 2L', 'Jugo 1L', 'Gaseosa 2L', 'Leche 1L', 'Yogurt 1L']
['Agua 2L', 'Jugo 1L', 'Papas 100g', 'Leche 1L']
['Papas 100g', 'Galletas', 'Maní 80g', 'Detergente 1kg', 'Jabón', 'Leche 1L', 'Yogurt 1L']
```

`isin([...])` es el `IN`. `between(6, 9)` incluye **ambos extremos**, igual que `BETWEEN`. `~` niega la condición.

**5. Texto: `str.contains`, `str.startswith`.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas.loc[tiendas["nombre"].str.contains("kiosco", case=False), "tienda_id"].tolist())
print(tiendas.loc[tiendas["nombre"].str.strip().str.startswith("Kiosco"), "tienda_id"].tolist())
```

```salida
[2, 5, 10]
[2, 5, 10]
```

Los métodos de texto de una columna van tras `.str`. `contains("kiosco", case=False)` ignora mayúsculas (es el `LIKE '%kiosco%'`). Igual que en SQL, `startswith("Kiosco")` sin limpiar espacios perdería la tienda 5; por eso se aplica antes `.str.strip()`.

**6. Los vacíos en filtros.** Una comparación con `NaN` da `False`; usa `isna()`:

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
no_norte = tiendas["zona"] != "Norte"
print(no_norte.sum())
print((no_norte | tiendas["zona"].isna()).sum())
print(tiendas["zona"].isna().sum())
```

```salida
9
9
2
```

`!= "Norte"` incluye las filas con `NaN` en Pandas (diferente de SQL, donde `<> 'Norte'` las pierde). Aquí `no_norte.sum()` da 9: 7 con otra zona más las 2 sin zona. Esta diferencia con SQL es una trampa: **cada herramienta trata los vacíos a su manera**; verifica con un conteo conocido.

**7. `iloc`: por posición.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas.iloc[0, 1])
print(tiendas.iloc[:3, :2])
```

```salida
Tienda La Palma
   tienda_id           nombre
0          1  Tienda La Palma
1          2   Kiosco El Faro
2          3   Farmacia Salud
```

`iloc[fila, columna]` usa posiciones desde 0 y la rebanada **excluye** el final. `iloc[:3, :2]` son las 3 primeras filas y las 2 primeras columnas. Úsalo para «las primeras n filas» o cuando no importa el nombre.

**8. Ordenar.**

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
orden = articulos.sort_values(["categoria", "precio"], ascending=[True, False])
print(orden[["categoria", "nombre", "precio"]].head(5))
```

```salida
  categoria          nombre  precio
2   Bebidas      Gaseosa 2L    11.5
1   Bebidas         Jugo 1L     9.0
0   Bebidas         Agua 2L     6.0
6  Limpieza  Detergente 1kg    14.0
7  Limpieza           Jabón     3.5
```

`sort_values` acepta una lista de columnas y una lista de direcciones. Igual que en SQL, si hay empates, el orden entre ellos **no está garantizado**: añade una columna única al final para desempatar (lección 1.5). Fíjate también en que el índice original se conserva; si quieres numerarlo de nuevo, usa `reset_index(drop=True)`.

**9. Trabajar sobre una copia antes de modificar.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
r01 = tiendas.loc[tiendas["ruta"] == "R01"].copy()
r01["nombre"] = r01["nombre"].str.strip()
print(len(r01), len(tiendas))
```

```salida
4 12
```

`.copy()` hace explícito que `r01` es una tabla independiente. Sin él, Pandas puede mostrar una advertencia (`SettingWithCopyWarning`) porque no sabe si quieres modificar la tabla original o el subconjunto; y a veces el cambio se pierde.

**10. Traducción rápida SQL → Pandas.**

| SQL | Pandas |
|---|---|
| `SELECT a, b` | `df[["a", "b"]]` |
| `WHERE x = 1` | `df.loc[df["x"] == 1]` |
| `WHERE x = 1 AND y > 2` | `df.loc[(df["x"] == 1) & (df["y"] > 2)]` |
| `WHERE x IN (1, 2)` | `df.loc[df["x"].isin([1, 2])]` |
| `ORDER BY x DESC` | `df.sort_values("x", ascending=False)` |
| `LIMIT 5` | `df.head(5)` |
| `DISTINCT x` | `df["x"].drop_duplicates()` |

Ejemplo comercial: «las ventas entregadas de la ruta R02 en septiembre» es una máscara con tres condiciones (estado, ruta y rango de fecha) entre paréntesis. El control: compara el número de filas con el que da la consulta equivalente en SQL.

## Errores comunes

- **Usar `and`/`or`** con series (`ValueError`).
- **Olvidar los paréntesis** alrededor de cada condición.
- **Confundir `loc` con `iloc`** (etiquetas frente a posiciones).
- **Modificar un subconjunto sin `.copy()`.**
- **Suponer que `!=` pierde los vacíos como en SQL.**
- **Ordenar sin desempate** cuando importa el orden.
- **Esperar que `sort_values` modifique la tabla**: devuelve una nueva (salvo `inplace=True`, que conviene evitar).

## Para comprobar que entendiste

1. ¿Qué devuelve `df["a"]` y qué `df[["a"]]`?
2. ¿Por qué `df.loc[df["x"] > 1 & df["y"] < 5]` falla?
3. ¿Qué diferencia hay entre `loc` e `iloc`?
4. ¿Qué hace `~`?

<details><summary>Respuestas</summary>

1. Una Series (columna) y un DataFrame de una columna.
2. Falta el paréntesis alrededor de cada condición; por la precedencia, `&` se evalúa antes que las comparaciones.
3. `loc` selecciona por etiquetas o máscaras; `iloc` por posición numérica.
4. Niega una máscara booleana.

</details>

<a id="micropractica"></a>

## Micropráctica

Con `ventas.csv`:

1. Las ventas entregadas de la tienda 1 o 3, con las columnas `venta_id`, `tienda_id` y `fecha`, ordenadas por fecha.
2. Cuántas ventas hay en septiembre (usa `str.startswith("2026-09")` sobre la fecha o `between`).
3. Las ventas anuladas, con la tienda y la fecha.
4. Compara el resultado de la 1 con la consulta equivalente de SQL de la lección 1.3 (cuenta las filas).

Cómo saber que está bien: 1 → 6 ventas (3 de la tienda 1 y 3 de la tienda 3, todas entregadas); 2 → 9 ventas; 3 → 2 filas.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
filtro = ventas["tienda_id"].isin([1, 3]) & (ventas["estado"] == "entregado")
print(ventas.loc[filtro, ["venta_id", "tienda_id", "fecha"]].sort_values("fecha"))
print(ventas["fecha"].str.startswith("2026-09").sum())
```

```salida
    venta_id  tienda_id       fecha
0          1          1  2026-08-03
2          3          3  2026-08-07
4          5          1  2026-08-19
8          9          3  2026-09-04
13        14          1  2026-09-22
15        16          3  2026-09-29
9
```

</details>

## Después, en los ejercicios

Filtrar y seleccionar son la base de P17–P20 en [Python](../../03_EJERCICIOS/Python/) y del paso de limpieza del mini-ETL. Siguiente: [9.5 Nulos y duplicados](05_nulos_duplicados.md).
