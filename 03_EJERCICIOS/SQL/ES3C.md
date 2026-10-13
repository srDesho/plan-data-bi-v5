# ES3C · Examen · participación de cada ruta en las ventas

Nivel 3/3 · Tiempo objetivo 10 min · Primera vez: 30–50 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/04_SQL_CTE_ventanas.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Calcula las ventas entregadas de cada ruta y el porcentaje que representa sobre el total de todas las rutas. Venta entregada = cantidad × precio_unitario de las líneas cuyo pedido tiene estado `entregado`. La ruta es la del cliente.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)
- `pedido_items`: item_id (clave), pedido_id, producto_id, cantidad (unidades), precio_unitario (Bs)
- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Cómo se relacionan:** `pedido_items.pedido_id = pedidos.pedido_id`; `pedidos.cliente_id = clientes.cliente_id`.

**Una fila del resultado representa:** una ruta.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `ruta` — ruta
2. `ventas` — ventas entregadas, en Bs, con 2 decimales
3. `pct_total` — porcentaje sobre las ventas de las seis rutas, con 1 decimal

**Reglas del requerimiento:**

- Una fila por ruta (seis).
- El porcentaje se calcula sobre el total de las seis rutas.
- Ordena de mayor a menor venta.

## Comprobación

Contrato de resultado: **6 filas × 3 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES3C mi_trabajo/sql/ES3C.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES3C.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Necesitas la venta de cada ruta y el total general en la misma fila.
2. **Concepto SQL.** Resume las ventas por ruta en un CTE y después usa una función de ventana que sume sobre todas las filas (como en V3).
3. **Si no cuadra.** Los seis porcentajes deben sumar cerca de 100.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Tres columnas.
- [ ] 6 filas.
- [ ] El denominador del porcentaje es la suma de las seis rutas, no un total parcial.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES3C.sql`, solo después del intento.
