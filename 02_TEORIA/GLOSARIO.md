# Glosario

Los términos clave del curso, en orden alfabético, con una definición breve y la lección donde se **define y se explica con ejemplo**. Cada término está en negrita en la lección enlazada (`herramientas/verificar_teoria.py` lo comprueba). Para ver todos los términos de un capítulo, abre su lista «Términos nuevos» en cada lección.

Notación: las lecciones se citan como *capítulo.lección* (por ejemplo, 7.4 es la cuarta lección del capítulo 7).

## A

- **ABC (clasificación)** — separar elementos en clases A, B y C según su aporte acumulado; requiere declarar la convención de borde. [6.5](06_KPIs/05_abc_pareto_rotacion.md)
- **Acumulador** — variable que se crea antes de un bucle y se actualiza en cada iteración para ir construyendo un resultado. [7.12](07_Python_basico/12_acumuladores.md)
- **Alias (SQL)** — nombre nuevo y temporal para una columna o tabla dentro de una consulta. [1.2](01_SQL_basico/02_select_from_alias.md)
- **Alias (lista)** — dos nombres que apuntan a la misma lista; cambiar una cambia la otra. [7.8](07_Python_basico/08_listas_tuplas.md)
- **Anti-join** — patrón `LEFT JOIN … IS NULL` para hallar las filas de la izquierda sin pareja. [3.3](03_SQL_joins/03_left_join_ausentes.md)
- **Argumento** — el dato que se entrega a una función al llamarla. [7.1](07_Python_basico/01_que_es_un_programa.md)
- **Arreglo** — secuencia de números del mismo tipo de NumPy sobre la que se opera de una vez. [9.1](09_Pandas_basico/01_numpy_arrays.md)
- **Asignación** — instrucción que le da un valor a un nombre (`=`). [7.2](07_Python_basico/02_variables_asignacion.md)
- **Autonomía** — capacidad de construir y defender una solución sin que otro escriba el código por ti. [17.3](17_Transferencia_debug/03_resolver_sin_ia.md)

## B

- **Base cero** — referencia igual a 0: la variación relativa no está definida. [6.4](06_KPIs/04_productividad_variaciones.md)
- **Bronze** — capa del dato tal como llegó, sin cambios. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **Bucle** — estructura que repite un bloque de instrucciones. [7.11](07_Python_basico/11_for_while.md)

## C

- **Cardinalidad** — cuántas filas de una tabla corresponden a una fila de otra (1:1, 1:N, N:M). [3.1](03_SQL_joins/01_claves_relaciones.md)
- **Carga atómica** — carga que se publica entera o no se publica (archivo temporal y reemplazo). [5.4](05_calidad_ETL/04_cargas_registro_reproducibilidad.md)
- **CASE** — expresión SQL que devuelve un valor según condiciones evaluadas en orden. [2.5](02_SQL_agregados/05_case_coalesce.md)
- **Censo** — observar a toda la población, no a una parte. [11.1](11_Estadistica_descriptiva/01_poblacion_muestra_variables.md)
- **Centavos enteros** — representar el dinero como enteros para que las sumas sean exactas. [5.3](05_calidad_ETL/03_rechazos_y_reconciliacion.md)
- **Clave foránea** — columna que guarda la clave primaria de otra tabla. [3.1](03_SQL_joins/01_claves_relaciones.md)
- **Clave huérfana** — clave foránea sin fila correspondiente en la otra tabla. [3.1](03_SQL_joins/01_claves_relaciones.md)
- **Clave primaria** — columna cuyo valor identifica una fila y no se repite. [1.1](01_SQL_basico/01_tablas_filas_columnas.md)
- **COALESCE** — devuelve el primer valor no NULL de una lista. [2.5](02_SQL_agregados/05_case_coalesce.md)
- **Comparaciones múltiples** — muchas pruebas sobre los mismos datos; aumentan el riesgo de falsas alarmas. [12.8](12_Estadistica_inferencia/08_interpretacion_limitaciones.md)
- **Contexto de filtro** — conjunto de filtros activos cuando DAX evalúa una medida. [14.3](14_PowerBI_DAX/03_dax_contexto.md)
- **Contrato de datos** — descripción escrita de lo que debe cumplir un archivo: columnas, tipos, claves, formatos y qué hacer con lo inválido. [5.2](05_calidad_ETL/02_contrato_de_datos.md)
- **Cuadre** — igualdad que el resultado debe cumplir (filas, totales). [5.2](05_calidad_ETL/02_contrato_de_datos.md)
- **Correlación (coeficiente de)** — medida entre −1 y +1 de la relación lineal entre dos variables; no implica causa. [11.7](11_Estadistica_descriptiva/07_correlacion_causalidad.md)
- **CTE** — resultado con nombre definido con `WITH`, que existe solo durante la consulta. [4.2](04_SQL_CTE_ventanas/02_cte.md)
- **Cumplimiento de presupuesto** — ventas reales / meta × 100, a la granularidad de la meta. [6.2](06_KPIs/02_cumplimiento_cobertura_efectividad.md)

## D

- **DataFrame** — tabla de columnas con índice, el objeto central de Pandas. [9.2](09_Pandas_basico/02_series_dataframe_csv.md)
- **Desviación estándar** — raíz cuadrada de la varianza; dispersión en las unidades de los datos. [11.4](11_Estadistica_descriptiva/04_dispersion.md)
- **Diccionario** — colección de pares clave → valor. [7.9](07_Python_basico/09_diccionarios_sets.md)
- **Dimensión (tabla de)** — tabla que describe el contexto de los hechos, con una fila y una clave única por elemento. [13.1](13_Modelado/01_hechos_dimensiones.md)
- **Distribución normal** — la «campana» simétrica descrita por su media y desviación. [11.6](11_Estadistica_descriptiva/06_distribuciones_histograma_z.md)
- **Drop size** — tamaño de una entrega, en Bs o unidades. [6.3](06_KPIs/03_ticket_frecuencia_activos.md)
- **Duplicado exacto** — fila idéntica a otra en todos los campos. [5.3](05_calidad_ETL/03_rechazos_y_reconciliacion.md)

## E

- **ELT** — cargar primero los datos crudos y transformarlos dentro del destino. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **Error estándar** — desviación estándar de un estadístico entre muestras; para la media, `s / √n`. [12.1](12_Estadistica_inferencia/01_por_que_inferencia.md)
- **Error tipo I** — rechazar `H0` cuando era cierta (falsa alarma). [12.3](12_Estadistica_inferencia/03_hipotesis.md)
- **Error tipo II** — no rechazar `H0` cuando era falsa. [12.3](12_Estadistica_inferencia/03_hipotesis.md)
- **Estadístico** — cifra calculada con una muestra. [11.1](11_Estadistica_descriptiva/01_poblacion_muestra_variables.md)
- **ETL** — extraer, transformar y cargar. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **Excepción** — error que Python detecta al ejecutar y que detiene el programa si nadie lo atiende. [7.7](07_Python_basico/07_conversiones.md)

## F

- **f-string** — texto con `f` antes de las comillas que incrusta valores entre llaves. [7.5](07_Python_basico/05_texto.md)
- **Fecha de corte** — fecha fija contra la que se mide un indicador. [2.4](02_SQL_agregados/04_redondeo_texto_fechas.md)
- **Ficha del KPI** — definición escrita de un indicador: población, período, unidad, fórmula, exclusiones y criterio de acción. [6.1](06_KPIs/01_que_es_un_kpi.md)
- **Función** — bloque de instrucciones con nombre que realiza una tarea. [7.1](07_Python_basico/01_que_es_un_programa.md)
- **Función de ventana** — función que calcula sobre filas relacionadas sin colapsarlas (`OVER`). [4.3](04_SQL_CTE_ventanas/03_ventanas.md)
- **Función pura** — función que solo depende de sus parámetros y solo devuelve un valor. [8.1](08_Python_funciones_archivos/01_funciones_con_contrato.md)

## G

- **Git** — programa que registra versiones de los archivos de una carpeta. [16.1](16_Git_comunicacion/01_git_desde_cero.md)
- **Gold** — capa de resúmenes listos para el negocio. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **Granularidad** — qué representa exactamente una fila de una tabla. [1.1](01_SQL_basico/01_tablas_filas_columnas.md)
- **GROUP BY** — cláusula que forma grupos y da una fila por grupo. [2.2](02_SQL_agregados/02_group_by_having.md)

## H

- **HAVING** — filtra grupos después de agrupar. [2.2](02_SQL_agregados/02_group_by_having.md)
- **Hipótesis nula** — afirmación de «no hay efecto» que se intenta refutar. [12.3](12_Estadistica_inferencia/03_hipotesis.md)

## I

- **Idempotencia** — ejecutar una operación varias veces deja el mismo resultado que ejecutarla una vez. [5.4](05_calidad_ETL/04_cargas_registro_reproducibilidad.md)
- **Índice (Python)** — número de posición de un elemento en una secuencia; empieza en 0. [7.5](07_Python_basico/05_texto.md)
- **Índice (base de datos)** — estructura auxiliar que acelera búsquedas por una columna. [4.4](04_SQL_CTE_ventanas/04_sql_kpis_fechas_rendimiento.md)
- **Inmutable** — que no se puede modificar después de creado (texto, tupla). [7.5](07_Python_basico/05_texto.md)
- **Intervalo de confianza** — rango de valores plausibles para un parámetro, construido con un método con nivel de confianza fijo. [12.2](12_Estadistica_inferencia/02_estimacion_intervalo_confianza.md)
- **Iteración** — cada vuelta de un bucle. [7.11](07_Python_basico/11_for_while.md)

## J – K

- **JOIN** — une dos tablas por coincidencia de una condición. [3.2](03_SQL_joins/02_inner_join.md)
- **KPI** — métrica elegida para seguir un objetivo y orientar una decisión. [6.1](06_KPIs/01_que_es_un_kpi.md)

## L

- **LEFT JOIN** — conserva todas las filas de la tabla izquierda aunque no tengan pareja. [3.3](03_SQL_joins/03_left_join_ausentes.md)
- **LIKE** — operador SQL que compara texto con un patrón (`%`, `_`). [1.6](01_SQL_basico/06_distinct_like.md)
- **Lista** — secuencia ordenada y mutable de elementos. [7.8](07_Python_basico/08_listas_tuplas.md)
- **Lista por comprensión** — forma abreviada de construir una lista nueva a partir de otra. [7.12](07_Python_basico/12_acumuladores.md)

## M

- **Mediana** — valor central de los datos ordenados. [11.3](11_Estadistica_descriptiva/03_media_mediana_moda.md)
- **Medida (DAX)** — fórmula que se calcula al vuelo según el contexto de filtro. [14.3](14_PowerBI_DAX/03_dax_contexto.md)
- **Medida (hecho)** — valor numérico de un evento que se suma o promedia. [13.1](13_Modelado/01_hechos_dimensiones.md)
- **`merge`** — unión de dos DataFrames por una o más claves. [10.3](10_Pandas_transformaciones/03_merge_cardinalidad.md)
- **Modelo estrella** — diseño con tablas de hechos al centro y dimensiones alrededor, con relaciones uno a muchos. [13.2](13_Modelado/02_modelo_estrella.md)
- **Muestra** — subconjunto de la población que realmente se observa. [11.1](11_Estadistica_descriptiva/01_poblacion_muestra_variables.md)
- **Muestreo estratificado** — sorteo dentro de cada grupo (estrato) para asegurar su representación. [11.8](11_Estadistica_descriptiva/08_muestreo.md)
- **Mutable** — que se puede modificar sin crear otro objeto (lista, diccionario). [7.8](07_Python_basico/08_listas_tuplas.md)

## N

- **NULL** — marca de dato desconocido o no registrado; no es cero ni texto vacío. [1.1](01_SQL_basico/01_tablas_filas_columnas.md)
- **Numerador** — la parte de arriba de un cociente. [2.3](02_SQL_agregados/03_granularidad_denominadores.md)
- **NumPy** — biblioteca de cálculo numérico con arreglos. [9.1](09_Pandas_basico/01_numpy_arrays.md)

## O – P

- **ORDER BY** — ordena las filas del resultado. [1.5](01_SQL_basico/05_order_limit.md)
- **Pandas** — biblioteca para trabajar con datos en forma de tabla. [9.2](09_Pandas_basico/02_series_dataframe_csv.md)
- **Parámetro** — nombre de la definición de una función que recibe un dato. [7.4](07_Python_basico/04_primera_funcion.md)
- **Percentil** — valor bajo el cual queda aproximadamente ese porcentaje de los datos. [11.5](11_Estadistica_descriptiva/05_percentiles_atipicos.md)
- **Pipeline** — conjunto de pasos encadenados que lleva los datos del origen al destino. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **Población** — conjunto completo de unidades sobre el que se quiere hablar. [11.1](11_Estadistica_descriptiva/01_poblacion_muestra_variables.md)
- **Power Query** — herramienta de Power BI para obtener y transformar datos. [14.1](14_PowerBI_DAX/01_power_bi_desde_cero.md)
- **p-valor** — probabilidad de un resultado al menos tan extremo como el observado si `H0` fuera cierta. [12.4](12_Estadistica_inferencia/04_pvalor.md)
- **Prueba de Welch** — prueba `t` para dos medias que no supone varianzas iguales. [12.5](12_Estadistica_inferencia/05_prueba_t_welch.md)

## R

- **Recencia** — días desde la última compra hasta la fecha de corte. [6.3](06_KPIs/03_ticket_frecuencia_activos.md)
- **Rechazos** — salida de las filas inválidas con su motivo. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **Reconciliación** — comprobar que filas y valores cuadran entre capas. [10.5](10_Pandas_transformaciones/05_controles_calidad.md)
- **Reproducibilidad** — que otra persona obtenga el mismo resultado con las mismas entradas y versiones. [5.4](05_calidad_ETL/04_cargas_registro_reproducibilidad.md)
- **Retorno** — valor que una función devuelve con `return`. [7.4](07_Python_basico/04_primera_funcion.md)

## S

- **Secuencia** — conjunto ordenado de elementos, cada uno en una posición. [7.5](07_Python_basico/05_texto.md)
- **Segmentador** — control de Power BI que filtra el informe. [14.1](14_PowerBI_DAX/01_power_bi_desde_cero.md)
- **Silver** — capa de datos limpios y validados. [5.1](05_calidad_ETL/01_etl_elt_medallon.md)
- **STAR (método)** — estructura para respuestas conductuales: situación, tarea, acción, resultado. [18.3](18_Entrevistas/03_conductuales_y_honestidad.md)
- **Subconsulta** — consulta SELECT entre paréntesis dentro de otra. [4.1](04_SQL_CTE_ventanas/01_subconsultas.md)

## T

- **Tabla de fechas** — dimensión con una fila por cada día del período, sin huecos. [13.3](13_Modelado/03_tabla_de_fechas.md)
- **Tabla de hechos** — tabla donde cada fila es un evento medible. [13.1](13_Modelado/01_hechos_dimensiones.md)
- **Tabla dinámica** — resumen interactivo de una tabla. [15.3](15_Excel_cuadres/03_tablas_dinamicas_cuadre.md)
- **Tamaño del efecto** — magnitud de una diferencia o asociación, independiente del tamaño de la muestra. [12.7](12_Estadistica_inferencia/07_tamano_del_efecto.md)
- **Ticket medio** — importe total / número de ventas. [6.3](06_KPIs/03_ticket_frecuencia_activos.md)
- **Traceback** — informe que imprime Python cuando una excepción no se atiende. [8.6](08_Python_funciones_archivos/06_leer_tracebacks.md)
- **Tupla** — secuencia ordenada e inmutable. [7.8](07_Python_basico/08_listas_tuplas.md)

## V

- **Variable (programación)** — nombre que apunta a un valor guardado en memoria. [7.2](07_Python_basico/02_variables_asignacion.md)
- **Variable estadística** — característica que se mide en cada unidad (equivale a una columna). [11.1](11_Estadistica_descriptiva/01_poblacion_muestra_variables.md)
- **Variabilidad muestral** — cambio del estadístico de una muestra a otra de la misma población. [12.1](12_Estadistica_inferencia/01_por_que_inferencia.md)
- **Varianza** — promedio de los cuadrados de las desviaciones respecto a la media. [11.4](11_Estadistica_descriptiva/04_dispersion.md)
- **Vectorización** — aplicar una operación a todo un arreglo de una vez. [9.1](09_Pandas_basico/01_numpy_arrays.md)

## Z

- **Puntaje z** — cuántas desviaciones estándar se aleja un dato de la media. [11.6](11_Estadistica_descriptiva/06_distribuciones_histograma_z.md)

Siguiente: [Fuentes](FUENTES.md) · [Índice de la teoría](INDICE.md).
