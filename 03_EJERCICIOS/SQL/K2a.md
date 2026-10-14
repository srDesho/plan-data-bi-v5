# K2a · Drop size promedio general

Nivel 3/3 · Tiempo objetivo 15 min · Primera vez: 35–60 min · Base: `04_DATASETS/comercial.db`.
Requisito: lee `02_TEORIA/03_SQL_joins.md`.

## Situación

La gerencia pregunta: ¿cuánto vale, en promedio, una entrega? Drop size de un pedido = suma de cantidad × precio_unitario de todas sus líneas (el valor de ese pedido en Bs). Es una cifra por pedido, no por línea.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `pedidos`: pedido_id (clave), cliente_id, vendedor_id, fecha (texto AAAA-MM-DD), estado (`entregado` o `anulado`)
- `pedido_items`: item_id (clave), pedido_id, producto_id, cantidad (unidades), precio_unitario (Bs)

**Cómo se relacionan:** `pedido_items.pedido_id = pedidos.pedido_id`.

**Una fila del resultado representa:** el promedio general (una sola fila).

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `drop_prom` — promedio del drop size por pedido entregado, en Bs, con 2 decimales

**Reglas del requerimiento:**

- Una fila y una columna llamada `drop_prom`.
- Promedia valores POR PEDIDO. No promedies el valor de las líneas.
- Solo pedidos entregados.

## Comprobación

Contrato de resultado: **1 fila × 1 columna** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py K2a mi_trabajo/sql/K2a.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/K2a.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Hay dos niveles: primero el valor de cada pedido, después el promedio de esos valores.
2. **Concepto SQL.** Una subconsulta en FROM (o un CTE) permite calcular primero el valor por pedido y promediar después (lecciones 2.3 «Granularidad y denominadores» y 4.2 «CTE»).
3. **Si no cuadra.** Si promedias directamente cantidad × precio sobre las líneas, mides el valor medio de una línea (unos 100 Bs), no de una entrega.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Una fila y una columna.
- [ ] Promedio por pedido, no por línea.
- [ ] El valor es consistente con K1 y con N9 (ticket medio).
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/K2a.sql`, solo después del intento.
