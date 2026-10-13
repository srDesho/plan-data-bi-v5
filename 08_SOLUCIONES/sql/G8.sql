SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS pedidos
FROM pedidos
GROUP BY mes
ORDER BY mes;
