# 11.6 Distribuciones, histogramas, normalidad y puntaje z

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisitos: [11.2 Frecuencias](02_frecuencias.md), [11.4 Dispersión](04_dispersion.md) y [11.5 Percentiles](05_percentiles_atipicos.md).

## Para qué sirve

Los resúmenes (media, desviación) esconden la **forma** de los datos: dónde se concentran, si son simétricos, si hay una cola larga. La forma decide qué medida usar y qué pruebas estadísticas son válidas más adelante. Un histograma la muestra de un vistazo, y el puntaje z permite comparar valores de variables distintas en una escala común.

## Términos nuevos

- **Distribución**: cómo se reparten los valores de una variable (cuántos hay en cada zona de valores).
- **Histograma**: un gráfico de barras pegadas donde cada barra representa un intervalo de valores y su altura es la frecuencia.
- **Distribución simétrica**: la parte izquierda es un reflejo de la derecha. En ella media ≈ mediana.
- **Asimetría positiva** (o «sesgo a la derecha»): hay una cola larga hacia los valores altos. Media > mediana. Es lo habitual en ventas, ingresos y tiempos.
- **Asimetría negativa**: cola larga hacia los valores bajos. Media < mediana.
- **Distribución normal**: la «campana» simétrica descrita por su media y su desviación estándar.
- **Regla empírica (68-95-99,7)**: en una distribución aproximadamente normal, cerca del 68 % de los datos queda a menos de 1 desviación de la media, el 95 % a menos de 2 y el 99,7 % a menos de 3.
- **Puntaje z**: cuántas desviaciones estándar se aleja un dato de la media: `z = (x − x̄) / s`. Positivo = por encima; negativo = por debajo.
- **Coeficiente de asimetría**: un número que resume el sesgo (cero = simétrica, positivo = cola derecha).

## Ejemplo paso a paso

Datos: las mismas 10 entregas `12, 15, 15, 18, 20, 22, 25, 28, 30, 55` (media 24; s = 12,36).

**1. Histograma a mano.** Agrupamos en intervalos de ancho 10 que incluyen el límite derecho:

| Intervalo | Datos | Frecuencia |
|---|---|---|
| (10, 20] | 12, 15, 15, 18, 20 | 5 |
| (20, 30] | 22, 25, 28, 30 | 4 |
| (30, 40] | — | 0 |
| (40, 50] | — | 0 |
| (50, 60] | 55 | 1 |
| **Total** | | **10** |

Dibujado con asteriscos se ve la forma:

```python
import pandas as pd

entregas = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
tramos = pd.cut(entregas, bins=[10, 20, 30, 40, 50, 60])
for intervalo, frecuencia in tramos.value_counts(sort=False).items():
    print(f"{str(intervalo):10} {'*' * frecuencia}")
```

```salida
(10, 20]   *****
(20, 30]   ****
(30, 40]   
(40, 50]   
(50, 60]   *
```

La mayoría de los datos está a la izquierda (entre 10 y 30) y hay una barra solitaria en 50-60: una **cola larga a la derecha**, es decir, asimetría positiva. La media (24) es mayor que la mediana (21), consistente con esa cola.

**2. Dibujar un histograma real con Matplotlib.** El mismo gráfico, con título y ejes:

```python
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

entregas = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
plt.hist(entregas, bins=[10, 20, 30, 40, 50, 60], edgecolor="black")
plt.title("Entregas por repartidor en un día")
plt.xlabel("Entregas")
plt.ylabel("Cantidad de repartidores")
plt.savefig("hist_entregas.png")
print(Path("hist_entregas.png").exists())
```

```salida
True
```

`matplotlib.use("Agg")` hace que no se abra una ventana (en tu equipo, sin esa línea y con `plt.show()`, verías el gráfico). Aquí se guarda en un archivo. Un buen gráfico tiene un **título que dice qué se ve**, ejes con etiqueta y unidades, y el rango de datos.

**3. La forma decide la medida.**

| Forma | Media vs mediana | Medida a reportar |
|---|---|---|
| Simétrica | media ≈ mediana | media y desviación estándar |
| Cola derecha | media > mediana | mediana y IQR (y también la media si se necesita el total) |
| Cola izquierda | media < mediana | mediana y IQR |

**4. Puntaje z a mano.** ¿Qué tan extremo es el repartidor con 55 entregas y el de 12?

- `z(55) = (55 − 24) / 12,36 = 31 / 12,36 = 2,51`
- `z(12) = (12 − 24) / 12,36 = −12 / 12,36 = −0,97`

El primero está **2,51 desviaciones por encima** de la media; el segundo, 0,97 por debajo. Como regla práctica (orientativa), |z| > 3 es muy inusual en datos normales, y |z| entre 2 y 3 merece mirarse. Con Pandas:

```python
import pandas as pd

serie = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
z = (serie - serie.mean()) / serie.std()
print(z.round(2).tolist())
```

```salida
[-0.97, -0.73, -0.73, -0.49, -0.32, -0.16, 0.08, 0.32, 0.49, 2.51]
```

Se usa `serie.std()` (muestral, `n − 1`), igual que en la mano. Si usaras la desviación poblacional, los z cambiarían ligeramente.

**5. Comparar valores en escalas distintas.** Un vendedor vendió Bs 480 cuando el promedio del equipo es 400 con desviación 50 (z = 1,6); otro vendió 36 unidades cuando el promedio es 30 con desviación 5 (z = 1,2). Aunque las unidades son distintas, el primero está más arriba **respecto a su grupo**. Esa es la utilidad del z: comparar «en desviaciones» en vez de en unidades.

**6. La regla 68-95-99,7 (solo si la forma es de campana).** Si las entregas fueran aproximadamente normales con media 24 y s = 12,36, el 68 % estaría entre 11,6 y 36,4 y el 95 % entre −0,7 y 48,7. Compruébalo con estos datos:

```python
import pandas as pd

serie = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
media, s = serie.mean(), serie.std()
dentro_1 = ((serie > media - s) & (serie < media + s)).mean() * 100
dentro_2 = ((serie > media - 2 * s) & (serie < media + 2 * s)).mean() * 100
print(round(dentro_1), round(dentro_2))
```

```salida
90 90
```

El 90 % de los datos cae a menos de una desviación de la media (la regla diría 68 %) y también el 90 % a menos de dos (la regla diría 95 %). Con 10 datos y una cola larga, la regla **no describe esta distribución**. Solo es aplicable a distribuciones aproximadamente normales.

**7. ¿Los datos son «normales»?** Una revisión informal, antes de usar métodos que lo supongan (capítulo 12):

1. **Histograma**: ¿forma de campana, sin cola marcada?
2. **Media vs mediana**: ¿casi iguales?
3. **Coeficiente de asimetría**: ¿cercano a 0?
4. **Cantidad de datos**: con pocos datos es difícil afirmar nada.

```python
import pandas as pd

serie = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
print(round(serie.skew(), 2))
```

```salida
1.95
```

Un valor positivo y grande (aquí 1,95) indica cola derecha. Hay pruebas formales de normalidad, pero con pocos datos tienen poco poder y con muchos detectan desviaciones irrelevantes; para este curso basta la revisión gráfica y numérica, y **escribir tu conclusión**.

Ejemplo comercial: la distribución de los tickets de venta casi siempre tiene cola derecha (muchas ventas pequeñas, pocas grandes). Por eso el «ticket mediano» describe mejor a la venta típica, y el «ticket medio» sirve para proyectar el total.

## Errores comunes

- **Hacer un histograma con demasiados o muy pocos intervalos** y ver una forma falsa.
- **Elegir intervalos sin decir si incluyen el límite derecho.**
- **Aplicar la regla 68-95-99,7 a datos que no son simétricos.**
- **Interpretar un z como porcentaje** (z = 2 no es 2 %).
- **Creer que z grande significa error**: significa distancia, no equivocación.
- **Gráficos sin título, sin unidades o con el eje truncado** que exagera diferencias.
- **Decidir la normalidad con 8 datos.**

## Para comprobar que entendiste

1. ¿Qué forma tiene una distribución con media mayor que la mediana?
2. Si `x̄ = 50`, `s = 10` y un dato vale 70, ¿cuánto es su z y qué significa?
3. ¿Por qué no se aplica la regla 68-95-99,7 a las entregas?
4. ¿Qué debe tener un buen gráfico además de las barras?

<details><summary>Respuestas</summary>

1. Asimetría positiva (cola larga hacia la derecha).
2. z = (70 − 50)/10 = 2: está 2 desviaciones por encima de la media.
3. Porque la distribución no es simétrica ni tiene forma de campana.
4. Título que describa qué se ve, ejes con etiquetas y unidades.

</details>

<a id="micropractica"></a>

## Micropráctica

Con los tiempos de entrega `[34, 28, 31, 29, 33, 30, 28, 95]` de la lección 11.3:

1. Arma a mano la tabla de frecuencias en intervalos de ancho 20 que empiecen en 20 y calcula la frecuencia de cada uno.
2. Calcula el z del valor 95 y el del valor 28.
3. Decide si la distribución es simétrica y qué medida reportarías.
4. Dibuja el histograma con Matplotlib y escribe un título que describa el hallazgo.

Cómo saber que está bien: (20, 40] contiene 7 valores y (80, 100] uno; el z del 95 es mayor que 2.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import pandas as pd

tiempos = pd.Series([34, 28, 31, 29, 33, 30, 28, 95])
print(pd.cut(tiempos, bins=[20, 40, 60, 80, 100]).value_counts(sort=False).tolist())
z = (tiempos - tiempos.mean()) / tiempos.std()
print(round(z.iloc[7], 2), round(z.iloc[1], 2))
```

```salida
[7, 0, 0, 1]
2.46 -0.46
```

</details>

## Después, en los ejercicios

El gráfico de ST03 y del caso C03 en [Estadística](../../03_EJERCICIOS/Estadistica/) debe tener título descriptivo, unidades y una recomendación. Siguiente: [11.7 Correlación y causalidad](07_correlacion_causalidad.md).
