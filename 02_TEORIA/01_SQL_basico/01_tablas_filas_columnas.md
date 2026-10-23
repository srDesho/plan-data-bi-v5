# 1.1 Tablas, filas, columnas y tipos de datos

> Tiempo estimado: 45 min (lectura 20 + práctica 25). No necesitas saber nada antes. Es la primera lección de SQL.

## Para qué sirve

Casi toda la información de una empresa vive en tablas: ventas, clientes, productos, visitas. Antes de escribir una sola consulta necesitas leer una tabla como la lee un analista: saber qué representa cada fila, qué dice cada columna y de qué tipo es cada dato. Si no lo tienes claro, puedes escribir una consulta que funcione y responder la pregunta equivocada.

Se usa siempre: es el primer paso antes de cualquier consulta, reporte o ETL.

## Términos nuevos

- **Base de datos**: un archivo (o un servidor) que guarda tablas organizadas y relacionadas entre sí. En este curso usas SQLite: la base completa es un solo archivo, por ejemplo `mini_base.db`.
- **Tabla**: un conjunto de datos con forma de cuadrícula. Cada tabla trata de *un solo tipo de cosa*: una tabla de tiendas, una tabla de ventas.
- **Fila** (también *registro*): una línea de la tabla. Representa *una* cosa concreta: una tienda, una venta.
- **Columna** (también *campo*): una propiedad que tienen todas las filas, como el nombre o la zona. Todas las filas tienen las mismas columnas.
- **Tipo de dato**: la clase de valor que acepta una columna. SQLite usa sobre todo `INTEGER` (enteros, como 12), `REAL` (decimales, como 6.5) y `TEXT` (texto, como 'Norte'). Las fechas se guardan como `TEXT` con el formato `AAAA-MM-DD`.
- **Clave primaria**: la columna (o grupo de columnas) cuyo valor identifica una fila y nunca se repite. Es como el número de carnet de una persona.
- **NULL**: la marca de "no hay valor". No es cero ni es texto vacío: significa que el dato falta o no se conoce.
- **Granularidad**: qué representa exactamente una fila de una tabla. En una tabla de ventas con una fila por venta, la granularidad es "una venta". Es la pregunta más importante de esta lección.
- **Consulta**: una instrucción escrita en **SQL** (el lenguaje para pedirle datos a una base de datos). Una consulta no cambia la tabla: solo lee.

## Ejemplo paso a paso

Usamos la mini-base de las lecciones (`04_DATASETS/mini_base/`, ver su README). Es una distribuidora inventada con tiendas, artículos y ventas. Para ver el contenido de una tabla pedimos "todas las columnas, solo las primeras 5 filas":

```sql
SELECT * FROM tiendas LIMIT 5;
```

```resultado
tienda_id | nombre | tipo | zona | ruta | fecha_alta
1 | Tienda La Palma | Tienda de barrio | Norte | R01 | 2025-02-10
2 | Kiosco El Faro | Kiosco | Centro | R01 | 2025-03-01
3 | Farmacia Salud | Farmacia | Centro | R02 | 2025-03-15
4 | Minimarket Sol Naciente | Minimarket | Norte | R02 | 2025-05-20
5 |   Kiosco La Esquina  | Kiosco | NULL | R03 | 2025-06-02
```

Paso a paso:

1. `SELECT *` significa "elige todas las columnas". El `*` es un atajo para "todas".
2. `FROM tiendas` dice de qué tabla leer.
3. `LIMIT 5` corta el resultado en 5 filas, para no llenar la pantalla.
4. El `;` marca el final de la instrucción.

Cómo se lee el resultado:

- La primera línea son los **nombres de columna**: `tienda_id`, `nombre`, `tipo`, `zona`, `ruta`, `fecha_alta`.
- Cada línea siguiente es una **fila**: la fila con `tienda_id` 1 es "Tienda La Palma", de tipo "Tienda de barrio", en la zona Norte, ruta R01, dada de alta el 10 de febrero de 2025.
- `tienda_id` es la clave primaria: cada tienda tiene un número distinto, aunque dos tiendas tengan el mismo nombre.
- Mira la fila 5: la zona dice `NULL`. Esa tienda no tiene zona registrada. No es "cero" ni "vacío": es **desconocido**. Más adelante verás por qué esto cambia los resultados.
- Mira también el nombre de la fila 5: tiene espacios al principio y al final. Los datos reales vienen así de sucios; ya aprenderás a limpiarlos.

Ahora veamos los tipos de cada columna con `PRAGMA table_info`, una instrucción propia de SQLite que describe una tabla:

```sql
PRAGMA table_info(articulos);
```

```resultado
cid | name | type | notnull | dflt_value | pk
0 | articulo_id | INTEGER | 0 | NULL | 1
1 | nombre | TEXT | 0 | NULL | 0
2 | categoria | TEXT | 0 | NULL | 0
3 | precio | REAL | 0 | NULL | 0
```

Cada fila de este resultado describe *una columna* de `articulos`. Lo que importa para ti: la columna `name` (nombre de la columna), `type` (su tipo) y `pk` (vale 1 si es la clave primaria). Aquí `articulo_id` es INTEGER y clave primaria; `nombre` y `categoria` son TEXT; `precio` es REAL porque tiene decimales.

Por último, la granularidad. Compara dos tablas:

```sql
SELECT * FROM ventas LIMIT 3;
```

```resultado
venta_id | tienda_id | vendedor_id | fecha | estado
1 | 1 | 1 | 2026-08-03 | entregado
2 | 2 | 1 | 2026-08-05 | entregado
3 | 3 | 2 | 2026-08-07 | entregado
```

```sql
SELECT * FROM venta_lineas LIMIT 4;
```

```resultado
linea_id | venta_id | articulo_id | cantidad | precio_unitario
1 | 1 | 1 | 10 | 6.0
2 | 1 | 4 | 6 | 7.5
3 | 1 | 9 | 4 | 8.0
4 | 2 | 3 | 8 | 11.5
```

- En `ventas`, **una fila es una venta**: una tienda, un vendedor, una fecha y un estado. La venta 1 la hizo la tienda 1.
- En `venta_lineas`, **una fila es un artículo dentro de una venta**. Las filas 1, 2 y 3 tienen `venta_id = 1`: la venta 1 tenía tres artículos distintos.
- Por eso `venta_lineas` tiene más filas que `ventas`. Si mezclas las dos sin cuidado contarás una venta tres veces. Este es el error silencioso más frecuente en SQL y lo tratarás en detalle en la lección de JOIN.

Ejemplo comercial: el gerente pregunta "¿cuántas ventas tuvimos?". Si respondes contando filas de `venta_lineas` das un número inflado, porque cada venta aparece una vez por artículo. Saber qué representa una fila evita esa respuesta incorrecta.

## Errores comunes

- **Confundir tabla con columna.** `tiendas` es una tabla; `zona` es una columna de esa tabla. Escribir `FROM zona` falla.
- **Creer que NULL es cero o texto vacío.** NULL significa "sin dato". Una zona NULL y una zona `''` (texto vacío) son cosas distintas.
- **Olvidar el `;`.** Algunas herramientas lo toleran, otras se quedan esperando. Acostúmbrate a escribirlo.
- **Escribir mal el nombre de la tabla o columna.** Verás `no such table` o `no such column`. Revisa la ortografía con `PRAGMA table_info(nombre_tabla);`.
- **No preguntarse qué es una fila.** Un resultado correcto de una pregunta equivocada es el error más caro.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre una fila y una columna?
2. ¿Para qué sirve la clave primaria? ¿Podría haber dos tiendas con el mismo `tienda_id`?
3. En `venta_lineas`, ¿qué representa una fila?
4. La zona de la tienda 8 es NULL. ¿Significa que su zona es 0?

<details><summary>Respuestas</summary>

1. Una fila es un registro completo (una tienda); una columna es una propiedad que todas las filas comparten (la zona).
2. Identifica de forma única cada fila; no puede haber dos tiendas con el mismo `tienda_id`. Sí puede haber dos con el mismo nombre.
3. Un artículo dentro de una venta (una línea de detalle).
4. No. Significa que la zona no está registrada o no se conoce.

</details>

<a id="micropractica"></a>

## Micropráctica

Sin copiar de arriba, hazlo tú y anota lo que ves:

1. Muestra las primeras 3 filas de `articulos`.
2. Describe con `PRAGMA table_info` la tabla `metas` y escribe, con tus palabras, qué representa una fila de `metas` y qué columnas la identifican.
3. Con `SELECT * FROM visitas_ej LIMIT 3;` anota qué representa una fila y qué significan las columnas `planificada`, `realizada` y `pedido_tomado` (pista: solo tienen valores 0 y 1).

Cómo saber que está bien: la consulta 1 devuelve 3 filas y 4 columnas; `metas` no tiene columna de identificador: una fila queda identificada por el par `mes` y `ruta`.

<details><summary>Comprobación de la consulta 1</summary>

```sql
SELECT * FROM articulos LIMIT 3;
```

```resultado
articulo_id | nombre | categoria | precio
1 | Agua 2L | Bebidas | 6.0
2 | Jugo 1L | Bebidas | 9.0
3 | Gaseosa 2L | Bebidas | 11.5
```

</details>

## Después, en los ejercicios

Con esta lección puedes empezar la serie S de los ejercicios de SQL (`03_EJERCICIOS/SQL/S1.md` en adelante): [índice de ejercicios SQL](../../03_EJERCICIOS/SQL/INDICE.md). Antes de escribir cada consulta, responde primero: ¿qué representa una fila de la tabla que voy a usar?

Siguiente: [1.2 SELECT, FROM y alias](02_select_from_alias.md).
