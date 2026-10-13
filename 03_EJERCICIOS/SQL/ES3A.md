# ES3A · Examen · ticket promedio de septiembre por ruta

Nivel 3/3 · Tiempo objetivo 10 min · Primera vez: 30–50 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/04_SQL_CTE_ventanas.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Calcula el ticket promedio (valor medio por pedido) de los pedidos entregados de septiembre de 2026 (del 01 al 30), por ruta del cliente. Drop size de un pedido = suma de cantidad × precio_unitario de todas sus líneas (el valor de ese pedido en Bs). Es una cifra por pedido, no por línea.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)
- `pedido_items`: item_id (clave), pedido_id, producto_id, cantidad (unidades), precio_unitario (Bs)
- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Cómo se relacionan:** `pedido_items.pedido_id = pedidos.pedido_id`; `pedidos.cliente_id = clientes.cliente_id`.

**Una fila del resultado representa:** una ruta.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `ruta` — ruta del cliente
2. `ticket` — promedio del valor por pedido, con 2 decimales

**Reglas del requerimiento:**

- Primero el valor por pedido y luego el promedio por ruta.
- Ordena por `ruta`.

## Comprobación

Contrato de resultado: **6 filas × 2 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES3A mi_trabajo/sql/ES3A.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES3A.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Dos niveles de agrupación.
2. **Concepto SQL.** CTE con el valor por pedido y luego agrupar por ruta.
3. **Si no cuadra.** Seis rutas; los valores son del orden de varios cientos de Bs.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Dos columnas.
- [ ] 6 filas.
- [ ] El promedio es de valores por pedido; no promedias líneas ni promedios de rutas.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES3A.sql`, solo después del intento.
