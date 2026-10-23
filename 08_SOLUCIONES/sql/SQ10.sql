-- SQ10 · Comparar contra un promedio
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT producto_id, nombre, precio_unitario FROM productos WHERE precio_unitario>(SELECT AVG(precio_unitario) FROM productos) ORDER BY precio_unitario DESC, producto_id;

-- apartado b
SELECT cliente_id, COUNT(*) AS pedidos FROM pedidos WHERE estado='entregado' GROUP BY cliente_id HAVING COUNT(*)>(SELECT AVG(n) FROM (SELECT COUNT(*) AS n FROM pedidos WHERE estado='entregado' GROUP BY cliente_id)) ORDER BY pedidos DESC, cliente_id LIMIT 10;
