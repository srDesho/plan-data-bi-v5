# 12.6 Relación entre dos categorías: la prueba chi-cuadrado

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [11.2 Frecuencias](../11_Estadistica_descriptiva/02_frecuencias.md) y [12.4 El p-valor](04_pvalor.md).

## Para qué sirve

La prueba `t` compara **promedios** de una variable numérica. Pero muchas preguntas son sobre **categorías**: ¿la proporción de clientes que hacen pedido es distinta cuando se les llama antes de visitarlos? ¿el estado de la entrega depende de la ruta? La prueba chi-cuadrado (`χ²`) compara las frecuencias observadas en una tabla de categorías contra las que se esperarían si las dos variables **no tuvieran relación**.

## Términos nuevos

- **Tabla de contingencia** (o *tabla cruzada*): una tabla de conteos que cruza dos variables categóricas: filas = una variable, columnas = la otra.
- **Frecuencia observada (`O`)**: el conteo real de cada celda.
- **Independencia**: dos variables son independientes si saber el valor de una no cambia la proporción esperada de la otra.
- **Frecuencia esperada (`E`)**: el conteo que habría en una celda si las variables fueran independientes: `E = (total de la fila × total de la columna) / total general`.
- **Estadístico chi-cuadrado (`χ²`)**: `Σ (O − E)² / E`, la suma sobre todas las celdas. Mide la distancia entre lo observado y lo esperado bajo independencia.
- **Grados de libertad**: `(filas − 1) × (columnas − 1)`. Una tabla 2×2 tiene 1.
- **Corrección de continuidad (de Yates)**: un ajuste que reduce un poco `χ²` en tablas 2×2; SciPy lo aplica por defecto.
- **Cramér V**: una medida del tamaño de la asociación entre 0 (nada) y 1 (total); se ve en 12.7.

## Ejemplo paso a paso

**El caso:** se prueba si llamar por teléfono antes de visitar a una tienda aumenta la probabilidad de que se tome un pedido. Se hicieron 100 visitas: 50 con llamada previa y 50 sin ella. Resultado:

| | Pedido tomado | Sin pedido | **Total** |
|---|---|---|---|
| **Con llamada previa** | 30 | 20 | **50** |
| **Sin llamada previa** | 18 | 32 | **50** |
| **Total** | **48** | **52** | **100** |

`H0`: tomar pedido es independiente de la llamada previa. `H1`: hay asociación. `α = 0,05`.

**1. Lo observado en porcentajes.** Con llamada: 30/50 = 60 % tomó pedido. Sin llamada: 18/50 = 36 %. Una diferencia de 24 puntos porcentuales. ¿Puede ser azar?

**2. Frecuencias esperadas bajo `H0`.** Si no hubiera relación, el 48 % de las visitas (48 de 100) terminaría en pedido, con o sin llamada:

- Celda (con llamada, pedido): `50 × 48 / 100 = 24`
- Celda (con llamada, sin pedido): `50 × 52 / 100 = 26`
- Celda (sin llamada, pedido): `50 × 48 / 100 = 24`
- Celda (sin llamada, sin pedido): `50 × 52 / 100 = 26`

Control: los esperados mantienen los mismos totales de fila y columna que los observados.

**3. El estadístico.** Se suma `(O − E)² / E` por celda:

| Celda | `O` | `E` | `(O − E)²` | `(O − E)² / E` |
|---|---|---|---|---|
| con llamada, pedido | 30 | 24 | 36 | 1,5000 |
| con llamada, sin pedido | 20 | 26 | 36 | 1,3846 |
| sin llamada, pedido | 18 | 24 | 36 | 1,5000 |
| sin llamada, sin pedido | 32 | 26 | 36 | 1,3846 |
| **Suma** | | | | **5,7692** |

`χ² = 5,769` con `(2 − 1) × (2 − 1) = 1` grado de libertad. El valor crítico de `χ²` al 5 % con 1 grado de libertad es **3,841**. Como 5,769 > 3,841, rechazamos `H0` (equivale a p < 0,05).

**4. El p-valor con SciPy.**

```python
import numpy as np
from scipy import stats

observado = np.array([[30, 20], [18, 32]])
resultado = stats.chi2_contingency(observado, correction=False)

print(round(resultado.statistic, 3))
print(resultado.dof)
print(round(resultado.pvalue, 4))
print(resultado.expected_freq)
```

```salida
5.769
1
0.0163
[[24. 26.]
 [24. 26.]]
```

`correction=False` desactiva la corrección de Yates para que el resultado coincida con el cálculo a mano: `χ² = 5,769`, 1 grado de libertad, **p = 0,0163**, y las frecuencias esperadas 24 y 26 que calculamos. Con `α = 0,05`, se rechaza `H0`.

**5. Con la corrección que SciPy aplica por defecto.**

```python
import numpy as np
from scipy import stats

observado = np.array([[30, 20], [18, 32]])
resultado = stats.chi2_contingency(observado)

print(round(resultado.statistic, 3))
print(round(resultado.pvalue, 4))
```

```salida
4.848
0.0277
```

Con la corrección de Yates el estadístico baja a 4,848 y el p-valor sube a 0,0277: ambas versiones rechazan `H0`, pero los números difieren. **Anota cuál usaste.** (La corrección es más prudente en tablas pequeñas.) Si comparas con otra herramienta (Excel, `R`), revisa su opción por defecto.

**6. Condiciones de uso.**

1. Los datos son **conteos** (no porcentajes).
2. Cada observación aparece en **una sola celda** y es independiente de las demás (no es la misma tienda medida varias veces).
3. Las frecuencias **esperadas** son suficientemente grandes: la regla práctica pide al menos 5 en cada celda. Si no, usa otra prueba (la exacta de Fisher) o junta categorías.
4. Las unidades se asignaron o muestrearon al azar para poder generalizar.

**7. Interpretar con cuidado.** El resultado dice que hay **asociación** estadísticamente detectable entre la llamada previa y la toma de pedido. No dice cuánta ni por qué:

- ¿Las visitas con llamada se hicieron a tiendas más grandes? ¿las llamó solo el vendedor más experimentado? Si la llamada no se asignó al azar, puede haber confusores.
- El tamaño de la asociación se mide aparte (12.7): aquí, 24 puntos porcentuales de diferencia y una V de Cramér de 0,24 (asociación pequeña a moderada).

**8. Tablas más grandes.** Con más categorías, `pd.crosstab` construye la tabla desde datos de filas:

```python
import pandas as pd

visitas = pd.read_csv("04_DATASETS/mini_base/visitas.csv")
tabla = pd.crosstab(visitas["realizada"], visitas["pedido_tomado"])
print(tabla)
```

```salida
pedido_tomado  0  1
realizada          
0              3  0
1              4  7
```

Esta tabla cruza «visita realizada» con «pedido tomado» en las 14 visitas de la mini-base. Observa que algunas celdas tienen conteos mínimos: con 14 datos y celdas pequeñas la condición de frecuencias esperadas ≥ 5 **no se cumple**, así que chi-cuadrado no sería apropiada aquí. Saber cuándo **no** aplicar una prueba es parte de usarla bien.

Ejemplo comercial: «¿el tipo de tienda (kiosco, farmacia...) está relacionado con aceptar un nuevo producto?». Cruzas tipo × aceptó/no, calculas los esperados, verificas que sean ≥ 5, y reportas `χ²`, grados de libertad, p-valor y V de Cramér.

## Errores comunes

- **Aplicar chi-cuadrado a porcentajes o a promedios** en lugar de conteos.
- **No revisar las frecuencias esperadas** (< 5).
- **Usar la misma unidad varias veces** (observaciones repetidas).
- **Confundir asociación con causa.**
- **No indicar si se usó la corrección de Yates.**
- **Concluir que un p-valor pequeño implica una asociación fuerte.**
- **Comparar cuando los grupos se formaron a dedo.**

## Para comprobar que entendiste

1. ¿Cómo se calcula la frecuencia esperada de una celda?
2. ¿Cuántos grados de libertad tiene una tabla de 3 filas por 4 columnas?
3. ¿Qué condición revisas en las frecuencias esperadas?
4. Si `χ² = 2,1` con 1 grado de libertad (valor crítico 3,841), ¿qué decides?

<details><summary>Respuestas</summary>

1. (Total de la fila × total de la columna) / total general.
2. (3 − 1) × (4 − 1) = 6.
3. Que sean al menos 5 (regla práctica).
4. No rechazo `H0`: 2,1 < 3,841.

</details>

## Micropráctica

Se compararon dos formas de entrega y si el cliente quedó conforme: reparto A: 40 conformes y 10 no conformes; reparto B: 30 conformes y 20 no conformes.

1. Arma la tabla con totales y calcula los porcentajes de conformes de cada reparto.
2. Calcula a mano las frecuencias esperadas, el `χ²` y compáralo con 3,841.
3. Verifica con SciPy (`correction=False`) y escribe la conclusión con una limitación.

Cómo saber que está bien: los esperados son 35, 15, 35 y 15; `χ²` ≈ 4,762 y p ≈ 0,029.

<details><summary>Comprobación de la parte 3</summary>

```python
import numpy as np
from scipy import stats

observado = np.array([[40, 10], [30, 20]])
r = stats.chi2_contingency(observado, correction=False)
print(round(r.statistic, 3), r.dof, round(r.pvalue, 4))
print(r.expected_freq)
```

```salida
4.762 1 0.0291
[[35. 15.]
 [35. 15.]]
```

</details>

## Después, en los ejercicios

ST07 y el caso C03 de [Estadística](../../03_EJERCICIOS/Estadistica/) usan tablas de contingencia. Verifica siempre las frecuencias esperadas antes de aplicar la prueba. Siguiente: [12.7 Tamaño del efecto](07_tamano_del_efecto.md).
