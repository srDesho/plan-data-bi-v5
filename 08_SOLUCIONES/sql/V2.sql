SELECT c.cliente_id, c.nombre_negocio, MAX(p.fecha) AS ultima_compra,
       CAST(julianday('2026-09-30') - julianday(MAX(p.fecha)) AS INTEGER) AS dias_sin_comprar
FROM clientes c
INNER JOIN pedidos p ON p.cliente_id = c.cliente_id
WHERE p.estado = 'entregado'
GROUP BY c.cliente_id, c.nombre_negocio
HAVING julianday('2026-09-30') - julianday(MAX(p.fecha)) > 60
ORDER BY dias_sin_comprar DESC;
