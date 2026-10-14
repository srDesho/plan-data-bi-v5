# 11.5 Percentiles, cuartiles y valores atípicos

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisitos: [11.3](03_media_mediana_moda.md) y [11.4](04_dispersion.md).

## Para qué sirve

La media y la desviación son sensibles a los valores extremos. Los percentiles describen la **posición** de un dato dentro del conjunto («el 90 % de las tiendas vende menos que esta») y no se distorsionan con extremos. Además permiten detectar de forma objetiva qué valores son **atípicos** y merecen revisión, en lugar de decidir «a ojo».

## Términos nuevos

- **Percentil `P`**: el valor por debajo del cual queda aproximadamente el `P` % de los datos. El percentil 50 es la mediana.
- **Cuartiles**: los percentiles 25, 50 y 75. **Q1** (primer cuartil) deja el 25 % de los datos por debajo; **Q2** es la mediana; **Q3** deja el 75 % por debajo.
- **Rango intercuartílico** (`IQR`): `Q3 − Q1`. Es el ancho del 50 % central de los datos; no se ve afectado por los extremos.
- **Interpolación lineal**: cuando la posición del percentil cae entre dos datos, se toma un punto proporcional entre ellos.
- **Valor atípico** (*outlier*): un dato inusualmente lejano al resto. No es necesariamente un error: puede ser un caso real extraordinario (una venta mayorista).
- **Regla de Tukey**: se consideran atípicos los valores menores que `Q1 − 1,5 × IQR` o mayores que `Q3 + 1,5 × IQR`. Esos dos límites se llaman **cercas** (*fences*).
- **Diagrama de caja** (*boxplot*): un gráfico que dibuja Q1, mediana y Q3 como una caja y marca los atípicos como puntos.

## Ejemplo paso a paso

Datos: entregas de 10 repartidores, ya ordenados: `12, 15, 15, 18, 20, 22, 25, 28, 30, 55` (n = 10).

**1. Posición del percentil.** Un método muy usado (el de NumPy, Pandas y Excel `PERCENTIL.INC`) calcula la posición `p = 1 + (n − 1) × P/100`, contando desde 1, e interpola si no es entera.

- **Mediana (P50)**: posición `1 + 9 × 0,50 = 5,5` → entre el 5.º (20) y el 6.º (22): 20 + 0,5 × (22 − 20) = **21**.
- **Q1 (P25)**: posición `1 + 9 × 0,25 = 3,25` → entre el 3.º (15) y el 4.º (18): 15 + 0,25 × (18 − 15) = **15,75**.
- **Q3 (P75)**: posición `1 + 9 × 0,75 = 7,75` → entre el 7.º (25) y el 8.º (28): 25 + 0,75 × (28 − 25) = **27,25**.

**2. IQR y cercas de Tukey.**

- `IQR = Q3 − Q1 = 27,25 − 15,75 = 11,5`.
- `1,5 × IQR = 17,25`.
- Cerca inferior: `15,75 − 17,25 = −1,5`.
- Cerca superior: `27,25 + 17,25 = 44,5`.

Un valor es atípico si es menor que −1,5 (ninguno) o mayor que 44,5 (el **55**). Conclusión: el repartidor con 55 entregas es un atípico según la regla de Tukey.

**3. Verificar con NumPy y Pandas.**

```python
import numpy as np
import pandas as pd

entregas = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
print(np.percentile(entregas, [25, 50, 75]))
serie = pd.Series(entregas)
print(serie.quantile([0.25, 0.5, 0.75]).tolist())
```

```salida
[15.75 21.   27.25]
[15.75, 21.0, 27.25]
```

Los dos dan 15,75; 21 y 27,25, igual que lo calculado a mano. (NumPy usa porcentajes 0–100; Pandas, fracciones 0–1.)

**4. Aplicar la regla y marcar atípicos.**

```python
import pandas as pd

serie = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
q1 = serie.quantile(0.25)
q3 = serie.quantile(0.75)
iqr = q3 - q1
inferior = q1 - 1.5 * iqr
superior = q3 + 1.5 * iqr
print(q1, q3, iqr, inferior, superior)
print(serie[(serie < inferior) | (serie > superior)].tolist())
```

```salida
15.75 27.25 11.5 -1.5 44.5
[55]
```

La condición `(serie < inferior) | (serie > superior)` usa `|` («o») entre paréntesis, que es la forma de combinar condiciones en Pandas (en lugar de `or`). El resultado `[55]` confirma el cálculo a mano.

**5. Cuidado: no hay un solo método de percentil.** Hay varias definiciones y las herramientas no siempre usan la misma:

```python
import statistics

entregas = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
print(statistics.quantiles(entregas, n=4))
print(statistics.quantiles(entregas, n=4, method="inclusive"))
```

```salida
[15.0, 21.0, 28.5]
[15.75, 21.0, 27.25]
```

El módulo `statistics` usa por defecto el método `exclusive`: Q1 = 15,0 y Q3 = 28,5, **distintos** de los 15,75 y 27,25 de NumPy/Pandas. Con `method="inclusive"` coincide con NumPy. Ninguno es «el correcto»: son definiciones diferentes. Lo importante es **escribir qué método usaste**, porque con datos reales los umbrales de atípicos (y por tanto la cantidad de atípicos) cambian con el método. En Excel, `PERCENTIL.INC` equivale a NumPy y `PERCENTIL.EXC` al método exclusivo.

**6. Percentil de un dato (posición relativa).** ¿Qué porcentaje de repartidores entregó menos de 22?

```python
import pandas as pd

serie = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
print((serie < 22).sum())
print((serie < 22).mean() * 100)
```

```salida
5
50.0
```

5 de 10 están por debajo de 22: el repartidor con 22 está aproximadamente en el percentil 50. `(serie < 22)` crea una serie de verdaderos/falsos; `.sum()` cuenta los verdaderos y `.mean()` da su proporción (lección 7.6).

**7. ¿Qué hacer con un atípico?** El error más peligroso es **borrarlo automáticamente**. El procedimiento sano:

1. **Detectarlo** con una regla objetiva (Tukey) y anotar cuántos son.
2. **Investigar su origen**: ¿error de digitación (550 en vez de 55)? ¿registro duplicado? ¿caso real (un pedido mayorista)?
3. **Decidir y documentar**: corregir si era un error comprobado; conservar si es real; analizar el resultado **con y sin** el atípico y reportar ambos.
4. **Elegir medidas robustas** (mediana, IQR) cuando los atípicos son parte de la realidad del negocio.

Con y sin el 55: media 24,0 frente a 20,56; mediana 21 frente a 20. El atípico cambia mucho la media y poco la mediana.

Ejemplo comercial: en una lista de ventas por tienda, las que superan la cerca superior son candidatas a «cuentas clave» (merecen atención especial), no a ser eliminadas.

## Errores comunes

- **Eliminar atípicos sin investigarlos.**
- **Calcular percentiles sin ordenar** (a mano) o sin decir el método.
- **Confundir percentil con porcentaje**: el percentil 90 es un valor, no un 90 %.
- **Comparar cuartiles de herramientas distintas** sin revisar el método.
- **Usar `or` en lugar de `|`** al combinar condiciones en Pandas.
- **Creer que la regla de Tukey identifica «errores»**: identifica valores inusuales.
- **Aplicar la regla con muy pocos datos** (n pequeño): los cuartiles son inestables.

## Para comprobar que entendiste

1. ¿Qué porcentaje de datos queda por debajo de Q3?
2. Si Q1 = 10 y Q3 = 30, ¿cuáles son las cercas de Tukey?
3. ¿Por qué `statistics.quantiles` y `np.percentile` pueden dar resultados distintos?
4. ¿Qué haces cuando encuentras un valor atípico?

<details><summary>Respuestas</summary>

1. Aproximadamente el 75 %.
2. IQR = 20; cerca inferior = 10 − 30 = −20; cerca superior = 30 + 30 = 60.
3. Porque usan definiciones distintas de percentil (`exclusive` frente a interpolación lineal).
4. Lo investigo, decido si es error o caso real, documento y, si es real, analizo con y sin él.

</details>

## Micropráctica

Con las ventas por tienda (en Bs) `[180, 210, 225, 240, 260, 275, 300, 320, 350, 900]` (n = 10):

1. Calcula **a mano** Q1, mediana y Q3 con el método lineal (`1 + (n − 1) × P/100`), el IQR y las cercas.
2. ¿Cuántos atípicos hay y cuál es su valor?
3. Verifica con Pandas.
4. Redacta una frase para el gerente que explique el resultado sin usar la palabra «percentil».

Cómo saber que está bien: Q1 = 228,75; mediana = 267,5; Q3 = 315; el atípico es 900.

<details><summary>Comprobación</summary>

```python
import pandas as pd

ventas = pd.Series([180, 210, 225, 240, 260, 275, 300, 320, 350, 900])
q1, mediana, q3 = ventas.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1
print(q1, mediana, q3, iqr)
print(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
print(ventas[(ventas < q1 - 1.5 * iqr) | (ventas > q3 + 1.5 * iqr)].tolist())
```

```salida
228.75 267.5 315.0 86.25
99.375 444.375
[900]
```

</details>

## Después, en los ejercicios

ST02 y ST03 de [Estadística](../../03_EJERCICIOS/Estadistica/) usan cuartiles, IQR y atípicos sobre datos reales. Escribe en tu respuesta qué método de percentil usaste y qué decidiste hacer con los atípicos. Siguiente: [11.6 Distribuciones, histogramas y puntaje z](06_distribuciones_histograma_z.md).
