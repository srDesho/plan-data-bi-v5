SELECT c.ruta, ROUND(AVG(d.drop_bs), 2) AS drop_prom, COUNT(*) AS pedidos
FROM (
    SELECT p.pedido_id, p.cliente_id, SUM(i.cantidad * i.precio_unitario) AS drop_bs
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    WHERE p.estado = 'entregado'
    GROUP BY p.pedido_id, p.cliente_id
) d
INNER JOIN clientes c ON c.cliente_id = d.cliente_id
GROUP BY c.ruta
ORDER BY c.ruta;
