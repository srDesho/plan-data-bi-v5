# K2b · Drop size promedio por ruta

Nivel 3/3 · Tiempo objetivo 15 min · Primera vez: 40–65 min · Base: `04_DATASETS/comercial.db`.
Requisito: lee `02_TEORIA/03_SQL_joins.md`.

## Situación

Cada supervisor quiere comparar el valor típico de una entrega en su ruta. Drop size de un pedido = suma de cantidad × precio_unitario de todas sus líneas (el valor de ese pedido en Bs). Es una cifra por pedido, no por línea. La ruta es la del cliente.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)
- `pedido_items`: item_id (clave), pedido_id, producto_id, cantidad (unidades), precio_unitario (Bs)
- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Cómo se relacionan:** `pedido_items.pedido_id = pedidos.pedido_id`; `pedidos.cliente_id = clientes.cliente_id`.

**Una fila del resultado representa:** una ruta.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `ruta` — ruta del cliente
2. `drop_prom` — promedio del drop size de sus pedidos entregados, con 2 decimales
3. `pedidos` — cantidad de pedidos entregados de la ruta

**Reglas del requerimiento:**

- Una fila por ruta (seis).
- Primero el valor de cada pedido, luego el promedio por ruta (no promedies líneas ni promedios de promedios).
- Solo pedidos entregados.
- Ordena por `ruta`.

## Comprobación

Contrato de resultado: **6 filas × 3 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py K2b mi_trabajo/sql/K2b.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/K2b.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Necesitas dos agrupaciones encadenadas: por pedido y luego por ruta.
2. **Concepto SQL.** Resuelve primero el valor por pedido en una subconsulta o CTE, une el resultado con clientes y agrupa por ruta.
3. **Si no cuadra.** La suma de la columna `pedidos` debe ser 3.442.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Tres columnas y seis filas.
- [ ] `pedidos` suma 3.442.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/K2b.sql`, solo después del intento.
