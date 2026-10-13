SELECT ROUND(SUM(i.cantidad*i.precio_unitario)/COUNT(DISTINCT p.pedido_id),2) ticket FROM pedidos p JOIN pedido_items i USING(pedido_id) WHERE p.estado='entregado';
