# 4.4 SQL para indicadores: fechas de corte, activos, crecimiento y rendimiento

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: capítulos 1 a 3 y lecciones [4.2](02_cte.md) y [4.3](03_ventanas.md).

## Para qué sirve

Los indicadores de negocio (tienda activa, recencia, crecimiento mensual) mezclan casi todo lo que aprendiste: filtros, fechas, JOIN, agregación y CTE. Aquí ves cómo se arman de forma **repetible**: con una fecha de corte fija, una definición escrita y controles. También das un primer vistazo a cómo saber si una consulta es lenta sin adivinar.

## Términos nuevos

- **Fecha de corte**: la fecha fija contra la que se calculan los indicadores del período («al 30 de septiembre de 2026»). Se escribe en la consulta (no se usa «hoy») para que el resultado no cambie con el tiempo.
- **Recencia**: días transcurridos desde la última compra hasta la fecha de corte.
- **Tienda activa**: una definición de negocio, por ejemplo «compró en los últimos 30 días hasta la fecha de corte». **La definición debe estar escrita**; con otra definición el número cambia.
- **Variación porcentual**: (valor actual − valor anterior) / valor anterior × 100.
- **Plan de consulta**: la descripción que da la base de datos de cómo piensa ejecutar la consulta. En SQLite se obtiene con `EXPLAIN QUERY PLAN`.
- **Índice**: una estructura auxiliar que permite encontrar filas por una columna sin recorrer toda la tabla (como el índice de un libro).
- **SCAN / SEARCH**: en el plan de SQLite, `SCAN` recorre la tabla completa; `SEARCH ... USING INDEX` encuentra las filas a través de un índice.

## Ejemplo paso a paso

**1. Recencia con fecha de corte fija.** Fecha de la última compra entregada de cada tienda y los días desde esa fecha hasta el corte `2026-09-30`:

```sql
WITH ultima AS (
    SELECT tienda_id, MAX(fecha) AS ultima_compra
    FROM ventas
    WHERE estado = 'entregado'
    GROUP BY tienda_id
)
SELECT t.tienda_id,
       u.ultima_compra,
       CAST(julianday('2026-09-30') - julianday(u.ultima_compra) AS INTEGER) AS dias_sin_comprar
FROM tiendas AS t
LEFT JOIN ultima AS u ON u.tienda_id = t.tienda_id
ORDER BY t.tienda_id;
```

```resultado
tienda_id | ultima_compra | dias_sin_comprar
1 | 2026-09-22 | 8
2 | 2026-09-02 | 28
3 | 2026-09-29 | 1
4 | 2026-09-10 | 20
5 | 2026-08-21 | 40
6 | 2026-08-28 | 33
7 | 2026-09-08 | 22
8 | NULL | NULL
9 | 2026-09-15 | 15
10 | 2026-09-25 | 5
11 | NULL | NULL
12 | NULL | NULL
```

Se usa `LEFT JOIN` desde `tiendas` para no perder a las tiendas que nunca compraron: su fecha y sus días salen `NULL`. Un NULL aquí significa «nunca compró», que es diferente de «compró hace cero días».

**2. Clasificar con una definición explícita.** Definición escrita: *activa = última compra entregada dentro de los 30 días anteriores o iguales al corte; inactiva = última compra más antigua; sin compras = nunca compró.*

```sql
WITH ultima AS (
    SELECT tienda_id, MAX(fecha) AS ultima_compra
    FROM ventas
    WHERE estado = 'entregado'
    GROUP BY tienda_id
),
clasificada AS (
    SELECT t.tienda_id,
           CASE
               WHEN u.ultima_compra IS NULL THEN 'sin compras'
               WHEN julianday('2026-09-30') - julianday(u.ultima_compra) <= 30 THEN 'activa'
               ELSE 'inactiva'
           END AS estado_tienda
    FROM tiendas AS t
    LEFT JOIN ultima AS u ON u.tienda_id = t.tienda_id
)
SELECT estado_tienda, COUNT(*) AS tiendas
FROM clasificada
GROUP BY estado_tienda
ORDER BY estado_tienda;
```

```resultado
estado_tienda | tiendas
activa | 7
inactiva | 2
sin compras | 3
```

Control: las tres cifras suman 12, el total de tiendas. Si cambias «30 días» por «45 días», el número de activas cambia; por eso la ventana de 30 días se declara en la definición y no se esconde en el código.

**3. Crecimiento mensual.** Ya lo calculaste con `LAG` en 4.3. Aquí lo importante es la regla de oro: si el mes anterior vale 0 o no existe, **no inventes un porcentaje**. `NULLIF(anterior, 0)` devuelve NULL y el resultado queda como «no calculable».

**4. Pensar en el plan: SCAN y SEARCH.** Veamos cómo ejecuta SQLite una búsqueda sin índice:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM ventas WHERE tienda_id = 3;
```

```resultado
id | parent | notused | detail
2 | 0 | 216 | SCAN ventas
```

`SCAN ventas` quiere decir que recorre las 16 filas. En una tabla de millones, sería lento. Ahora creamos un índice (sobre una **copia** de la base: nunca experimentes en la base real) y volvemos a pedir el plan:

```sql
CREATE INDEX idx_ventas_tienda ON ventas(tienda_id);
EXPLAIN QUERY PLAN
SELECT * FROM ventas WHERE tienda_id = 3;
```

```resultado
id | parent | notused | detail
3 | 0 | 61 | SEARCH ventas USING INDEX idx_ventas_tienda (tienda_id=?)
```

Ahora aparece `SEARCH ventas USING INDEX idx_ventas_tienda (tienda_id=?)`: encuentra las filas por el índice sin recorrer todo. El texto exacto y los números de las primeras columnas pueden variar según la versión de SQLite; lo que debes reconocer es la diferencia entre `SCAN` y `SEARCH`.

Tres cuidados: más índices no siempre es mejor (ocupan espacio y hacen más lentas las escrituras); envolver la columna en una función (`WHERE strftime('%Y', fecha) = '2026'`) puede impedir que se use el índice; y en una base de 16 filas no verás ninguna diferencia en milisegundos. En este curso interpretas el plan; no persigues micro-optimizaciones.

**5. Nota sobre SQL Server.** Muchos trabajos usan SQL Server. Las diferencias que más verás: `TOP n` en lugar de `LIMIT n`; `DATEDIFF(day, inicio, fin)` en lugar de restar `julianday`; `YEAR()`/`MONTH()` o `FORMAT()` en lugar de `strftime`; `CONCAT()` en lugar de `||`; y tipos de fecha más estrictos. Estos equivalentes son una referencia conceptual: en este curso no se ejecutaron en SQL Server.

Ejemplo comercial: «clientes inactivos» es una lista de acción para el vendedor. Si la definición cambia entre dos reportes (30 días en uno, 45 en otro) nadie entiende por qué los números no coinciden: **la definición va escrita y con su fecha de corte**.

## Errores comunes

- **Usar la fecha de hoy** (`'now'`) en un indicador que debe poder reproducirse.
- **No escribir la definición** de «activo», «inactivo», «nuevo».
- **Convertir el NULL de «nunca compró» en 0 días** y clasificarlo como activo.
- **Calcular crecimiento sin controlar el denominador cero.**
- **Medir el rendimiento en una tabla diminuta** y sacar conclusiones.
- **Crear índices en la base original** para probar.
- **Comparar fechas guardadas como texto en otro formato.**

## Para comprobar que entendiste

1. ¿Por qué se fija la fecha de corte en la consulta?
2. ¿Qué significa que la recencia de una tienda sea NULL?
3. ¿Qué diferencia hay entre `SCAN` y `SEARCH` en un plan de SQLite?
4. ¿Por qué se pone la definición de «activa» por escrito?

<details><summary>Respuestas</summary>

1. Para que el indicador dé el mismo resultado siempre.
2. Que nunca compró (no hay última compra).
3. SCAN recorre la tabla completa; SEARCH usa un índice para ubicar las filas.
4. Porque con otra definición cambia el número, y quien lo lea debe saber cuál se usó.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Con corte `2026-09-05`, calcula cuántas tiendas distintas tuvieron al menos una visita **realizada** entre el 3 y el 5 de septiembre (usa `visitas_ej`) y escribe la definición en una línea.
2. Calcula el importe de ventas entregadas por semana ISO (`strftime('%W', fecha)`) y la variación porcentual contra la semana anterior con `LAG`.
3. Escribe el plan (`EXPLAIN QUERY PLAN`) de una consulta que busque ventas por `fecha` y comenta qué verías si existiera un índice por `fecha`.

Cómo saber que está bien: en la 1 el resultado es 5 tiendas y tu definición dice qué es «últimos 3 días»; en la 2 la primera semana tiene variación NULL; en la 3 el plan sin índice dice `SCAN`.

<details><summary>Comprobación de la consulta 2</summary>

```sql
WITH por_semana AS (
    SELECT strftime('%W', v.fecha) AS semana, SUM(l.cantidad * l.precio_unitario) AS importe
    FROM venta_lineas AS l
    INNER JOIN ventas AS v ON v.venta_id = l.venta_id
    WHERE v.estado = 'entregado'
    GROUP BY semana
)
SELECT semana,
       importe,
       ROUND(100.0 * (importe - LAG(importe) OVER (ORDER BY semana)) / NULLIF(LAG(importe) OVER (ORDER BY semana), 0), 1) AS variacion_pct
FROM por_semana
ORDER BY semana;
```

```resultado
semana | importe | variacion_pct
31 | 414.0 | NULL
33 | 291.5 | -29.6
34 | 288.0 | -1.2
35 | 272.0 | -5.6
36 | 385.0 | 41.5
37 | 160.0 | -58.4
38 | 378.0 | 136.3
39 | 144.0 | -61.9
```

Observa que faltan semanas intermedias (no hubo ventas esas semanas): `LAG` compara con la semana disponible anterior, no con la semana calendario previa. Es el límite que se advirtió en 4.3.

</details>

## Después, en los ejercicios

Los ejercicios K, V, X y N de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) con «activos», «recencia», «crecimiento» o «plan de consulta» usan esta lección. El contexto de negocio de cada indicador está en el [capítulo 6 (KPIs)](../06_KPIs.md).

Siguiente capítulo: [5.1 ETL, ELT y medallón](../05_calidad_ETL/01_etl_elt_medallon.md).
