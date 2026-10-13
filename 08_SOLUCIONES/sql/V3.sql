WITH v AS (
    SELECT c.cliente_id, c.nombre_negocio,
           SUM(i.cantidad * i.precio_unitario) AS ventas
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
    WHERE p.estado = 'entregado'
    GROUP BY c.cliente_id, c.nombre_negocio
)
SELECT nombre_negocio,
       ROUND(ventas, 2) AS ventas,
       ROUND(100.0 * ventas / SUM(ventas) OVER (), 2) AS pct,
       ROUND(100.0 * SUM(ventas) OVER (ORDER BY ventas DESC, cliente_id) / SUM(ventas) OVER (), 2) AS pct_acum
FROM v
ORDER BY ventas DESC
LIMIT 15;
