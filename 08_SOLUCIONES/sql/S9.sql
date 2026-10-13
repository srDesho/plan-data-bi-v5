SELECT nombre, categoria, precio_unitario
FROM productos
WHERE precio_unitario BETWEEN 5 AND 10
  AND categoria IN ('Snacks', 'Lácteos')
ORDER BY categoria, nombre;
