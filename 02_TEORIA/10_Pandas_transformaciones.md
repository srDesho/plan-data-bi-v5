# Capítulo 10 — Pandas: transformar, unir y validar

Con las tablas ya leídas y perfiladas (capítulo 9), aquí las **transformas**: columnas derivadas, agregaciones por grupo, uniones con control de cardinalidad, tablas de resumen exportadas y, sobre todo, **controles de calidad y reconciliación**. El capítulo termina con un catálogo de errores silenciosos (un merge que duplica importes, un `groupby` que pierde filas con clave vacía) y la forma de detectarlos. Es la base del mini-ETL y del ETL final.

**Tiempo total estimado de primera vez:** unas 6 h 0 min (6 lecciones). Se reparte con los ejercicios P21–P28.

**Antes de empezar:** el [capítulo 9](09_Pandas_basico.md) completo y la lección 3.4 de SQL (cuando el JOIN duplica).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 10.1 | [Columnas nuevas y transformaciones](10_Pandas_transformaciones/01_columnas_nuevas.md) | vectorizar, `np.where`/`np.select`, `map`, `.str`, `.dt`, `assign`, alineación por índice | núcleo · D16 | 55 min |
| 10.2 | [groupby y agregaciones](10_Pandas_transformaciones/02_groupby_agg.md) | `size`/`count`/`nunique`, agregación con nombre, `transform`, `pivot_table`, `dropna` | núcleo · D17 | 60 min |
| 10.3 | [merge y cardinalidad](10_Pandas_transformaciones/03_merge_cardinalidad.md) | `validate`, `indicator`, huérfanas, agregar antes de unir | núcleo · D17 | 65 min |
| 10.4 | [Tablas de resumen y exportación](10_Pandas_transformaciones/04_resumen_y_exportacion.md) | `to_csv`, `to_sql`, idempotencia, orden determinista | refuerzo | 55 min |
| 10.5 | [Controles de calidad y reconciliación](10_Pandas_transformaciones/05_controles_calidad.md) | estructura frente a fila, Bronze/Silver/Gold, cuadre de filas y de valor | refuerzo | 65 min |
| 10.6 | [Errores silenciosos](10_Pandas_transformaciones/06_errores_silenciosos.md) | catálogo de 10 errores que no avisan y su control | refuerzo | 60 min |

## Ideas centrales

- Limpiar no es eliminar todo lo extraño: es convertir representaciones conocidas a una forma acordada y **registrar lo que no se puede interpretar**.
- Todo `merge` lleva `validate` y se revisa `indicator`; después se comparan filas y totales.
- Sumar una columna de un nivel superior (meta, saldo) tras unir con un nivel más detallado multiplica el valor: agrega primero al mismo nivel.
- `groupby` descarta las claves vacías salvo `dropna=False`: los grupos deben sumar el total.
- Bronze conserva la entrada; Silver, los registros válidos con tipos y claves; los rechazos explican las diferencias; Gold alimenta el reporte.
- Cuadre de filas: Bronze = duplicados + rechazadas + Silver. Cuadre de valor: Silver = Gold.
- `assert` ayuda en ejercicios; en producción usa excepciones explícitas.

## Ejercicios autónomos de este capítulo

P21–P28, los notebooks N02/N03 y el proyecto ETL en [`03_EJERCICIOS/Python/`](../03_EJERCICIOS/Python/), [`03_EJERCICIOS/Notebooks/`](../03_EJERCICIOS/Notebooks/) y [`05_PROYECTOS/`](../05_PROYECTOS/). Las microprácticas de las lecciones no son evaluables. Dinero y fechas: usa `Decimal` y centavos enteros en el proyecto final (lección 9.6).

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 11 — Estadística descriptiva](11_Estadistica_descriptiva.md) (o, en el orden del plan, [Capítulo 6 — KPIs](06_KPIs.md)).
