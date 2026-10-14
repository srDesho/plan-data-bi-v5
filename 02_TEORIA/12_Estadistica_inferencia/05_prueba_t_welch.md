# 12.5 Comparar dos promedios: la prueba t (Student y Welch)

> Tiempo estimado: 70 min (lectura 30 + práctica 40). Prerrequisitos: [11.4 Dispersión](../11_Estadistica_descriptiva/04_dispersion.md), [12.2 Intervalos](02_estimacion_intervalo_confianza.md) y [12.4 El p-valor](04_pvalor.md).

## Para qué sirve

La pregunta más frecuente en un piloto comercial es: **¿este grupo tiene un promedio distinto de aquel?** (tiendas con visita extra frente a tiendas sin ella, ruta A frente a ruta B, antes frente a después). Con muestras grandes y sin extremos extremos, la prueba `t` responde si la diferencia observada se explica razonablemente por el azar. Aquí la calculas a mano y luego con SciPy, y aprendes cuándo usar la variante de Welch.

## Términos nuevos

- **Prueba `t` para dos grupos independientes**: compara las medias de dos grupos formados por unidades distintas (no las mismas tiendas medidas dos veces).
- **Estadístico `t`**: la diferencia de medias dividida entre su error estándar: `t = (x̄A − x̄B) / √(sA²/nA + sB²/nB)`. Mide «cuántos errores estándar» se separan los promedios.
- **Prueba de Welch**: la versión que **no supone** que los dos grupos tengan la misma varianza. Es la opción recomendada por defecto.
- **Prueba `t` de Student (varianzas iguales)**: la versión clásica que combina las dos varianzas en una sola; solo es adecuada si hay buenas razones para suponerlas iguales.
- **Grados de libertad de Welch**: un número (casi nunca entero) calculado con la fórmula de Welch–Satterthwaite que ajusta la forma de la distribución `t`.
- **Muestras pareadas**: cuando cada dato de un grupo se empareja con uno del otro (la misma tienda antes y después). Requieren otra prueba (`t` pareada), no la de dos grupos independientes.
- **Supuestos**: las condiciones que la prueba necesita: datos independientes, muestras aleatorias o asignación aleatoria, y distribuciones no demasiado asimétricas (o muestras suficientemente grandes).

## Ejemplo paso a paso

Los mismos datos de la visita extra: A = `31, 27, 35, 29` y B = `24, 28, 22, 26` (pedidos por tienda). `H0`: `μA = μB`. `H1`: `μA ≠ μB`. `α = 0,05`.

**1. Resumen de cada grupo.**

| | `n` | media | desviaciones al cuadrado (suma) | varianza `s²` |
|---|---|---|---|---|
| A | 4 | 30,5 | 0,25 + 12,25 + 20,25 + 2,25 = 35 | 35 / 3 = 11,667 |
| B | 4 | 25,0 | 1 + 9 + 9 + 1 = 20 | 20 / 3 = 6,667 |

**2. Error estándar de la diferencia.**

`√(sA²/nA + sB²/nB) = √(11,667/4 + 6,667/4) = √(2,9167 + 1,6667) = √4,5833 = 2,141`

**3. Estadístico `t`.**

`t = (30,5 − 25,0) / 2,141 = 5,5 / 2,141 = 2,569`

La diferencia observada está a unos 2,57 errores estándar de cero. Cuanto más lejos de 0 esté `t`, menos compatible es la diferencia con `H0`.

**4. Grados de libertad (Welch).**

`gl = (sA²/nA + sB²/nB)² / [ (sA²/nA)²/(nA − 1) + (sB²/nB)²/(nB − 1) ]`
`= 4,5833² / [ 2,9167²/3 + 1,6667²/3 ] = 21,007 / (2,8356 + 0,9259) = 21,007 / 3,7616 = 5,58`

**5. P-valor.** Se busca, en la distribución `t` con 5,58 grados de libertad, la probabilidad de un valor tan extremo como 2,569 en cualquiera de las dos colas. Eso requiere una tabla o una función; lo obtenemos con SciPy:

```python
from scipy import stats

grupo_a = [31, 27, 35, 29]
grupo_b = [24, 28, 22, 26]
resultado = stats.ttest_ind(grupo_a, grupo_b, equal_var=False)

print(round(resultado.statistic, 3))
print(round(resultado.df, 2))
print(round(resultado.pvalue, 4))
```

```salida
2.569
5.58
0.0452
```

Coincide con el cálculo a mano: `t = 2,569`, `gl = 5,58` y **p = 0,0452**. `equal_var=False` pide la versión de Welch. Con `α = 0,05`, 0,0452 < 0,05: **se rechaza `H0`**. En 12.4 la permutación exacta dio 0,0571 y aquí 0,0452: ambos valores están pegados al umbral y la decisión cambia según el método. Mensaje honesto: *evidencia moderada de que la visita extra aumenta los pedidos, pero muy cercana al límite y con solo 4 tiendas por grupo*.

**6. Reproducir el cálculo a mano con Python** (para entender cada pieza):

```python
import math
import statistics

a = [31, 27, 35, 29]
b = [24, 28, 22, 26]

media_a, media_b = statistics.mean(a), statistics.mean(b)
va, vb = statistics.variance(a), statistics.variance(b)
na, nb = len(a), len(b)

error = math.sqrt(va / na + vb / nb)
t = (media_a - media_b) / error
gl = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))

print(round(error, 3), round(t, 3), round(gl, 2))
```

```salida
2.141 2.569 5.58
```

**7. Intervalo de confianza de la diferencia.** Además del p-valor, el intervalo dice **cuánto** puede ser la diferencia: `diferencia ± t* × error estándar`, con `t*` de 5,58 grados de libertad al 95 %:

```python
import math
import statistics
from scipy import stats

a = [31, 27, 35, 29]
b = [24, 28, 22, 26]
va, vb = statistics.variance(a), statistics.variance(b)
error = math.sqrt(va / 4 + vb / 4)
gl = (va / 4 + vb / 4) ** 2 / ((va / 4) ** 2 / 3 + (vb / 4) ** 2 / 3)
t_critico = stats.t.ppf(0.975, gl)
diferencia = statistics.mean(a) - statistics.mean(b)

print(round(diferencia - t_critico * error, 2), round(diferencia + t_critico * error, 2))
```

```salida
0.17 10.83
```

Intervalo del 95 %: de aproximadamente **0,2 a 10,8 pedidos** más por tienda. El intervalo es muy ancho: la visita extra podría aportar casi nada o casi 11 pedidos más. Esa amplitud (consecuencia de 4 tiendas por grupo) es información tan importante como el p-valor, y la saltan quienes solo miran «significativo/no».

**8. Student frente a Welch.** Con los mismos datos y el supuesto de varianzas iguales:

```python
from scipy import stats

a = [31, 27, 35, 29]
b = [24, 28, 22, 26]
print(round(stats.ttest_ind(a, b, equal_var=True).pvalue, 4))
print(round(stats.ttest_ind(a, b, equal_var=False).pvalue, 4))
```

```salida
0.0424
0.0452
```

Con tamaños iguales y varianzas parecidas las dos versiones casi coinciden. La diferencia importa cuando los tamaños o las varianzas son distintos; **Welch no pierde casi nada cuando las varianzas son iguales y protege cuando no lo son**, por eso es la opción por defecto.

**9. Los supuestos, uno por uno.**

1. **Independencia**: cada tienda aparece una sola vez y lo que ocurre en una no afecta a otra. Si midieras las mismas tiendas antes y después, usa la prueba pareada.
2. **Aleatoriedad**: las tiendas se asignaron al azar a cada grupo. Si el vendedor escogió «a dedo» las tiendas con visita extra (¡las mejores!), la prueba compara criterios de selección, no el efecto.
3. **Forma de los datos**: la prueba `t` funciona bien si los datos no son demasiado asimétricos o si hay muestras razonablemente grandes (el teorema del límite central de 12.1). Con muestras diminutas y datos con atípicos, desconfía y apóyate en una permutación o en más datos.
4. **Sin atípicos influyentes**: un solo dato extremo puede hacer o deshacer el resultado.

Ejemplo comercial: «las tiendas con exhibidor vendieron en promedio Bs 38 más». Antes de creerlo: ¿se asignó el exhibidor al azar o se puso en las tiendas más grandes? ¿cuántas tiendas? ¿cuál es el intervalo de la diferencia?

## Errores comunes

- **Usar la prueba para dos grupos independientes con datos pareados.**
- **Usar Student sin justificar la igualdad de varianzas.**
- **Aplicar la prueba con pocos datos y atípicos fuertes sin revisarlos.**
- **Interpretar p < 0,05 como «el efecto es grande o importante».**
- **Reportar solo el p-valor** sin la diferencia de medias, el intervalo y los tamaños de grupo.
- **Comparar muchos grupos de a pares sin corregir** (12.8).
- **Olvidar que la asignación no aleatoria impide hablar de causa.**

## Para comprobar que entendiste

1. ¿Qué mide el estadístico `t`?
2. ¿Por qué se prefiere Welch a Student por defecto?
3. ¿Qué prueba usarías para comparar las ventas de las mismas 10 tiendas antes y después?
4. ¿Qué información extra aporta el intervalo de confianza de la diferencia?

<details><summary>Respuestas</summary>

1. Cuántos errores estándar separan la diferencia de medias observada de cero.
2. Porque no exige varianzas iguales y casi no pierde potencia cuando lo son.
3. La `t` pareada (muestras relacionadas), no la de grupos independientes.
4. El rango plausible del tamaño de la diferencia, que muestra qué tan precisa es la estimación.

</details>

## Micropráctica

Dos rutas miden el tiempo de entrega (en minutos): R_A = `42, 38, 45, 50, 41, 47, 44, 39` y R_B = `35, 40, 33, 38, 36, 41, 34, 37`.

1. Plantea `H0`, `H1` y `α`.
2. Calcula a mano las medias y las varianzas muestrales (la media de R_A es 43,25 y la de R_B es 36,75).
3. Calcula con SciPy la prueba de Welch y el intervalo de la diferencia.
4. Redacta la conclusión en lenguaje de negocio, incluyendo el tamaño de la diferencia y una limitación.

Cómo saber que está bien: la diferencia de medias es 6,5 minutos y el p-valor es menor que 0,01.

<details><summary>Comprobación de la parte 3</summary>

```python
import math
import statistics
from scipy import stats

ra = [42, 38, 45, 50, 41, 47, 44, 39]
rb = [35, 40, 33, 38, 36, 41, 34, 37]
r = stats.ttest_ind(ra, rb, equal_var=False)
va, vb = statistics.variance(ra), statistics.variance(rb)
error = math.sqrt(va / 8 + vb / 8)
gl = r.df
tc = stats.t.ppf(0.975, gl)
dif = statistics.mean(ra) - statistics.mean(rb)

print(round(dif, 2), round(r.statistic, 3), round(gl, 2), round(r.pvalue, 4))
print(round(dif - tc * error, 2), round(dif + tc * error, 2))
```

```salida
6.5 3.72 12.47 0.0028
2.71 10.29
```

</details>

## Después, en los ejercicios

ST05 y ST06 de [Estadística](../../03_EJERCICIOS/Estadistica/) piden una comparación de dos grupos con prueba `t`. Entrega `H0`, `H1`, `α`, la prueba usada y por qué, la diferencia, el intervalo, el p-valor y la interpretación con su limitación. Siguiente: [12.6 Chi-cuadrado](06_chi_cuadrado.md).
