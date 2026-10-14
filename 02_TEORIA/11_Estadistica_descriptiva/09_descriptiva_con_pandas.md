# 11.9 Estadística descriptiva con Pandas: un informe completo

> Tiempo estimado: 60 min (lectura 20 + práctica 40). Prerrequisitos: lecciones 11.1 a 11.8 y el capítulo 10 (`groupby` y `merge`).

## Para qué sirve

Ya calculaste cada medida a mano con pocos datos. Con miles de filas usarás Pandas, que resume todo en una instrucción, pero hay trampas: el divisor de la desviación, los valores vacíos, el método de los cuartiles. Aquí juntas todo en un procedimiento repetible y en un informe corto que podrías mostrar a un gerente.

## Términos nuevos

- **`describe()`**: el método de Pandas que devuelve de golpe la cantidad de datos, la media, la desviación, el mínimo, los cuartiles y el máximo.
- **Resumen por grupo**: aplicar las medidas a cada categoría por separado con `groupby`.
- **Informe descriptivo**: un resumen escrito de una variable que incluye tamaño, tipo, vacíos, centro, dispersión, forma, atípicos, conclusión y limitaciones.
- **Dato vacío** (`NaN`): valor faltante. La mayoría de las funciones de Pandas lo **omiten** en silencio.

## Ejemplo paso a paso

**1. Preparar la variable de análisis.** El importe de cada línea de venta (`cantidad × precio_unitario`) de la mini-base:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
print(lineas[["linea_id", "cantidad", "precio_unitario", "importe"]].head(3))
print(len(lineas), lineas["importe"].isna().sum())
```

```salida
   linea_id  cantidad  precio_unitario  importe
0         1        10              6.0     60.0
1         2         6              7.5     45.0
2         3         4              8.0     32.0
39 0
```

Primer control: 39 líneas y 0 vacíos en `importe`. **Unidad de análisis**: una línea de venta. **Variable**: `importe`, cuantitativa continua, en Bs.

**2. `describe()`.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
print(lineas["importe"].describe().round(2))
```

```salida
count     39.00
mean      69.78
std       36.75
min       27.00
25%       45.00
50%       60.00
75%       90.00
max      230.00
Name: importe, dtype: float64
```

Cómo leerlo: `count` es `n`; `mean` la media; `std` la desviación **muestral** (`n − 1`); `min` y `max` los extremos; `25%`, `50%` y `75%` son Q1, mediana y Q3 con interpolación lineal (el método de 11.5). Notarás que `mean` (aprox. 69,8) es mayor que `50%` (aprox. 60): la asimetría positiva de siempre.

**3. Completar con lo que `describe` no da.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
importe = lineas["importe"]

q1, q3 = importe.quantile(0.25), importe.quantile(0.75)
iqr = q3 - q1
cerca_sup = q3 + 1.5 * iqr
cerca_inf = q1 - 1.5 * iqr
atipicos = importe[(importe > cerca_sup) | (importe < cerca_inf)]

print("moda:", importe.mode().tolist())
print("rango:", importe.max() - importe.min())
print("coef. de variación (%):", round(importe.std() / importe.mean() * 100, 1))
print("asimetría:", round(importe.skew(), 2))
print("cercas:", cerca_inf, cerca_sup)
print("atípicos:", atipicos.tolist())
```

```salida
moda: [60.0, 90.0]
rango: 203.0
coef. de variación (%): 52.7
asimetría: 2.26
cercas: -22.5 157.5
atípicos: [230.0]
```

El coeficiente de variación (unos 53 %) indica una dispersión alta. La asimetría positiva (2,26) confirma una cola a la derecha. La cerca superior es Bs 157,5 y solo una línea la supera: la de Bs 230. Hay dos modas (60 y 90).

**4. Resumen por grupo.** ¿Cómo se comporta el importe por categoría de artículo? Primero traemos la categoría uniendo con `articulos` (relación muchos a uno, por lo que no cambia el número de filas):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]

unido = lineas.merge(articulos[["articulo_id", "categoria"]], on="articulo_id", how="left", validate="m:1")
print(len(lineas), len(unido))

resumen = unido.groupby("categoria")["importe"].agg(["count", "mean", "median", "std", "min", "max"]).round(1)
print(resumen)
```

```salida
39 39
           count  mean  median   std   min    max
categoria                                        
Bebidas       15  95.9    90.0  42.2  54.0  230.0
Limpieza       6  38.5    38.5  10.6  28.0   56.0
Lácteos        8  66.0    62.0  22.0  32.0   96.0
Snacks        10  52.4    47.5  18.6  27.0   90.0
```

Dos controles inmediatos: el número de filas no cambió (39 antes y después de unir), y la columna `count` suma 39. Ahora puedes comparar categorías: la mediana y la media de cada una, y su dispersión. Con entre 6 y 15 líneas por categoría, cualquier diferencia entre categorías hay que leerla con cautela: son pocos datos.

**5. Las trampas clásicas, en una tabla.**

| Trampa | Qué ocurre | Qué hacer |
|---|---|---|
| Divisor de la desviación | Pandas `std()` usa `n − 1`; NumPy `np.std()` usa `n` | escribir cuál usas; `ddof=1` en NumPy |
| Vacíos | `mean`, `std`, `describe` los omiten sin avisar | contar `isna().sum()` antes y reportarlo |
| Método de cuartiles | `statistics.quantiles` usa otro método que Pandas | usar un solo método y declararlo |
| Variable de texto | un monto en texto no entra en `describe` numérico | convertir con `pd.to_numeric` y revisar errores |
| Códigos como números | promediar `venta_id` no significa nada | excluirlos del resumen numérico |
| Unidad de análisis mezclada | resumir importes de líneas como si fueran ventas | agregar primero a la granularidad correcta |

**6. El informe descriptivo (plantilla).** Con los resultados anteriores, un párrafo como este:

> *Se analizó el importe de las 39 líneas de venta de la mini-base (unidad de análisis: línea; variable cuantitativa continua, en Bs; sin valores vacíos). El importe típico (mediana) es de Bs 60 y el promedio de Bs 69,8; la media supera a la mediana porque la distribución tiene cola derecha (asimetría positiva). La desviación estándar muestral es de Bs 36,75 (coeficiente de variación ≈ 53 %): la dispersión es alta. Según la regla de Tukey, hay un importe atípico (Bs 230) por encima de la cerca superior de Bs 157,5; se recomienda revisar si corresponde a una venta mayorista real. Limitación: son datos inventados de una sola base pequeña y no permiten generalizar.*

Cada frase tiene un dato verificable y una interpretación. **El informe termina con una limitación**, no con un «todo está bien».

Ejemplo comercial: un gerente pide «un resumen de las ventas por cliente». Entregas la tabla de `describe`, la mediana y los atípicos con una frase de recomendación: «cinco clientes concentran el 30 % de la venta: asignarles un ejecutivo». Sin la limitación («datos de un trimestre») sería una afirmación incompleta.

## Errores comunes

- **Pegar el resultado de `describe()` sin interpretar.**
- **No contar los vacíos** y no decir cuántos datos entraron.
- **Reportar solo la media** en variables con cola.
- **Mezclar divisores** al comparar con Excel o NumPy.
- **Resumir una columna de códigos** como si fuera una cantidad.
- **Unir tablas sin controlar el número de filas.**
- **Informes sin limitación** ni mención de la población.

## Para comprobar que entendiste

1. ¿Qué divisor usa `Series.std()` por defecto?
2. ¿Qué hace `describe()` con los valores vacíos?
3. ¿Por qué se controla el número de filas después de un `merge`?
4. ¿Qué elementos debe tener un informe descriptivo?

<details><summary>Respuestas</summary>

1. `n − 1` (desviación muestral).
2. Los omite; hay que contarlos aparte.
3. Para detectar duplicaciones o pérdidas silenciosas.
4. Tamaño y unidad de análisis, tipo de variable, vacíos, centro, dispersión, forma, atípicos, conclusión y limitación.

</details>

## Micropráctica

Con el precio de `articulos.csv`:

1. Calcula `describe()` y completa con la moda, el rango, el coeficiente de variación, la asimetría y los atípicos de Tukey.
2. Calcula la media y la mediana por categoría.
3. Redacta el informe descriptivo de cuatro frases siguiendo la plantilla (con la limitación).

Cómo saber que está bien: `count` = 10, `mean` = 8,1; ningún atípico por Tukey.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
precio = articulos["precio"]
print(precio.describe().round(2))
q1, q3 = precio.quantile(0.25), precio.quantile(0.75)
iqr = q3 - q1
print(precio[(precio > q3 + 1.5 * iqr) | (precio < q1 - 1.5 * iqr)].tolist())
print(articulos.groupby("categoria")["precio"].agg(["mean", "median"]).round(2))
```

```salida
count    10.00
mean      8.10
std       3.51
min       3.50
25%       5.25
50%       7.75
75%      10.88
max      14.00
Name: precio, dtype: float64
[]
            mean  median
categoria               
Bebidas     8.83    9.00
Limpieza    8.75    8.75
Lácteos    10.00   10.00
Snacks      5.67    5.00
```

</details>

## Después, en los ejercicios

Aquí empieza la preparación para ST01–ST04 y el caso C03 de [Estadística](../../03_EJERCICIOS/Estadistica/): cuando los resuelvas, entrega la tabla, la plantilla de informe y una limitación. No reutilices los números de estos ejemplos. Siguiente capítulo: [Capítulo 12 — Inferencia](../12_Estadistica_inferencia.md).
