WITH v AS (
    SELECT c.cliente_id, c.nombre_negocio, c.ruta,
           SUM(i.cantidad * i.precio_unitario) AS ventas
    FROM pedidos p
    INNER JOIN pedido_items i ON i.pedido_id = p.pedido_id
    INNER JOIN clientes c     ON c.cliente_id = p.cliente_id
    WHERE p.estado = 'entregado'
    GROUP BY c.cliente_id, c.nombre_negocio, c.ruta
),
r AS (
    SELECT *, RANK() OVER (PARTITION BY ruta ORDER BY ventas DESC) AS puesto
    FROM v
)
SELECT ruta, puesto, nombre_negocio, ROUND(ventas, 2) AS ventas
FROM r
WHERE puesto <= 3
ORDER BY ruta, puesto;
