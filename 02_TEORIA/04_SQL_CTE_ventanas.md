# Subconsultas, ventanas, fechas e índices

Una subconsulta produce un resultado utilizado por otra consulta. Una CTE (`WITH nombre AS (...)`) le asigna un nombre temporal dentro de una sentencia. Sirve para separar pasos: primero ventas por pedido, luego ticket por ruta. No es automáticamente una tabla persistida ni una garantía de mayor rendimiento.

Una ventana calcula sobre un conjunto relacionado de filas sin colapsarlas. `GROUP BY` da una fila por grupo; `SUM(ventas) OVER()` conserva cada cliente y añade el total general. `PARTITION BY ruta` reinicia el cálculo por ruta; `ORDER BY ventas DESC` define un orden analítico.

```sql
WITH v AS (
 SELECT cliente_id, COUNT(*) pedidos
 FROM pedidos WHERE estado='entregado' GROUP BY cliente_id
)
SELECT cliente_id, pedidos,
       RANK() OVER (ORDER BY pedidos DESC) puesto
FROM v ORDER BY puesto,cliente_id;
```

`ROW_NUMBER` asigna números consecutivos; si hay empates necesitas un desempate determinista. `RANK` da el mismo puesto a empates y deja huecos; `DENSE_RANK` no deja huecos. Una condición sobre una ventana se aplica en una consulta exterior o CTE, porque WHERE se evalúa antes de la ventana.

Para acumulados usa `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` y un orden completo. El marco por defecto puede tratar empates como un grupo y cambiar el acumulado. `LAG(ventas) OVER(ORDER BY mes)` recupera el mes anterior disponible; si hay meses ausentes debes construir un calendario y decidir si su valor es cero o desconocido. Crecimiento = (actual−anterior)/anterior; con anterior cero no inventes un porcentaje.

ABC por ventas ordena clientes por aporte y usa participación acumulada. En V4 se evalúa el acumulado ANTES del cliente actual: el cliente que cruza 80% permanece en A. Es una convención explícita, no una ley universal. ABC por variedad de SKU responde otra pregunta; N10 cuenta variedad y cualquier umbral A/B/C requiere una regla acordada. No intercambies las clasificaciones.

## Fechas y SQL Server

SQLite: `strftime('%Y-%m',fecha)` extrae mes; `julianday(corte)-julianday(ultima)` calcula días. La recencia usa corte fijo 2026-09-30 para ser reproducible. SQL Server: TOP sustituye LIMIT; DATEFROMPARTS/YEAR/MONTH permiten trabajar meses; DATEDIFF(day, ultima, corte) cuenta límites diarios. CAST y tipos de fecha son más estrictos que en SQLite. La concatenación puede hacerse con CONCAT en SQL Server y `||` en SQLite. Los ejemplos T-SQL son de adaptación conceptual: no se ejecutaron en SQL Server.

## Rendimiento sin adivinar

`EXPLAIN QUERY PLAN` muestra el plan SQLite. Compara SCAN (recorrido) con SEARCH (búsqueda) antes y después de crear un índice en una COPIA de la base: `CREATE INDEX idx_pedidos_cliente_fecha ON pedidos(cliente_id,fecha);`. No presupongas que más índices son mejores: ocupan espacio y encarecen escrituras. Filtrar por clave/fecha puede beneficiarse; envolver la columna en una función puede impedir aprovechar algunos índices. En este curso se interpreta el plan; no se exige una mejora de milisegundos en una base pequeña.

Práctica: K1–K6, V1–V5, X1–X8, N5–N7, N13 y N15. Fuente: SQLite ventanas, fechas y EXPLAIN QUERY PLAN; Microsoft Learn, DATEDIFF.
