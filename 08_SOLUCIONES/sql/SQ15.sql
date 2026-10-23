-- SQ15 · Acumulado y porcentaje acumulado
-- Referencia: ábrela solo después de tu intento.

-- apartado a
WITH m AS (SELECT strftime('%Y-%m',p.fecha) AS mes, SUM(i.cantidad*i.precio_unitario) AS ventas FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id WHERE p.estado='entregado' GROUP BY mes) SELECT mes, ROUND(ventas,2) AS ventas, ROUND(SUM(ventas) OVER (ORDER BY mes),2) AS acumulado, ROUND(100.0*SUM(ventas) OVER (ORDER BY mes)/SUM(ventas) OVER (),1) AS pct_acumulado FROM m ORDER BY mes;
