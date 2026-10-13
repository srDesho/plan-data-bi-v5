SELECT p.pedido_id, COUNT(*) AS items
FROM pedidos p
INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
WHERE p.fecha BETWEEN '2026-09-01' AND '2026-09-30'
GROUP BY p.pedido_id
HAVING COUNT(*) > 10;
