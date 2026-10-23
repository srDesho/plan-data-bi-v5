# 9.1 NumPy: de listas a arreglos

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: [7.8 Listas](../07_Python_basico/08_listas_tuplas.md) y [7.12 Acumuladores](../07_Python_basico/12_acumuladores.md).

## Para qué sirve

En el capítulo 7 sumaste una lista recorriéndola con un `for`. Con miles o millones de datos eso es lento e incómodo. NumPy guarda los números en un **arreglo** y aplica una operación a todos a la vez, sin escribir el recorrido. Es la base sobre la que está construido Pandas: entender el arreglo ahorra mucha confusión después.

## Términos nuevos

- **NumPy**: la biblioteca de Python para cálculo numérico con arreglos. Se importa como `import numpy as np`.
- **Arreglo** (*array*, `ndarray`): una secuencia de números **del mismo tipo** guardada de forma compacta. A diferencia de una lista, no mezcla tipos.
- **Vectorización**: aplicar una operación a todo el arreglo de una vez (`arreglo * 2`) en lugar de recorrerlo con un bucle. Es más corta y mucho más rápida.
- **`shape`** (forma): las dimensiones del arreglo: `(5,)` es una fila de 5 números; `(3, 4)` es una tabla de 3 filas y 4 columnas.
- **`dtype`**: el tipo de los elementos (`int64`, `float64`, `bool`).
- **Máscara booleana**: un arreglo de `True`/`False` obtenido al comparar (`arreglo > 5`); sirve para elegir elementos.
- **`NaN`** (*not a number*): el valor especial de NumPy y Pandas para «dato faltante» en columnas numéricas. Es el equivalente de `NULL`.
- **Desviación estándar** y **varianza**: dos medidas de qué tan dispersos están los datos alrededor de su media (la desviación es la raíz cuadrada de la varianza). Se estudian a fondo en la lección 11.4; aquí solo necesitas saber que NumPy las calcula con `std` y `var`.
- **`ddof`**: «grados de libertad delta». Es el número que se resta de `n` al dividir en la desviación o varianza: `ddof=0` divide entre `n` (poblacional), `ddof=1` entre `n − 1` (muestral).

## Ejemplo paso a paso

**1. De lista a arreglo.**

```python
import numpy as np

ventas_lista = [120, 80, 200, 150]
ventas = np.array(ventas_lista)

print(ventas)
print(ventas.shape, ventas.dtype)
print(type(ventas_lista), type(ventas))
```

```salida
[120  80 200 150]
(4,) int64
<class 'list'> <class 'numpy.ndarray'>
```

`np.array(...)` convierte la lista. `shape` es `(4,)`: un arreglo de una dimensión con 4 elementos; `dtype` es `int64`, enteros.

**2. Una lista no se "multiplica" como esperas; un arreglo sí.** Queremos aplicar un aumento del 10 % a cada venta:

```python
import numpy as np

ventas_lista = [120, 80, 200, 150]
print(ventas_lista * 2)

ventas = np.array(ventas_lista)
print(ventas * 2)
print(ventas * 1.10)
print(ventas + 5)
```

```salida
[120, 80, 200, 150, 120, 80, 200, 150]
[240 160 400 300]
[132.  88. 220. 165.]
[125  85 205 155]
```

- En una **lista**, `* 2` la **repite** (concatena dos veces): no es el cálculo que querías.
- En un **arreglo**, `* 2` multiplica **cada elemento** por 2. También `* 1.10` y `+ 5` actúan elemento por elemento.

Esa es la vectorización: la operación se aplica a todo el arreglo sin que escribas un `for`.

**3. Operaciones entre dos arreglos.** Se hacen posición por posición:

```python
import numpy as np

cantidad = np.array([10, 6, 4])
precio = np.array([6.0, 7.5, 8.0])
importe = cantidad * precio

print(importe)
print(importe.sum())
```

```salida
[60. 45. 32.]
137.0
```

`cantidad * precio` multiplica los elementos de la misma posición (10×6, 6×7,5, 4×8). Es exactamente el cálculo de importe de las líneas de venta, con una instrucción en lugar de un bucle. Para que funcione, ambos arreglos deben tener la misma cantidad de elementos.

**4. Resumir un arreglo.**

```python
import numpy as np

ventas = np.array([120, 80, 200, 150])

print(ventas.sum(), ventas.mean(), ventas.min(), ventas.max())
print(np.median(ventas))
print(round(ventas.std(), 2))
print(round(ventas.std(ddof=1), 2))
```

```salida
550 137.5 80 200
135.0
43.8
50.58
```

Atención al último par: `ventas.std()` usa `ddof=0` (divide entre `n`) y da 43,8; `ventas.std(ddof=1)` divide entre `n − 1` y da 50,58. **NumPy usa por defecto el divisor poblacional**, a diferencia de Pandas y de Excel `DESVEST.M`. Si tus datos son una muestra (casi siempre), escribe `ddof=1` explícitamente.

**5. Máscaras para filtrar.**

```python
import numpy as np

ventas = np.array([120, 80, 200, 150])
mascara = ventas > 100
print(mascara)
print(ventas[mascara])
print((ventas > 100).sum())
```

```salida
[ True False  True  True]
[120 200 150]
3
```

`ventas > 100` produce un arreglo de verdaderos y falsos. Al usarlo entre corchetes, `ventas[mascara]` se queda solo con los elementos donde es `True`. Y como `True` vale 1, `.sum()` cuenta cuántos cumplen (lección 7.6). Las condiciones combinadas usan `&` (y) y `|` (o) con paréntesis: `(ventas > 100) & (ventas < 180)`.

```python
import numpy as np

ventas = np.array([120, 80, 200, 150])
print(ventas[(ventas > 100) & (ventas < 180)])
```

```salida
[120 150]
```

**6. Faltantes: `NaN`.**

```python
import numpy as np

con_faltante = np.array([10.0, np.nan, 30.0])
print(con_faltante.mean())
print(np.nanmean(con_faltante))
print(np.isnan(con_faltante))
```

```salida
nan
20.0
[False  True False]
```

Un solo `NaN` contamina `mean()` y da `nan`. `np.nanmean` ignora los faltantes. **Importante:** ignorar un faltante cambia el denominador: el promedio de 10 y 30 es 20, pero tú decidiste que el dato faltante "no cuenta". Esa decisión debe ser consciente. (Pandas, en cambio, omite los `NaN` automáticamente; lo verás en 9.2.)

**7. Tipos que se mezclan.**

```python
import numpy as np

print(np.array([1, 2, 3.5]))
print(np.array([1, 2, "tres"]))
```

```salida
[1.  2.  3.5]
['1' '2' 'tres']
```

Si mezclas números con un decimal, todo pasa a `float64`. Si mezclas números con texto, **todo pasa a texto** (`<U21` significa cadena de hasta 21 caracteres) y ya no puedes calcular. Es la señal de que un dato mal escrito convirtió la columna entera en texto.

**8. Arreglos de dos dimensiones (solo lo necesario).**

```python
import numpy as np

tabla = np.array([[10, 20, 30],
                  [40, 50, 60]])
print(tabla.shape)
print(tabla.sum(axis=0))
print(tabla.sum(axis=1))
```

```salida
(2, 3)
[50 70 90]
[ 60 150]
```

`axis=0` suma **por columnas** (baja por las filas) y `axis=1` suma **por filas**. Pandas oculta casi siempre estos detalles con nombres de columna, pero el concepto aparece al calcular totales por fila o por columna.

Ejemplo comercial: tienes dos columnas, `cantidad` y `precio`, de 100 000 líneas. Con arreglos, `(cantidad * precio).sum()` calcula el total de ventas en una línea y en milisegundos; con un `for` y un acumulador sería más largo y más lento, aunque daría el mismo resultado.

## Errores comunes

- **Esperar que `lista * 2` multiplique** (la repite).
- **Mezclar tipos** y que el arreglo se convierta en texto sin avisar.
- **Usar `np.std()` creyendo que es muestral** (divide entre `n`).
- **Un `NaN` que contamina el promedio** y no se detecta.
- **Operar arreglos de distinto tamaño** (error de forma).
- **Usar `and`/`or`** en lugar de `&`/`|` con máscaras.
- **Olvidar los paréntesis** en condiciones combinadas.

## Para comprobar que entendiste

1. ¿Qué devuelve `np.array([1, 2, 3]) * 2`? ¿Y `[1, 2, 3] * 2`?
2. ¿Qué divisor usa `np.std` por defecto?
3. ¿Qué hace `ventas[ventas > 100]`?
4. ¿Qué pasa con `np.mean` si hay un `NaN`?

<details><summary>Respuestas</summary>

1. `[2 4 6]`; y la lista `[1, 2, 3, 1, 2, 3]`.
2. `n` (poblacional, `ddof=0`).
3. Devuelve solo los elementos mayores que 100.
4. Devuelve `nan`; hay que usar `np.nanmean` o decidir qué hacer con el faltante.

</details>

<a id="micropractica"></a>

## Micropráctica

Con `precios = [6.0, 9.0, 11.5, 7.5]` y `unidades = [10, 8, 4, 6]`:

1. Calcula con arreglos el importe de cada línea y el total.
2. Aplica un descuento del 5 % al precio y muestra los nuevos precios redondeados a 2 decimales (`np.round`).
3. ¿Cuántos precios son mayores que 7? Respóndelo con una máscara.
4. Calcula la desviación estándar muestral y la poblacional de los precios y explica por qué difieren.

Cómo saber que está bien: importes `[60, 72, 46, 45]` y total 223; 3 precios mayores que 7.

<details><summary>Comprobación</summary>

```python
import numpy as np

precios = np.array([6.0, 9.0, 11.5, 7.5])
unidades = np.array([10, 8, 4, 6])
importe = precios * unidades
print(importe, importe.sum())
print(np.round(precios * 0.95, 2))
print((precios > 7).sum())
print(round(precios.std(ddof=1), 2), round(precios.std(), 2))
```

```salida
[60. 72. 46. 45.] 223.0
[ 5.7   8.55 10.92  7.12]
3
2.35 2.03
```

</details>

## Después, en los ejercicios

NumPy se usa de apoyo en los ejercicios de estadística (ST01–ST04) y en los P17–P20 de [Python](../../03_EJERCICIOS/Python/) cuando la guía lo pida. Siguiente: [9.2 Series, DataFrame y leer un CSV](02_series_dataframe_csv.md).
