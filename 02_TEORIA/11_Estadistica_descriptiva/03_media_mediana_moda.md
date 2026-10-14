# 11.3 Media, mediana y moda

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisito: [11.2 Frecuencias](02_frecuencias.md), practicadas con G6.

Antes de calcular, declara qué representa cada observación: AN01 prepara esa pregunta. AN08 describe los pedidos de K1, sin inferir resultados para otra población. [11.1](01_poblacion_muestra_variables.md) amplía población, muestra y tipos de variable; no sustituye los cálculos que se enseñan aquí.

## Para qué sirve

Cuando alguien pregunta «¿cuánto vende una tienda normalmente?» o «¿cuántas entregas hace un repartidor al día?», quiere **un solo número que represente a todos**. Hay tres formas de elegirlo (media, mediana y moda) y dan respuestas distintas cuando los datos no son simétricos. Elegir la medida equivocada es una de las formas más comunes de contar una historia falsa con números verdaderos.

## Términos nuevos

- **Medida de tendencia central**: un valor que resume dónde se concentra un conjunto de datos.
- **Media aritmética** (promedio): la suma de todos los valores dividida entre la cantidad de valores. Se escribe `x̄` (x barra) para una muestra: `x̄ = Σx / n`. El símbolo `Σ` (sigma) significa «suma de todos los valores».
- **Mediana**: el valor del medio cuando los datos están ordenados de menor a mayor. La mitad de los valores está por debajo y la otra mitad por encima. Si `n` es par, es el promedio de los dos valores centrales.
- **Moda**: el valor que más se repite. Puede haber más de una moda, o ninguna.
- **Valor atípico** (*outlier*): un valor muy lejano al resto. Se estudia en 11.5.
- **Robusta**: una medida que casi no cambia cuando aparecen valores extremos. La mediana es robusta; la media no.
- **Asimetría**: cuando la distribución no es simétrica; tiene una «cola» larga hacia un lado.

## Ejemplo paso a paso

Datos inventados: entregas realizadas en un día por 10 repartidores de la distribuidora:

`12, 15, 15, 18, 20, 22, 25, 28, 30, 55`

**1. La media.**

1. Suma todos los valores: 12 + 15 + 15 + 18 + 20 + 22 + 25 + 28 + 30 + 55 = **240**.
2. Cuenta los valores: n = **10**.
3. Divide: 240 / 10 = **24**.

La media es 24 entregas por repartidor.

**2. La mediana.** Ya están ordenados. Con n = 10 (par), los dos valores del centro son el 5.º (20) y el 6.º (22). La mediana es su promedio: (20 + 22) / 2 = **21**.

**3. La moda.** El valor 15 aparece dos veces; los demás una. La moda es **15**.

**4. Comprobar con Python.**

```python
import statistics

entregas = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
print(statistics.mean(entregas))
print(statistics.median(entregas))
print(statistics.mode(entregas))
```

```salida
24
21.0
15
```

Coincide con lo calculado a mano: 24, 21 y 15. **Siempre calcula una vez a mano con pocos datos para saber qué hace la función.**

**5. Por qué importa elegir.** Los tres números son distintos (24, 21, 15). La media (24) es mayor que la mediana (21) porque el repartidor de 55 entregas «jala» el promedio hacia arriba. Quita ese valor y mira:

```python
import statistics

sin_extremo = [12, 15, 15, 18, 20, 22, 25, 28, 30]
print(round(statistics.mean(sin_extremo), 2))
print(statistics.median(sin_extremo))
```

```salida
20.56
20
```

La media baja de 24 a 20,56 (un cambio de 3,4 entregas por un solo valor), mientras que la mediana pasa solo de 21 a 20. Por eso decimos que la **mediana es robusta** y la media no. Con un valor atípico, la media deja de representar al repartidor «típico»: nueve de los diez hicieron 30 o menos, pero la media (24) sugiere que lo normal es acercarse a 24.

**6. Cuándo usar cada una.**

| Situación | Medida adecuada | Por qué |
|---|---|---|
| Datos simétricos, sin extremos | media | usa toda la información |
| Datos con cola larga (ingresos, tickets, tiempos) | mediana | no la arrastran los extremos |
| Variable categórica | moda | no se puede promediar una categoría |
| Necesitas el total (ventas totales = media × n) | media | solo la media conserva el total |

Esta última fila es importante: si quieres proyectar un total, usa la media; si quieres describir al caso típico, usa la mediana. Muchas veces se reportan las dos.

**7. Con Pandas.**

```python
import pandas as pd

entregas = pd.Series([12, 15, 15, 18, 20, 22, 25, 28, 30, 55])
print(entregas.mean())
print(entregas.median())
print(entregas.mode().tolist())
```

```salida
24.0
21.0
[15]
```

`mode()` devuelve una lista porque puede haber varias modas; aquí hay una.

**8. Medias que engañan: el promedio de promedios.** Dos rutas: la ruta A tiene 2 repartidores con promedio 40 y la B tiene 8 con promedio 20. El promedio de los dos promedios es 30, pero el promedio real de los 10 repartidores es (2×40 + 8×20) / 10 = 24. Igual que con los porcentajes de la lección 2.3: **para combinar grupos, pondera por tamaño** (suma total entre n total).

Ejemplo comercial: si «la venta mediana por tienda es de Bs 220» pero «la venta media es de Bs 265» (cifras inventadas para ilustrar), la tienda típica vende menos de lo que el promedio sugiere, porque unas pocas tiendas grandes elevan la media. Un gerente que presupuesta cada tienda con la media sobreestima a la mayoría.

## Errores comunes

- **Usar la media con datos muy sesgados** sin mirar la mediana.
- **Promediar promedios de grupos de distinto tamaño.**
- **Calcular la moda de una variable continua** sin agrupar (casi nunca se repite).
- **Olvidar ordenar antes de buscar la mediana.**
- **Confundir la mediana con el promedio de los extremos.**
- **Ignorar los valores nulos**: `mean()` de Pandas los omite, y eso cambia `n`.
- **Reportar solo un número** sin la cantidad de datos.

## Para comprobar que entendiste

1. Calcula a mano la media y la mediana de `4, 8, 6, 5, 3, 200`.
2. ¿Cuál de las dos medidas es más representativa del caso típico y por qué?
3. ¿Qué es la moda de `{"A", "B", "B", "C"}`?
4. ¿Por qué la media de 2 promedios no es el promedio global?

<details><summary>Respuestas</summary>

1. Suma = 226, n = 6, media = 37,67. Ordenados: 3, 4, 5, 6, 8, 200; mediana = (5 + 6) / 2 = 5,5.
2. La mediana (5,5), porque el 200 arrastra la media.
3. `"B"`.
4. Porque los grupos tienen distinto tamaño; hay que ponderar.

</details>

## Micropráctica

Con los tiempos de entrega (en minutos) `[34, 28, 31, 29, 33, 30, 28, 95]`:

1. Calcula a mano la media, la mediana y la moda. Después verifica con Python.
2. Calcula la media sin el valor 95 y explica en una frase qué ocurrió.
3. Decide cuál presentarías al jefe de logística como «tiempo típico» y justifícalo.

Cómo saber que está bien: media 38,5; mediana 30,5; moda 28; sin el 95 la media baja a 30,43.

<details><summary>Comprobación</summary>

```python
import statistics

tiempos = [34, 28, 31, 29, 33, 30, 28, 95]
print(statistics.mean(tiempos), statistics.median(tiempos), statistics.mode(tiempos))
print(round(statistics.mean([34, 28, 31, 29, 33, 30, 28]), 2))
```

```salida
38.5 30.5 28
30.43
```

</details>

## Después, en los ejercicios

ST01 y ST02 de [Estadística](../../03_EJERCICIOS/Estadistica/) piden estas medidas; el enunciado indica qué medida reportar y por qué. Siguiente: [11.4 Medidas de dispersión](04_dispersion.md).
