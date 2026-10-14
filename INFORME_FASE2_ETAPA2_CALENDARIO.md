# Informe Fase 2 · Etapa 2: integración pedagógica, calendario y modalidades de estudio

Plan Data & BI v5 · 13 de octubre de 2026 · Etapa 2 **completa, pendiente de tu revisión**. No se hizo la Etapa 3. No hay commits, ramas nuevas ni push. `mi_trabajo` y D01 no se tocaron; D02 solo recibió un bloque informativo de lecciones.

## 1. Resumen

| Tu requisito | Resultado |
|---|---|
| 1. Resolver las 91 horas de teoría | Las 100 lecciones están clasificadas **una por una**: 47 NÚCLEO (con día asignado), 33 REFUERZO y 20 PROFUNDIZACIÓN. Todas siguen disponibles. La ruta BASE son 15 h netas por semana; la EXTENDIDA añade tiempo voluntario hasta 20–25 h. Los tiempos de los ejercicios **no se redujeron**; 484 min de ejercicios pasaron de OBLIGATORIO a REFUERZO/OPCIONAL (sección 4). |
| 2. Criterio analítico empresarial | 18 actividades `AN01–AN18` (martes a viernes, 15 min), con cifras de control recalculadas por un verificador. Cubren problema de negocio, elección de KPI, tendencias, comparación, datos insuficientes, hechos frente a hipótesis y recomendaciones, además de media, mediana, moda, dispersión, percentiles, cuartiles, ABC, cumplimiento, cobertura, efectividad y productividad (sección 7). |
| 3. Demostrar comprensión | 8 hitos `H01–H08`, uno por puerta: explicar, predecir, resolver una variante nueva y justificar. «Un OK del corrector no basta» quedó escrito en `COMPETENCIAS.md` (sección 7). |
| 4. Reparar la integración | P02 y P07 corregidos y, con ellos, 27 enunciados de Python, 28 de SQL y los criterios de ST01–ST07; orden de los capítulos 5 y 6 documentado; las guías diarias enlazan las lecciones con sus minutos; D01 intacto, D02 con objetivo, ejercicios y tiempos originales, domingos flexibles (sección 8). |
| 5. Control final | 42 jornadas con tiempos de plan y estimados (sección 5), teoría obligatoria frente a práctica (sección 4), horas BASE y EXTENDIDA por semana (sección 3) y revisión de prerrequisitos (sección 6). |

**Lo que debes saber antes de aprobar (honestidad primero):**

- El plan sigue en **900 min (15 h) por semana**, pero la **estimación de primera vez** de lo que contiene es de unos **991 min (16,5 h) de media**; las semanas 3, 4 y 5 estiman entre 16,7 y 17,1 h. Ya era así antes: la versión anterior estimaba entre 970 y 1010 min por semana (media 992 en las semanas 2–6, sin incluir lecciones) y la actual, entre 955 y 1023 (media 995 en las mismas semanas, **con** lecciones y criterio analítico). Es decir, se **reasignó** el tiempo en lugar de agrandarlo. No bajé las estimaciones para que el número se vea mejor. Qué hacer con esa diferencia es la decisión 1 de la sección 10.
- Las estimaciones tienen un error razonable de ±35 % y no son mediciones. Registra tus minutos reales en `mi_trabajo/progreso.csv`.
- Prerrequisitos: 17 de los prerrequisitos de las lecciones NÚCLEO son lecturas REFUERZO **recomendadas**, no obligatorias (sección 6). Los demás están cubiertos por una lección NÚCLEO anterior o por un ejercicio anterior.

## 2. Cómo se clasificaron las 100 lecciones

Criterio, aplicado lección por lección en `01_PLAN_DIARIO/lecciones.json` (fuente única):

- **NÚCLEO**: el ejercicio o la puerta de la ruta BASE la necesita, o es el único lugar donde se enseña algo que se evalúa. Su **lectura** (el campo «lectura N min» del encabezado) cuenta dentro de las 15 h y tiene día. Su **micropráctica** es práctica guiada sin corrector: en BASE la sustituyen los ejercicios del día.
- **REFUERZO**: sirve cuando una competencia no está dominada (cada lección dice **cuándo**) y aparece en la EXTENDIDA de un día concreto.
- **PROFUNDIZACIÓN**: va más allá de la base (inferencia estadística, BI avanzado, portafolio, entrevistas). EXTENDIDA u otros periodos, después de la evaluación final.

| Cap. | Tema | NÚCLEO | REFUERZO | PROFUNDIZACIÓN | Lectura NÚCLEO (min) | Total de primera vez (min) |
|---:|---|---:|---:|---:|---:|---:|
| 1 | SQL desde cero: una pregunta, una tabla y un resultado | 2 | 5 | 0 | 30 | 300 |
| 2 | Agregar sin perder el significado | 4 | 1 | 0 | 85 | 260 |
| 3 | JOIN: conectar tablas y controlar multiplicaciones | 3 | 1 | 0 | 65 | 210 |
| 4 | Subconsultas, CTE, ventanas, fechas e índices | 2 | 2 | 0 | 40 | 215 |
| 5 | Calidad de datos y ETL: un proceso que puedas defender | 2 | 3 | 0 | 50 | 275 |
| 6 | KPIs empresariales: definición antes de fórmula | 5 | 1 | 0 | 120 | 340 |
| 7 | Python: construir el razonamiento antes de Pandas | 8 | 5 | 0 | 178 | 715 |
| 8 | Funciones, errores y archivos reproducibles | 4 | 3 | 0 | 87 | 370 |
| 9 | NumPy y Pandas básico: tablas después de entender listas y funciones | 3 | 3 | 0 | 62 | 335 |
| 10 | Pandas: transformar, unir y validar | 3 | 3 | 0 | 65 | 360 |
| 11 | Estadística descriptiva: resumir antes de concluir | 3 | 2 | 4 | 85 | 515 |
| 12 | Estadística inferencial: decidir con incertidumbre | 0 | 0 | 8 | 0 | 485 |
| 13 | Modelado dimensional: hechos, dimensiones y modelo estrella | 1 | 1 | 1 | 25 | 160 |
| 14 | Power BI, Power Query y DAX: cargar, modelar, medir y comprobar | 2 | 0 | 3 | 65 | 285 |
| 15 | Excel como segundo camino de validación | 1 | 2 | 0 | 30 | 170 |
| 16 | Documentar y comunicar trabajo real: Git, README y empleo honesto | 1 | 1 | 1 | 25 | 140 |
| 17 | Transferencia y autonomía: resolver datos que cambian | 2 | 0 | 1 | 55 | 175 |
| 18 | Preparación técnica y conductual para entrevistas | 1 | 0 | 2 | 25 | 155 |
| **Total** | | **47** | **33** | **20** | **1092** | **5465** |

Los índices de capítulo (`02_TEORIA/NN_*.md`) muestran la clase de cada lección y, si es NÚCLEO, el día. `02_TEORIA/INDICE.md` y `01_PLAN_DIARIO/RUTAS.md` (generado) resumen la ruta. Python (capítulos 7 y 8) y SQL (1–4) conservan sus lecciones de fundamentos como NÚCLEO; lo que pasa a REFUERZO es lo que ya practican D01–D02 (7.1–7.5, 1.1–1.3, 1.5) o lo que ocurre dentro de un ejercicio (por ejemplo 8.6 con DB01).

## 3. Horas por semana: BASE y EXTENDIDA

| Semana | BASE plan (min) | BASE estimado (min / h) | Teoría y lecciones NÚCLEO | Criterio e hitos | Ejercicios OBLIGATORIOS | EXTENDIDA extra (L–S) | EXTENDIDA plan (h) | EXTENDIDA estimada (h) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 900 | 976 / 16,3 | 268 min (12 lecc.) | 65 min | 353 min (9 ej.) | 390 min | 21,5–23,5 | 22,8–24,8 |
| 2 | 900 | 975 / 16,2 | 242 min (11 lecc.) | 80 min | 363 min (9 ej.) | 390 min | 21,5–23,5 | 22,8–24,8 |
| 3 | 900 | 1017 / 16,9 | 237 min (11 lecc.) | 80 min | 410 min (8 ej.) | 390 min | 21,5–23,5 | 23,4–25,4 |
| 4 | 900 | 1023 / 17,1 | 165 min (7 lecc.) | 75 min | 493 min (7 ej.) | 390 min | 21,5–23,5 | 23,6–25,6 |
| 5 | 900 | 1003 / 16,7 | 140 min (5 lecc.) | 70 min | 503 min (9 ej.) | 390 min | 21,5–23,5 | 23,2–25,2 |
| 6 | 900 | 955 / 15,9 | 130 min (5 lecc.) | 65 min | 470 min (5 ej.) | 390 min | 21,5–23,5 | 22,4–24,4 |

- **BASE plan**: 900 min por semana en las seis semanas. **BASE estimado**: suma del plan fijo (empleo, examen, cierre) más la lectura NÚCLEO, el criterio y los ejercicios OBLIGATORIOS con su tiempo de «primera vez». La semana 1 incluye D01 y D02 tal como estaban diseñados (D02 suma 5 min por sus dos lecciones).
- **EXTENDIDA plan**: BASE más 30–75 min voluntarios por jornada de lunes a sábado (390 min por semana) y, opcionalmente, un domingo de 45–120 min. Da 21,5–23,5 h; con la estimación de BASE llega a 22,4–25,6 h. Si tu semana BASE ya consumió más de 16,5 h reales, la guía te dice que no uses EXTENDIDA esa semana.
- Cada guía diaria lista en «EXTENDIDA» las lecciones REFUERZO/PROFUNDIZACIÓN y los ejercicios REFUERZO de ese día con sus minutos. No todo cabe: lo que sobra es para «otros periodos».

## 4. Teoría obligatoria frente a práctica

| Semana | Teoría y lecciones NÚCLEO | Criterio e hitos | Ejercicios OBLIGATORIOS (estimado) | Teoría : práctica | Examen y corrección | Empleo y cierre |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 268 | 65 | 353 | 1 : 1,3 | 115 | 175 |
| 2 | 242 | 80 | 363 | 1 : 1,5 | 115 | 175 |
| 3 | 237 | 80 | 410 | 1 : 1,7 | 115 | 175 |
| 4 | 165 | 75 | 493 | 1 : 3,0 | 115 | 175 |
| 5 | 140 | 70 | 503 | 1 : 3,6 | 115 | 175 |
| 6 | 130 | 65 | 470 | 1 : 3,6 | 115 | 175 |

La proporción pasa de 1 : 1,3 en la semana 1 a 1 : 3,6 en las semanas 5–6: al principio se aprende leyendo y practicando; después el tiempo se va a los proyectos (mini-ETL, ETL guiado, Power BI, C06), cuyos enunciados llevan sus propias instrucciones.

**Ejercicios que dejaron de ser OBLIGATORIOS** (484 min en total). Siguen en la guía del día como REFUERZO/OPCIONAL y cuentan para EXTENDIDA y recuperación:

| Ejercicio | Día antes | Primera vez (min) | Ahora | Motivo |
|---|---:|---:|---|---|
| S5 | D03 | 20 | REFUERZO en D03 | misma habilidad que S3 y S6 (filtros y LIKE); sin evidencia propia en S01 |
| ST01 | D04 | 55 | REFUERZO en D04 | la media, la mediana y la moda se practican en 11.3 y en AN08; el ejercicio queda como práctica extra |
| G7 | D06 | 28 | REFUERZO en D06 | repite G5/G6 con dos columnas; no es evidencia de S01 |
| G8 | D06 | 32 | REFUERZO en D06 | exige strftime (lección 2.4, refuerzo); no es evidencia de S01 |
| J3 | D10 | 40 | REFUERZO en D09 | repite J1/J2 con una tabla más; la evidencia de la P2 es J1, J2 y J5 |
| J4 | D10 | 35 | REFUERZO en D10 | repite J1/J2 con otra dimensión; queda como REFUERZO en D10 |
| ST02 | D12 | 65 | REFUERZO en D12 | percentiles en 11.5 y AN13; el ejercicio queda como práctica extra |
| P19 | D15 | 42 | REFUERZO en D16 | P20 reutiliza su lógica; no se pide aprobar P19 para la Puerta 3 |
| K3 | D18 | 55 | REFUERZO en D18 | V3 cubre el CTE y el promedio; no es evidencia del S03 |
| V2 | D19 | 60 | REFUERZO en D19 | no es evidencia de S03; la lección 4.4 queda como refuerzo |
| ME04 | D31 | 52 | REFUERZO en D31 | el hito H04 (regla nueva sobre tu mini-ETL) reemplaza su papel de «modificar un ETL» |
| **Total** | | **484** | | |

**Ejercicios que cambiaron de día** (siguen siendo OBLIGATORIOS, solo se reordenaron para que su lección se lea antes):

| Ejercicio | Cambio de día | Por qué |
|---|---|---|
| P08 | D05 → D08 | las lecciones 7.10–7.13 llenan D05; P08 repite el `if/elif` de P02 |
| P09 | D08 → D10 | necesita 7.7, 8.1 y 8.5 antes (lecciones D08–D09) |
| P10 | D09 → D12 | necesita 8.4 y 8.5 (D09–D10) |
| P11 | D11 → D12 | necesita 7.7 y 8.5; D11 ya tiene J5 |
| DB01 | D12 → D11 | se lee el traceback (19 §1) en D11 |
| P17 | D12 → D15 | Pandas empieza con la lección 9.2 (D15) |
| E4 | D13 → D31 | sólo lo exigen EX01 y S05; D13 es el sábado del examen |
| P20 | D16 → D17 | necesita la lección 10.2 (D17) |
| P22 | D17 → D16 | necesita 9.5 (D16) |
| P23 | D18 → D19 | necesita 9.3 y 9.5; D19 tiene espacio tras V3 |
| V3 | D19 → D18 | ventanas se leen en D18 |
| V4 | D20 → D19 | necesita 2.5 y 6.5 (D19) |

La Puerta 3 ya no exige P19 ni K3 (P20 reutiliza la lógica de P19; V3 cubre el CTE) y exige H03; la Puerta 2 y las demás exigen su hito. Los exámenes S01–S06 **no se modificaron** (son de la Etapa 3); `auditar_enunciados.py` confirma que todo lo que evalúan está preparado como OBLIGATORIO/REPASO antes del examen.

## 5. Las 42 jornadas

Tiempos de **plan** por bloque (suman los 900 min de cada semana) y **estimado** de primera vez. «Lecciones» es lectura NÚCLEO (en D01 y D02 es el bloque «Teoría» original). «Razón» = estimado / plan; por encima de 1,2 la jornada es AJUSTADA y se usa el modo REDUCIDO (no se alarga el día).

| Día | Fecha | Jornada | Plan | Lecciones | SQL | Práctica | Criterio | Examen | Empleo | Cierre | Estimado | Razón |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| D01 | 2026-10-12 | Entorno, filas y variables | 90 | 20 | 15 | 35 | 0 | 0 | 10 | 10 | 90 | 1,00 |
| D02 | 2026-10-13 | Filtros, NULL y texto | 160 | 30 | 25 | 70 | 0 | 0 | 25 | 10 | 165 | 1,03 |
| D03 | 2026-10-14 | Listas, diccionarios y clientes únicos | 150 | 55 | 30 | 30 | 15 | 0 | 10 | 10 | 174 | 1,16 |
| D04 | 2026-10-15 | Agrupación, bucles y media/mediana | 150 | 60 | 15 | 20 | 15 | 0 | 30 | 10 | 163 | 1,09 |
| D05 | 2026-10-16 | Condiciones, funciones cortas y KPIs | 150 | 73 | 25 | 17 | 15 | 0 | 10 | 10 | 184 | 1,23 |
| D06 | 2026-10-17 | Primer examen y cierre de fundamentos | 200 | 25 | 0 | 0 | 20 | 115 | 30 | 10 | 200 | 1,00 |
| D07 | 2026-10-18 | Domingo flexible (45–120 min voluntarios) | 0 | — | — | — | — | — | — | — | 0 | — |
| D08 | 2026-10-19 | Funciones con contrato y condiciones | 90 | 45 | 0 | 25 | 0 | 0 | 10 | 10 | 93 | 1,03 |
| D09 | 2026-10-20 | Primer JOIN y errores visibles | 160 | 40 | 70 | 0 | 15 | 0 | 25 | 10 | 157 | 0,98 |
| D10 | 2026-10-21 | Funciones que convierten y archivos CSV | 150 | 47 | 0 | 68 | 15 | 0 | 10 | 10 | 179 | 1,19 |
| D11 | 2026-10-22 | Ausencia con LEFT JOIN | 150 | 60 | 25 | 10 | 15 | 0 | 30 | 10 | 183 | 1,22 |
| D12 | 2026-10-23 | Fechas, cantidades y leer un error | 150 | 25 | 0 | 90 | 15 | 0 | 10 | 10 | 163 | 1,09 |
| D13 | 2026-10-24 | Examen de JOIN y conciliación | 200 | 25 | 0 | 0 | 20 | 115 | 30 | 10 | 200 | 1,00 |
| D14 | 2026-10-25 | Domingo flexible (45–120 min voluntarios) | 0 | — | — | — | — | — | — | — | 0 | — |
| D15 | 2026-10-26 | Primer DataFrame y perfilado | 90 | 40 | 10 | 20 | 0 | 0 | 10 | 10 | 100 | 1,11 |
| D16 | 2026-10-27 | Duplicados exactos y drop size | 160 | 42 | 40 | 28 | 15 | 0 | 25 | 10 | 175 | 1,09 |
| D17 | 2026-10-28 | Agrupar y unir con validación | 150 | 45 | 0 | 70 | 15 | 0 | 10 | 10 | 195 | 1,30 |
| D18 | 2026-10-29 | CTE y concentración de ventas | 150 | 40 | 55 | 0 | 15 | 0 | 30 | 10 | 160 | 1,07 |
| D19 | 2026-10-30 | ABC, perfilado y criterio | 150 | 45 | 45 | 25 | 15 | 0 | 10 | 10 | 187 | 1,25 |
| D20 | 2026-10-31 | Examen Pandas y SQL intermedio | 200 | 25 | 0 | 0 | 20 | 115 | 30 | 10 | 200 | 1,00 |
| D21 | 2026-11-01 | Domingo flexible (45–120 min voluntarios) | 0 | — | — | — | — | — | — | — | 0 | — |
| D22 | 2026-11-02 | Mini-ETL (1): extraer y perfilar | 90 | 0 | 0 | 70 | 0 | 0 | 10 | 10 | 90 | 1,00 |
| D23 | 2026-11-03 | Mini-ETL (2): transformar con reglas y rechazos | 160 | 40 | 0 | 70 | 15 | 0 | 25 | 10 | 180 | 1,12 |
| D24 | 2026-11-04 | Mini-ETL (3): validar, cuadrar y cargar | 150 | 40 | 0 | 65 | 25 | 0 | 10 | 10 | 180 | 1,20 |
| D25 | 2026-11-05 | ETL guiado (1): contrato, Bronze y texto | 150 | 60 | 0 | 35 | 15 | 0 | 30 | 10 | 190 | 1,27 |
| D26 | 2026-11-06 | ETL guiado (2): fechas, cantidad, claves y duplicados | 150 | 25 | 0 | 85 | 20 | 0 | 10 | 10 | 180 | 1,20 |
| D27 | 2026-11-07 | Examen S04: mini-ETL y ETL hasta claves | 200 | 0 | 45 | 0 | 0 | 115 | 30 | 10 | 203 | 1,01 |
| D28 | 2026-11-08 | Domingo flexible (45–120 min voluntarios) | 0 | — | — | — | — | — | — | — | 0 | — |
| D29 | 2026-11-09 | ETL guiado (3): Silver, validación y rechazos | 90 | 30 | 0 | 40 | 0 | 0 | 10 | 10 | 100 | 1,11 |
| D30 | 2026-11-10 | ETL guiado (4): Gold, carga y cuadre SQL | 160 | 25 | 0 | 80 | 20 | 0 | 25 | 10 | 190 | 1,19 |
| D31 | 2026-11-11 | Excel: tabla dinámica y cuadre | 150 | 20 | 30 | 65 | 15 | 0 | 10 | 10 | 175 | 1,17 |
| D32 | 2026-11-12 | Power BI (1): importar y relacionar | 150 | 30 | 0 | 65 | 15 | 0 | 30 | 10 | 180 | 1,20 |
| D33 | 2026-11-13 | Power BI (2): primeras medidas | 150 | 35 | 0 | 75 | 20 | 0 | 10 | 10 | 155 | 1,03 |
| D34 | 2026-11-14 | Examen S05: ETL guiado completo y BI mínimo | 200 | 0 | 45 | 0 | 0 | 115 | 30 | 10 | 203 | 1,01 |
| D35 | 2026-11-15 | Domingo flexible (45–120 min voluntarios) | 0 | — | — | — | — | — | — | — | 0 | — |
| D36 | 2026-11-16 | Caso nuevo C06 (0): contrato y plan | 90 | 30 | 0 | 40 | 0 | 0 | 10 | 10 | 90 | 1,00 |
| D37 | 2026-11-17 | C06 (1): extraer, Bronze y perfil | 160 | 0 | 0 | 110 | 15 | 0 | 25 | 10 | 150 | 0,94 |
| D38 | 2026-11-18 | C06 (2): Silver y rechazos | 150 | 25 | 0 | 90 | 15 | 0 | 10 | 10 | 170 | 1,13 |
| D39 | 2026-11-19 | C06 (3): Gold y cuadres | 150 | 25 | 0 | 70 | 15 | 0 | 30 | 10 | 170 | 1,13 |
| D40 | 2026-11-20 | C06 (4): SQLite, repetición y README | 150 | 25 | 0 | 85 | 20 | 0 | 10 | 10 | 175 | 1,17 |
| D41 | 2026-11-21 | Último examen y preparación del final | 200 | 25 | 20 | 0 | 0 | 115 | 30 | 10 | 200 | 1,00 |
| D42 | 2026-11-22 | Domingo flexible (45–120 min voluntarios) | 0 | — | — | — | — | — | — | — | 0 | — |

Jornadas por encima de 1,2: D05 (1,23), D11 (1,22), D17 (1,30), D19 (1,25), D25 (1,27). Todas tienen modo REDUCIDO (`Haz solo:`) y una lección de lectura prioritaria (`Lecciones en REDUCIDO:`).

## 6. Revisión de prerrequisitos

`RUTAS.md` lista cada prerrequisito declarado en el encabezado de cada lección NÚCLEO con su estado: **núcleo** (lección NÚCLEO el mismo día o antes), **práctica** (lo cubre un ejercicio OBLIGATORIO anterior, comprobado por el verificador) o **recomendada** (lectura REFUERZO que conviene hacer si el concepto no está claro). No queda ningún prerrequisito sin estado. Resultado: 73 núcleo, 15 práctica y 17 recomendadas. Estas últimas son la parte que debes mirar:

| NÚCLEO | Día | Prerrequisito (REFUERZO) | Qué lo cubre |
|---|---:|---|---|
| 3.2 | D09 | 3.1 | Claves y relaciones: J1 y 3.2 lo retoman; léela si no sabes cuál es la clave de cada tabla. |
| 3.4 | D11 | 3.1 | Claves y relaciones: J1 y 3.2 lo retoman; léela si no sabes cuál es la clave de cada tabla. |
| 4.2 | D18 | 4.1 | 4.2 re-explica la idea de resultado con nombre; 4.1 se lee si una subconsulta anidada te confunde. |
| 5.3 | D24 | 10.5 | Controles en Pandas: ME02 y ME03 los piden paso a paso; léela si no sabes comparar antes y después. |
| 6.6 | D39 | 6.3 | Ticket y drop size: 6.6 los usa en sus ejemplos; K1 y AN08 los practican. Léela si no distingues ticket de drop size. |
| 9.2 | D15 | 9.1 | NumPy: 9.2 reintroduce Series; léela si no sabes qué es un arreglo. |
| 10.1 | D16 | 9.1 | NumPy: 9.2 reintroduce Series; léela si no sabes qué es un arreglo. |
| 10.1 | D16 | 9.4 | Filtrar un DataFrame: P17–P23 lo usan en una línea; léela si un filtro te da el resultado equivocado. |
| 10.1 | D16 | 9.6 | Tipos, texto y fechas en Pandas: P24 y ETL-2 los piden; léela antes de convertir fechas. |
| 10.3 | D17 | 3.1 | Claves y relaciones: J1 y 3.2 lo retoman; léela si no sabes cuál es la clave de cada tabla. |
| 11.3 | D13 | 11.1 | Población, muestra y tipos de variable: AN01 (unidad de análisis) los usa sin nombrarlos; léela si dudas qué es una variable numérica o categórica. |
| 13.2 | D30 | 13.1 | Hechos y dimensiones: 13.2 los usa; léela si no distingues una tabla de hechos de una dimensión. |
| 15.3 | D29 | 15.2 | Funciones de Excel: EX01 guía los pasos mínimos; léela si no sabes SUMAR.SI. |
| 16.2 | D40 | 16.1 | Git: cada jornada pide preparar un commit; léela si no sabes qué guarda un commit. |
| 17.1 | D36 | 10.5 | Controles en Pandas: ME02 y ME03 los piden paso a paso; léela si no sabes comparar antes y después. |
| 17.2 | D38 | 8.7 | Pruebas con assert: léela antes de C06; DB01–DB03 ya practican depurar. |
| 17.2 | D38 | 10.6 | Errores silenciosos: DB02, DB03 y C05 los practican; léela antes de C06. |

Prerrequisitos de **Python, SQL, Pandas y ETL**: las lecciones 7.6–7.13, 8.1, 8.3–8.5, 2.1–2.3, 2.5, 3.2–3.4, 4.2–4.3, 9.2–9.3, 9.5, 10.1–10.3, 5.2–5.3 y las secciones 1–4 del capítulo 19 son todas NÚCLEO y se leen antes del ejercicio que las usa (el verificador lo comprueba lección por lección contra cada OBLIGATORIO). Las lecciones 4.1 (subconsultas) y 9.1 (NumPy) quedan como recomendadas porque 4.2 y 9.2 vuelven a presentar lo mínimo; 10.5 y 10.6 porque ME02–ME03 y DB02–DB03 practican sus controles paso a paso. Si prefieres que una de ellas sea NÚCLEO, cuesta 20–25 min de lectura y empeora una semana ya densa (decisión 2).

**Orden de los capítulos 5 y 6.** El capítulo 5 (5.2, 5.3) se lee en D23–D24, después de Pandas (D15–D17) y junto a ME02–ME03. En el capítulo 6, la lección 6.1 se lee en D12 con sus ejemplos de **SQL** (sus ejemplos de Python hacen falta desde Pandas; se retoman desde D16), 6.5 en D19 junto a V3/V4, 6.2 en D26, 6.4 en D31 y 6.6 en D39. La lección 6.3 es refuerzo. Está escrito en `02_TEORIA/INDICE.md`.

## 7. Criterio analítico y comprensión

### Actividades de criterio analítico (15 min, martes a viernes)

| Actividad | Jornada | Habilidad de criterio | Lecciones |
|---|---:|---|---|
| [AN01 · ¿Qué estamos contando?](03_EJERCICIOS/Analitico/AN01.md) | D03 | definir el problema de negocio y la unidad de análisis | 1.6, 7.9 |
| [AN02 · Hechos e hipótesis: los pedidos anulados](03_EJERCICIOS/Analitico/AN02.md) | D04 | separar hechos de hipótesis | 2.1 |
| [AN03 · ¿Qué es una ruta «grande»?](03_EJERCICIOS/Analitico/AN03.md) | D05 | comparar y elegir un criterio con su denominador | 2.2 |
| [AN04 · Cumplimiento: ¿a quién felicitas?](03_EJERCICIOS/Analitico/AN04.md) | D09 | elegir un KPI y entender su denominador | 2.3, 3.2 |
| [AN05 · ¿El INNER JOIN pierde filas?](03_EJERCICIOS/Analitico/AN05.md) | D10 | detectar datos insuficientes y comprobar un supuesto | 3.2 |
| [AN06 · Recomendación a gerencia: clientes sin compra](03_EJERCICIOS/Analitico/AN06.md) | D11 | redactar una recomendación con hechos, límites y una acción | 3.3 |
| [AN07 · Tres preguntas, tres KPI](03_EJERCICIOS/Analitico/AN07.md) | D12 | elegir el KPI adecuado y definirlo con su ficha | 6.1 |
| [AN08 · ¿Cuál es el pedido típico?](03_EJERCICIOS/Analitico/AN08.md) | D16 | elegir entre media, mediana y moda y comparar | 11.3 |
| [AN09 · Tendencia: ¿más pedidos o pedidos más grandes?](03_EJERCICIOS/Analitico/AN09.md) | D17 | analizar una tendencia y descomponer una variación | 10.2 |
| [AN10 · Concentración: ¿de cuántos clientes dependemos?](03_EJERCICIOS/Analitico/AN10.md) | D18 | interpretar una concentración de ventas | 4.3 |
| [AN11 · ABC: qué hacer con cada clase](03_EJERCICIOS/Analitico/AN11.md) | D19 | traducir una clasificación en decisiones | 6.5 |
| [AN12 · Rechazos: ¿problema de datos o señal de negocio?](03_EJERCICIOS/Analitico/AN12.md) | D23 | detectar datos insuficientes y separar hechos de hipótesis | 5.2, 19.2 |
| [AN13 · Dispersión y atípicos: ¿qué pedido es «raro»?](03_EJERCICIOS/Analitico/AN13.md) | D25 | usar dispersión, cuartiles y percentiles para decidir | 11.4, 11.5 |
| [AN14 · Cobertura frente a efectividad: ¿a quién ayudas?](03_EJERCICIOS/Analitico/AN14.md) | D31 | comparar vendedores con el KPI correcto | 6.2, 6.4 |
| [AN15 · Productividad: dos formas de medir una ruta](03_EJERCICIOS/Analitico/AN15.md) | D32 | comparar resultados cambiando el denominador | 6.4 |
| [AN16 · C06: el problema de negocio antes del código](03_EJERCICIOS/Analitico/AN16.md) | D37 | definir el problema de negocio y lo que los datos no pueden responder | 10.6, 17.1 |
| [AN17 · C06: ¿hay tendencia o ruido?](03_EJERCICIOS/Analitico/AN17.md) | D38 | comparar periodos y reconocer datos insuficientes | 17.2 |
| [AN18 · C06: el memo para gerencia](03_EJERCICIOS/Analitico/AN18.md) | D39 | redactar una recomendación a gerencia con hechos, límites y una acción | 6.6 |

Cada una tiene Situación, Datos, Qué debes entregar, Reglas, tres Pistas y Criterios de aceptación. No hay corrector: se evalúa tu razonamiento y se contrasta con `08_SOLUCIONES/controles_analitico.md` **después** de escribir. Los datos salen de **tus propios resultados** (G1, G5, K1, V3, V4, J5, E4, ME02…) o de números inventados en el enunciado, así que ningún enunciado publica el resultado de un ejercicio (el verificador lo comprueba contra `controles_sql.json`).

### Hitos de comprensión (uno por puerta)

| Hito | Puerta | Jornada | Título |
|---|---|---:|---|
| [H01](03_EJERCICIOS/Comprension/H01.md) | P1 | D06 | consultar y calcular |
| [H02](03_EJERCICIOS/Comprension/H02.md) | P2 | D13 | funciones, errores y JOIN |
| [H03](03_EJERCICIOS/Comprension/H03.md) | P3 | D20 | Pandas, claves y ventanas |
| [H04](03_EJERCICIOS/Comprension/H04.md) | P4 | D24 | el mini-ETL |
| [H05](03_EJERCICIOS/Comprension/H05.md) | P5a | D26 | claves, duplicados y fechas |
| [H06](03_EJERCICIOS/Comprension/H06.md) | P5 | D30 | Gold, cuadre y repetición |
| [H07](03_EJERCICIOS/Comprension/H07.md) | P6 | D33 | BI mínimo |
| [H08](03_EJERCICIOS/Comprension/H08.md) | P7 | D40 | transferencia a un caso nuevo |

Cada hito tiene cuatro partes: **explica** (sin mirar tu código), **predice** (un bloque de código o una tabla pequeña de datos, antes de ejecutar), **variante nueva** (distinta de los ejercicios resueltos) y **justifica** (comparando alternativas). Se da por cumplido con tres de cuatro criterios sostenidos oralmente. El DAX de H07 **no se ejecutó**: la predicción simula el contexto de filtro con Python y la variante pide marcar lo no ejecutado como PENDIENTE.

Estadística: las medidas pedidas aparecen así: media, mediana y moda en 11.3 (D13) y AN08; dispersión, cuartiles y percentiles en 11.4–11.5 (D25) y AN13; cumplimiento en AN04; cobertura y efectividad en 6.2 (D26) y AN14; productividad en 6.4 (D31) y AN15; ABC y Pareto en 6.5 (D19), AN10 y AN11. ST01 y ST02 pasaron a REFUERZO porque esas mismas medidas se practican en las actividades.

## 8. Reparación de la integración y lo que no se tocó

- **P02 y P07**: sus punteros «capítulo 08, ejemplo de cumplimiento» y «capítulo 07, sumar solo entregados» apuntaban a secciones que ya no existen. Ahora citan lecciones concretas (P02: 7.3 y 7.6; P07: 7.12 y 7.13).
- **Otros punteros**: 27 enunciados de Python y 28 de SQL dicen ahora la lección exacta (por ejemplo, groupby era «capítulo 09» y está en 10.2; `drop_duplicates` era «capítulo 10» y está en 9.5). Dos conceptos (`UNION ALL`, vistas temporales) no están en las lecciones y el enunciado lo dice. P01, P03 y los ejercicios S1, S2, S7, S9, S10 de D01–D02 conservan su texto porque sus punteros siguen siendo válidos.
- **ST01–ST07**: los criterios de aceptación se imprimían como una lista de Python en una sola línea; ahora son casillas.
- **Guías diarias**: D03–D41 se generan desde `nucleo.json` y `lecciones.json` con las lecciones del día (enlace y minutos), la distribución de bloques, el criterio analítico y la EXTENDIDA. La prueba de sincronización regenera todo en una copia y compara.
- **D01**: sin cambios. **D02**: objetivo, ejercicios y tiempos intactos; se añadió un bloque (marcado con `E2:LECCIONES`) con las lecciones 1.4 y 7.6 (35 min de lectura frente a 30 del bloque «Teoría»; la guía dice qué hacer si no cabe). **`mi_trabajo`**: sin cambios (verificado).
- **Domingos**: descanso por defecto; opcionalmente 45–120 min en **una** opción (recuperar un REFUERZO o una lección EXTENDIDA). D42 avisa que es la víspera de la evaluación final.
- **UAGRM**: `02_TEORIA/UAGRM/LEEME.md` tiene un mapa de las clases 1 y 2 a las lecciones. El temario real lo define el profesor.
- **N1**: `COMPETENCIAS.md` define el perfil N1 (analista junior) con la evidencia de cada competencia.
- **ETL y BI**: la escalera de cinco peldaños (función → tabla → leer un error → mini-ETL → ETL guiado y C06) no cambió; sí cambió el orden de lectura (ver sección 6). BI queda como estaba, con alcance mínimo (Excel D31, Power BI D32–D33); sus lecciones PROFUNDIZACIÓN (14.2, 14.4, 14.5, 13.3) están en EXTENDIDA.

**Incidente corregido.** Al escribir la clase de cada lección en los índices de capítulo, mi primer script dañó tres celdas: las columnas «Tiempo» de los capítulos 1–4 (que sólo tenían cuatro columnas) y dos celdas de «Qué aprendes» con la barra escapada `\|`. Lo detecté con el verificador, recalculé los tiempos desde los encabezados de las lecciones, restauré la celda 2.4 tal como era y **reescribí la celda de 9.4** (`loc`/`iloc`, máscaras, `&` y `\|`, `isin`, `str.contains`, `sort_values`) porque su texto original se había perdido; las lecciones no se afectaron. Ahora el índice se genera con un procedimiento que respeta las barras escapadas.

## 9. Archivos

**Nuevos**: `01_PLAN_DIARIO/lecciones.json`, `01_PLAN_DIARIO/RUTAS.md` (generado), `03_EJERCICIOS/Analitico/AN01–AN18.md`, `03_EJERCICIOS/Comprension/H01–H08.md`, `08_SOLUCIONES/controles_analitico.json` y `.md`, `herramientas/verificar_etapa2.py`, este informe.

**Modificados**: `herramientas/aplicar_nucleo.py` (genera lecciones, bloques, criterio, EXTENDIDA, domingos, RUTAS, CARGA e índices de capítulo), `01_PLAN_DIARIO/nucleo.json`, `calendario.json/csv`, `CARGA_ESTIMADA.md`, `PLAN_V5.md`, `COMPETENCIAS.md`, `HITOS_Y_RECUPERACION.md`, las guías D02–D42, los 18 índices de capítulo y `INDICE.md`, `UAGRM/LEEME.md`, 27 enunciados de Python, 28 de SQL (sólo la línea de lectura o la pista), ST01–ST07 (formato), `README.md`, `herramientas/crear_espacio.py` (carpetas `analitico` y `hitos` para tu espacio, que no se crearon en `mi_trabajo`), `herramientas/verificar_paquete.py` (grupo nuevo) y `PROGRESO_FASE2.md`. El manifiesto SHA256 se regeneró.

## 10. Decisiones que necesito de ti

1. **Horas.** ¿Aceptas BASE = 15 h planificadas y ≈ 16,5 h estimadas de primera vez (semanas 3–5 ≈ 17 h), con REDUCIDO y corrimiento de puertas como válvula? Si prefieres acercarte a 15,5 h estimadas, habría que mover a REFUERZO unos 60–80 min por semana en las semanas 3–5; los candidatos son ejercicios que S03/S05 evalúan (por ejemplo P22 o P23, K1, E4), lo que exige ajustar esos exámenes: es trabajo de la Etapa 3. No lo hice por mi cuenta porque cambia lo que evalúa cada puerta.
2. **Prerrequisitos recomendados.** ¿Dejas las 17 lecturas como recomendadas o quieres alguna como NÚCLEO (más lectura, semana más densa)?
3. **ST01 y ST02** pasaron a REFUERZO. ¿Prefieres que alguno vuelva a ser obligatorio?
4. **Exámenes y evaluación final**: sin cambios hasta que digas «AUTORIZO ETAPA 3».

## 11. Pruebas ejecutadas (Python 3.12.10 y pandas 2.2.3 del `.venv`)

- `herramientas/verificar_etapa2.py`: **9 de 9 grupos** (lecciones, jornadas, guías, prerrequisitos, ejercicios y lecciones, actividades con **42 cifras de control recalculadas**, documentos, sincronización en copia temporal, D01/`mi_trabajo`). Con **20 mutaciones** (quitar un enlace, mover una lección a un domingo, publicar un resultado en un enunciado, alterar una cifra, restaurar un puntero viejo, citar una lección de PROFUNDIZACIÓN en un OBLIGATORIO, dejar un prerrequisito sin cobertura, etc.) el verificador detectó las **20**.
- `herramientas/verificar_teoria.py`: 7 de 7 grupos (620 bloques ejecutados), tras actualizar los índices.
- `herramientas/auditar_enunciados.py`: 6 de 6 grupos, 0 problemas (dependencias y exámenes alineados con el nuevo calendario).
- `herramientas/verificar_paquete.py` en copia temporal: **21 de 21 pruebas OK** (la 21.ª es el grupo nuevo de la Etapa 2), con el manifiesto regenerado.
- Aviso del verificador: D17 (1,30) y D25 (1,27) son las jornadas más ajustadas; las semanas 3, 4 y 5 estiman más de 1,1 veces el plan.

**Nota sobre el entorno.** El `python` del sistema de esta máquina es 3.14 con pandas 3.0.3, distinto del `.venv` (3.12.10, pandas 2.2.3). Todas las comprobaciones de este informe se corrieron con el del `.venv`; si ejecutas algo con otro intérprete, los ejemplos de Pandas pueden imprimir tipos distintos.

## 12. Limitaciones

- Los tiempos son estimaciones de «primera vez»; ninguna fue medida con tus datos reales todavía.
- El código DAX/M, los pasos de Power BI Desktop y de Excel **no se ejecutaron**; H07 y las lecciones lo declaran.
- Los `AN` no tienen corrector: dependen de que contrastes tu razonamiento con la rúbrica y el control; los hitos exigen sostener la explicación oralmente, algo que ningún archivo puede comprobar por ti.
- Los datos de las actividades salen de la base comercial y de las referencias del paquete; no se probaron con datos de una empresa real.
- El mapa UAGRM se basa en los archivos aportados; el temario real lo define la clase.

## 13. Siguiente paso

Revisa este informe y `01_PLAN_DIARIO/RUTAS.md`. **Me detengo aquí.** La Etapa 3 (mejorar los exámenes S01–S06, rediseñar la evaluación final, validación completa e `INFORME_FASE2_FINAL.md`) no se empieza sin la frase exacta **«AUTORIZO ETAPA 3»**.
