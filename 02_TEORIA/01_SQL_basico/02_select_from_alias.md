# 1.2 SELECT, FROM, alias y columnas calculadas

> Tiempo estimado: 45 min (lectura 15 + práctica 30). Prerrequisito: [1.1 Tablas, filas y columnas](01_tablas_filas_columnas.md).

## Para qué sirve

Casi nunca necesitas todas las columnas de una tabla. Un reporte para el gerente pide tres o cuatro datos, con nombres claros y, a veces, un valor que no existe en la tabla y hay que calcular (por ejemplo, el subtotal de una línea de venta). `SELECT` elige qué columnas ver, `FROM` dice de dónde salen y un **alias** les pone un nombre legible.

## Términos nuevos

- **Cláusula**: cada parte de una consulta que empieza con una palabra reservada (`SELECT`, `FROM`, `WHERE`...). Una consulta se arma juntando cláusulas.
- **SELECT**: la cláusula que lista las columnas (o cálculos) que quieres en el resultado.
- **FROM**: la cláusula que nombra la tabla de donde se leen las filas.
- **Alias**: un nombre nuevo, temporal, que le das a una columna del resultado con `AS`. No cambia la tabla; solo cambia el título de esa columna en lo que ves.
- **Expresión calculada**: una columna del resultado que no existe en la tabla y se obtiene operando con otras (por ejemplo, `cantidad * precio_unitario`).
- **Operador aritmético**: `+`, `-`, `*`, `/`. Operan columna por columna, fila por fila.

## Ejemplo paso a paso

**1. Elegir columnas.** Del listado de tiendas queremos solo el nombre y la zona:

```sql
SELECT nombre, zona FROM tiendas;
```

```resultado
nombre | zona
Tienda La Palma | Norte
Kiosco El Faro | Centro
Farmacia Salud | Centro
Minimarket Sol Naciente | Norte
  Kiosco La Esquina  | NULL
Restaurante Sabor | Equipetrol
Tienda Don Pepe | Plan 3000
Farmacia Vida | NULL
Minimarket Central | Centro
Kiosco Luna | Norte
Tienda Nueva Esperanza | Plan 3000
Restaurante El Buen Gusto | Centro
```

Se lee: "de la tabla `tiendas`, trae las columnas `nombre` y `zona`". El orden en que las escribes en `SELECT` es el orden en que aparecen. Las columnas se separan con coma, y **no hay coma después de la última**. Vuelven las 12 filas porque aún no pusimos ningún filtro.

**2. Cambiar el orden o repetir columnas.** El orden del `SELECT` no tiene que respetar el de la tabla:

```sql
SELECT zona, nombre, ruta FROM tiendas LIMIT 4;
```

```resultado
zona | nombre | ruta
Norte | Tienda La Palma | R01
Centro | Kiosco El Faro | R01
Centro | Farmacia Salud | R02
Norte | Minimarket Sol Naciente | R02
```

**3. Alias con AS.** Los nombres de columna de la base a veces son técnicos. Con `AS` el reporte queda legible:

```sql
SELECT nombre AS tienda, ruta AS ruta_asignada FROM tiendas LIMIT 4;
```

```resultado
tienda | ruta_asignada
Tienda La Palma | R01
Kiosco El Faro | R01
Farmacia Salud | R02
Minimarket Sol Naciente | R02
```

Ahora los títulos del resultado son `tienda` y `ruta_asignada`, pero la tabla `tiendas` sigue igual. Si el alias lleva espacios, ponlo entre comillas dobles: `AS "ruta asignada"`. Es más cómodo evitar espacios y usar guion bajo.

**4. Columna calculada.** En `venta_lineas` cada fila tiene `cantidad` y `precio_unitario`. El importe de la línea (en Bs) no está guardado; lo calculamos:

```sql
SELECT linea_id, cantidad, precio_unitario, cantidad * precio_unitario AS subtotal
FROM venta_lineas
LIMIT 5;
```

```resultado
linea_id | cantidad | precio_unitario | subtotal
1 | 10 | 6.0 | 60.0
2 | 6 | 7.5 | 45.0
3 | 4 | 8.0 | 32.0
4 | 8 | 11.5 | 92.0
5 | 12 | 4.5 | 54.0
```

Línea por línea:

1. `SELECT linea_id, cantidad, precio_unitario` trae tres columnas tal cual.
2. `cantidad * precio_unitario AS subtotal` multiplica, **en cada fila**, las dos columnas y llama `subtotal` al resultado. En la fila 1: 10 unidades a Bs 6,00 son Bs 60.
3. `FROM venta_lineas` indica la tabla; `LIMIT 5` corta a 5 filas.
4. Comprobación a mano de la fila 2: 6 unidades × Bs 7,50 = Bs 45. El resultado debe coincidir. **Siempre verifica una fila a mano** cuando creas una columna calculada.

**5. Mezclar columnas y valores fijos.** Un valor fijo se repite en todas las filas. Sirve para etiquetar:

```sql
SELECT nombre, precio, precio * 12 AS precio_docena, 'Bs' AS moneda
FROM articulos
LIMIT 3;
```

```resultado
nombre | precio | precio_docena | moneda
Agua 2L | 6.0 | 72.0 | Bs
Jugo 1L | 9.0 | 108.0 | Bs
Gaseosa 2L | 11.5 | 138.0 | Bs
```

Texto fijo va entre **comillas simples** (`'Bs'`). Las comillas dobles se usan para nombres de columna o alias, no para texto.

Ejemplo comercial: el jefe de ventas pide "tienda, ruta y el importe de cada línea" para revisar a mano. La respuesta es una consulta de dos o tres líneas como las de arriba, no un `SELECT *` con todo.

## Errores comunes

- **Coma de más antes de `FROM`**: `SELECT nombre, FROM tiendas;` produce un error de sintaxis. Sobra la coma final.
- **Falta de coma entre columnas**: `SELECT nombre zona FROM tiendas;` no falla: SQLite interpreta `zona` como alias de `nombre` y solo devuelve una columna con título equivocado. Es un error silencioso.
- **Comillas dobles para texto**: `'Bs'` es texto; `"Bs"` se interpreta como un nombre de columna (y en algunas bases falla).
- **Usar `SELECT *` por costumbre**: sirve para explorar. En un reporte, nombra las columnas que necesitas para controlar el resultado.
- **Alias igual al de otra columna**: confunde al leer. Escoge alias que digan qué es el dato.
- **No verificar una fila calculada a mano**: si multiplicaste la columna equivocada nadie te avisa.

## Para comprobar que entendiste

1. ¿Qué cambia `AS` y qué no cambia?
2. ¿Qué devuelve `SELECT nombre zona FROM tiendas;` y por qué es peligroso?
3. En `cantidad * precio_unitario`, ¿cuántas veces se hace la multiplicación en una tabla de 39 filas?
4. ¿Cuándo van comillas simples y cuándo dobles?

<details><summary>Respuestas</summary>

1. Cambia el título de la columna en el resultado; no cambia la tabla ni los datos.
2. Una sola columna, con los nombres de las tiendas, titulada `zona`. Es peligroso porque no da error y parece correcto.
3. 39 veces: una por fila.
4. Simples para valores de texto; dobles (si hacen falta) para nombres de columnas o alias con espacios.

</details>

## Micropráctica

Sobre `articulos` y `venta_lineas` escribe, sin copiar los ejemplos:

1. Nombre y categoría de todos los artículos, con los alias `producto` y `familia`.
2. Para las primeras 6 líneas de `venta_lineas`: `linea_id`, `venta_id` y el subtotal.
3. Para `articulos`: nombre y el precio de media docena (6 unidades) con alias `precio_media_docena`.

Cómo saber que está bien: la 1 devuelve 10 filas y 2 columnas; la 2, 6 filas con un subtotal de Bs 60 en la primera; la 3, 10 filas y la primera fila (Agua 2L) vale 36.

<details><summary>Comprobación de la consulta 3</summary>

```sql
SELECT nombre, precio * 6 AS precio_media_docena FROM articulos LIMIT 3;
```

```resultado
nombre | precio_media_docena
Agua 2L | 36.0
Jugo 1L | 54.0
Gaseosa 2L | 69.0
```

</details>

## Después, en los ejercicios

Aplica esta lección en la serie S de [los ejercicios SQL](../../03_EJERCICIOS/SQL/INDICE.md) (S1–S10): cada enunciado pide columnas concretas, con alias y a veces una columna calculada.

Siguiente: [1.3 WHERE y operadores](03_where_operadores.md).
