SELECT producto_id,ROUND(1.0*salidas_unidades/NULLIF((stock_inicial+stock_final)/2.0,0),2) rotacion FROM inventario ORDER BY producto_id;
