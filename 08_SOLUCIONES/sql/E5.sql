SELECT c.nombre_negocio, COUNT(p.pedido_id) AS pedidos_entregados
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'entregado'
WHERE c.zona = 'Centro'
GROUP BY c.cliente_id, c.nombre_negocio
ORDER BY pedidos_entregados DESC;
