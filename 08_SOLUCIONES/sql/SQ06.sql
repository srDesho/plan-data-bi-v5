-- SQ06 · Cadena de cuatro tablas y pedidos distintos
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT pr.categoria, c.ruta, SUM(i.cantidad) AS unidades FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN productos pr ON pr.producto_id=i.producto_id JOIN clientes c ON c.cliente_id=p.cliente_id WHERE p.estado='entregado' GROUP BY pr.categoria, c.ruta ORDER BY unidades DESC, pr.categoria, c.ruta LIMIT 5;

-- apartado b
SELECT c.tipo, COUNT(DISTINCT p.pedido_id) AS pedidos FROM pedidos p JOIN clientes c ON c.cliente_id=p.cliente_id JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN productos pr ON pr.producto_id=i.producto_id WHERE p.estado='entregado' AND pr.categoria='Bebidas' GROUP BY c.tipo ORDER BY pedidos DESC, c.tipo;
