# Capítulo 11 — Estadística descriptiva: resumir antes de concluir

Este capítulo te enseña a **describir datos** con honestidad: de quién son (población y muestra), de qué tipo son, cuál es su centro, cuánto se dispersan, qué forma tienen, cuáles son atípicos, si dos variables se mueven juntas y cómo escoger una muestra que sirva. Cada medida se calcula **primero a mano** con pocos datos y después con Python y Pandas, y cada lección dice qué puedes y qué no puedes concluir. Todos los datos de los ejemplos son inventados y distintos de los de los ejercicios.

**Tiempo total estimado de primera vez:** unas 8 h 35 min (9 lecciones). Recomendado: una lección por sesión, con la tabla a mano en papel antes de abrir Python.

**Antes de empezar:** leer un CSV con Pandas (capítulo 9) o, como mínimo, las listas de diccionarios de 7.13. El módulo estándar `statistics` y NumPy se usan para verificar lo calculado a mano.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 11.1 | [Población, muestra y tipos de variables](11_Estadistica_descriptiva/01_poblacion_muestra_variables.md) | unidad de análisis, parámetro y estadístico, tipos de variable | NÚCLEO · D09 | 50 min |
| 11.2 | [Frecuencias](11_Estadistica_descriptiva/02_frecuencias.md) | absolutas, relativas, porcentajes, acumuladas, intervalos | NÚCLEO · D11 | 45 min |
| 11.3 | [Media, mediana y moda](11_Estadistica_descriptiva/03_media_mediana_moda.md) | cuándo usar cada una, efecto de los extremos | NÚCLEO · D11 | 55 min |
| 11.4 | [Dispersión](11_Estadistica_descriptiva/04_dispersion.md) | rango, varianza poblacional y muestral, desviación estándar, `n − 1` | NÚCLEO · D18 | 65 min |
| 11.5 | [Percentiles, cuartiles y atípicos](11_Estadistica_descriptiva/05_percentiles_atipicos.md) | IQR, regla de Tukey, métodos de percentil | NÚCLEO · D25 | 65 min |
| 11.6 | [Distribuciones, histogramas y puntaje z](11_Estadistica_descriptiva/06_distribuciones_histograma_z.md) | forma, asimetría, regla 68-95-99,7, z | COMPLEMENTARIA | 65 min |
| 11.7 | [Correlación y causalidad](11_Estadistica_descriptiva/07_correlacion_causalidad.md) | Pearson a mano, confusores, límites | COMPLEMENTARIA | 55 min |
| 11.8 | [Muestreo](11_Estadistica_descriptiva/08_muestreo.md) | aleatorio simple, estratificado, sesgo, tamaño | NÚCLEO · D32 | 55 min |
| 11.9 | [Descriptiva con Pandas y un informe completo](11_Estadistica_descriptiva/09_descriptiva_con_pandas.md) | `describe`, resumen por grupo, trampas, plantilla de informe | COMPLEMENTARIA | 60 min |

## Ideas centrales

- Antes de calcular: **¿de quién son los datos y qué tipo de variable es?**
- Centro y dispersión van **juntos**; con cola larga, la mediana y el IQR cuentan mejor la historia.
- La desviación estándar muestral divide entre `n − 1`; Pandas lo hace por defecto, NumPy no. Escribe cuál usaste.
- Un atípico se **investiga**, no se borra.
- Correlación no es causalidad; una muestra sesgada no se arregla con más datos.
- Todo informe termina con una **limitación**.

## Ejercicios autónomos de este capítulo

ST01–ST04 y el caso C03 en [`03_EJERCICIOS/Estadistica/`](../03_EJERCICIOS/Estadistica/). Entrega para cada uno: la tabla de resultados, el método usado (divisor, método de percentil), un gráfico con título que describa un hallazgo (con unidad, período y recomendación) y una limitación. Las microprácticas de las lecciones no son evaluables. El notebook N04 y la clase UAGRM 2 ([`UAGRM/`](UAGRM/LEEME.md)) complementan este capítulo.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 12 — Estadística inferencial](12_Estadistica_inferencia.md).
