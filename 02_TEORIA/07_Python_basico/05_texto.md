# 7.5 Texto: cadenas, métodos y f-strings

> Tiempo estimado: 72 min (lectura 34 + práctica 38). Prerrequisitos: [7.2 Variables](02_variables_asignacion.md) y [7.3 Tipos de datos](03_tipos_aritmetica.md).

<!-- TEORIA:PREPARACION:INICIO -->
<a id="preparacion-p03"></a>
## Base inicial de texto · 12 min

Esta base reúne limpieza, inmutabilidad y partir/unir antes de P03; el desarrollo posterior permanece como REFUERZO. Un método se llama con un punto después del texto: `texto.strip()` quita espacios externos; `lower()`, `upper()` y `title()` cambian a minúsculas, mayúsculas o iniciales mayúsculas. Se pueden encadenar. Cada método devuelve un texto nuevo: si quieres conservarlo, asígnalo a una variable; el texto original no cambia.

`split(separador)` divide un texto en partes y `separador.join(partes)` las reúne en un texto nuevo. Sin separador, `split()` divide por espacios en blanco y omite partes vacías. Predice este ejemplo independiente antes de ejecutarlo:

```python
etiqueta = "  uno   DOS  "
partes = etiqueta.split()
print(partes)
print(" | ".join(partes))
print("tres CUATRO".title())
print(etiqueta)
```

`split()` **sin separador** divide por espacios en blanco y omite los trozos vacíos: produce `['uno', 'DOS']`. `join` construye un texto nuevo con el separador elegido: `uno | DOS`. `title` produce `Tres Cuatro`. La última línea conserva los espacios y mayúsculas originales: los métodos no modifican un `str`. `strip` quita los espacios de los extremos, no los repetidos en el interior.

Ahora cambia el separador y predice el resultado. Resuelve el ejercicio escogiendo y combinando tú las herramientas; aquí no se da la función pedida. Si REDUCIDO omite P03, recupera esta base inicial antes de normalizar texto en P09/D10; no se da por aprendido por haber visto una pista.

El encabezado de esta lección incluye esta sección de 12 min. Si ya la estudiaste en D02, quedan 22 min de lectura del desarrollo; no vuelvas a sumar esta sección. La práctica de 38 min se contabiliza por separado según la guía.
<!-- TEORIA:PREPARACION:FIN -->

<a id="desarrollo"></a>

## Para qué sirve

Casi todos los datos que llegan de un archivo CSV o de un sistema llegan como **texto**: nombres, códigos de ruta, fechas, incluso los montos. Y llegan sucios: espacios sobrantes, mayúsculas y minúsculas mezcladas, comas donde debería haber puntos. Limpiar y examinar texto es el trabajo diario de un ETL. Esta lección te da las herramientas básicas.

## Términos nuevos

- **Cadena de texto** (*string*, tipo `str`): un conjunto de caracteres entre comillas. Los textos de este curso van con comillas dobles `"..."` o simples `'...'`; son equivalentes.
- **Concatenar**: unir textos con `+`. `"R" + "01"` da `"R01"`.
- **Método**: una función que pertenece a un tipo de dato y se llama escribiendo un punto después del valor: `texto.upper()`. Cada tipo tiene sus propios métodos.
- **Inmutable**: que no se puede modificar después de creado. Un `str` es inmutable: los métodos no lo cambian; **devuelven un texto nuevo**.
- **Secuencia**: un conjunto ordenado de elementos, cada uno en una posición. Un texto es una secuencia de caracteres.
- **Índice**: el número de posición de un elemento en una secuencia. **Empieza en 0**: en `"Sol"`, la `S` está en el índice 0, la `o` en el 1 y la `l` en el 2.
- **Rebanada** (*slice*): un pedazo de una secuencia, escrito `[inicio:fin]`; incluye el índice `inicio` y excluye el `fin`.
- **f-string**: un texto que empieza con `f` antes de las comillas y permite incrustar valores entre llaves: `f"Total: {total}"`.

## Ejemplo paso a paso

**1. Longitud, concatenación e índices.**

```python
ruta = "R01"
print(len(ruta))
print(ruta + "-Norte")
print(ruta[0])
print(ruta[1])
print(ruta[-1])
```

```salida
3
R01-Norte
R
0
1
```

- `len(ruta)` cuenta los caracteres: 3.
- `ruta + "-Norte"` pega dos textos.
- `ruta[0]` es el primer carácter (`R`), `ruta[1]` el segundo (`0`). Los índices **empiezan en 0**.
- `ruta[-1]` cuenta desde el final: el último carácter (`1`).

**2. Rebanadas.**

```python
codigo = "R01-2026-09"
print(codigo[0:3])
print(codigo[4:8])
print(codigo[9:])
print(codigo[:3])
```

```salida
R01
2026
09
R01
```

`codigo[0:3]` toma los caracteres de los índices 0, 1 y 2 (el 3 **no** se incluye): `R01`. `codigo[4:8]` toma 4 caracteres desde el índice 4: `2026`. Si omites el fin (`[9:]`) llega hasta el final; si omites el inicio (`[:3]`) parte desde el principio.

**3. Métodos de limpieza.** Un texto que llegó sucio:

```python
crudo = "  kiosco LUNA  "
print("[" + crudo + "]")
print("[" + crudo.strip() + "]")
print(crudo.strip().lower())
print(crudo.strip().upper())
print(crudo.strip().title())
```

```salida
[  kiosco LUNA  ]
[kiosco LUNA]
kiosco luna
KIOSCO LUNA
Kiosco Luna
```

- `strip()` elimina los espacios (y saltos de línea) al inicio y al final. Los corchetes los hacen visibles.
- `lower()` pasa a minúsculas, `upper()` a mayúsculas y `title()` pone cada palabra con mayúscula inicial.
- Se pueden **encadenar**: `crudo.strip().lower()` limpia primero y baja a minúsculas después.

**4. Los métodos no modifican el original.** Como el texto es inmutable:

```python
nombre = "  Farmacia Vida  "
nombre.strip()
print("[" + nombre + "]")
nombre = nombre.strip()
print("[" + nombre + "]")
```

```salida
[  Farmacia Vida  ]
[Farmacia Vida]
```

La línea `nombre.strip()` calculó un texto limpio pero **nadie lo guardó**, así que `nombre` sigue sucio. Para quedarte con el resultado tienes que asignarlo: `nombre = nombre.strip()`. Es un error muy común.

**5. Buscar y reemplazar.**

```python
producto = "Gaseosa 2L"
print("2L" in producto)
print(producto.startswith("Gas"))
print(producto.endswith("1L"))
print(producto.replace("Gaseosa", "Jugo"))
print(producto.replace(" ", "_"))
```

```salida
True
True
False
Jugo 2L
Gaseosa_2L
```

`in` pregunta si un pedazo está dentro del texto y devuelve `True` o `False`. `startswith` y `endswith` preguntan por el inicio y el final. `replace(buscado, nuevo)` reemplaza **todas** las apariciones.

**5b. Quitar un prefijo o un sufijo.** Para eliminar un texto fijo al inicio o al final (como el símbolo de moneda) sin tocar el resto:

```python
precio = "Bs 12,50"
print(precio.removeprefix("Bs"))
print(precio.removeprefix("Bs").strip())
print("R01-Norte".removesuffix("-Norte"))
```

```salida
 12,50
12,50
R01
```

`removeprefix` y `removesuffix` solo quitan el texto indicado si está **al inicio / al final**; si no está, devuelven el texto sin cambios (a diferencia de `replace`, que cambia todas las apariciones en cualquier lugar). Después de quitar `"Bs"` queda un espacio, que se limpia con `strip()`.

**6. Partir y unir.** `split` parte un texto en una lista de pedazos; `join` hace lo contrario:

```python
linea = "1,Tienda La Palma,R01,Norte"
partes = linea.split(",")
print(partes)
print(partes[1])
print(" | ".join(partes))
```

```salida
['1', 'Tienda La Palma', 'R01', 'Norte']
Tienda La Palma
1 | Tienda La Palma | R01 | Norte
```

`split(",")` usa la coma como separador y devuelve una **lista** (la verás en la lección 7.8). Así se lee a mano una línea de un CSV, aunque para archivos reales usarás el módulo `csv` (lección 8.3).

**7. Montos escritos como texto.** El caso más peligroso del curso: cuánto es «11,50»? Si solo quitas la coma:

```python
monto = "11,50"
print(monto.replace(",", ""))
print(monto.replace(",", "."))
```

```salida
1150
11.50
```

Quitar la coma da `1150` (¡cien veces más!). Cambiarla por un punto da `11.50`, que es lo que quieres si la coma era el separador decimal. Pero si el monto fuera `1.234,50` (mil doscientos treinta y cuatro con cincuenta), habría que quitar primero el punto de los miles y luego cambiar la coma. **Antes de limpiar un número, averigua en qué formato viene.** Lo convertirás a número en la lección 7.7.

**8. f-strings para presentar.**

```python
tienda = "Kiosco Luna"
total = 1234.5
print(f"{tienda}: Bs {total}")
print(f"{tienda}: Bs {total:.2f}")
print(f"{tienda}: Bs {total:,.2f}")
print(f"Cumplimiento: {78.5714:.1f}%")
```

```salida
Kiosco Luna: Bs 1234.5
Kiosco Luna: Bs 1234.50
Kiosco Luna: Bs 1,234.50
Cumplimiento: 78.6%
```

Dentro de las llaves va una expresión. Después de los dos puntos se escribe el **formato**: `.2f` significa «float con 2 decimales», y la coma (`,.2f`) agrega separador de miles, pero con **coma** como en inglés (1,234.50). Para el formato boliviano (1.234,50) hay que intercambiar los símbolos después; si el reporte lo exige, hazlo con `replace` y documéntalo.

Ejemplo comercial: tres códigos de ruta llegaron como `" r01"`, `"R01 "` y `"R01"`. Son la misma ruta, pero para Python son tres textos distintos. Con `.strip().upper()` los tres se convierten en `"R01"` y recién ahí puedes agrupar y contar sin duplicar categorías.

## Errores comunes

- **No guardar el resultado de un método** (`texto.strip()` sin asignar).
- **Quitar la coma de un monto** y obtener un número cien veces mayor.
- **Contar índices desde 1**: el primer carácter es el 0.
- **Olvidar que el fin de una rebanada no se incluye.**
- **Comparar textos con distinta mayúscula** (`"R01" == "r01"` es `False`).
- **Pedir un índice que no existe** (`"Sol"[5]`): `IndexError`.
- **Olvidar la `f`** antes de las comillas en un f-string: las llaves se imprimen tal cual.

## Para comprobar que entendiste

1. ¿Qué devuelve `"Norte"[1:3]`?
2. ¿Por qué `texto.upper()` solo no cambia la variable `texto`?
3. ¿Qué hace `"a-b-c".split("-")`?
4. ¿Qué formato da dos decimales dentro de un f-string?

<details><summary>Respuestas</summary>

1. `"or"` (índices 1 y 2).
2. Porque los textos son inmutables: el método devuelve un texto nuevo y hay que asignarlo.
3. Devuelve la lista `["a", "b", "c"]`.
4. `{valor:.2f}`.

</details>

## Micropráctica

1. Limpia el texto `"  zona CENTRO "` para que quede en mayúsculas y sin espacios en los extremos. Muestra el resultado entre corchetes.
2. Dado `fecha = "2026-09-18"`, extrae con rebanadas el año, el mes y el día en tres variables y muéstralos como `18/09/2026`.
3. Convierte el texto `"1.234,50"` en el texto `"1234.50"` (pista: dos reemplazos, en el orden correcto).
4. Escribe un f-string que muestre `Ruta R02: 450.0 Bs (meta 600.0 Bs)` a partir de tres variables.

Cómo saber que está bien: en la 1 ves `[ZONA CENTRO]`; en la 2 `18/09/2026`; en la 3 `1234.50`.

<details><summary>Comprobación de las partes 1 a 3</summary>

```python
print("[" + "  zona CENTRO ".strip().upper() + "]")

fecha = "2026-09-18"
anio = fecha[0:4]
mes = fecha[5:7]
dia = fecha[8:10]
print(f"{dia}/{mes}/{anio}")

texto = "1.234,50"
print(texto.replace(".", "").replace(",", "."))
```

```salida
[ZONA CENTRO]
18/09/2026
1234.50
```

</details>

## Después, en los ejercicios

Los métodos de texto son la base de P03 y P10 en [Python](../../03_EJERCICIOS/Python/) y del paso de limpieza de cualquier ETL. Siguiente: [7.6 Booleanos, comparaciones y None](06_booleanos_comparaciones_none.md).
