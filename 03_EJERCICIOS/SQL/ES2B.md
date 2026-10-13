# ES2B · Examen · clientes sin compra entregada en agosto

Nivel 2/3 · Tiempo objetivo 10 min · Primera vez: 25–40 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/03_SQL_joins.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Lista los clientes que no tuvieron ningún pedido entregado entre el 2026-08-01 y el 2026-08-31.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta
- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)

**Cómo se relacionan:** `pedidos.cliente_id = clientes.cliente_id`.

**Una fila del resultado representa:** un cliente sin compras entregadas en agosto.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `cliente_id` — código del cliente
2. `nombre_negocio` — nombre, tal como está guardado

**Reglas del requerimiento:**

- Incluye clientes sin pedidos o con pedidos solo en otros meses o anulados.
- Ordena por `cliente_id`.

## Comprobación

Contrato de resultado: **30 filas × 2 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES2B mi_trabajo/sql/ES2B.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES2B.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Pregunta por una ausencia (como J5).
2. **Concepto SQL.** LEFT JOIN con las condiciones en el ON y WHERE … IS NULL.
3. **Si no cuadra.** Debes obtener 30 filas.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Dos columnas.
- [ ] 30 filas.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES2B.sql`, solo después del intento.
