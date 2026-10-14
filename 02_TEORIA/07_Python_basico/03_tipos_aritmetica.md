# 7.3 Tipos de datos y aritmética

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisito: [7.2 Variables y asignación](02_variables_asignacion.md).

## Para qué sirve

Python no trata igual un `3` que un `"3"`: el primero es un número con el que puedes calcular, el segundo es un texto. Esa diferencia explica la mitad de los errores de principiante (por ejemplo, sumar un monto leído de un archivo, que llega como texto). Aquí aprendes qué tipos básicos existen, cómo hacer cuentas y por qué algunas cuentas con decimales dan resultados raros.

## Términos nuevos

- **Tipo de dato**: la clase de valor, que determina qué operaciones tiene sentido hacer con él. Se consulta con `type(valor)`.
- **`int`** (entero): números sin decimales: `3`, `-12`, `0`.
- **`float`** (decimal, «punto flotante»): números con decimales: `8.5`, `0.1`. En Python el separador decimal es el **punto**, no la coma.
- **`str`** (texto, *string*): una cadena de caracteres entre comillas: `"R01"`, `'Ana'`, `"3"`.
- **`bool`** (booleano): solo dos valores, `True` (verdadero) y `False` (falso). Se detalla en la lección 7.6.
- **`None`**: el valor que significa «no hay valor» (parecido a `NULL` de SQL). Es su propio tipo.
- **Operador**: el símbolo que indica una operación: `+`, `-`, `*`, `/`, `//`, `%`, `**`.
- **División entera (`//`)**: la división que descarta los decimales y da solo el cociente entero.
- **Módulo o resto (`%`)**: lo que sobra al dividir. `17 % 5` es 2, porque 17 = 3 × 5 + 2.
- **Precedencia**: el orden en que se resuelven los operadores; los paréntesis lo cambian.
- **Punto flotante**: la forma en que la computadora guarda los decimales; es una aproximación, por eso algunas cuentas dan resultados con restos diminutos.

## Ejemplo paso a paso

**1. Ver el tipo de un valor.**

```python
print(type(3))
print(type(8.5))
print(type("3"))
print(type(True))
print(type(None))
```

```salida
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

`<class 'int'>` quiere decir «tipo `int`». Observa que `3` (entero) y `"3"` (texto) son tipos distintos aunque se vean parecidos.

**2. Las operaciones básicas.**

```python
print(7 + 2)
print(7 - 2)
print(7 * 2)
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(7 ** 2)
```

```salida
9
5
14
3.5
3
1
49
```

- `+`, `-`, `*`: suma, resta, multiplicación.
- `/`: división «normal»: **siempre da un `float`**, incluso si es exacta (`6 / 3` da `2.0`).
- `//`: división entera: 7 entre 2 da 3 (se descarta el 0,5).
- `%`: resto: 7 entre 2 da 3 y sobra 1.
- `**`: potencia: 7 elevado a 2.

Uso de negocio del resto: saber si un número es par o múltiplo de algo. Por ejemplo, ¿cuántas cajas completas salen de 50 unidades si cada caja trae 12, y cuántas sobran?

```python
unidades = 50
por_caja = 12
cajas_completas = unidades // por_caja
sueltas = unidades % por_caja
print(cajas_completas, sueltas)
```

```salida
4 2
```

Resultado: 4 cajas completas y 2 unidades sueltas (4 × 12 + 2 = 50). Siempre se cumple `dividendo = cociente × divisor + resto`.

**3. Precedencia.** Primero potencias, luego multiplicación y división, luego suma y resta; los paréntesis mandan:

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
```

```salida
14
20
```

En la primera, 3 × 4 = 12 y luego + 2 = 14. En la segunda, el paréntesis fuerza 2 + 3 = 5 y luego × 4 = 20. Si dudas, **usa paréntesis**: no cuestan nada y aclaran la intención.

**4. Mezclar `int` y `float`.** El resultado se vuelve `float`:

```python
unidades = 12
precio = 8.5
print(unidades * precio)
print(type(unidades * precio))
```

```salida
102.0
<class 'float'>
```

**5. Texto y números no se mezclan sin conversión.**

```python
cantidad = "3"
precio = 10
print(cantidad * 2)
print(precio * 2)
```

```salida
33
20
```

`"3" * 2` **repite** el texto («33»); `10 * 2` calcula 20. Y si intentas sumar un texto y un número, falla:

```python
print("3" + 10)
```

```error
TypeError: can only concatenate str (not "int") to str
```

`TypeError` significa «tipos incompatibles». Python no adivina si querías que `"3"` fuera el número 3 o que `10` fuera el texto «10». La solución es convertir explícitamente (lección 7.7).

**6. Los decimales no son exactos.**

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

```salida
0.30000000000000004
False
```

El primer resultado no es 0.3 sino `0.30000000000000004`. La computadora guarda 0.1 y 0.2 en binario con una pequeña aproximación y la suma arrastra ese resto. No es un error de Python: pasa en cualquier lenguaje. Consecuencias prácticas: **no compares decimales con `==`**; para dinero, define una regla de redondeo (por ejemplo, trabajar en centavos como enteros o redondear al final) y escríbela.

**7. Redondear.** `round(valor, n)` redondea a `n` decimales:

```python
print(round(3.14159, 2))
print(round(0.5), round(1.5), round(2.5))
```

```salida
3.14
0 2 2
```

Atención al segundo renglón: `round(0.5)` da 0, `round(1.5)` da 2 y `round(2.5)` da 2. Python redondea los «medios» hacia el entero **par** más cercano. Excel redondea el 2,5 hacia 3. Si tu reporte debe coincidir con Excel o con SQL, comprueba qué regla usa cada herramienta y decide una sola; no lo dejes al azar.

Ejemplo comercial: una línea de 3 unidades a Bs 0,10 de comisión da `3 * 0.1 = 0.30000000000000004`. En un reporte lo presentas con 2 decimales (lección 7.5), pero en una comparación o en un control de cuadre ese resto puede hacer fallar un `==`.

## Errores comunes

- **Sumar un texto con un número**: `TypeError`. Los montos leídos de un archivo llegan como texto.
- **Esperar un entero de `/`**: la división normal siempre devuelve `float`.
- **Comparar decimales con `==`**: usa un redondeo o una tolerancia.
- **Usar coma como separador decimal** (`8,5`): Python lo lee como dos valores, no como un decimal.
- **Olvidar la precedencia**: `2 + 3 * 4` no es 20.
- **Dividir entre cero**: `ZeroDivisionError`; hay que comprobar el denominador antes.
- **Dar por hecho que `round` redondea como Excel.**

## Para comprobar que entendiste

1. ¿Cuál es el tipo de `7 / 7`? ¿Y de `7 // 7`?
2. ¿Cuánto da `23 % 5` y qué significa?
3. ¿Por qué `0.1 + 0.2 == 0.3` da `False`?
4. ¿Qué devuelve `"4" * 3`?

<details><summary>Respuestas</summary>

1. `float` (1.0) y `int` (1).
2. 3: al dividir 23 entre 5, sobran 3.
3. Porque los decimales se guardan de forma aproximada y la suma arrastra un resto diminuto.
4. `"444"` (repite el texto).

</details>

## Micropráctica

1. Calcula con Python cuántas cajas completas y cuántas unidades sueltas salen de 137 unidades con 24 unidades por caja.
2. Un importe de Bs 125,50 lleva una comisión del 3 %. Calcula la comisión en una variable y muéstrala redondeada a 2 decimales.
3. Predice y luego comprueba: `print(10 - 4 / 2)` y `print((10 - 4) / 2)`.
4. Escribe el tipo de cada uno: `15`, `15.0`, `"15"`, `15 > 3`.

Cómo saber que está bien: la 1 da 5 cajas y 17 sueltas; la 2 da 3.77 (la comisión exacta es 3,765); la 3 da 8.0 y 3.0.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
unidades = 137
por_caja = 24
print(unidades // por_caja, unidades % por_caja)

importe = 125.50
comision = importe * 3 / 100
print(round(comision, 2))
```

```salida
5 17
3.77
```

Nota: `round(3.765, 2)` puede dar 3.77 o 3.76 según la representación interna del decimal; por eso en dinero conviene fijar y documentar una regla de redondeo. Aquí el resultado mostrado es el que realmente imprime Python 3.12.

</details>

## Después, en los ejercicios

Las operaciones y los tipos son la base de P01, P02 y P08 en [Python](../../03_EJERCICIOS/Python/). Siguiente: [7.4 Tu primera función corta](04_primera_funcion.md).
