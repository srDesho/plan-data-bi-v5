# 3.3 LEFT JOIN: conservar todo lo de la izquierda y encontrar a los que no aparecen

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisito: [3.2 INNER JOIN](02_inner_join.md).

## Para qué sirve

Con `INNER JOIN` solo aparecen las coincidencias. Pero muchas preguntas de negocio son sobre quien **no** aparece: tiendas que no compraron, clientes sin visita, artículos que no se vendieron. Esas preguntas no se pueden responder con INNER JOIN, porque justamente las filas que buscas son las que desaparecen. `LEFT JOIN` mantiene todas las filas de la tabla izquierda aunque no tengan pareja.

## Términos nuevos

- **LEFT JOIN**: conserva **todas** las filas de la tabla de la izquierda (la que va en `FROM`) y trae los datos de la derecha cuando hay coincidencia; si no la hay, esas columnas salen `NULL`.
- **Tabla izquierda / derecha**: la que escribes antes / después de la palabra `JOIN`.
- **Anti-join**: patrón para hallar las filas de la izquierda **sin** pareja a la derecha: `LEFT JOIN ... WHERE derecha.clave IS NULL`.
- **Filas sin coincidencia**: las filas de la izquierda para las que el `ON` no encontró nada. Aparecen con todas las columnas de la derecha en `NULL`.

## Ejemplo paso a paso

**1. INNER contra LEFT.** Cantidad de tiendas con su cantidad de ventas. Primero con INNER JOIN:

```sql
SELECT COUNT(DISTINCT t.tienda_id) AS tiendas_con_ventas
FROM tiendas AS t
INNER JOIN ventas AS v ON v.tienda_id = t.tienda_id;
```

```resultado
tiendas_con_ventas
9
```

Solo 9 de las 12 tiendas tienen alguna venta; las otras 3 no aparecen en este resultado. Con `LEFT JOIN` se conservan:

```sql
SELECT t.tienda_id, t.nombre, v.venta_id
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id
WHERE t.tienda_id IN (8, 9, 11)
ORDER BY t.tienda_id, v.venta_id;
```

```resultado
tienda_id | nombre | venta_id
8 | Farmacia Vida | NULL
9 | Minimarket Central | 12
9 | Minimarket Central | 13
11 | Tienda Nueva Esperanza | NULL
```

Mira las tiendas 8 y 11: aparecen **una vez** con `venta_id = NULL`, porque no tienen ventas. La tienda 9, que sí compró, aparece una vez por cada venta (dos ventas, dos filas).

**2. El anti-join: ¿qué tiendas no compraron nunca?** Es el patrón central de esta lección:

```sql
SELECT t.tienda_id, t.nombre
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id
WHERE v.venta_id IS NULL
ORDER BY t.tienda_id;
```

```resultado
tienda_id | nombre
8 | Farmacia Vida
11 | Tienda Nueva Esperanza
12 | Restaurante El Buen Gusto
```

Cómo funciona: el `LEFT JOIN` agrega `NULL` en las columnas de `ventas` para las tiendas sin ventas; el `WHERE v.venta_id IS NULL` se queda justo con esas. Usamos la clave primaria `venta_id` de la tabla de la derecha para detectar la ausencia: una venta real nunca tiene `venta_id` NULL.

**3. Contar con ceros.** Cantidad de ventas por tienda, incluyendo las tiendas con 0:

```sql
SELECT t.tienda_id, COUNT(v.venta_id) AS ventas
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id
GROUP BY t.tienda_id
ORDER BY ventas DESC, t.tienda_id;
```

```resultado
tienda_id | ventas
1 | 3
3 | 3
2 | 2
4 | 2
9 | 2
5 | 1
6 | 1
7 | 1
10 | 1
8 | 0
11 | 0
12 | 0
```

Ahora sí aparecen las 12 tiendas, incluso las de 0 ventas. Fíjate en que contamos `COUNT(v.venta_id)`, **no** `COUNT(*)`. Prueba la diferencia:

```sql
SELECT t.tienda_id, COUNT(*) AS filas, COUNT(v.venta_id) AS ventas
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id
WHERE t.tienda_id = 8
GROUP BY t.tienda_id;
```

```resultado
tienda_id | filas | ventas
8 | 1 | 0
```

La tienda 8 tiene **1 fila** (la fila de la tienda con NULL a la derecha) pero **0 ventas**. `COUNT(*)` cuenta esa fila vacía como si fuera una venta; `COUNT(columna_de_la_derecha)` ignora los NULL y cuenta bien. Es el error más común con LEFT JOIN.

**4. Filtro en `ON` frente a filtro en `WHERE`.** Queremos todas las tiendas, con la cantidad de ventas **anuladas** que tienen (0 si no tienen). Mira dos versiones:

```sql
SELECT t.tienda_id, COUNT(v.venta_id) AS anuladas
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id AND v.estado = 'anulado'
GROUP BY t.tienda_id
ORDER BY anuladas DESC, t.tienda_id
LIMIT 4;
```

```resultado
tienda_id | anuladas
4 | 1
9 | 1
1 | 0
2 | 0
```

```sql
SELECT t.tienda_id, COUNT(v.venta_id) AS anuladas
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id
WHERE v.estado = 'anulado'
GROUP BY t.tienda_id
ORDER BY anuladas DESC, t.tienda_id;
```

```resultado
tienda_id | anuladas
4 | 1
9 | 1
```

La primera pone el filtro `estado = 'anulado'` dentro del `ON`: el LEFT JOIN conserva todas las tiendas y solo «trae» las ventas anuladas. Las tiendas 4 y 9 salen con 1 y el resto con 0 (aquí vemos las primeras 4 filas). La segunda pone el filtro en `WHERE`, y el `WHERE` se evalúa **después** del join: las tiendas sin ventas tienen `estado = NULL`, la condición no es verdadera y la fila se pierde. Resultado: solo 2 filas. **Regla: si quieres conservar las filas sin coincidencia, los filtros sobre la tabla de la derecha van en el `ON`**, no en el `WHERE`.

**5. Artículos que nunca se vendieron.**

```sql
SELECT a.articulo_id, a.nombre
FROM articulos AS a
LEFT JOIN venta_lineas AS l ON l.articulo_id = a.articulo_id
WHERE l.linea_id IS NULL;
```

```resultado
articulo_id | nombre
```

Sin filas: todos los artículos se han vendido al menos una vez. Un resultado vacío también es una respuesta válida: significa «no hay ausentes».

Ejemplo comercial: «clientes que no compraron en septiembre» es un anti-join con el filtro de fecha en el `ON`. Si pones la fecha en el `WHERE` pierdes justo a los clientes que buscas. Y recuerda que «no compró» y «nunca compró» son preguntas diferentes: decide cuál te piden.

## Errores comunes

- **Filtrar la tabla derecha en `WHERE`** y convertir sin querer el LEFT JOIN en un INNER JOIN.
- **`COUNT(*)` en lugar de `COUNT(columna_derecha)`**: cuenta las filas vacías como ventas.
- **Invertir izquierda y derecha**: un `LEFT JOIN` con las tablas al revés busca otra cosa.
- **Detectar ausentes con una columna que puede ser NULL por sí misma**: usa la clave primaria de la tabla derecha.
- **Olvidar que un resultado vacío es válido.**
- **Dar a un anti-join la interpretación equivocada**: «sin ventas» en esta tabla no significa «sin ventas en la empresa» si faltan datos.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre INNER JOIN y LEFT JOIN?
2. ¿Qué valores tienen las columnas de la derecha para una fila sin coincidencia?
3. ¿Por qué se usa `COUNT(v.venta_id)` y no `COUNT(*)` en un LEFT JOIN?
4. ¿Dónde va el filtro `estado = 'anulado'` para no perder tiendas sin ventas?

<details><summary>Respuestas</summary>

1. INNER solo conserva coincidencias; LEFT conserva todas las filas de la izquierda.
2. NULL.
3. Porque `COUNT(*)` cuenta la fila vacía como 1, y `COUNT(v.venta_id)` ignora los NULL y cuenta 0.
4. En el `ON` del LEFT JOIN.

</details>

## Micropráctica

1. Lista los vendedores (`vendedores_ej`) que no tienen ninguna venta en `ventas`.
2. Cuenta las visitas realizadas por tienda en `visitas_ej`, incluyendo las tiendas sin ninguna visita, y ordena de mayor a menor.
3. Lista las tiendas que **no tuvieron ninguna venta entregada**.

Cómo saber que está bien: la 1 devuelve 1 vendedor (Pedro); en la 2 aparecen las 12 tiendas; la 3 devuelve aquí las 3 tiendas sin ventas. Las tiendas 4 y 9 tienen una venta anulada, pero también tienen ventas entregadas, por eso no aparecen; con otros datos la consulta traería además a las tiendas que solo tuvieron ventas anuladas.

<details><summary>Comprobación de las consultas 1 y 3</summary>

```sql
SELECT vd.vendedor_id, vd.nombre
FROM vendedores_ej AS vd
LEFT JOIN ventas AS v ON v.vendedor_id = vd.vendedor_id
WHERE v.venta_id IS NULL;
```

```resultado
vendedor_id | nombre
4 | Pedro
```

```sql
SELECT t.tienda_id, t.nombre
FROM tiendas AS t
LEFT JOIN ventas AS v ON v.tienda_id = t.tienda_id AND v.estado = 'entregado'
WHERE v.venta_id IS NULL
ORDER BY t.tienda_id;
```

```resultado
tienda_id | nombre
8 | Farmacia Vida
11 | Tienda Nueva Esperanza
12 | Restaurante El Buen Gusto
```

</details>

## Después, en los ejercicios

Los ejercicios con «sin ventas», «sin visitas», «que no» o «nunca» de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) son anti-joins. Antes de escribir, decide qué tabla es la izquierda (la que quieres conservar completa) y dónde va cada filtro.

Siguiente: [3.4 Cuando el JOIN duplica](04_duplicacion_por_join.md).
