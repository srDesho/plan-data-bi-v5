SELECT COUNT(*) AS con_espacios
FROM clientes
WHERE nombre_negocio <> TRIM(nombre_negocio);
