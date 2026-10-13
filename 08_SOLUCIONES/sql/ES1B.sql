SELECT categoria, COUNT(*) AS productos, ROUND(AVG(precio_unitario), 2) AS precio_medio
FROM productos
GROUP BY categoria
HAVING AVG(precio_unitario) > 9
ORDER BY categoria;
