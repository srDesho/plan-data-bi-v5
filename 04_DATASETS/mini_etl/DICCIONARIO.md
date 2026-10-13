# Datos sintéticos: mini-ETL (ME01–ME04)

Archivos pequeños para practicar un ETL completo antes del caso de la distribuidora. Son inventados.
Raw: `ventas_mini_raw.csv`, separador `;`, UTF-8. Catálogo: `productos_mini.csv`, separador `,`.
`ventas_mini_raw_v2.csv` repite el raw y añade tres filas; solo se usa en ME04.

Una fila válida es una línea de ticket. `ticket_id` es la clave. Los textos de tienda pueden traer espacios
sobrantes y mayúsculas distintas; el nombre normalizado es `Título` con un espacio entre palabras.

| Columna | Qué contiene | Regla |
|---|---|---|
| ticket_id | clave | no puede repetirse con contenido distinto (conflicto: detener) |
| fecha | ISO `YYYY-MM-DD` o `DD/MM/YYYY` | fecha imposible: rechazar |
| tienda | nombre de la tienda | normalizar espacios y mayúsculas |
| producto | código de catálogo | debe existir en `productos_mini.csv` |
| unidades | cantidad | entero positivo; `4.0` es válido, `2.5`, `0` y texto no |
| estado | entregado / anulado | otro valor: rechazar |
| precio | precio unitario | admite `Bs` y coma decimal; no negativo; máximo dos decimales |

Las filas anuladas se conservan en Silver y no suman a las ventas. El dinero se guarda en centavos enteros.
Los duplicados exactos se eliminan después de comprobar que no hay claves en conflicto. Cada fila rechazada
se guarda con su causa (palabras clave: `fecha`, `unidades`, `precio`, `producto`, `estado`).
Ecuación de control: `filas del raw = duplicados exactos + rechazadas + filas Silver`.
