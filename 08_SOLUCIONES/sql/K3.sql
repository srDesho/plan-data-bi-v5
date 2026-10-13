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
