# 9.2 Series, DataFrame y leer un CSV

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisito: [8.3 Archivos CSV](../08_Python_funciones_archivos/03_archivos_csv_json.md).

## Para qué sirve

Una tabla de datos (filas y columnas con nombre) es lo que manejas casi siempre: ventas, clientes, visitas. Pandas la representa con un **DataFrame**, que combina la comodidad de una hoja de Excel con la potencia de Python. Con él lees un CSV en una línea, calculas sobre columnas enteras y filtras sin escribir bucles. Esta lección te enseña a reconocer sus partes y a leer un archivo con cuidado.

Puedes empezar con tus listas y diccionarios de Python: aquí se presentan Series, índice, tipos y operaciones sobre columnas desde cero. No necesitas construir arreglos de NumPy para resolver P17. [9.1 NumPy](01_numpy_arrays.md) es una consulta opcional si quieres entender la biblioteca que sostiene esos cálculos.

## Términos nuevos

- **Pandas**: la biblioteca de Python para trabajar con datos en forma de tabla. Se importa como `import pandas as pd`.
- **Series**: una columna de datos con nombre y un **índice**. Es como un arreglo de NumPy con etiquetas.
- **DataFrame**: una tabla de columnas (cada una una Series) que comparten el mismo índice. Tiene filas, columnas e índice.
- **Índice** (*index*): las etiquetas de las filas. Por defecto son los números 0, 1, 2... pero pueden ser cualquier cosa. No es una columna más.
- **Columna**: una variable de la tabla, accesible por su nombre: `df["precio"]`.
- **`dtype`** de una columna: su tipo (`int64`, `float64`, `object` para texto, `bool`, `datetime64`).
- **`read_csv`**: la función que lee un archivo CSV y devuelve un DataFrame.
- **`object`**: el tipo con el que Pandas guarda texto (y a veces mezclas).

## Ejemplo paso a paso

**1. Una Series.**

```python
import pandas as pd

ventas = pd.Series([120, 80, 200, 150], index=["lun", "mar", "mié", "jue"], name="ventas_bs")
print(ventas)
print(ventas["mar"])
print(ventas.mean())
```

```salida
lun    120
mar     80
mié    200
jue    150
Name: ventas_bs, dtype: int64
80
137.5
```

Cada valor tiene una etiqueta (`lun`, `mar`...). `ventas["mar"]` busca por etiqueta. Las operaciones (`mean`, `sum`) actúan sobre todos los valores. Si no pones `index`, las etiquetas serían 0, 1, 2, 3.

**2. Un DataFrame construido a mano.**

```python
import pandas as pd

df = pd.DataFrame({
    "tienda": ["La Palma", "El Faro", "Salud"],
    "ruta": ["R01", "R01", "R02"],
    "ventas": [1265.0, 510.0, 557.5],
})
print(df)
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
```

```salida
     tienda ruta  ventas
0  La Palma  R01  1265.0
1   El Faro  R01   510.0
2     Salud  R02   557.5
(3, 3)
['tienda', 'ruta', 'ventas']
tienda     object
ruta       object
ventas    float64
dtype: object
```

Cada clave del diccionario es una columna. A la izquierda de la tabla aparece el **índice** (0, 1, 2), que no es una columna. `shape` es `(filas, columnas)` = `(3, 3)`. `dtypes` muestra `object` para las columnas de texto y `float64` para `ventas`.

**3. Leer un CSV.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas.shape)
print(tiendas.head(3))
print(tiendas.dtypes)
```

```salida
(12, 6)
   tienda_id           nombre              tipo    zona ruta  fecha_alta
0          1  Tienda La Palma  Tienda de barrio   Norte  R01  2025-02-10
1          2   Kiosco El Faro            Kiosco  Centro  R01  2025-03-01
2          3   Farmacia Salud          Farmacia  Centro  R02  2025-03-15
tienda_id      int64
nombre        object
tipo          object
zona          object
ruta          object
fecha_alta    object
dtype: object
```

`pd.read_csv(ruta)` lee el archivo, usa la primera línea como nombres de columna e **infiere el tipo** de cada una. Lo hizo bien: `tienda_id` es entero, y el resto texto (`object`). `head(3)` muestra las primeras 3 filas.

**4. Acceder a una columna y operar sobre ella.**

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
precios = articulos["precio"]
print(type(precios))
print(precios.sum(), precios.mean(), precios.max())
print((precios * 12).head(3))
```

```salida
<class 'pandas.core.series.Series'>
81.0 8.1 14.0
0     72.0
1    108.0
2    138.0
Name: precio, dtype: float64
```

`articulos["precio"]` es una Series. `precios * 12` multiplica **toda la columna** de una vez (vectorización, como en NumPy), sin bucles, y devuelve otra Series con el mismo índice.

**5. Cuidado: Pandas decide los tipos por ti.** Un identificador con ceros a la izquierda se destruye si se interpreta como número. Lo simulamos con un CSV en memoria:

```python
import io
import pandas as pd

texto = "codigo,monto\n007,10\n012,20\n"
mal = pd.read_csv(io.StringIO(texto))
bien = pd.read_csv(io.StringIO(texto), dtype={"codigo": str})

print(mal["codigo"].tolist())
print(bien["codigo"].tolist())
```

```salida
[7, 12]
['007', '012']
```

Sin indicar el tipo, `007` se convirtió en el número 7 y se perdió el código original. Con `dtype={"codigo": str}` se conserva. **Regla: los identificadores y códigos se leen como texto.** (`io.StringIO` convierte un texto en algo que `read_csv` puede leer como si fuera un archivo; es solo para el ejemplo.)

**6. Los vacíos llegan como `NaN`.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas["zona"].isna().sum())
print(tiendas["zona"].isna().tolist()[:6])
```

```salida
2
[False, False, False, False, True, False]
```

`isna()` devuelve `True` donde falta el dato. Pandas leyó los campos vacíos de `zona` como `NaN` (recuerda que con el módulo `csv` de Python llegaban como `''`). Hay 2 faltantes.

**7. Otros parámetros útiles de `read_csv`.** Cuando el archivo no es un CSV estándar:

| Parámetro | Para qué | Ejemplo |
|---|---|---|
| `sep=";"` | el separador no es coma | `pd.read_csv(ruta, sep=";")` |
| `encoding="utf-8-sig"` | archivo con BOM de Excel | |
| `dtype={"col": str}` | forzar tipos | |
| `usecols=["a","b"]` | leer solo algunas columnas | |
| `parse_dates=["fecha"]` | convertir fechas al leer | |
| `decimal=","` | coma decimal | |
| `nrows=5` | leer solo las primeras filas para explorar | |

Si ves una sola columna con todo junto, o nombres de columna con `;`, el separador no es la coma.

Ejemplo comercial: el ERP exporta `ventas.csv` con `;` y decimales con coma. Una lectura con valores por defecto produce una sola columna de texto; con `sep=";"` y `decimal=","` obtienes columnas numéricas. Aun así, abre las primeras líneas antes de confiar.

## Errores comunes

- **Aceptar los tipos que Pandas infiere** sin revisarlos (`dtypes`).
- **Leer códigos o teléfonos como números.**
- **Confundir el índice con una columna.**
- **Ignorar el separador o el decimal** del archivo.
- **Asumir que `NaN` y texto vacío son lo mismo** al comparar con el módulo `csv`.
- **Creer que ver las primeras filas basta** (se profundiza en 9.3).
- **Modificar un DataFrame leído sin guardar una copia del original.**

## Para comprobar que entendiste

1. ¿Cuál es la diferencia entre una Series y un DataFrame?
2. ¿Qué es el índice y qué valor tiene por defecto?
3. ¿Cómo evitas que `007` se lea como el número 7?
4. ¿Qué devuelve `df.shape` para 12 filas y 6 columnas?

<details><summary>Respuestas</summary>

1. Una Series es una columna con índice; un DataFrame es una tabla de varias columnas que comparten índice.
2. Las etiquetas de las filas; por defecto 0, 1, 2...
3. Con `dtype={"codigo": str}` en `read_csv`.
4. `(12, 6)`.

</details>

## Micropráctica

1. Lee `ventas.csv` de la mini-base y muestra su forma, los nombres de columnas y los tipos.
2. Crea un DataFrame a mano con tres artículos (nombre, precio, stock) y calcula el valor de inventario por artículo (`precio * stock`) como nueva columna.
3. Lee `vendedores.csv` y obtén cuántos vendedores hay y cuáles son sus rutas.
4. Simula con `io.StringIO` un CSV con `;` y coma decimal, y léelo correctamente con `sep` y `decimal`.

Cómo saber que está bien: `ventas.csv` tiene forma `(16, 5)`; `vendedores.csv`, 4 filas.

<details><summary>Comprobación de las partes 1 y 3</summary>

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
print(ventas.shape)
print(ventas.dtypes)

vendedores = pd.read_csv("04_DATASETS/mini_base/vendedores.csv")
print(len(vendedores), vendedores["ruta"].tolist())
```

```salida
(16, 5)
venta_id        int64
tienda_id       int64
vendedor_id     int64
fecha          object
estado         object
dtype: object
4 ['R01', 'R02', 'R03', 'R01']
```

</details>

## Después, en los ejercicios

P17–P20 de [Python](../../03_EJERCICIOS/Python/) y el notebook N01 empiezan aquí: cargar los datos, mirar su forma y sus tipos. Siguiente: [9.3 Inspeccionar los datos](03_inspeccionar.md).
