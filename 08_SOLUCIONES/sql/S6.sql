SELECT cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta
FROM clientes
WHERE nombre_negocio LIKE '%sol%'
ORDER BY cliente_id;
