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
