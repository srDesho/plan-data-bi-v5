# MD01 · Movimiento de inventario por producto (referencia)

Ábrelo solo después de tu intento.

## Grano

Una fila de `fact_inventario` representa el movimiento de **un producto en un periodo de inventario**. En `04_DATASETS/inventario.csv` hay un periodo ficticio por producto, así que el archivo tiene 40 filas: una por producto.

## Hecho

| Columna | Tipo | Rol |
|---|---|---|
| producto_id | entero | clave foránea hacia dim_producto |
| periodo_id | entero | clave foránea hacia dim_periodo |
| stock_inicial | entero | medida semiaditiva: se suma entre productos, no entre periodos |
| stock_final | entero | medida semiaditiva: se suma entre productos, no entre periodos |
| salidas_unidades | entero | medida aditiva: se puede sumar entre productos y entre periodos |

La clave del hecho es (producto_id, periodo_id).

## Dimensiones

### dim_producto

Clave: `producto_id`. Atributos: nombre, categoria, precio_unitario, costo_unitario. Es la misma tabla que ya usa `fact_ventas`.

### dim_periodo

Clave: `periodo_id`. Atributos: etiqueta del periodo, fecha de inicio y fecha de fin. Es una dimensión propia del inventario porque el periodo del archivo es ficticio y no coincide con las fechas de venta.

## Dimensiones conformadas

`dim_producto` es conformada: tiene la misma clave y los mismos atributos en el inventario y en las ventas, y por eso se pueden comparar «salidas de inventario» y «unidades vendidas» por producto o por categoría. `dim_periodo` no se comparte con las ventas. `fact_inventario` y `fact_ventas` no se relacionan entre sí; se comparan solo por la dimensión compartida, nunca con una relación directa de hecho a hecho.

## Controles de calidad

1. `producto_id` no se repite dentro de un mismo periodo (clave del hecho única).
2. Todo `producto_id` del hecho existe en `dim_producto` (sin huérfanos).
3. `stock_inicial`, `stock_final` y `salidas_unidades` son enteros no negativos.
4. El número de filas del hecho (40) coincide con el del archivo de origen.
5. La suma de `salidas_unidades` por categoría coincide con la del archivo agrupado a mano; y no se compara como venta, porque el inventario es un caso independiente.
