SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS anulados
FROM pedidos
WHERE estado = 'anulado'
GROUP BY mes
ORDER BY mes;
