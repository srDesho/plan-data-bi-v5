SELECT nombre, categoria, precio_unitario FROM productos
WHERE categoria IN ('Snacks', 'Lácteos') AND precio_unitario BETWEEN 5 AND 10
ORDER BY categoria, nombre;