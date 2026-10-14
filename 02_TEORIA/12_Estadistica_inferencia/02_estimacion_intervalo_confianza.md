# 12.2 Estimación e intervalos de confianza

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisito: [12.1 Variabilidad entre muestras](01_por_que_inferencia.md).

## Para qué sirve

Decir «el ticket promedio es 114» es incompleto. Es más útil decir «el ticket promedio está probablemente entre 106 y 122». Un **intervalo de confianza** convierte una estimación en un rango razonable de valores para el parámetro poblacional, y su ancho te dice qué tan precisa es la estimación. Con él puedes responder: ¿vale la pena decidir con esta muestra o necesito más datos?

## Términos nuevos

- **Intervalo de confianza**: un rango de valores calculado con una muestra, construido con un método que, si se repitiera muchas veces, contendría al parámetro verdadero en un porcentaje fijo de los casos (el nivel de confianza).
- **Nivel de confianza**: ese porcentaje a largo plazo (habitualmente 95 %).
- **Margen de error**: la mitad del ancho del intervalo: lo que se suma y se resta a la estimación puntual.
- **Distribución `t` de Student**: una distribución parecida a la campana normal pero con colas más pesadas; se usa para la media cuando la desviación de la población se desconoce y se estima con `s`. Su forma depende de los **grados de libertad** (`n − 1`).
- **Valor crítico `t*`**: el número que se multiplica por el error estándar para obtener el margen de error. Para 95 % y 11 grados de libertad vale 2,201.
- **Intervalo para una media**: `x̄ ± t* × (s / √n)`.

## Ejemplo paso a paso

Datos (inventados): tickets de 12 ventas escogidas al azar, en Bs: `112, 98, 130, 105, 120, 99, 140, 115, 108, 125, 101, 117`. Queremos estimar el ticket promedio de **todas** las ventas.

**1. Estimación puntual.** `x̄ = 1370 / 12 = 114,17` Bs. Es nuestra mejor estimación, pero sabemos (lección 12.1) que otra muestra daría otro valor.

**2. Dispersión de la muestra.** Las desviaciones al cuadrado respecto a 114,17 suman 1869,67; entonces:

- `s² = 1869,67 / (12 − 1) = 169,97`
- `s = √169,97 = 13,04`

**3. Error estándar.** `s / √n = 13,04 / √12 = 13,04 / 3,464 = 3,76`.

**4. Valor crítico.** Para un nivel de confianza del 95 % y `n − 1 = 11` grados de libertad, el valor crítico de la distribución `t` es **2,201** (se lee en una tabla `t`, o se obtiene con una función; lo verificaremos abajo).

**5. Margen de error e intervalo.**

- Margen de error: `2,201 × 3,76 = 8,28`.
- Intervalo: `114,17 ± 8,28` → **de 105,88 a 122,45** Bs.

**6. Verificar con Python** (y obtener `t*` con SciPy):

```python
import math
import statistics
from scipy import stats

tickets = [112, 98, 130, 105, 120, 99, 140, 115, 108, 125, 101, 117]
n = len(tickets)
media = statistics.mean(tickets)
s = statistics.stdev(tickets)
error_estandar = s / math.sqrt(n)
t_critico = stats.t.ppf(0.975, df=n - 1)
margen = t_critico * error_estandar

print(round(media, 2), round(s, 2), round(error_estandar, 2))
print(round(t_critico, 3), round(margen, 2))
print(round(media - margen, 2), round(media + margen, 2))
```

```salida
114.17 13.04 3.76
2.201 8.28
105.88 122.45
```

`stats.t.ppf(0.975, df=11)` devuelve el valor de `t` que deja el 97,5 % del área por debajo: así el intervalo del 95 % deja 2,5 % en cada cola. El resultado coincide con el cálculo a mano.

**7. Cómo se interpreta correctamente.** «Con una confianza del 95 %, el ticket promedio de la población está entre Bs 105,9 y Bs 122,5.» Lo que significa el 95 %: **si repitiéramos todo el procedimiento muchas veces** (sacar una muestra, calcular el intervalo), aproximadamente el 95 % de los intervalos construidos contendría la media verdadera. **No** significa «hay 95 % de probabilidad de que la media esté en este intervalo concreto»: la media verdadera es un número fijo; el intervalo es el que varía. Esta sutileza se entiende mejor con una simulación.

**8. Comprobar la cobertura con una simulación.** Usamos la población artificial de 12.1 (media verdadera 64,46). Construimos 1 000 intervalos de 95 % con muestras de 12 y contamos cuántos contienen a la media verdadera:

```python
import math
import random
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
mu = statistics.mean(poblacion)
azar = random.Random(11)
t_critico = 2.201

contienen = 0
for _ in range(1000):
    muestra = azar.sample(poblacion, 12)
    media = statistics.mean(muestra)
    margen = t_critico * statistics.stdev(muestra) / math.sqrt(12)
    if media - margen <= mu <= media + margen:
        contienen = contienen + 1

print(contienen, "de 1000")
```

```salida
943 de 1000
```

De los 1 000 intervalos, **943** contienen a la media verdadera: cerca del 95 % prometido (en una simulación finita nunca es exactamente 950; además la población artificial es plana y no normal). Los otros 57 fallaron: son la parte inevitable de la incertidumbre.

**9. Qué determina el ancho del intervalo.**

| Si... | el intervalo... | porque |
|---|---|---|
| aumenta `n` | se estrecha | el error estándar `s/√n` baja |
| aumenta la dispersión `s` | se ensancha | hay más variabilidad en los datos |
| aumentas el nivel de confianza (99 % en vez de 95 %) | se ensancha | pides más seguridad, aceptas menos precisión |

Con la misma muestra, el intervalo de 99 % es más ancho que el de 95 %. No existe un intervalo muy estrecho y muy seguro al mismo tiempo sin más datos.

**10. Intervalo para una proporción.** Si 36 de 60 clientes encuestados dicen estar satisfechos, la proporción muestral es `p̂ = 36/60 = 0,60`. Un intervalo aproximado del 95 % es `p̂ ± 1,96 × √(p̂(1 − p̂)/n)`:

```python
import math

n = 60
exitos = 36
p = exitos / n
error = math.sqrt(p * (1 - p) / n)
print(round(p, 2), round(1.96 * error, 3))
print(round(p - 1.96 * error, 3), round(p + 1.96 * error, 3))
```

```salida
0.6 0.124
0.476 0.724
```

El 60 % observado tiene un margen de error de aproximadamente ±12,4 puntos: el verdadero porcentaje de satisfechos estaría entre 47,6 % y 72,4 %. Con solo 60 encuestas no se puede afirmar que «más de la mitad» está satisfecha con seguridad, porque el límite inferior queda por debajo del 50 %. Esta fórmula aproximada requiere que haya suficientes éxitos y fracasos (al menos unos 10 de cada uno).

Ejemplo comercial: «el tiempo de entrega medio es de 38 minutos, con un intervalo de confianza del 95 % de 33 a 43» es una frase honesta. Si el contrato exige «menos de 35 minutos», el intervalo muestra que **no es seguro** que se cumpla.

## Errores comunes

- **Interpretar el 95 % como probabilidad del intervalo concreto.**
- **Reportar solo la media** sin su intervalo.
- **Usar 1,96 (normal) con muestras muy pequeñas**: para `n` pequeño se usa `t*`, que es mayor.
- **Calcular el intervalo con datos no aleatorios** (muestra sesgada): el intervalo es matemáticamente correcto pero engañoso.
- **Creer que un intervalo estrecho prueba que no hay sesgo.**
- **Mezclar la desviación estándar con el error estándar** al calcular el margen.
- **Aplicar la fórmula de proporciones con muy pocos casos.**

## Para comprobar que entendiste

1. ¿Qué indica el ancho de un intervalo?
2. Si `x̄ = 50`, `s = 10`, `n = 25` y `t* = 2,064`, ¿cuál es el intervalo del 95 %?
3. ¿Por qué un intervalo del 99 % es más ancho que uno del 95 %?
4. ¿Qué significa «nivel de confianza del 95 %»?

<details><summary>Respuestas</summary>

1. La precisión de la estimación: más ancho, más incertidumbre.
2. Error estándar = 10/5 = 2; margen = 2,064 × 2 = 4,128; intervalo: de 45,87 a 54,13.
3. Porque pide más seguridad de contener al parámetro, y eso exige un rango mayor.
4. Que el método, repetido muchas veces con muestras distintas, contiene al parámetro verdadero en cerca del 95 % de las veces.

</details>

## Micropráctica

Con los tiempos de entrega (en minutos) `[34, 28, 31, 29, 33, 30, 28, 36, 32, 27]` (n = 10; valor crítico `t*` = 2,262 para 9 grados de libertad):

1. Calcula **a mano** la media, `s`, el error estándar, el margen de error y el intervalo del 95 %.
2. Verifica con Python (obtén `t*` con SciPy).
3. Si el contrato exige un promedio de 30 minutos o menos, ¿qué dices a partir del intervalo?

Cómo saber que está bien: la media es 30,8 y el intervalo queda aproximadamente entre 28,7 y 32,9.

<details><summary>Comprobación de la parte 2</summary>

```python
import math
import statistics
from scipy import stats

tiempos = [34, 28, 31, 29, 33, 30, 28, 36, 32, 27]
n = len(tiempos)
media = statistics.mean(tiempos)
ee = statistics.stdev(tiempos) / math.sqrt(n)
t = stats.t.ppf(0.975, df=n - 1)
print(round(media, 2), round(ee, 3), round(t, 3))
print(round(media - t * ee, 2), round(media + t * ee, 2))
```

```salida
30.8 0.929 2.262
28.7 32.9
```

</details>

## Después, en los ejercicios

Los intervalos se usan en ST05–ST07 de [Estadística](../../03_EJERCICIOS/Estadistica/) para acompañar las comparaciones. Siguiente: [12.3 Hipótesis nula y alternativa](03_hipotesis.md).
