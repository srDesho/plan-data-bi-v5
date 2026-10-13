SELECT COALESCE(zona, 'Sin zona') AS zona, COUNT(*) AS clientes
FROM clientes
GROUP BY COALESCE(zona, 'Sin zona')
ORDER BY clientes DESC, zona;
