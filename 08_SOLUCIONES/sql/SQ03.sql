-- SQ03 · Grupos con condición
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT estado, COUNT(*) AS pedidos FROM pedidos GROUP BY estado ORDER BY estado;

-- apartado b
SELECT producto_id, SUM(cantidad) AS unidades FROM pedido_items GROUP BY producto_id HAVING SUM(cantidad)>=4500 ORDER BY unidades DESC, producto_id;

-- apartado c
SELECT fecha, SUM(planificada) AS plan, SUM(realizada) AS real FROM visitas GROUP BY fecha HAVING SUM(realizada)<SUM(planificada) ORDER BY fecha;
