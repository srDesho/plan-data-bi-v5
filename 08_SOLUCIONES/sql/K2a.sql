SELECT ROUND(AVG(drop_bs), 2) AS drop_prom
FROM (
    SELECT p.pedido_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id
);
