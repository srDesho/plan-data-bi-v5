-- SQ17 · Tabla plana para un tablero
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT strftime('%Y-%m',p.fecha) AS mes, pr.categoria, COUNT(DISTINCT p.pedido_id) AS pedidos, SUM(i.cantidad) AS unidades, ROUND(SUM(i.cantidad*i.precio_unitario),2) AS ventas_bs FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN productos pr ON pr.producto_id=i.producto_id WHERE p.estado='entregado' GROUP BY mes, pr.categoria ORDER BY mes, pr.categoria;

-- apartado b
SELECT ROUND(SUM(i.cantidad*i.precio_unitario),2) AS control FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id WHERE p.estado='entregado';
