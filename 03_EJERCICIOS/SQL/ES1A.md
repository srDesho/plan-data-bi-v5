# ES1A · Examen · clientes de la ruta R06

Nivel 1/3 · Tiempo objetivo 10 min · Primera vez: 10–20 min · Base: `04_DATASETS/comercial.db`.
Lee `02_TEORIA/01_SQL_basico.md` antes del examen, no durante la resolución.

## Situación

Variante de examen: resuélvela sin ayuda dentro del tiempo del examen. Lista los clientes de la ruta R06.

## Qué debes entregar

**Tablas que necesitas** (detalle en `04_DATASETS/DICCIONARIO.md`):

- `clientes`: cliente_id (clave), nombre_negocio, tipo, zona (puede estar vacía), ruta (R01…R06), fecha_alta

**Una fila del resultado representa:** un cliente de R06.

**Columnas del resultado, en este orden** (los nombres de las columnas son libres; el orden y el contenido, no):

1. `cliente_id` — código del cliente
2. `nombre_negocio` — nombre, tal como está guardado

**Reglas del requerimiento:**

- Solo la ruta R06.
- Ordena por `cliente_id`.

## Comprobación

Contrato de resultado: **25 filas × 2 columnas** (`CONTRATOS.md` lo lista como ayuda de comprobación; no sustituye este enunciado).
Corrector: `python herramientas/corregir_sql.py ES1A mi_trabajo/sql/ES1A.sql`. Compara el contenido completo, sin importar el orden de las filas salvo cuando el orden decide cuáles entran (por ejemplo, un LIMIT); no te muestra la consulta de referencia.
Entrega: `mi_trabajo/sql/ES1A.sql` y una interpretación de dos frases: qué mide el resultado y qué no puedes concluir con él.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Una condición de igualdad sobre `ruta`.
2. **Concepto SQL.** WHERE + ORDER BY.
3. **Si no cuadra.** R06 es una de las rutas grandes (G5): debes obtener 25 filas.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] Dos columnas.
- [ ] 25 filas.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/sql/ES1A.sql`, solo después del intento.
