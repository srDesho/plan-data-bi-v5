CREATE TEMP VIEW clientes_limpios AS
SELECT cliente_id,
       UPPER(TRIM(nombre_negocio)) AS nombre_negocio,
       tipo,
       COALESCE(zona, 'Sin zona') AS zona,
       ruta,
       fecha_alta
FROM clientes;
SELECT COUNT(*) AS clientes FROM clientes_limpios;
