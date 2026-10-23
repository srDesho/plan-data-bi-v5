-- SQ01 · Catálogo, ruta e inventario
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT nombre, precio_unitario, ROUND(precio_unitario*1.13,2) AS precio_con_iva FROM productos WHERE categoria='Snacks' ORDER BY precio_unitario, producto_id LIMIT 5;

-- apartado b
SELECT cliente_id, nombre_negocio, tipo FROM clientes WHERE (tipo='Farmacia' OR tipo='Kiosco') AND ruta='R02' ORDER BY cliente_id;

-- apartado c
SELECT producto_id, salidas_unidades, stock_final, salidas_unidades-stock_final AS diferencia FROM inventario WHERE salidas_unidades>stock_final ORDER BY diferencia DESC, producto_id LIMIT 5;

-- apartado d
PRAGMA table_info(visitas);
-- Una fila de visitas es una visita planificada a un cliente en una fecha.
-- planificada = 1 si la visita estaba programada; realizada = 1 si se hizo; pedido_tomado = 1 si de ella salió un pedido.
