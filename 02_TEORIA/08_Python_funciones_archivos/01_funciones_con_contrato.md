# 8.1 Funciones con contrato

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [7.4 Tu primera función corta](../07_Python_basico/04_primera_funcion.md) y [7.10 Condicionales](../07_Python_basico/10_condicionales.md).

## Para qué sirve

En la lección 7.4 escribiste funciones que hacían una cuenta. Las funciones de un ETL deben hacer algo más: declarar **qué aceptan**, **qué devuelven** y **qué hacen cuando el dato no sirve**. Esa promesa se llama contrato. Una función con contrato se prueba con facilidad, se reutiliza sin sorpresas y permite aislar un fallo en lugar de buscarlo en cien líneas.

## Términos nuevos

- **Contrato**: la descripción de lo que una función recibe (tipos y valores aceptados), lo que devuelve y qué hace con los casos raros (vacío, cero, texto inválido).
- **Valor por defecto**: un valor que toma un parámetro cuando quien llama no lo da. Se escribe en la definición: `def f(x, decimales=2)`.
- **Argumento por nombre** (*keyword*): un argumento que se escribe como `parametro=valor` en la llamada.
- **Docstring**: el texto entre triples comillas dentro de la función, justo debajo de `def`, que documenta su contrato.
- **Valor centinela**: un valor especial, como `None`, que una función devuelve para señalar «no se puede calcular» sin detener el programa.
- **Tupla de retorno**: cuando una función devuelve varios valores separados por coma, Python los entrega en una tupla que se puede desempaquetar.
- **Efecto secundario**: algo que la función hace además de devolver un valor (imprimir, escribir un archivo, modificar una lista que recibió).
- **Función pura**: una función que solo depende de sus parámetros y solo devuelve un valor, sin efectos secundarios. Es la más fácil de probar.

## Ejemplo paso a paso

**1. Parámetros con valor por defecto.**

```python
def redondear_monto(valor, decimales=2):
    return round(valor, decimales)


print(redondear_monto(3.14159))
print(redondear_monto(3.14159, 3))
print(redondear_monto(3.14159, decimales=0))
```

```salida
3.14
3.142
3.0
```

Si no pasas `decimales`, usa 2. Los parámetros con valor por defecto van **después** de los obligatorios. Cuando el argumento por nombre aclara qué significa un número, úsalo (`decimales=0`).

**2. Un contrato escrito con docstring.** Margen comercial: qué porcentaje del precio de venta es ganancia.

```python
def margen_pct(precio_venta, costo):
    """Margen porcentual sobre el precio de venta.

    Recibe: precio_venta y costo, números (Bs).
    Devuelve: (precio_venta - costo) / precio_venta * 100,
              o None si precio_venta es 0 o negativo.
    """
    if precio_venta <= 0:
        return None
    return (precio_venta - costo) / precio_venta * 100


print(margen_pct(10, 6))
print(margen_pct(0, 5))
print(margen_pct(8, 8))
```

```salida
40.0
None
0.0
```

El docstring dice qué entra, qué sale y qué pasa en el caso raro. El caso `precio_venta <= 0` no se resuelve inventando un 0 %: devuelve `None` (valor centinela) para decir «no se puede calcular», que es distinto de «margen cero». La tercera prueba (`8, 8`) es un caso límite: margen exactamente 0. Python muestra el docstring con `help(margen_pct)`.

**3. Probar el contrato con casos normal, límite e inválido.**

```python
def margen_pct(precio_venta, costo):
    if precio_venta <= 0:
        return None
    return (precio_venta - costo) / precio_venta * 100


assert margen_pct(10, 6) == 40
assert margen_pct(8, 8) == 0
assert margen_pct(0, 5) is None
assert margen_pct(-3, 1) is None
print("el contrato se cumple")
```

```salida
el contrato se cumple
```

Tres tipos de prueba: **normal** (10 y 6 → 40 %), **límite** (costo igual al precio → 0 %) e **inválido** (precio cero o negativo → `None`). Si cambias la función y una prueba falla, lo sabes al instante.

**4. Devolver varios valores.**

```python
def resumir(valores):
    total = 0
    for v in valores:
        total = total + v
    cantidad = len(valores)
    promedio = total / cantidad if cantidad > 0 else None
    return total, cantidad, promedio


total, cantidad, promedio = resumir([10, 20, 30])
print(total, cantidad, promedio)
print(resumir([]))
```

```salida
60 3 20.0
(0, 0, None)
```

`return total, cantidad, promedio` devuelve una **tupla**; al llamar, la desempaquetas en tres variables. Observa la expresión `a if condicion else b`: devuelve `a` si la condición es verdadera y `b` si no. Es un `if` en una línea. Para listas vacías el promedio es `None`, no un error.

**5. Funciones pequeñas que se combinan.** En lugar de una función gigante que lo hace todo, escribe piezas con una sola responsabilidad:

```python
def limpiar_codigo(texto):
    return texto.strip().upper()


def es_ruta_valida(codigo):
    return len(codigo) == 3 and codigo[0] == "R" and codigo[1:].isdigit()


def validar_ruta(texto):
    codigo = limpiar_codigo(texto)
    if es_ruta_valida(codigo):
        return codigo
    return None


print(validar_ruta(" r02 "))
print(validar_ruta("R2"))
print(validar_ruta("X01"))
```

```salida
R02
None
None
```

`limpiar_codigo` solo limpia; `es_ruta_valida` solo decide; `validar_ruta` las combina. Si una ruta válida se rechaza, sabes exactamente dónde mirar. Este principio (separar **extraer**, **transformar** y **cargar**) es el que sostiene un ETL mantenible: una función que limpia, escribe un archivo y manda un mensaje a la vez es imposible de probar.

**6. El efecto secundario escondido.**

```python
def agregar_total(montos):
    montos.append(sum(montos))
    return montos


ventas = [10, 20]
resultado = agregar_total(ventas)
print(ventas)
print(resultado)
```

```salida
[10, 20, 30]
[10, 20, 30]
```

La función **modificó la lista original** (`ventas` ahora tiene un elemento más) además de devolverla. Es un efecto secundario sorpresa; lo explicamos en la lección 8.2. Una función pura habría devuelto una lista nueva: `return montos + [sum(montos)]`.

Ejemplo comercial: `ticket_promedio(ventas, pedidos)` devuelve `None` si `pedidos` es 0, no 0 ni un error: el consumidor decide qué mostrar. Esa decisión queda documentada en el docstring.

## Errores comunes

- **Imprimir en lugar de devolver.**
- **Devolver `0` para un caso que significa «no calculable».**
- **Mezclar en una función limpieza, cálculo y escritura de archivos.**
- **No probar el caso límite ni el inválido.**
- **Funciones que modifican sin avisar los datos que reciben.**
- **Poner un parámetro con valor por defecto antes de uno obligatorio** (`SyntaxError`).
- **No escribir qué devuelve la función cuando falla.**

## Para comprobar que entendiste

1. ¿Qué es un contrato?
2. ¿Cuándo conviene devolver `None` en lugar de `0`?
3. ¿Qué devuelve `return a, b`?
4. ¿Qué es una función pura?

<details><summary>Respuestas</summary>

1. Lo que la función recibe, devuelve y hace con los casos raros.
2. Cuando «no hay dato o no se puede calcular» significa algo distinto de «cero».
3. Una tupla `(a, b)`.
4. Una que solo depende de sus parámetros y solo devuelve un valor, sin efectos secundarios.

</details>

## Micropráctica

1. Escribe `def variacion_pct(actual, anterior)` que devuelva el porcentaje de variación respecto al período anterior, o `None` si `anterior` es 0. Escribe tres `assert` (normal, límite, inválido) con resultados calculados a mano antes de ejecutar.
2. Escribe `def minimo_y_maximo(valores)` que devuelva el mínimo y el máximo como tupla, o `(None, None)` si la lista está vacía.
3. Añade a una función tuya un docstring con «Recibe», «Devuelve» y «Casos raros».

Cómo saber que está bien: `variacion_pct(120, 100)` es 20 y `variacion_pct(5, 0)` es `None`; `minimo_y_maximo([3, 9, 1])` da `(1, 9)`.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
def variacion_pct(actual, anterior):
    if anterior == 0:
        return None
    return (actual - anterior) / anterior * 100


assert variacion_pct(120, 100) == 20
assert variacion_pct(100, 100) == 0
assert variacion_pct(5, 0) is None


def minimo_y_maximo(valores):
    if len(valores) == 0:
        return None, None
    return min(valores), max(valores)


print(minimo_y_maximo([3, 9, 1]), minimo_y_maximo([]))
```

```salida
(1, 9) (None, None)
```

</details>

## Después, en los ejercicios

Los ejercicios P09–P16 de [Python](../../03_EJERCICIOS/Python/) piden funciones con reglas claras para entradas inválidas. Lee el apartado «Qué recibe y qué devuelve» del enunciado como un contrato y escribe tus `assert` antes de la función. Siguiente: [8.2 Ámbito de las variables y efectos secundarios](02_ambito_efectos.md).
