SELECT nombre, precio_unitario
FROM productos
WHERE categoria = 'Bebidas' AND precio_unitario > 10
ORDER BY precio_unitario DESC;
