# 7.2 Variables y asignación

> Tiempo estimado: 45 min (lectura 15 + práctica 30). Prerrequisito: [7.1 Qué es un programa](01_que_es_un_programa.md).

## Para qué sirve

Un programa que solo imprime textos fijos no sirve para analizar datos. Necesitas **guardar valores con un nombre** (la cantidad vendida, el precio, el total) para usarlos después y cambiarlos. Eso es una variable. Entenderla bien evita el error más común del principiante: creer que Python recalcula solo, como una celda de Excel.

## Términos nuevos

- **Variable**: un nombre que apunta a un valor guardado en la memoria. Por ejemplo, el nombre `cantidad` apuntando al valor `3`.
- **Valor**: el dato en sí (el número 3, el texto «Ana»).
- **Asignación**: la instrucción que le da un valor a un nombre. Se escribe con **un solo** signo igual: `cantidad = 3`. Se lee «`cantidad` pasa a valer 3», no «cantidad es igual a 3».
- **Identificador**: el nombre de la variable. Puede tener letras, números y guion bajo, pero no puede empezar con número ni tener espacios.
- **Reasignar**: darle un valor nuevo a un nombre que ya existía. El valor anterior se pierde.
- **Expresión**: una combinación de valores, variables y operadores que Python puede calcular (por ejemplo `cantidad * precio`).
- **snake_case**: la convención de escribir nombres en minúsculas separando palabras con guion bajo: `total_ventas`.

## Ejemplo paso a paso

**1. Crear y usar variables.** Una línea de venta: 3 unidades a Bs 10:

```python
cantidad = 3
precio = 10
total = cantidad * precio
print(total)
```

```salida
30
```

Línea por línea:

1. `cantidad = 3`: Python evalúa el lado derecho (3) y crea el nombre `cantidad` apuntando a ese valor.
2. `precio = 10`: lo mismo con `precio`.
3. `total = cantidad * precio`: **primero** calcula el lado derecho (`3 * 10`, que da 30) y **después** guarda el resultado bajo el nombre `total`.
4. `print(total)` muestra el valor al que apunta `total`.

La regla de oro de la asignación: **primero se calcula el lado derecho, luego se guarda en el nombre de la izquierda**.

**2. Una variable no es una fórmula de Excel.** Cambiamos `cantidad` después de calcular `total`:

```python
cantidad = 3
precio = 10
total = cantidad * precio
cantidad = 5
print(total)
print(cantidad)
```

```salida
30
5
```

`total` sigue valiendo 30. Cuando escribiste `total = cantidad * precio`, Python calculó 30 *en ese momento* y guardó el 30. Cambiar `cantidad` después no recalcula nada. Si quieres un `total` nuevo, tienes que volver a escribir la línea del cálculo.

**3. Reasignar usando el valor anterior.** Una variable que va creciendo:

```python
ventas = 100
ventas = ventas + 50
ventas = ventas + 25
print(ventas)
```

```salida
175
```

`ventas = ventas + 50` no es una ecuación matemática (no tiene sentido que algo sea igual a sí mismo más 50). Es una orden: «toma el valor actual de `ventas` (100), súmale 50 (150) y guarda el resultado de nuevo en `ventas`». Una **tabla de seguimiento** te ayuda a verlo:

| Después de la línea | Valor de `ventas` |
|---|---|
| `ventas = 100` | 100 |
| `ventas = ventas + 50` | 150 |
| `ventas = ventas + 25` | 175 |

Esta idea (una variable que se actualiza usando su valor anterior) es la base del **acumulador** que verás en la lección 7.12.

**4. Un atajo común.** `+=` significa «súmale a la variable»:

```python
ventas = 100
ventas += 50
print(ventas)
```

```salida
150
```

Es lo mismo que `ventas = ventas + 50`. Existen también `-=`, `*=` y `/=`.

**5. Nombres claros.** Compara:

```python
x = 12
y = 8.5
z = x * y
print(z)
```

```salida
102.0
```

```python
unidades = 12
precio_unitario = 8.5
importe = unidades * precio_unitario
print(importe)
```

```salida
102.0
```

Los dos programas hacen exactamente lo mismo, pero solo el segundo se puede leer dentro de un mes. Usa nombres que digan **qué es** el dato (y su unidad, si ayuda: `precio_bs`, `dias_sin_comprar`).

**6. Dos errores clásicos.** Usar un nombre antes de crearlo, o escribirlo distinto:

```python
total_ventas = 500
print(total_venta)
```

```error
NameError: name 'total_venta' is not defined
```

Falta una `s`: `total_venta` es otro nombre, y Python no lo conoce. Mayúsculas y minúsculas también cuentan: `Total` y `total` son nombres diferentes.

```python
precio = 10
precio = precio * 2
print(precio)
```

```salida
20
```

Aquí el segundo valor reemplazó al primero; el 10 ya no existe. Si necesitabas ambos, usa dos nombres (`precio_base`, `precio_final`).

**7. Asignar no es comparar.** En Python, `=` **asigna** y `==` **compara** (lo verás en la lección 7.6). Escribir `cantidad == 3` no cambia `cantidad`: pregunta si vale 3.

Ejemplo comercial: un script de cierre guarda `ventas_entregadas`, `ventas_anuladas` y calcula `pct_anuladas = ventas_anuladas / (ventas_entregadas + ventas_anuladas) * 100`. Cada nombre explica un número del negocio. Si usaras `a`, `b` y `c`, nadie (ni tú) podría revisar la fórmula.

## Errores comunes

- **Creer que la variable se recalcula sola**, como en Excel.
- **Usar `==` donde querías asignar** o `=` donde querías comparar.
- **Nombres con espacios o que empiezan con número**: `mi total`, `2ventas` son errores de sintaxis.
- **Nombres demasiado cortos o genéricos** (`a`, `x1`, `dato`).
- **Reutilizar el mismo nombre para cosas distintas** y perder un valor que necesitabas.
- **Usar como nombre una palabra que Python ya usa** (`print`, `sum`, `list`, `max`): reemplazas la función original y luego falla de formas confusas.
- **Mezclar mayúsculas y minúsculas**: `Cantidad` y `cantidad` son diferentes.

## Para comprobar que entendiste

1. Después de `a = 4` y `b = a + 1` y `a = 10`, ¿cuánto vale `b`?
2. ¿Qué hace Python primero en `total = cantidad * precio`: guardar o calcular?
3. ¿Qué significa `ventas += 20`?
4. ¿`2024_ventas` es un nombre válido?

<details><summary>Respuestas</summary>

1. 5. `b` se calculó cuando `a` valía 4 y no cambia después.
2. Calcula el lado derecho y luego lo guarda.
3. Súmale 20 al valor actual de `ventas` y guarda el resultado.
4. No: no puede empezar con un número.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Crea las variables `unidades = 24` y `precio_unitario = 7.5`, calcula `importe` y muéstralo. Después cambia `unidades` a 30 y muestra `importe`: ¿cambió? Explica por qué.
2. Escribe una tabla de seguimiento para este programa y predice el resultado final antes de ejecutarlo: `saldo = 200`, `saldo = saldo - 50`, `saldo = saldo * 2`, `saldo += 10`.
3. Cambia a nombres claros este fragmento: `a = 5000`, `b = 20`, `c = a * b / 100`.

Cómo saber que está bien: en la 1, el importe es 180,0 y no cambia al modificar `unidades`; en la 2, el resultado es 310.

<details><summary>Comprobación de la parte 2</summary>

```python
saldo = 200
saldo = saldo - 50
saldo = saldo * 2
saldo += 10
print(saldo)
```

```salida
310
```

</details>

## Después, en los ejercicios

Las variables aparecen en cada ejercicio de [Python](../../03_EJERCICIOS/Python/). Cuando uno falle, imprime las variables importantes y compáralas con tu tabla de seguimiento. Siguiente: [7.3 Tipos de datos y aritmética](03_tipos_aritmetica.md).
