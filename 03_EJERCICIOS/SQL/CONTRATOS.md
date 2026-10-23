# Contratos de resultados SQL

Tabla de comprobación: para cada ejercicio, las columnas que debe devolver tu consulta (en ese orden) y el número de filas esperado.
Los nombres de columna son libres; el orden y el contenido, no. **No es el enunciado**: lo que debes calcular, con qué filtros, redondeo y orden, está en cada archivo del ejercicio.
El corrector compara el contenido completo; no revisa el orden de las filas salvo cuando decide cuáles entran (LIMIT).

| ID | Columnas en orden | Filas |
|---|---|---:|
| S1 | cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta | 10 |
| S2 | tipo | 5 |
| S3 | cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta | 14 |
| S4 | nombre, precio_unitario | 3 |
| S5 | cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta | 15 |
| S6 | cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta | 12 |
| S7 | cliente_id, nombre_negocio, tipo, zona, ruta, fecha_alta | 6 |
| S8 | pedido_id, cliente_id, vendedor_id, fecha, estado | 399 |
| S9 | nombre, categoria, precio_unitario | 8 |
| S10 | total_clientes | 1 |
| G1 | estado, pedidos | 2 |
| G2 | unidades | 1 |
| G3 | valor_items | 1 |
| G4 | categoria, precio_prom, precio_min, precio_max | 5 |
| G5 | ruta, clientes | 6 |
| G6 | ruta, clientes | 3 |
| G7 | tipo, zona, clientes | 32 |
| G8 | mes, pedidos | 6 |
| J1 | pedido_id, fecha, nombre_negocio | 3600 |
| J2 | ventas_bs | 1 |
| J3 | categoria, ventas_bs | 5 |
| J4 | nombre, ventas_bs | 6 |
| J5 | cliente_id, nombre_negocio | 19 |
| J6 | nombre, unidades | 5 |
| E1 | tipo, clientes | 4 |
| E2 | nombre, precio_unitario | 3 |
| E3 | mes, anulados | 6 |
| E4 | ruta, ventas_bs | 6 |
| E5 | nombre_negocio, pedidos_entregados | 17 |
| E6 | tipo, categoria, unidades | 25 |
| E7 | pedido_id, items | 3 |
| E8 | cliente_id, nombre_negocio | 51 |
| CL1 | con_espacios | 1 |
| CL2 | cliente_id, nombre_limpio | 120 |
| CL3 | zona, clientes | 8 |
| CL4 | clientes | 1 |
| K1 | pedido_id, fecha, drop_bs, unidades | 3442 |
| K2a | drop_prom | 1 |
| K2b | ruta, drop_prom, pedidos | 6 |
| K3 | pedido_id, drop_bs | 1325 |
| K4 | tamano, pedidos | 3 |
| K5 | pedido_id, nombre_negocio, vendedor, drop_bs | 10 |
| K6 | nombre_negocio, drop_prom, pedidos | 5 |
| V1 | cliente_id, nombre_negocio, ultima_compra | 120 |
| V2 | cliente_id, nombre_negocio, ultima_compra, dias_sin_comprar | 11 |
| V3 | nombre_negocio, ventas, pct, pct_acum | 15 |
| V4 | abc, clientes, pct_ventas | 3 |
| V5 | ruta, puesto, nombre_negocio, ventas | 18 |
| X1 | mes, ventas_bs | 6 |
| X2 | mes, drop_prom | 6 |
| X3 | nombre_negocio, ventas_bs | 10 |
| X4 | categoria, ventas_bs, pct_total | 5 |
| X5 | ruta, pedidos, anulados, pct_anulados | 6 |
| X6 | pedido_id, fecha, nombre_negocio, drop_bs | 1 |
| X7 | puesto, nombre, ventas_bs | 6 |
| X8 | cliente_id, nombre_negocio, ventas_bs | 6 |
| N1 | mes, ruta, ventas, presupuesto_bs, cumplimiento | 36 |
| N2 | planificadas, realizadas, cobertura | 1 |
| N3 | pedidos, realizadas, efectividad | 1 |
| N4 | planificados, visitados | 1 |
| N5 | mes, ventas_bs, crecimiento | 6 |
| N6 | mes, acumulado | 6 |
| N7 | cliente_id, ultima, recencia | 120 |
| N8 | prueba, fallos | 2 |
| N9 | ticket | 1 |
| N10 | cliente_id, sku_distintos | 120 |
| N11 | producto_id, rotacion | 40 |
| N12 | activos, pedidos, frecuencia | 1 |
| N13 | id, parent, notused, detail | 1 |
| N14 | cliente_id, ruta, zona, estado_calidad | 120 |
| N15 | producto_id, unidades, puesto | 40 |
| N16 | cliente_id, nombre, motivo | 6 |
| ES1A | cliente_id, nombre_negocio | 25 |
| ES1B | categoria, productos, precio_medio | 2 |
| ES1C | anulados | 1 |
| ES2A | ventas | 1 |
| ES2B | cliente_id, nombre_negocio | 30 |
| ES2C | vendedor_id, nombre, pedidos | 6 |
| ES3A | ruta, ticket | 6 |
| ES3B | cliente_id, ultima | 11 |
| ES3C | ruta, ventas, pct_total | 6 |
| SQ01a | nombre, precio_unitario, precio_con_iva | 5 |
| SQ01b | cliente_id, nombre_negocio, tipo | 6 |
| SQ01c | producto_id, salidas_unidades, stock_final, diferencia | 5 |
| SQ02a | cliente_id, nombre_negocio, zona | 14 |
| SQ02b | cliente_id, nombre_negocio, zona | 103 |
| SQ02c | cliente_id, nombre_negocio | 10 |
| SQ02d | tipo, ruta | 24 |
| SQ03a | estado, pedidos | 2 |
| SQ03b | producto_id, unidades | 3 |
| SQ03c | fecha, plan, real | 4 |
| SQ04a | ruta, ventas_bs | 6 |
| SQ04b | total_bs | 1 |
| SQ05a | vendedor_id, estado, pedidos | 12 |
| SQ05b | vendedor_id, pct_anulados | 6 |
| SQ05c | vendedor_id, pedidos | 2 |
| SQ06a | categoria, ruta, unidades | 5 |
| SQ06b | tipo, pedidos | 5 |
| SQ07a | cliente_id, nombre_negocio | 24 |
| SQ07b | ruta, clientes_sin_pedido_tomado | 6 |
| SQ08a | total_bs | 1 |
| SQ08b | total_bs | 1 |
| SQ08c | filas_unidas | 1 |
| SQ08d | total_bs | 1 |
| SQ09a | clase, clientes | 2 |
| SQ09b | zona, clientes | 8 |
| SQ09c | ruta, efectividad | 6 |
| SQ10a | producto_id, nombre, precio_unitario | 15 |
| SQ10b | cliente_id, pedidos | 10 |
| SQ11a | ruta, mes, ventas, presupuesto_bs, cumplimiento | 6 |
| SQ11b | cliente_id, ventas | 5 |
| SQ12a | categoria, nombre, unidades, pos | 10 |
| SQ13a | nombres_con_espacios | 1 |
| SQ13b | ruta, sin_zona | 2 |
| SQ13c | items_sin_pedido | 1 |
| SQ13d | pedidos_sin_cliente | 1 |
| KP01a | vendedor_id, ventas_bs, dias_con_ventas, productividad_bs_dia | 6 |
| KP01b | ruta, ventas_agosto, ventas_septiembre, variacion_abs, variacion_pct | 6 |
| KP01c | ruta, ventas_marzo, ventas_abril, variacion_abs, variacion_pct | 6 |
| SQ14a | pedidos, entregados, anulados | 1 |
| SQ14b | suma_meses, total_directo | 1 |
| SQ15a | mes, ventas, acumulado, pct_acumulado | 6 |
| SQ16a | producto_id, nombre, unidades, acum_antes, clase | 40 |
| SQ16b | productos_a | 1 |
| SQ17a | mes, categoria, pedidos, unidades, ventas_bs | 30 |
| SQ17b | control | 1 |
