# ES1C · Examen · pedidos anulados de septiembre

Nivel 1/3 · Tiempo objetivo 10 min · Primera vez: 10–20 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/01_SQL_basico.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Cuenta los pedidos anulados con fecha del 2026-09-01 al 2026-09-30.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)

**Una fila del resultado representa:** el total (una sola fila).

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `anulados` — cantidad de pedidos anulados en septiembre

**Reglas del requerimiento:**

- Una fila y una columna llamada `anulados`.
- Ambos filtros a la vez: estado y rango de fechas.

## Comprobación

Contrato de resultado: **1 fila × 1 columna** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES1C mi_trabajo/sql/ES1C.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES1C.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Un conteo con dos condiciones.
2. **Concepto SQL.** COUNT(*) con WHERE … AND …; BETWEEN incluye ambos extremos.
3. **Si no cuadra.** Compara con E3: septiembre es una de sus seis filas.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Una fila.
- [ ] Estado y fechas están en el mismo WHERE, unidos con AND.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES1C.sql`, solo después del intento.
