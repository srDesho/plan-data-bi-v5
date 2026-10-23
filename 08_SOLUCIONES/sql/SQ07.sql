-- SQ07 · Clientes que no aparecen en visitas
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT c.cliente_id, c.nombre_negocio FROM clientes c LEFT JOIN visitas v ON v.cliente_id=c.cliente_id AND v.realizada=1 WHERE v.visita_id IS NULL ORDER BY c.cliente_id;

-- apartado b
SELECT c.ruta, COUNT(*) AS clientes_sin_pedido_tomado FROM clientes c LEFT JOIN visitas v ON v.cliente_id=c.cliente_id AND v.pedido_tomado=1 WHERE v.visita_id IS NULL GROUP BY c.ruta ORDER BY c.ruta;

-- apartado a (respuesta abierta): la condición realizada = 1 va en el ON y no en el WHERE: en el WHERE descartaría también a los clientes sin ninguna visita (su fila unida es NULL) y el anti-join dejaría de encontrarlos.
