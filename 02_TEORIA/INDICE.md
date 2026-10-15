# Índice de la teoría

La teoría del curso son **19 capítulos**. Cada capítulo tiene un archivo de entrada (por ejemplo, `07_Python_basico.md`) con su resumen, el orden de lectura, el tiempo y los ejercicios que prepara; y, en una carpeta del mismo nombre, las **lecciones** (100 en total, más el capítulo 19, que es un archivo único). Todas las lecciones siguen el mismo esquema: *para qué sirve → términos nuevos → ejemplo paso a paso → errores comunes → preguntas de comprobación → micropráctica → ejercicios autónomos*.

## Cómo usar este material

1. Lee la lección con el ejemplo **a la vista y escríbelo tú**: predice el resultado antes de ejecutarlo.
2. Haz la micropráctica **sin mirar** la comprobación. Es **práctica guiada**, sin corrector. Dos checkpoints sí son OBLIGATORIOS: PD-BASE en 10.1 y PD-AGR en 10.2 (10 min cada uno, contados una sola vez en la guía); sus demás minutos son REFUERZO. Los otros ejercicios evaluables están en [`03_EJERCICIOS/`](../03_EJERCICIOS/) (SQL, Python, estadística, mini-ETL, depuración y casos).
3. Cuando un ejercicio te bloquee, vuelve a la lección enlazada en su enunciado y usa el método de la 8.7 y la 17.2.
4. Los ejemplos usan datos de la **mini-base inventada** o tablas de papel y valores independientes identificados en cada sección ([`04_DATASETS/mini_base/`](../04_DATASETS/mini_base/README.md)), distinta de los datos de los ejercicios, para que ningún ejemplo coincida con la respuesta de un ejercicio.

## Capítulos, en orden numérico

| Cap. | Tema | Lecciones | Tiempo de primera vez | Se apoya en | Ejercicios que prepara |
|---|---|---|---|---|---|
| [1](01_SQL_basico.md) | SQL desde cero | 7 | 5 h 21 min | — | S1–S10 |
| [2](02_SQL_agregados.md) | Agregar sin perder el significado | 5 | 4 h 20 min | 1 | G1–G8, N2 |
| [3](03_SQL_joins.md) | JOIN y duplicación | 4 | 3 h 35 min | 1–2 | J1–J6, E1–E8, N8, N9 |
| [4](04_SQL_CTE_ventanas.md) | Subconsultas, CTE, ventanas, índices | 4 | 3 h 35 min | 1–3 | K, V, X, N5–N7, N13, N15 |
| [5](05_calidad_ETL.md) | Calidad de datos y ETL | 5 | 4 h 35 min | 8–10 | proyecto ETL, P21–P30, C04, C06 |
| [6](06_KPIs.md) | KPIs empresariales | 6 | 5 h 46 min | 1–4 (y 9–10 para los ejemplos en Python) | J2, J4, K1, N1–N5, N7, N9–N12, V1–V4 |
| [7](07_Python_basico.md) | Python desde cero | 13 | 12 h 22 min | — | P01–P08 |
| [8](08_Python_funciones_archivos.md) | Funciones, archivos, errores | 7 | 6 h 10 min | 7 | P09–P16, P29–P30 |
| [9](09_Pandas_basico.md) | NumPy y Pandas básico | 6 | 5 h 35 min | 7–8 | P17–P20, N01 |
| [10](10_Pandas_transformaciones.md) | Pandas: transformar, unir, validar | 6 | 6 h 5 min | 9 | P21–P28, N02, N03 |
| [11](11_Estadistica_descriptiva.md) | Estadística descriptiva | 9 | 8 h 35 min | 9 | ST01–ST04, N04, C03 |
| [12](12_Estadistica_inferencia.md) | Estadística inferencial | 8 | 8 h 5 min | 11 | ST05–ST07, N05 |
| [13](13_Modelado.md) | Modelado dimensional | 3 | 2 h 45 min | 3, 10 | proyecto Power BI |
| [14](14_PowerBI_DAX.md) | Power BI, Power Query y DAX | 5 | 4 h 49 min | 10, 13 | proyecto Power BI |
| [15](15_Excel_cuadres.md) | Excel como segundo camino | 3 | 2 h 50 min | 2–3, 6 | EX01–EX03 |
| [16](16_Git_comunicacion.md) | Git, documentación, empleo honesto | 3 | 2 h 20 min | 7 | proyecto SQL, README, CV |
| [17](17_Transferencia_debug.md) | Transferencia y autonomía | 3 | 2 h 55 min | 5, 8, 10 | C06, evaluación final |
| [18](18_Entrevistas.md) | Entrevistas | 3 | 2 h 35 min | 1–5 | simulacros |
| [19](19_Puente_Python_a_ETL.md) | Puente: de funciones a un ETL | (archivo único) | 1 h 15 min | 7–8 | ME01–ME04, DB01–DB03 |

**Total de lecciones:** 100 más el capítulo 19. **Tiempo total estimado de primera vez** (lectura, ejemplos y microprácticas, sin los ejercicios autónomos): 5 538 min ≈ **92,3 h** más el capítulo 19. Los checkpoints BASE son parte de esa práctica, no contenido adicional contado dos veces. La teoría incluye ahora los 58 min trasladados desde enunciados (16 de D01 y 42 ya añadidos al plan): cambia su ubicación, no la estimación BASE de 5.813 min. Las guías enlazan los apartados y descuentan su lectura del desarrollo restante.

> **Ruta de estudio.** Ese tiempo es la suma de todas las lecciones y no cabe en las seis semanas junto con los ejercicios. Por eso cada lección está clasificada una a una (columna «Tipo» de cada capítulo): **núcleo** (indispensable para los fundamentos; tiene día asignado en la ruta BASE de 15 h semanales), **refuerzo** (se lee cuando la competencia no está dominada) y **profundización** (EXTENDIDA u otros periodos). **Todas siguen disponibles como material de consulta.** La tabla completa, las horas por semana y la revisión de prerrequisitos están en [`01_PLAN_DIARIO/RUTAS.md`](../01_PLAN_DIARIO/RUTAS.md); la fuente de la clasificación es [`01_PLAN_DIARIO/lecciones.json`](../01_PLAN_DIARIO/lecciones.json).

## Dependencias entre capítulos que no siguen el orden numérico

- Los capítulos **5** (ETL) y **6** (KPIs) tienen ejemplos en Pandas: se estudian mejor **después** del 10, aunque su número sea menor. Sus ideas (contrato de datos, fichas de KPI) pueden leerse antes; los ejemplos en Python se recomiendan cuando ya sepas Pandas.
  - **Orden en la ruta BASE:** 9.2 se lee en D12, después de los archivos CSV de D10; P17/9.3 en D15. En D16, 10.1 precede a 9.5 y PD-BASE demuestra filtros, tipos y columnas; en D17 PD-AGR demuestra agrupación antes de P21. El capítulo 5 (5.2 y 5.3) se lee en D23–D24 junto a ME02–ME03. En el capítulo 6, 6.1 se lee en D12 con sus ejemplos de **SQL** (los de Python se retoman desde D16), 6.5 en D19, 6.2 en D25, 6.4 en D31 y 6.6 en D39. La lección 6.3 es refuerzo.
- El capítulo **9** usa `statistics` y NumPy para verificar; la lección 9.1 define lo mínimo de desviación estándar sin exigir el capítulo 11.
- El capítulo **19** es un puente corto que se lee junto a ME01–ME04 y DB01–DB03; sus §1–§4 son lo que las guías y los ejercicios citan.

## Buscar por tema

| Si necesitas… | Ve a… |
|---|---|
| leer un error de Python | [8.6](08_Python_funciones_archivos/06_leer_tracebacks.md), [19 §1](19_Puente_Python_a_ETL.md) |
| que un total deje de multiplicarse al unir tablas | [3.4](03_SQL_joins/04_duplicacion_por_join.md), [10.3](10_Pandas_transformaciones/03_merge_cardinalidad.md) |
| un porcentaje o un promedio correcto | [2.3](02_SQL_agregados/03_granularidad_denominadores.md), [6.2](06_KPIs/02_cumplimiento_cobertura_efectividad.md) |
| tratar vacíos y duplicados | [1.4](01_SQL_basico/04_null.md), [9.5](09_Pandas_basico/05_nulos_duplicados.md), [5.3](05_calidad_ETL/03_rechazos_y_reconciliacion.md) |
| convertir fechas y montos | [9.6](09_Pandas_basico/06_tipos_textos_fechas.md), [7.7](07_Python_basico/07_conversiones.md), [8.4](08_Python_funciones_archivos/04_modulos_imports.md) |
| una media, una desviación o un percentil | [11.3](11_Estadistica_descriptiva/03_media_mediana_moda.md), [11.4](11_Estadistica_descriptiva/04_dispersion.md), [11.5](11_Estadistica_descriptiva/05_percentiles_atipicos.md) |
| entender un p-valor | [12.4](12_Estadistica_inferencia/04_pvalor.md) |
| comparar dos grupos | [12.5](12_Estadistica_inferencia/05_prueba_t_welch.md), [12.6](12_Estadistica_inferencia/06_chi_cuadrado.md), [12.7](12_Estadistica_inferencia/07_tamano_del_efecto.md) |
| diseñar un ETL | [5.2](05_calidad_ETL/02_contrato_de_datos.md), [5.5](05_calidad_ETL/05_estructura_etl_funciones.md), [17.1](17_Transferencia_debug/01_ocho_pasos_caso_nuevo.md) |
| un total que no cuadra | [17.2](17_Transferencia_debug/02_cuando_no_cuadra.md), [15.3](15_Excel_cuadres/03_tablas_dinamicas_cuadre.md) |
| modelo estrella y calendario | [13.2](13_Modelado/02_modelo_estrella.md), [13.3](13_Modelado/03_tabla_de_fechas.md) |
| medidas DAX | [14.3](14_PowerBI_DAX/03_dax_contexto.md), [14.4](14_PowerBI_DAX/04_medidas_utiles.md) |
| Git y README | [16.1](16_Git_comunicacion/01_git_desde_cero.md), [16.2](16_Git_comunicacion/02_documentar_y_explicar.md) |
| prepararte para una entrevista | [18.1](18_Entrevistas/01_responder_pregunta_tecnica.md), [18.3](18_Entrevistas/03_conductuales_y_honestidad.md) |

## Verificación automática de la teoría

Desde la raíz del paquete:

```
python herramientas/verificar_teoria.py
```

Ejecuta cada ejemplo SQL y Python de las lecciones y compara con la salida mostrada; revisa el formato de las lecciones, los enlaces internos, la coherencia de los tiempos con la tabla de cada capítulo, que los términos se definan antes de usarse, que el glosario enlace a la lección donde se define cada término y que ningún ejemplo coincida con una solución o con un resultado publicado de los ejercicios. `--rellenar` reescribe los bloques de salida con lo que realmente imprime el código (úsalo al editar una lección y revisa el cambio). La mini-base se regenera con `python herramientas/crear_mini_base.py`.

También: [Glosario](GLOSARIO.md) · [Fuentes y versiones](FUENTES.md) · [Material de la UAGRM](UAGRM/LEEME.md).
