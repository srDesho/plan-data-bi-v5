# Fuentes oficiales y lectura concreta

Los apuntes son el material principal; estas páginas sirven para confirmar sintaxis y ampliar.
Consulta solo la sección indicada y registra la pregunta que resolviste. No necesitas leer toda la documentación.
Versiones utilizadas en pruebas: Python 3.12, Pandas 2.2.3, NumPy 2.3.5, SciPy 1.17.0.
La documentación web puede mostrar versiones posteriores: si una API cambia, usa la versión de tu entorno.

| Tema | Recurso oficial | Qué consultar |
|---|---|---|
| Python | [Tutorial Python 3.12](https://docs.python.org/3.12/tutorial/) | capítulos 3–5, luego 7–8 y 12 |
| Archivos | [pathlib](https://docs.python.org/3.12/library/pathlib.html) | Path, read_text, open |
| Dinero | [Decimal](https://docs.python.org/3.12/library/decimal.html) | Decimal a partir de texto, precisión |
| SQL básico | [SQLite SELECT](https://www.sqlite.org/lang_select.html) | WHERE, GROUP BY, JOIN, ORDER BY |
| SQL ventanas | [SQLite ventanas](https://www.sqlite.org/windowfunctions.html) | aggregate, LAG, RANK, marcos |
| Fechas | [SQLite fechas](https://www.sqlite.org/lang_datefunc.html) | strftime y julianday |
| Índices | [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) | SCAN y SEARCH |
| SQL Server | [DATEDIFF](https://learn.microsoft.com/en-us/sql/t-sql/functions/datediff-transact-sql) | límites diarios y argumentos |
| Pandas | [Introductory tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/) | selección, agregación, merge, fechas |
| NumPy | [Absolute beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) | arrays y operaciones |
| Inferencia | [SciPy stats](https://docs.scipy.org/doc/scipy/reference/stats.html) | ttest_ind, chi 2_contingency, t, pearsonr |
| Arquitectura | [Databricks Medallion](https://docs.databricks.com/aws/en/lakehouse/medallion) | responsabilidades Bronze/Silver/Gold |
| Modelado | [Microsoft esquema estrella](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) | hechos, dimensiones, granularidad |
| Calendario | [Microsoft tablas fecha](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables) | marcar tabla y requisitos |
| DAX | [CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax) | contexto y filtros |
| DAX | [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax) | denominador cero y BLANK |
| Git | [Git book](https://git-scm.com/book/en/v2) | capítulos 1–2: status, add, commit, remotes |

SQLite SELECT, ventanas, Pandas, Python, SciPy, Microsoft esquema estrella/calendario/CALCULATE
y Databricks se consultaron durante la construcción. Los demás enlaces son referencias adicionales;
su disponibilidad individual no se comprobó. Las tareas centrales funcionan offline tras instalar dependencias.
El PDF y notebooks UAGRM aportados se incluyen como complemento; no son requisito de ejecución del núcleo.
