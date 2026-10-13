SELECT pedido_id, cliente_id, vendedor_id, fecha, estado
FROM pedidos
WHERE fecha BETWEEN '2026-09-01' AND '2026-09-15'
ORDER BY fecha, pedido_id;
