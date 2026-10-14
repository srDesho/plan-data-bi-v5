# 3.1 Claves, relaciones y cardinalidad

> Tiempo estimado: 45 min (lectura 20 + práctica 25). Prerrequisitos: [1.1 Tablas, filas y columnas](../01_SQL_basico/01_tablas_filas_columnas.md) y [2.2 GROUP BY](../02_SQL_agregados/02_group_by_having.md).

## Para qué sirve

Los datos de una empresa no viven en una sola tabla gigante: viven repartidos (tiendas por un lado, ventas por otro, detalle por otro) para no repetir la misma información cien veces. Para responder preguntas como «ventas por zona» necesitas **conectar** esas tablas. Antes de escribir un `JOIN` tienes que saber por qué columna se conectan y cuántas filas de una corresponden a cuántas de la otra. Si te equivocas ahí, los totales se multiplican sin avisar.

## Términos nuevos

- **Clave primaria** (ya la conoces): la columna cuyo valor identifica una sola fila y no se repite. En `tiendas` es `tienda_id`.
- **Clave foránea**: una columna que guarda la clave primaria de *otra* tabla y así «apunta» a una fila de ella. `ventas.tienda_id` apunta a `tiendas.tienda_id`.
- **Relación**: el vínculo entre dos tablas a través de una clave foránea.
- **Cardinalidad**: cuántas filas de una tabla pueden corresponder a una fila de la otra. Se escribe `1:1` (uno a uno), `1:N` (uno a muchos) o `N:M` (muchos a muchos).
- **Tabla puente**: una tabla intermedia que resuelve una relación muchos a muchos. `venta_lineas` conecta ventas con artículos.
- **Clave huérfana**: una clave foránea que no tiene fila correspondiente en la otra tabla (una venta que apunta a una tienda que no existe).
- **Clave compuesta**: una clave formada por más de una columna. En `metas` la fila queda identificada por `mes` + `ruta` juntas.

## Ejemplo paso a paso

El mapa de la mini-base es este (la flecha va de la clave foránea a la clave primaria):

```text
tiendas (tienda_id) <---- ventas (tienda_id)
vendedores_ej (vendedor_id) <---- ventas (vendedor_id)
ventas (venta_id) <---- venta_lineas (venta_id)
articulos (articulo_id) <---- venta_lineas (articulo_id)
metas: una fila por (mes, ruta)       visitas_ej (tienda_id) ----> tiendas
```

**1. Relación uno a muchos (1:N).** Una tienda puede tener muchas ventas, pero cada venta es de una sola tienda. ¿Cuántas ventas tiene cada tienda?

```sql
SELECT tienda_id, COUNT(*) AS ventas
FROM ventas
GROUP BY tienda_id
ORDER BY ventas DESC, tienda_id;
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
```

La tienda 1 aparece con varias ventas: del lado de `tiendas` es **una** fila; del lado de `ventas` son **varias**. La tabla del lado «uno» (`tiendas`) es la que tiene la clave primaria; la del lado «muchos» (`ventas`) tiene la clave foránea. Nota que faltan tiendas en este resultado: hay tiendas que no compraron nada. Lo recuperarás en la lección 3.3.

**2. Comprobar que una clave primaria no se repite.** Una consulta de control: ¿hay algún `tienda_id` que aparezca más de una vez?

```sql
SELECT tienda_id, COUNT(*) AS veces
FROM tiendas
GROUP BY tienda_id
HAVING COUNT(*) > 1;
```

```resultado
tienda_id | veces
```

Sin filas: no hay duplicados, así que `tienda_id` sirve de clave. **Esta consulta es un control que debes hacer antes de unir**: si una clave que crees única se repite, el JOIN multiplica filas.

**3. Una clave que NO es única.** `ruta` parece una buena columna para conectar tiendas con vendedores, pero:

```sql
SELECT ruta, COUNT(*) AS vendedores
FROM vendedores_ej
GROUP BY ruta
ORDER BY ruta;
```

```resultado
ruta | vendedores
R01 | 2
R02 | 1
R03 | 1
```

La ruta R01 tiene **dos** vendedores. Una columna que se repite no es una clave de la tabla `vendedores_ej`: si unes `tiendas` con `vendedores_ej` por `ruta`, cada tienda de R01 aparecerá dos veces. Lo verás en 3.4. La clave de `vendedores_ej` es `vendedor_id`.

**4. Clave compuesta.** En `metas`, ni `mes` ni `ruta` bastan por separado, pero juntas identifican la fila:

```sql
SELECT mes, ruta, COUNT(*) AS filas
FROM metas
GROUP BY mes, ruta
HAVING COUNT(*) > 1;
```

```resultado
mes | ruta | filas
```

Sin filas: cada par (mes, ruta) aparece una vez. La meta es una cifra por mes y ruta, no por tienda; recuerda esto cuando quieras comparar ventas con metas.

**5. Muchos a muchos con tabla puente.** Una venta tiene varios artículos y un artículo aparece en varias ventas. Esa relación N:M no cabe en ninguna de las dos tablas, por eso existe `venta_lineas`, con una fila por cada pareja (venta, artículo):

```sql
SELECT venta_id, articulo_id, cantidad
FROM venta_lineas
WHERE venta_id = 3
ORDER BY articulo_id;
```

```resultado
venta_id | articulo_id | cantidad
3 | 2 | 6
3 | 7 | 3
3 | 8 | 10
```

La venta 3 tiene tres artículos distintos, uno por fila. Por eso, al unir ventas con su detalle, cada venta se repetirá tantas veces como líneas tenga.

Ejemplo comercial: «ventas por zona de la tienda» necesita `ventas` (monto y fecha) y `tiendas` (zona); la conexión es `ventas.tienda_id = tiendas.tienda_id`, una relación 1:N donde cada venta encuentra exactamente una tienda. Esa es una unión segura. «Ventas contra metas» es otra cosa: la meta está a nivel de ruta y mes, no de tienda, y el cruce debe hacerse a esa granularidad.

## Errores comunes

- **Unir por una columna que no es clave** (nombre, ruta, categoría): el resultado se multiplica.
- **No saber del lado de cuál tabla está el «uno»**: antes de unir, di en voz alta «una fila de A corresponde a muchas/una de B».
- **Suponer que una clave es única sin comprobarlo**: haz la consulta de control `GROUP BY … HAVING COUNT(*) > 1`.
- **Ignorar las claves huérfanas**: un INNER JOIN las descarta en silencio y los totales bajan.
- **Confundir cardinalidad con cantidad de filas**: la cardinalidad describe la relación, no el tamaño de las tablas.
- **Unir por nombres de negocio** («Kiosco Luna»): pueden repetirse o venir con espacios.

## Para comprobar que entendiste

1. ¿Cuál es la clave primaria de `articulos` y cuál es la clave foránea de `venta_lineas`?
2. Describe la cardinalidad entre `tiendas` y `ventas`.
3. ¿Por qué `venta_lineas` se llama tabla puente?
4. ¿Qué haces antes de unir por una columna para saber si es segura?

<details><summary>Respuestas</summary>

1. La clave primaria es `articulo_id`; `venta_lineas` tiene dos claves foráneas: `venta_id` y `articulo_id`.
2. Uno a muchos (1:N): una tienda, muchas ventas.
3. Porque conecta ventas con artículos, que son una relación muchos a muchos.
4. Compruebo que no tenga duplicados con `GROUP BY ... HAVING COUNT(*) > 1`.

</details>

## Micropráctica

1. Escribe la consulta de control que demuestra que `venta_id` es única en `ventas`.
2. Cuenta cuántas líneas tiene cada venta (`venta_lineas`) y ordénalas de más a menos líneas, desempatando por `venta_id`. ¿Cuál es la venta con más líneas?
3. Dibuja (en papel) las relaciones entre `visitas_ej`, `tiendas` y `ventas`, e indica la cardinalidad de cada una.

Cómo saber que está bien: la 1 no devuelve filas; en la 2 hay ventas con 3 líneas (varias) y ventas con 1; en la 3, una tienda tiene muchas visitas y muchas ventas, de modo que visitas y ventas se relacionan entre sí **a través de** `tiendas` (no directamente).

<details><summary>Comprobación de la consulta 2</summary>

```sql
SELECT venta_id, COUNT(*) AS lineas
FROM venta_lineas
GROUP BY venta_id
ORDER BY lineas DESC, venta_id
LIMIT 5;
```

```resultado
venta_id | lineas
1 | 3
3 | 3
5 | 3
7 | 3
8 | 3
```

</details>

## Después, en los ejercicios

Antes de cada ejercicio J de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) escribe la frase «una fila de ___ corresponde a ___ de ___» para cada unión. El proyecto SQL te pedirá una nota sobre la cardinalidad de cada unión.

Siguiente: [3.2 INNER JOIN](02_inner_join.md).
