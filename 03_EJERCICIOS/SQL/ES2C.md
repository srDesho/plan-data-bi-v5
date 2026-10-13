# ES2C · Examen · pedidos entregados por vendedor

Nivel 2/3 · Tiempo objetivo 10 min · Primera vez: 20–35 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/03_SQL_joins.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Cuenta los pedidos entregados de cada vendedor, incluyendo vendedores que no tengan ninguno.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `vendedores`: vendedor_id (clave), nombre, ruta
- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)

**Cómo se relacionan:** `pedidos.vendedor_id = vendedores.vendedor_id`.

**Una fila del resultado representa:** un vendedor.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `vendedor_id` — código del vendedor
2. `nombre` — nombre del vendedor
3. `pedidos` — pedidos entregados (0 si no tiene)

**Reglas del requerimiento:**

- Una fila por vendedor (seis).
- Ordena por `vendedor_id`.

## Comprobación

Contrato de resultado: **6 filas × 3 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES2C mi_trabajo/sql/ES2C.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES2C.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Parte de los vendedores.
2. **Concepto SQL.** LEFT JOIN desde vendedores con el estado en el ON; COUNT de una columna de `pedidos`.
3. **Si no cuadra.** Debes ver seis vendedores; la suma de pedidos es 3.442.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Tres columnas.
- [ ] 6 filas.
- [ ] Si un vendedor no tuviera pedidos entregados aparecería con 0: ningún vendedor desaparece.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES2C.sql`, solo después del intento.
