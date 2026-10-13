SELECT cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta
FROM clientes
WHERE zona IS NULL
ORDER BY cliente_id;
