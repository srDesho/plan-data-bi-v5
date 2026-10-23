# 11.8 Muestreo: cómo escoger una muestra que sirva

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisito: [11.1 Población, muestra y variables](01_poblacion_muestra_variables.md).

## Para qué sirve

No siempre puedes revisar a todos los clientes: una encuesta, una auditoría de inventario o una prueba piloto trabajan con una parte. Si la parte se escoge mal, ninguna cuenta posterior la arregla: tus conclusiones serán sobre un grupo distinto del que querías estudiar. Esta lección explica cómo escoger muestras confiables y por qué el tamaño no lo es todo.

## Términos nuevos

- **Muestreo**: el proceso de escoger una muestra de la población.
- **Marco muestral**: la lista de unidades de la que realmente se puede escoger (por ejemplo, el listado de clientes activos). Si el marco no incluye a todos, parte de la población no tiene oportunidad de ser elegida.
- **Muestreo aleatorio simple**: cada unidad tiene la misma probabilidad de ser escogida, y la elección se hace al azar (sorteo).
- **Muestreo estratificado**: se divide la población en grupos homogéneos llamados **estratos** (por ejemplo, rutas) y se toma una muestra al azar de cada estrato. Garantiza que todos los grupos estén representados.
- **Muestreo sistemático**: se escoge cada `k`-ésima unidad de una lista, a partir de un punto inicial al azar.
- **Muestra de conveniencia**: la que se arma con lo que es fácil de alcanzar (los clientes cercanos, los que contestaron). No es aleatoria.
- **Sesgo de selección**: cuando la forma de escoger favorece a ciertas unidades y la muestra no representa a la población.
- **Sesgo de no respuesta**: cuando quienes no contestan son distintos de quienes contestan.
- **Error de muestreo**: la diferencia inevitable entre el estadístico de la muestra y el parámetro de la población, por el simple hecho de ver solo una parte.
- **Semilla** (*seed*): un número que fija el azar de la computadora para que el sorteo sea repetible.

## Ejemplo paso a paso

Población (inventada): las ventas de septiembre, en Bs, de 12 tiendas de tres rutas (4 por ruta):

| Ruta | Ventas de sus 4 tiendas (Bs) |
|---|---|
| R01 | 320, 150, 410, 90 |
| R02 | 560, 220, 180, 730 |
| R03 | 260, 140, 300, 480 |

**1. El parámetro.** Si tenemos a las 12, la media poblacional es la suma entre 12. La suma es 320+150+410+90 + 560+220+180+730 + 260+140+300+480 = 970 + 1690 + 1180 = **3840**; 3840 / 12 = **320**. El parámetro es 320 Bs por tienda.

**2. Muestra aleatoria simple.** Sorteamos 4 de las 12 con una semilla fija:

```python
import random
import statistics

poblacion = [320, 150, 410, 90, 560, 220, 180, 730, 260, 140, 300, 480]
print(statistics.mean(poblacion))

azar = random.Random(5)
muestra = azar.sample(poblacion, 4)
print(muestra)
print(statistics.mean(muestra))
```

```salida
320
[140, 560, 220, 260]
295
```

`random.Random(5)` crea un generador con la semilla 5, y `sample(poblacion, 4)` escoge 4 elementos **sin repetir**. Con otra semilla saldría otra muestra. Cada muestra da un promedio distinto del parámetro (320): esa diferencia es el **error de muestreo**, y es normal.

**3. Muestra de conveniencia: el sesgo.** Un vendedor propone «preguntemos a las 4 tiendas más grandes, que son las más fáciles de ubicar»:

```python
import statistics

poblacion = [320, 150, 410, 90, 560, 220, 180, 730, 260, 140, 300, 480]
las_mas_grandes = sorted(poblacion, reverse=True)[:4]
print(las_mas_grandes)
print(statistics.mean(las_mas_grandes))
```

```salida
[730, 560, 480, 410]
545
```

La media de esta muestra es 545, muy por encima del 320 real. No es mala suerte: es **sesgo**. La forma de escoger favorece sistemáticamente a las tiendas grandes, así que se repetiría en cualquier intento. **Una muestra grande pero sesgada es peor que una pequeña pero aleatoria**, porque el sesgo no desaparece al agregar más datos del mismo tipo.

**4. Muestreo estratificado.** Queremos asegurarnos de que cada ruta aparezca. Tomamos 2 tiendas al azar de cada ruta (6 en total):

```python
import random
import statistics

estratos = {
    "R01": [320, 150, 410, 90],
    "R02": [560, 220, 180, 730],
    "R03": [260, 140, 300, 480],
}
azar = random.Random(5)
muestra = []
for ruta, ventas in estratos.items():
    muestra = muestra + azar.sample(ventas, 2)

print(muestra)
print(len(muestra), statistics.mean(muestra))
```

```salida
[410, 90, 180, 730, 260, 140]
6 301.6666666666667
```

Cada ruta aporta exactamente 2 tiendas, así que ninguna queda sin representar (algo que una muestra aleatoria simple de 6 podría no lograr). Como todos los estratos tienen el mismo tamaño aquí, el promedio de la muestra es un buen estimador; si los estratos tuvieran tamaños distintos habría que ponderar por su peso en la población.

**5. El tamaño de la muestra y la variabilidad.** Repetimos el sorteo 500 veces con muestras de 3 y de 9 tiendas, y miramos cuánto varían los promedios obtenidos:

```python
import random
import statistics

poblacion = [320, 150, 410, 90, 560, 220, 180, 730, 260, 140, 300, 480]
azar = random.Random(2026)

for n in (3, 9):
    promedios = [statistics.mean(azar.sample(poblacion, n)) for _ in range(500)]
    print(n, round(statistics.mean(promedios), 1), round(statistics.stdev(promedios), 1))
```

```salida
3 321.9 93.3
9 319.7 32.9
```

(La línea `[... for _ in range(500)]` es una lista por comprensión, vista en 7.12: construye la lista repitiendo la expresión 500 veces.) Con 500 repeticiones, el promedio de los promedios está cerca de 320 en ambos casos (el muestreo aleatorio no tiene sesgo), pero la **dispersión de los promedios es menor con n = 9** que con n = 3. Más datos aleatorios dan estimaciones más estables. Esa dispersión de los promedios de muestra es el tema central del capítulo 12.

**6. Fuentes de sesgo que verás en la práctica.**

- **Marco incompleto**: encuestar solo a clientes con teléfono.
- **No respuesta**: los clientes molestos no contestan.
- **Muestra voluntaria**: responde quien tiene algo que decir.
- **Escoger «a dedo»**: el vendedor señala sus mejores clientes para una prueba piloto.
- **Período no representativo**: medir solo la semana de fin de mes.

Ejemplo comercial: para evaluar la satisfacción de 1 200 clientes con una encuesta telefónica, se estratifica por ruta y se sortean 30 por ruta. Se registra cuántos no contestaron, porque si los que no contestan son los más molestos, el resultado se vuelve optimista.

## Errores comunes

- **Elegir «los primeros» o «los más fáciles»** y llamarlos aleatorios.
- **Creer que más datos corrigen un sesgo.**
- **No registrar el marco muestral** ni quién quedó fuera.
- **No usar semilla** y no poder repetir el sorteo.
- **Estratificar sin ponderar** cuando los estratos son de tamaño distinto.
- **Ignorar la no respuesta.**
- **Generalizar a una población distinta de la muestreada.**

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre muestreo aleatorio simple y estratificado?
2. ¿Por qué una muestra grande de conveniencia puede ser peor que una pequeña aleatoria?
3. ¿Para qué sirve fijar una semilla?
4. ¿Qué es el error de muestreo y por qué es inevitable?

<details><summary>Respuestas</summary>

1. En el simple se sortea de toda la población; en el estratificado se sortea dentro de cada grupo para asegurar que todos estén representados.
2. Porque el sesgo no desaparece con más datos; la aleatoriedad sí evita el sesgo sistemático.
3. Para que el sorteo sea repetible y verificable.
4. La diferencia entre el estadístico y el parámetro por ver solo una parte; es inevitable porque cada muestra es distinta.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Sortea (semilla 11) una muestra aleatoria simple de 4 tiendas de la población de esta lección y compara su media con 320.
2. Arma una muestra estratificada de 1 tienda por ruta (semilla 11) y compárala con la anterior.
3. Redacta dos frases: una sobre un posible sesgo en «preguntar a los clientes que visitan la oficina» y otra sobre cómo lo corregirías.

Cómo saber que está bien: las medias de las muestras difieren de 320 (error de muestreo); en la 3 mencionas el marco o la no respuesta.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import random
import statistics

poblacion = [320, 150, 410, 90, 560, 220, 180, 730, 260, 140, 300, 480]
azar = random.Random(11)
simple = azar.sample(poblacion, 4)
print(simple, statistics.mean(simple))

estratos = [[320, 150, 410, 90], [560, 220, 180, 730], [260, 140, 300, 480]]
azar = random.Random(11)
una_por_ruta = [azar.choice(grupo) for grupo in estratos]
print(una_por_ruta, statistics.mean(una_por_ruta))
```

```salida
[730, 260, 480, 140] 402.5
[90, 730, 480] 433.3333333333333
```

</details>

## Después, en los ejercicios

Las preguntas de muestreo del caso C03 y de ST04–ST07 en [Estadística](../../03_EJERCICIOS/Estadistica/) piden indicar cómo se escogió la muestra. Si no fue aleatoria, dilo y limita lo que concluyes. Siguiente: [11.9 Descriptiva con Pandas y un informe completo](09_descriptiva_con_pandas.md).
