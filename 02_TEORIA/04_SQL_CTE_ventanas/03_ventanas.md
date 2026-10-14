# 4.3 Funciones de ventana: calcular sin colapsar las filas

> Tiempo estimado: 65 min (lectura 25 + práctica 40). Prerrequisitos: [2.2 GROUP BY](../02_SQL_agregados/02_group_by_having.md) y [4.2 CTE](02_cte.md).

## Para qué sirve

`GROUP BY` convierte muchas filas en una por grupo. Pero a veces quieres **conservar cada fila** y, al lado, un dato calculado sobre un conjunto de filas relacionadas: el puesto de cada venta dentro de su tienda, el acumulado del mes, el porcentaje de cada ruta sobre el total, el valor del mes anterior. Eso son las funciones de ventana.

## Términos nuevos

- **Función de ventana**: una función que calcula un valor para cada fila mirando un conjunto de filas relacionadas (su «ventana»), **sin eliminar filas** del resultado.
- **OVER ( ... )**: la cláusula que convierte una función normal en función de ventana y define su ventana.
- **PARTITION BY**: divide las filas en bloques independientes; el cálculo se reinicia en cada bloque (parecido a `GROUP BY`, pero sin colapsar).
- **ORDER BY (dentro de OVER)**: define el orden de las filas dentro de cada bloque para calcular puestos, acumulados o valores anteriores.
- **ROW_NUMBER**: numera las filas 1, 2, 3... sin repetir números.
- **RANK**: da puestos; los empates reciben el mismo puesto y el siguiente se salta (1, 1, 3).
- **DENSE_RANK**: como RANK pero sin saltos (1, 1, 2).
- **LAG(columna)**: el valor de la fila anterior dentro del orden de la ventana (NULL en la primera fila).
- **Acumulado**: suma que va creciendo fila a fila.
- **Marco** (*frame*): qué filas de la ventana entran en el cálculo de cada fila, por ejemplo «desde la primera hasta la actual» (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).

## Ejemplo paso a paso

Usamos primero una tabla pequeña de importes por venta (una CTE que ya conoces).

**1. Contraste con GROUP BY.** Importe de cada venta y, al lado, el total general. Con `GROUP BY` perderías el detalle; con una ventana lo conservas:

```sql
WITH por_venta AS (
    SELECT venta_id, SUM(cantidad * precio_unitario) AS importe
    FROM venta_lineas
    GROUP BY venta_id
)
SELECT venta_id,
       importe,
       SUM(importe) OVER () AS total_general,
       ROUND(100.0 * importe / SUM(importe) OVER (), 1) AS pct_del_total
FROM por_venta
ORDER BY venta_id
LIMIT 5;
```

```resultado
venta_id | importe | total_general | pct_del_total
1 | 137.0 | 2721.5 | 5.0
2 | 146.0 | 2721.5 | 5.4
3 | 131.0 | 2721.5 | 4.8
4 | 320.0 | 2721.5 | 11.8
5 | 182.0 | 2721.5 | 6.7
```

`SUM(importe) OVER ()` con paréntesis vacíos significa «la ventana es toda la tabla»: cada fila recibe el mismo total, y a partir de él calculamos el porcentaje. Las 16 filas siguen ahí (vemos 5).

**2. PARTITION BY: reiniciar por bloque.** Numerar las ventas de cada tienda de la más antigua a la más reciente:

```sql
SELECT tienda_id,
       venta_id,
       fecha,
       ROW_NUMBER() OVER (PARTITION BY tienda_id ORDER BY fecha, venta_id) AS n_venta_de_la_tienda
FROM ventas
WHERE tienda_id IN (1, 3)
ORDER BY tienda_id, fecha, venta_id;
```

```resultado
tienda_id | venta_id | fecha | n_venta_de_la_tienda
1 | 1 | 2026-08-03 | 1
1 | 5 | 2026-08-19 | 2
1 | 14 | 2026-09-22 | 3
3 | 3 | 2026-08-07 | 1
3 | 9 | 2026-09-04 | 2
3 | 16 | 2026-09-29 | 3
```

La numeración empieza en 1 en cada tienda: la tienda 1 tiene las ventas 1, 5 y 14 en su bloque; la tienda 3, las ventas 3, 9 y 16. El `ORDER BY` dentro de `OVER` fija qué es «primera» y «última». Si necesitaras **solo la última venta de cada tienda**, la técnica es ordenar de forma descendente, numerar y quedarse con el número 1 (en una consulta externa; ver errores comunes).

**3. RANK y empates.** Comparamos los tres tipos de numeración sobre una lista con valores repetidos (cantidades vendidas por línea de la venta 4, 7 y 11):

```sql
SELECT linea_id,
       cantidad,
       ROW_NUMBER() OVER (ORDER BY cantidad DESC, linea_id) AS fila_num,
       RANK() OVER (ORDER BY cantidad DESC) AS rango,
       DENSE_RANK() OVER (ORDER BY cantidad DESC) AS rango_denso
FROM venta_lineas
WHERE venta_id IN (4, 7, 11)
ORDER BY cantidad DESC, linea_id;
```

```resultado
linea_id | cantidad | fila_num | rango | rango_denso
9 | 20 | 1 | 1 | 1
18 | 20 | 2 | 1 | 1
27 | 20 | 3 | 1 | 1
10 | 15 | 4 | 4 | 2
16 | 12 | 5 | 5 | 3
28 | 10 | 6 | 6 | 4
17 | 6 | 7 | 7 | 5
```

Mira las tres líneas con cantidad 20: `ROW_NUMBER` les da 1, 2 y 3 (necesita el desempate `linea_id`); `RANK` les da a las tres el puesto 1 y salta al 4; `DENSE_RANK` les da 1 y continúa con 2. ¿Cuál usar? Depende de la pregunta: «los 3 primeros» con empates suele pedir `DENSE_RANK` o una regla de desempate explícita; define cuál antes de calcular.

**4. Acumulado.** Importe acumulado de las ventas entregadas ordenadas por fecha:

```sql
WITH por_venta AS (
    SELECT v.venta_id, v.fecha, SUM(l.cantidad * l.precio_unitario) AS importe
    FROM venta_lineas AS l
    INNER JOIN ventas AS v ON v.venta_id = l.venta_id
    WHERE v.estado = 'entregado'
    GROUP BY v.venta_id, v.fecha
)
SELECT venta_id,
       fecha,
       importe,
       SUM(importe) OVER (ORDER BY fecha, venta_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado
FROM por_venta
ORDER BY fecha, venta_id
LIMIT 6;
```

```resultado
venta_id | fecha | importe | acumulado
1 | 2026-08-03 | 137.0 | 137.0
2 | 2026-08-05 | 146.0 | 283.0
3 | 2026-08-07 | 131.0 | 414.0
5 | 2026-08-19 | 182.0 | 596.0
6 | 2026-08-21 | 109.5 | 705.5
7 | 2026-08-28 | 288.0 | 993.5
```

Cada fila suma su importe más todos los anteriores. El marco `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` dice «desde la primera fila hasta esta». Escribe el marco y un orden **completo** (con desempate): sin ellos, filas con el mismo valor de orden pueden tratarse como un grupo y el acumulado no sube fila a fila. Control: la última fila del acumulado completo debe igualar el total entregado (2332,5).

**5. LAG: comparar con el período anterior.** Importe por mes y variación respecto al mes anterior:

```sql
WITH por_mes AS (
    SELECT strftime('%Y-%m', v.fecha) AS mes, SUM(l.cantidad * l.precio_unitario) AS importe
    FROM venta_lineas AS l
    INNER JOIN ventas AS v ON v.venta_id = l.venta_id
    WHERE v.estado = 'entregado'
    GROUP BY mes
)
SELECT mes,
       importe,
       LAG(importe) OVER (ORDER BY mes) AS mes_anterior,
       ROUND(100.0 * (importe - LAG(importe) OVER (ORDER BY mes)) / NULLIF(LAG(importe) OVER (ORDER BY mes), 0), 1) AS variacion_pct
FROM por_mes
ORDER BY mes;
```

```resultado
mes | importe | mes_anterior | variacion_pct
2026-08 | 993.5 | NULL | NULL
2026-09 | 1339.0 | 993.5 | 34.8
```

El primer mes no tiene anterior: `LAG` devuelve NULL, y la variación también (correcto: no hay con qué comparar). La fórmula es (actual − anterior) / anterior; `NULLIF(…, 0)` evita dividir entre cero. Si faltara un mes entero, `LAG` tomaría el último mes *disponible* y no el calendario anterior: en ese caso necesitas construir una lista completa de meses antes de calcular.

**6. Una condición sobre una ventana va en una consulta externa.** `WHERE` se evalúa antes que las ventanas, así que no puedes escribir `WHERE ROW_NUMBER() ... = 1`. Se hace en dos pasos con una CTE: la venta más reciente de cada tienda.

```sql
WITH numeradas AS (
    SELECT tienda_id, venta_id, fecha,
           ROW_NUMBER() OVER (PARTITION BY tienda_id ORDER BY fecha DESC, venta_id DESC) AS n
    FROM ventas
)
SELECT tienda_id, venta_id, fecha
FROM numeradas
WHERE n = 1
ORDER BY tienda_id;
```

```resultado
tienda_id | venta_id | fecha
1 | 14 | 2026-09-22
2 | 8 | 2026-09-02
3 | 16 | 2026-09-29
4 | 11 | 2026-09-10
5 | 6 | 2026-08-21
6 | 7 | 2026-08-28
7 | 10 | 2026-09-08
9 | 13 | 2026-09-18
10 | 15 | 2026-09-25
```

Una fila por tienda con compras: su última venta. Esta técnica («el último de cada grupo») es muy frecuente.

Ejemplo comercial: el ranking de rutas por ventas con `DENSE_RANK`, el acumulado de ventas en el mes para ver si se llega a la meta y el crecimiento mensual con `LAG` son tres usos que verás en cualquier reporte.

## Errores comunes

- **Poner la condición sobre la ventana en `WHERE`**: da error. Usa una CTE o subconsulta y filtra afuera.
- **Olvidar el desempate** en `ROW_NUMBER` o en un acumulado.
- **Confundir `RANK` con `DENSE_RANK`** cuando hay empates.
- **Creer que `PARTITION BY` reduce las filas**: no lo hace; solo reinicia el cálculo.
- **Calcular `LAG` con meses faltantes** y suponer que el anterior es el mes calendario previo.
- **No comprobar que el acumulado final es igual al total.**
- **Dividir entre un `LAG` que puede ser 0**: usa `NULLIF`.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre `SUM(x) OVER ()` y `SUM(x)` con `GROUP BY`?
2. Tres filas empatadas en el primer puesto: ¿qué puesto recibe la siguiente con `RANK` y con `DENSE_RANK`?
3. ¿Por qué `WHERE ROW_NUMBER() ... = 1` no funciona?
4. ¿Qué devuelve `LAG` en la primera fila?

<details><summary>Respuestas</summary>

1. La de ventana conserva todas las filas y repite el total; `GROUP BY` colapsa a una fila por grupo.
2. 4 con `RANK`; 2 con `DENSE_RANK`.
3. Porque `WHERE` se evalúa antes de calcular las ventanas; hay que filtrar en una consulta externa.
4. NULL.

</details>

## Micropráctica

1. Para cada línea de `venta_lineas` de las ventas 1 a 3, muestra el subtotal y qué porcentaje es del importe de **su** venta (`PARTITION BY venta_id`).
2. Numera las visitas de `visitas_ej` de cada tienda por fecha (n.º de visita de la tienda).
3. Para cada mes de ventas entregadas, calcula el importe y el porcentaje que representa sobre el total del período (una ventana sin partición).

Cómo saber que está bien: en la 1 los porcentajes de cada venta suman 100; en la 2 la tienda 1 tiene 3 visitas numeradas del 1 al 3; en la 3 los dos porcentajes suman 100.

<details><summary>Comprobación de la consulta 1</summary>

```sql
SELECT venta_id,
       linea_id,
       cantidad * precio_unitario AS subtotal,
       ROUND(100.0 * cantidad * precio_unitario / SUM(cantidad * precio_unitario) OVER (PARTITION BY venta_id), 1) AS pct_de_la_venta
FROM venta_lineas
WHERE venta_id IN (1, 2, 3)
ORDER BY venta_id, linea_id;
```

```resultado
venta_id | linea_id | subtotal | pct_de_la_venta
1 | 1 | 60.0 | 43.8
1 | 2 | 45.0 | 32.8
1 | 3 | 32.0 | 23.4
2 | 4 | 92.0 | 63.0
2 | 5 | 54.0 | 37.0
3 | 6 | 42.0 | 32.1
3 | 7 | 35.0 | 26.7
3 | 8 | 54.0 | 41.2
```

</details>

## Después, en los ejercicios

Las series V y X de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) usan estas funciones. Para cada una escribe primero la ventana en español: «para cada ___, dentro de cada ___, ordenado por ___».

Siguiente: [4.4 SQL para indicadores, fechas y rendimiento](04_sql_kpis_fechas_rendimiento.md).
