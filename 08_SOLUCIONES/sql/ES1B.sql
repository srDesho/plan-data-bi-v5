SELECT categoria,COUNT(*) productos,ROUND(AVG(precio_unitario),2) precio_medio FROM productos GROUP BY categoria HAVING COUNT(*)>=5 ORDER BY categoria;
