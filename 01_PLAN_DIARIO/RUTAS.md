# Lecciones: clasificación y ruta de estudio

Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json` y `lecciones.json`; no lo edites a mano.

Las 100 lecciones de `02_TEORIA` (los 18 capítulos más el puente del capítulo 19) tienen una sola clase. REFUERZO es una categoría de **ejercicios**, no de lecciones.

| Clase | Significado | Dónde aparece | Lecciones |
|---|---|---|---:|
| **NÚCLEO** | Indispensable: tiene día y minutos en la ruta BASE; toda su teoría se lee antes de los ejercicios de esa jornada | Sección A de cada guía | 87 |
| **COMPLEMENTARIA** | Amplía o consulta; no está programada y ningún ejercicio BASE o REFUERZO la exige por primera vez | Material de consulta | 10 |
| **EMPLEO** | Se lee dentro del bloque de empleo de su jornada | Sección H | 3 |

Una lección puede leerse en partes: «solo la sección inicial» (la parte mínima que necesita un ejercicio), «resto» (el desarrollo) o «completa». Los minutos de cada parte se cuentan una sola vez.

## Ruta NÚCLEO por jornada

| Día | Fecha | Lecciones y partes | Lectura (min) |
|---:|---|---|---:|
| D01 | 2026-10-12 | 7.1, 1.1, 7.2, 1.2 (sec.), 7.4 (sec.) | 66 |
| D02 | 2026-10-13 | 1.2 (resto), 1.3, 1.4, 1.6 (sec.), 7.3, 7.4 (resto), 7.5 (sec.), 7.5 (resto), 7.6, 7.10 (sec.) | 164 |
| D03 | 2026-10-14 | 1.5, 1.6 (resto), 7.8, 7.9 | 70 |
| D04 | 2026-10-15 | 2.1, 2.4 (sec.), 7.10 (resto), 7.11, 7.12 | 94 |
| D05 | 2026-10-16 | 2.2, 2.3, 7.13, 16.1 | 90 |
| D08 | 2026-10-19 | 7.7, 8.1 | 50 |
| D09 | 2026-10-20 | 3.1, 3.2, 8.5, 19.1, 11.1 | 110 |
| D10 | 2026-10-21 | 8.3, 8.4 | 55 |
| D11 | 2026-10-22 | 3.3, 3.4, 2.4 (resto), 11.2, 11.3 | 104 |
| D12 | 2026-10-23 | 6.1, 8.6, 8.7 | 81 |
| D15 | 2026-10-26 | 9.2, 9.3 | 45 |
| D16 | 2026-10-27 | 10.1, 9.5, 6.3 | 72 |
| D17 | 2026-10-28 | 10.2, 10.3, 9.4, 2.5 | 85 |
| D18 | 2026-10-29 | 4.1, 4.2, 4.3, 11.4 | 90 |
| D19 | 2026-10-30 | 6.5, 10.5 | 50 |
| D22 | 2026-11-02 | 5.1, 19.3 | 55 |
| D23 | 2026-11-03 | 5.2, 5.5, 19.2, 9.6 | 90 |
| D24 | 2026-11-04 | 5.3, 19.4, 10.4, 5.4 | 85 |
| D25 | 2026-11-05 | 6.2, 11.5, 6.4 | 75 |
| D26 | 2026-11-06 | 13.1, 10.6 | 50 |
| D29 | 2026-11-09 | 13.2 | 30 |
| D30 | 2026-11-10 | 14.1, 15.1 | 59 |
| D31 | 2026-11-11 | 15.2, 15.3, 14.2 | 80 |
| D32 | 2026-11-12 | 13.3, 11.8 | 45 |
| D33 | 2026-11-13 | 14.3, 14.4, 14.5 (sec.) | 77 |
| D36 | 2026-11-16 | 17.1, 12.1 | 55 |
| D37 | 2026-11-17 | 12.2, 12.3 | 60 |
| D38 | 2026-11-18 | 17.2, 6.6, 12.4 | 80 |
| D39 | 2026-11-19 | 12.5, 12.8 | 60 |
| D40 | 2026-11-20 | 16.2, 18.1 | 50 |

## Todas las lecciones

| Lección | Título | Clase | Jornada(s) | Lectura (min) | Micropráctica |
|---|---|---|---|---:|---|
| 1.1 | 1.1 Tablas, filas, columnas y tipos de datos | NÚCLEO | D01 | 20 | — |
| 1.2 | 1.2 SELECT, FROM, alias y columnas calculadas | NÚCLEO | D01 (sec.), D02 (resto) | 23 | — |
| 1.3 | 1.3 WHERE: filtrar filas con operadores | NÚCLEO | D02 | 26 | — |
| 1.4 | 1.4 NULL: cuando falta el dato | NÚCLEO | D02 | 15 | — |
| 1.5 | 1.5 ORDER BY y LIMIT: ordenar y recortar | NÚCLEO | D03 | 15 | — |
| 1.6 | 1.6 DISTINCT y LIKE: valores únicos y búsquedas por patrón | NÚCLEO | D02 (sec.), D03 (resto) | 22 | — |
| 1.7 | 1.7 Del requerimiento a la consulta: un método de cinco preguntas | COMPLEMENTARIA | — | 15 | — |
| 2.1 | 2.1 Funciones de agregación: contar, sumar, promediar | NÚCLEO | D04 | 20 | obligatorios 3 de 4 |
| 2.2 | 2.2 GROUP BY y HAVING: una cifra por grupo | NÚCLEO | D05 | 20 | obligatorios 3 de 3 |
| 2.3 | 2.3 Granularidad y denominadores: el número correcto para la pregunta correcta | NÚCLEO | D05 | 25 | obligatorios 1, 2, 3 de 3 |
| 2.4 | 2.4 Redondeo, texto y fechas: preparar los datos para el reporte | NÚCLEO | D04 (sec.), D11 (resto) | 20 | obligatorios 1, 2, 3, 4 de 4 |
| 2.5 | 2.5 CASE y COALESCE: condiciones dentro de la consulta y valores faltantes | NÚCLEO | D17 | 20 | obligatorios 1, 3 de 3 |
| 3.1 | 3.1 Claves, relaciones y cardinalidad | NÚCLEO | D09 | 20 | obligatorios 1, 3 de 3 |
| 3.2 | 3.2 INNER JOIN: combinar tablas por coincidencia | NÚCLEO | D09 | 25 | obligatorios 2, 3 de 3 |
| 3.3 | 3.3 LEFT JOIN: conservar todo lo de la izquierda y encontrar a los que no aparecen | NÚCLEO | D11 | 20 | obligatorios 2 de 3 |
| 3.4 | 3.4 Cuando el JOIN duplica: el error silencioso más caro | NÚCLEO | D11 | 25 | obligatorios 1, 2, 3 de 3 |
| 4.1 | 4.1 Subconsultas: una consulta dentro de otra | NÚCLEO | D18 | 20 | obligatorios 1, 3 de 3 |
| 4.2 | 4.2 CTE: dividir una consulta larga en pasos con nombre | NÚCLEO | D18 | 15 | obligatorios 2 de 2 |
| 4.3 | 4.3 Funciones de ventana: calcular sin colapsar las filas | NÚCLEO | D18 | 25 | obligatorios 1, 3 de 3 |
| 4.4 | 4.4 SQL para indicadores: fechas de corte, activos, crecimiento y rendimiento | COMPLEMENTARIA | — | 25 | — |
| 5.1 | 5.1 ETL, ELT y capas Bronze, Silver y Gold | NÚCLEO | D22 | 30 | obligatorios 1, 2 de 3 |
| 5.2 | 5.2 El contrato de datos: escribirlo antes de programar | NÚCLEO | D23 | 25 | obligatorios 1, 3, 4 de 4 |
| 5.3 | 5.3 Rechazos, duplicados y reconciliación | NÚCLEO | D24 | 25 | obligatorios 1, 3, 4 de 4 |
| 5.4 | 5.4 Cargas repetibles, registro (logging) y reproducibilidad | NÚCLEO | D24 | 25 | obligatorios 1, 2 de 4 |
| 5.5 | 5.5 Estructura de un ETL: cuatro funciones y un `main` pequeño | NÚCLEO | D23 | 25 | obligatorios 3 de 4 |
| 6.1 | 6.1 Qué es un KPI: la ficha de definición y las ventas entregadas | NÚCLEO | D12 | 41 | obligatorios 1, 3 de 3 |
| 6.2 | 6.2 Cumplimiento, cobertura y efectividad | NÚCLEO | D25 | 25 | obligatorios 1, 2 de 3 |
| 6.3 | 6.3 Ticket medio, drop size, frecuencia y clientes activos | NÚCLEO | D16 | 25 | obligatorios 1, 3 de 3 |
| 6.4 | 6.4 Productividad, crecimiento y variaciones | NÚCLEO | D25 | 20 | obligatorios 2, 3 de 3 |
| 6.5 | 6.5 ABC, Pareto y rotación de inventario | NÚCLEO | D19 | 25 | obligatorios 2, 3 de 3 |
| 6.6 | 6.6 Interpretar, recomendar y qué hacer cuando faltan datos | NÚCLEO | D38 | 25 | obligatorios 2, 3 de 3 |
| 7.1 | 7.1 Qué es un programa y cómo se ejecuta | NÚCLEO | D01 | 15 | obligatorios 1 de 3 |
| 7.2 | 7.2 Variables y asignación | NÚCLEO | D01 | 15 | obligatorios 2 de 3 |
| 7.3 | 7.3 Tipos de datos y aritmética | NÚCLEO | D02 | 20 | obligatorios 2, 3 de 4 |
| 7.4 | 7.4 Tu primera función corta | NÚCLEO | D01 (sec.), D02 (resto) | 28 | obligatorios 3 de 3 |
| 7.5 | 7.5 Texto: cadenas, métodos y f-strings | NÚCLEO | D02 (sec.), D02 (resto) | 34 | obligatorios 2, 3 de 4 |
| 7.6 | 7.6 Booleanos, comparaciones y None | NÚCLEO | D02 | 20 | obligatorios 1 de 4 |
| 7.7 | 7.7 Conversiones de tipo y los primeros errores de valor | NÚCLEO | D08 | 30 | obligatorios 1, 2, 4 de 4 |
| 7.8 | 7.8 Listas y tuplas: guardar varios valores | NÚCLEO | D03 | 20 | obligatorios 1, 2, 4 de 4 |
| 7.9 | 7.9 Diccionarios y conjuntos | NÚCLEO | D03 | 20 | obligatorios 2, 3, 4 de 4 |
| 7.10 | 7.10 Condicionales: if, elif y else | NÚCLEO | D02 (sec.), D04 (resto) | 27 | obligatorios 1, 2 de 3 |
| 7.11 | 7.11 Repetir: for y while | NÚCLEO | D04 | 20 | obligatorios 1, 2, 3, 4 de 4 |
| 7.12 | 7.12 Acumuladores y patrones de recorrido | NÚCLEO | D04 | 28 | obligatorios 2, 3, 5 de 5 |
| 7.13 | 7.13 Recorrer registros: listas de diccionarios | NÚCLEO | D05 | 25 | obligatorios 1, 2, 3 de 4 |
| 8.1 | 8.1 Funciones con contrato | NÚCLEO | D08 | 20 | obligatorios 1, 3 de 3 |
| 8.2 | 8.2 Ámbito de las variables y efectos secundarios | COMPLEMENTARIA | — | 15 | — |
| 8.3 | 8.3 Archivos: rutas, CSV y JSON | NÚCLEO | D10 | 25 | obligatorios 3, 4 de 4 |
| 8.4 | 8.4 Módulos e importaciones | NÚCLEO | D10 | 30 | obligatorios 2, 3, 5 de 5 |
| 8.5 | 8.5 Excepciones: try, except y raise | NÚCLEO | D09 | 25 | obligatorios 1, 2, 4 de 4 |
| 8.6 | 8.6 Leer un traceback | NÚCLEO | D12 | 20 | obligatorios 1, 3 de 3 |
| 8.7 | 8.7 Pruebas con assert y depuración paso a paso | NÚCLEO | D12 | 20 | obligatorios 1, 3 de 3 |
| 9.1 | 9.1 NumPy: de listas a arreglos | COMPLEMENTARIA | — | 20 | — |
| 9.2 | 9.2 Series, DataFrame y leer un CSV | NÚCLEO | D15 | 25 | obligatorios 1, 2, 4 de 4 |
| 9.3 | 9.3 Inspeccionar los datos antes de usarlos (perfilado) | NÚCLEO | D15 | 20 | obligatorios 1, 3 de 3 |
| 9.4 | 9.4 Seleccionar, filtrar y ordenar | NÚCLEO | D17 | 20 | obligatorios 1, 2 de 4 |
| 9.5 | 9.5 Valores vacíos y filas duplicadas | NÚCLEO | D16 | 22 | obligatorios 3, 4 de 4 |
| 9.6 | 9.6 Convertir tipos, limpiar texto y trabajar con fechas | NÚCLEO | D23 | 25 | obligatorios 1, 2 de 3 |
| 10.1 | 10.1 Columnas nuevas y transformaciones | NÚCLEO | D16 | 25 | obligatorios 1, 2, 3 de 4 |
| 10.2 | 10.2 groupby y agregaciones | NÚCLEO | D17 | 20 | obligatorios 1, 2, 3 de 4 |
| 10.3 | 10.3 merge: unir tablas y controlar la cardinalidad | NÚCLEO | D17 | 25 | obligatorios 1, 2, 3 de 4 |
| 10.4 | 10.4 Tablas de resumen y exportación (CSV y SQLite) | NÚCLEO | D24 | 20 | obligatorios 2, 3 de 4 |
| 10.5 | 10.5 Controles de calidad y reconciliación en Pandas | NÚCLEO | D19 | 25 | obligatorios 1, 2, 3 de 4 |
| 10.6 | 10.6 Errores silenciosos: los que no avisan | NÚCLEO | D26 | 25 | obligatorios 1, 2, 4 de 4 |
| 11.1 | 11.1 Población, muestra y tipos de variables | NÚCLEO | D09 | 25 | obligatorios 1, 3 de 3 |
| 11.2 | 11.2 Frecuencias: contar y expresar en porcentaje | NÚCLEO | D11 | 20 | obligatorios 1, 3 de 3 |
| 11.3 | 11.3 Media, mediana y moda | NÚCLEO | D11 | 25 | obligatorios 2, 3 de 3 |
| 11.4 | 11.4 Dispersión: rango, varianza y desviación estándar | NÚCLEO | D18 | 30 | obligatorios 1, 3 de 3 |
| 11.5 | 11.5 Percentiles, cuartiles y valores atípicos | NÚCLEO | D25 | 30 | obligatorios 1, 2, 4 de 4 |
| 11.6 | 11.6 Distribuciones, histogramas, normalidad y puntaje z | COMPLEMENTARIA | — | 30 | — |
| 11.7 | 11.7 Correlación y causalidad | COMPLEMENTARIA | — | 25 | — |
| 11.8 | 11.8 Muestreo: cómo escoger una muestra que sirva | NÚCLEO | D32 | 25 | obligatorios 1, 2, 3 de 3 |
| 11.9 | 11.9 Estadística descriptiva con Pandas: un informe completo | COMPLEMENTARIA | — | 20 | — |
| 12.1 | 12.1 Por qué hace falta la inferencia: la variabilidad entre muestras | NÚCLEO | D36 | 25 | obligatorios 1, 2, 3 de 3 |
| 12.2 | 12.2 Estimación e intervalos de confianza | NÚCLEO | D37 | 30 | obligatorios 1, 3 de 3 |
| 12.3 | 12.3 Hipótesis nula, hipótesis alternativa y errores | NÚCLEO | D37 | 30 | obligatorios 1, 2 de 3 |
| 12.4 | 12.4 El p-valor, calculado de verdad | NÚCLEO | D38 | 30 | obligatorios 1, 2, 3 de 3 |
| 12.5 | 12.5 Comparar dos promedios: la prueba t (Student y Welch) | NÚCLEO | D39 | 30 | obligatorios 2, 3 de 4 |
| 12.6 | 12.6 Relación entre dos categorías: la prueba chi-cuadrado | COMPLEMENTARIA | — | 25 | — |
| 12.7 | 12.7 Tamaño del efecto: significativo no es lo mismo que importante | COMPLEMENTARIA | — | 25 | — |
| 12.8 | 12.8 Interpretar, comunicar y no equivocarse | NÚCLEO | D39 | 30 | obligatorios 1, 3 de 3 |
| 13.1 | 13.1 Hechos, dimensiones y granularidad | NÚCLEO | D26 | 25 | obligatorios 1, 2 de 3 |
| 13.2 | 13.2 El modelo estrella: relaciones y varios hechos | NÚCLEO | D29 | 30 | obligatorios 2, 3 de 3 |
| 13.3 | 13.3 La tabla de fechas (calendario) | NÚCLEO | D32 | 20 | obligatorios 1, 3 de 3 |
| 14.1 | 14.1 Power BI desde cero: qué es, el flujo de trabajo y la configuración regional | NÚCLEO | D30 | 34 | obligatorios 2, 3 de 3 |
| 14.2 | 14.2 Power Query y el lenguaje M | NÚCLEO | D31 | 25 | obligatorios 1, 2 de 3 |
| 14.3 | 14.3 DAX: medidas y contexto de filtro | NÚCLEO | D33 | 35 | obligatorios 2, 3, 4 de 4 |
| 14.4 | 14.4 Medidas útiles de un tablero comercial y cómo controlarlas | NÚCLEO | D33 | 30 | obligatorios 1, 2, 4 de 4 |
| 14.5 | 14.5 Diseño del tablero y lista de comprobación manual | NÚCLEO | D33 (sec.) | 25 | obligatorios 1 de 3 |
| 15.1 | 15.1 Excel desde cero: datos limpios, tablas y la configuración regional | NÚCLEO | D30 | 25 | obligatorios 1, 2, 3 de 4 |
| 15.2 | 15.2 Funciones de Excel para cuadrar: condiciones, sumas y búsquedas | NÚCLEO | D31 | 25 | obligatorios 1, 2, 3 de 4 |
| 15.3 | 15.3 Tablas dinámicas, estadística en Excel y el cuadre entre herramientas | NÚCLEO | D31 | 30 | obligatorios 4 de 4 |
| 16.1 | 16.1 Git desde cero: guardar versiones de tu trabajo | NÚCLEO | D05 | 20 | obligatorios 1, 2, 3 de 4 |
| 16.2 | 16.2 Documentar y explicar tu trabajo: README, errores y decisiones | NÚCLEO | D40 | 25 | obligatorios 2, 3 de 4 |
| 16.3 | 16.3 Portafolio y búsqueda de empleo honesta desde la primera semana | EMPLEO | — | 25 | — |
| 17.1 | 17.1 Los ocho pasos frente a un caso nuevo | NÚCLEO | D36 | 30 | — |
| 17.2 | 17.2 Cuando no cuadra: reducir el problema hasta encontrar el primer desvío | NÚCLEO | D38 | 25 | — |
| 17.3 | 17.3 Resolver sin ayuda externa: método, evidencia y honestidad | COMPLEMENTARIA | — | 30 | — |
| 18.1 | 18.1 Cómo responder una pregunta técnica en cuatro pasos | NÚCLEO | D40 | 25 | obligatorios 1, 2, 3 de 4 |
| 18.2 | 18.2 Banco de preguntas frecuentes y respuestas modelo | EMPLEO | — | 30 | — |
| 18.3 | 18.3 Preguntas de comportamiento, apoyo de IA y honestidad | EMPLEO | — | 25 | — |

## SQL de recuperación (práctica frecuente y progresiva)

Entre las lecciones de SQL (capítulos 1–4) y el final del programa, las jornadas normales incluyen una variante breve de SQL ya enseñado (SQ01–SQ17, KP01) para que el SQL no se olvide mientras se avanza en Python, Pandas, ETL y BI. Las jornadas D08, D22 y D36 (lunes con clase UAGRM) no la llevan.

| Día | Ejercicios | Minutos |
|---:|---|---:|
| D10 | SQ01 | 25 |
| D12 | SQ02, SQ03 | 40 |
| D15 | SQ04 | 15 |
| D17 | SQ05 | 15 |
| D23 | SQ06 | 15 |
| D24 | SQ07 | 15 |
| D25 | SQ08 | 15 |
| D26 | SQ09 | 15 |
| D30 | SQ10, SQ11 | 30 |
| D32 | SQ12 | 15 |
| D33 | SQ13 | 15 |
| D37 | SQ14 | 15 |
| D38 | SQ15 | 15 |
| D39 | SQ16 | 20 |
| D40 | SQ17 | 15 |

## REFUERZO y recursos fuera de la ruta

- Cada jornada normal sugiere un REFUERZO voluntario (en total hasta 2048 min), con ejercicios **diferentes** de los obligatorios y sobre contenidos ya enseñados.
- 33 ejercicios existentes no tienen jornada y quedan como banco de práctica: C01, C02, C04, C05, CL4, DB02, DB03, EX02, EX03, K3, K6, ME04, N1, N10, N11, N15, N4, N5, N6, N8, P24, P25, P26, P27, P28, P30, PB04, PB06, V1, V5, X2, X4, X7.
- Ejercicios que exigen lecciones COMPLEMENTARIAS y por eso no están en la ruta: ST03 (exige 11.6); ST04 (exige 11.7, 11.9 y 9.1); ST06 (exige 12.6/12.7 (chi-cuadrado, V de Cramér)); C03 (exige 11.6, 11.7, 11.9, 12.6); P20 (declara 9.1 (revisar si NumPy es imprescindible)); N7 (exige 4.4); N13 (exige 4.4 (EXPLAIN)); V2 (declara 4.4 (revisar)); PB05 (exige 14.5 completa).
