-- ============================================================================
-- SOLUCIONES SQL v3 · base: distribuidora.db (SQLite)
-- NO ABRAS ESTE ARCHIVO ANTES DE INTENTAR EL EJERCICIO. Primero escribe tu consulta,
-- ejecútala, y recién compara. Si la tuya da el mismo resultado por otro camino, también está bien.
--
-- Los códigos (S, G, J, K, V, E, X) son del TEMA, no del día. El plan dice qué ejercicios toca cada día.
--
-- Diferencias con SQL Server (T-SQL), que es lo que piden las vacantes:
--   LIMIT 10                      ->  SELECT TOP 10 ...
--   strftime('%Y-%m', fecha)      ->  FORMAT(fecha, 'yyyy-MM')  o  YEAR(fecha), MONTH(fecha)
--   julianday(a) - julianday(b)   ->  DATEDIFF(day, b, a)
--   a || b  (concatenar)          ->  a + b  o  CONCAT(a, b)
--   LIKE en SQLite ignora mayúsculas en ASCII; en SQL Server depende del collation.
--   Percentil: SQLite no tiene PERCENTILE_CONT; SQL Server sí (WITHIN GROUP ... OVER).
-- ============================================================================


-- ############################ S · SELECT y WHERE ########################

-- [S1] Primeras 10 filas de clientes
SELECT * FROM clientes LIMIT 10;

-- [S2] Tipos de negocio distintos
SELECT DISTINCT tipo FROM clientes;

-- [S3] Clientes de la ruta R03
SELECT * FROM clientes WHERE ruta = 'R03';

-- [S4] Bebidas con precio > 10, de mayor a menor precio
SELECT nombre, precio_unitario
FROM productos
WHERE categoria = 'Bebidas' AND precio_unitario > 10
ORDER BY precio_unitario DESC;

-- [S5] Kioscos o farmacias
SELECT * FROM clientes WHERE tipo IN ('Kiosco', 'Farmacia');

-- [S6] Nombre que contiene "sol"
SELECT * FROM clientes WHERE nombre_negocio LIKE '%sol%';

-- [S7] Clientes sin zona. Con "= NULL" no funciona porque NULL no es un valor: es "desconocido", y nada es igual a desconocido.
SELECT * FROM clientes WHERE zona IS NULL;

-- [S8] Pedidos del 1 al 15 de septiembre
SELECT * FROM pedidos WHERE fecha BETWEEN '2026-09-01' AND '2026-09-15';

-- [S9] Precio entre 5 y 10 en Snacks o Lácteos
SELECT nombre, categoria, precio_unitario
FROM productos
WHERE precio_unitario BETWEEN 5 AND 10
  AND categoria IN ('Snacks', 'Lácteos');

-- [S10] Cuántos clientes hay
SELECT COUNT(*) AS total_clientes FROM clientes;


-- ############################ G · Agregaciones y GROUP BY ###############

-- [G1] Pedidos entregados y anulados
SELECT estado, COUNT(*) AS pedidos FROM pedidos GROUP BY estado;

-- [G2] Unidades vendidas en total
SELECT SUM(cantidad) AS unidades FROM pedido_items;

-- [G3] Valor total de los ítems (incluye pedidos anulados: mañana lo corriges con un JOIN)
SELECT SUM(cantidad * precio_unitario) AS valor_items FROM pedido_items;

-- [G4] Precio promedio, mínimo y máximo por categoría
SELECT categoria,
       ROUND(AVG(precio_unitario), 2) AS precio_prom,
       MIN(precio_unitario)           AS precio_min,
       MAX(precio_unitario)           AS precio_max
FROM productos
GROUP BY categoria;

-- [G5] Clientes por ruta, de mayor a menor
SELECT ruta, COUNT(*) AS clientes FROM clientes GROUP BY ruta ORDER BY clientes DESC;

-- [G6] Rutas con más de 20 clientes (HAVING filtra grupos; WHERE filtra filas)
SELECT ruta, COUNT(*) AS clientes FROM clientes GROUP BY ruta HAVING COUNT(*) > 20;

-- [G7] Clientes por tipo y zona (los NULL aparecen como un grupo propio)
SELECT tipo, zona, COUNT(*) AS clientes FROM clientes GROUP BY tipo, zona ORDER BY tipo, zona;

-- [G8] Pedidos por mes
SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS pedidos
FROM pedidos
GROUP BY mes
ORDER BY mes;


-- ############################ J · JOIN ##################################

-- [J1] Pedidos con el nombre del cliente
SELECT p.pedido_id, p.fecha, c.nombre_negocio
FROM pedidos p
INNER JOIN clientes c ON c.cliente_id = p.cliente_id;

-- [J2] Ventas totales (Bs) de pedidos entregados
SELECT ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
WHERE p.estado = 'entregado';

-- [J3] Ventas por categoría de producto
SELECT pr.categoria,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN productos pr   ON pr.producto_id = i.producto_id
WHERE p.estado = 'entregado'
GROUP BY pr.categoria
ORDER BY ventas_bs DESC;

-- [J4] Ventas por vendedor
SELECT v.nombre,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN vendedores v   ON v.vendedor_id = p.vendedor_id
WHERE p.estado = 'entregado'
GROUP BY v.nombre
ORDER BY ventas_bs DESC;

-- [J5] Clientes SIN pedidos entregados en septiembre.
-- La condición de septiembre va en el ON: si la pones en el WHERE, borras justo las filas sin pedido y el LEFT JOIN se convierte en INNER.
SELECT c.cliente_id, c.nombre_negocio
FROM clientes c
LEFT JOIN pedidos p
       ON p.cliente_id = c.cliente_id
      AND p.estado = 'entregado'
      AND p.fecha BETWEEN '2026-09-01' AND '2026-09-30'
WHERE p.pedido_id IS NULL;

-- [J6] Top 5 productos por unidades entregadas
SELECT pr.nombre, SUM(i.cantidad) AS unidades
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN productos pr   ON pr.producto_id = i.producto_id
WHERE p.estado = 'entregado'
GROUP BY pr.nombre
ORDER BY unidades DESC
LIMIT 5;


-- ############################ K · Drop size, CASE, subconsultas, CTE ####

-- [K1] Drop size (Bs) y unidades de cada pedido entregado
SELECT p.pedido_id, p.fecha,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS drop_bs,
       SUM(i.cantidad)                               AS unidades
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
WHERE p.estado = 'entregado'
GROUP BY p.pedido_id, p.fecha;

-- [K2a] Drop size promedio general
SELECT ROUND(AVG(drop_bs), 2) AS drop_prom
FROM (
    SELECT p.pedido_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id
);

-- [K2b] Drop size promedio por ruta
SELECT c.ruta, ROUND(AVG(d.drop_bs), 2) AS drop_prom, COUNT(*) AS pedidos
FROM (
    SELECT p.pedido_id, p.cliente_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id, p.cliente_id
) d
INNER JOIN clientes c ON c.cliente_id = d.cliente_id
GROUP BY c.ruta
ORDER BY c.ruta;

-- [K3] Pedidos con drop size mayor al promedio general (subconsulta)
WITH d AS (
    SELECT p.pedido_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id
)
SELECT pedido_id, ROUND(drop_bs, 2) AS drop_bs
FROM d
WHERE drop_bs > (SELECT AVG(drop_bs) FROM d)
ORDER BY drop_bs DESC;

-- [K4] Clasificar pedidos en Pequeño (<200), Mediano (200 a 600) y Grande (>600) y contarlos
WITH d AS (
    SELECT p.pedido_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id
)
SELECT CASE WHEN drop_bs < 200 THEN 'Pequeño'
            WHEN drop_bs <= 600 THEN 'Mediano'
            ELSE 'Grande' END AS tamano,
       COUNT(*) AS pedidos
FROM d
GROUP BY tamano
ORDER BY pedidos DESC;

-- [K5] Top 10 pedidos por drop size, con cliente y vendedor
SELECT p.pedido_id, c.nombre_negocio, v.nombre AS vendedor,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS drop_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
INNER JOIN vendedores v   ON v.vendedor_id = p.vendedor_id
WHERE p.estado = 'entregado'
GROUP BY p.pedido_id, c.nombre_negocio, v.nombre
ORDER BY drop_bs DESC
LIMIT 10;

-- [K6] Con CTE: drop size promedio por cliente y los 5 mayores
WITH d AS (
    SELECT p.pedido_id, p.cliente_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id, p.cliente_id
),
por_cliente AS (
    SELECT cliente_id, ROUND(AVG(drop_bs), 2) AS drop_prom, COUNT(*) AS pedidos
    FROM d
    GROUP BY cliente_id
)
SELECT c.nombre_negocio, pc.drop_prom, pc.pedidos
FROM por_cliente pc
INNER JOIN clientes c ON c.cliente_id = pc.cliente_id
ORDER BY pc.drop_prom DESC
LIMIT 5;


-- ############################ V · Última compra, ventanas, ABC ###########

-- [V1] Última compra (entregada) por cliente
SELECT c.cliente_id, c.nombre_negocio, MAX(p.fecha) AS ultima_compra
FROM clientes c
INNER JOIN pedidos p ON p.cliente_id = c.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.cliente_id, c.nombre_negocio
ORDER BY ultima_compra;

-- [V2] Clientes que no compran hace más de 60 días (fecha de corte 2026-09-30)
SELECT c.cliente_id, c.nombre_negocio, MAX(p.fecha) AS ultima_compra,
       CAST(julianday('2026-09-30') - julianday(MAX(p.fecha)) AS INTEGER) AS dias_sin_comprar
FROM clientes c
INNER JOIN pedidos p ON p.cliente_id = c.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.cliente_id, c.nombre_negocio
HAVING julianday('2026-09-30') - julianday(MAX(p.fecha)) > 60
ORDER BY dias_sin_comprar DESC;

-- [V3] Ventas por cliente, participación % y acumulado %
WITH v AS (
    SELECT c.cliente_id, c.nombre_negocio,
           SUM(i.cantidad * i.precio_unitario) AS ventas
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
    WHERE p.estado = 'entregado'
    GROUP BY c.cliente_id, c.nombre_negocio
)
SELECT nombre_negocio,
       ROUND(ventas, 2) AS ventas,
       ROUND(100.0 * ventas / SUM(ventas) OVER (), 2) AS pct,
       ROUND(100.0 * SUM(ventas) OVER (ORDER BY ventas DESC, cliente_id) / SUM(ventas) OVER (), 2) AS pct_acum
FROM v
ORDER BY ventas DESC
LIMIT 15;

-- [V4] Clasificación ABC: A = hasta 80% de las ventas, B = hasta 95%, C = el resto.
-- Se mide el acumulado ANTES de sumar al cliente actual; así el cliente que cruza el 80% todavía es A.
WITH v AS (
    SELECT c.cliente_id,
           SUM(i.cantidad * i.precio_unitario) AS ventas
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
    WHERE p.estado = 'entregado'
    GROUP BY c.cliente_id
),
acum AS (
    SELECT cliente_id, ventas,
           (SUM(ventas) OVER (ORDER BY ventas DESC, cliente_id) - ventas) / SUM(ventas) OVER () AS pct_antes
    FROM v
),
clase AS (
    SELECT *, CASE WHEN pct_antes < 0.80 THEN 'A'
                   WHEN pct_antes < 0.95 THEN 'B'
                   ELSE 'C' END AS abc
    FROM acum
)
SELECT abc,
       COUNT(*) AS clientes,
       ROUND(100.0 * SUM(ventas) / (SELECT SUM(ventas) FROM clase), 1) AS pct_ventas
FROM clase
GROUP BY abc
ORDER BY abc;

-- [V5] Ranking de clientes por ventas dentro de cada ruta (los 3 mejores por ruta)
WITH v AS (
    SELECT c.cliente_id, c.nombre_negocio, c.ruta,
           SUM(i.cantidad * i.precio_unitario) AS ventas
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
    WHERE p.estado = 'entregado'
    GROUP BY c.cliente_id, c.nombre_negocio, c.ruta
),
r AS (
    SELECT *, RANK() OVER (PARTITION BY ruta ORDER BY ventas DESC) AS puesto
    FROM v
)
SELECT ruta, puesto, nombre_negocio, ROUND(ventas, 2) AS ventas
FROM r
WHERE puesto <= 3
ORDER BY ruta, puesto;


-- ############################ EXAMEN 2 (semana 2, 8 consultas con CTE y ventanas) #############

-- [X1] Ventas (Bs) por mes, solo entregados
SELECT strftime('%Y-%m', p.fecha) AS mes,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
WHERE p.estado = 'entregado'
GROUP BY mes
ORDER BY mes;

-- [X2] Drop size promedio por mes
WITH d AS (
    SELECT p.pedido_id, p.fecha, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id, p.fecha
)
SELECT strftime('%Y-%m', fecha) AS mes, ROUND(AVG(drop_bs), 2) AS drop_prom
FROM d
GROUP BY mes
ORDER BY mes;

-- [X3] Top 10 clientes por ventas
SELECT c.nombre_negocio, ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.nombre_negocio
ORDER BY ventas_bs DESC
LIMIT 10;

-- [X4] Ventas por categoría y % del total
WITH cat AS (
    SELECT pr.categoria, SUM(i.cantidad * i.precio_unitario) AS ventas
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    INNER JOIN productos pr   ON pr.producto_id = i.producto_id
    WHERE p.estado = 'entregado'
    GROUP BY pr.categoria
)
SELECT categoria, ROUND(ventas, 2) AS ventas_bs,
       ROUND(100.0 * ventas / SUM(ventas) OVER (), 1) AS pct_total
FROM cat
ORDER BY ventas DESC;

-- [X5] Porcentaje de pedidos anulados por ruta
SELECT c.ruta,
       COUNT(*) AS pedidos,
       SUM(CASE WHEN p.estado = 'anulado' THEN 1 ELSE 0 END) AS anulados,
       ROUND(100.0 * SUM(CASE WHEN p.estado = 'anulado' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_anulados
FROM pedidos p
INNER JOIN clientes c ON c.cliente_id = p.cliente_id
GROUP BY c.ruta
ORDER BY pct_anulados DESC;

-- [X6] Pedido con mayor drop size (con cliente y fecha)
SELECT p.pedido_id, p.fecha, c.nombre_negocio,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS drop_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
WHERE p.estado = 'entregado'
GROUP BY p.pedido_id, p.fecha, c.nombre_negocio
ORDER BY drop_bs DESC
LIMIT 1;

-- [X7] Ranking de vendedores por ventas
SELECT RANK() OVER (ORDER BY SUM(i.cantidad * i.precio_unitario) DESC) AS puesto,
       v.nombre,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN vendedores v   ON v.vendedor_id = p.vendedor_id
WHERE p.estado = 'entregado'
GROUP BY v.nombre;

-- [X8] Clientes con zona nula y cuánto compraron (revela datos que hay que corregir en origen)
SELECT c.cliente_id, c.nombre_negocio,
       ROUND(COALESCE(SUM(i.cantidad * i.precio_unitario), 0), 2) AS ventas_bs
FROM clientes c
LEFT JOIN pedidos p       ON p.cliente_id = c.cliente_id AND p.estado = 'entregado'
LEFT JOIN pedido_items i  ON i.pedido_id = p.pedido_id
WHERE c.zona IS NULL
GROUP BY c.cliente_id, c.nombre_negocio;


-- ############################ EXAMEN 1 (semana 1, solo S, G y J) #############

-- [E1] Tipos de cliente con más de 10 clientes
SELECT tipo, COUNT(*) AS clientes
FROM clientes
GROUP BY tipo
HAVING COUNT(*) > 10;

-- [E2] Las 3 bebidas más caras
SELECT nombre, precio_unitario
FROM productos
WHERE categoria = 'Bebidas'
ORDER BY precio_unitario DESC
LIMIT 3;

-- [E3] Pedidos anulados por mes
SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS anulados
FROM pedidos
WHERE estado = 'anulado'
GROUP BY mes
ORDER BY mes;

-- [E4] Ventas (Bs) por ruta, solo entregados
SELECT c.ruta, ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.ruta
ORDER BY c.ruta;

-- [E5] Clientes de la zona Centro con su cantidad de pedidos entregados (incluye los que tienen 0)
SELECT c.nombre_negocio, COUNT(p.pedido_id) AS pedidos_entregados
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'entregado'
WHERE c.zona = 'Centro'
GROUP BY c.cliente_id, c.nombre_negocio
ORDER BY pedidos_entregados DESC;

-- [E6] Unidades vendidas por tipo de cliente y categoría de producto (entregados)
SELECT c.tipo, pr.categoria, SUM(i.cantidad) AS unidades
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
INNER JOIN productos pr   ON pr.producto_id = i.producto_id
WHERE p.estado = 'entregado'
GROUP BY c.tipo, pr.categoria
ORDER BY c.tipo, pr.categoria;

-- [E7] Pedidos de septiembre con más de 10 ítems
SELECT p.pedido_id, COUNT(*) AS items
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
WHERE p.fecha BETWEEN '2026-09-01' AND '2026-09-30'
GROUP BY p.pedido_id
HAVING COUNT(*) > 10;

-- [E8] Clientes que nunca tuvieron un pedido anulado
SELECT c.cliente_id, c.nombre_negocio
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'anulado'
WHERE p.pedido_id IS NULL;


-- ############################ LIMPIEZA (CL) · semana 1, sábado ################

-- [CL1] Detectar nombres de negocio con espacios al inicio o al final (control: 8)
SELECT COUNT(*) AS con_espacios
FROM clientes
WHERE nombre_negocio <> TRIM(nombre_negocio);

-- [CL2] Nombres normalizados: sin espacios sobrantes y en mayúsculas
-- OJO: en SQLite UPPER() solo convierte letras sin tilde (queda 'TRéBOL'). En Python, .upper() sí convierte todo. En SQL Server no pasa.
SELECT cliente_id, UPPER(TRIM(nombre_negocio)) AS nombre_limpio
FROM clientes
ORDER BY cliente_id;

-- [CL3] Clientes por zona, mostrando 'Sin zona' cuando es NULL (control: 'Sin zona' = 6)
SELECT COALESCE(zona, 'Sin zona') AS zona, COUNT(*) AS clientes
FROM clientes
GROUP BY COALESCE(zona, 'Sin zona')
ORDER BY clientes DESC;

-- [CL4] Vista TEMPORAL con clientes limpios (no modifica el archivo .db) y consulta de prueba
CREATE TEMP VIEW clientes_limpios AS
SELECT cliente_id,
       UPPER(TRIM(nombre_negocio)) AS nombre_negocio,
       tipo,
       COALESCE(zona, 'Sin zona') AS zona,
       ruta,
       fecha_alta
FROM clientes;
