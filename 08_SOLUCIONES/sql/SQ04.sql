-- SQ04 · Ventas de septiembre por ruta y control de cuadre
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT c.ruta, ROUND(SUM(i.cantidad*i.precio_unitario),2) AS ventas_bs FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id JOIN clientes c ON c.cliente_id=p.cliente_id WHERE p.estado='entregado' AND strftime('%Y-%m',p.fecha)='2026-09' GROUP BY c.ruta ORDER BY c.ruta;

-- apartado b
SELECT ROUND(SUM(i.cantidad*i.precio_unitario),2) AS total_bs FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id WHERE p.estado='entregado' AND strftime('%Y-%m',p.fecha)='2026-09';
