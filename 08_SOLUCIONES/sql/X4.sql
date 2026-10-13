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
