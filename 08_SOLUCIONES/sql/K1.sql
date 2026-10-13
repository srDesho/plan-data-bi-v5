SELECT p.pedido_id, p.fecha,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS drop_bs,
       SUM(i.cantidad)                               AS unidades
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
WHERE p.estado = 'entregado'
GROUP BY p.pedido_id, p.fecha
ORDER BY p.pedido_id;
