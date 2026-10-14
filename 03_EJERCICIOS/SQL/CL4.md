# CL4 · Vista temporal de clientes limpios

Nivel 2/3 · Tiempo objetivo 15 min · Primera vez: 30–50 min · Base: `04_DATASETS/comercial.db`.
Requisito: lee `02_TEORIA/02_SQL_agregados.md`.

## Situación

Para no repetir la limpieza en cada consulta, crea una vista temporal con los clientes ya limpios y compruébala con un conteo.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Una fila del resultado representa:** el total de la vista (una sola fila).

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `clientes` — cantidad de filas de la vista (consulta final)

**Reglas del requerimiento:**

- Crea una vista TEMPORAL llamada `clientes_limpios` con las seis columnas del cliente: `nombre_negocio` sin espacios en los extremos y en mayúsculas; `zona` con la etiqueta «Sin zona» cuando falta; el resto sin cambios.
- Una vista temporal no modifica el archivo de la base de datos.
- Tu archivo termina con una consulta que cuenta las filas de la vista, con la columna llamada `clientes` (debe dar 120).
- El corrector ejecuta todo el archivo y evalúa el resultado de la última consulta.

## Comprobación

Contrato de resultado: **1 fila × 1 columna** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py CL4 mi_trabajo/sql/CL4.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/CL4.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Son dos pasos en el mismo archivo: definir la vista y luego consultarla.
2. **Concepto SQL.** CREATE TEMP VIEW nombre AS SELECT … crea una vista que desaparece al cerrar la conexión (esta sintaxis no está en las lecciones: consulta la documentación de SQLite sobre vistas temporales). Separa las dos sentencias con punto y coma.
3. **Si no cuadra.** Si el corrector indica un error de sintaxis, ejecuta cada sentencia por separado con `ejecutar_sql.py` para ubicar cuál falla.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] La vista incluye las seis columnas del cliente, con la limpieza pedida.
- [ ] La consulta final devuelve una fila con 120.
- [ ] No usaste CREATE TABLE ni modificaste datos.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/CL4.sql`, solo después del intento.
