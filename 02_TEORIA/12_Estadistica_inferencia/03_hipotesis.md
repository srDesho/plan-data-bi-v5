# 12.3 Hipótesis nula, hipótesis alternativa y errores

> Tiempo estimado: 60 min (lectura 30 + práctica 30). Prerrequisitos: [12.1](01_por_que_inferencia.md) y [12.2](02_estimacion_intervalo_confianza.md).

## Para qué sirve

«La visita extra aumentó los pedidos»: ¿lo demuestran los datos o fue el azar? Una prueba de hipótesis es el procedimiento ordenado para decidir si una diferencia observada es **lo bastante grande como para no atribuirla razonablemente al azar**. Entender su lógica (qué se supone, qué se decide y qué errores se pueden cometer) es más importante que memorizar fórmulas, porque la lógica es la misma en todas las pruebas.

## Términos nuevos

- **Hipótesis nula (`H0`)**: la afirmación de «no pasa nada»: no hay diferencia, no hay efecto, no hay relación. Es el punto de partida que se intenta refutar.
- **Hipótesis alternativa (`H1`)**: la afirmación que se sospecha: sí hay diferencia o efecto.
- **Prueba de hipótesis**: el procedimiento que mide qué tan compatibles son los datos con `H0`.
- **Estadístico de prueba**: un número calculado con la muestra (por ejemplo `t`) que resume qué tan lejos están los datos de lo esperado bajo `H0`.
- **p-valor**: la probabilidad de obtener un resultado **tan extremo o más** que el observado **si `H0` fuera cierta**. Se estudia a fondo en 12.4.
- **Nivel de significancia (`α`)**: el umbral que fijas **antes** de ver los datos (casi siempre 0,05) para decidir. Si p-valor ≤ `α`, rechazas `H0`.
- **Rechazar `H0`**: concluir que los datos son difíciles de explicar solo con el azar bajo `H0`.
- **No rechazar `H0`**: concluir que los datos no aportan evidencia suficiente contra `H0`. **No** equivale a demostrar que `H0` es cierta.
- **Error tipo I**: rechazar `H0` cuando era cierta (falsa alarma). Su probabilidad máxima es `α`.
- **Error tipo II**: no rechazar `H0` cuando era falsa (no detectar un efecto real). Su probabilidad se llama `β`.
- **Potencia** (`1 − β`): la probabilidad de detectar un efecto real. Depende del tamaño de la muestra y del tamaño del efecto.
- **Prueba bilateral / unilateral**: la bilateral detecta diferencias en cualquier sentido (`H1`: «distinto»); la unilateral, solo en un sentido (`H1`: «mayor»).

## Ejemplo paso a paso

**El caso:** la distribuidora prueba una **visita extra** a 4 tiendas (grupo A) y deja 4 tiendas igual que siempre (grupo B). Se mide el número de pedidos por tienda en un mes: A = `31, 27, 35, 29` y B = `24, 28, 22, 26`.

**1. Formular las hipótesis (antes de mirar el resultado).**

- `H0`: la visita extra no cambia el promedio de pedidos (`μA = μB`).
- `H1`: la visita extra cambia el promedio de pedidos (`μA ≠ μB`) (bilateral).
- Nivel de significancia: `α = 0,05`.

**2. Lo que se observa.** `x̄A = 30,5` y `x̄B = 25,0`; la diferencia es **5,5 pedidos**. La pregunta correcta no es «¿hay diferencia?» (siempre habrá alguna) sino: *si la visita extra no hiciera nada, ¿qué tan raro sería ver una diferencia de 5,5 o más solo por cómo cayeron las tiendas en cada grupo?*

**3. La lógica del tribunal.** Es como un juicio: `H0` es la presunción de inocencia. Se necesita evidencia fuerte para rechazarla. Si la evidencia no alcanza, «no se declara culpable», pero eso **no prueba** que sea inocente: significa que el caso no se pudo sostener con estas pruebas.

**4. Los cuatro resultados posibles.**

| Realidad → / Decisión ↓ | `H0` es cierta (no hay efecto) | `H0` es falsa (sí hay efecto) |
|---|---|---|
| **No rechazar `H0`** | decisión correcta | **error tipo II** (se perdió un efecto real) |
| **Rechazar `H0`** | **error tipo I** (falsa alarma) | decisión correcta (potencia) |

Ejemplo de negocio: error tipo I = generalizar la visita extra a todas las rutas gastando dinero por un efecto que era azar. Error tipo II = descartar una visita extra que sí funcionaba. Cuál es más costoso depende del negocio; por eso `α` se fija con criterio y no por costumbre.

**5. Qué significa `α = 0,05` en la práctica.** Si `H0` fuera cierta y repitiéramos el experimento muchas veces, rechazaríamos `H0` por mala suerte en el 5 % de los casos. Lo comprobamos simulando 1 000 comparaciones entre dos grupos de 15 tickets sacados de la **misma** población (donde `H0` es cierta por construcción):

```python
import random
from scipy import stats

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(3)

falsas_alarmas = 0
for _ in range(1000):
    a = azar.sample(poblacion, 15)
    b = azar.sample(poblacion, 15)
    p = stats.ttest_ind(a, b, equal_var=False).pvalue
    if p < 0.05:
        falsas_alarmas = falsas_alarmas + 1

print(falsas_alarmas, "de 1000")
```

```salida
39 de 1000
```

(`stats.ttest_ind` es la prueba `t` de la lección 12.5; aquí solo la usamos como una herramienta que devuelve el p-valor de cada comparación.) De las 1 000 comparaciones, **39** resultaron «significativas» aunque no había ninguna diferencia real: cerca del 5 % esperado (50). Esto es el error tipo I en acción: **5 % de falsas alarmas es el costo de usar `α = 0,05`**. Si haces 20 comparaciones, esperas encontrar una falsa alarma en promedio (lo retomamos en 12.8).

**6. La potencia y el tamaño de la muestra.** Con muestras de 4 tiendas por grupo, detectar diferencias pequeñas es muy difícil: aunque el efecto fuera real, el azar lo taparía muchas veces (error tipo II alto). Para aumentar la potencia: más datos, menos variabilidad en la medición o un efecto más grande. **No rechazar `H0` con una muestra pequeña casi nunca significa «no hay efecto»; significa «no se pudo ver».**

**7. Cómo se decide (los pasos).**

1. Plantear `H0`, `H1` y `α` **antes** de ver los datos.
2. Verificar que las condiciones de la prueba se cumplan (independencia, aleatoriedad, forma de los datos).
3. Calcular el estadístico y el p-valor (lecciones 12.4 y 12.5).
4. Decidir: p-valor ≤ `α` → rechazar `H0`; si no, no rechazar.
5. **Interpretar en lenguaje del negocio**, con el tamaño del efecto (12.7) y las limitaciones (12.8).

**8. Prueba unilateral o bilateral.** Si solo te importa saber si la visita **aumenta** los pedidos, `H1` es «mayor» (unilateral). Pero decídelo antes de ver los datos: elegir la dirección después, mirando hacia dónde salieron, es hacer trampa. En caso de duda usa bilateral, que es más exigente.

Ejemplo comercial: «el nuevo horario reduce el tiempo de entrega» tiene `H0`: no lo reduce. Aun si el promedio nuevo es menor, solo rechazas `H0` si esa diferencia sería rara bajo el azar; y la decisión de cambiar el horario para toda la flota considera también el costo de equivocarse.

## Errores comunes

- **Plantear las hipótesis después de ver los resultados.**
- **Decir «aceptamos `H0`»** como si estuviera demostrada.
- **Confundir significancia (`α`) con probabilidad de que `H0` sea cierta.**
- **Elegir `α` después de ver el p-valor.**
- **Ignorar el error tipo II** con muestras pequeñas.
- **Usar prueba unilateral solo porque da un p-valor menor.**
- **Creer que «significativo» significa «importante»** (lo verás en 12.7).

## Para comprobar que entendiste

1. ¿Qué afirma `H0` en la prueba de la visita extra?
2. Si el p-valor es 0,03 y `α = 0,05`, ¿qué decides?
3. ¿Qué es un error tipo II y cuándo es probable?
4. ¿Por qué «no rechazar `H0`» no es lo mismo que «`H0` es cierta»?

<details><summary>Respuestas</summary>

1. Que la visita extra no cambia el promedio de pedidos.
2. Rechazo `H0`: 0,03 ≤ 0,05.
3. No detectar un efecto real; es probable con muestras pequeñas o mucha variabilidad.
4. Porque la falta de evidencia no demuestra que no haya efecto; puede deberse a pocos datos.

</details>

## Micropráctica

1. Plantea `H0`, `H1` y `α` para esta pregunta: «¿el tiempo medio de entrega de la ruta R02 es distinto al de R03?».
2. Para un nuevo sistema de pedidos, describe un error tipo I y uno tipo II en términos del negocio.
3. Con tus palabras: ¿por qué un resultado «no significativo» con 5 observaciones por grupo es débil como argumento de que no hay diferencia?

Cómo saber que está bien: en la 1 `H1` es bilateral («distinto»); en la 3 mencionas la potencia o el tamaño de la muestra.

<details><summary>Ejemplo de respuesta para la parte 1</summary>

`H0`: el tiempo medio de entrega de R02 es igual al de R03 (`μ2 = μ3`). `H1`: son distintos (`μ2 ≠ μ3`). `α = 0,05`, fijado antes de revisar los datos.

</details>

## Después, en los ejercicios

ST05–ST07 de [Estadística](../../03_EJERCICIOS/Estadistica/) piden plantear `H0`, `H1` y `α` antes de calcular. Escríbelos primero en tu hoja. Siguiente: [12.4 El p-valor](04_pvalor.md).
