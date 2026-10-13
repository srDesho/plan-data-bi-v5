SELECT cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta
FROM clientes
WHERE tipo IN ('Kiosco', 'Farmacia')
ORDER BY cliente_id;
