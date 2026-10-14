# 7.11 Repetir: for y while

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [7.8 Listas](08_listas_tuplas.md) y [7.10 Condicionales](10_condicionales.md).

## Para qué sirve

Un archivo tiene miles de filas y quieres hacer lo mismo con cada una. Escribir la instrucción miles de veces es imposible. Un **bucle** repite un bloque de instrucciones, y es el mecanismo con el que todo programa de datos recorre filas. En esta lección solo aprendes a **repetir y a recorrer**; la técnica de ir acumulando resultados (sumar, contar) se enseña aparte, en la lección 7.12.

## Términos nuevos

- **Bucle** (*loop*): una estructura que repite un bloque de instrucciones.
- **Iteración**: cada vuelta del bucle. Un bucle que recorre 5 elementos hace 5 iteraciones.
- **`for`**: el bucle que recorre uno por uno los elementos de una secuencia (o de cualquier colección).
- **Variable de bucle**: la variable que en cada iteración toma el valor del elemento actual: en `for x in lista`, `x` es la variable de bucle.
- **`range(n)`**: una forma de generar los números 0, 1, ..., n-1 para repetir algo `n` veces.
- **`while`**: el bucle que repite mientras una condición sea verdadera.
- **Contador**: una variable entera que se actualiza en cada vuelta (`i = i + 1`).
- **Bucle infinito**: un bucle cuya condición nunca se vuelve falsa; el programa no termina.
- **`break` y `continue`**: `break` sale del bucle; `continue` salta a la siguiente iteración.

## Ejemplo paso a paso

**1. Recorrer una lista con `for`.**

```python
rutas = ["R01", "R02", "R03"]

for ruta in rutas:
    print("Procesando", ruta)

print("Terminé")
```

```salida
Procesando R01
Procesando R02
Procesando R03
Terminé
```

Línea por línea:

1. `for ruta in rutas:` significa «para cada elemento de `rutas`, llámalo `ruta` y ejecuta el bloque». Los dos puntos son obligatorios.
2. El bloque indentado se ejecuta **una vez por elemento**: 3 iteraciones.
3. `print("Terminé")` está fuera del bucle (sin sangría): se ejecuta una sola vez al final.

Tabla de seguimiento de las iteraciones:

| Iteración | Valor de `ruta` | Qué se imprime |
|---|---|---|
| 1 | `"R01"` | Procesando R01 |
| 2 | `"R02"` | Procesando R02 |
| 3 | `"R03"` | Procesando R03 |

**2. Hacer algo con cada elemento.**

```python
precios = [6.0, 9.0, 11.5]

for precio in precios:
    con_descuento = precio * 0.9
    print(precio, "->", con_descuento)
```

```salida
6.0 -> 5.4
9.0 -> 8.1
11.5 -> 10.35
```

Dentro del bloque puedes escribir varias instrucciones. En cada iteración `precio` vale un elemento distinto y `con_descuento` se recalcula. Cuidado: `con_descuento` queda con el valor de la **última** iteración al terminar el bucle; los resultados anteriores se perdieron salvo que los guardes (eso es lo que hacen los acumuladores en 7.12).

**3. `range`: repetir un número de veces.**

```python
for i in range(3):
    print("vuelta", i)

for i in range(1, 4):
    print("número", i)
```

```salida
vuelta 0
vuelta 1
vuelta 2
número 1
número 2
número 3
```

`range(3)` genera 0, 1, 2 (empieza en 0 y **no incluye** el 3). `range(1, 4)` genera 1, 2, 3 (incluye el inicio, excluye el fin), igual que las rebanadas.

**4. Recorrer con la posición: `enumerate`.** Cuando necesitas el número de orden además del elemento:

```python
rutas = ["R01", "R02", "R03"]

for posicion, ruta in enumerate(rutas, start=1):
    print(posicion, ruta)
```

```salida
1 R01
2 R02
3 R03
```

`enumerate(rutas, start=1)` entrega pares (posición, elemento) empezando a contar en 1. Evita el feo `rutas[i]` con `range(len(rutas))`.

**5. Recorrer un texto y un diccionario.**

```python
for letra in "R01":
    print(letra)

precios = {"Agua 2L": 6.0, "Jugo 1L": 9.0}
for producto, precio in precios.items():
    print(producto, precio)
```

```salida
R
0
1
Agua 2L 6.0
Jugo 1L 9.0
```

Un texto se recorre carácter por carácter. Un diccionario con `.items()` entrega cada par (clave, valor).

**6. `while`: repetir mientras se cumpla una condición.**

```python
vuelta = 1

while vuelta <= 3:
    print("vuelta", vuelta)
    vuelta = vuelta + 1

print("fin, vuelta vale", vuelta)
```

```salida
vuelta 1
vuelta 2
vuelta 3
fin, vuelta vale 4
```

Cómo funciona: antes de cada iteración Python evalúa `vuelta <= 3`; si es verdadera ejecuta el bloque, y si es falsa sale del bucle. La línea `vuelta = vuelta + 1` es **imprescindible**: sin ella la condición siempre sería verdadera y el bucle no terminaría nunca. Al salir, `vuelta` vale 4.

Tabla de seguimiento:

| Antes de la iteración | `vuelta` | ¿`vuelta <= 3`? | Acción |
|---|---|---|---|
| 1 | 1 | sí | imprime 1; `vuelta` pasa a 2 |
| 2 | 2 | sí | imprime 2; `vuelta` pasa a 3 |
| 3 | 3 | sí | imprime 3; `vuelta` pasa a 4 |
| 4 | 4 | no | sale del bucle |

Usa `for` cuando sabes qué recorrer (lo habitual en datos) y `while` cuando repites hasta que algo ocurra (por ejemplo, reintentar).

**7. `break` y `continue`.**

```python
ventas = [120, 0, 80, 200]

for monto in ventas:
    if monto == 0:
        continue
    if monto > 150:
        print("Primer monto mayor a 150:", monto)
        break
    print("revisado", monto)
```

```salida
revisado 120
revisado 80
Primer monto mayor a 150: 200
```

- `continue` ignora el resto de la iteración actual: el `0` se salta sin imprimirse.
- `break` termina el bucle completo: al encontrar 200 se imprime el aviso y ya no se siguen revisando más elementos (aquí era el último, pero si hubiera más, tampoco se mirarían).

**8. El bucle infinito (y cómo detenerlo).** Si por error olvidas actualizar el contador, el programa no termina. En la terminal se interrumpe con **Ctrl+C**. Como prevención, antes de escribir un `while`, pregúntate: «¿qué línea hará que la condición deje de cumplirse?».

Ejemplo comercial: «para cada archivo de ventas de la carpeta, leerlo y validarlo» es un `for archivo in archivos:`. «Reintentar la conexión hasta 3 veces» es un `while intentos < 3:`.

## Errores comunes

- **Olvidar los dos puntos** o la sangría.
- **Esperar que `range(5)` incluya el 5.**
- **Un `while` sin actualizar la variable de la condición** (bucle infinito).
- **Modificar una lista mientras la recorres** con `for`: produce saltos y omisiones.
- **Usar el nombre de la variable de bucle fuera del bucle** esperando que valga lo mismo en todas partes: vale lo de la última iteración.
- **Escribir `for i in len(lista)`**: `len` devuelve un número, no una secuencia; usa `range(len(lista))` o, mejor, recorre la lista directamente.
- **Poner dentro del bucle algo que debía ejecutarse una sola vez** (como un `print` final).

## Para comprobar que entendiste

1. ¿Cuántas iteraciones hace `for x in [5, 6, 7, 8]`?
2. ¿Qué números genera `range(2, 5)`?
3. ¿Cuándo termina un `while`?
4. ¿Qué diferencia hay entre `break` y `continue`?

<details><summary>Respuestas</summary>

1. 4.
2. 2, 3 y 4.
3. Cuando su condición se evalúa como falsa.
4. `break` sale del bucle; `continue` salta a la siguiente iteración.

</details>

## Micropráctica

1. Imprime los números del 1 al 5 con `for` y `range`, luego del 5 al 1 con `while`.
2. Dada la lista `tiendas = ["La Palma", "El Faro", "Salud"]`, imprime `1. La Palma`, `2. El Faro`, `3. Salud` con `enumerate`.
3. Con `montos = [50, 0, 120, 0, 75]`, imprime solo los montos mayores que cero, saltando los ceros con `continue`.
4. Escribe una tabla de seguimiento (en papel) para un `while` que cuente hacia atrás de 3 a 1.

Cómo saber que está bien: 1 imprime 1 2 3 4 5 y luego 5 4 3 2 1; 3 imprime 50, 120 y 75.

<details><summary>Comprobación de las partes 1 y 3</summary>

```python
for n in range(1, 6):
    print(n, end=" ")
print()

n = 5
while n >= 1:
    print(n, end=" ")
    n = n - 1
print()

montos = [50, 0, 120, 0, 75]
for monto in montos:
    if monto == 0:
        continue
    print(monto)
```

```salida
1 2 3 4 5 
5 4 3 2 1 
50
120
75
```

</details>

## Después, en los ejercicios

Los bucles aparecen desde P05 y P07 en [Python](../../03_EJERCICIOS/Python/). En la próxima lección aprendes la técnica que casi siempre los acompaña: el acumulador. Siguiente: [7.12 Acumuladores y patrones de recorrido](12_acumuladores.md).
