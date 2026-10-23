-- SQ08 · El JOIN que multiplica
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT ROUND(SUM(cantidad*precio_unitario),2) AS total_bs FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id WHERE p.estado='entregado';

-- apartado b
SELECT ROUND(SUM(i.cantidad*i.precio_unitario),2) AS total_bs FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id JOIN visitas v ON v.cliente_id=p.cliente_id WHERE p.estado='entregado';

-- apartado c
SELECT COUNT(*) AS filas_unidas FROM pedidos p JOIN visitas v ON v.cliente_id=p.cliente_id;

-- apartado d
SELECT ROUND(SUM(i.cantidad*i.precio_unitario),2) AS total_bs FROM pedido_items i JOIN pedidos p ON p.pedido_id=i.pedido_id LEFT JOIN (SELECT cliente_id, COUNT(*) AS n FROM visitas GROUP BY cliente_id) v ON v.cliente_id=p.cliente_id WHERE p.estado='entregado';

-- apartado b (respuesta abierta): cada pedido se une con todas las visitas de su cliente (4 por cliente), así que cada ítem se suma 4 veces: el total se infla al multiplicar la granularidad. Se corrige agregando visitas por cliente antes de unir (apartado d).
