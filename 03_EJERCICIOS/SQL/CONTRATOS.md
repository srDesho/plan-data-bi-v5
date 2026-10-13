# Contratos de resultados SQL

Los nombres de alias son libres; el orden de columnas sí importa.

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
| K1 | pedido_id, fecha, drop_bs, unidades | 3442 |
| K2 a | drop_prom | 1 |
| K2 b | ruta, drop_prom, pedidos | 6 |
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
| N1 | mes, ruta, ventas, presupuesto_bs, cumplimiento | 36 |
| N2 | planificadas, realizadas, cobertura | 1 |
| N3 | pedidos, realizadas, efectividad | 1 |
| N4 | planificados, visitados | 1 |
| N5 | mes, ROUND(ventas,2), crecimiento | 6 |
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
