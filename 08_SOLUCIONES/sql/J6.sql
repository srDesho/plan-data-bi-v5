SELECT pr.nombre, SUM(i.cantidad) AS unidades
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN productos pr   ON pr.producto_id = i.producto_id
WHERE p.estado = 'entregado'
GROUP BY pr.nombre
ORDER BY unidades DESC
LIMIT 5;
