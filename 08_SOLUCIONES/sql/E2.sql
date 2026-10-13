SELECT nombre, precio_unitario
FROM productos
WHERE categoria = 'Bebidas'
ORDER BY precio_unitario DESC
LIMIT 3;
