# RM01 · fact_visitas (referencia)

Ábrelo solo después de tu intento.

## Grano

Una fila de `fact_visitas` representa **una visita planificada a un cliente en una fecha**; `04_DATASETS/visitas.csv` tiene 480 filas (120 clientes × 4 jornadas de agenda de septiembre).

## Hecho

| Columna | Tipo | Rol |
|---|---|---|
| visita_id | entero | identificador de la fila (clave del hecho) |
| cliente_id | entero | clave foránea hacia dim_cliente |
| fecha_id | entero AAAAMMDD | clave foránea hacia dim_fecha |
| planificada | 0/1 | medida aditiva (indicador) |
| realizada | 0/1 | medida aditiva (indicador) |
| pedido_tomado | 0/1 | medida aditiva (indicador de conversión simulada) |

`ruta` es un atributo del cliente: se toma de `dim_cliente` y no se repite en el hecho.

## Dimensiones

### dim_cliente

Clave: `cliente_id`. Atributos: nombre_negocio, tipo, zona, ruta, fecha_alta.

### dim_fecha

Clave: `fecha_id`. Atributos: fecha, mes, semana, día de la semana.

## Dimensiones conformadas

`dim_cliente` y `dim_fecha` son conformadas: son las mismas tablas, con las mismas claves, que usa `fact_ventas`; por eso se puede comparar visitas y ventas por cliente, por ruta o por día. `fact_visitas` y `fact_ventas` no se conectan entre sí. `pedido_tomado` no es una venta ni una clave hacia pedidos: no se suma como ingreso.

## Controles de calidad

1. `visita_id` es único (480 valores distintos).
2. Todo `cliente_id` de `fact_visitas` existe en `dim_cliente` (sin huérfanos).
3. Todo `fecha_id` existe en `dim_fecha`.
4. `planificada`, `realizada` y `pedido_tomado` solo valen 0 o 1.
5. Coherencia: `pedido_tomado` ≤ `realizada` ≤ `planificada` en cada fila; el conteo de realizadas (384) coincide con el filtro del origen.
