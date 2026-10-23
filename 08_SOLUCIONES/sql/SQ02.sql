-- SQ02 · Valores ausentes y valores distintos
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT cliente_id, nombre_negocio, zona FROM clientes WHERE ruta='R03' AND zona IS NOT NULL ORDER BY cliente_id;

-- apartado b
SELECT cliente_id, nombre_negocio, zona FROM clientes WHERE zona IS NULL OR zona<>'Centro' ORDER BY cliente_id;

-- apartado c
SELECT cliente_id, nombre_negocio FROM clientes WHERE nombre_negocio LIKE '%Rosa%' ORDER BY cliente_id;

-- apartado d
SELECT DISTINCT tipo, ruta FROM clientes ORDER BY tipo, ruta;

-- apartado b (respuesta abierta): con `zona <> 'Centro'` solo, las filas con zona NULL no pasan el filtro porque NULL <> 'Centro' no es verdadero; por eso se añade `zona IS NULL OR`.
