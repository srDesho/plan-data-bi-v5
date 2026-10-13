# Fuentes, claves y reglas

Todos los datos comerciales son ficticios. La distribuidora existente se reutiliza del ZIP v 3;
visitas, presupuesto, inventario, pilotos, transferencia y final se generaron para este programa.
No contienen exportaciones privadas de Cruzimex. UTF-8; CSV principal usa coma y raw ETL punto y coma.

`comercial.db` contiene las cinco tablas originales más tres tablas auxiliares.
La base original permanece en `distribuidora/distribuidora.db`.

| Tabla | Grano y clave | Columnas y tipos conceptuales | Filas |
|---|---|---|---:|
| clientes | Cliente; cliente_id | ID entero, nombre_negocio texto, tipo texto, zona texto nullable, ruta texto, fecha_alta fecha ISO |120|
| vendedores | Vendedor; vendedor_id | ID entero, nombre texto, ruta texto |6|
| productos | Producto; producto_id | ID entero, nombre/categoria texto, precio_unitario y costo_unitario Bs numéricos |40|
| pedidos | Pedido; pedido_id | ID entero, cliente_id/vendedor_id enteros, fecha ISO, estado entregado/anulado |3600|
| pedido_items | Línea; item_id | ID entero, pedido_id/producto_id enteros, cantidad unidades, precio_unitario Bs |16178|
| visitas | Visita planificada; visita_id | ID entero, fecha ISO, cliente_id, ruta, planificada/realizada/pedido_tomado indicadores 0/1 |480|
| presupuesto | Mes/ruta; (mes, ruta) | mes YYYY-MM, ruta texto, presupuesto_bs Bs numérico |36|
| inventario | Producto, periodo ficticio separado; producto_id | stock_inicial, stock_final, salidas_unidades enteros no negativos |40|

Relaciones: pedido→cliente y vendedor; ítem→pedido y producto; visita→cliente.
Visitas representan cuatro jornadas de agenda en septiembre; pedido_tomado registra conversión simulada,
no es una FK a pedidos ni debe utilizarse como venta entregada. Presupuesto es una meta ficticia,
no se generó a partir de ventas. Inventario es un caso independiente y no cuadra movimientos
de stock de la distribuidora histórica, que no tiene todas las entradas/salidas.

Los pedidos cubren 2026-04-01 a 2026-09-30. Un pedido es un drop en esta práctica;
un producto puede aparecer en muchos pedidos. En otros sistemas debes revisar esa equivalencia.

## Raw ETL existente

`distribuidora/etl/ventas_erp_raw.csv`: 16378 filas de texto.
Columnas nro_pedido, fecha, cliente, ruta, vendedor, estado, producto, categoria, cantidad, precio_unitario.
Tres fechas admitidas: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YY. Hay 200 duplicados,
301 vendedores vacíos y representaciones de texto variadas. En este caso la clave normalizada
es nro_pedido/producto. Una tabla de vendedores_por_ruta única permite recuperar faltantes.
La salida correcta tiene 16178 filas, 3600 pedidos y 120 clientes.

`drop_por_pedido.csv`: pedido_id, fecha, ruta, drop_bs y unidades. Una fila por entregado;
3442 filas. Sirve para estadística y para comprobar las agregaciones SQL.

Los diccionarios de transferencia/final están junto a sus CSV. Datos de inferencia:
`experimento_piloto.csv` = una tienda por fila/grupo con ticket_bs; `encuesta_canales.csv` =
una tienda por fila/grupo con compra binaria. Ambos son simulaciones separadas.
