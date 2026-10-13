SELECT c.cliente_id, c.nombre_negocio
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'anulado'
WHERE p.pedido_id IS NULL;
