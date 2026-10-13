SELECT ruta, COUNT(*) AS clientes FROM clientes GROUP BY ruta ORDER BY clientes DESC;
