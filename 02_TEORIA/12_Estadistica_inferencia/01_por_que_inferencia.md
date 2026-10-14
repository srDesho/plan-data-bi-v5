# 12.1 Por qué hace falta la inferencia: la variabilidad entre muestras

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: capítulo 11 completo, en especial [11.1](../11_Estadistica_descriptiva/01_poblacion_muestra_variables.md) y [11.8](../11_Estadistica_descriptiva/08_muestreo.md).

## Para qué sirve

La estadística descriptiva te dice qué pasó **en los datos que tienes**. Pero las decisiones suelen ser sobre algo más grande: «si cambiamos la ruta, ¿venderemos más en todas las tiendas?». Solo observas una muestra, y otra muestra habría dado un resultado distinto. La **inferencia** es el conjunto de métodos para sacar conclusiones sobre la población a partir de una muestra, **midiendo la incertidumbre** en lugar de ignorarla. Esta lección muestra, con una simulación, de dónde sale esa incertidumbre.

## Términos nuevos

- **Inferencia estadística**: concluir sobre una población a partir de una muestra, acompañando la conclusión con una medida de incertidumbre.
- **Estimador**: una fórmula que calcula, con una muestra, un valor que estima un parámetro. La media muestral `x̄` es un estimador de la media poblacional `μ` (mu).
- **Estimación puntual**: el valor concreto que da el estimador con tu muestra (un solo número).
- **Variabilidad muestral**: el hecho de que el estadístico cambia de una muestra a otra aunque la población sea la misma.
- **Distribución muestral**: la distribución de los valores que tomaría un estadístico si repitieras el muestreo muchas veces.
- **Error estándar**: la desviación estándar de la distribución muestral; mide cuánto varía una estimación de una muestra a otra. Para la media se estima con `s / √n`.
- **Teorema del límite central**: resultado que dice que, con muestras suficientemente grandes, la distribución muestral de la media se parece a una campana (normal) aunque los datos individuales no lo sean.
- **Simulación**: repetir un experimento aleatorio muchas veces en la computadora para ver qué ocurre.

## Ejemplo paso a paso

**1. Una población de la que conocemos todo.** Para estudiar el muestreo necesitamos saber la «verdad». Construimos una población artificial de 1 000 tickets de venta (en Bs) con una fórmula fija y calculamos su media `μ` y su desviación `σ`:

```python
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
print(len(poblacion), min(poblacion), max(poblacion))
print(statistics.mean(poblacion))
print(round(statistics.pstdev(poblacion), 2))
```

```salida
1000 20 109
64.46
25.99
```

La población tiene 1 000 tickets entre Bs 20 y Bs 109. La media verdadera es **64,46** y la desviación poblacional es 25,99. En la vida real **nunca conoces esos números**; aquí los conocemos para poder comprobar qué tan bien funcionan las muestras.

**2. Cinco muestras, cinco promedios.** Sacamos 5 muestras de 30 tickets y calculamos el promedio de cada una:

```python
import random
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(7)

for numero in range(1, 6):
    muestra = azar.sample(poblacion, 30)
    print(numero, round(statistics.mean(muestra), 2))
```

```salida
1 60.93
2 67.43
3 63.07
4 65.37
5 63.07
```

Los cinco promedios son distintos entre sí y distintos de 64,46: unos quedan por debajo y otros por encima. **Eso es la variabilidad muestral**. Ninguna muestra se equivocó: cada una vio una parte distinta. Si hubieras tenido solo la primera, habrías estimado un promedio de 60,93; con la segunda, 67,43.

**3. Muchas muestras: la distribución muestral.** Repetimos el muestreo 1 000 veces y estudiamos los 1 000 promedios:

```python
import random
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(7)
promedios = [statistics.mean(azar.sample(poblacion, 30)) for _ in range(1000)]

print(round(statistics.mean(promedios), 2))
print(round(statistics.stdev(promedios), 2))
```

```salida
64.59
4.7
```

- El promedio de los 1 000 promedios es **64,59**, casi igual a la media verdadera (64,46): la media muestral **no tiene sesgo**; en promedio acierta.
- La desviación estándar de los promedios es **4,70**: esa es la medida de cuánto se mueve una estimación de una muestra a otra. Es el **error estándar**.

**4. El error estándar se estima con una sola muestra.** No necesitas repetir el muestreo (en la vida real tienes una sola muestra): el error estándar de la media se estima con la fórmula `s / √n`. Para una población con `σ = 25,99` y `n = 30`:

`25,99 / √30 = 25,99 / 5,477 = 4,74`

Un valor muy cercano al 4,70 de la simulación. La fórmula resume lo que viste: **la incertidumbre de un promedio depende de cuán dispersos son los datos (`s`) y de cuántos son (`n`)**.

**5. El efecto del tamaño de la muestra.** Repetimos con muestras de 120 tickets:

```python
import random
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(7)

for n in (30, 120):
    promedios = [statistics.mean(azar.sample(poblacion, n)) for _ in range(1000)]
    print(n, round(statistics.stdev(promedios), 2))
```

```salida
30 4.7
120 2.33
```

Con `n = 30` el error estándar es 4,70 y con `n = 120` baja a 2,33: **cuadruplicar el tamaño de la muestra reduce el error a la mitad** (porque divide entre `√n`: `√4 = 2`). Más datos dan estimaciones más estables, pero con rendimientos decrecientes. (Un detalle técnico: aquí la muestra de 120 sale de una población finita de 1 000, lo que reduce un poco más el error; con poblaciones muy grandes ese efecto no existe.)

**6. La forma de la distribución muestral.** Un histograma de texto de los 1 000 promedios de la parte 3:

```python
import random
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(7)
promedios = [statistics.mean(azar.sample(poblacion, 30)) for _ in range(1000)]

limites = [50, 55, 60, 65, 70, 75, 80]
for i in range(len(limites) - 1):
    cuantos = sum(1 for p in promedios if limites[i] <= p < limites[i + 1])
    print(f"{limites[i]:>3}-{limites[i + 1]:<3} {'#' * (cuantos // 10)} {cuantos}")
```

```salida
 50-55  # 11
 55-60  ############### 154
 60-65  ################################### 355
 65-70  ################################### 355
 70-75  ########## 107
 75-80  # 15
```

La figura tiene forma de campana, centrada en la media verdadera (64,5), aunque la población original **no** tiene forma de campana (sus valores se reparten parejo entre 20 y 109). Eso es el **teorema del límite central**: los promedios de muestras suficientemente grandes se distribuyen aproximadamente normal. Es la razón por la que los métodos del resto del capítulo funcionan.

**7. Qué significa todo esto para las decisiones.** Cuando alguien te dice «el promedio de la muestra es 67», la pregunta inmediata es: *¿con qué incertidumbre?* Un promedio sin su error estándar (o sin un intervalo, lección 12.2) no permite saber si «67» es distinto de «64» o es la variación normal entre muestras.

Ejemplo comercial: dos semanas de prueba con un nuevo horario de reparto dan 5 % más de pedidos que el horario anterior. Si el pedido semanal normalmente fluctúa ±8 % por simple variación, ese 5 % puede ser ruido. La inferencia ayuda a separar la señal del ruido.

## Errores comunes

- **Tratar el resultado de una muestra como el valor exacto de la población.**
- **Ignorar el tamaño de la muestra** al comparar promedios.
- **Pensar que una muestra mayor elimina todo error**: lo reduce con `√n`.
- **Confundir desviación estándar** (dispersión de los datos) **con error estándar** (dispersión del promedio entre muestras).
- **Creer que si dos muestras difieren, una está mal.**
- **Extraer conclusiones de una sola muestra pequeña y sesgada.**
- **Olvidar que el teorema del límite central necesita datos independientes** y una muestra suficientemente grande.

## Para comprobar que entendiste

1. ¿Qué es la variabilidad muestral?
2. ¿En qué se diferencia la desviación estándar de los datos del error estándar de la media?
3. Si el error estándar con `n = 25` es 6, ¿cuánto esperarías con `n = 100`?
4. ¿Por qué el histograma de los promedios parece una campana aunque los datos no?

<details><summary>Respuestas</summary>

1. El cambio del estadístico (por ejemplo el promedio) de una muestra a otra de la misma población.
2. La primera mide cuánto se dispersan los datos individuales; la segunda, cuánto varía el promedio de una muestra a otra.
3. Unos 3: cuadruplicar `n` divide el error entre 2.
4. Por el teorema del límite central: los promedios de muestras suficientemente grandes se acercan a la normal.

</details>

## Micropráctica

1. Con la misma población, saca 8 muestras de tamaño 10 (semilla 21) y anota sus promedios. ¿Varían más o menos que las de tamaño 30?
2. Calcula el error estándar teórico `σ / √n` para `n = 10` y compáralo con la desviación estándar de 1 000 promedios simulados.
3. Explica a un compañero, en dos frases, por qué «el promedio de mi muestra es 67» no basta.

Cómo saber que está bien: el error con `n = 10` es mayor que con `n = 30` (alrededor de 8).

<details><summary>Comprobación de la parte 2</summary>

```python
import math
import random
import statistics

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(21)
promedios = [statistics.mean(azar.sample(poblacion, 10)) for _ in range(1000)]
print(round(25.99 / math.sqrt(10), 2), round(statistics.stdev(promedios), 2))
```

```salida
8.22 8.23
```

</details>

## Después, en los ejercicios

Las preguntas sobre «¿puede ser azar?» de ST05–ST07 en [Estadística](../../03_EJERCICIOS/Estadistica/) parten de esta idea. Siguiente: [12.2 Estimación e intervalos de confianza](02_estimacion_intervalo_confianza.md).
