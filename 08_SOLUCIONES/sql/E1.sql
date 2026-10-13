SELECT tipo, COUNT(*) AS clientes
FROM clientes
GROUP BY tipo
HAVING COUNT(*) > 10;
