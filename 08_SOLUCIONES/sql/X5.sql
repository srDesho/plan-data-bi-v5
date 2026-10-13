SELECT c.ruta,
       COUNT(*) AS pedidos,
       SUM(CASE WHEN p.estado = 'anulado' THEN 1 ELSE 0 END) AS anulados,
       ROUND(100.0 * SUM(CASE WHEN p.estado = 'anulado' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_anulados
FROM pedidos p
INNER JOIN clientes c ON c.cliente_id = p.cliente_id
GROUP BY c.ruta
ORDER BY pct_anulados DESC;
