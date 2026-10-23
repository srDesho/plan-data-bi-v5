# Carga estimada por jornada (ruta BASE)

Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json`; no lo edites a mano.

Estimación de **primera vez** para una persona que todavía depende de ayuda externa. **No es una medición**: los minutos de cada ejercicio son el punto medio del rango «Primera vez» de su enunciado (ya incluye leer, equivocarse, depurar y verificar) y los de lectura vienen de la cabecera de cada lección; el error razonable es de ±35 %. Registra tus minutos reales en `mi_trabajo/progreso.csv` y corrige esta tabla con tus datos.

## Qué cuenta cada columna (sin dobles conteos)

| Columna | Qué incluye |
|---|---|
| **Teoría** | Lectura de las lecciones NÚCLEO del día (o de la parte asignada: sección inicial, resto o completa) |
| **Micro** | Solo los apartados obligatorios de las microprácticas esenciales y la preparación del entorno |
| **Ejerc.** | Ejercicios BASE autónomos y casos (tiempo de primera vez de cada enunciado) |
| **SQL** | SQL de recuperación: variantes breves de SQL ya enseñado |
| **Crit.** | Criterio analítico o hito de comprensión |
| **Emp.** | Empleo (CV, GitHub, postulaciones, seguimiento) |
| **Cierre/Exam.** | Cierre de 10 min; en sábado de examen, examen + corrección + simulacro = 115 min |
| **Techo** | 150 min en lunes (clase UAGRM aparte), 270 en martes–viernes (objetivo 240), sin techo en examen |

El REFUERZO es voluntario y **no** está incluido en el total BASE. La evaluación final (23–30 de noviembre, 570 min en total) es un bloque posterior y tampoco está incluida.

| Día | Fecha | Contenido | Tipo | Teoría | Micro | Ejerc. | SQL | Crit. | Emp. | Cierre/Exam. | **BASE** | Techo | Sesiones | REFUERZO (máx.) |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| D01 | 2026-10-12 | Entorno · filas/columnas · variables · función | lunes | 66 | 0 | 65 | 0 | 0 | 10 | 10 | **151** | 150 | — | 0 |
| D02 | 2026-10-13 | WHERE/NULL/DISTINCT · texto · booleanos y decisiones | normal | 164 | 0 | 84 | 0 | 0 | 20 | 10 | **278** | 270 | 2 | 43 |
| D03 | 2026-10-14 | Listas · diccionarios · ORDER/LIMIT | normal | 70 | 50 | 84 | 0 | 15 | 20 | 10 | **249** | 270 | — | 60 |
| D04 | 2026-10-15 | Agregados · bucles · acumuladores | normal | 88 | 125 | 68 | 0 | 15 | 15 | 10 | **321** | 270 | 2 | 50 |
| D05 | 2026-10-16 | GROUP BY/HAVING · denominadores · registros · Git | normal | 90 | 90 | 76 | 0 | 15 | 15 | 10 | **296** | 270 | 2 | 25 |
| D06 | 2026-10-17 | EXAMEN S01 | examen | 0 | 0 | 0 | 0 | 20 | 40 | 125 | **185** | — | — | 0 |
| D07 | 2026-10-18 | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |
| D08 | 2026-10-19 | Conversiones · errores de valor · contratos | lunes | 50 | 50 | 28 | 0 | 0 | 15 | 10 | **153** | 150 | — | 50 |
| D09 | 2026-10-20 | Claves · INNER JOIN · excepciones · traceback | normal | 110 | 80 | 87 | 0 | 15 | 25 | 10 | **327** | 270 | 2 | 60 |
| D10 | 2026-10-21 | CSV · módulos · portafolio GitHub | normal | 55 | 80 | 127 | 25 | 15 | 15 | 10 | **327** | 270 | 2 | 73 |
| D11 | 2026-10-22 | LEFT JOIN · JOIN que duplica · fechas · variables · depuración | normal | 110 | 95 | 48 | 0 | 15 | 30 | 10 | **308** | 270 | 2 | 75 |
| D12 | 2026-10-23 | KPI · frecuencias · pruebas · fechas y cantidades | normal | 81 | 55 | 103 | 40 | 15 | 20 | 10 | **324** | 270 | 2 | 100 |
| D13 | 2026-10-24 | EXAMEN S02 | examen | 0 | 0 | 0 | 0 | 20 | 40 | 125 | **185** | — | — | 0 |
| D14 | 2026-10-25 | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |
| D15 | 2026-10-26 | Primer DataFrame · perfilado | lunes | 45 | 50 | 30 | 15 | 0 | 10 | 10 | **160** | 150 | 2 | 45 |
| D16 | 2026-10-27 | Nulos/duplicados · drop size | normal | 72 | 70 | 93 | 0 | 0 | 20 | 10 | **265** | 270 | — | 100 |
| D17 | 2026-10-28 | groupby · merge · filtros · CASE | normal | 85 | 100 | 80 | 15 | 15 | 20 | 10 | **325** | 270 | 2 | 88 |
| D18 | 2026-10-29 | Subconsulta · CTE · ventanas · media/mediana | normal | 90 | 85 | 90 | 0 | 15 | 20 | 10 | **310** | 270 | 2 | 100 |
| D19 | 2026-10-30 | ABC · controles Pandas · dispersión · pruebas | normal | 50 | 55 | 132 | 0 | 30 | 20 | 10 | **297** | 270 | 2 | 77 |
| D20 | 2026-10-31 | EXAMEN S03 | examen | 0 | 0 | 0 | 0 | 20 | 40 | 125 | **185** | — | — | 0 |
| D21 | 2026-11-01 | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |
| D22 | 2026-11-02 | ETL/ELT · capas · mini-ETL (1) | lunes | 55 | 15 | 70 | 0 | 0 | 15 | 10 | **165** | 150 | 2 | 48 |
| D23 | 2026-11-03 | Contrato · estructura ETL · fechas/dinero · mini-ETL (2) | normal | 90 | 55 | 90 | 15 | 15 | 25 | 10 | **300** | 270 | 2 | 99 |
| D24 | 2026-11-04 | Rechazos · carga SQLite · mini-ETL (3) | normal | 85 | 55 | 95 | 15 | 20 | 20 | 10 | **300** | 270 | 2 | 92 |
| D25 | 2026-11-05 | Cumplimiento · productividad · percentiles · ETL-1 | normal | 75 | 75 | 130 | 15 | 0 | 20 | 10 | **325** | 270 | 2 | 70 |
| D26 | 2026-11-06 | Hechos/dimensiones · errores silenciosos · ETL-2/3 | normal | 50 | 45 | 180 | 15 | 20 | 20 | 10 | **340** | 270 | 2 | 75 |
| D27 | 2026-11-07 | EXAMEN S04 | examen | 0 | 0 | 0 | 0 | 0 | 40 | 125 | **165** | — | — | 0 |
| D28 | 2026-11-08 | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |
| D29 | 2026-11-09 | Modelo estrella · ETL-4 · productividad | lunes | 30 | 25 | 80 | 0 | 0 | 15 | 10 | **160** | 150 | 2 | 42 |
| D30 | 2026-11-10 | Power BI (flujo) · Excel (tabla) · ETL-5/6 | normal | 59 | 30 | 145 | 30 | 20 | 20 | 10 | **314** | 270 | 2 | 85 |
| D31 | 2026-11-11 | Excel: pivote y fórmulas · Power Query | normal | 80 | 55 | 155 | 0 | 0 | 20 | 10 | **320** | 270 | 2 | 87 |
| D32 | 2026-11-12 | Fecha · modelo PB · Power Query | normal | 45 | 45 | 145 | 15 | 30 | 20 | 10 | **310** | 270 | 2 | 92 |
| D33 | 2026-11-13 | DAX/CALCULATE · medidas · panel mínimo | normal | 77 | 55 | 125 | 15 | 20 | 20 | 10 | **322** | 270 | 2 | 83 |
| D34 | 2026-11-14 | EXAMEN S05 | examen | 0 | 0 | 0 | 0 | 15 | 40 | 125 | **180** | — | — | 0 |
| D35 | 2026-11-15 | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |
| D36 | 2026-11-16 | Caso C06 (0) · muestreo | lunes | 55 | 30 | 40 | 0 | 0 | 15 | 10 | **150** | 150 | — | 48 |
| D37 | 2026-11-17 | C06 (1) · intervalos de confianza · errores silenciosos | normal | 60 | 45 | 165 | 15 | 15 | 20 | 10 | **330** | 270 | 2 | 42 |
| D38 | 2026-11-18 | C06 (2) · hipótesis · p-valor · interpretar | normal | 80 | 55 | 140 | 15 | 15 | 20 | 10 | **335** | 270 | 2 | 100 |
| D39 | 2026-11-19 | C06 (3) · Welch · ST05 | normal | 60 | 35 | 170 | 20 | 15 | 20 | 10 | **330** | 270 | 2 | 52 |
| D40 | 2026-11-20 | C06 (4) · README · entrevistas · ST07 | normal | 50 | 30 | 150 | 15 | 20 | 20 | 10 | **295** | 270 | 2 | 87 |
| D41 | 2026-11-21 | EXAMEN S06 | examen | 0 | 0 | 0 | 0 | 0 | 40 | 125 | **165** | — | — | 0 |
| D42 | 2026-11-22 | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |

## Totales por semana

| Semana | Fechas | BASE (min) | BASE (h) | REFUERZO máx. (min) | Jornadas sobre el máximo |
|---:|---|---:|---:|---:|---:|
| 1 | 12–18 octubre | 1480 | 24,7 | 178 | 3 |
| 2 | 19–25 octubre | 1624 | 27,1 | 358 | 4 |
| 3 | 26 octubre–1 noviembre | 1542 | 25,7 | 410 | 4 |
| 4 | 2–8 noviembre | 1595 | 26,6 | 384 | 5 |
| 5 | 9–15 noviembre | 1606 | 26,8 | 389 | 5 |
| 6 | 16–22 noviembre | 1605 | 26,8 | 329 | 4 |

**Total BASE de las 42 jornadas: 9452 min = 157 h 32 min** (REFUERZO voluntario: hasta 2048 min = 34 h 08 min).

## Por qué el total supera 240 min por día

El plan prioriza una formación estudiable, con teoría antes de la práctica, práctica suficiente de SQL, Python, Pandas y BI y preparación para trabajos de Analista de Datos, BI y Data Engineering. Esa carga completa no cabe en 240 minutos por día: **25 jornadas superan su máximo por más de 4 minutos** (exceso total 1029 min). En cada una, la guía divide el trabajo en **sesiones retomables** con un punto de interrupción y un entregable por sesión, para que no se presente como una sola sentada. Puedes usar más de un día real sin cambiar la fecha académica; si decides no hacerlo, usa REDUCIDO y mueve la puerta sin acumular horas.

## Jornadas sobre su máximo

| Día | BASE | Máximo | Exceso | Sesiones |
|---:|---:|---:|---:|---|
| D02 | 278 | 270 | 8 | D02-S1 (135 min), D02-S2 (143 min) |
| D04 | 321 | 270 | 51 | D04-S1 (153 min), D04-S2 (168 min) |
| D05 | 296 | 270 | 26 | D05-S1 (140 min), D05-S2 (156 min) |
| D09 | 327 | 270 | 57 | D09-S1 (175 min), D09-S2 (152 min) |
| D10 | 327 | 270 | 57 | D10-S1 (160 min), D10-S2 (167 min) |
| D11 | 308 | 270 | 38 | D11-S1 (160 min), D11-S2 (148 min) |
| D12 | 324 | 270 | 54 | D12-S1 (161 min), D12-S2 (163 min) |
| D15 | 160 | 150 | 10 | D15-S1 (70 min), D15-S2 (90 min) |
| D17 | 325 | 270 | 55 | D17-S1 (165 min), D17-S2 (160 min) |
| D18 | 310 | 270 | 40 | D18-S1 (150 min), D18-S2 (160 min) |
| D19 | 297 | 270 | 27 | D19-S1 (177 min), D19-S2 (120 min) |
| D22 | 165 | 150 | 15 | D22-S1 (70 min), D22-S2 (95 min) |
| D23 | 300 | 270 | 30 | D23-S1 (145 min), D23-S2 (155 min) |
| D24 | 300 | 270 | 30 | D24-S1 (155 min), D24-S2 (145 min) |
| D25 | 325 | 270 | 55 | D25-S1 (165 min), D25-S2 (160 min) |
| D26 | 340 | 270 | 70 | D26-S1 (175 min), D26-S2 (165 min) |
| D29 | 160 | 150 | 10 | D29-S1 (85 min), D29-S2 (75 min) |
| D30 | 314 | 270 | 44 | D30-S1 (159 min), D30-S2 (155 min) |
| D31 | 320 | 270 | 50 | D31-S1 (175 min), D31-S2 (145 min) |
| D32 | 310 | 270 | 40 | D32-S1 (155 min), D32-S2 (155 min) |
| D33 | 322 | 270 | 52 | D33-S1 (147 min), D33-S2 (175 min) |
| D37 | 330 | 270 | 60 | D37-S1 (185 min), D37-S2 (145 min) |
| D38 | 335 | 270 | 65 | D38-S1 (180 min), D38-S2 (155 min) |
| D39 | 330 | 270 | 60 | D39-S1 (195 min), D39-S2 (135 min) |
| D40 | 295 | 270 | 25 | D40-S1 (135 min), D40-S2 (160 min) |
