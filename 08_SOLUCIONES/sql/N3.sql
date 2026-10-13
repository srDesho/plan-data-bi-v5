SELECT SUM(pedido_tomado) pedidos,SUM(realizada) realizadas,ROUND(100.0*SUM(pedido_tomado)/NULLIF(SUM(realizada),0),2) efectividad FROM visitas;
