-- SQ16 · Clasificación ABC de productos
-- Referencia: ábrela solo después de tu intento.

-- apartado a
WITH u AS (SELECT pr.producto_id, pr.nombre, SUM(i.cantidad) AS unidades FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id JOIN productos pr ON pr.producto_id=i.producto_id WHERE p.estado='entregado' GROUP BY pr.producto_id, pr.nombre), a AS (SELECT *, SUM(unidades) OVER (ORDER BY unidades DESC, producto_id) AS acum, SUM(unidades) OVER () AS total FROM u) SELECT producto_id, nombre, unidades, ROUND(100.0*(acum-unidades)/total,1) AS acum_antes, CASE WHEN 100.0*(acum-unidades)/total<80 THEN 'A' WHEN 100.0*(acum-unidades)/total<95 THEN 'B' ELSE 'C' END AS clase FROM a ORDER BY unidades DESC, producto_id;

-- apartado b
SELECT COUNT(*) AS productos_a FROM (WITH u AS (SELECT pr.producto_id, pr.nombre, SUM(i.cantidad) AS unidades FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id JOIN productos pr ON pr.producto_id=i.producto_id WHERE p.estado='entregado' GROUP BY pr.producto_id, pr.nombre), a AS (SELECT *, SUM(unidades) OVER (ORDER BY unidades DESC, producto_id) AS acum, SUM(unidades) OVER () AS total FROM u) SELECT producto_id, nombre, unidades, ROUND(100.0*(acum-unidades)/total,1) AS acum_antes, CASE WHEN 100.0*(acum-unidades)/total<80 THEN 'A' WHEN 100.0*(acum-unidades)/total<95 THEN 'B' ELSE 'C' END AS clase FROM a ORDER BY unidades DESC, producto_id) WHERE clase='A';

-- apartado b (respuesta abierta): los productos A concentran el primer 80 % de las unidades entregadas; el número exacto sale de la consulta, no de una regla fija 20/80.
