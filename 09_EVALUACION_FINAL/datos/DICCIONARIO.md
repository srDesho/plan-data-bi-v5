# Datos sintéticos: evaluación final

Distribuidora ficticia. No provienen de Cruzimex. Separador raw `;`; catálogo `,`; UTF-8.
Una fila válida es una línea de documento. `linea_id` es la clave; `documento` puede repetirse.
`cliente_id`, `ruta` y `sku` son códigos; el nombre no es una clave.
Fecha admite ISO YYYY-MM-DD o DD/MM/YYYY. Precio unitario admite `Bs` y coma decimal.
Cantidad debe ser entera positiva; precio no negativo con dos decimales. Estado: entregado/anulado.
La venta válida es cantidad × precio de líneas entregadas. Los anulados se preservan en Silver y se excluyen de ventas Gold.
El catálogo tiene 60 SKU únicos y categorías. El join es muchos a uno por SKU.
Hay duplicados exactos y filas inválidas. Detecta primero conflictos de una misma clave;
elimina solo duplicados exactos; registra cada rechazo con su causa. No inventes valores.
No se solicitan impuestos, descuentos ni devoluciones: esos campos no están disponibles.
