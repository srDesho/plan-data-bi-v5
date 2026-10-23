-- SQ11 · Una CTE por consulta
-- Referencia: ábrela solo después de tu intento.

-- apartado a
WITH v AS (SELECT c.ruta, strftime('%Y-%m',p.fecha) AS mes, SUM(i.cantidad*i.precio_unitario) AS ventas FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN clientes c ON c.cliente_id=p.cliente_id WHERE p.estado='entregado' GROUP BY c.ruta, mes) SELECT v.ruta, v.mes, ROUND(v.ventas,2) AS ventas, pr.presupuesto_bs, ROUND(100.0*v.ventas/pr.presupuesto_bs,1) AS cumplimiento FROM v JOIN presupuesto pr ON pr.ruta=v.ruta AND pr.mes=v.mes WHERE v.mes='2026-09' ORDER BY v.ruta;

-- apartado b
WITH t AS (SELECT cliente_id, SUM(cantidad*precio_unitario) AS ventas FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id WHERE p.estado='entregado' GROUP BY cliente_id) SELECT cliente_id, ROUND(ventas,2) AS ventas FROM t ORDER BY ventas DESC, cliente_id LIMIT 5;
