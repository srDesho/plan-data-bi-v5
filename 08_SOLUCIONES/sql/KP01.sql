-- KP01 · Productividad y variación
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT p.vendedor_id, ROUND(SUM(i.cantidad*i.precio_unitario),2) AS ventas_bs, COUNT(DISTINCT p.fecha) AS dias_con_ventas, ROUND(SUM(i.cantidad*i.precio_unitario)/COUNT(DISTINCT p.fecha),2) AS productividad_bs_dia FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id WHERE p.estado='entregado' GROUP BY p.vendedor_id ORDER BY p.vendedor_id;

-- apartado b
WITH v AS (SELECT c.ruta, SUM(CASE WHEN strftime('%Y-%m',p.fecha)='2026-08' THEN i.cantidad*i.precio_unitario ELSE 0 END) AS base, SUM(CASE WHEN strftime('%Y-%m',p.fecha)='2026-09' THEN i.cantidad*i.precio_unitario ELSE 0 END) AS actual FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN clientes c ON c.cliente_id=p.cliente_id WHERE p.estado='entregado' GROUP BY c.ruta) SELECT ruta, ROUND(base,2) AS ventas_agosto, ROUND(actual,2) AS ventas_septiembre, ROUND(actual-base,2) AS variacion_abs, CASE WHEN base=0 THEN 'n/c' ELSE ROUND(100.0*(actual-base)/base,1) END AS variacion_pct FROM v ORDER BY ruta;

-- apartado c
WITH v AS (SELECT c.ruta, SUM(CASE WHEN strftime('%Y-%m',p.fecha)='2026-03' THEN i.cantidad*i.precio_unitario ELSE 0 END) AS base, SUM(CASE WHEN strftime('%Y-%m',p.fecha)='2026-04' THEN i.cantidad*i.precio_unitario ELSE 0 END) AS actual FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN clientes c ON c.cliente_id=p.cliente_id WHERE p.estado='entregado' GROUP BY c.ruta) SELECT ruta, ROUND(base,2) AS ventas_marzo, ROUND(actual,2) AS ventas_abril, ROUND(actual-base,2) AS variacion_abs, CASE WHEN base=0 THEN 'n/c' ELSE ROUND(100.0*(actual-base)/base,1) END AS variacion_pct FROM v ORDER BY ruta;

-- apartado b (respuesta abierta): con base 0 el porcentaje no está definido: se muestra 'n/c' en lugar de dividir por cero ni inventar un 0 % o un 100 %.
