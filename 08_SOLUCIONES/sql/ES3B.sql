SELECT cliente_id,MAX(fecha) ultima FROM pedidos WHERE estado='entregado' GROUP BY cliente_id HAVING MAX(fecha)<'2026-08-01' ORDER BY cliente_id;
