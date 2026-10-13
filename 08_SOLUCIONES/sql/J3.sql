SELECT pr.categoria,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN productos pr   ON pr.producto_id = i.producto_id
WHERE p.estado = 'entregado'
GROUP BY pr.categoria
ORDER BY ventas_bs DESC;
