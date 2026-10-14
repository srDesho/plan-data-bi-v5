# 3.2 INNER JOIN: combinar tablas por coincidencia

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisito: claves y cardinalidad, introducidas a continuación; [3.1 Claves y relaciones](01_claves_relaciones.md) queda como REFUERZO.

## Para qué sirve

`ventas` dice qué tienda compró; `tiendas` dice cómo se llama y en qué zona está. Para un reporte «ventas por zona» necesitas ambos datos en la misma fila. `JOIN` hace esa unión: lee dos tablas y devuelve una fila por cada pareja de filas que cumple una condición.

## Términos nuevos

- **Clave primaria**: identifica una sola fila; sus valores no se repiten ni están vacíos. En `tiendas` es `tienda_id`.
- **Clave foránea**: referencia la clave de otra tabla. `ventas.tienda_id` indica a qué tienda pertenece cada venta; puede repetirse porque una tienda puede tener varias ventas.
- **Cardinalidad**: cuántas filas de un lado corresponden a una del otro. Tienda → ventas es **1:N**; ventas → tienda es **N:1**. El sentido importa: al traer el nombre de la tienda, cada venta debe encontrar una sola fila.
- **JOIN** (o **INNER JOIN**): une dos tablas y conserva solo las filas que tienen coincidencia en **ambas**.
- **ON**: la cláusula que dice cuándo dos filas coinciden. Normalmente iguala una clave foránea con una clave primaria.
- **Alias de tabla**: un nombre corto para la tabla dentro de la consulta: `FROM ventas AS v`.
- **Columna calificada**: una columna escrita con el alias de su tabla (`v.fecha`). Es obligatoria cuando dos tablas tienen una columna con el mismo nombre.
- **Producto cartesiano**: el resultado de combinar *cada* fila de una tabla con *cada* fila de la otra, sin condición. Con 12 y 16 filas da 192. Casi nunca es lo que quieres.

## Ejemplo paso a paso

**Antes de unir: identificar las claves y comprobar el lado «uno».** Sin escribir todavía el JOIN, completa en voz alta: «una fila de `ventas` representa ___; su `tienda_id` puede repetirse porque ___; en `tiendas`, `tienda_id` debe ser ___». Comprueba esa última condición con la mini-base:

```sql
SELECT tienda_id, COUNT(*) AS veces
FROM tiendas
GROUP BY tienda_id
HAVING COUNT(*) > 1;
```

```resultado
tienda_id | veces
```

No devuelve filas: no hay claves repetidas. Si devolviera alguna, una venta podría encontrar varias tiendas y multiplicarse. Las claves vacías tampoco identifican una tienda. Antes de continuar, predice qué pasaría con una venta cuya tienda no existe: el INNER JOIN la descartaría. Por eso se revisan tanto la unicidad como las filas y totales después de unir.

**1. La unión más simple.** Cada venta con el nombre de su tienda:

```sql
SELECT v.venta_id, v.fecha, t.nombre AS tienda
FROM ventas AS v
INNER JOIN tiendas AS t ON t.tienda_id = v.tienda_id
ORDER BY v.venta_id
LIMIT 5;
```

```resultado
venta_id | fecha | tienda
1 | 2026-08-03 | Tienda La Palma
2 | 2026-08-05 | Kiosco El Faro
3 | 2026-08-07 | Farmacia Salud
4 | 2026-08-12 | Minimarket Sol Naciente
5 | 2026-08-19 | Tienda La Palma
```

Línea por línea:

1. `FROM ventas AS v` es la tabla principal; `v` es su alias.
2. `INNER JOIN tiendas AS t` indica la segunda tabla.
3. `ON t.tienda_id = v.tienda_id` es la condición: «une cada venta con la tienda cuyo `tienda_id` es igual».
4. En `SELECT` calificamos cada columna con su alias (`v.fecha`, `t.nombre`). `tienda_id` existe en las dos tablas: sin el alias SQL no sabría de cuál hablas.

El control inmediato: la cantidad de filas. Como en esta mini-base cada venta encuentra una sola tienda (relación N:1 desde ventas hacia tiendas), el resultado debe tener **tantas filas como ventas**:

```sql
SELECT COUNT(*) AS filas_tras_unir
FROM ventas AS v
INNER JOIN tiendas AS t ON t.tienda_id = v.tienda_id;
```

```resultado
filas_tras_unir
16
```

16, igual que las filas de `ventas`. Si hubiera salido otro número, algo se perdió o se multiplicó.

**2. Una unión que agrega.** Cantidad de ventas por zona de la tienda:

```sql
SELECT t.zona, COUNT(*) AS ventas
FROM ventas AS v
INNER JOIN tiendas AS t ON t.tienda_id = v.tienda_id
GROUP BY t.zona
ORDER BY ventas DESC, t.zona;
```

```resultado
zona | ventas
Centro | 7
Norte | 6
NULL | 1
Equipetrol | 1
Plan 3000 | 1
```

Observa el grupo `NULL`: son las ventas de las tiendas sin zona. El control: 7 + 6 + 1 + 1 + 1 debe dar 16, el número de ventas.

**3. Unir tres tablas.** El importe vendido por ruta de la tienda, **solo ventas entregadas**. Esto es lo que antes no se podía: `venta_lineas` no tiene estado ni tienda. Hay que unirla con `ventas` (para el estado) y con `tiendas` (para la ruta):

```sql
SELECT t.ruta, SUM(l.cantidad * l.precio_unitario) AS importe_bs
FROM venta_lineas AS l
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
INNER JOIN tiendas AS t ON t.tienda_id = v.tienda_id
WHERE v.estado = 'entregado'
GROUP BY t.ruta
ORDER BY t.ruta;
```

```resultado
ruta | importe_bs
R01 | 1265.0
R02 | 510.0
R03 | 557.5
```

Cada `JOIN` se apoya en el anterior: líneas → ventas (por `venta_id`) → tiendas (por `tienda_id`). El `WHERE` descarta las ventas anuladas **antes** de sumar. Control: los tres importes deben sumar el total entregado, que calculamos por otro camino (sin tiendas):

```sql
SELECT SUM(l.cantidad * l.precio_unitario) AS total_entregado_bs
FROM venta_lineas AS l
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
WHERE v.estado = 'entregado';
```

```resultado
total_entregado_bs
2332.5
```

Si los tres importes por ruta suman exactamente este total, la unión con `tiendas` no perdió ni multiplicó filas. Esa comparación de dos caminos es el control más barato y poderoso que tienes.

**4. Uniendo con el catálogo.** Importe por categoría de artículo (entregadas):

```sql
SELECT a.categoria, SUM(l.cantidad) AS unidades, SUM(l.cantidad * l.precio_unitario) AS importe_bs
FROM venta_lineas AS l
INNER JOIN articulos AS a ON a.articulo_id = l.articulo_id
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
WHERE v.estado = 'entregado'
GROUP BY a.categoria
ORDER BY importe_bs DESC;
```

```resultado
categoria | unidades | importe_bs
Bebidas | 135 | 1050.0
Lácteos | 54 | 528.0
Snacks | 95 | 523.5
Limpieza | 39 | 231.0
```

**5. El error de olvidar ON.** Una unión sin condición produce el producto cartesiano:

```sql
SELECT COUNT(*) AS filas
FROM ventas AS v, tiendas AS t;
```

```resultado
filas
192
```

16 × 12 = 192 filas: cada venta emparejada con cada tienda, correctas o no. Si ves que el resultado crece de forma absurda, busca la condición `ON` que falta o está mal escrita.

Ejemplo comercial: el gerente pide «ventas entregadas por ruta y vendedor». Unes líneas → ventas (estado, vendedor) → tiendas (ruta) → vendedores_ej (nombre). Cada paso es una relación 1:N hacia el lado «uno», así que el número de líneas no cambia.

## Errores comunes

- **Olvidar el `ON`** o escribirlo contra la columna equivocada.
- **No calificar las columnas repetidas**: error `ambiguous column name`.
- **Poner el filtro de estado en el lugar equivocado** o no ponerlo: sumas ventas anuladas.
- **Un INNER JOIN que descarta filas en silencio**: si una venta apunta a una tienda que no existe, desaparece del total. Compara siempre con el total sin unir.
- **Unir por una columna que no es clave** (visto en 3.1): las filas se multiplican.
- **No comprobar el número de filas después de unir.**

## Para comprobar que entendiste

1. ¿Qué filas conserva un INNER JOIN?
2. ¿Qué indica la condición `ON`?
3. ¿Por qué se usan alias como `v` y `t`?
4. ¿Cómo compruebas que unir `ventas` con `tiendas` no cambió el número de ventas?

<details><summary>Respuestas</summary>

1. Solo las que tienen coincidencia en ambas tablas.
2. Cuándo una fila de una tabla corresponde a una fila de la otra (normalmente clave foránea = clave primaria).
3. Para abreviar y para distinguir columnas con el mismo nombre en distintas tablas.
4. Cuento las filas antes y después: deben ser iguales (16) porque cada venta tiene una sola tienda.

</details>

## Micropráctica

1. Lista cada línea de la venta 3 con el nombre del artículo, la cantidad y el subtotal (unir `venta_lineas` con `articulos`).
2. Calcula las unidades vendidas por tipo de tienda (`tiendas.tipo`) **solo de ventas entregadas**, uniendo líneas → ventas → tiendas.
3. Comprueba con dos caminos distintos que la suma de las unidades por tipo de tienda es igual al total de unidades entregadas.

Cómo saber que está bien: la 1 devuelve 3 filas; en la 3 las dos cifras coinciden. Si no coinciden, tu unión perdió o multiplicó filas.

<details><summary>Comprobación de la consulta 1</summary>

```sql
SELECT a.nombre, l.cantidad, l.cantidad * l.precio_unitario AS subtotal
FROM venta_lineas AS l
INNER JOIN articulos AS a ON a.articulo_id = l.articulo_id
WHERE l.venta_id = 3
ORDER BY a.nombre;
```

```resultado
nombre | cantidad | subtotal
Detergente 1kg | 3 | 42.0
Jabón | 10 | 35.0
Jugo 1L | 6 | 54.0
```

</details>

## Después, en los ejercicios

Las series J y E de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) empiezan aquí. En cada una, después de escribir la consulta haz dos controles: el número de filas tras unir y el total por un camino alternativo.

Siguiente: [3.3 LEFT JOIN y los que no aparecen](03_left_join_ausentes.md).
