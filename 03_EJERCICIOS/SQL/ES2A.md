# ES2A · Examen · ventas entregadas de Snacks

Nivel 2/3 · Tiempo objetivo 10 min · Primera vez: 20–35 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/03_SQL_joins.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Calcula las ventas entregadas de la categoría Snacks en todo el periodo. Venta entregada = cantidad × precio_unitario de las líneas cuyo pedido tiene estado `entregado`.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)
- `pedido_items`: item_id (clave), pedido_id, producto_id, cantidad (unidades), precio_unitario (Bs)
- `productos`: producto_id (clave), nombre, categoria, precio_unitario (Bs), costo_unitario (Bs)

**Cómo se relacionan:** `pedido_items.pedido_id = pedidos.pedido_id`; `pedido_items.producto_id = productos.producto_id`.

**Una fila del resultado representa:** el total (una sola fila).

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `ventas` — ventas entregadas de Snacks, en Bs, con 2 decimales

**Reglas del requerimiento:**

- Una fila y una columna llamada `ventas`.
- Solo pedidos entregados y solo productos de la categoría `Snacks`.

## Comprobación

Contrato de resultado: **1 fila × 1 columna** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES2A mi_trabajo/sql/ES2A.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES2A.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Dos filtros en tablas distintas.
2. **Concepto SQL.** Dos JOIN y SUM de cantidad × precio.
3. **Si no cuadra.** El resultado debe ser menor que el total de J2 (que incluye todas las categorías).

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Una fila.
- [ ] La categoría se filtra con `productos` y el estado con `pedidos`.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES2A.sql`, solo después del intento.
