SELECT cliente_id,TRIM(nombre_negocio) nombre,'Zona faltante' motivo FROM clientes WHERE zona IS NULL ORDER BY cliente_id;
