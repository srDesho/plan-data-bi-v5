# INFORME FASE 2 · ETAPA 1 — Reconstrucción de la teoría (`02_TEORIA`)

Fecha de ejecución: 13 de octubre de 2026. Rama: `main`. Sin commits, sin ramas nuevas, sin push. No se tocaron `mi_trabajo`, D01 ni D02.

**Estado: Etapa 1 COMPLETA.** Las Etapas 2 y 3 siguen PENDIENTES y **no se iniciaron**: esperan las frases «AUTORIZO ETAPA 2» / «AUTORIZO ETAPA 3».

## Resumen

- Los 19 capítulos se reconstruyeron desde cero como material para un principiante. Los capítulos 1–18 son ahora un **archivo de entrada** (se conserva el nombre, porque lo enlazan guías y ejercicios) más una carpeta con **100 lecciones**. El capítulo 19 se conserva como archivo único con sus §1–§5 intactos (las guías los citan) y se amplía con un §6.
- De unas **10 157 palabras** en los 19 capítulos se pasó a unas **147 800** (con código y salidas). Antes, 14 de los 19 capítulos tenían menos de 500 palabras.
- Cada lección tiene: para qué sirve, términos nuevos definidos, ejemplo paso a paso con código explicado línea por línea y resultado, errores comunes, preguntas de comprobación con respuestas, micropráctica independiente con su comprobación y referencia a los ejercicios autónomos.
- Los ejemplos usan una **mini-base inventada** (`04_DATASETS/mini_base/`) distinta de los datos de los ejercicios; así ningún ejemplo revela una respuesta.
- **620 bloques de código se ejecutan y se comparan con la salida mostrada** (159 SQL y 461 Python) con una herramienta nueva, `herramientas/verificar_teoria.py`, que además revisa formato, enlaces, tiempos, definición previa de términos, glosario y fugas de resultados de ejercicios.
- Se eliminaron de la teoría los resultados y totales de ejercicios que antes estaban publicados (estadística de ST02/ST03, tabla de chi-cuadrado, totales de Power BI y Excel, cifras de los KPI de los ejercicios).
- Hallazgo importante para la Etapa 2: la suma de las lecciones es **≈ 91 h** de primera vez (más 1 h 15 min del capítulo 19), más de lo que cabe en las 6 semanas junto con los ejercicios. Hace falta definir una **ruta mínima** por modalidad (ver §6 y §10).

## 1. Inventario de capítulos

| Capítulo | Palabras antes | Palabras ahora | Lecciones | Bloques SQL | Bloques Python | Errores mostrados |
|---|---|---|---|---|---|---|
| 01 SQL_basico | 482 | 8 565 | 7 | 46 | 0 | 0 |
| 02 SQL_agregados | 691 | 7 007 | 5 | 44 | 0 | 0 |
| 03 SQL_joins | 431 | 5 786 | 4 | 31 | 0 | 0 |
| 04 SQL_CTE_ventanas | 474 | 6 008 | 4 | 24 | 0 | 0 |
| 05 calidad_ETL | 566 | 7 924 | 5 | 0 | 19 | 0 |
| 06 KPIs | 1 288 | 9 242 | 6 | 12 | 22 | 0 |
| 07 Python_basico | 514 | 17 752 | 13 | 0 | 119 | 13 |
| 08 Python_funciones_archivos | 416 | 9 583 | 7 | 0 | 52 | 8 |
| 09 Pandas_basico | 354 | 8 721 | 6 | 0 | 50 | 0 |
| 10 Pandas_transformaciones | 385 | 9 436 | 6 | 0 | 53 | 2 |
| 11 Estadistica_descriptiva | 461 | 12 677 | 9 | 0 | 43 | 0 |
| 12 Estadistica_inferencia | 479 | 12 428 | 8 | 0 | 29 | 0 |
| 13 Modelado | 398 | 4 392 | 3 | 0 | 14 | 0 |
| 14 PowerBI_DAX | 489 | 8 010 | 5 | 0 | 14 | 0 |
| 15 Excel_cuadres | 386 | 4 587 | 3 | 0 | 12 | 0 |
| 16 Git_comunicacion | 433 | 4 313 | 3 | 0 | 9 | 0 |
| 17 Transferencia_debug | 411 | 5 277 | 3 | 0 | 17 | 0 |
| 18 Entrevistas | 388 | 4 719 | 3 | 2 | 5 | 0 |
| 19 Puente_Python_a_ETL | 1 111 | 1 388 | — (archivo único) | 0 | 3 | 0 |
| **Total** | **10 157** | **147 815** | **100** | **159** | **461** | **23** |

Otros archivos de `02_TEORIA/`: `GLOSARIO.md` (359 → 1 724 palabras; ahora ≈ 100 términos, cada uno enlazado a la lección donde se define y comprobado automáticamente), `FUENTES.md` (319 → 957; con versiones exactas y qué se verificó y qué no), `INDICE.md` (nuevo, 1 147 palabras: orden de lectura, tiempos, dependencias, búsqueda por tema). Sin cambios: `UAGRM/`.

Los «Errores mostrados» son salidas de error que la lección enseña a leer; la herramienta comprueba que realmente ocurren.

## 2. Cambios por capítulo

| Cap. | Qué cambió |
|---|---|
| 1 SQL desde cero | De un resumen de 482 palabras a 7 lecciones: tabla/fila/columna/tipos, SELECT y alias, WHERE y operadores, NULL, ORDER BY y LIMIT, DISTINCT y LIKE, y un método de cinco preguntas para pasar del requerimiento a la consulta. Cada bloque con una tabla pequeña, consulta, resultado y explicación. |
| 2 Agregados | 5 lecciones: funciones de agregación (y cómo tratan NULL), GROUP BY/HAVING, granularidad y denominadores (división entera, promedio de promedios, NULLIF, controles), redondeo-texto-fechas y CASE/COALESCE. La sección «Funciones que usarás desde G4» pasó a las lecciones 2.4 y 2.5. |
| 3 JOIN | 4 lecciones: claves y cardinalidad, INNER JOIN, LEFT JOIN y anti-join, y duplicación por JOIN con los tres controles. Se quitó la cifra del total entregado de los ejercicios. |
| 4 Subconsultas y ventanas | 4 lecciones: subconsultas (incluida la trampa de `NOT IN` con NULL), CTE, funciones de ventana, y SQL para indicadores con fecha de corte, `EXPLAIN QUERY PLAN` y notas de SQL Server (no ejecutadas). Se eliminó el ejemplo ABC de V4. |
| 5 Calidad y ETL | 5 lecciones: ETL/ELT y medallón, contrato de datos, rechazos y reconciliación, cargas repetibles con `logging`, y estructura de cuatro funciones con un ETL completo de ejemplo. Se quitaron los totales del ETL de la distribuidora (16 378, 200, 301, 581, 1.468.924,50). |
| 6 KPIs | De una lista de 13 fórmulas a 6 lecciones con ficha del KPI, cumplimiento/cobertura/efectividad, ticket/frecuencia/activos, productividad/variaciones, ABC/Pareto/rotación e interpretación con «cuando faltan datos». Los 13 KPI se conservan con datos de la mini-base. Se eliminaron las cifras de los ejercicios. |
| 7 Python básico | De 514 palabras a 13 lecciones, desde «qué es un programa» hasta recorrer registros. Cada término (variable, secuencia, mutable, iteración, acumulador, argumento, parámetro, retorno...) se define antes de usarse; los bucles, los acumuladores y los registros se enseñan por separado antes de combinarlos. Incluye «Tu primera función corta» (P01) y los temas que citan P01–P08. |
| 8 Funciones y archivos | 7 lecciones: funciones con contrato, ámbito, archivos/CSV/JSON, módulos, excepciones, tracebacks y pruebas con depuración paso a paso. Se quitó el ejemplo de `cumplimiento` (ver §6). |
| 9 NumPy y Pandas básico | 6 lecciones: arreglos, Series/DataFrame/CSV, perfilado, selección y filtros, vacíos y duplicados, tipos y fechas. Se quitaron las referencias a totales de los ejercicios (3 442). |
| 10 Pandas: transformar | 6 lecciones: columnas nuevas, groupby, merge con `validate`/`indicator`, exportación, controles de calidad y un catálogo de errores silenciosos (merge que duplica importes, alineación por índice, `groupby` que pierde claves vacías...). |
| 11 Estadística descriptiva | De 461 palabras a 9 lecciones con **cálculo manual completo** sobre conjuntos pequeños y verificación posterior en Python/Pandas: población y variables, frecuencias, centro, dispersión (`n` frente a `n−1`), percentiles y atípicos, distribución y puntaje z, correlación, muestreo e informe descriptivo. Se eliminaron los resultados de ST02/ST03. |
| 12 Inferencia | 8 lecciones en el orden pedido: variabilidad muestral, intervalos de confianza, hipótesis y errores, p-valor calculado a mano por permutación, prueba t y Welch, chi-cuadrado, tamaño del efecto e interpretación. **No se empieza con SciPy**: cada cálculo se hace antes a mano. Se eliminaron la tabla de chi-cuadrado y el valor de `t` publicados. |
| 13 Modelado | 3 lecciones: hechos y dimensiones, modelo estrella con varios hechos, y tabla de fechas. Se mantiene la advertencia de que el modelo usa la ruta actual del cliente. |
| 14 Power BI / DAX | 5 lecciones: Power BI desde cero con configuración regional, Power Query y M, contexto de filtro simulado en Python, medidas útiles y diseño con lista de comprobación manual. **El código DAX/M y los pasos de interfaz no se ejecutaron en Desktop**; así consta en cada lección. Se eliminaron los totales de los ejercicios. |
| 15 Excel | 3 lecciones: importar y valor frente a formato, funciones para cuadrar, tablas dinámicas y diagnóstico de discrepancias. Las fórmulas no se ejecutaron en Excel; sí sus valores esperados (Python). Se eliminaron Q1/Q3 de ST02 y las cifras del caso de discrepancia. |
| 16 Git y comunicación | 3 lecciones: Git desde cero (comandos ejecutados en carpetas temporales), documentación (README, errores, decisiones) y portafolio/empleo honesto. |
| 17 Transferencia | 3 lecciones: los ocho pasos frente a un caso nuevo con cambios adversos, cómo reducir un total que no cuadra y cómo trabajar sin ayuda externa. |
| 18 Entrevistas | 3 lecciones: método de cuatro pasos, banco de preguntas con respuesta modelo y trampa, y preguntas conductuales con honestidad sobre el apoyo de IA. |
| 19 Puente | Se conservan §1–§5 sin cambios (las guías y los ejercicios los citan). Se añadieron el tiempo estimado, un mapa hacia las lecciones y un §6 de autoevaluación. |

## 3. Sublecciones nuevas (100)

**Capítulo 1 — SQL desde cero: una pregunta, una tabla y un resultado**

- 1.1 Tablas, filas, columnas y tipos de datos (45 min) — [`01_SQL_basico/01_tablas_filas_columnas.md`](02_TEORIA/01_SQL_basico/01_tablas_filas_columnas.md)
- 1.2 SELECT, FROM, alias y columnas calculadas (45 min) — [`01_SQL_basico/02_select_from_alias.md`](02_TEORIA/01_SQL_basico/02_select_from_alias.md)
- 1.3 WHERE: filtrar filas con operadores (50 min) — [`01_SQL_basico/03_where_operadores.md`](02_TEORIA/01_SQL_basico/03_where_operadores.md)
- 1.4 NULL: cuando falta el dato (40 min) — [`01_SQL_basico/04_null.md`](02_TEORIA/01_SQL_basico/04_null.md)
- 1.5 ORDER BY y LIMIT: ordenar y recortar (40 min) — [`01_SQL_basico/05_order_limit.md`](02_TEORIA/01_SQL_basico/05_order_limit.md)
- 1.6 DISTINCT y LIKE: valores únicos y búsquedas por patrón (40 min) — [`01_SQL_basico/06_distinct_like.md`](02_TEORIA/01_SQL_basico/06_distinct_like.md)
- 1.7 Del requerimiento a la consulta: un método de cinco preguntas (40 min) — [`01_SQL_basico/07_del_requerimiento_a_la_consulta.md`](02_TEORIA/01_SQL_basico/07_del_requerimiento_a_la_consulta.md)

**Capítulo 2 — Agregar sin perder el significado**

- 2.1 Funciones de agregación: contar, sumar, promediar (50 min) — [`02_SQL_agregados/01_funciones_agregadas.md`](02_TEORIA/02_SQL_agregados/01_funciones_agregadas.md)
- 2.2 GROUP BY y HAVING: una cifra por grupo (55 min) — [`02_SQL_agregados/02_group_by_having.md`](02_TEORIA/02_SQL_agregados/02_group_by_having.md)
- 2.3 Granularidad y denominadores: el número correcto para la pregunta correcta (55 min) — [`02_SQL_agregados/03_granularidad_denominadores.md`](02_TEORIA/02_SQL_agregados/03_granularidad_denominadores.md)
- 2.4 Redondeo, texto y fechas: preparar los datos para el reporte (50 min) — [`02_SQL_agregados/04_redondeo_texto_fechas.md`](02_TEORIA/02_SQL_agregados/04_redondeo_texto_fechas.md)
- 2.5 CASE y COALESCE: condiciones dentro de la consulta y valores faltantes (50 min) — [`02_SQL_agregados/05_case_coalesce.md`](02_TEORIA/02_SQL_agregados/05_case_coalesce.md)

**Capítulo 3 — JOIN: conectar tablas y controlar multiplicaciones**

- 3.1 Claves, relaciones y cardinalidad (45 min) — [`03_SQL_joins/01_claves_relaciones.md`](02_TEORIA/03_SQL_joins/01_claves_relaciones.md)
- 3.2 INNER JOIN: combinar tablas por coincidencia (55 min) — [`03_SQL_joins/02_inner_join.md`](02_TEORIA/03_SQL_joins/02_inner_join.md)
- 3.3 LEFT JOIN: conservar todo lo de la izquierda y encontrar a los que no aparecen (55 min) — [`03_SQL_joins/03_left_join_ausentes.md`](02_TEORIA/03_SQL_joins/03_left_join_ausentes.md)
- 3.4 Cuando el JOIN duplica: el error silencioso más caro (55 min) — [`03_SQL_joins/04_duplicacion_por_join.md`](02_TEORIA/03_SQL_joins/04_duplicacion_por_join.md)

**Capítulo 4 — Subconsultas, CTE, ventanas, fechas e índices**

- 4.1 Subconsultas: una consulta dentro de otra (50 min) — [`04_SQL_CTE_ventanas/01_subconsultas.md`](02_TEORIA/04_SQL_CTE_ventanas/01_subconsultas.md)
- 4.2 CTE: dividir una consulta larga en pasos con nombre (45 min) — [`04_SQL_CTE_ventanas/02_cte.md`](02_TEORIA/04_SQL_CTE_ventanas/02_cte.md)
- 4.3 Funciones de ventana: calcular sin colapsar las filas (65 min) — [`04_SQL_CTE_ventanas/03_ventanas.md`](02_TEORIA/04_SQL_CTE_ventanas/03_ventanas.md)
- 4.4 SQL para indicadores: fechas de corte, activos, crecimiento y rendimiento (55 min) — [`04_SQL_CTE_ventanas/04_sql_kpis_fechas_rendimiento.md`](02_TEORIA/04_SQL_CTE_ventanas/04_sql_kpis_fechas_rendimiento.md)

**Capítulo 5 — Calidad de datos y ETL: un proceso que puedas defender**

- 5.1 ETL, ELT y capas Bronze, Silver y Gold (50 min) — [`05_calidad_ETL/01_etl_elt_medallon.md`](02_TEORIA/05_calidad_ETL/01_etl_elt_medallon.md)
- 5.2 El contrato de datos: escribirlo antes de programar (50 min) — [`05_calidad_ETL/02_contrato_de_datos.md`](02_TEORIA/05_calidad_ETL/02_contrato_de_datos.md)
- 5.3 Rechazos, duplicados y reconciliación (55 min) — [`05_calidad_ETL/03_rechazos_y_reconciliacion.md`](02_TEORIA/05_calidad_ETL/03_rechazos_y_reconciliacion.md)
- 5.4 Cargas repetibles, registro (logging) y reproducibilidad (55 min) — [`05_calidad_ETL/04_cargas_registro_reproducibilidad.md`](02_TEORIA/05_calidad_ETL/04_cargas_registro_reproducibilidad.md)
- 5.5 Estructura de un ETL: cuatro funciones y un `main` pequeño (65 min) — [`05_calidad_ETL/05_estructura_etl_funciones.md`](02_TEORIA/05_calidad_ETL/05_estructura_etl_funciones.md)

**Capítulo 6 — KPIs empresariales: definición antes de fórmula**

- 6.1 Qué es un KPI: la ficha de definición y las ventas entregadas (50 min) — [`06_KPIs/01_que_es_un_kpi.md`](02_TEORIA/06_KPIs/01_que_es_un_kpi.md)
- 6.2 Cumplimiento, cobertura y efectividad (60 min) — [`06_KPIs/02_cumplimiento_cobertura_efectividad.md`](02_TEORIA/06_KPIs/02_cumplimiento_cobertura_efectividad.md)
- 6.3 Ticket medio, drop size, frecuencia y clientes activos (60 min) — [`06_KPIs/03_ticket_frecuencia_activos.md`](02_TEORIA/06_KPIs/03_ticket_frecuencia_activos.md)
- 6.4 Productividad, crecimiento y variaciones (55 min) — [`06_KPIs/04_productividad_variaciones.md`](02_TEORIA/06_KPIs/04_productividad_variaciones.md)
- 6.5 ABC, Pareto y rotación de inventario (60 min) — [`06_KPIs/05_abc_pareto_rotacion.md`](02_TEORIA/06_KPIs/05_abc_pareto_rotacion.md)
- 6.6 Interpretar, recomendar y qué hacer cuando faltan datos (55 min) — [`06_KPIs/06_interpretar_y_recomendar.md`](02_TEORIA/06_KPIs/06_interpretar_y_recomendar.md)

**Capítulo 7 — Python: construir el razonamiento antes de Pandas**

- 7.1 Qué es un programa y cómo se ejecuta (45 min) — [`07_Python_basico/01_que_es_un_programa.md`](02_TEORIA/07_Python_basico/01_que_es_un_programa.md)
- 7.2 Variables y asignación (45 min) — [`07_Python_basico/02_variables_asignacion.md`](02_TEORIA/07_Python_basico/02_variables_asignacion.md)
- 7.3 Tipos de datos y aritmética (50 min) — [`07_Python_basico/03_tipos_aritmetica.md`](02_TEORIA/07_Python_basico/03_tipos_aritmetica.md)
- 7.4 Tu primera función corta (55 min) — [`07_Python_basico/04_primera_funcion.md`](02_TEORIA/07_Python_basico/04_primera_funcion.md)
- 7.5 Texto: cadenas, métodos y f-strings (60 min) — [`07_Python_basico/05_texto.md`](02_TEORIA/07_Python_basico/05_texto.md)
- 7.6 Booleanos, comparaciones y None (50 min) — [`07_Python_basico/06_booleanos_comparaciones_none.md`](02_TEORIA/07_Python_basico/06_booleanos_comparaciones_none.md)
- 7.7 Conversiones de tipo y los primeros errores de valor (60 min) — [`07_Python_basico/07_conversiones.md`](02_TEORIA/07_Python_basico/07_conversiones.md)
- 7.8 Listas y tuplas: guardar varios valores (55 min) — [`07_Python_basico/08_listas_tuplas.md`](02_TEORIA/07_Python_basico/08_listas_tuplas.md)
- 7.9 Diccionarios y conjuntos (55 min) — [`07_Python_basico/09_diccionarios_sets.md`](02_TEORIA/07_Python_basico/09_diccionarios_sets.md)
- 7.10 Condicionales: if, elif y else (50 min) — [`07_Python_basico/10_condicionales.md`](02_TEORIA/07_Python_basico/10_condicionales.md)
- 7.11 Repetir: for y while (55 min) — [`07_Python_basico/11_for_while.md`](02_TEORIA/07_Python_basico/11_for_while.md)
- 7.12 Acumuladores y patrones de recorrido (70 min) — [`07_Python_basico/12_acumuladores.md`](02_TEORIA/07_Python_basico/12_acumuladores.md)
- 7.13 Recorrer registros: listas de diccionarios (65 min) — [`07_Python_basico/13_registros_listas_de_diccionarios.md`](02_TEORIA/07_Python_basico/13_registros_listas_de_diccionarios.md)

**Capítulo 8 — Funciones, errores y archivos reproducibles**

- 8.1 Funciones con contrato (55 min) — [`08_Python_funciones_archivos/01_funciones_con_contrato.md`](02_TEORIA/08_Python_funciones_archivos/01_funciones_con_contrato.md)
- 8.2 Ámbito de las variables y efectos secundarios (40 min) — [`08_Python_funciones_archivos/02_ambito_efectos.md`](02_TEORIA/08_Python_funciones_archivos/02_ambito_efectos.md)
- 8.3 Archivos: rutas, CSV y JSON (65 min) — [`08_Python_funciones_archivos/03_archivos_csv_json.md`](02_TEORIA/08_Python_funciones_archivos/03_archivos_csv_json.md)
- 8.4 Módulos e importaciones (55 min) — [`08_Python_funciones_archivos/04_modulos_imports.md`](02_TEORIA/08_Python_funciones_archivos/04_modulos_imports.md)
- 8.5 Excepciones: try, except y raise (55 min) — [`08_Python_funciones_archivos/05_excepciones.md`](02_TEORIA/08_Python_funciones_archivos/05_excepciones.md)
- 8.6 Leer un traceback (45 min) — [`08_Python_funciones_archivos/06_leer_tracebacks.md`](02_TEORIA/08_Python_funciones_archivos/06_leer_tracebacks.md)
- 8.7 Pruebas con assert y depuración paso a paso (55 min) — [`08_Python_funciones_archivos/07_pruebas_y_depuracion.md`](02_TEORIA/08_Python_funciones_archivos/07_pruebas_y_depuracion.md)

**Capítulo 9 — NumPy y Pandas básico: tablas después de entender listas y funciones**

- 9.1 NumPy: de listas a arreglos (50 min) — [`09_Pandas_basico/01_numpy_arrays.md`](02_TEORIA/09_Pandas_basico/01_numpy_arrays.md)
- 9.2 Series, DataFrame y leer un CSV (55 min) — [`09_Pandas_basico/02_series_dataframe_csv.md`](02_TEORIA/09_Pandas_basico/02_series_dataframe_csv.md)
- 9.3 Inspeccionar los datos antes de usarlos (perfilado) (55 min) — [`09_Pandas_basico/03_inspeccionar.md`](02_TEORIA/09_Pandas_basico/03_inspeccionar.md)
- 9.4 Seleccionar, filtrar y ordenar (55 min) — [`09_Pandas_basico/04_seleccion_filtros.md`](02_TEORIA/09_Pandas_basico/04_seleccion_filtros.md)
- 9.5 Valores vacíos y filas duplicadas (60 min) — [`09_Pandas_basico/05_nulos_duplicados.md`](02_TEORIA/09_Pandas_basico/05_nulos_duplicados.md)
- 9.6 Convertir tipos, limpiar texto y trabajar con fechas (60 min) — [`09_Pandas_basico/06_tipos_textos_fechas.md`](02_TEORIA/09_Pandas_basico/06_tipos_textos_fechas.md)

**Capítulo 10 — Pandas: transformar, unir y validar**

- 10.1 Columnas nuevas y transformaciones (55 min) — [`10_Pandas_transformaciones/01_columnas_nuevas.md`](02_TEORIA/10_Pandas_transformaciones/01_columnas_nuevas.md)
- 10.2 groupby y agregaciones (60 min) — [`10_Pandas_transformaciones/02_groupby_agg.md`](02_TEORIA/10_Pandas_transformaciones/02_groupby_agg.md)
- 10.3 merge: unir tablas y controlar la cardinalidad (65 min) — [`10_Pandas_transformaciones/03_merge_cardinalidad.md`](02_TEORIA/10_Pandas_transformaciones/03_merge_cardinalidad.md)
- 10.4 Tablas de resumen y exportación (CSV y SQLite) (55 min) — [`10_Pandas_transformaciones/04_resumen_y_exportacion.md`](02_TEORIA/10_Pandas_transformaciones/04_resumen_y_exportacion.md)
- 10.5 Controles de calidad y reconciliación en Pandas (65 min) — [`10_Pandas_transformaciones/05_controles_calidad.md`](02_TEORIA/10_Pandas_transformaciones/05_controles_calidad.md)
- 10.6 Errores silenciosos: los que no avisan (60 min) — [`10_Pandas_transformaciones/06_errores_silenciosos.md`](02_TEORIA/10_Pandas_transformaciones/06_errores_silenciosos.md)

**Capítulo 11 — Estadística descriptiva: resumir antes de concluir**

- 11.1 Población, muestra y tipos de variables (50 min) — [`11_Estadistica_descriptiva/01_poblacion_muestra_variables.md`](02_TEORIA/11_Estadistica_descriptiva/01_poblacion_muestra_variables.md)
- 11.2 Frecuencias: contar y expresar en porcentaje (45 min) — [`11_Estadistica_descriptiva/02_frecuencias.md`](02_TEORIA/11_Estadistica_descriptiva/02_frecuencias.md)
- 11.3 Media, mediana y moda (55 min) — [`11_Estadistica_descriptiva/03_media_mediana_moda.md`](02_TEORIA/11_Estadistica_descriptiva/03_media_mediana_moda.md)
- 11.4 Dispersión: rango, varianza y desviación estándar (65 min) — [`11_Estadistica_descriptiva/04_dispersion.md`](02_TEORIA/11_Estadistica_descriptiva/04_dispersion.md)
- 11.5 Percentiles, cuartiles y valores atípicos (65 min) — [`11_Estadistica_descriptiva/05_percentiles_atipicos.md`](02_TEORIA/11_Estadistica_descriptiva/05_percentiles_atipicos.md)
- 11.6 Distribuciones, histogramas, normalidad y puntaje z (65 min) — [`11_Estadistica_descriptiva/06_distribuciones_histograma_z.md`](02_TEORIA/11_Estadistica_descriptiva/06_distribuciones_histograma_z.md)
- 11.7 Correlación y causalidad (55 min) — [`11_Estadistica_descriptiva/07_correlacion_causalidad.md`](02_TEORIA/11_Estadistica_descriptiva/07_correlacion_causalidad.md)
- 11.8 Muestreo: cómo escoger una muestra que sirva (55 min) — [`11_Estadistica_descriptiva/08_muestreo.md`](02_TEORIA/11_Estadistica_descriptiva/08_muestreo.md)
- 11.9 Estadística descriptiva con Pandas: un informe completo (60 min) — [`11_Estadistica_descriptiva/09_descriptiva_con_pandas.md`](02_TEORIA/11_Estadistica_descriptiva/09_descriptiva_con_pandas.md)

**Capítulo 12 — Estadística inferencial: decidir con incertidumbre**

- 12.1 Por qué hace falta la inferencia: la variabilidad entre muestras (55 min) — [`12_Estadistica_inferencia/01_por_que_inferencia.md`](02_TEORIA/12_Estadistica_inferencia/01_por_que_inferencia.md)
- 12.2 Estimación e intervalos de confianza (65 min) — [`12_Estadistica_inferencia/02_estimacion_intervalo_confianza.md`](02_TEORIA/12_Estadistica_inferencia/02_estimacion_intervalo_confianza.md)
- 12.3 Hipótesis nula, hipótesis alternativa y errores (60 min) — [`12_Estadistica_inferencia/03_hipotesis.md`](02_TEORIA/12_Estadistica_inferencia/03_hipotesis.md)
- 12.4 El p-valor, calculado de verdad (65 min) — [`12_Estadistica_inferencia/04_pvalor.md`](02_TEORIA/12_Estadistica_inferencia/04_pvalor.md)
- 12.5 Comparar dos promedios: la prueba t (Student y Welch) (70 min) — [`12_Estadistica_inferencia/05_prueba_t_welch.md`](02_TEORIA/12_Estadistica_inferencia/05_prueba_t_welch.md)
- 12.6 Relación entre dos categorías: la prueba chi-cuadrado (60 min) — [`12_Estadistica_inferencia/06_chi_cuadrado.md`](02_TEORIA/12_Estadistica_inferencia/06_chi_cuadrado.md)
- 12.7 Tamaño del efecto: significativo no es lo mismo que importante (55 min) — [`12_Estadistica_inferencia/07_tamano_del_efecto.md`](02_TEORIA/12_Estadistica_inferencia/07_tamano_del_efecto.md)
- 12.8 Interpretar, comunicar y no equivocarse (55 min) — [`12_Estadistica_inferencia/08_interpretacion_limitaciones.md`](02_TEORIA/12_Estadistica_inferencia/08_interpretacion_limitaciones.md)

**Capítulo 13 — Modelado dimensional: hechos, dimensiones y modelo estrella**

- 13.1 Hechos, dimensiones y granularidad (55 min) — [`13_Modelado/01_hechos_dimensiones.md`](02_TEORIA/13_Modelado/01_hechos_dimensiones.md)
- 13.2 El modelo estrella: relaciones y varios hechos (60 min) — [`13_Modelado/02_modelo_estrella.md`](02_TEORIA/13_Modelado/02_modelo_estrella.md)
- 13.3 La tabla de fechas (calendario) (45 min) — [`13_Modelado/03_tabla_de_fechas.md`](02_TEORIA/13_Modelado/03_tabla_de_fechas.md)

**Capítulo 14 — Power BI, Power Query y DAX: cargar, modelar, medir y comprobar**

- 14.1 Power BI desde cero: qué es, el flujo de trabajo y la configuración regional (50 min) — [`14_PowerBI_DAX/01_power_bi_desde_cero.md`](02_TEORIA/14_PowerBI_DAX/01_power_bi_desde_cero.md)
- 14.2 Power Query y el lenguaje M (55 min) — [`14_PowerBI_DAX/02_power_query.md`](02_TEORIA/14_PowerBI_DAX/02_power_query.md)
- 14.3 DAX: medidas y contexto de filtro (70 min) — [`14_PowerBI_DAX/03_dax_contexto.md`](02_TEORIA/14_PowerBI_DAX/03_dax_contexto.md)
- 14.4 Medidas útiles de un tablero comercial y cómo controlarlas (65 min) — [`14_PowerBI_DAX/04_medidas_utiles.md`](02_TEORIA/14_PowerBI_DAX/04_medidas_utiles.md)
- 14.5 Diseño del tablero y lista de comprobación manual (45 min) — [`14_PowerBI_DAX/05_diseno_y_comprobacion.md`](02_TEORIA/14_PowerBI_DAX/05_diseno_y_comprobacion.md)

**Capítulo 15 — Excel como segundo camino de validación**

- 15.1 Excel desde cero: datos limpios, tablas y la configuración regional (45 min) — [`15_Excel_cuadres/01_excel_desde_cero.md`](02_TEORIA/15_Excel_cuadres/01_excel_desde_cero.md)
- 15.2 Funciones de Excel para cuadrar: condiciones, sumas y búsquedas (60 min) — [`15_Excel_cuadres/02_funciones_para_cuadrar.md`](02_TEORIA/15_Excel_cuadres/02_funciones_para_cuadrar.md)
- 15.3 Tablas dinámicas, estadística en Excel y el cuadre entre herramientas (65 min) — [`15_Excel_cuadres/03_tablas_dinamicas_cuadre.md`](02_TEORIA/15_Excel_cuadres/03_tablas_dinamicas_cuadre.md)

**Capítulo 16 — Documentar y comunicar trabajo real: Git, README y empleo honesto**

- 16.1 Git desde cero: guardar versiones de tu trabajo (50 min) — [`16_Git_comunicacion/01_git_desde_cero.md`](02_TEORIA/16_Git_comunicacion/01_git_desde_cero.md)
- 16.2 Documentar y explicar tu trabajo: README, errores y decisiones (45 min) — [`16_Git_comunicacion/02_documentar_y_explicar.md`](02_TEORIA/16_Git_comunicacion/02_documentar_y_explicar.md)
- 16.3 Portafolio y búsqueda de empleo honesta desde la primera semana (45 min) — [`16_Git_comunicacion/03_portafolio_y_empleo.md`](02_TEORIA/16_Git_comunicacion/03_portafolio_y_empleo.md)

**Capítulo 17 — Transferencia y autonomía: resolver datos que cambian**

- 17.1 Los ocho pasos frente a un caso nuevo (70 min) — [`17_Transferencia_debug/01_ocho_pasos_caso_nuevo.md`](02_TEORIA/17_Transferencia_debug/01_ocho_pasos_caso_nuevo.md)
- 17.2 Cuando no cuadra: reducir el problema hasta encontrar el primer desvío (60 min) — [`17_Transferencia_debug/02_cuando_no_cuadra.md`](02_TEORIA/17_Transferencia_debug/02_cuando_no_cuadra.md)
- 17.3 Resolver sin ayuda externa: método, evidencia y honestidad (45 min) — [`17_Transferencia_debug/03_resolver_sin_ia.md`](02_TEORIA/17_Transferencia_debug/03_resolver_sin_ia.md)

**Capítulo 18 — Preparación técnica y conductual para entrevistas**

- 18.1 Cómo responder una pregunta técnica en cuatro pasos (50 min) — [`18_Entrevistas/01_responder_pregunta_tecnica.md`](02_TEORIA/18_Entrevistas/01_responder_pregunta_tecnica.md)
- 18.2 Banco de preguntas frecuentes y respuestas modelo (60 min) — [`18_Entrevistas/02_banco_de_preguntas.md`](02_TEORIA/18_Entrevistas/02_banco_de_preguntas.md)
- 18.3 Preguntas de comportamiento, apoyo de IA y honestidad (45 min) — [`18_Entrevistas/03_conductuales_y_honestidad.md`](02_TEORIA/18_Entrevistas/03_conductuales_y_honestidad.md)


## 4. Ejemplos ejecutados

- **Cómo:** `python herramientas/verificar_teoria.py`. SQL: cada bloque se ejecuta sobre una copia en memoria de `mini_base.db`. Python: en una carpeta temporal con una copia de `mini_base`, de modo que las lecciones que escriben archivos (CSV, JSON, SQLite, módulos) no tocan el paquete.
- **Cuántos:** 620 bloques (159 SQL y 461 Python), todos sin fallo; 23 bloques muestran un error esperado (`error`) y la herramienta comprueba que ese error realmente ocurre y que su última línea coincide.
- **Entorno:** Python 3.12.10, SQLite 3.49.1, pandas 2.2.3, numpy 2.3.5, scipy 1.17.0, matplotlib 3.10.8, Git 2.45.1 (Windows 11). **No se agregó ninguna dependencia nueva** (todo está en `requirements.txt` o en la biblioteca estándar).
- Los bloques con `salida`/`resultado` se **rellenan** con `--rellenar` y luego se revisaron a mano contra el texto de la lección; no se escribieron resultados "de memoria".

## 5. Resultados verificados

1. **Todas las cifras numéricas del texto** se compararon con la salida real. Al hacerlo se corrigieron afirmaciones propias que no coincidían; algunos ejemplos: en 1.3 la micropráctica anunciaba 4 líneas y eran 6; en 2.4 la tienda 5 pasaba de 20 a 17 caracteres y no de 21 a 18; en 3.2 el control por zonas era 7 + 6 + 1 + 1 + 1; en 4.1–4.3 varios recuentos de la micropráctica; en 6.3 el drop size es 23,07 unidades y no 24,7; en 9.1 la desviación con `ddof=0` es 43,8; en 11.9 la desviación es 36,75 y no 48,7; en 12.4 la diferencia con el grupo A modificado es 9,5 y no 9; en 17.2 el síntoma era 900 Bs y no 120. Un error de redacción propio (un texto de error inventado en 7.7) también se detectó y se corrigió con el mensaje real.
2. **Cálculos manuales** (estadística y KPI) recalculados con Python: media 24, mediana 21, desviaciones 11,73 y 12,36, Q1 15,75 y Q3 27,25, `r` = 0,920, intervalo de confianza 105,88–122,45, p exacto por permutación 4/70 = 0,0571 frente al de Welch 0,0452, `χ²` = 5,769 (p = 0,0163), `d` de Cohen 1,82 y V de Cramér 0,24.
3. **Trampas que las lecciones demuestran con código:** `NOT IN` con NULL devuelve 0 filas; `groupby` pierde 2 de 12 tiendas con clave vacía; un `merge` sin `validate` pasa de 150 a 200 Bs; la meta se multiplica por 4 al unir por una clave repetida; `np.std` usa `n` y `pandas.std` usa `n − 1`; `round(2.5)` es 2; la corrección de Yates cambia `χ²` de 5,769 a 4,848.
4. **Cobertura de los punteros de los ejercicios:** se revisó cada puntero «capítulo N, tema» de P01–P30, ST07, ME y DB. Los temas que faltaban se añadieron a la teoría (`Decimal`, `removeprefix`, comparación de fechas ISO como texto, texto vacío con `eq("")`, `mkdir`); el único puntero que ya no existe está en §6.
5. **Definición previa de términos:** la herramienta comprueba que la primera lección que usa cada uno de 43 términos controlados (variable, mutable, secuencia, iteración, acumulador, argumento, parámetro, retorno, granularidad, cardinalidad, DataFrame, varianza, hipótesis nula, contexto de filtro, etc.) lo define en negrita. Resultado: sin violaciones.

## 6. Pendientes de sincronización con las guías (para la Etapa 2)

1. **Carga total de la teoría.** 5 465 min (≈ 91 h) en lecciones + 75 min del capítulo 19. El plan tiene 6 semanas (≈ 90 h con 15 h/semana, incluyendo todos los ejercicios). Hay que decidir la **ruta mínima** por modalidad (BASE 15 h, EXTENDIDA 20–25 h) y marcar el resto como ampliación o consulta. La columna «Tipo» de las tablas de capítulo dice «núcleo» en todas porque esa decisión es de la Etapa 2.
2. **Las guías enlazan capítulos, no lecciones.** `nucleo.json` usa solo archivos de capítulo en `teoria`. Hay que asignar a cada día las lecciones concretas.
3. **Orden de los capítulos 5 y 6.** Se estudian mejor después del 10 (sus ejemplos usan Pandas), aunque su número sea menor; el calendario actual puede tenerlos antes.
4. **Punteros de ejercicios a revisar:** P02 cita «capítulo 08, ejemplo de cumplimiento», que ya no existe (el concepto, comprobar el denominador antes de dividir, está en 7.10 y 8.1); P07 cita «sumar solo entregados» (el patrón está en 7.12–7.13 con otra condición). No se modificaron los ejercicios.
5. **`INFORME_CORRECCION_PEDAGOGICA_V5.md`** menciona la sección «Funciones que usarás desde G4» del capítulo 2; ahora son las lecciones 2.4 y 2.5.
6. **Las guías de D03 en adelante deben revisar sus «Antes de empezar»** con los nuevos prerrequisitos (cada lección declara los suyos).
7. **Los tiempos de las lecciones son estimaciones** (lectura + comprensión + práctica + depuración para un principiante); no se midieron con un estudiante real. La Etapa 2 debe contrastarlos con la carga de `CARGA_ESTIMADA.md`.
8. **Hallazgo previo a esta etapa (corregido en la herramienta, no en el contenido):** `auditar_enunciados.py` fallaba en S1 y S10 porque solo reconocía criterios con `- [ ]` y la estudiante marcó `- [x]` al terminar D01. Se corrigió el auditor para aceptar ambas formas; los enunciados no se tocaron.
9. **`10_VALIDACION/resultados_pruebas.json`** conserva las evidencias de la Fase 1; la prueba «Ejemplos Python de los apuntes» de `verificar_paquete.py` ahora ejecuta toda la verificación de la teoría. Conviene regenerar esa evidencia al cerrar la Etapa 3.

## 7. Archivos modificados y creados

**Modificados (24):** los 19 archivos de capítulo `02_TEORIA/01_…md` a `19_…md`; `02_TEORIA/GLOSARIO.md`; `02_TEORIA/FUENTES.md`; `README.md` (filas de `02_TEORIA` y `04_DATASETS` y mención de la nueva herramienta); `herramientas/verificar_paquete.py` (la prueba de los apuntes ahora llama a `verificar_teoria.py`); `herramientas/auditar_enunciados.py` (acepta criterios marcados).

**Creados:** `02_TEORIA/INDICE.md`; 18 carpetas con 100 lecciones (`02_TEORIA/NN_nombre/`); `04_DATASETS/mini_base/` (`mini_base.sql`, `mini_base.db`, 7 CSV, `README.md`); `herramientas/crear_mini_base.py`; `herramientas/verificar_teoria.py`; `PROGRESO_FASE2.md`; este informe. El manifiesto `10_VALIDACION/MANIFIESTO_SHA256.json` se regeneró al final.

**No modificados:** `mi_trabajo/`, `01_PLAN_DIARIO/` (D01, D02 y el resto), `03_EJERCICIOS/`, `08_SOLUCIONES/`, `09_EVALUACION_FINAL/`, datasets existentes, `nucleo.json`, `CARGA_ESTIMADA.md`.

## 8. Pruebas ejecutadas

| Prueba | Resultado |
|---|---|
| `verificar_teoria.py` (620 bloques; formato; enlaces; tiempos; términos; glosario; fugas) | OK |
| Pruebas de mutación del propio verificador, en una copia temporal: salida alterada; valor de ejercicio publicado; enlace roto; término sin definir; tiempo incoherente; glosario que enlaza la lección equivocada; apartado obligatorio ausente | **7 de 7 detectadas**, cada una en el grupo de comprobación esperado |
| `auditar_enunciados.py` | 6 grupos OK (tras el arreglo del auditor) |
| `verificar_paquete.py` sobre una **copia temporal** del repositorio (sin `.venv`, sin `.git`, sin `mi_trabajo`; manifiesto regenerado en la copia) | **20 de 20 OK, 0 fallos** |
| `prueba_sqlite_cierre.py` (incluida dentro de la anterior) | OK |
| Determinismo: dos ejecuciones consecutivas de `verificar_teoria.py` | mismas salidas |
| Versión: todos los ejemplos corren en Python 3.12.10 | OK |

Antes del arreglo del auditor, `verificar_paquete.py` en la copia daba 19 de 20 (fallaba solo la comprobación de enunciados por las casillas marcadas de S1 y S10; ver §6.8).

## 9. Limitaciones

- **No se ejecutó nada en Power BI Desktop, Excel ni SQL Server.** El código DAX, el código M, las fórmulas de Excel, los pasos de interfaz y los ejemplos de `TOP`/`DATEDIFF` son referencia; sus cifras de control sí están calculadas con Python. Cada lección lo declara.
- Algunas salidas dependen del entorno: rutas con `\` en Windows (8.3), el texto de `EXPLAIN QUERY PLAN` (SQLite 3.49.1), los mensajes de error de Python 3.12 y las muestras aleatorias con semilla (`random` y `pandas.sample`). Con otras versiones pueden variar.
- **Los tiempos son estimaciones**, no mediciones con un estudiante.
- **No se verificó en línea la disponibilidad de los enlaces externos** de `FUENTES.md`.
- No hubo revisión por una persona experta en pedagogía ni lectura por un principiante real; la calidad del texto se verificó con las comprobaciones automáticas y con una revisión propia lección por lección.
- El glosario curado tiene ≈ 100 términos; las lecciones definen 741 en total (cada lección enumera los suyos).
- La mini-base es pequeña a propósito; no sirve para ilustrar rendimiento ni distribuciones grandes.
- La estadística usa conjuntos pequeños para poder calcular a mano; las conclusiones son pedagógicas, no inferencias reales.

## 10. Preparación para la Etapa 2

Listo para iniciar cuando lo autorices:

- Teoría completa, verificada y navegable (`02_TEORIA/INDICE.md`); cada lección declara tiempo, prerrequisitos y ejercicios que prepara.
- Inventario de ejercicios y de punteros: ver §6.
- Datos para decidir la ruta mínima: tiempos por lección en las tablas de cada capítulo.
- Herramienta de verificación: `python herramientas/verificar_teoria.py` (y `verificar_paquete.py`).
- Restricciones vigentes registradas en `PROGRESO_FASE2.md`.

Pregunta formal: **¿Autorizas comenzar la Etapa 2: integración pedagógica, calendario y modalidades de estudio?**
