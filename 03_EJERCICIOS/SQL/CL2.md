# CL2 · Nombres de negocio normalizados

Nivel 2/3 · Tiempo objetivo 15 min · Primera vez: 20–35 min · Base: `04_DATASETS/comercial.db`.
Requisito: lee `02_TEORIA/02_SQL_agregados.md`.

## Situación

Para unir el maestro con un archivo externo, necesitas una versión normalizada del nombre: sin espacios en los extremos y en mayúsculas.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Una fila del resultado representa:** un cliente.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `cliente_id` — código del cliente
2. `nombre_limpio` — nombre sin espacios en los extremos y en mayúsculas

**Reglas del requerimiento:**

- Una fila por cliente (120).
- No modifiques la tabla: solo calcula la columna en la consulta.
- Ordena por `cliente_id`.

## Comprobación

Contrato de resultado: **120 filas × 2 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py CL2 mi_trabajo/sql/CL2.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/CL2.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Hay dos transformaciones de texto que aplicar al mismo valor, una detrás de otra.
2. **Concepto SQL.** TRIM y UPPER son funciones de texto; se pueden anidar: el resultado de una es la entrada de la otra (capítulo 02).
3. **Si no cuadra.** Compara varios nombres a mano con los que devuelve tu consulta, especialmente los que tenían espacios (CL1).

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Dos columnas y 120 filas.
- [ ] Los nombres con espacios quedan limpios y en mayúsculas.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/CL2.sql`, solo después del intento.
