SELECT c.ruta, ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.ruta
ORDER BY c.ruta;
