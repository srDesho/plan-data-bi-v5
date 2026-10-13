SELECT c.cliente_id, c.nombre_negocio
FROM clientes c
LEFT JOIN pedidos p
       ON p.cliente_id = c.cliente_id
      AND p.estado = 'entregado'
      AND p.fecha BETWEEN '2026-09-01' AND '2026-09-30'
WHERE p.pedido_id IS NULL;
