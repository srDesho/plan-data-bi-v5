SELECT cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta
FROM clientes
WHERE ruta = 'R03'
ORDER BY cliente_id;
