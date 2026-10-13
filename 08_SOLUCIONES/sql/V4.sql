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
