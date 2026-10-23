# Capítulo 9 — NumPy y Pandas básico: tablas después de entender listas y funciones

Aquí pasas de recorrer listas con bucles a trabajar con **tablas** completas: arreglos de NumPy, Series y DataFrames de Pandas. Aprendes a leer un CSV, a **perfilar** los datos antes de usarlos, a filtrar y ordenar, a tratar vacíos y duplicados sin destruir información y a convertir tipos y fechas. Cada operación se compara con su equivalente en SQL o con un cálculo hecho a mano.

**Tiempo total estimado de primera vez:** unas 5 h 40 min (6 lecciones). Se reparte con los ejercicios P17–P20 y el notebook N01.

**Antes de empezar:** el [capítulo 7](07_Python_basico.md) (listas, diccionarios, bucles) y la lección 8.3 (CSV).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 9.1 | [NumPy: de listas a arreglos](09_Pandas_basico/01_numpy_arrays.md) | vectorización, `shape`, `dtype`, máscaras, `NaN`, `ddof` | COMPLEMENTARIA | 50 min |
| 9.2 | [Series, DataFrame y leer un CSV](09_Pandas_basico/02_series_dataframe_csv.md) | índice, columnas, `read_csv`, tipos inferidos, códigos como texto | NÚCLEO · D15 | 60 min |
| 9.3 | [Inspeccionar los datos (perfilado)](09_Pandas_basico/03_inspeccionar.md) | `info`, `describe`, `value_counts`, función de perfil, 8 preguntas | NÚCLEO · D15 | 55 min |
| 9.4 | [Seleccionar, filtrar y ordenar](09_Pandas_basico/04_seleccion_filtros.md) | `loc`/`iloc`, máscaras, `&` y `\|`, `isin`, `str.contains`, `sort_values` | NÚCLEO · D17 | 55 min |
| 9.5 | [Vacíos y duplicados](09_Pandas_basico/05_nulos_duplicados.md) | política de faltantes, duplicados exactos y con conflicto | NÚCLEO · D16 | 60 min |
| 9.6 | [Tipos, textos y fechas](09_Pandas_basico/06_tipos_textos_fechas.md) | `to_numeric`, `to_datetime(format=)`, `.str`, `.dt`, centavos | NÚCLEO · D23 | 60 min |

## Ideas centrales

- Una operación primero se entiende en una lista de tres filas; después se usa la versión vectorizada.
- **Perfila antes de calcular**: las primeras cinco filas no demuestran que el resto esté limpio.
- `&` y `|` con paréntesis; `loc` por etiqueta, `iloc` por posición; `.copy()` antes de modificar un subconjunto.
- `errors="coerce"` convierte lo inválido en vacío: **cuenta y aparta** esas filas, no las pierdas.
- Una limpieza se cierra con el cuadre: entrada = válidas + rechazadas + duplicados eliminados.
- Los códigos con ceros iniciales se leen como texto; las fechas con `format=` explícito.
- NumPy usa `ddof=0` por defecto; Pandas, `ddof=1`.

## Ejercicios autónomos de este capítulo

P17–P20 y el notebook N01 en [`03_EJERCICIOS/Python/`](../03_EJERCICIOS/Python/) (enunciados) y [`03_EJERCICIOS/Notebooks/`](../03_EJERCICIOS/Notebooks/). Como puente con SQL, reproduce con CSV una consulta que ya resolviste en SQL y compara fila por fila (ordena ambos por su clave). Las microprácticas de las lecciones no son evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 10 — Pandas: transformar, unir y validar](10_Pandas_transformaciones.md).
