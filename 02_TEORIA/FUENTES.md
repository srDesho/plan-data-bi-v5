# Fuentes oficiales, versiones y qué consultar

Los apuntes de `02_TEORIA/` son el material principal; estas páginas sirven para **confirmar sintaxis y ampliar**. Consulta solo la sección indicada y registra la pregunta que resolviste (lección 17.3). No necesitas leer toda la documentación.

## Versiones con las que se ejecutaron los ejemplos

| Componente | Versión | Dónde consta |
|---|---|---|
| Python | 3.12.10 | entorno `.venv` del curso |
| SQLite (módulo `sqlite3`) | 3.49.1 | incluido con Python |
| Pandas | 2.2.3 | `requirements.txt` |
| NumPy | 2.3.5 | `requirements.txt` |
| SciPy | 1.17.0 | `requirements.txt` |
| Matplotlib | 3.10.8 | `requirements.txt` (solo para guardar un histograma en 11.6) |
| Git | 2.45.1 (Windows) | para los ejemplos de 16.1; cualquier versión reciente sirve |

La salida de los ejemplos puede variar levemente con otras versiones (por ejemplo, los mensajes de error o el texto de `EXPLAIN QUERY PLAN`). Si la documentación en línea muestra una versión posterior, usa la de tu entorno. **No se agregaron dependencias nuevas** para reconstruir la teoría: todo el código usa lo que ya figura en `requirements.txt` y la biblioteca estándar.

## Cómo se verificó el contenido

- Los ejemplos SQL y Python de las lecciones se ejecutan con `python herramientas/verificar_teoria.py` y se comparan con la salida mostrada. Los datos son los de la mini-base inventada (`04_DATASETS/mini_base/`).
- Los **cálculos manuales** (estadística, KPIs) se recalcularon con Python.
- El **código DAX, el código M y los pasos de interfaz de Power BI Desktop y de Excel no se ejecutaron en esas aplicaciones**. Se presentan como guía de referencia con cifras de control calculadas con Python; la comprobación en Desktop es manual (lección 14.5).
- Los **ejemplos de SQL Server** (`TOP`, `DATEDIFF`) son referencia conceptual: no se ejecutaron en SQL Server.
- **No se comprobó en línea la disponibilidad actual de cada enlace** de esta página durante la reconstrucción. Las tareas centrales funcionan sin conexión una vez instaladas las dependencias.

## Python

| Tema | Recurso | Qué consultar | Lecciones |
|---|---|---|---|
| Lenguaje | [Tutorial de Python 3.12](https://docs.python.org/3.12/tutorial/) | tipos, control de flujo, estructuras de datos, errores y excepciones | 7.x, 8.5 |
| Texto | [Métodos de `str`](https://docs.python.org/3.12/library/stdtypes.html#string-methods) | `strip`, `split`, `replace`, `removeprefix` | 7.5 |
| Archivos | [`pathlib`](https://docs.python.org/3.12/library/pathlib.html) | `Path`, `read_text`, `open`, `mkdir` | 8.3 |
| CSV y JSON | [`csv`](https://docs.python.org/3.12/library/csv.html) y [`json`](https://docs.python.org/3.12/library/json.html) | `DictReader`, `DictWriter`, `dumps`, `loads` | 8.3 |
| Fechas | [`datetime`](https://docs.python.org/3.12/library/datetime.html) | `date.fromisoformat`, `strptime`, `timedelta` | 8.4, 9.6 |
| Dinero | [`decimal`](https://docs.python.org/3.12/library/decimal.html) | `Decimal` desde texto, exactitud | 7.7, 5.3 |
| Estadística básica | [`statistics`](https://docs.python.org/3.12/library/statistics.html) | `mean`, `median`, `stdev`, `pstdev`, `quantiles` | 11.3–11.5 |
| Combinatoria | [`itertools`](https://docs.python.org/3.12/library/itertools.html) | `combinations` | 12.4 |
| Registro | [`logging`](https://docs.python.org/3.12/library/logging.html) | `getLogger`, niveles, formato | 5.4 |
| Conexiones | [`contextlib.closing`](https://docs.python.org/3.12/library/contextlib.html#contextlib.closing) y [`sqlite3`](https://docs.python.org/3.12/library/sqlite3.html) | cerrar la conexión; ejecutar y confirmar | 5.4, 19 §4 |
| Pruebas | [`assert`](https://docs.python.org/3.12/reference/simple_stmts.html#the-assert-statement) | semántica y optimización | 8.7, 10.5 |

## SQL

| Tema | Recurso | Qué consultar | Lecciones |
|---|---|---|---|
| Consultas | [SQLite SELECT](https://www.sqlite.org/lang_select.html) | `WHERE`, `GROUP BY`, `HAVING`, `JOIN`, `ORDER BY`, `LIMIT` | 1.x–3.x |
| Funciones | [Funciones SQL de SQLite](https://www.sqlite.org/lang_corefunc.html) | `ROUND`, `TRIM`, `COALESCE`, `NULLIF` | 2.4–2.5 |
| Agregados | [Funciones de agregación](https://www.sqlite.org/lang_aggfunc.html) | `COUNT`, `SUM`, `AVG` | 2.1 |
| Fechas | [Fechas y horas](https://www.sqlite.org/lang_datefunc.html) | `strftime`, `julianday`, modificadores | 2.4 |
| CTE | [`WITH`](https://www.sqlite.org/lang_with.html) | CTE no recursivas | 4.2 |
| Ventanas | [Funciones de ventana](https://www.sqlite.org/windowfunctions.html) | `OVER`, `PARTITION BY`, marcos, `LAG`, `RANK` | 4.3 |
| Índices | [`EXPLAIN QUERY PLAN`](https://www.sqlite.org/eqp.html) | `SCAN` frente a `SEARCH` | 4.4 |
| SQL Server (referencia) | [`DATEDIFF`](https://learn.microsoft.com/en-us/sql/t-sql/functions/datediff-transact-sql) | límites de fecha y argumentos | 4.4 |

## NumPy, Pandas y estadística

| Tema | Recurso | Qué consultar | Lecciones |
|---|---|---|---|
| NumPy | [Absolute beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) | arreglos, operaciones, `axis` | 9.1 |
| Pandas | [Tutoriales introductorios](https://pandas.pydata.org/docs/getting_started/intro_tutorials/) | selección, agregación, fechas | 9.x–10.x |
| Pandas | [`merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) | `how`, `validate`, `indicator` | 10.3 |
| Pandas | [Datos faltantes](https://pandas.pydata.org/docs/user_guide/missing_data.html) | `isna`, `fillna`, `NaT` | 9.5 |
| Pandas | [`to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) | `format`, `errors` | 9.6 |
| SciPy | [`scipy.stats`](https://docs.scipy.org/doc/scipy/reference/stats.html) | `ttest_ind` (`equal_var`), `chi2_contingency` (`correction`), `t.ppf` | 12.2, 12.5, 12.6 |
| Matplotlib | [Tutorial de uso](https://matplotlib.org/stable/users/explain/quick_start.html) | `hist`, `savefig` | 11.6 |

Las definiciones, los ejemplos de negocio y las interpretaciones están desarrollados en las lecciones para que puedas estudiar sin depender de búsquedas. La documentación de SciPy sirve para confirmar parámetros; **no** reemplaza la lógica de los cálculos a mano.

## ETL, modelado y herramientas de BI

| Tema | Recurso | Qué consultar | Lecciones |
|---|---|---|---|
| Arquitectura medallón | [Databricks Medallion](https://docs.databricks.com/aws/en/lakehouse/medallion) | responsabilidades de Bronze, Silver y Gold | 5.1 |
| Modelado | [Esquema estrella en Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) | hechos, dimensiones, granularidad | 13.1–13.2 |
| Calendario | [Tablas de fechas](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables) | marcar la tabla y requisitos | 13.3 |
| DAX | [`CALCULATE`](https://learn.microsoft.com/en-us/dax/calculate-function-dax) | contexto de filtro | 14.3 |
| DAX | [`DIVIDE`](https://learn.microsoft.com/en-us/dax/divide-function-dax) | denominador cero y `BLANK` | 14.3 |
| Power Query | [Lenguaje M](https://learn.microsoft.com/en-us/powerquery-m/) | `Table.*`, `Csv.Document`, culturas | 14.2 |
| Excel | [Soporte de Microsoft para Excel](https://support.microsoft.com/es-es/excel) | `SUMAR.SI.CONJUNTO`, `BUSCARX`, tablas dinámicas, `PERCENTIL.INC` | 15.x |

## Git y comunicación

| Tema | Recurso | Qué consultar | Lecciones |
|---|---|---|---|
| Git | [Pro Git](https://git-scm.com/book/es/v2) | capítulos 1–2: `status`, `add`, `commit`, remotos | 16.1 |
| Ignorar archivos | [`gitignore`](https://git-scm.com/docs/gitignore) | patrones | 16.1 |

## Material complementario del curso

El PDF y los notebooks de la UAGRM aportados se incluyen como complemento en [`UAGRM/`](UAGRM/LEEME.md); no son requisito de ejecución del núcleo del curso.

Volver al [índice de la teoría](INDICE.md) · [Glosario](GLOSARIO.md).
