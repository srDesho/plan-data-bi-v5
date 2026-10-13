# ES3B · Examen · clientes cuya última compra fue antes de agosto

Nivel 3/3 · Tiempo objetivo 10 min · Primera vez: 25–45 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/04_SQL_CTE_ventanas.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Lista los clientes cuya última compra entregada es anterior al 2026-08-01, con esa fecha.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)

**Una fila del resultado representa:** un cliente cuya última compra fue antes del 2026-08-01.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `cliente_id` — código del cliente
2. `ultima` — fecha de su último pedido entregado

**Reglas del requerimiento:**

- Solo pedidos entregados.
- Ordena por `cliente_id`.

## Comprobación

Contrato de resultado: **11 filas × 2 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES3B mi_trabajo/sql/ES3B.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES3B.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Primero la última fecha por cliente; luego una condición sobre ella.
2. **Concepto SQL.** MAX(fecha) por cliente con HAVING.
3. **Si no cuadra.** Debes obtener 11 filas.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Dos columnas.
- [ ] 11 filas.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES3B.sql`, solo después del intento.
