# 7.12 Acumuladores y patrones de recorrido

> Tiempo estimado: 70 min (lectura 28 + práctica 42). Prerrequisitos: [7.2 Variables](02_variables_asignacion.md) (reasignar), [7.10 Condicionales](10_condicionales.md) y [7.11 for y while](11_for_while.md).

## Para qué sirve

Casi todo cálculo sobre datos sigue el mismo esquema: empezar con un valor inicial, recorrer los elementos y **ir actualizando** un resultado: un total, un conteo, un máximo, una lista de los que cumplen algo. Aprenderás cada patrón por separado, con una lista de números sencillos y una tabla de seguimiento. Solo al final los combinarás.

## Términos nuevos

- **Acumulador**: una variable que se crea **antes** del bucle con un valor inicial y se actualiza **dentro** del bucle en cada iteración. Guarda el resultado que se va construyendo.
- **Valor inicial**: el valor con el que arranca el acumulador. Para sumar es `0`; para contar es `0`; para construir una lista es `[]`.
- **Patrón de recorrido**: una receta reutilizable de bucle. Los cuatro de esta lección: **sumar**, **contar**, **buscar el máximo/mínimo** y **filtrar**.
- **Filtrar**: quedarte solo con los elementos que cumplen una condición.
- **Lista por comprensión**: una forma abreviada de construir una lista nueva a partir de otra en una sola línea: `[expresión for elemento in secuencia if condición]`. Es equivalente a un bucle con `append`.
- **Caso vacío**: probar el patrón con una secuencia sin elementos. Un buen patrón se comporta bien incluso con una lista vacía.

## Ejemplo paso a paso

Usamos la lista de ventas de siete días: `[310, 0, 275, 410, 360, 295, 0]`.

**1. Patrón «sumar».** Calcular el total sin usar `sum`:

```python
ventas = [310, 0, 275, 410, 360, 295, 0]

total = 0
for monto in ventas:
    total = total + monto

print(total)
```

```salida
1650
```

Las tres partes del patrón:

1. **Antes del bucle**: `total = 0` (el valor inicial; sumar cero no cambia nada).
2. **Dentro del bucle**: `total = total + monto` actualiza el acumulador con el elemento actual.
3. **Después del bucle**: `print(total)` usa el resultado. Está **fuera** del bucle (sin sangría) porque solo interesa el total final.

Tabla de seguimiento (las primeras tres iteraciones):

| Iteración | `monto` | `total` antes | `total` después |
|---|---|---|---|
| 1 | 310 | 0 | 310 |
| 2 | 0 | 310 | 310 |
| 3 | 275 | 310 | 585 |

Al terminar las siete iteraciones, `total` vale 1650, igual que `sum(ventas)`. **Comprueba siempre tu bucle contra una cuenta hecha a mano o contra `sum`**.

**2. Patrón «contar».** Cuántos días tuvieron ventas (monto mayor que cero):

```python
ventas = [310, 0, 275, 410, 360, 295, 0]

dias_con_ventas = 0
for monto in ventas:
    if monto > 0:
        dias_con_ventas = dias_con_ventas + 1

print(dias_con_ventas)
```

```salida
5
```

El acumulador empieza en 0 y **sube de uno en uno solo cuando la condición se cumple**. El `if` va dentro del bucle y la suma dentro del `if`. Si pusieras la suma fuera del `if`, contarías todos los días.

**3. Patrón «máximo».** El mejor día:

```python
ventas = [310, 0, 275, 410, 360, 295, 0]

mejor = ventas[0]
for monto in ventas:
    if monto > mejor:
        mejor = monto

print(mejor)
```

```salida
410
```

El valor inicial es **el primer elemento** (no `0`: si todos los montos fueran negativos, el `0` inicial daría un máximo equivocado). En cada vuelta, si el elemento actual supera al mejor visto hasta ahora, lo reemplaza. Para el mínimo, cambia el `>` por `<`.

**4. Patrón «filtrar» (construir una lista).** Quedarse con los montos mayores que 300:

```python
ventas = [310, 0, 275, 410, 360, 295, 0]

grandes = []
for monto in ventas:
    if monto > 300:
        grandes.append(monto)

print(grandes)
```

```salida
[310, 410, 360]
```

Aquí el acumulador es una **lista vacía** (`[]`), y en lugar de sumar, `append` agrega los elementos que cumplen la condición. Resultado: `[310, 410, 360]`.

**5. Combinar patrones: sumar solo lo que cumple.** Total de los días que superaron 300:

```python
ventas = [310, 0, 275, 410, 360, 295, 0]

total_grandes = 0
for monto in ventas:
    if monto > 300:
        total_grandes = total_grandes + monto

print(total_grandes)
```

```salida
1080
```

Es la combinación de «filtrar» (`if`) y «sumar» (acumulador): 310 + 410 + 360 = 1080. Con esta forma resuelves la pregunta de negocio «¿cuánto vendí solo en los días buenos?».

**6. Varios acumuladores a la vez.** Un mismo recorrido puede actualizar varios resultados:

```python
ventas = [310, 0, 275, 410, 360, 295, 0]

total = 0
cantidad = 0
for monto in ventas:
    total = total + monto
    cantidad = cantidad + 1

promedio = total / cantidad
print(total, cantidad, round(promedio, 2))
```

```salida
1650 7 235.71
```

El promedio es el total entre la cantidad. Se calcula **después** del bucle. Si la lista estuviera vacía, `cantidad` sería 0 y la división daría `ZeroDivisionError`: este es el **caso vacío** que tienes que prever.

**7. Probar el caso vacío.**

```python
def promedio(valores):
    total = 0
    cantidad = 0
    for v in valores:
        total = total + v
        cantidad = cantidad + 1
    if cantidad == 0:
        return None
    return total / cantidad


print(promedio([10, 20, 30]))
print(promedio([]))
```

```salida
20.0
None
```

Con una lista vacía la función devuelve `None` («no se puede calcular») en lugar de romperse. Es la misma idea del `NULLIF` de SQL en el denominador.

**8. El acumulador mal colocado.** El error número uno es inicializar dentro del bucle:

```python
ventas = [310, 0, 275]

for monto in ventas:
    total = 0
    total = total + monto

print(total)
```

```salida
275
```

Imprime 275, no 585: en cada vuelta `total = 0` borra lo acumulado. **El valor inicial va siempre antes del bucle.**

**9. Un atajo: la lista por comprensión.** Los patrones «transformar cada elemento» y «filtrar» son tan frecuentes que Python tiene una forma corta para construir una lista nueva:

```python
unidades = [12, 5, 0, 8, 20, 0, 3]

dobles = [u * 2 for u in unidades]
mayores = [u for u in unidades if u > 7]

print(dobles)
print(mayores)
```

```salida
[24, 10, 0, 16, 40, 0, 6]
[12, 8, 20]
```

Se lee de izquierda a derecha: `[u * 2 for u in unidades]` significa «para cada `u` de `unidades`, el valor `u * 2`»; con `if u > 7` al final, solo para los que cumplen. Es **exactamente** lo mismo que el bucle con `append` del ejemplo 4:

```python
unidades = [12, 5, 0, 8, 20, 0, 3]

mayores = []
for u in unidades:
    if u > 7:
        mayores.append(u)
print(mayores)
```

```salida
[12, 8, 20]
```

Úsala cuando la transformación o el filtro cabe en una línea clara; si necesitas varias instrucciones, un acumulador o mucha lógica, escribe el bucle completo, que es más fácil de leer y de depurar. Verás esta forma en lecciones posteriores.

Ejemplo comercial: «cuántas ventas anuladas hubo» (contar), «cuánto vendí en entregadas» (sumar con condición), «cuál fue la venta más alta» (máximo) y «cuáles superaron la meta» (filtrar) son los cuatro patrones, y casi todo reporte inicial se arma con ellos.

## Errores comunes

- **Inicializar el acumulador dentro del bucle.**
- **Poner el `print` del resultado dentro del bucle** (imprime resultados parciales).
- **Usar `0` como valor inicial de un máximo** en datos que pueden ser negativos.
- **Olvidar el `if`** y sumar o contar todo.
- **Dividir entre la cantidad sin prever la lista vacía.**
- **Escribir `total + monto` sin asignar** (`total = total + monto`): no cambia nada.
- **No comprobar el resultado contra una cuenta a mano.**

## Para comprobar que entendiste

1. ¿Cuál es el valor inicial de un acumulador de conteo?
2. ¿Por qué el máximo se inicializa con el primer elemento y no con 0?
3. ¿Dónde va la línea `print(total)`: dentro o fuera del bucle?
4. ¿Qué devuelve el patrón de promedio con una lista vacía si no lo proteges?

<details><summary>Respuestas</summary>

1. 0.
2. Porque con datos negativos el 0 inicial sería mayor que todos y daría un máximo falso.
3. Fuera, después del bucle, para imprimir solo el resultado final.
4. Un `ZeroDivisionError`.

</details>

<a id="micropractica"></a>

## Micropráctica

Con la lista `unidades = [12, 5, 0, 8, 20, 0, 3]`, escribe cada patrón por separado y comprueba a mano:

1. Total de unidades (deben ser 48).
2. Cuántos elementos son mayores que cero (deben ser 5).
3. El valor mínimo entre los elementos mayores que cero (debe ser 3). Pista: filtra primero y luego busca el mínimo, o actualiza el mínimo solo si el elemento es mayor que cero.
4. La lista de los elementos mayores que 7.
5. Combina: el total de las unidades de los elementos mayores que 7.

Cómo saber que está bien: 48, 5, 3, `[12, 8, 20]`, 40.

<details><summary>Comprobación</summary>

```python
unidades = [12, 5, 0, 8, 20, 0, 3]

total = 0
for u in unidades:
    total = total + u
print(total)

positivos = 0
for u in unidades:
    if u > 0:
        positivos = positivos + 1
print(positivos)

mayores = []
for u in unidades:
    if u > 7:
        mayores.append(u)
print(mayores)

suma_mayores = 0
for u in unidades:
    if u > 7:
        suma_mayores = suma_mayores + u
print(suma_mayores)

minimo_positivo = None
for u in unidades:
    if u > 0 and (minimo_positivo is None or u < minimo_positivo):
        minimo_positivo = u
print(minimo_positivo)
```

```salida
48
5
[12, 8, 20]
40
3
```

</details>

## Después, en los ejercicios

Estos cuatro patrones, usados con condiciones, resuelven buena parte de P05–P08 y P14 en [Python](../../03_EJERCICIOS/Python/). Cuando un bucle te dé un resultado distinto al esperado, escribe la tabla de seguimiento de tres iteraciones. Siguiente: [7.13 Recorrer registros (listas de diccionarios)](13_registros_listas_de_diccionarios.md).
