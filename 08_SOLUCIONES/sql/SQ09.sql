-- SQ09 · CASE, COALESCE y NULLIF
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT CASE WHEN fecha_alta<'2026-01-01' THEN 'antigua' ELSE 'reciente' END AS clase, COUNT(*) AS clientes FROM clientes GROUP BY clase ORDER BY clase;

-- apartado b
SELECT COALESCE(zona,'Sin zona') AS zona, COUNT(*) AS clientes FROM clientes GROUP BY COALESCE(zona,'Sin zona') ORDER BY clientes DESC, zona;

-- apartado c
SELECT ruta, ROUND(100.0*SUM(pedido_tomado)/NULLIF(SUM(realizada),0),1) AS efectividad FROM visitas GROUP BY ruta ORDER BY ruta;
