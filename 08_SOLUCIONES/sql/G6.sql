SELECT ruta, COUNT(*) AS clientes
FROM clientes
GROUP BY ruta
HAVING COUNT(*) > 20
ORDER BY clientes DESC, ruta;
