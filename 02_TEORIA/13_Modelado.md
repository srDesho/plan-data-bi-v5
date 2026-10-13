# Hechos, dimensiones y modelo estrella

El modelo responde a preguntas empresariales con una estructura explícita. Una tabla de hechos almacena eventos medibles; una dimensión los describe. En este proyecto, una fila de `fact_ventas` es una línea de producto en un pedido. La clave es `item_id`; `pedido_id` se repite y permite contar pedidos distintos. El monto es cantidad×precio y el estado evita perder anulaciones.

Dimensiones: cliente (código, nombre, tipo, zona, ruta), producto (SKU, categoría), vendedor y fecha. Cada clave de dimensión es única y aparece en muchas filas del hecho. Las relaciones deben ser 1:* y normalmente con filtro en un sentido desde dimensión a hecho. Una relación muchos a muchos puede ocultar un defecto de claves.

## Datos que no comparten granularidad

Presupuesto tiene una fila por mes y ruta; visitas tienen una fila por visita planificada. No añadas un presupuesto a cada línea de venta. El modelo del curso exporta `fact_presupuesto` y `fact_visitas` separados, más `dim_mes` y `dim_ruta`. Así puedes filtrar ventas y presupuesto con las mismas dimensiones conformadas sin multiplicarlos.

Relaciones propuestas: dim_cliente→fact_ventas, dim_producto→fact_ventas, dim_vendedor→fact_ventas, dim_fecha→fact_ventas; dim_mes→fact_ventas y fact_presupuesto; dim_ruta→fact_ventas, fact_presupuesto y fact_visitas. dim_fecha→fact_visitas. No conectes dim_ruta a dim_cliente en este diseño porque añadirías un camino alternativo hacia ventas.

## Calendario

La tabla fecha incluye TODOS los días del periodo, aunque no haya ventas. Debe tener una fecha única por fila, sin nulos ni huecos. Añade año, mes, mes_numero, mes_id y fecha_id. En Power BI marca la columna fecha como tabla de fechas, usa tipos Date y ordena etiquetas de mes por mes_numero o año/mes. Una fecha con hora debe convertirse al mismo nivel diario antes de relacionar.

La medida de ventas suma importes entregados; pedidos usa DISTINCTCOUNT. El importe es aditivo por cliente y producto, pero recencia, ticket y porcentajes no se suman. Recalcula razones en cada contexto en vez de sumar tickets.

## Límites

Este modelo usa la ruta actual del cliente del dataset; no modela cambios históricos de asignación. En un sistema real necesitarías fecha de vigencia o ruta del evento para comparar periodos históricos. No presentes como histórico un atributo maestro actual. La plantilla es deliberadamente básica y documenta ese límite.

Práctica: exportador de modelo y proyecto Power BI. Antes de abrir Power BI prueba claves únicas, huérfanos, filas del hecho y total de ventas. El diseño y CSV se comprueban automáticamente; las relaciones dentro de Power BI deben comprobarse manualmente.
