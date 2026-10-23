# Plan Data & BI v5 (revisión pedagógica v6)

Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json`, salvo las casillas, que son tuyas y se conservan.

**Formación: 12 de octubre–22 de noviembre de 2026 (42 jornadas). Evaluación final: 23–30 de noviembre, un bloque posterior de 9,5 horas que no forma parte de las 42 jornadas.** Las 42 jornadas suman **157 h 32 min de trabajo BASE** (promedio de martes a viernes: 310 min); no son 90 horas ni 15 horas semanales. Detalle en [Carga estimada](CARGA_ESTIMADA.md).

El punto de partida es una pasantía de BI con fuerte apoyo de IA y bases técnicas todavía en construcción. El objetivo es resolver SQL, programar Python y construir un ETL junior propio, comprobado y explicable, y llegar preparado para postular a puestos de Analista de Datos, BI y Data Engineering. El programa no garantiza empleo ni autonomía profesional avanzada en seis semanas.

**Revisión pedagógica v6:** la teoría necesaria se lee **antes** de los ejercicios de cada jornada; la práctica BASE (SQL, Python, Pandas, estadística, ETL y BI) se agrupa por competencia y dificultad; el SQL se retoma con frecuencia mediante variantes breves; el REFUERZO es voluntario, diferente de lo obligatorio y sin teoría nueva; las jornadas que superan su máximo se dividen en sesiones retomables; no existe una ruta EXTENDIDA. Los exámenes S01–S06, sus contratos y puntuaciones, y las 42 fechas no cambian.

## Carga y modalidades

Las clases UAGRM del lunes (19:30–22:00) van aparte. Comienza habitualmente a las 13:00 y añade descansos de diez minutos cada 45–50 minutos; son pausas, no actividades pendientes.

| Día | COMPLETO (BASE) | REDUCIDO | MÍNIMO |
|---|---|---|---|
| Lunes | 150 min o menos de objetivo; algunas jornadas lo superan y se dividen en sesiones | ≈ 60 min de lo primero de la guía | 20 min |
| Martes a viernes | objetivo 240 min, máximo 270; las jornadas con más carga se dividen en sesiones retomables | ≈ 60 min | 20 min |
| Sábado | examen (115 min) más hito o criterio, empleo y cierre: 180–185 min | evaluación sin corrección (60 min) | 20 min |
| Domingo | descanso (0 min obligatorios) | descanso | descanso |

Las modalidades son alternativas de la misma jornada. REDUCIDO no es el mismo ejercicio con menos minutos: es una sesión corta con lo primero de la guía, y lo que no hagas sigue pendiente (nunca pasa a REFUERZO ni se suma a otra jornada). MÍNIMO: quince minutos de práctica ya conocida y cinco de cierre; no acredita contenidos nuevos ni cumple puertas. Si necesitas descansar, el descanso reemplaza la sesión. Un domingo no requiere consulta, publicación ni commit; si tienes energía puedes usar **45–120 minutos voluntarios** en una sola opción.

## Estructura de cada jornada

A. Qué estudiar (todas las lecciones NÚCLEO, antes de cualquier ejercicio) · B. Distribución neta (y sesiones retomables si hace falta) · C. Práctica y archivos (todos los obligatorios, por competencia y dificultad) · D. REFUERZO voluntario · E. Comprobar y entregar · F. REDUCIDO · G. MÍNIMO · H. Empleo y clase. Los sábados de examen y los domingos tienen una estructura propia. Más detalle: [Rutas de estudio](RUTAS.md), [Competencias y puertas](COMPETENCIAS.md) y [Hitos y recuperación](HITOS_Y_RECUPERACION.md).

## Método de estudio y prioridad

Teoría breve → ejemplo explicado → micropráctica → práctica autónoma → validación → reflexión. Predice el resultado antes de ejecutar. Intenta diez minutos, comprueba, depura otros diez y recién pide una pista. Consulta la solución después del intento y explica la diferencia con tu código. De martes a viernes hay una actividad de criterio analítico (`03_EJERCICIOS/Analitico/`) y cada puerta exige un hito de comprensión.

## Empleo

D01–D05: CV y GitHub (sin postulaciones obligatorias). D08–D10: CV final, vacantes pertinentes y primeras candidaturas preparadas. **D11: primera postulación real** si hay CV y vacante pertinente. Después, seguimiento y hasta dos postulaciones de calidad por semana. LinkedIn: publica solo entregables terminados y verificados, nunca por calendario; no inventes experiencia.

## Progresión

| Semana | Fechas | Resultado verificable | BASE |
|---:|---|---|---:|
| 1 | 12–18 octubre | Filtros, agregación, Python básico, KPIs y S01 (Puerta 1) | 24 h 40 min |
| 2 | 19–25 octubre | JOIN, funciones con errores, archivos CSV, estadística descriptiva inicial y S02 (Puerta 2) | 27 h 04 min |
| 3 | 26 octubre–1 noviembre | Pandas, merge validado, duplicados, CTE, ventanas, ABC y S03 (Puerta 3) | 25 h 42 min |
| 4 | 2–8 noviembre | Mini-ETL y ETL guiado hasta claves y duplicados; S04 (Puerta 5a) | 26 h 35 min |
| 5 | 9–15 noviembre | ETL guiado completo, modelo estrella, Excel y Power BI mínimo; S05 (Puerta 6) | 26 h 46 min |
| 6 | 16–22 noviembre | Estadística inferencial y caso nuevo C06 en cinco bloques; S06 (Puerta 7) | 26 h 45 min |

## Registro diario

Marca el día cuando completaste su objetivo y puedes explicar el control. Registra modalidad, minutos reales, ayuda utilizada y siguiente base en `mi_trabajo/progreso.csv`; anota errores en `mi_trabajo/errores.md`. Guarda consultas, scripts y explicaciones propios en GitHub; los borradores y referencias no prueban aprendizaje.

## Jornadas

### Semana 1

- [ ] **D01 · 12/10 lunes:** [Entorno · filas/columnas · variables · función](dias/D01_2026-10-12.md) · BASE 151 min.
- [ ] **D02 · 13/10 martes:** [WHERE/NULL/DISTINCT · texto · booleanos y decisiones](dias/D02_2026-10-13.md) · BASE 278 min en 2 sesiones · REFUERZO ≤ 43 min.
- [ ] **D03 · 14/10 miércoles:** [Listas · diccionarios · ORDER/LIMIT](dias/D03_2026-10-14.md) · BASE 249 min · REFUERZO ≤ 60 min.
- [ ] **D04 · 15/10 jueves:** [Agregados · bucles · acumuladores](dias/D04_2026-10-15.md) · BASE 321 min en 2 sesiones · REFUERZO ≤ 50 min.
- [ ] **D05 · 16/10 viernes:** [GROUP BY/HAVING · denominadores · registros · Git](dias/D05_2026-10-16.md) · BASE 296 min en 2 sesiones · REFUERZO ≤ 25 min.
- [ ] **D06 · 17/10 sábado:** [EXAMEN S01](dias/D06_2026-10-17.md) · BASE 185 min.
- [ ] **D07 · 18/10 domingo:** [Descanso (0 min obligatorios)](dias/D07_2026-10-18.md) · descanso (0 min obligatorios).
- [ ] Hito semana 1: examen S01 corregido y Puerta 1 evaluada (decisión de continuidad registrada).

### Semana 2

- [ ] **D08 · 19/10 lunes:** [Conversiones · errores de valor · contratos](dias/D08_2026-10-19.md) · BASE 153 min · REFUERZO ≤ 50 min.
- [ ] **D09 · 20/10 martes:** [Claves · INNER JOIN · excepciones · traceback](dias/D09_2026-10-20.md) · BASE 327 min en 2 sesiones · REFUERZO ≤ 60 min.
- [ ] **D10 · 21/10 miércoles:** [CSV · módulos · portafolio GitHub](dias/D10_2026-10-21.md) · BASE 327 min en 2 sesiones · REFUERZO ≤ 73 min.
- [ ] **D11 · 22/10 jueves:** [LEFT JOIN · JOIN que duplica · fechas · variables · depuración](dias/D11_2026-10-22.md) · BASE 308 min en 2 sesiones · REFUERZO ≤ 75 min.
- [ ] **D12 · 23/10 viernes:** [KPI · frecuencias · pruebas · fechas y cantidades](dias/D12_2026-10-23.md) · BASE 324 min en 2 sesiones · REFUERZO ≤ 100 min.
- [ ] **D13 · 24/10 sábado:** [EXAMEN S02](dias/D13_2026-10-24.md) · BASE 185 min.
- [ ] **D14 · 25/10 domingo:** [Descanso (0 min obligatorios)](dias/D14_2026-10-25.md) · descanso (0 min obligatorios).
- [ ] Hito semana 2: examen S02 corregido y Puerta 2 evaluada (decisión de continuidad registrada).

### Semana 3

- [ ] **D15 · 26/10 lunes:** [Primer DataFrame · perfilado](dias/D15_2026-10-26.md) · BASE 160 min en 2 sesiones · REFUERZO ≤ 45 min.
- [ ] **D16 · 27/10 martes:** [Nulos/duplicados · drop size](dias/D16_2026-10-27.md) · BASE 265 min · REFUERZO ≤ 100 min.
- [ ] **D17 · 28/10 miércoles:** [groupby · merge · filtros · CASE](dias/D17_2026-10-28.md) · BASE 325 min en 2 sesiones · REFUERZO ≤ 88 min.
- [ ] **D18 · 29/10 jueves:** [Subconsulta · CTE · ventanas · media/mediana](dias/D18_2026-10-29.md) · BASE 310 min en 2 sesiones · REFUERZO ≤ 100 min.
- [ ] **D19 · 30/10 viernes:** [ABC · controles Pandas · dispersión · pruebas](dias/D19_2026-10-30.md) · BASE 297 min en 2 sesiones · REFUERZO ≤ 77 min.
- [ ] **D20 · 31/10 sábado:** [EXAMEN S03](dias/D20_2026-10-31.md) · BASE 185 min.
- [ ] **D21 · 01/11 domingo:** [Descanso (0 min obligatorios)](dias/D21_2026-11-01.md) · descanso (0 min obligatorios).
- [ ] Hito semana 3: examen S03 corregido y Puerta 3 evaluada (decisión de continuidad registrada).

### Semana 4

- [ ] **D22 · 02/11 lunes:** [ETL/ELT · capas · mini-ETL (1)](dias/D22_2026-11-02.md) · BASE 165 min en 2 sesiones · REFUERZO ≤ 48 min.
- [ ] **D23 · 03/11 martes:** [Contrato · estructura ETL · fechas/dinero · mini-ETL (2)](dias/D23_2026-11-03.md) · BASE 300 min en 2 sesiones · REFUERZO ≤ 99 min.
- [ ] **D24 · 04/11 miércoles:** [Rechazos · carga SQLite · mini-ETL (3)](dias/D24_2026-11-04.md) · BASE 300 min en 2 sesiones · REFUERZO ≤ 92 min.
- [ ] **D25 · 05/11 jueves:** [Cumplimiento · productividad · percentiles · ETL-1](dias/D25_2026-11-05.md) · BASE 325 min en 2 sesiones · REFUERZO ≤ 70 min.
- [ ] **D26 · 06/11 viernes:** [Hechos/dimensiones · errores silenciosos · ETL-2/3](dias/D26_2026-11-06.md) · BASE 340 min en 2 sesiones · REFUERZO ≤ 75 min.
- [ ] **D27 · 07/11 sábado:** [EXAMEN S04](dias/D27_2026-11-07.md) · BASE 165 min.
- [ ] **D28 · 08/11 domingo:** [Descanso (0 min obligatorios)](dias/D28_2026-11-08.md) · descanso (0 min obligatorios).
- [ ] Hito semana 4: mini-ETL defendido y checkpoint S04 (Puerta 5a) registrados (decisión de continuidad registrada).

### Semana 5

- [ ] **D29 · 09/11 lunes:** [Modelo estrella · ETL-4 · productividad](dias/D29_2026-11-09.md) · BASE 160 min en 2 sesiones · REFUERZO ≤ 42 min.
- [ ] **D30 · 10/11 martes:** [Power BI (flujo) · Excel (tabla) · ETL-5/6](dias/D30_2026-11-10.md) · BASE 314 min en 2 sesiones · REFUERZO ≤ 85 min.
- [ ] **D31 · 11/11 miércoles:** [Excel: pivote y fórmulas · Power Query](dias/D31_2026-11-11.md) · BASE 320 min en 2 sesiones · REFUERZO ≤ 87 min.
- [ ] **D32 · 12/11 jueves:** [Fecha · modelo PB · Power Query](dias/D32_2026-11-12.md) · BASE 310 min en 2 sesiones · REFUERZO ≤ 92 min.
- [ ] **D33 · 13/11 viernes:** [DAX/CALCULATE · medidas · panel mínimo](dias/D33_2026-11-13.md) · BASE 322 min en 2 sesiones · REFUERZO ≤ 83 min.
- [ ] **D34 · 14/11 sábado:** [EXAMEN S05](dias/D34_2026-11-14.md) · BASE 180 min.
- [ ] **D35 · 15/11 domingo:** [Descanso (0 min obligatorios)](dias/D35_2026-11-15.md) · descanso (0 min obligatorios).
- [ ] Hito semana 5: ETL guiado completo y BI mínimo (Puerta 6) registrados con honestidad (decisión de continuidad registrada).

### Semana 6

- [ ] **D36 · 16/11 lunes:** [Caso C06 (0) · muestreo](dias/D36_2026-11-16.md) · BASE 150 min · REFUERZO ≤ 48 min.
- [ ] **D37 · 17/11 martes:** [C06 (1) · intervalos de confianza · errores silenciosos](dias/D37_2026-11-17.md) · BASE 330 min en 2 sesiones · REFUERZO ≤ 42 min.
- [ ] **D38 · 18/11 miércoles:** [C06 (2) · hipótesis · p-valor · interpretar](dias/D38_2026-11-18.md) · BASE 335 min en 2 sesiones · REFUERZO ≤ 100 min.
- [ ] **D39 · 19/11 jueves:** [C06 (3) · Welch · ST05](dias/D39_2026-11-19.md) · BASE 330 min en 2 sesiones · REFUERZO ≤ 52 min.
- [ ] **D40 · 20/11 viernes:** [C06 (4) · README · entrevistas · ST07](dias/D40_2026-11-20.md) · BASE 295 min en 2 sesiones · REFUERZO ≤ 87 min.
- [ ] **D41 · 21/11 sábado:** [EXAMEN S06](dias/D41_2026-11-21.md) · BASE 165 min.
- [ ] **D42 · 22/11 domingo:** [Descanso (0 min obligatorios)](dias/D42_2026-11-22.md) · descanso (0 min obligatorios).
- [ ] Hito semana 6: C06 y examen S06 (Puerta 7) registrados (decisión de continuidad registrada).

## Evaluación final

- [ ] 23 de noviembre: Contrato propio y perfil de los datos nuevos (despachos de una ferretería mayorista).
- [ ] 24 de noviembre: Funciones adaptadas a las reglas nuevas, pruebas de formatos y Bronze.
- [ ] 25 de noviembre: Silver con clave compuesta, catálogo, rechazos y cuadre de conteos.
- [ ] 26 de noviembre: Gold por sucursal, mes y línea; SQLite y validación previa a publicar.
- [ ] 27 de noviembre: SQL independiente, segunda ejecución y cuatro entradas adversas.
- [ ] 28 de noviembre: README, informe de KPIs con tabla o gráfico, hallazgos y ensayo de la defensa.
- [ ] 29 de noviembre: Descanso.
- [ ] 30 de noviembre: Defensa con observador (decisiones, predicción, reparación y modificación en vivo), corrector y rúbrica.

**Carga:** 570 minutos netos (9,5 h) en un bloque posterior y explícito, que no forma parte de las 42 jornadas. La evaluación final solo se toma si la Puerta 7 está cumplida; si no, se reprograma sin acumular horas y no se declara autonomía.

Guía completa: [Evaluación final](../09_EVALUACION_FINAL/ENUNCIADO.md). La habilidad se acredita con trabajo propio, cuadres y explicación; si falta una puerta crítica, registra la limitación y refuerza dos bases antes de una nueva variante.
