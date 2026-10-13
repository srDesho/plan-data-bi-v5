SELECT c.cliente_id, c.nombre_negocio, MAX(p.fecha) AS ultima_compra
FROM clientes c
INNER JOIN pedidos p ON p.cliente_id = c.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.cliente_id, c.nombre_negocio
ORDER BY ultima_compra;
