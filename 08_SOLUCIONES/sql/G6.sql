SELECT ruta, COUNT(*) AS clientes FROM clientes GROUP BY ruta HAVING COUNT(*) > 20;
