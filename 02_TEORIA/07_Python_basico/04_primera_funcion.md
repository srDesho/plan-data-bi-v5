# 7.4 Tu primera función corta

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [7.2 Variables](02_variables_asignacion.md) y [7.3 Tipos y aritmética](03_tipos_aritmetica.md).

## Para qué sirve

Si necesitas el mismo cálculo en diez lugares, copiarlo diez veces es una invitación al error: arreglas uno y olvidas los otros nueve. Una **función** guarda los pasos bajo un nombre y la usas cuantas veces quieras con datos distintos. Los ejercicios P01–P30 son, casi todos, funciones que escribes tú; aquí aprendes la forma mínima de una función antes de profundizar en el capítulo 8.

## Términos nuevos

- **Función** (ya la viste en 7.1): un bloque de instrucciones con nombre. Aquí aprendes a **escribir** las tuyas.
- **Definir una función**: escribir sus instrucciones con `def`. Aún no se ejecutan.
- **Llamar** (o *invocar*) una función: escribir su nombre con paréntesis para que sus instrucciones se ejecuten.
- **Parámetro**: el nombre que escribes **entre los paréntesis de la definición** para recibir un dato. Funciona como una variable que vive solo dentro de la función.
- **Argumento**: el valor real que escribes **en la llamada**. Se asigna al parámetro. (En `def f(x)`, `x` es el parámetro; en `f(5)`, `5` es el argumento.)
- **Retorno** (`return`): la instrucción que **devuelve** un resultado a quien llamó a la función y termina la función. El valor devuelto es el *valor de retorno*.
- **Bloque**: las líneas de la función que van con **sangría** (4 espacios) debajo de `def`. La sangría indica qué líneas pertenecen a la función.
- **Firma**: la primera línea (`def nombre(parámetros):`). Es el «contrato»: cómo se llama y qué recibe.

## Ejemplo paso a paso

**1. Una función mínima.** Calcula el descuento en Bs de un precio, dado un porcentaje:

```python
def descuento_en_bs(precio, pct):
    return precio * pct / 100


print(descuento_en_bs(200, 10))
```

```salida
20.0
```

Línea por línea:

1. `def descuento_en_bs(precio, pct):` define una función llamada `descuento_en_bs` con dos parámetros, `precio` y `pct`. Los **dos puntos** al final son obligatorios.
2. `return precio * pct / 100` está **indentada** (4 espacios): pertenece a la función. Calcula `200 * 10 / 100` = 20.0 y lo devuelve.
3. Las líneas en blanco no importan. La línea `print(descuento_en_bs(200, 10))` ya no tiene sangría: está fuera de la función. **Llama** a la función con los argumentos `200` y `10`, y `print` muestra lo que la función devolvió.

Orden de ejecución: Python lee `def`, guarda la función **sin ejecutarla**, y recién en la llamada ejecuta su bloque. Si nunca la llamas, nunca se ejecuta.

**2. Reutilizarla con otros datos.**

```python
def descuento_en_bs(precio, pct):
    return precio * pct / 100


print(descuento_en_bs(200, 10))
print(descuento_en_bs(80, 25))
print(descuento_en_bs(precio=50, pct=5))
```

```salida
20.0
20.0
2.5
```

Cada llamada usa argumentos distintos. En la tercera los escribimos con el nombre del parámetro (`precio=50`); así el orden ya no importa y la llamada es más legible.

**3. Guardar el resultado en una variable.** Como la función **devuelve** un valor, puedes guardarlo y seguir calculando:

```python
def descuento_en_bs(precio, pct):
    return precio * pct / 100


precio_lista = 120
descuento = descuento_en_bs(precio_lista, 15)
precio_final = precio_lista - descuento
print(descuento, precio_final)
```

```salida
18.0 102.0
```

**4. `print` no es `return`.** Esta es la confusión más común. Una función que solo imprime no entrega nada:

```python
def descuento_mal(precio, pct):
    print(precio * pct / 100)


resultado = descuento_mal(200, 10)
print("El resultado guardado es:", resultado)
```

```salida
20.0
El resultado guardado es: None
```

Primero se imprime `20.0` (lo hizo el `print` de dentro de la función), pero `resultado` vale `None`: la función no devolvió nada. Si necesitas usar el valor después (sumarlo, compararlo, guardarlo), tiene que salir con `return`. Los correctores de los ejercicios P comprueban lo que la función **devuelve**, no lo que imprime.

**5. Probar la función con `assert`.** `assert` verifica que una condición sea verdadera; si no, el programa se detiene con un error. Así pruebas tu función con casos que calculaste a mano:

```python
def descuento_en_bs(precio, pct):
    return precio * pct / 100


assert descuento_en_bs(200, 10) == 20
assert descuento_en_bs(0, 50) == 0
assert descuento_en_bs(80, 25) == 20
print("Pruebas correctas")
```

```salida
Pruebas correctas
```

Si alguna prueba fallara, verías `AssertionError` indicando la línea. La mejor práctica: **primero calculas a mano el resultado esperado, después lo escribes en un `assert`, y recién entonces escribes (o corriges) la función**.

**6. Errores típicos.** Llamar con menos argumentos de los que pide:

```python
def descuento_en_bs(precio, pct):
    return precio * pct / 100


print(descuento_en_bs(200))
```

```error
TypeError: descuento_en_bs() missing 1 required positional argument: 'pct'
```

Dice: a `descuento_en_bs()` le falta 1 argumento obligatorio, `pct`. Otros errores frecuentes: olvidar los dos puntos (`SyntaxError`), olvidar la sangría (`IndentationError`), o escribir `return` sin valor y obtener `None`.

Ejemplo comercial: la regla «un cliente es de alto valor si su ticket supera Bs 500» se escribe en una sola función; todos los reportes la llaman. Si el umbral cambia a 600, lo cambias en un lugar.

## Errores comunes

- **Olvidar los dos puntos** al final de la línea `def`.
- **No indentar el cuerpo** de la función.
- **Usar `print` en lugar de `return`** y obtener `None`.
- **Confundir parámetro con argumento**: el primero está en la definición, el segundo en la llamada.
- **Llamar con una cantidad incorrecta de argumentos.**
- **Escribir `descuento_en_bs` sin paréntesis** (sin llamar): no se ejecuta.
- **Cambiar el nombre de la función** respecto al que pide el ejercicio: el corrector no la encontrará.
- **No probar con un caso calculado a mano** antes de dar la función por buena.

## Para comprobar que entendiste

1. En `def f(x, y):` y en la llamada `f(3, 4)`, ¿cuáles son los parámetros y cuáles los argumentos?
2. ¿Qué devuelve una función que no tiene `return`?
3. ¿Qué diferencia práctica hay entre `print` y `return`?
4. ¿Qué hace `assert f(3, 4) == 7`?

<details><summary>Respuestas</summary>

1. Parámetros: `x` e `y`. Argumentos: `3` y `4`.
2. `None`.
3. `print` muestra algo en pantalla; `return` entrega un valor que el resto del programa puede usar.
4. Verifica que `f(3, 4)` valga 7; si no, detiene el programa con `AssertionError`.

</details>

## Micropráctica

1. Escribe `def precio_con_iva(precio, tasa)` que devuelva el precio más el impuesto (tasa en porcentaje, por ejemplo 13). Prueba con `assert` que `precio_con_iva(100, 13)` es 113.
2. Escribe `def unidades_por_caja_completa(unidades, por_caja)` que devuelva cuántas cajas completas se pueden armar (usa `//`). Calcula a mano un caso y pruébalo con `assert`.
3. Escribe una función que **imprima** en lugar de devolver y comprueba, guardando su resultado en una variable, que vale `None`.

Cómo saber que está bien: tus `assert` no producen error; si cambias a propósito el 113 por 114, deben fallar con `AssertionError`.

<details><summary>Comprobación de la parte 1</summary>

```python
def precio_con_iva(precio, tasa):
    return precio + precio * tasa / 100


assert precio_con_iva(100, 13) == 113
print(precio_con_iva(250, 13))
```

```salida
282.5
```

</details>

## Después, en los ejercicios

Puedes empezar [P01](../../03_EJERCICIOS/Python/P01.md): escribe tu función en `mi_trabajo/python/mis_funciones.py` partiendo de la plantilla, calcula a mano un ejemplo y pruébalo con `assert` antes de pasar el corrector. El capítulo 8 profundiza: valores por defecto, devolver varios valores, ámbito y archivos. Siguiente: [7.5 Texto](05_texto.md).
