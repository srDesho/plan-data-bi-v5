# CL3 · Clientes por zona con etiqueta para los vacíos

Nivel 2/3 · Tiempo objetivo 15 min · Primera vez: 25–40 min · Base: `04_DATASETS/comercial.db`.
Requisito: lee `02_TEORIA/02_SQL_agregados.md`.

## Situación

Para el informe de cobertura geográfica, los clientes sin zona deben aparecer bajo una etiqueta legible y no como un valor vacío.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Una fila del resultado representa:** una zona (o «Sin zona»).

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `zona` — zona, o la etiqueta «Sin zona» cuando no tiene
2. `clientes` — cantidad de clientes de la zona

**Reglas del requerimiento:**

- Una fila por zona, ocho en total, incluida «Sin zona» con 6 clientes.
- No cambies los datos de la tabla: la etiqueta solo existe en el resultado.
- Ordena de más a menos clientes; desempate por `zona`.

## Comprobación

Contrato de resultado: **8 filas × 2 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py CL3 mi_trabajo/sql/CL3.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/CL3.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Necesitas reemplazar el valor ausente por un texto, y agrupar por ese texto resultante.
2. **Concepto SQL.** COALESCE devuelve el primer valor que no es NULL (capítulo 01). Puedes agrupar por la misma expresión que muestras.
3. **Si no cuadra.** El grupo «Sin zona» debe sumar 6. Si ves una fila con zona vacía, no aplicaste la etiqueta antes de agrupar.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Dos columnas y ocho filas.
- [ ] «Sin zona» = 6.
- [ ] Los conteos suman 120.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/CL3.sql`, solo después del intento.
