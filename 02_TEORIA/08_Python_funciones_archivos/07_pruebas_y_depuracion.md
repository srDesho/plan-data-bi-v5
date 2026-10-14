# 8.7 Pruebas con assert y depuración paso a paso

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [8.1 Funciones con contrato](01_funciones_con_contrato.md) y [8.6 Leer un traceback](06_leer_tracebacks.md).

## Para qué sirve

Cuando un resultado no cuadra no sirve «mirar a ver qué pasa». Un método de depuración convierte la frustración en pasos: reproducir, reducir, formular una hipótesis, comprobarla y cambiar **una sola cosa**. Y las pruebas con `assert` te avisan del fallo antes de que llegue a un reporte. Juntos son lo que te vuelve independiente de cualquier ayuda externa.

## Términos nuevos

- **Prueba**: un `assert` (o varios) que comprueba que una función da el resultado esperado para una entrada conocida.
- **Caso normal / límite / inválido**: los tres tipos de entrada que toda función debe probarse: una típica, una en el borde de una regla y una que no cumple la regla.
- **Depurar** (*debug*): encontrar y corregir la causa de un resultado incorrecto.
- **Hipótesis**: una explicación posible del fallo que se puede comprobar («el acumulador se reinicia en cada vuelta»).
- **`print` de depuración**: imprimir valores intermedios para ver qué ocurre; se retiran al terminar.
- **Punto de interrupción** (*breakpoint*): una marca en el editor que detiene el programa en esa línea para inspeccionar las variables.
- **Ejecución paso a paso**: avanzar línea por línea mirando cómo cambian las variables.
- **Regresión**: un error que vuelve a aparecer porque un cambio rompió algo que antes funcionaba; las pruebas lo detectan.

## Ejemplo paso a paso

**1. Un programa con resultado incorrecto (sin error visible).** Queremos el promedio de ventas sin contar los días en cero:

```python
def promedio_dias_con_ventas(ventas):
    total = 0
    cantidad = 0
    for v in ventas:
        if v > 0:
            total = total + v
        cantidad = cantidad + 1
    return total / cantidad


print(promedio_dias_con_ventas([100, 0, 200, 0]))
```

```salida
75.0
```

Imprime 75.0 pero el promedio de 100 y 200 es 150. No hay traceback: el programa «funciona» y da una cifra equivocada. Este es el tipo de error más peligroso.

**2. Método: reproducir y reducir.** Usa el caso más pequeño posible con respuesta conocida: `[100, 0, 200, 0]` ya es pequeño y sabemos que debe dar 150.

**3. Hipótesis y comprobación con `print`.** Imprime los acumuladores en cada iteración:

```python
def promedio_dias_con_ventas(ventas):
    total = 0
    cantidad = 0
    for v in ventas:
        if v > 0:
            total = total + v
        cantidad = cantidad + 1
        print("v =", v, "total =", total, "cantidad =", cantidad)
    return total / cantidad


promedio_dias_con_ventas([100, 0, 200, 0])
```

```salida
v = 100 total = 100 cantidad = 1
v = 0 total = 100 cantidad = 2
v = 200 total = 300 cantidad = 3
v = 0 total = 300 cantidad = 4
```

Mira la columna `cantidad`: sube en **todas** las iteraciones (1, 2, 3, 4), incluso cuando `v` es 0. Hipótesis confirmada: `cantidad = cantidad + 1` está fuera del `if`, así que cuenta todos los días y no solo los que tuvieron ventas.

**4. Corregir UNA cosa y verificar.** Mover esa línea dentro del `if`:

```python
def promedio_dias_con_ventas(ventas):
    total = 0
    cantidad = 0
    for v in ventas:
        if v > 0:
            total = total + v
            cantidad = cantidad + 1
    if cantidad == 0:
        return None
    return total / cantidad


print(promedio_dias_con_ventas([100, 0, 200, 0]))
print(promedio_dias_con_ventas([0, 0]))
```

```salida
150.0
None
```

Ahora da 150.0, y para una lista sin días con ventas devuelve `None` en lugar de romper con `ZeroDivisionError`. Cambiamos dos cosas relacionadas a propósito; en general, **un cambio por vez** y se prueba antes del siguiente.

**5. Convertir lo aprendido en pruebas.** Un `assert` por cada caso, calculados a mano antes:

```python
def promedio_dias_con_ventas(ventas):
    total = 0
    cantidad = 0
    for v in ventas:
        if v > 0:
            total = total + v
            cantidad = cantidad + 1
    if cantidad == 0:
        return None
    return total / cantidad


assert promedio_dias_con_ventas([100, 0, 200, 0]) == 150      # normal
assert promedio_dias_con_ventas([50]) == 50                   # límite: un solo elemento
assert promedio_dias_con_ventas([0, 0]) is None               # inválido: sin ventas
assert promedio_dias_con_ventas([]) is None                   # vacío
print("todas las pruebas pasan")
```

```salida
todas las pruebas pasan
```

Estas pruebas quedan como **red de seguridad**: si mañana cambias la función y reaparece el error (regresión), un `assert` fallará al instante en lugar de que el error llegue a un reporte.

**6. Cuando falla una prueba.**

```python
def doble(x):
    return x * 3


assert doble(4) == 8, "doble(4) debería ser 8"
```

```error
AssertionError: doble(4) debería ser 8
```

El texto después de la coma es el mensaje; explica qué esperabas. Un mensaje claro ahorra tiempo.

**7. La rutina de trabajo para cada ejercicio.**

1. **Calcula a mano** un caso pequeño (el resultado esperado).
2. Escribe el `assert` de ese caso y de un caso límite.
3. Escribe la función.
4. Ejecuta; si falla, aplica reproducir → reducir → hipótesis → comprobar → una sola corrección.
5. Pasa el corrector del ejercicio.
6. Escribe en `errores.md` qué falló y cómo lo encontraste.

Método con tiempos para los ejercicios: **intento 10 min → comprobar → depurar 10 min → pista → solución solo con explicación propia**. Así entrenas autonomía en lugar de dependencia.

**8. Depurar con el editor (comprobación manual).** VS Code permite poner un *breakpoint* (clic a la izquierda del número de línea), ejecutar con «Run and Debug» y avanzar línea por línea mirando las variables en el panel lateral. Es equivalente a los `print` pero sin modificar el código. Esta función de la interfaz **no se comprueba automáticamente** en este paquete: pruébala tú en tu equipo; si no la tienes configurada, los `print` bastan.

Ejemplo comercial: un total de ventas que no cuadra con el de SQL. Reduces a una sola tienda, comparas sus filas con SQL, descubres que Python incluyó anuladas porque faltó un `if estado`. Ese camino (reproducir → reducir → comparar → corregir) es la defensa en la entrevista: «así lo encontré».

## Errores comunes

- **Cambiar código al azar** esperando que funcione.
- **Cambiar varias cosas a la vez.**
- **No tener el resultado esperado calculado a mano.**
- **Probar solo el caso feliz.**
- **Dejar los `print` de depuración en el código final.**
- **Pegar el error a una IA y aceptar la solución sin entenderla.**
- **No guardar lo aprendido** del error (para no repetirlo).

## Para comprobar que entendiste

1. ¿Qué son un caso normal, uno límite y uno inválido?
2. ¿Por qué es peligroso un error sin traceback?
3. ¿Qué es una regresión y cómo la detectan los `assert`?
4. Menciona los pasos del método de depuración.

<details><summary>Respuestas</summary>

1. Entrada típica, entrada en el borde de una regla, entrada que no cumple la regla.
2. Porque el programa da un resultado incorrecto que parece válido y nadie lo cuestiona.
3. Un error que reaparece tras un cambio; un `assert` fallará al ejecutarse de nuevo.
4. Reproducir, reducir, formular hipótesis, comprobar, cambiar una sola cosa y volver a probar.

</details>

## Micropráctica

1. La función siguiente debería devolver la suma de los números pares de una lista, pero devuelve un valor equivocado. Sin ver la solución, aplica el método: calcula a mano el esperado para `[1, 2, 3, 4]` (es 6), añade `print` de depuración, encuentra la causa y corrígela.
   ```py
   def suma_pares(lista):
       for n in lista:
           total = 0
           if n % 2 == 0:
               total = total + n
       return total
   ```
2. Escribe cuatro `assert` (normal, límite, vacío, inválido) para una función `descuento_en_bs` de la lección 7.4 y verifica que pasan.
3. Introduce a propósito un error en tu función y comprueba que un `assert` lo detecta.

Cómo saber que está bien: en la 1 la causa es que `total = 0` está dentro del bucle (se reinicia en cada vuelta); la función corregida devuelve 6 para `[1, 2, 3, 4]`.

<details><summary>Comprobación de la parte 1</summary>

```python
def suma_pares(lista):
    total = 0
    for n in lista:
        if n % 2 == 0:
            total = total + n
    return total


assert suma_pares([1, 2, 3, 4]) == 6
assert suma_pares([]) == 0
assert suma_pares([1, 3]) == 0
print("ok")
```

```salida
ok
```

</details>

## Después, en los ejercicios

Usa esta rutina en todos los P de [Python](../../03_EJERCICIOS/Python/) y en los DB01–DB03 de [Depuración](../../03_EJERCICIOS/Depuracion/). Registra cada error en `mi_trabajo/errores.md` con «qué falló / cómo lo encontré / qué aprendí». Siguiente capítulo: [Capítulo 9 — Pandas básico](../09_Pandas_basico.md).
