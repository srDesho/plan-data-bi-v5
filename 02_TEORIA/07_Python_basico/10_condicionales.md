# 7.10 Condicionales: if, elif y else

> Tiempo estimado: 57 min (lectura 27 + práctica 30). Prerrequisito: [7.6 Booleanos y comparaciones](06_booleanos_comparaciones_none.md).

<!-- TEORIA:PREPARACION:INICIO -->
<a id="preparacion-p02"></a>
## Base inicial de condicionales · 7 min

Una comparación produce `True` o `False`; `if` usa ese resultado para decidir **qué instrucciones ejecutar**. No basta con calcular una comparación si después ejecutas siempre la misma operación.

```python
def aviso_stock(unidades):
    if unidades < 0:
        return None
    return unidades + 2
```

Los dos puntos abren el bloque de la condición y su sangría indica qué pertenece a él. Con -1, la condición es verdadera: se devuelve `None` y termina la función. Con 3, se salta ese bloque y se devuelve 5. La última línea tiene la sangría de la función, no la del `if`: se alcanza únicamente si la llamada no terminó antes. `None` significa que no se publica un valor calculable; no equivale a 0.

Predice las llamadas con 0 y -2: devuelven 2 y `None`. Comprueba el recorrido, no solo la salida. Es un ejemplo de stock; decide tú qué condición y operación corresponden al ejercicio. En aritmética, `/` produce un decimal y no admite denominador cero: la decisión que impida una operación inválida debe ocurrir **antes** de realizarla.

Se conserva antes de P02 en BASE y REDUCIDO. Completa primero las comparaciones y `None` de 7.6; si no cabe, pospón la entrega y recupera la base antes de D03/H01/S01. El desarrollo completo de esta lección permanece en D04 para ampliar `if/elif/else`.

El encabezado de esta lección incluye esta sección de 7 min. Si ya la estudiaste en D02, quedan 20 min de lectura del desarrollo; no vuelvas a sumar esta sección. La práctica de 30 min se contabiliza por separado según la guía.
<!-- TEORIA:PREPARACION:FIN -->

<a id="desarrollo"></a>

## Para qué sirve

Hasta ahora todas las instrucciones se ejecutaban siempre. Los programas útiles **deciden**: si la venta está anulada, no la sumes; si el stock es bajo, avisa; si el dato es inválido, recházalo. Un condicional ejecuta un bloque de instrucciones solo cuando se cumple una condición. Es la versión en Python del `CASE WHEN` de SQL.

## Términos nuevos

- **Condicional**: una estructura que ejecuta ciertas instrucciones solo si una condición es verdadera.
- **`if`**: «si» la condición es verdadera, ejecuta su bloque.
- **`elif`** (*else if*): «si no, pero si» esta otra condición es verdadera. Se evalúa solo si las anteriores fueron falsas.
- **`else`**: «en cualquier otro caso». No lleva condición.
- **Bloque**: las líneas con sangría debajo de `if`, `elif` o `else`. Termina cuando la sangría vuelve a la izquierda.
- **Rama**: cada camino posible de un condicional.
- **Caso límite**: un valor justo en el borde de una condición (por ejemplo, un monto exactamente igual al umbral).

## Ejemplo paso a paso

**1. Un `if` simple.**

```python
stock = 4

if stock < 10:
    print("Stock bajo: reponer")

print("Fin de la revisión")
```

```salida
Stock bajo: reponer
Fin de la revisión
```

Línea por línea:

1. `if stock < 10:` evalúa la condición `stock < 10` (con `stock = 4`, es `True`). **Los dos puntos** del final son obligatorios.
2. `print("Stock bajo: reponer")` está indentada (4 espacios): pertenece al `if` y solo se ejecuta si la condición es verdadera.
3. La última línea no tiene sangría: está fuera del `if` y se ejecuta **siempre**.

Cambia `stock` a 25 y la primera frase ya no aparece, pero «Fin de la revisión» sí.

**2. `if` con `else`.**

```python
monto = 80

if monto >= 100:
    print("Venta grande")
else:
    print("Venta normal")
```

```salida
Venta normal
```

Exactamente **una** de las dos ramas se ejecuta: nunca las dos, nunca ninguna.

**3. Varias condiciones con `elif`.** Clasificar un nivel de stock:

```python
stock = 15

if stock < 10:
    nivel = "bajo"
elif stock < 30:
    nivel = "medio"
else:
    nivel = "alto"

print(nivel)
```

```salida
medio
```

Python revisa de arriba hacia abajo y **se detiene en la primera condición verdadera**. Con `stock = 15`: `15 < 10` es falso; `15 < 30` es verdadero → `nivel = "medio"`, y no mira el `else`. Por eso el orden importa: la segunda condición solo se evalúa si la primera fue falsa, así que ya sabemos que `stock` es 10 o más, y basta con preguntar `< 30`.

Tabla de seguimiento para tres valores:

| `stock` | `stock < 10` | `stock < 30` | `nivel` |
|---|---|---|---|
| 4 | verdadero | no se evalúa | bajo |
| 15 | falso | verdadero | medio |
| 30 | falso | falso | alto |

El 30 es un **caso límite**: no es menor que 30, así que cae en `else`. Si el negocio quisiera que 30 fuera «medio», habría que escribir `<= 30`. Las decisiones de borde se escriben, se prueban y se anotan.

**4. Combinar condiciones.**

```python
estado = "entregado"
monto = 500

if estado == "entregado" and monto > 0:
    print("Cuenta para el total")
else:
    print("No cuenta")
```

```salida
Cuenta para el total
```

**5. El tercer caso: el dato inválido.** Un error clásico es tener solo dos ramas cuando el dato puede traer una tercera cosa:

```python
estado = "pendiente"

if estado == "entregado":
    print("cuenta")
elif estado == "anulado":
    print("no cuenta")
else:
    print("estado desconocido: revisar")
```

```salida
estado desconocido: revisar
```

Con `if/else` solo, un estado inesperado como `"pendiente"` o `"Entregado "` (con mayúscula y espacio) caería silenciosamente en la rama equivocada. Con `elif` + `else` el caso desconocido se detecta y se marca para revisión en lugar de convertirse en «entregado» o «anulado» sin avisar. **Nunca conviertas en silencio un valor desconocido en uno válido.**

**6. Condicionales dentro de funciones.** Lo habitual es poner la decisión en una función que devuelve la clasificación:

```python
def nivel_de_stock(stock):
    if stock < 10:
        return "bajo"
    elif stock < 30:
        return "medio"
    return "alto"


print(nivel_de_stock(4), nivel_de_stock(15), nivel_de_stock(30))
```

```salida
bajo medio alto
```

Como `return` termina la función, no hace falta el `else`: si ninguna de las condiciones anteriores se cumplió, la ejecución llega a `return "alto"`. Este estilo (retornos tempranos) es muy común.

**7. Errores de sangría.** La sangría es parte de la sintaxis:

```python
stock = 4
if stock < 10:
print("bajo")
```

```error
IndentationError: expected an indented block after 'if' statement on line 2
```

Python avisa: después del `if` esperaba un bloque con sangría. Usa siempre 4 espacios y no mezcles tabuladores con espacios.

Ejemplo comercial: la regla «descuento del 5 % si la compra supera Bs 500, 10 % si supera Bs 1000, nada en otro caso» son dos `elif`/`if` ordenados **de la condición más exigente a la menos**: primero `> 1000`, luego `> 500`. Si pones `> 500` primero, una compra de 1200 recibiría el 5 %.

## Errores comunes

- **Olvidar los dos puntos** después de la condición.
- **Sangría incorrecta**: `IndentationError`.
- **Usar `=` en lugar de `==`** dentro de un `if`: `SyntaxError`.
- **Ordenar mal las condiciones** de un `elif` (de menos a más exigente).
- **No cubrir el caso desconocido** y clasificarlo mal sin avisar.
- **Olvidar los casos límite** (`<` contra `<=`).
- **Varios `if` seguidos en lugar de `elif`**: se evalúan todos y varios bloques pueden ejecutarse.

## Para comprobar que entendiste

1. En un `if/elif/else`, ¿cuántos bloques se ejecutan como máximo?
2. ¿Qué imprime `if 7 > 5: print("A")` seguido de `if 7 > 6: print("B")`? ¿Y con `elif` en el segundo?
3. ¿Qué pasa si una condición en `elif` es verdadera pero la del `if` anterior también lo era?
4. ¿Por qué es importante el `else` final al validar estados?

<details><summary>Respuestas</summary>

1. Uno.
2. Con dos `if` separados imprime `A` y `B`; con `elif`, solo `A`.
3. El `elif` no se evalúa: gana la primera condición verdadera.
4. Para detectar valores inesperados en lugar de clasificarlos mal en silencio.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe una función `etiqueta_cumplimiento(pct)` que devuelva `"cumple"` si `pct >= 90`, `"parcial"` si `pct >= 70` y `"no cumple"` en otro caso. Prueba con 95, 90, 89.9, 70 y 10 y anota el resultado de cada uno antes de ejecutar.
2. Escribe un programa que, dado `estado`, imprima `"suma"`, `"no suma"` o `"revisar"`. Pruébalo con `"entregado"`, `"anulado"`, `"ENTREGADO "` y `""`. ¿Qué resultado dan los dos últimos? ¿Es lo que querías? Mejora el programa para que `"ENTREGADO "` sí cuente como entregado limpiando antes de comparar.
3. Predice: `x = 12`; `if x > 10: print("A")`, `elif x > 5: print("B")`, `else: print("C")`.

Cómo saber que está bien: en la 1 los resultados son cumple, cumple, parcial, parcial, no cumple; en la 2, con una rama para `"entregado"`, otra para `"anulado"` y `revisar` para todo lo demás, las cuatro pruebas dan suma, no suma, revisar y revisar, y tras limpiar antes de comparar `"ENTREGADO "` pasa a suma mientras `""` sigue en revisar; en la 3 solo se imprime `A`.

<details><summary>Comprobación de la parte 1</summary>

```python
def etiqueta_cumplimiento(pct):
    if pct >= 90:
        return "cumple"
    elif pct >= 70:
        return "parcial"
    return "no cumple"


print(95, etiqueta_cumplimiento(95))
print(90, etiqueta_cumplimiento(90))
print(89.9, etiqueta_cumplimiento(89.9))
print(70, etiqueta_cumplimiento(70))
print(10, etiqueta_cumplimiento(10))
```

```salida
95 cumple
90 cumple
89.9 parcial
70 parcial
10 no cumple
```

Observa los dos casos de borde: 90 y 70 cumplen con `>=`, por eso quedan en la categoría de arriba.

</details>

## Después, en los ejercicios

Los condicionales son el núcleo de P08 y de la validación de P09–P12 en [Python](../../03_EJERCICIOS/Python/). Siguiente: [7.11 Repetir: for y while](11_for_while.md).
