-- SQ14 · Conciliar una carga
-- Referencia: ábrela solo después de tu intento.

-- apartado a
SELECT (SELECT COUNT(*) FROM pedidos) AS pedidos, (SELECT COUNT(*) FROM pedidos WHERE estado='entregado') AS entregados, (SELECT COUNT(*) FROM pedidos WHERE estado='anulado') AS anulados;

-- apartado b
WITH m AS (SELECT strftime('%Y-%m',p.fecha) AS mes, SUM(i.cantidad*i.precio_unitario) AS ventas FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id WHERE p.estado='entregado' GROUP BY mes) SELECT ROUND(SUM(ventas),2) AS suma_meses, (SELECT ROUND(SUM(i.cantidad*i.precio_unitario),2) FROM pedidos p JOIN pedido_items i ON i.pedido_id=p.pedido_id WHERE p.estado='entregado') AS total_directo FROM m;

-- apartado a (respuesta abierta): entregados + anulados = pedidos totales (3442 + 158 = 3600): no se perdió ni se duplicó ningún pedido.

-- apartado b (respuesta abierta): la suma de las ventas mensuales es igual al total directo: agrupar por mes no pierde ni duplica ventas.
