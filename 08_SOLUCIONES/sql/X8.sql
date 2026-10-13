SELECT c.cliente_id, c.nombre_negocio,
       ROUND(COALESCE(SUM(i.cantidad * i.precio_unitario), 0), 2) AS ventas_bs
FROM clientes c
LEFT JOIN pedidos p       ON p.cliente_id = c.cliente_id AND p.estado = 'entregado'
LEFT JOIN pedido_items i  ON i.pedido_id = p.pedido_id
WHERE c.zona IS NULL
GROUP BY c.cliente_id, c.nombre_negocio;
