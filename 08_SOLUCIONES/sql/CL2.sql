SELECT cliente_id, UPPER(TRIM(nombre_negocio)) AS nombre_limpio
FROM clientes
ORDER BY cliente_id;
