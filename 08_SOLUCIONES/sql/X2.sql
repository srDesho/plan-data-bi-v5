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
