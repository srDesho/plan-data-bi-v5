WITH r AS (
  SELECT c.ruta, SUM(i.cantidad * i.precio_unitario) AS ventas
  FROM pedidos p
  JOIN pedido_items i USING (pedido_id)
  JOIN clientes c USING (cliente_id)
  WHERE p.estado = 'entregado'
  GROUP BY c.ruta
)
SELECT ruta, ROUND(ventas, 2) AS ventas, ROUND(100.0 * ventas / SUM(ventas) OVER (), 1) AS pct_total
FROM r
ORDER BY ventas DESC;
