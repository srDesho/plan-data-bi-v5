# 7.9 Diccionarios y conjuntos

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisito: [7.8 Listas y tuplas](08_listas_tuplas.md).

## Para qué sirve

Una fila de una tabla (un cliente, una venta) tiene varios datos con significado: id, nombre, ruta, monto. Guardarla en una lista obliga a recordar que «la posición 2 es la ruta». Un **diccionario** guarda cada dato con su nombre, así que el código se lee solo. Y cuando solo te importa saber qué valores distintos existen, un **conjunto** los guarda sin repetir.

## Términos nuevos

- **Diccionario** (`dict`): una colección de pares **clave → valor**, escrita entre llaves: `{"id": 1, "ruta": "R01"}`. Se busca por clave, no por posición.
- **Clave**: el nombre con el que se busca un valor dentro del diccionario. Debe ser única dentro de ese diccionario y no modificable (normalmente un texto o un número).
- **Valor**: el dato asociado a una clave. Puede ser de cualquier tipo.
- **`KeyError`**: la excepción que ocurre al pedir una clave que no existe.
- **Conjunto** (`set`): una colección **sin orden** y **sin elementos repetidos**, escrita entre llaves con elementos sueltos: `{"R01", "R02"}`.
- **Pertenencia**: preguntar si un elemento está dentro de una colección con `in`.

## Ejemplo paso a paso

**1. Crear un diccionario y leer valores.**

```python
tienda = {"id": 1, "nombre": "Tienda La Palma", "ruta": "R01", "zona": "Norte"}
print(tienda["nombre"])
print(tienda["ruta"])
print(len(tienda))
print("zona" in tienda)
print("telefono" in tienda)
```

```salida
Tienda La Palma
R01
4
True
False
```

`tienda["nombre"]` busca la clave `"nombre"` y devuelve su valor. `len` cuenta los pares. `in` pregunta si una **clave** existe (no si existe un valor).

**2. Pedir una clave que no existe.**

```python
tienda = {"id": 1, "nombre": "Tienda La Palma"}
print(tienda["telefono"])
```

```error
KeyError: 'telefono'
```

`KeyError` dice cuál clave no se encontró: `'telefono'`. Es el error más frecuente al leer filas de archivos: la clave está mal escrita (`"Telefono"`, `"teléfono"`) o el dato falta. Para no detener el programa, hay `get`:

```python
tienda = {"id": 1, "nombre": "Tienda La Palma"}
print(tienda.get("telefono"))
print(tienda.get("telefono", "sin dato"))
print(tienda.get("nombre", "sin dato"))
```

```salida
None
sin dato
Tienda La Palma
```

`get(clave)` devuelve `None` si la clave no existe; `get(clave, defecto)` devuelve el valor por defecto. No uses `get` para esconder un error que deberías ver: si la clave **debe** existir, es mejor que falle con `KeyError`.

**3. Agregar, cambiar y borrar.**

```python
tienda = {"id": 1, "nombre": "Tienda La Palma"}
tienda["ruta"] = "R01"
tienda["nombre"] = "La Palma"
print(tienda)
del tienda["id"]
print(tienda)
```

```salida
{'id': 1, 'nombre': 'La Palma', 'ruta': 'R01'}
{'nombre': 'La Palma', 'ruta': 'R01'}
```

Asignar a una clave que no existe la **crea**; asignar a una que existe **reemplaza** su valor. `del` elimina un par.

**4. Recorrer sus partes.**

```python
precios = {"Agua 2L": 6.0, "Jugo 1L": 9.0}
print(list(precios.keys()))
print(list(precios.values()))
print(list(precios.items()))
```

```salida
['Agua 2L', 'Jugo 1L']
[6.0, 9.0]
[('Agua 2L', 6.0), ('Jugo 1L', 9.0)]
```

`keys()` son las claves, `values()` los valores e `items()` los pares como tuplas `(clave, valor)`. Los recorrerás con `for` en la lección 7.11.

**5. Un diccionario como «tabla de consulta».** Traducir un código a un nombre:

```python
nombre_ruta = {"R01": "Norte", "R02": "Centro", "R03": "Sur"}
codigo = "R02"
print(nombre_ruta[codigo])
print(nombre_ruta.get("R09", "ruta desconocida"))
```

```salida
Centro
ruta desconocida
```

Es el equivalente de un `BUSCARV` de Excel o de un `JOIN` pequeño. Más adelante harás lo mismo con tablas completas en Pandas.

**6. Una lista de diccionarios: varias filas.**

```python
ventas = [
    {"venta_id": 1, "estado": "entregado", "monto": 137.0},
    {"venta_id": 2, "estado": "anulado", "monto": 90.0},
]
print(ventas[0]["estado"])
print(ventas[1]["monto"])
print(len(ventas))
```

```salida
entregado
90.0
2
```

`ventas[0]` es el primer diccionario (la primera fila); `ventas[0]["estado"]` entra a esa fila y toma el dato «estado». Así se representa una tabla pequeña. Aún no la recorremos entera: eso llega en la lección 7.13, cuando ya sepas `for` y acumuladores.

**7. Conjuntos: valores únicos.**

```python
rutas_vistas = ["R01", "R02", "R01", "R03", "R02", "R01"]
unicas = set(rutas_vistas)
print(len(rutas_vistas), len(unicas))
print(sorted(unicas))
print("R03" in unicas)
```

```salida
6 3
['R01', 'R02', 'R03']
True
```

Convertir una lista en `set` elimina las repeticiones. Un set **no tiene orden**: por eso `sorted(unicas)` lo convierte en una lista ordenada antes de mostrarlo. Nunca uses el orden de un set como el orden de un reporte.

Operaciones entre conjuntos (útiles para comparar dos listas de clientes):

```python
compraron = {"A", "B", "C"}
visitados = {"B", "C", "D"}
print(sorted(compraron & visitados))
print(sorted(compraron - visitados))
print(sorted(compraron | visitados))
```

```salida
['B', 'C']
['A']
['A', 'B', 'C', 'D']
```

`&` es la intersección (están en ambos), `-` la diferencia (están en el primero pero no en el segundo) y `|` la unión. En SQL serían un `INNER JOIN`, un anti-join y un `UNION`.

Ejemplo comercial: «clientes que compraron y no fueron visitados» es `compraron - visitados`. Es exactamente la pregunta que en SQL responderías con un anti-join, resuelta en una línea.

## Errores comunes

- **Pedir una clave con distinto texto** (`"Ruta"` en vez de `"ruta"`).
- **Usar `get` para esconder claves que deberían existir.**
- **Creer que `in` busca valores**: en un diccionario busca claves.
- **Esperar un orden en un set.**
- **Escribir `{}` esperando un set vacío**: `{}` es un diccionario vacío; el set vacío es `set()`.
- **Repetir una clave al crear el diccionario**: la segunda sobrescribe la primera sin avisar.
- **Usar una lista como clave**: no se puede (no es inmutable).

## Para comprobar que entendiste

1. ¿Cómo obtienes el valor asociado a la clave `"ruta"` en un diccionario `d`?
2. ¿Qué diferencia hay entre `d["x"]` y `d.get("x")` cuando la clave no existe?
3. ¿Cuántos elementos tiene `set([1, 1, 2, 3, 3])`?
4. ¿Por qué `{}` no es un set vacío?

<details><summary>Respuestas</summary>

1. `d["ruta"]`.
2. El primero lanza `KeyError`; el segundo devuelve `None`.
3. 3.
4. Porque Python lo interpreta como un diccionario vacío; el set vacío es `set()`.

</details>

## Micropráctica

1. Crea un diccionario con los datos de un artículo (`nombre`, `categoria`, `precio`), cambia el precio y agrega una clave `stock`. Muéstralo.
2. Dado `estados = ["entregado", "anulado", "entregado", "pendiente", "entregado"]`, obtén la lista ordenada de estados distintos y cuántos hay.
3. Dadas dos listas de códigos de tienda, `a = [1, 2, 3, 4]` y `b = [3, 4, 5]`, obtén las que están en `a` y no en `b`, y las que están en ambas.
4. Dado `d = {"a": 1}`, escribe dos líneas: una que lea la clave `"b"` sin romper el programa y otra que provoque `KeyError` a propósito.

Cómo saber que está bien: la 2 da `['anulado', 'entregado', 'pendiente']` y 3; la 3 da `[1, 2]` y `[3, 4]`.

<details><summary>Comprobación de las partes 2 y 3</summary>

```python
estados = ["entregado", "anulado", "entregado", "pendiente", "entregado"]
distintos = sorted(set(estados))
print(distintos, len(distintos))

a = [1, 2, 3, 4]
b = [3, 4, 5]
print(sorted(set(a) - set(b)), sorted(set(a) & set(b)))
```

```salida
['anulado', 'entregado', 'pendiente'] 3
[1, 2] [3, 4]
```

</details>

## Después, en los ejercicios

Diccionarios y conjuntos son la base de P04, P05 y P06 en [Python](../../03_EJERCICIOS/Python/). Justifica en tu cuaderno por qué elegiste lista, diccionario o set en cada uno. Siguiente: [7.10 Condicionales](10_condicionales.md).
