SELECT ROUND(SUM(i.cantidad*i.precio_unitario),2) ventas FROM pedido_items i JOIN pedidos p USING(pedido_id) JOIN productos pr USING(producto_id) WHERE p.estado='entregado' AND pr.categoria='Snacks';
