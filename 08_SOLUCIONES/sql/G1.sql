SELECT estado, COUNT(*) AS pedidos
FROM pedidos
GROUP BY estado
ORDER BY estado;
