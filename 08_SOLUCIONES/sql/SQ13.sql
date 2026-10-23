-- SQ13 · Controles de calidad de la base
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT COUNT(*) AS nombres_con_espacios FROM clientes WHERE nombre_negocio<>TRIM(nombre_negocio);

-- apartado b
SELECT ruta, COUNT(*) AS sin_zona FROM clientes WHERE zona IS NULL GROUP BY ruta ORDER BY ruta;

-- apartado c
SELECT COUNT(*) AS items_sin_pedido FROM pedido_items i LEFT JOIN pedidos p ON p.pedido_id=i.pedido_id WHERE p.pedido_id IS NULL;

-- apartado d
SELECT COUNT(*) AS pedidos_sin_cliente FROM pedidos p LEFT JOIN clientes c ON c.cliente_id=p.cliente_id WHERE c.cliente_id IS NULL;

-- apartado d (respuesta abierta): un 0 en un control de huérfanos significa que no hay filas que incumplan la regla (todo ítem tiene pedido y todo pedido tiene cliente); es el resultado esperado, no un error ni una consulta vacía por casualidad.
