# 4.1 Subconsultas: una consulta dentro de otra

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: capítulos 1 a 3.

## Para qué sirve

Hay preguntas que se responden en dos pasos: «las ventas **mayores que el promedio**», «las tiendas que **están entre** las que compraron en septiembre», «el artículo más caro de cada categoría». En el primer paso calculas algo (el promedio, la lista de tiendas) y en el segundo lo usas. Una **subconsulta** es ese primer paso escrito dentro de la consulta principal.

## Términos nuevos

- **Subconsulta**: una consulta `SELECT` escrita entre paréntesis dentro de otra consulta.
- **Consulta externa**: la principal, la que contiene a la subconsulta.
- **Subconsulta escalar**: devuelve **una sola fila con una sola columna** (un número, por ejemplo el promedio). Se puede usar donde iría un valor.
- **Subconsulta de lista**: devuelve una columna con varias filas y se usa con `IN`.
- **Subconsulta en FROM** (o tabla derivada): su resultado se trata como si fuera una tabla; necesita un alias.
- **CTE**: una subconsulta con nombre escrita al principio con `WITH`. Se explica en la lección 4.2; la mencionamos aquí porque es la salida cuando las subconsultas se anidan demasiado.
- **EXISTS**: pregunta si la subconsulta devuelve al menos una fila. `NOT EXISTS` pregunta si no devuelve ninguna.

## Ejemplo paso a paso

**1. Subconsulta escalar: comparar contra un promedio.** ¿Qué artículos cuestan más que el precio promedio?

Primero, el promedio solo:

```sql
SELECT AVG(precio) AS promedio FROM articulos;
```

```resultado
promedio
8.1
```

Ahora, en lugar de copiar el número a mano, ponemos esa consulta entre paréntesis:

```sql
SELECT nombre, precio
FROM articulos
WHERE precio > (SELECT AVG(precio) FROM articulos)
ORDER BY precio DESC;
```

```resultado
nombre | precio
Detergente 1kg | 14.0
Yogurt 1L | 12.0
Gaseosa 2L | 11.5
Jugo 1L | 9.0
```

SQL ejecuta primero la subconsulta (devuelve 8,1, un solo valor) y luego usa ese valor en el `WHERE` de la consulta externa. La ventaja de no copiar el número a mano: si los precios cambian, la consulta sigue siendo correcta.

**2. Subconsulta de lista con IN.** Nombres de las tiendas que compraron en septiembre:

```sql
SELECT tienda_id, nombre
FROM tiendas
WHERE tienda_id IN (
    SELECT tienda_id FROM ventas WHERE fecha BETWEEN '2026-09-01' AND '2026-09-30'
)
ORDER BY tienda_id;
```

```resultado
tienda_id | nombre
1 | Tienda La Palma
2 | Kiosco El Faro
3 | Farmacia Salud
4 | Minimarket Sol Naciente
7 | Tienda Don Pepe
9 | Minimarket Central
10 | Kiosco Luna
```

La subconsulta devuelve una lista de `tienda_id` (con repeticiones, no importa) y el `IN` pregunta si el `tienda_id` de cada tienda está en esa lista.

**3. Subconsulta en FROM: agregar y luego agregar otra vez.** El importe promedio **por venta** (no por línea). Para eso primero necesitas el importe de cada venta (una fila por venta) y después promediar esa lista:

```sql
SELECT ROUND(AVG(importe_venta), 2) AS ticket_promedio_bs
FROM (
    SELECT venta_id, SUM(cantidad * precio_unitario) AS importe_venta
    FROM venta_lineas
    GROUP BY venta_id
) AS por_venta;
```

```resultado
ticket_promedio_bs
170.09
```

La subconsulta interna produce una fila por venta (16 filas); la consulta externa promedia esa columna. El alias `por_venta` es obligatorio. Es la solución limpia al problema de «promedio sobre el detalle» de la lección 2.3: **primero llevas los datos a la granularidad correcta y luego calculas**.

**4. EXISTS y NOT EXISTS.** Las tiendas que **no** tienen ninguna venta, escrito con otro estilo que el anti-join de 3.3:

```sql
SELECT t.tienda_id, t.nombre
FROM tiendas AS t
WHERE NOT EXISTS (SELECT 1 FROM ventas AS v WHERE v.tienda_id = t.tienda_id)
ORDER BY t.tienda_id;
```

```resultado
tienda_id | nombre
8 | Farmacia Vida
11 | Tienda Nueva Esperanza
12 | Restaurante El Buen Gusto
```

Para cada tienda, la subconsulta pregunta «¿existe alguna venta de esta tienda?». Esa subconsulta usa una columna de la consulta externa (`t.tienda_id`): se llama **subconsulta correlacionada**. `SELECT 1` solo importa por la existencia de filas, no por su contenido. El resultado es el mismo que el LEFT JOIN + IS NULL, y es otra herramienta legítima.

**5. La trampa de NOT IN con NULL.** Se parece a `NOT EXISTS`, pero se comporta distinto cuando la lista contiene un NULL. Lo probamos con una tabla temporal pequeña:

```sql
CREATE TEMP TABLE lista (valor INTEGER);
INSERT INTO lista VALUES (1), (NULL);
SELECT COUNT(*) AS filas_not_in
FROM tiendas
WHERE tienda_id NOT IN (SELECT valor FROM lista);
```

```resultado
filas_not_in
0
```

Devuelve 0: ninguna tienda cumple, **aunque ninguna tienda tenga `tienda_id` igual a NULL**. Comparar con un NULL da «desconocido» (lección 1.4), así que `NOT IN` queda sin respuesta verdadera para todas las filas. Con `NOT EXISTS` no pasa. **Regla: para «los que no están en…», prefiere `NOT EXISTS` o LEFT JOIN + IS NULL; usa `NOT IN` solo si estás seguro de que la lista no tiene NULL.**

Ejemplo comercial: «ventas por encima del ticket promedio del mes» combina una subconsulta en FROM (importe por venta), un promedio escalar y una comparación. Siempre pregúntate qué granularidad devuelve cada subconsulta.

## Errores comunes

- **Subconsulta escalar que devuelve varias filas**: SQLite toma solo la primera sin avisar. Verifica que devuelve una sola.
- **Olvidar el alias** en una subconsulta del `FROM`.
- **`NOT IN` con una lista que puede traer NULL**: devuelve cero filas.
- **Subconsultas anidadas sin sangría**: se vuelven ilegibles. Si pasas de dos niveles, usa una CTE (siguiente lección).
- **Calcular dos veces lo mismo** sin necesidad.
- **No entender qué granularidad devuelve la subconsulta interna.**

## Para comprobar que entendiste

1. ¿Qué devuelve una subconsulta escalar?
2. ¿Por qué la subconsulta del ejemplo 3 es necesaria para el ticket promedio?
3. ¿Qué diferencia hay entre `IN` y `EXISTS`?
4. ¿Por qué `NOT IN` es peligroso cuando la lista puede tener NULL?

<details><summary>Respuestas</summary>

1. Un solo valor (una fila, una columna).
2. Porque primero hay que obtener una fila por venta; promediar el detalle daría el promedio por línea.
3. `IN` compara un valor con una lista; `EXISTS` pregunta si una subconsulta tiene filas.
4. Porque comparar con NULL es «desconocido» y ninguna fila queda verdadera.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Lista los artículos cuyo precio es menor que el precio promedio general de `articulos`.
2. Lista las tiendas que tienen al menos una visita en `visitas_ej` (usa `EXISTS`).
3. Calcula el promedio de unidades por venta (cantidad total por venta, y luego el promedio de esas cantidades).

Cómo saber que está bien: en la 1 (el promedio general es 8,1) salen 6 artículos; en la 2 salen 10 tiendas (las que tienen alguna visita registrada); en la 3 el resultado es 22,75 unidades (compruébalo sumando a mano las unidades de dos ventas).

<details><summary>Comprobación de las consultas 2 y 3</summary>

```sql
SELECT t.tienda_id, t.nombre
FROM tiendas AS t
WHERE EXISTS (SELECT 1 FROM visitas_ej AS vi WHERE vi.tienda_id = t.tienda_id)
ORDER BY t.tienda_id;
```

```resultado
tienda_id | nombre
1 | Tienda La Palma
2 | Kiosco El Faro
3 | Farmacia Salud
4 | Minimarket Sol Naciente
5 |   Kiosco La Esquina 
6 | Restaurante Sabor
7 | Tienda Don Pepe
8 | Farmacia Vida
9 | Minimarket Central
10 | Kiosco Luna
```

```sql
SELECT ROUND(AVG(unidades), 2) AS unidades_promedio_por_venta
FROM (SELECT venta_id, SUM(cantidad) AS unidades FROM venta_lineas GROUP BY venta_id);
```

```resultado
unidades_promedio_por_venta
22.75
```

</details>

## Después, en los ejercicios

Las series K y X de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) usan subconsultas. Cuando una subconsulta se haga difícil de leer, pásala a CTE (4.2).

Siguiente: [4.2 CTE con WITH](02_cte.md).
