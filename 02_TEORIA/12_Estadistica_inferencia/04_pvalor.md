# 12.4 El p-valor, calculado de verdad

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisito: [12.3 Hipótesis nula y alternativa](03_hipotesis.md).

## Para qué sirve

El p-valor es el número más usado y peor entendido de la estadística. Casi todos los programas lo calculan con una sola instrucción, y por eso casi nadie sabe de dónde sale. Aquí lo construyes **a mano, sin fórmulas ni SciPy**, contando posibilidades en un ejemplo pequeño. Cuando lo hayas visto nacer, su definición ya no será una frase que memorizar.

## Términos nuevos

- **p-valor**: la probabilidad de obtener, **si `H0` fuera cierta**, un resultado al menos tan extremo como el que observaste. Valores pequeños indican que lo observado sería muy raro bajo `H0`.
- **Prueba de permutación**: una prueba que calcula el p-valor reasignando al azar (o en todas las formas posibles) los datos a los grupos, para ver cuántos repartos dan una diferencia tan grande como la observada.
- **Combinación**: una forma de escoger `k` elementos de `n` sin importar el orden. De 8 tiendas, hay 70 maneras de escoger 4 para el grupo A.
- **Extremo**: «al menos tan lejos de lo esperado como lo observado». En una prueba bilateral cuenta en ambos sentidos.
- **Significativo**: un resultado con p-valor ≤ `α`. Es una etiqueta estadística, no un juicio de importancia.

## Ejemplo paso a paso

Recuperamos la prueba de la visita extra de 12.3: A = `31, 27, 35, 29` y B = `24, 28, 22, 26`.

**1. El resultado observado.** Media de A = 30,5; media de B = 25,0. Diferencia observada = **5,5**.

**2. La idea central.** Supongamos que `H0` es cierta: la visita extra no hace nada. Entonces los 8 números `31, 27, 35, 29, 24, 28, 22, 26` serían simplemente 8 valores de pedidos, y el hecho de que 4 de ellos hayan quedado en el grupo A y 4 en el B sería **casualidad**. Pregunta: de todas las formas posibles de repartir esos 8 números en dos grupos de 4, ¿cuántas dan una diferencia de medias tan grande como 5,5 (en cualquier sentido)?

**3. Contar los repartos posibles.** Hay 8 valores y hay que escoger 4 para el grupo A: `C(8, 4) = 8! / (4! × 4!) = 70` repartos posibles, todos igualmente probables bajo `H0`.

**4. Calcularlos todos con Python.** El computador genera las 70 combinaciones y calcula la diferencia de medias de cada una:

```python
import itertools
import statistics

todos = [31, 27, 35, 29, 24, 28, 22, 26]
observada = statistics.mean([31, 27, 35, 29]) - statistics.mean([24, 28, 22, 26])
print("diferencia observada:", observada)

repartos = 0
tan_extremos = 0
for indices_a in itertools.combinations(range(8), 4):
    grupo_a = [todos[i] for i in indices_a]
    grupo_b = [todos[i] for i in range(8) if i not in indices_a]
    diferencia = statistics.mean(grupo_a) - statistics.mean(grupo_b)
    repartos = repartos + 1
    if abs(diferencia) >= abs(observada) - 1e-9:
        tan_extremos = tan_extremos + 1

print("repartos:", repartos)
print("repartos tan extremos:", tan_extremos)
print("p-valor:", round(tan_extremos / repartos, 4))
```

```salida
diferencia observada: 5.5
repartos: 70
repartos tan extremos: 4
p-valor: 0.0571
```

Línea por línea:

1. `itertools.combinations(range(8), 4)` produce todas las formas de escoger 4 posiciones entre 8 (las 70 combinaciones).
2. Para cada una, `grupo_a` son los 4 valores escogidos y `grupo_b` los otros 4.
3. Se calcula la diferencia de medias y se compara su **valor absoluto** con el observado (así cuentan los dos sentidos: bilateral). El `- 1e-9` evita que un error diminuto de redondeo deje fuera un empate exacto.
4. Se cuentan los repartos tan extremos: **4** de 70.

**p-valor = 4 / 70 = 0,0571.** Se lee: *«si la visita extra no hiciera nada, solo en el 5,7 % de los repartos al azar se vería una diferencia tan grande como 5,5 pedidos (en cualquier sentido)»*.

Los 4 repartos extremos son el observado, su imagen invertida (A y B intercambiados) y otros dos con diferencias de 5,5 o más.

**5. Decidir.** Con `α = 0,05`: 0,0571 > 0,05, **no se rechaza `H0`**. La evidencia es cercana al umbral pero no lo cruza. Un detalle crucial: con `α = 0,06` la decisión sería la contraria. **El umbral 0,05 es una convención, no una ley de la naturaleza**; un p-valor de 0,049 y uno de 0,051 contienen casi la misma información. Presenta el p-valor exacto, no solo «significativo / no significativo».

**6. Lo que el p-valor NO es.** Todas estas frases son erróneas:

| Frase incorrecta | Por qué está mal |
|---|---|
| «Hay 5,7 % de probabilidad de que `H0` sea cierta» | el p-valor supone `H0` cierta; no da su probabilidad |
| «Hay 94,3 % de probabilidad de que el efecto sea real» | no es la probabilidad de la hipótesis alternativa |
| «Un p-valor pequeño significa un efecto grande» | mide rareza bajo `H0`, no tamaño del efecto (12.7) |
| «Un p-valor grande prueba que no hay efecto» | puede ser falta de datos |
| «p = 0,04 significa que el 4 % de las tiendas no mejoró» | no habla de porcentaje de unidades |

Lo que sí es: *una medida de qué tan sorprendentes serían los datos si no hubiera ningún efecto*.

**7. Lo que cambia el p-valor.** Con el mismo tamaño de diferencia (5,5), el p-valor baja si:

- hay **más datos**,
- los datos son **menos dispersos**,
- la diferencia observada es **mayor**.

Prueba con una diferencia más grande, cambiando el grupo A a `35, 31, 39, 33` (media 34,5; diferencia 9,5):

```python
import itertools
import statistics

a = [35, 31, 39, 33]
b = [24, 28, 22, 26]
todos = a + b
observada = statistics.mean(a) - statistics.mean(b)

extremos = 0
total = 0
for indices_a in itertools.combinations(range(8), 4):
    grupo_a = [todos[i] for i in indices_a]
    grupo_b = [todos[i] for i in range(8) if i not in indices_a]
    total = total + 1
    if abs(statistics.mean(grupo_a) - statistics.mean(grupo_b)) >= abs(observada) - 1e-9:
        extremos = extremos + 1

print(observada, extremos, total, round(extremos / total, 4))
```

```salida
9.5 2 70 0.0286
```

Ahora la diferencia es 9,5 y solo 2 de los 70 repartos (el observado y su inverso) son tan extremos: p = 2/70 = 0,0286, y sí se rechazaría `H0`. Con 4 datos por grupo, el **p-valor más pequeño posible** es 2/70 = 0,0286: no se podría obtener un p-valor menor aunque la separación fuera total. Es un recordatorio de lo limitado que es trabajar con muestras diminutas.

**8. Relación con la prueba `t`.** La prueba `t` de Welch (12.5) calcula el p-valor con una fórmula en lugar de contar repartos. Con estos mismos datos de la visita extra da p = 0,045, un valor un poco distinto al 0,057 exacto de la permutación: con muestras tan pequeñas, la aproximación de la fórmula no es perfecta. Que el p-valor cruce o no 0,05 según el método usado es la señal de que **la decisión está en el límite** y de que se necesitan más datos.

Ejemplo comercial: el piloto de la visita extra da p = 0,057 con 4 tiendas por grupo. La decisión sensata no es «no funciona» ni «funciona», sino «hay una señal que merece repetirse con más tiendas».

## Errores comunes

- **Interpretar el p-valor como la probabilidad de que `H0` sea cierta.**
- **Tratar 0,05 como un acantilado.**
- **Presentar solo «significativo/no significativo»** sin el p-valor exacto ni el tamaño del efecto.
- **Pensar que p pequeño = efecto grande o importante.**
- **Pensar que p grande = no hay diferencia.**
- **Buscar combinaciones de análisis hasta obtener p < 0,05** (lo veremos en 12.8).
- **No saber si la prueba era bilateral o unilateral.**

## Para comprobar que entendiste

1. ¿Qué cuenta el p-valor de una prueba de permutación?
2. Con 70 repartos y 7 tan extremos, ¿cuánto vale el p-valor?
3. ¿Por qué «p = 0,03» no significa «3 % de probabilidad de que `H0` sea cierta»?
4. ¿Qué dos cosas pueden hacer bajar un p-valor sin que el efecto real cambie?

<details><summary>Respuestas</summary>

1. La proporción de repartos al azar que producen una diferencia al menos tan extrema como la observada.
2. 7 / 70 = 0,10.
3. Porque el p-valor se calcula suponiendo que `H0` es cierta; no es la probabilidad de la hipótesis.
4. Aumentar el tamaño de la muestra y reducir la dispersión de los datos.

</details>

## Micropráctica

Con A = `18, 22, 25` y B = `14, 15, 19` (3 datos por grupo; hay `C(6, 3) = 20` repartos):

1. Calcula a mano la diferencia observada de medias (A − B).
2. Escribe y ejecuta el programa de permutación para obtener el p-valor bilateral.
3. Explica en una frase qué significa el resultado y por qué un p-valor tan grande no prueba que «no hay diferencia».

Cómo saber que está bien: la diferencia observada es 5,67 y el p-valor es 0,20 (4 de 20).

<details><summary>Comprobación de la parte 2</summary>

```python
import itertools
import statistics

a = [18, 22, 25]
b = [14, 15, 19]
todos = a + b
observada = statistics.mean(a) - statistics.mean(b)

extremos = 0
total = 0
for indices_a in itertools.combinations(range(6), 3):
    grupo_a = [todos[i] for i in indices_a]
    grupo_b = [todos[i] for i in range(6) if i not in indices_a]
    total = total + 1
    if abs(statistics.mean(grupo_a) - statistics.mean(grupo_b)) >= abs(observada) - 1e-9:
        extremos = extremos + 1

print(round(observada, 2), extremos, total, extremos / total)
```

```salida
5.67 4 20 0.2
```

</details>

## Después, en los ejercicios

El p-valor aparece en ST05–ST07 de [Estadística](../../03_EJERCICIOS/Estadistica/). Cuando lo reportes, escribe qué probabilidad es y qué decisión tomas, nunca solo el número. Siguiente: [12.5 Prueba t y Welch](05_prueba_t_welch.md).
