-- SQ05 · Denominador por grupo
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT vendedor_id, estado, COUNT(*) AS pedidos FROM pedidos GROUP BY vendedor_id, estado ORDER BY vendedor_id, estado;

-- apartado b
SELECT vendedor_id, ROUND(100.0*SUM(CASE WHEN estado='anulado' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_anulados FROM pedidos GROUP BY vendedor_id ORDER BY vendedor_id;

-- apartado c
SELECT vendedor_id, COUNT(*) AS pedidos FROM pedidos GROUP BY vendedor_id HAVING 100.0*SUM(CASE WHEN estado='anulado' THEN 1 ELSE 0 END)/COUNT(*)>4.5 ORDER BY vendedor_id;
