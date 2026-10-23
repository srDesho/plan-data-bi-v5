# 7.13 Recorrer registros: listas de diccionarios

> Tiempo estimado: 65 min (lectura 25 + práctica 40). Prerrequisitos: [7.9 Diccionarios](09_diccionarios_sets.md), [7.10 Condicionales](10_condicionales.md), [7.11 for](11_for_while.md) y [7.12 Acumuladores](12_acumuladores.md).

## Para qué sirve

Los datos reales son tablas: cada fila es un registro con varios campos. En Python, una tabla pequeña se representa como una **lista de diccionarios**: la lista es la tabla y cada diccionario es una fila. Casi todo el trabajo de un ETL (leer un CSV, validar, calcular totales, separar lo malo) es recorrer una estructura así. Esta lección junta, por primera vez, todas las piezas anteriores, y lo hace de a una.

## Términos nuevos

- **Registro**: una fila de datos, representada aquí como un diccionario `{"campo": valor, ...}`.
- **Campo**: cada clave de un registro (equivale a una columna).
- **Colección de registros**: una lista cuyos elementos son registros (equivale a una tabla).
- **Acumulador de diccionario**: un diccionario vacío al que se le agregan o actualizan claves mientras se recorre (por ejemplo, un conteo por categoría).
- **Registro válido / rechazado**: uno que cumple las reglas y sigue, frente a uno que no las cumple y se aparta con su motivo.
- **Resumen**: el resultado final calculado a partir de los registros (totales, conteos, promedios).

## Ejemplo paso a paso

Usamos seis líneas de venta inventadas (distintas de los ejercicios):

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
    {"articulo": "Jabón", "categoria": "Limpieza", "cantidad": 10, "precio": 3.5},
    {"articulo": "Galletas", "categoria": "Snacks", "cantidad": 12, "precio": 4.5},
    {"articulo": "Gaseosa 2L", "categoria": "Bebidas", "cantidad": 4, "precio": 11.5},
]
print(len(lineas))
print(lineas[0])
print(lineas[0]["articulo"])
```

```salida
6
{'articulo': 'Agua 2L', 'categoria': 'Bebidas', 'cantidad': 10, 'precio': 6.0}
Agua 2L
```

`lineas` es la lista (la tabla), `lineas[0]` es el primer diccionario (la primera fila) y `lineas[0]["articulo"]` es un campo de esa fila. Seis registros.

**Paso 1: solo recorrer.** Sin acumular nada todavía:

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
]

for linea in lineas:
    print(linea["articulo"], linea["cantidad"])
```

```salida
Agua 2L 10
Papas 100g 6
Jugo 1L 8
```

En cada iteración `linea` es un diccionario completo (una fila). Con `linea["articulo"]` accedes a sus campos. Tres iteraciones, tres filas.

**Paso 2: una columna calculada por fila.** El importe de cada línea:

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
]

for linea in lineas:
    importe = linea["cantidad"] * linea["precio"]
    print(linea["articulo"], importe)
```

```salida
Agua 2L 60.0
Papas 100g 45.0
Jugo 1L 72.0
```

**Paso 3: un acumulador numérico.** El importe total de las seis líneas:

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
    {"articulo": "Jabón", "categoria": "Limpieza", "cantidad": 10, "precio": 3.5},
    {"articulo": "Galletas", "categoria": "Snacks", "cantidad": 12, "precio": 4.5},
    {"articulo": "Gaseosa 2L", "categoria": "Bebidas", "cantidad": 4, "precio": 11.5},
]

total = 0
for linea in lineas:
    total = total + linea["cantidad"] * linea["precio"]

print(total)
```

```salida
312.0
```

Es el patrón «sumar» de 7.12 con una fila en lugar de un número. Comprobación a mano: 60 + 45 + 72 + 35 + 54 + 46 = 312.

**Paso 4: sumar solo las que cumplen una condición.** El importe de la categoría Bebidas:

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
    {"articulo": "Jabón", "categoria": "Limpieza", "cantidad": 10, "precio": 3.5},
    {"articulo": "Galletas", "categoria": "Snacks", "cantidad": 12, "precio": 4.5},
    {"articulo": "Gaseosa 2L", "categoria": "Bebidas", "cantidad": 4, "precio": 11.5},
]

total_bebidas = 0
for linea in lineas:
    if linea["categoria"] == "Bebidas":
        total_bebidas = total_bebidas + linea["cantidad"] * linea["precio"]

print(total_bebidas)
```

```salida
178.0
```

Filtrar (`if`) + sumar (acumulador). Control: 60 + 72 + 46 = 178.

**Paso 5: un diccionario como acumulador (agrupar).** El importe por categoría, el equivalente a `GROUP BY categoria`:

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
    {"articulo": "Jabón", "categoria": "Limpieza", "cantidad": 10, "precio": 3.5},
    {"articulo": "Galletas", "categoria": "Snacks", "cantidad": 12, "precio": 4.5},
    {"articulo": "Gaseosa 2L", "categoria": "Bebidas", "cantidad": 4, "precio": 11.5},
]

por_categoria = {}
for linea in lineas:
    categoria = linea["categoria"]
    importe = linea["cantidad"] * linea["precio"]
    por_categoria[categoria] = por_categoria.get(categoria, 0) + importe

print(por_categoria)
```

```salida
{'Bebidas': 178.0, 'Snacks': 99.0, 'Limpieza': 35.0}
```

La línea clave es `por_categoria[categoria] = por_categoria.get(categoria, 0) + importe`:

1. `por_categoria.get(categoria, 0)` pregunta: «¿cuánto llevo acumulado para esta categoría? Si todavía no existe, 0».
2. Le suma el importe de la línea actual.
3. Guarda el resultado en la misma clave.

Tabla de seguimiento del diccionario:

| Línea | `categoria` | `importe` | `por_categoria` después |
|---|---|---|---|
| 1 | Bebidas | 60.0 | `{'Bebidas': 60.0}` |
| 2 | Snacks | 45.0 | `{'Bebidas': 60.0, 'Snacks': 45.0}` |
| 3 | Bebidas | 72.0 | `{'Bebidas': 132.0, 'Snacks': 45.0}` |
| ... | ... | ... | ... |

**Control de cuadre:** los valores del diccionario deben sumar el total del paso 3 (312). Con `sum(por_categoria.values())` lo compruebas en una línea. Si no suman, tu agrupación perdió o duplicó algo.

**Paso 6: separar válidos y rechazados.** Los datos reales traen filas malas. Aquí una cantidad vacía y un precio no numérico:

```python
lineas = [
    {"articulo": "Agua 2L", "cantidad": "10", "precio": "6.0"},
    {"articulo": "Jugo 1L", "cantidad": "", "precio": "9.0"},
    {"articulo": "Jabón", "cantidad": "5", "precio": "tres"},
    {"articulo": "Galletas", "cantidad": "12", "precio": "4.5"},
]

validas = []
rechazadas = []
for linea in lineas:
    if linea["cantidad"].strip() == "":
        rechazadas.append((linea["articulo"], "cantidad vacía"))
        continue
    try:
        cantidad = int(linea["cantidad"])
        precio = float(linea["precio"])
    except ValueError:
        rechazadas.append((linea["articulo"], "valor no numérico"))
        continue
    validas.append({"articulo": linea["articulo"], "importe": cantidad * precio})

print(len(validas), len(rechazadas))
print(validas)
print(rechazadas)
```

```salida
2 2
[{'articulo': 'Agua 2L', 'importe': 60.0}, {'articulo': 'Galletas', 'importe': 54.0}]
[('Jugo 1L', 'cantidad vacía'), ('Jabón', 'valor no numérico')]
```

Aquí aparece una pieza nueva, `try/except`, que se explica en la lección 8.5: significa «intenta convertir; si da `ValueError`, no detengas el programa: ejecuta el bloque `except`». Lo importante es la idea: cada fila se clasifica en **válida** o **rechazada con motivo**, y al final el control es `válidas + rechazadas = filas de entrada` (aquí 2 + 2 = 4). Ninguna fila desaparece sin dejar registro.

**Paso 7: empaquetar en una función.** El mismo cálculo del paso 5 como función reutilizable y probada:

```python
def importe_por_categoria(lineas):
    resultado = {}
    for linea in lineas:
        categoria = linea["categoria"]
        importe = linea["cantidad"] * linea["precio"]
        resultado[categoria] = resultado.get(categoria, 0) + importe
    return resultado


prueba = [
    {"categoria": "A", "cantidad": 2, "precio": 5},
    {"categoria": "B", "cantidad": 1, "precio": 10},
    {"categoria": "A", "cantidad": 1, "precio": 5},
]
assert importe_por_categoria(prueba) == {"A": 15, "B": 10}
assert importe_por_categoria([]) == {}
print("pruebas correctas")
```

```salida
pruebas correctas
```

Dos pruebas con casos calculados a mano: uno normal y el **caso vacío**. Así comprobarás tus propias funciones.

Ejemplo comercial: leer las visitas del día como lista de registros, contar cuántas fueron realizadas por ruta (diccionario acumulador), y separar las visitas sin cliente como rechazadas con el motivo: es el esqueleto de un mini ETL, el mismo que escribirás con archivos reales en el capítulo 8.

## Errores comunes

- **Confundir la lista con el registro**: `lineas["articulo"]` falla (`TypeError`); es `linea["articulo"]` dentro del bucle o `lineas[0]["articulo"]`.
- **Escribir mal el nombre de un campo** (`KeyError`).
- **Inicializar el acumulador dentro del bucle.**
- **Olvidar `.get(clave, 0)`** y obtener `KeyError` la primera vez que aparece una categoría.
- **No separar los registros inválidos** y perderlos sin saber cuántos eran.
- **No comprobar el cuadre**: suma de grupos igual al total, válidos + rechazados igual a entrada.
- **Probar solo con datos «buenos»** y no con vacío, texto y valores raros.

## Para comprobar que entendiste

1. ¿Qué es `datos[2]["ruta"]` si `datos` es una lista de diccionarios?
2. ¿Qué hace `d[k] = d.get(k, 0) + 1`?
3. ¿Por qué el cuadre «válidas + rechazadas = entrada» es importante?
4. ¿Por qué se prueba una función con una lista vacía?

<details><summary>Respuestas</summary>

1. El valor del campo `ruta` de la tercera fila.
2. Cuenta: suma 1 al contador de la clave `k`, empezando en 0 si no existe.
3. Garantiza que ninguna fila desapareció sin registro.
4. Porque es un caso real frecuente (un archivo sin filas) y puede romper cálculos como promedios.

</details>

<a id="micropractica"></a>

## Micropráctica

Con la lista de seis líneas del ejemplo inicial:

1. Calcula la cantidad total de unidades por categoría con un diccionario acumulador y comprueba que suman 50.
2. Calcula el importe promedio por línea (total entre cantidad de líneas), protegiendo el caso de una lista vacía.
3. Encuentra el artículo con mayor importe de línea (patrón «máximo» guardando el nombre).
4. Escribe la lista de los nombres de artículos de la categoría Snacks (patrón «filtrar»).

Cómo saber que está bien: 1 → Bebidas 22, Snacks 18, Limpieza 10; 2 → 52.0; 3 → Jugo 1L (72.0); 4 → `['Papas 100g', 'Galletas']`.

<details><summary>Comprobación de las partes 1 y 3</summary>

```python
lineas = [
    {"articulo": "Agua 2L", "categoria": "Bebidas", "cantidad": 10, "precio": 6.0},
    {"articulo": "Papas 100g", "categoria": "Snacks", "cantidad": 6, "precio": 7.5},
    {"articulo": "Jugo 1L", "categoria": "Bebidas", "cantidad": 8, "precio": 9.0},
    {"articulo": "Jabón", "categoria": "Limpieza", "cantidad": 10, "precio": 3.5},
    {"articulo": "Galletas", "categoria": "Snacks", "cantidad": 12, "precio": 4.5},
    {"articulo": "Gaseosa 2L", "categoria": "Bebidas", "cantidad": 4, "precio": 11.5},
]

unidades = {}
for linea in lineas:
    c = linea["categoria"]
    unidades[c] = unidades.get(c, 0) + linea["cantidad"]
print(unidades, sum(unidades.values()))

mejor_articulo = None
mejor_importe = None
for linea in lineas:
    importe = linea["cantidad"] * linea["precio"]
    if mejor_importe is None or importe > mejor_importe:
        mejor_importe = importe
        mejor_articulo = linea["articulo"]
print(mejor_articulo, mejor_importe)
```

```salida
{'Bebidas': 22, 'Snacks': 18, 'Limpieza': 10} 50
Jugo 1L 72.0
```

</details>

## Después, en los ejercicios

Estás listo para la serie P04–P08 y P14 en [Python](../../03_EJERCICIOS/Python/): cada una usa una o dos de estas piezas con datos y reglas distintos. Antes de escribir código, anota «qué recorro, qué acumulo y qué condición aplico». El siguiente capítulo ([8](../08_Python_funciones_archivos.md)) lleva estas ideas a funciones robustas y archivos reales.
