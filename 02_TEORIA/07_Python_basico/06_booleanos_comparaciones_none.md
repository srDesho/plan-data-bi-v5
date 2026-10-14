# 7.6 Booleanos, comparaciones y None

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: [7.3 Tipos de datos](03_tipos_aritmetica.md) y [7.5 Texto](05_texto.md).

## Para qué sirve

Un programa que decide («si la venta está anulada, no la sumes») necesita hacerse preguntas cuya respuesta sea verdadera o falsa. Esas preguntas son las comparaciones, y su respuesta es un valor booleano. También necesitas distinguir entre «el valor es cero», «el texto está vacío» y «no hay valor»: tres situaciones que en un reporte significan cosas muy distintas.

## Términos nuevos

- **Booleano** (`bool`): un tipo con solo dos valores: `True` y `False`. Es el resultado de toda comparación.
- **Comparación**: una expresión que compara dos valores y devuelve un booleano.
- **Operador de comparación**: `==` (igual), `!=` (distinto), `<`, `>`, `<=`, `>=`.
- **Operador lógico**: `and` (ambas verdaderas), `or` (al menos una verdadera), `not` (invierte).
- **`None`**: el valor que representa «no hay valor» o «sin dato». No es cero, ni texto vacío, ni `False`.
- **Valor falso** (*falsy*): un valor que, usado como condición, Python trata como falso: `False`, `None`, `0`, `0.0`, `""` (texto vacío) y las colecciones vacías. Cualquier otro valor se trata como verdadero.
- **`is`**: el operador para preguntar si algo es exactamente `None`: `x is None`.

## Ejemplo paso a paso

**1. Asignar no es comparar.** Hasta ahora usaste `=` para guardar. Para comparar se usa `==` (dos signos):

```python
cantidad = 5
print(cantidad == 5)
print(cantidad == 6)
print(cantidad != 6)
print(cantidad > 3)
print(cantidad <= 4)
```

```salida
True
False
True
True
False
```

Cada línea hace una pregunta y `print` muestra la respuesta: `True` o `False`. La primera línea (`=`) **cambió** la variable; las demás (`==`, `!=`, `>`, `<=`) solo **preguntan** y no cambian nada. Escribir `if cantidad = 5:` es un error de sintaxis precisamente por eso.

**2. Comparar textos.** Distingue mayúsculas, minúsculas y espacios:

```python
estado = "entregado"
print(estado == "entregado")
print(estado == "Entregado")
print("entregado " == estado)
print(estado.strip().lower() == "entregado")
```

```salida
True
False
False
True
```

Un espacio de más o una mayúscula hacen que dos textos sean distintos. Normaliza con `strip()` y `lower()` **antes** de comparar si los datos pueden venir sucios.

**3. Combinar condiciones con `and`, `or`, `not`.**

```python
monto = 600
estado = "entregado"
print(monto > 500 and estado == "entregado")
print(monto > 500 and estado == "anulado")
print(monto > 500 or estado == "anulado")
print(not estado == "anulado")
```

```salida
True
False
True
True
```

- `and`: verdadero solo si **las dos** lo son.
- `or`: verdadero si **al menos una** lo es.
- `not`: invierte el resultado.

La tabla completa para dos condiciones A y B:

| A | B | A and B | A or B |
|---|---|---|---|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

Igual que en SQL, `and` se resuelve antes que `or`; usa paréntesis cuando los mezcles.

**4. Comparación encadenada.** Python permite escribir un rango de forma natural:

```python
descuento = 12
print(0 <= descuento <= 100)
print(0 <= descuento <= 10)
```

```salida
True
False
```

**5. Los booleanos se comportan como 1 y 0.** Esto permite contar sumando:

```python
print(True + True + False)
total_cumplidas = True + False + True + True
print(total_cumplidas)
```

```salida
2
3
```

Cada `True` vale 1 y cada `False` vale 0. Una suma de booleanos cuenta cuántas veces se cumplió algo: es el truco que luego usarás con listas (lección 7.12) y con Pandas para contar filas que cumplen una condición.

**6. `None`: la ausencia de valor.**

```python
zona = None
print(zona is None)
print(zona == 0)
print(zona == "")
print(type(zona))
```

```salida
True
False
False
<class 'NoneType'>
```

`None` no es igual a `0` ni a `""`: es otra cosa. Para preguntar si algo es `None`, usa `is None` (o `is not None`). `None` es el equivalente en Python del `NULL` de SQL y de la celda vacía de un registro sin dato.

**7. Qué cuenta como falso en un `if`.** Usa `bool(valor)` para ver cómo trata Python cada valor:

```python
print(bool(0), bool(0.0), bool(""), bool(None), bool(False))
print(bool(1), bool("texto"), bool(" "))
```

```salida
False False False False False
True True True
```

La primera línea muestra valores falsos y la segunda valores verdaderos. `0`, `0.0`, `""`, `None` y `False` son falsos; `1`, `"texto"` y hasta `" "` (un espacio) son verdaderos. La trampa: un `if monto:` es falso cuando `monto` vale `0` **y** cuando es `None`, pero esas dos situaciones no significan lo mismo en el negocio (una venta de cero Bs frente a una venta sin monto registrado). Cuando importe la diferencia, pregunta explícitamente: `if monto is None:`.

Ejemplo comercial: «el cliente es válido si tiene ruta y no está anulado» se escribe `ruta is not None and estado != "anulado"`. Cada condición responde una pregunta concreta; unidas con `and` forman la regla.

## Errores comunes

- **Usar `=` donde querías `==`.**
- **Comparar con `None` usando `==`** en lugar de `is None`. Funciona casi siempre, pero `is` es la forma correcta.
- **Confundir `0`, `""` y `None`** en un `if`.
- **Olvidar que `"Entregado" != "entregado"`.**
- **Mezclar `and` y `or` sin paréntesis.**
- **Escribir `if x == 1 or 2:`** pensando que significa «x es 1 o 2» (la parte `or 2` siempre es verdadera). Lo correcto es `x == 1 or x == 2` o `x in (1, 2)`.
- **Comparar tipos distintos**: `"5" == 5` es `False`.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre `x = 3` y `x == 3`?
2. ¿Cuánto da `True and False or True`? (recuerda la precedencia)
3. ¿Cuándo es falsa la condición `if monto:`?
4. ¿Cómo preguntas correctamente si `zona` es `None`?

<details><summary>Respuestas</summary>

1. La primera asigna el valor 3; la segunda pregunta si `x` vale 3 y devuelve `True` o `False`.
2. `True` (primero `True and False` es `False`; luego `False or True` es `True`).
3. Cuando `monto` es `0`, `0.0`, `None` o un valor vacío.
4. `zona is None`.

</details>

## Micropráctica

Sin ejecutar, predice el resultado. Después ejecuta y compara.

1. `monto = 0` → `print(monto == 0, monto is None, bool(monto))`
2. `ruta = "r01"` → `print(ruta == "R01", ruta.upper() == "R01")`
3. `stock = 15` → `print(10 <= stock <= 20, stock < 10 or stock > 20)`
4. Escribe una expresión que sea verdadera solo cuando `estado` es `"entregado"` y `monto` es mayor que 0.

Cómo saber que está bien: 1 → `True False False`; 2 → `False True`; 3 → `True False`.

<details><summary>Comprobación</summary>

```python
monto = 0
print(monto == 0, monto is None, bool(monto))

ruta = "r01"
print(ruta == "R01", ruta.upper() == "R01")

stock = 15
print(10 <= stock <= 20, stock < 10 or stock > 20)

estado = "entregado"
monto = 120
print(estado == "entregado" and monto > 0)
```

```salida
True False False
False True
True False
True
```

</details>

## Después, en los ejercicios

Las comparaciones y `None` son la base de las condiciones de P08, P09 y P11 en [Python](../../03_EJERCICIOS/Python/). Siguiente: [7.7 Conversiones de tipo y primeros errores de valor](07_conversiones.md).
