# 7.8 Listas y tuplas: guardar varios valores

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [7.5 Texto](05_texto.md) (índices y rebanadas) y [7.6 Booleanos](06_booleanos_comparaciones_none.md).

## Para qué sirve

Una variable guarda un valor. Pero los datos vienen en conjuntos: las ventas de cada día, los códigos de ruta, las filas de un archivo. Una **lista** guarda varios valores en orden bajo un solo nombre, y es el contenedor más usado de Python. Entenderla bien (índices, rebanadas y, sobre todo, que se puede modificar) evita muchos errores silenciosos.

## Términos nuevos

- **Lista** (`list`): una secuencia ordenada de elementos, escrita entre corchetes: `[10, 20, 30]`. Puede mezclar tipos, aunque normalmente guarda elementos del mismo tipo.
- **Elemento**: cada valor dentro de la lista.
- **Índice** y **rebanada**: ya los conoces con los textos (7.5). Funcionan igual: el primer elemento es el índice 0, y `[a:b]` incluye `a` y excluye `b`.
- **Mutable**: que se puede modificar después de creado. Las listas son mutables: puedes agregar, quitar o cambiar elementos **sin crear una lista nueva**. (Lo opuesto, inmutable, ya lo viste con el texto.)
- **Método de lista**: una función propia de las listas: `append`, `remove`, `sort`...
- **Tupla** (`tuple`): una secuencia ordenada e **inmutable**, escrita entre paréntesis: `(2026, 9, 18)`. Sirve para agrupar valores que van juntos y no deben cambiar.
- **Alias**: dos nombres que apuntan a la **misma** lista. Cambiar una cambia la otra.

## Ejemplo paso a paso

**1. Crear una lista y leer elementos.**

```python
ventas = [120, 80, 200, 150]
print(ventas)
print(len(ventas))
print(ventas[0])
print(ventas[3])
print(ventas[-1])
print(ventas[1:3])
```

```salida
[120, 80, 200, 150]
4
120
150
150
[80, 200]
```

- `len(ventas)` da la cantidad de elementos: 4.
- `ventas[0]` es el primero (120); `ventas[3]` el cuarto (150); `ventas[-1]` el último (150).
- `ventas[1:3]` es la rebanada de los índices 1 y 2: `[80, 200]`.

Pedir un índice que no existe produce un error:

```python
ventas = [120, 80, 200, 150]
print(ventas[4])
```

```error
IndexError: list index out of range
```

Una lista de 4 elementos tiene índices del 0 al 3. El 4 «está fuera de rango».

**2. Resumir con funciones de Python.**

```python
ventas = [120, 80, 200, 150]
print(sum(ventas))
print(min(ventas), max(ventas))
print(sum(ventas) / len(ventas))
print(120 in ventas, 99 in ventas)
```

```salida
550
80 200
137.5
True False
```

`sum` suma todos los elementos, `min` y `max` dan el menor y el mayor, y `in` pregunta si un valor está en la lista. El promedio es la suma entre la cantidad: 550 / 4 = 137,5.

**3. Modificar una lista (porque es mutable).**

```python
rutas = ["R01", "R02"]
rutas.append("R03")
print(rutas)
rutas[0] = "R10"
print(rutas)
rutas.remove("R02")
print(rutas)
ultima = rutas.pop()
print(ultima, rutas)
```

```salida
['R01', 'R02', 'R03']
['R10', 'R02', 'R03']
['R10', 'R03']
R03 ['R10']
```

- `append(x)` agrega `x` **al final**.
- `rutas[0] = "R10"` reemplaza el elemento del índice 0.
- `remove(x)` quita la primera aparición del valor `x`.
- `pop()` quita y **devuelve** el último elemento.

Todos estos métodos **cambian la lista original** y no devuelven una lista nueva. Por eso no se escribe `rutas = rutas.append("R03")`: `append` devuelve `None` y perderías la lista.

**4. Ordenar: dos formas.**

```python
ventas = [120, 80, 200, 150]
ordenada = sorted(ventas)
print(ordenada)
print(ventas)
ventas.sort(reverse=True)
print(ventas)
```

```salida
[80, 120, 150, 200]
[120, 80, 200, 150]
[200, 150, 120, 80]
```

`sorted(ventas)` devuelve una lista **nueva** ordenada y deja la original intacta. `ventas.sort()` ordena la propia lista (y devuelve `None`). `reverse=True` ordena de mayor a menor.

**5. La trampa del alias.** Si «copias» con `=`, no copias: creas un segundo nombre para la misma lista.

```python
original = [1, 2, 3]
copia_mala = original
copia_mala.append(99)
print(original)

original = [1, 2, 3]
copia_buena = original.copy()
copia_buena.append(99)
print(original, copia_buena)
```

```salida
[1, 2, 3, 99]
[1, 2, 3] [1, 2, 3, 99]
```

En la primera parte, `copia_mala` y `original` son dos nombres de la misma lista, así que agregar a una cambia la otra. Con `.copy()` obtienes una lista independiente. Esta trampa es una causa típica de resultados que «cambian solos» cuando una función modifica la lista que recibió.

**6. Tuplas: agrupar sin poder cambiar.**

```python
fecha = (2026, 9, 18)
print(fecha[0], fecha[1], fecha[2])
anio, mes, dia = fecha
print(f"{dia}/{mes}/{anio}")
```

```salida
2026 9 18
18/9/2026
```

Una tupla se lee igual que una lista, pero no se puede modificar:

```python
fecha = (2026, 9, 18)
fecha[1] = 10
```

```error
TypeError: 'tuple' object does not support item assignment
```

La línea `anio, mes, dia = fecha` se llama **desempaquetar**: asigna cada elemento de la tupla a un nombre distinto. Es la forma en que las funciones suelen devolver varios valores a la vez (lección 8.1).

**7. Listas de listas y de tuplas.** Una pequeña tabla como lista de tuplas:

```python
lineas = [("Agua 2L", 10, 6.0), ("Jugo 1L", 6, 9.0)]
print(lineas[0])
print(lineas[1][0])
print(len(lineas))
```

```salida
('Agua 2L', 10, 6.0)
Jugo 1L
2
```

`lineas[0]` es la primera tupla completa; `lineas[1][0]` es el primer elemento de la segunda tupla: «Jugo 1L». Dos corchetes seguidos significan «entra al elemento y luego al elemento de ese elemento». En la lección 7.9 verás una forma mejor de guardar cada fila, con nombres en lugar de posiciones, porque con tuplas hay que recordar qué significa cada posición.

Ejemplo comercial: las ventas diarias de una semana en una lista permiten calcular con `sum`, `min`, `max` y `len` el total, el mejor día, el peor día y el promedio, sin escribir ninguna repetición todavía.

## Errores comunes

- **Contar índices desde 1** o usar `len(lista)` como índice (fuera de rango).
- **`lista = lista.append(x)`**: deja `lista` en `None`.
- **Copiar con `=`** y modificar sin querer la original.
- **Intentar modificar una tupla.**
- **Olvidar que `sort()` cambia la lista** y `sorted()` no.
- **Esperar que `remove` quite todas las apariciones**: quita solo la primera, y falla con `ValueError` si el valor no está.
- **Mezclar tipos** en una misma lista (números y textos) y fallar luego al ordenar o sumar.

## Para comprobar que entendiste

1. ¿Qué devuelve `[5, 6, 7, 8][1:3]`?
2. ¿Por qué `b = a` no copia una lista?
3. ¿Qué diferencia hay entre `sorted(x)` y `x.sort()`?
4. ¿Qué es mutable: una lista, una tupla o ambas?

<details><summary>Respuestas</summary>

1. `[6, 7]`.
2. Porque solo crea un segundo nombre para la misma lista.
3. `sorted(x)` devuelve una lista nueva; `x.sort()` modifica `x` y devuelve `None`.
4. La lista; la tupla es inmutable.

</details>

## Micropráctica

Con `ventas_semana = [310, 0, 275, 410, 360, 295, 0]`:

1. Calcula el total, el promedio, el mejor y el peor día (sin repeticiones).
2. Calcula el promedio de los días **con ventas** (sin los dos ceros) escribiendo la lista de días con ventas a mano; luego explica en una frase por qué cambia el promedio y cuál es más honesto según la pregunta.
3. Muestra los tres primeros y los dos últimos días con rebanadas.
4. Demuestra el problema del alias con una lista de tu elección.

Cómo saber que está bien: total 1650, promedio 235,71 aprox., mejor 410, peor 0.

<details><summary>Comprobación de las partes 1 y 3</summary>

```python
ventas_semana = [310, 0, 275, 410, 360, 295, 0]
print(sum(ventas_semana), round(sum(ventas_semana) / len(ventas_semana), 2))
print(max(ventas_semana), min(ventas_semana))
print(ventas_semana[:3], ventas_semana[-2:])
```

```salida
1650 235.71
410 0
[310, 0, 275] [295, 0]
```

</details>

## Después, en los ejercicios

Listas y tuplas son la base de P05, P06 y P07 en [Python](../../03_EJERCICIOS/Python/). Siguiente: [7.9 Diccionarios y conjuntos](09_diccionarios_sets.md).
