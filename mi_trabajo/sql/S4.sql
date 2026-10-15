SELECT nombre, precio_unitario
FROM productos
WHERE precio_unitario > 10 AND categoria = 'Bebidas'
ORDER BY precio_unitario DESC;