# 7.7 Conversiones de tipo y los primeros errores de valor

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [7.3 Tipos](03_tipos_aritmetica.md), [7.5 Texto](05_texto.md) y [7.6 Booleanos y None](06_booleanos_comparaciones_none.md).

## Para qué sirve

Los datos que lees de un archivo llegan como texto: `"12"`, `"8.5"`, `"2026-09-18"`. Para calcular necesitas convertirlos a número. Pero un texto que *parece* un número no siempre se puede convertir (`"11,50"`, `""`, `"N/A"`), y ahí Python se detiene con un error. Esta lección enseña a convertir, a entender por qué falla y a decidir qué hacer con lo que no se puede convertir, que es el corazón de la validación en un ETL.

## Términos nuevos

- **Conversión de tipo** (*cast*): transformar un valor de un tipo a otro, con funciones como `int()`, `float()`, `str()`, `bool()`.
- **Excepción**: un error que Python detecta mientras ejecuta (no al leer el código) y que detiene el programa si nadie lo atiende. Tiene un *tipo* (`ValueError`, `TypeError`, `ZeroDivisionError`...) y un mensaje. El traceback que viste en 7.1 es el informe de una excepción.
- **`ValueError`**: la excepción que significa «el tipo es correcto, pero el valor no sirve». `int("abc")` es un caso.
- **Truncar**: descartar los decimales sin redondear. `int(3.9)` da 3, no 4.
- **Validación**: comprobar que un dato cumple las reglas antes de usarlo.
- **Dato inválido**: un valor que no cumple el formato esperado (texto donde iría un número).
- **`Decimal`**: un tipo del módulo estándar `decimal` que guarda números decimales **de forma exacta** (a diferencia de `float`). Se crea desde un **texto**: `Decimal("0.1")`.
- **Parte entera**: el número sin sus decimales (la parte entera de 2,5 es 2).

## Ejemplo paso a paso

**1. Las cuatro conversiones básicas.**

```python
print(int("12"))
print(float("8.5"))
print(str(250))
print(int(7.9))
print(float(3))
```

```salida
12
8.5
250
7
3.0
```

- `int("12")` convierte el texto en el entero 12.
- `float("8.5")` convierte a decimal.
- `str(250)` convierte el número en el texto `"250"`.
- `int(7.9)` da 7: **trunca**, no redondea. Si necesitas redondear, usa `round(7.9)`.
- `float(3)` da `3.0`.

**2. Convertir para poder calcular.** Un monto leído de un archivo:

```python
monto_texto = "250"
cantidad = 4
print(monto_texto * cantidad)
print(int(monto_texto) * cantidad)
```

```salida
250250250250
1000
```

Sin convertir, `"250" * 4` **repite** el texto cuatro veces. Después de convertir, la multiplicación es la que querías. Este es exactamente el error silencioso de sumar montos «que parecen números» sin convertirlos.

**3. Cuando la conversión falla: `ValueError`.**

```python
print(int("12.5"))
```

```error
ValueError: invalid literal for int() with base 10: '12.5'
```

`int("12.5")` falla: el texto tiene un punto decimal y `int` solo acepta enteros. Tres formas de resolverlo según lo que necesites: `float("12.5")` si quieres el decimal, `int(float("12.5"))` si quieres truncar, o `round(float("12.5"))` si quieres redondear. Otros textos que fallan:

```python
print(float("11,50"))
```

```error
ValueError: could not convert string to float: '11,50'
```

La coma decimal no es válida para Python. Hay que preparar el texto antes: `float("11,50".replace(",", "."))`.

```python
print(int(""))
```

```error
ValueError: invalid literal for int() with base 10: ''
```

Un texto vacío tampoco se puede convertir. En un archivo real, los campos vacíos son frecuentes: debes decidir qué hacer con ellos antes de convertir.

**4. Los espacios sí se toleran, la basura no.**

```python
print(int(" 12 "))
print(float("  8.5\n"))
```

```salida
12
8.5
```

`int` y `float` ignoran los espacios y saltos de línea en los extremos. Pero no toleran miles ni símbolos: `"1,200"`, `"Bs 50"` o `"50%"` fallan.

**5. `None` no se puede convertir.**

```python
print(int(None))
```

```error
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

El tipo de error es `TypeError`: aquí el problema no es el *valor* sino el *tipo*, porque `None` no es texto ni número.

**6. Un patrón seguro de conversión.** Reglas explícitas en lugar de suponer:

```python
def a_numero(texto):
    limpio = texto.strip().replace(",", ".")
    if limpio == "":
        return None
    return float(limpio)


print(a_numero(" 11,50 "))
print(a_numero(""))
print(a_numero("8"))
```

```salida
11.5
None
8.0
```

La función limpia el texto, **decide** qué hacer con el vacío (devolver `None` para indicar «sin dato») y convierte. Las decisiones están escritas: nadie tiene que adivinar qué pasa con un campo vacío. Lo que sigue (qué hacer con `"N/A"`) se resuelve con `try/except`, en la lección 8.5.

**7. Conversión a booleano y a texto.**

```python
print(bool(0), bool(5))
print(str(True) + "!")
print("Total: " + str(1234.5))
```

```salida
False True
True!
Total: 1234.5
```

Para unir un número con un texto con `+` hay que convertir el número con `str()`. Con f-strings (7.5) no hace falta.

**8. `Decimal`: convertir sin perder exactitud.** Los `float` guardan los decimales de forma aproximada (lección 7.3). Para dinero y cantidades que deben validarse con exactitud se usa `Decimal`, siempre **desde un texto**:

```python
from decimal import Decimal

print(0.1 + 0.2)
print(Decimal("0.1") + Decimal("0.2"))
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

cantidad = Decimal("2.5")
print(cantidad == cantidad.to_integral_value())
print(Decimal("3") == Decimal("3").to_integral_value())
print(int(float("2.5")))
```

```salida
0.30000000000000004
0.3
True
False
True
2
```

- `Decimal("0.1") + Decimal("0.2")` da exactamente `0.3`, y la comparación es verdadera (con `float` no lo era).
- Para saber si una cantidad es **entera**, compárala con su parte entera: `cantidad == cantidad.to_integral_value()`. Con `2.5` da `False` (hay una fracción) y con `3` da `True`.
- La última línea muestra el peligro: `int(float("2.5"))` **trunca en silencio** a 2 y nadie se entera de que se perdió medio. Si la regla dice que las unidades deben ser enteras, el `2.5` debe **rechazarse**, no truncarse.
- `Decimal(0.1)` (desde un `float`, sin comillas) hereda la imprecisión del `float`; por eso se pasa el texto.

Ejemplo comercial: la columna `monto` de un CSV trae `"1500.50"`, `""`, `"abc"` y `"2,000"`. Convertirlas a `float` de golpe detiene el programa en el primer valor inválido. La estrategia profesional es separar: los que se pueden convertir siguen, los que no se envían a una lista de **rechazados** con el motivo (así lo harás en el ETL).

## Errores comunes

- **No convertir y calcular con texto**: `"250" * 4` no da 1000.
- **`int()` de un texto con decimales** (`int("12.5")`).
- **Creer que `int(7.9)` redondea**: trunca.
- **Convertir con `float("11,50")`** sin cambiar la coma.
- **Convertir un campo vacío** sin haber decidido qué significa.
- **Ignorar el tipo de error**: `ValueError` (valor malo) y `TypeError` (tipo malo) apuntan a causas distintas.
- **Convertir todo de golpe y dejar que el programa muera** en la primera fila mala sin saber cuál era.

## Para comprobar que entendiste

1. ¿Qué devuelve `int(9.99)`? ¿Y `round(9.99)`?
2. ¿Por qué `float("1,5")` falla?
3. ¿Qué diferencia hay entre `ValueError` y `TypeError`?
4. ¿Qué devuelve `"7" + "3"`? ¿Y `int("7") + int("3")`?

<details><summary>Respuestas</summary>

1. `9` y `10`.
2. Porque Python solo acepta el punto como separador decimal.
3. `ValueError`: el tipo es aceptable pero el valor no sirve; `TypeError`: el tipo no es adecuado.
4. `"73"` (concatena) y `10`.

</details>

## Micropráctica

1. Convierte `"1.250,75"` (formato con punto de miles y coma decimal) a un número decimal y muéstralo. Pista: dos reemplazos.
2. Escribe `def a_entero(texto)` que limpie espacios, devuelva `None` si el texto está vacío y, si no, el entero. Pruébala con `" 15 "`, `""` y `"7"`.
3. Provoca (y lee) un `ValueError` con `int("tres")` y anota las dos partes de la última línea.

Cómo saber que está bien: en la 1 el resultado es `1250.75`; en la 2 las tres pruebas dan `15`, `None` y `7`.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
print(float("1.250,75".replace(".", "").replace(",", ".")))


def a_entero(texto):
    limpio = texto.strip()
    if limpio == "":
        return None
    return int(limpio)


print(a_entero(" 15 "), a_entero(""), a_entero("7"))
```

```salida
1250.75
15 None 7
```

</details>

## Después, en los ejercicios

Las conversiones son el núcleo de P09 y P11 en [Python](../../03_EJERCICIOS/Python/). Fíjate en lo que el enunciado pide hacer con valores inválidos: devolver `None`, lanzar un error o rechazarlos. Siguiente: [7.8 Listas, tuplas, índices y rebanadas](08_listas_tuplas.md).
