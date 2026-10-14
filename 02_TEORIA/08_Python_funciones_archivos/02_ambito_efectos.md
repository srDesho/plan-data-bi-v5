# 8.2 Ámbito de las variables y efectos secundarios

> Tiempo estimado: 40 min (lectura 15 + práctica 25). Prerrequisito: [8.1 Funciones con contrato](01_funciones_con_contrato.md).

## Para qué sirve

Una variable creada dentro de una función no existe fuera de ella, y una función puede cambiar sin querer datos que están fuera. Dos errores muy frecuentes en los primeros programas de datos nacen aquí: el `NameError` por usar fuera lo que se creó dentro, y los resultados que «cambian solos» porque una función modificó una lista que recibió. Entender el ámbito evita ambos.

## Términos nuevos

- **Ámbito** (*scope*): la zona del programa donde un nombre existe y puede usarse.
- **Variable local**: la que se crea dentro de una función; existe solo mientras la función se ejecuta.
- **Variable global**: la que se crea fuera de cualquier función, al nivel principal del archivo; las funciones pueden **leerla**.
- **`UnboundLocalError`**: el error que aparece cuando una función intenta asignar a un nombre que también existe fuera y lo lee antes de asignarlo.
- **Parámetro como copia del nombre**: al llamar una función, el parámetro apunta al **mismo objeto** que el argumento. Si el objeto es mutable (lista, diccionario), modificarlo dentro de la función lo modifica también fuera.
- **Efecto secundario** (ya visto en 8.1): cambiar algo fuera de la función además de devolver un valor.

## Ejemplo paso a paso

**1. Las variables locales no se ven desde fuera.**

```python
def calcular_total(cantidad, precio):
    total = cantidad * precio
    return total


resultado = calcular_total(3, 10)
print(resultado)
print(total)
```

```error
NameError: name 'total' is not defined
```

`total` se creó **dentro** de la función y desaparece cuando termina. Fuera, el nombre no existe. Para usar el resultado fuera, la función lo **devuelve** y quien llama lo guarda en otra variable (`resultado`).

**2. Una función puede leer una variable global.**

```python
IVA = 13


def monto_iva(precio):
    return precio * IVA / 100


print(monto_iva(100))
```

```salida
13.0
```

`IVA` está fuera de la función; la función la lee sin problema. Por convención, los valores fijos que se leen en varias partes se escriben en MAYÚSCULAS (constantes).

**3. Asignar dentro de una función crea una variable local nueva.**

```python
contador = 0


def sumar_uno():
    contador = 1
    return contador


print(sumar_uno())
print(contador)
```

```salida
1
0
```

La función creó **su propia** `contador` local; la de afuera sigue en 0. Este comportamiento sorprende al principiante, que esperaba que la función cambiara la global. Y si la función intentara leer antes de asignar:

```python
contador = 0


def sumar_uno():
    contador = contador + 1
    return contador


print(sumar_uno())
```

```error
UnboundLocalError: cannot access local variable 'contador' where it is not associated with a value
```

Como la función asigna a `contador`, Python la considera local en toda la función, y al leerla antes de asignarla no tiene valor. La solución correcta no es usar `global`, sino **pasar el valor como parámetro y devolver el nuevo**:

```python
def sumar_uno(contador):
    return contador + 1


contador = 0
contador = sumar_uno(contador)
contador = sumar_uno(contador)
print(contador)
```

```salida
2
```

El flujo es claro: entra un valor, sale otro, y quien llama decide dónde guardarlo.

**4. Las listas y diccionarios se modifican «por dentro».** Una función que recibe una lista puede cambiarla:

```python
def agregar_ceros(lista):
    lista.append(0)
    lista.append(0)


ventas = [10, 20]
agregar_ceros(ventas)
print(ventas)
```

```salida
[10, 20, 0, 0]
```

La función no devolvió nada, y sin embargo `ventas` cambió: el parámetro `lista` y la variable `ventas` apuntan a **la misma lista**. Es la misma trampa del alias de la lección 7.8. En un programa grande, una función que modifica sus entradas puede alterar datos que otra parte del programa creía intactos. Versión sin efectos:

```python
def con_ceros(lista):
    return lista + [0, 0]


ventas = [10, 20]
nueva = con_ceros(ventas)
print(ventas)
print(nueva)
```

```salida
[10, 20]
[10, 20, 0, 0]
```

`lista + [0, 0]` crea una lista **nueva**; `ventas` queda intacta. Regla práctica: **una función recibe por parámetros, devuelve resultados y no modifica sus entradas**, salvo que su propósito declarado sea justamente modificarlas.

**5. Cuando sí quieres modificar una copia.**

```python
def ordenar_sin_tocar(lista):
    copia = lista.copy()
    copia.sort()
    return copia


desordenada = [3, 1, 2]
print(ordenar_sin_tocar(desordenada))
print(desordenada)
```

```salida
[1, 2, 3]
[3, 1, 2]
```

Si necesitas ordenar o limpiar dentro de la función, trabaja sobre una copia.

**6. Por qué se evita `global`.** Python permite declarar `global contador` dentro de la función para cambiar la global. Funciona, pero hace que cualquier función pueda cambiar el estado del programa sin que se vea en su firma. Es la fuente de errores difíciles de rastrear («¿quién cambió esta variable?»). En este curso **no usarás `global`**: usa parámetros y `return`.

Ejemplo comercial: una función `limpiar_filas(filas)` que modifica la lista de filas originales destruye el dato crudo. En un ETL quieres conservar el crudo para poder reprocesar; por eso las transformaciones devuelven una lista nueva.

## Errores comunes

- **Usar fuera de una función una variable creada dentro** (`NameError`).
- **Esperar que asignar dentro de una función cambie la global.**
- **Leer y asignar el mismo nombre dentro de una función sin pasarlo como parámetro** (`UnboundLocalError`).
- **Modificar la lista o diccionario recibido sin querer.**
- **Usar `global` para evitar pasar parámetros.**
- **Nombrar igual una variable local y una global** y confundirse.

## Para comprobar que entendiste

1. ¿Dónde existe una variable local?
2. ¿Qué pasa si una función hace `lista.append(1)` sobre su parámetro?
3. ¿Cómo se pasa un valor de una función a otra parte del programa sin `global`?
4. ¿Cómo evitas modificar la lista original dentro de una función?

<details><summary>Respuestas</summary>

1. Solo dentro de la función, mientras se ejecuta.
2. La lista original cambia, porque parámetro y argumento apuntan a la misma lista.
3. Con `return`, guardando el resultado en una variable de quien llama.
4. Trabajando sobre una copia (`copy()`) o construyendo una lista nueva.

</details>

## Micropráctica

1. Predice y comprueba qué imprime: `x = 5`, `def f(): x = 10; return x`, `print(f(), x)`.
2. Escribe `def quitar_negativos(lista)` que **devuelva** una lista nueva sin los valores negativos y deje la original intacta. Compruébalo imprimiendo ambas.
3. Reescribe, sin `global`, una función `incrementar()` que subía un contador global.

Cómo saber que está bien: 1 imprime `10 5`; en 2 la lista original conserva sus negativos.

<details><summary>Comprobación de la parte 2</summary>

```python
def quitar_negativos(lista):
    nueva = []
    for v in lista:
        if v >= 0:
            nueva.append(v)
    return nueva


datos = [4, -2, 7, -1, 0]
print(quitar_negativos(datos))
print(datos)
```

```salida
[4, 7, 0]
[4, -2, 7, -1, 0]
```

</details>

## Después, en los ejercicios

Los correctores de [Python](../../03_EJERCICIOS/Python/) llaman a tus funciones con datos propios y comprueban lo que **devuelven**; esta lección te ayuda a entender por qué una función que solo imprime o que modifica sus entradas es difícil de reutilizar y de probar. Siguiente: [8.3 Archivos: rutas, CSV y JSON](03_archivos_csv_json.md).
