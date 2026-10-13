SELECT c.tipo, pr.categoria, SUM(i.cantidad) AS unidades
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
INNER JOIN productos pr   ON pr.producto_id = i.producto_id
WHERE p.estado = 'entregado'
GROUP BY c.tipo, pr.categoria
ORDER BY c.tipo, pr.categoria;
