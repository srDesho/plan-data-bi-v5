# 11.4 Dispersión: rango, varianza y desviación estándar

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisito: [11.3 Media, mediana y moda](03_media_mediana_moda.md).

En la primera sesión, calcula con la tabla de desviaciones y una calculadora. La raíz cuadrada es el número que multiplicado por sí mismo devuelve la varianza; en Python se escribe `varianza ** 0.5`. Comprueba después con el módulo estándar `statistics`, cuyo uso inicial se explica en 11.3. Los ejemplos de Pandas y NumPy comparan herramientas para una fase posterior; no son prerrequisitos del cálculo manual ni de ST01.

## Para qué sirve

Dos repartidores pueden tener el mismo promedio de entregas (20 al día) y ser totalmente distintos: uno entrega siempre entre 19 y 21, el otro oscila entre 5 y 35. Si solo miras el promedio no ves la diferencia. La **dispersión** mide cuánto se separan los datos de su centro. Es indispensable para decidir cuánta confianza tener en un promedio, y la usarás en todo el capítulo 12.

## Términos nuevos

- **Dispersión** (o variabilidad): qué tan separados están los datos entre sí o de su media.
- **Rango**: máximo menos mínimo.
- **Desviación**: la diferencia entre un dato y la media: `x − x̄`. Algunas son positivas y otras negativas; su suma siempre es cero.
- **Varianza**: el promedio de los **cuadrados** de las desviaciones. Se eleva al cuadrado para que las desviaciones negativas y positivas no se cancelen. Sus unidades son las unidades al cuadrado (entregas², Bs²).
- **Varianza poblacional** (`σ²`, sigma cuadrado): se divide entre `n`. Se usa cuando tienes **toda** la población.
- **Varianza muestral** (`s²`): se divide entre `n − 1`. Se usa cuando tienes una **muestra** y quieres estimar la variabilidad de la población.
- **Desviación estándar**: la raíz cuadrada de la varianza. Vuelve a las unidades originales (entregas, Bs), por eso es la más usada para comunicar. Se escribe `σ` (población) o `s` (muestra).
- **Grados de libertad**: aquí, `n − 1`: la cantidad de datos que pueden variar libremente cuando la media ya está fija.
- **Coeficiente de variación**: la desviación estándar dividida entre la media (`s / x̄`); permite comparar la variabilidad de variables en distintas unidades o escalas.

## Ejemplo paso a paso

Los mismos 10 repartidores de 11.3: `12, 15, 15, 18, 20, 22, 25, 28, 30, 55`, con media `x̄ = 24`.

**1. Rango.** Máximo 55 − mínimo 12 = **43** entregas. Es fácil de calcular pero depende solo de los dos extremos: el 55 lo agranda mucho.

**2. Desviaciones y sus cuadrados.** Se calcula la tabla (media = 24):

| Dato `x` | Desviación `x − 24` | Cuadrado `(x − 24)²` |
|---|---|---|
| 12 | −12 | 144 |
| 15 | −9 | 81 |
| 15 | −9 | 81 |
| 18 | −6 | 36 |
| 20 | −4 | 16 |
| 22 | −2 | 4 |
| 25 | 1 | 1 |
| 28 | 4 | 16 |
| 30 | 6 | 36 |
| 55 | 31 | 961 |
| **Suma** | **0** | **1376** |

Dos controles: la suma de las desviaciones es **0** (siempre, por definición de la media); la suma de cuadrados es **1376**. Si tu suma de desviaciones no da 0, hay un error de cálculo en la media o en una resta.

**3. Varianza poblacional** (si estas 10 personas son *toda* la población): 1376 / 10 = **137,6**.

**4. Varianza muestral** (si son una muestra de una población más grande): 1376 / (10 − 1) = 1376 / 9 = **152,89**.

**5. Desviación estándar.** Raíz cuadrada:

- poblacional: √137,6 = **11,73** entregas;
- muestral: √152,89 = **12,36** entregas.

La interpretación: «un repartidor típico se aleja de la media de 24 entregas en unos 12 entregas». Es una forma de medir la dispersión *típica*, no un límite.

**6. ¿Por qué se divide entre `n − 1` en la muestra?** Cuando calculas la media con la propia muestra, los datos quedan un poco «más cerca» de esa media de lo que estarían de la media verdadera de la población, así que los cuadrados salen demasiado pequeños. Dividir entre `n − 1` en vez de `n` corrige ese sesgo. No hace falta demostrarlo: lo que debes recordar es **usar `n − 1` cuando los datos son una muestra** (que es lo habitual) y `n` solo cuando tienes toda la población.

**7. Verificar con Python.**

```python
import statistics

entregas = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
print(statistics.pvariance(entregas))
print(statistics.variance(entregas))
print(round(statistics.pstdev(entregas), 2))
print(round(statistics.stdev(entregas), 2))
```

```salida
137.6
152.88888888888889
11.73
12.36
```

En el módulo `statistics`, el prefijo `p` indica **población** (`pvariance`, `pstdev`, dividen entre `n`) y los nombres sin prefijo son **muestrales** (`variance`, `stdev`, dividen entre `n − 1`). Los resultados coinciden con los de la tabla.

**8. Pandas y NumPy no usan el mismo divisor.** Esta es una trampa clásica:

```python
import numpy as np
import pandas as pd

datos = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
print(round(pd.Series(datos).std(), 2))
print(round(np.std(datos), 2))
print(round(np.std(datos, ddof=1), 2))
```

```salida
12.36
11.73
12.36
```

- `Series.std()` de Pandas usa por defecto `n − 1` (muestral): 12,36.
- `np.std()` de NumPy usa por defecto `n` (poblacional): 11,73.
- `np.std(datos, ddof=1)` (los «grados de libertad delta») fuerza `n − 1`: 12,36.

Si comparas dos resultados de herramientas distintas y no coinciden, mira primero el divisor. **Escribe siempre en tu reporte si la desviación es muestral o poblacional.** Excel tiene `DESVEST.M` (muestral) y `DESVEST.P` (poblacional).

**9. Dos repartidores, mismo promedio.**

```python
import statistics

estable = [19, 20, 21, 20, 20]
variable = [5, 35, 20, 10, 30]
print(statistics.mean(estable), statistics.mean(variable))
print(round(statistics.stdev(estable), 2), round(statistics.stdev(variable), 2))
```

```salida
20 20
0.71 12.75
```

Ambos promedian 20, pero la desviación estándar es 0,71 frente a 12,75. El promedio los muestra iguales; la dispersión revela que el segundo es **mucho menos predecible**.

**10. Coeficiente de variación.** Para comparar la variabilidad de cosas medidas en escalas diferentes (entregas diarias y ventas en Bs), se divide la desviación entre la media: con los datos del punto 7, `12,36 / 24 = 0,515`, es decir 51,5 %. Una desviación del 51,5 % del promedio es una dispersión alta; la de `estable` es 0,71 / 20 = 3,5 %.

Ejemplo comercial: dos vendedores con un promedio de ventas semanal igual (Bs 1 000) pero uno con desviación de Bs 50 y otro de Bs 400. El segundo es difícil de presupuestar y de evaluar con una sola semana de datos.

## Errores comunes

- **Dividir entre `n` cuando los datos son una muestra** (y no decirlo).
- **Mezclar resultados de Pandas, NumPy y Excel** sin revisar el divisor.
- **Interpretar la varianza como si estuviera en las unidades originales**: está al cuadrado.
- **Confundir «desviación estándar» con «error» o con «rango»**.
- **Creer que la desviación estándar es el máximo que se puede separar un dato** de la media.
- **Calcular dispersión de una variable categórica.**
- **Olvidar el control «las desviaciones suman 0»** al calcular a mano.

## Para comprobar que entendiste

1. ¿Por qué la suma de las desviaciones respecto a la media es siempre 0?
2. Con `n = 5` y suma de cuadrados 40, ¿cuánto vale la varianza muestral y cuánto la poblacional?
3. ¿Qué devuelve `np.std(datos)` por defecto: dispersión muestral o poblacional?
4. ¿Por qué se usa la desviación estándar en lugar de la varianza para comunicar?

<details><summary>Respuestas</summary>

1. Porque las desviaciones positivas y negativas se compensan exactamente cuando la media es el punto de equilibrio de los datos.
2. Muestral: 40 / 4 = 10. Poblacional: 40 / 5 = 8.
3. Poblacional (divide entre `n`).
4. Porque está en las mismas unidades que los datos (Bs, entregas).

</details>

<a id="micropractica"></a>

## Micropráctica

Con las ventas diarias (en Bs) de un puesto de venta durante una semana: `[310, 275, 410, 360, 295, 330, 300]`:

1. Calcula **a mano** la media (2 280 / 7), arma la tabla de desviaciones y cuadrados (trabaja con la media redondeada a 325,71), y obtén la varianza muestral y la desviación estándar muestral. Comprueba que las desviaciones suman (casi) 0.
2. Verifica con `statistics.variance` y `statistics.stdev`.
3. Calcula el coeficiente de variación e interpreta si la venta diaria es estable.

Cómo saber que está bien: la desviación estándar muestral es cercana a 46; el coeficiente de variación ronda 14 %.

<details><summary>Comprobación</summary>

```python
import statistics

ventas = [310, 275, 410, 360, 295, 330, 300]
media = statistics.mean(ventas)
print(round(media, 2))
print(round(statistics.variance(ventas), 2))
print(round(statistics.stdev(ventas), 2))
print(round(statistics.stdev(ventas) / media * 100, 1))
```

```salida
325.71
2120.24
46.05
14.1
```

</details>

## Después, en los ejercicios

ST01–ST03 de [Estadística](../../03_EJERCICIOS/Estadistica/) piden desviación estándar muestral; asegúrate de usar el divisor correcto en tu herramienta. Siguiente: [11.5 Percentiles, cuartiles y atípicos](05_percentiles_atipicos.md).
