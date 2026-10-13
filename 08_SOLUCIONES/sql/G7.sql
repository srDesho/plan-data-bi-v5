SELECT tipo, zona, COUNT(*) AS clientes FROM clientes GROUP BY tipo, zona ORDER BY tipo, zona;
