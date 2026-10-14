# 12.7 Tamaño del efecto: significativo no es lo mismo que importante

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [12.5 Prueba t](05_prueba_t_welch.md) y [12.6 Chi-cuadrado](06_chi_cuadrado.md).

## Para qué sirve

Un p-valor pequeño dice que la diferencia **probablemente no es azar**; no dice que sea **grande** ni que valga la pena actuar. Con muchos datos, hasta una diferencia ínfima sale «significativa»; con pocos datos, una diferencia enorme puede no serlo. El tamaño del efecto mide **cuánto** cambia algo, en una escala comparable, y es lo que realmente necesita quien decide.

## Términos nuevos

- **Tamaño del efecto**: una medida de la magnitud de una diferencia o de una asociación, independiente del tamaño de la muestra.
- **Significancia estadística**: que el resultado sea difícil de explicar solo por azar (p-valor ≤ `α`).
- **Significancia práctica**: que la diferencia sea lo bastante grande como para importar al negocio (costo, ganancia, riesgo).
- **`d` de Cohen**: la diferencia de medias dividida entre la desviación estándar combinada: `d = (x̄A − x̄B) / s_comb`. Expresa la diferencia en «desviaciones estándar».
- **Desviación estándar combinada** (*pooled*): `s_comb = √[((nA − 1)·sA² + (nB − 1)·sB²) / (nA + nB − 2)]`.
- **Diferencia de proporciones** y **riesgo relativo**: para categorías; la diferencia en puntos porcentuales y el cociente entre las dos proporciones.
- **V de Cramér**: tamaño de la asociación en una tabla de contingencia: `V = √(χ² / (n × (k − 1)))`, con `k` = el menor entre filas y columnas. Va de 0 a 1.
- **Costo-beneficio**: comparar el beneficio esperado de una diferencia con lo que cuesta lograrla.

## Ejemplo paso a paso

**1. `d` de Cohen para la visita extra.** Con A = `31, 27, 35, 29` y B = `24, 28, 22, 26`:

- Diferencia de medias: `30,5 − 25,0 = 5,5` pedidos.
- Varianzas: `sA² = 11,667` y `sB² = 6,667`.
- Desviación combinada: `s_comb = √[(3 × 11,667 + 3 × 6,667) / 6] = √(55 / 6) = √9,167 = 3,028`.
- `d = 5,5 / 3,028 = 1,82`.

La diferencia es de **1,8 desviaciones estándar**: un efecto grande. Como referencia orientativa (convenciones de Cohen, no leyes): 0,2 pequeño, 0,5 mediano, 0,8 grande.

```python
import math
import statistics

a = [31, 27, 35, 29]
b = [24, 28, 22, 26]
va, vb = statistics.variance(a), statistics.variance(b)
s_comb = math.sqrt((3 * va + 3 * vb) / 6)
d = (statistics.mean(a) - statistics.mean(b)) / s_comb
print(round(s_comb, 3), round(d, 2))
```

```salida
3.028 1.82
```

Sin embargo, recuerda que esa estimación se basa en solo 4 tiendas por grupo: un `d` de 1,8 con tan pocos datos es muy incierto. El tamaño del efecto debe ir acompañado de su **intervalo** o, al menos, de una advertencia.

**2. Efecto en categorías.** En la tabla de la llamada previa (12.6): 60 % frente a 36 %.

- **Diferencia de proporciones**: `0,60 − 0,36 = 0,24` → 24 puntos porcentuales.
- **Riesgo relativo**: `0,60 / 0,36 = 1,67` → con llamada previa, la probabilidad de pedido es 1,67 veces (67 % mayor) que sin ella.
- **V de Cramér**: `√(5,769 / (100 × 1)) = √0,05769 = 0,24`.

```python
import math

con_llamada, sin_llamada = 30 / 50, 18 / 50
print(round(con_llamada - sin_llamada, 2))
print(round(con_llamada / sin_llamada, 2))
print(round(math.sqrt(5.769 / (100 * 1)), 2))
```

```salida
0.24
1.67
0.24
```

Las dos primeras cifras son las que entiende un gerente («24 puntos más», «1,67 veces»). La V indica una asociación de pequeña a moderada.

**3. Un efecto minúsculo puede ser «significativo».** Simulamos dos grupos enormes de 20 000 clientes cuyo ticket medio difiere en apenas Bs 0,86 sobre una dispersión de Bs 25:

```python
import random
import statistics
from scipy import stats

azar = random.Random(5)
a = [azar.gauss(100, 25) for _ in range(20000)]
b = [azar.gauss(100.8, 25) for _ in range(20000)]

prueba = stats.ttest_ind(b, a, equal_var=False)
diferencia = statistics.mean(b) - statistics.mean(a)
print("diferencia de medias:", round(diferencia, 2))
print("p-valor:", round(prueba.pvalue, 4))
print("d de Cohen:", round(diferencia / 25, 3))
```

```salida
diferencia de medias: 0.86
p-valor: 0.0006
d de Cohen: 0.034
```

El p-valor (≈ 0,0006) es mucho menor que 0,05: **estadísticamente significativo**. Pero la diferencia es de Bs 0,86 sobre un ticket de unos Bs 100 (menos de 1 %), y `d ≈ 0,03`: un efecto prácticamente nulo. Si cambiar el proceso para conseguir esa mejora cuesta más de lo que aporta, la decisión correcta es **no hacerlo**, aunque «sea significativo». El tamaño de la muestra hizo posible detectar algo que no importa.

**4. El caso contrario.** Un efecto grande con pocos datos puede no ser significativo: es lo que nos pasó en 12.4 (p = 0,057) con `d = 1,8`. La conclusión no es «no hay efecto», sino «no hay datos suficientes para estar seguros: repetir con más tiendas».

**5. Resumen: cuatro combinaciones.**

| | efecto grande | efecto pequeño |
|---|---|---|
| **p ≤ 0,05** | actuar (verificando supuestos y costos) | detectable pero quizá irrelevante: mirar el costo-beneficio |
| **p > 0,05** | prometedor pero inconcluso: conseguir más datos | probablemente nada relevante |

**6. Qué reportar siempre.** Para una comparación: tamaños de grupo, medias (o medianas), diferencia, intervalo de confianza de la diferencia, p-valor, tamaño del efecto (`d` o puntos porcentuales) e interpretación de negocio con una limitación. Un número solo (p = 0,03) es información incompleta.

**7. Traducir el efecto a dinero.** Si la visita extra aporta 5,5 pedidos por tienda al mes, a una ganancia de Bs 20 por pedido son Bs 110 por tienda; si la visita cuesta Bs 90, la ganancia neta es de Bs 20 por tienda. Con esa cuenta, la decisión depende de la precisión: si el intervalo incluye valores cercanos a 0 pedidos (como vimos en 12.5), la inversión podría perderse. La estadística informa; la decisión incorpora el costo y el riesgo.

Ejemplo comercial: una promoción sube el ticket promedio Bs 1,20 con un p-valor de 0,001 en 15 000 clientes. Significativo, sí. Pero si la promoción cuesta Bs 2 por cliente, **pierde dinero**.

## Errores comunes

- **Reportar solo el p-valor.**
- **Confundir «significativo» con «grande» o «importante».**
- **Concluir «no hay efecto» ante un p-valor alto con pocos datos.**
- **Usar el `d` de Cohen sin mirar la dispersión ni los atípicos.**
- **Comparar tamaños de efecto de variables muy distintas sin considerar el contexto.**
- **Olvidar el costo del cambio** al evaluar una diferencia.
- **Presentar el riesgo relativo sin las proporciones absolutas** (un «aumento del 50 %» de 2 % a 3 % es solo 1 punto).

## Para comprobar que entendiste

1. ¿Por qué un p-valor muy pequeño puede acompañar a una diferencia sin importancia práctica?
2. Si `d = 0,2`, ¿cómo lo describirías?
3. ¿Qué diferencia hay entre 24 puntos porcentuales y un riesgo relativo de 1,67?
4. ¿Qué cuatro números mínimos debe llevar el reporte de una comparación de medias?

<details><summary>Respuestas</summary>

1. Porque con muchísimos datos el azar casi no tiene espacio y se detectan diferencias minúsculas.
2. Un efecto pequeño (la diferencia es una quinta parte de una desviación estándar).
3. Los puntos porcentuales son la diferencia absoluta (60 % − 36 %); el riesgo relativo es el cociente (60 % / 36 %).
4. La diferencia de medias, su intervalo de confianza, el p-valor y el tamaño del efecto (además de los `n`).

</details>

## Micropráctica

Con las rutas de 12.5 (R_A y R_B de tiempos de entrega):

1. Calcula el `d` de Cohen a mano con la desviación combinada.
2. Interprétalo con la escala de 0,2 / 0,5 / 0,8.
3. Si cada minuto menos de entrega vale Bs 4 por pedido y la ruta atiende 200 pedidos al mes, ¿cuánto vale la diferencia de medias en Bs al mes? (Esta cuenta es ilustrativa.)

Cómo saber que está bien: `d` ≈ 1,86 (efecto muy grande) y la diferencia de 6,5 minutos × Bs 4 × 200 = Bs 5 200 al mes, antes de descontar costos.

<details><summary>Comprobación de la parte 1</summary>

```python
import math
import statistics

ra = [42, 38, 45, 50, 41, 47, 44, 39]
rb = [35, 40, 33, 38, 36, 41, 34, 37]
s_comb = math.sqrt((7 * statistics.variance(ra) + 7 * statistics.variance(rb)) / 14)
print(round(s_comb, 3), round((statistics.mean(ra) - statistics.mean(rb)) / s_comb, 2))
```

```salida
3.495 1.86
```

</details>

## Después, en los ejercicios

ST06 y ST07 de [Estadística](../../03_EJERCICIOS/Estadistica/) piden separar «significativo» de «importante». Cierra cada respuesta con una recomendación que considere el tamaño del efecto y una limitación. Siguiente: [12.8 Interpretar, comunicar y no equivocarse](08_interpretacion_limitaciones.md).
