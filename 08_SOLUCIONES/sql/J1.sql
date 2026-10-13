SELECT p.pedido_id, p.fecha, c.nombre_negocio
FROM pedidos p
INNER JOIN clientes c ON c.cliente_id = p.cliente_id;
