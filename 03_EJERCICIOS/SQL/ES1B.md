# ES1B · Examen · categorías con precio medio alto

Nivel 1/3 · Tiempo objetivo 10 min · Primera vez: 15–30 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/02_SQL_agregados.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Para cada categoría de producto, cuenta sus productos y calcula su precio medio; muestra solo las categorías cuyo precio medio supera 9 Bs.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `productos`: producto_id (clave), nombre, categoria, precio_unitario (Bs), costo_unitario (Bs)

**Una fila del resultado representa:** una categoría con precio medio mayor a 9.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `categoria` — categoría
2. `productos` — cantidad de productos de la categoría
3. `precio_medio` — precio promedio con 2 decimales

**Reglas del requerimiento:**

- El filtro es sobre el promedio ya calculado de cada categoría (estrictamente mayor que 9).
- Ordena por `categoria`.

## Comprobación

Contrato de resultado: **2 filas × 3 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES1B mi_trabajo/sql/ES1B.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES1B.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** El filtro depende de un resultado agrupado.
2. **Concepto SQL.** HAVING filtra grupos por una agregación.
3. **Si no cuadra.** Debes obtener 2 categorías. Si salen 5, filtraste antes de agrupar o no filtraste.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Tres columnas.
- [ ] 2 filas.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES1B.sql`, solo después del intento.
