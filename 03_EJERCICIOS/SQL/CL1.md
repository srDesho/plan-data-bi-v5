# CL1 · Cuántos nombres tienen espacios sobrantes

Nivel 2/3 · Tiempo objetivo 15 min · Primera vez: 20–35 min · Base: `04_DATASETS/comercial.db`.
Requisito: lee `02_TEORIA/02_SQL_agregados.md`.

## Situación

Antes de unir bases, el equipo de datos quiere medir el problema: ¿cuántos nombres de negocio tienen espacios al inicio o al final?

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Una fila del resultado representa:** el total (una sola fila).

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `con_espacios` — cantidad de clientes cuyo nombre tiene espacios al inicio o al final

**Reglas del requerimiento:**

- Una fila y una columna llamada `con_espacios`.
- Cuenta un nombre si es distinto de sí mismo sin los espacios de los extremos.

## Comprobación

Contrato de resultado: **1 fila × 1 columna** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py CL1 mi_trabajo/sql/CL1.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/CL1.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Compara el texto original con una versión limpia de sí mismo; si difieren, tenía espacios sobrantes.
2. **Concepto SQL.** TRIM quita los espacios de los extremos (lección 2.4 «Redondeo, texto y fechas»; TRIM también aparece en 1.6). Compara con `<>` dentro de WHERE y cuenta.
3. **Si no cuadra.** Para ver ejemplos reales, selecciona `'[' || nombre_negocio || ']'` y mira cuáles muestran espacios dentro de los corchetes.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Una fila y una columna.
- [ ] Tu criterio no cuenta espacios intermedios.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/CL1.sql`, solo después del intento.
