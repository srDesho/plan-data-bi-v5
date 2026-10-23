-- SQ12 · Mejores productos por categoría
-- Referencia: ábrela solo después de tu intento.

-- apartado a
WITH u AS (SELECT pr.categoria, pr.nombre, SUM(i.cantidad) AS unidades FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id JOIN productos pr ON pr.producto_id=i.producto_id WHERE p.estado='entregado' GROUP BY pr.categoria, pr.nombre), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY unidades DESC, nombre) AS pos FROM u) SELECT categoria, nombre, unidades, pos FROM r WHERE pos<=2 ORDER BY categoria, pos;
