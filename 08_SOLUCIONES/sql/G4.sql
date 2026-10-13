SELECT categoria,
       ROUND(AVG(precio_unitario), 2) AS precio_prom,
       MIN(precio_unitario) AS precio_min,
       MAX(precio_unitario) AS precio_max
FROM productos
GROUP BY categoria
ORDER BY categoria;
