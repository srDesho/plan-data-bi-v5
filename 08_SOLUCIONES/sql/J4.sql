SELECT v.nombre,
       ROUND(SUM(i.cantidad * i.precio_unitario), 2) AS ventas_bs
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
INNER JOIN vendedores v   ON v.vendedor_id = p.vendedor_id
WHERE p.estado = 'entregado'
GROUP BY v.nombre
ORDER BY ventas_bs DESC;
