SELECT p.pedido_id, c.nombre_negocio, v.nombre AS vendedor,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS drop_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
INNER JOIN vendedores v   ON v.vendedor_id = p.vendedor_id
WHERE p.estado = 'entregado'
GROUP BY p.pedido_id, c.nombre_negocio, v.nombre
ORDER BY drop_bs DESC
LIMIT 10;
