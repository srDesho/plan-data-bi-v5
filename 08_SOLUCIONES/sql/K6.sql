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
