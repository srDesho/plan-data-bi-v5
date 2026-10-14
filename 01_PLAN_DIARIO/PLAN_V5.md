# Plan Data & BI v 5

**Formación: 12 de octubre–22 de noviembre de 2026 (42 jornadas, 90 horas de plan). Evaluación final: 23–30 de noviembre, un bloque posterior de 9,5 horas que no está incluido en las 90.**

El punto de partida es una pasantía de BI con fuerte apoyo de IA y bases técnicas todavía en construcción.
El objetivo es resolver SQL, programar Python y construir un ETL junior propio, comprobado y explicable.
El programa no garantiza empleo ni autonomía profesional avanzada en seis semanas.

**Revisión 5.1 (tras la auditoría):** cada jornada separa ejercicios OBLIGATORIOS, REFUERZO y OPCIONALES, el avance depende de puertas de competencia ([Competencias y puertas](COMPETENCIAS.md)) y se añadieron un mini-ETL y tres ejercicios de depuración antes del ETL grande. Las fechas son objetivos, no plazos. D01 y D02 no cambiaron.

**Revisión 5.2 (Fase 2, Etapa 2):** las 100 lecciones de la teoría están clasificadas (NÚCLEO, REFUERZO y PROFUNDIZACIÓN) y las lecciones NÚCLEO tienen día; el bloque de aprendizaje de cada jornada se reparte entre lecciones, SQL, práctica y criterio analítico; cada puerta exige un hito de comprensión; la ruta EXTENDIDA es voluntaria y los domingos son flexibles. Siguen vigentes el Plan v5, sus 42 jornadas y sus fechas. D01 no cambió y D02 solo recibió un bloque de lecciones. Detalle: [Rutas BASE y EXTENDIDA](RUTAS.md).

**Revisión 5.3 (Fase 2, Etapa 3):** los validadores revisan filas, claves y agrupaciones (no solo totales); cada jornada declara qué se exige al entrar y define su modo REDUCIDO como una entrega menor; los exámenes S01–S06 muestran competencia → preparación → evidencia → puntos, con variantes y diagnósticos; los hitos exigen la variante y la explicación; la evaluación final usa un contrato nuevo y es un bloque posterior de 9,5 h fuera de las 90 horas. Siguen vigentes el Plan v5, sus 42 jornadas y sus fechas.

## Carga y modalidades

15 horas semanales netas: **900 minutos**, incluyendo empleo, entrevistas y documentación.
Las clases UAGRM del lunes, 19:30–22:00, van aparte. Comienza habitualmente a las 13:00.
Añade descansos de diez minutos cada 45–50 minutos; son pausas, no actividades pendientes.

| Día | COMPLETO | REDUCIDO | MÍNIMO |
|---|---:|---:|---:|
| Lunes |90 min|45 min|20 min|
| Martes |160 min|60 min|20 min|
| Miércoles |150 min|60 min|20 min|
| Jueves |150 min|60 min|20 min|
| Viernes |150 min|60 min|20 min|
| Sábado |200 min|60 min|20 min|
| Domingo |Descanso (0 min obligatorios)|Descanso|Descanso|

Las modalidades son alternativas de la misma jornada. REDUCIDO no es el mismo ejercicio con menos minutos: cada guía define una lectura mínima y una **entrega menor y realizable** con la preparación que necesita, y dice qué pasa a REFUERZO. MÍNIMO: quince minutos de práctica ya conocida (una consulta o una función que ya resolviste) y cinco de
validación/reflexión. No acredita contenidos nuevos ni cumple puertas. Si necesitas descansar, el descanso reemplaza la sesión.
Un domingo no requiere consulta, publicación ni commit. Si tienes energía puedes usar **45–120 minutos voluntarios** en una sola opción (recuperación de un REFUERZO o una lección de EXTENDIDA); si no, descansas. No se genera una deuda de horas.

## Rutas BASE y EXTENDIDA

Las 100 lecciones de `02_TEORIA` suman unas 91 horas y no caben en seis semanas junto con los ejercicios. Cada lección está clasificada como **NÚCLEO** (indispensable; su lectura cuenta dentro de las 15 horas y tiene día), **REFUERZO** (se lee si una competencia no está dominada) o **PROFUNDIZACIÓN** (EXTENDIDA u otros periodos); todas permanecen como material de consulta. La guía de cada día lista las lecciones NÚCLEO del día y los minutos de lectura; el bloque de aprendizaje se reparte entre **Lecciones**, **SQL**, **Práctica** y **Criterio**.

- **BASE:** 900 minutos por semana (15 horas), con la estimación de primera vez en [Carga estimada](CARGA_ESTIMADA.md). Si una semana no cabe, usa REDUCIDO y mueve la puerta sin acumular horas.
- **EXTENDIDA:** BASE más hasta 30–75 minutos voluntarios por jornada (lunes a sábado) y un domingo opcional de 45–120 minutos: entre 20 y 25 horas por semana. Nunca es obligatoria.
- Detalle completo (42 jornadas, teoría obligatoria frente a práctica, horas por semana y prerrequisitos): [Rutas BASE y EXTENDIDA](RUTAS.md).

## Criterio analítico y comprensión

Calcular no basta: debes entender qué significa cada indicador y cuándo usarlo. De martes a viernes hay una actividad de **criterio analítico** de 15 minutos (`03_EJERCICIOS/Analitico/`): definir el problema de negocio, elegir el KPI, comparar resultados, analizar tendencias, reconocer datos insuficientes, separar hechos de hipótesis y redactar recomendaciones a gerencia; incluye media, mediana, moda, dispersión, percentiles, cuartiles, ABC, cumplimiento, cobertura, efectividad y productividad. Cada puerta exige además un **hito de comprensión** (`03_EJERCICIOS/Comprension/`): explicar, predecir un resultado, resolver una variante nueva y justificar una decisión, sin copiar soluciones.

## Método de estudio y prioridad

Teoría breve → ejemplo explicado → práctica guiada → práctica autónoma → validación → reflexión.
Predice el resultado antes de ejecutar. Intenta diez minutos, comprueba, depura otros diez y recién pide una pista.
Consulta la solución después del intento y explica la diferencia con tu código.

La guía diaria clasifica cada ejercicio: **OBLIGATORIO** (núcleo del día), **REPASO** (SQL ya hecho, de memoria), **REFUERZO** (si la puerta falló o sobra tiempo)
y **OPCIONAL** (nunca desplaza lo obligatorio). Los notebooks muestran ejemplos guiados y no añaden una sesión completa.
La estimación de lo obligatorio está en [Carga estimada](CARGA_ESTIMADA.md). Al llegar al tiempo, guarda el punto y recorta REFUERZO y OPCIONAL, sin prolongar la jornada.
Los sábados prioriza el examen y su corrección; las consultas listadas son repaso.

Si una puerta no se cumple, reemplaza el siguiente bloque práctico por recuperación de esa base y mueve la secuencia completa. No dupliques jornadas ni acumules horas.
La fecha ordena el material; avanzar de nivel exige comprender las funciones, las claves y los cuadres anteriores.
Lee [Hitos y recuperación](HITOS_Y_RECUPERACION.md) y [Competencias y puertas](COMPETENCIAS.md).

## Progresión

| Semana | Fechas | Resultado verificable | Horas |
|---|---|---|---:|
|1|12–18 octubre|Filtros/agregación, Python básico, KPIs, CV inicial y S01 (Puerta 1)|15|
|2|19–25 octubre|JOIN, funciones con errores, archivos CSV, media/mediana/moda y S02 (Puerta 2)|15|
|3|26 octubre–1 noviembre|Primer DataFrame, merge validado, duplicados y perfilado; CTE, ventanas y ABC; S03 (Puerta 3)|15|
|4|2–8 noviembre|Mini-ETL (Puerta 4) y ETL guiado desde el contrato hasta claves y duplicados; checkpoint S04 (Puerta 5a)|15|
|5|9–15 noviembre|ETL guiado completo (Puerta 5); Excel y Power BI en alcance mínimo (Puerta 6); S05|15|
|6|16–22 noviembre|Caso nuevo C06 en cinco bloques, defensa y S06 (Puerta 7)|15|

Postulaciones desde el jueves 15 de octubre: una el jueves y hasta dos el sábado, si hay puestos pertinentes.
LinkedIn: dos publicaciones semanales, miércoles y viernes, solo con evidencia propia. La tercera es opcional y
reemplaza tiempo de ampliación. CV y entrevistas se preparan desde las primeras semanas, sin inventar experiencia.

## Registro diario

Marca el día cuando completaste su objetivo y puedes explicar el control. Registra modalidad, minutos reales,
ayuda utilizada y siguiente base en `mi_trabajo/progreso.csv`; anota errores en `mi_trabajo/errores.md`.
Guarda consultas, scripts y explicaciones propios en GitHub; los borradores y referencias no prueban aprendizaje.

## Jornadas


### Semana 1


- [ ] **D01 · 12/10 lunes:** [Entorno, filas y variables](dias/D01_2026-10-12.md) · C 90 / R 45 / M 20 min.

- [ ] **D02 · 13/10 martes:** [Filtros, NULL y texto](dias/D02_2026-10-13.md) · C 160 / R 60 / M 20 min.

- [ ] **D03 · 14/10 miércoles:** [Listas, diccionarios y clientes únicos](dias/D03_2026-10-14.md) · C 150 / R 60 / M 20 min.

- [ ] **D04 · 15/10 jueves:** [Agrupación, bucles y media/mediana](dias/D04_2026-10-15.md) · C 150 / R 60 / M 20 min.

- [ ] **D05 · 16/10 viernes:** [Condiciones, funciones cortas y KPIs](dias/D05_2026-10-16.md) · C 150 / R 60 / M 20 min.

- [ ] **D06 · 17/10 sábado:** [Primer examen y cierre de fundamentos](dias/D06_2026-10-17.md) · C 200 / R 60 / M 20 min.

- [ ] **D07 · 18/10 domingo:** [Descanso real](dias/D07_2026-10-18.md) · C 0 / R 0 / M 0 min.


- [ ] Hito semana 1: examen S01 corregido y Puerta 1 evaluada (decisión de continuidad registrada).


### Semana 2


- [ ] **D08 · 19/10 lunes:** [Funciones con contrato y condiciones](dias/D08_2026-10-19.md) · C 90 / R 45 / M 20 min.

- [ ] **D09 · 20/10 martes:** [Primer JOIN y errores visibles](dias/D09_2026-10-20.md) · C 160 / R 60 / M 20 min.

- [ ] **D10 · 21/10 miércoles:** [Funciones que convierten y archivos CSV](dias/D10_2026-10-21.md) · C 150 / R 60 / M 20 min.

- [ ] **D11 · 22/10 jueves:** [Ausencia con LEFT JOIN](dias/D11_2026-10-22.md) · C 150 / R 60 / M 20 min.

- [ ] **D12 · 23/10 viernes:** [Fechas, cantidades y leer un error](dias/D12_2026-10-23.md) · C 150 / R 60 / M 20 min.

- [ ] **D13 · 24/10 sábado:** [Examen de JOIN y conciliación](dias/D13_2026-10-24.md) · C 200 / R 60 / M 20 min.

- [ ] **D14 · 25/10 domingo:** [Descanso real](dias/D14_2026-10-25.md) · C 0 / R 0 / M 0 min.


- [ ] Hito semana 2: examen S02 corregido y Puerta 2 evaluada (decisión de continuidad registrada).


### Semana 3


- [ ] **D15 · 26/10 lunes:** [Primer DataFrame y perfilado](dias/D15_2026-10-26.md) · C 90 / R 45 / M 20 min.

- [ ] **D16 · 27/10 martes:** [Duplicados exactos y drop size](dias/D16_2026-10-27.md) · C 160 / R 60 / M 20 min.

- [ ] **D17 · 28/10 miércoles:** [Agrupar y unir con validación](dias/D17_2026-10-28.md) · C 150 / R 60 / M 20 min.

- [ ] **D18 · 29/10 jueves:** [CTE y concentración de ventas](dias/D18_2026-10-29.md) · C 150 / R 60 / M 20 min.

- [ ] **D19 · 30/10 viernes:** [ABC, perfilado y criterio](dias/D19_2026-10-30.md) · C 150 / R 60 / M 20 min.

- [ ] **D20 · 31/10 sábado:** [Examen Pandas y SQL intermedio](dias/D20_2026-10-31.md) · C 200 / R 60 / M 20 min.

- [ ] **D21 · 01/11 domingo:** [Descanso real](dias/D21_2026-11-01.md) · C 0 / R 0 / M 0 min.


- [ ] Hito semana 3: examen S03 corregido y Puerta 3 evaluada (decisión de continuidad registrada).


### Semana 4


- [ ] **D22 · 02/11 lunes:** [Mini-ETL (1): extraer y perfilar](dias/D22_2026-11-02.md) · C 90 / R 45 / M 20 min.

- [ ] **D23 · 03/11 martes:** [Mini-ETL (2): transformar con reglas y rechazos](dias/D23_2026-11-03.md) · C 160 / R 60 / M 20 min.

- [ ] **D24 · 04/11 miércoles:** [Mini-ETL (3): validar, cuadrar y cargar](dias/D24_2026-11-04.md) · C 150 / R 60 / M 20 min.

- [ ] **D25 · 05/11 jueves:** [ETL guiado (1): contrato, Bronze y texto](dias/D25_2026-11-05.md) · C 150 / R 60 / M 20 min.

- [ ] **D26 · 06/11 viernes:** [ETL guiado (2): fechas, cantidad, claves y duplicados](dias/D26_2026-11-06.md) · C 150 / R 60 / M 20 min.

- [ ] **D27 · 07/11 sábado:** [Examen S04: mini-ETL y ETL hasta claves](dias/D27_2026-11-07.md) · C 200 / R 60 / M 20 min.

- [ ] **D28 · 08/11 domingo:** [Descanso real](dias/D28_2026-11-08.md) · C 0 / R 0 / M 0 min.


- [ ] Hito semana 4: mini-ETL aprobado (Puerta 4) y checkpoint S04 (Puerta 5a) registrados.


### Semana 5


- [ ] **D29 · 09/11 lunes:** [ETL guiado (3): Silver, validación y rechazos](dias/D29_2026-11-09.md) · C 90 / R 45 / M 20 min.

- [ ] **D30 · 10/11 martes:** [ETL guiado (4): Gold, carga y cuadre SQL](dias/D30_2026-11-10.md) · C 160 / R 60 / M 20 min.

- [ ] **D31 · 11/11 miércoles:** [Excel: tabla dinámica y cuadre](dias/D31_2026-11-11.md) · C 150 / R 60 / M 20 min.

- [ ] **D32 · 12/11 jueves:** [Power BI (1): importar y relacionar](dias/D32_2026-11-12.md) · C 150 / R 60 / M 20 min.

- [ ] **D33 · 13/11 viernes:** [Power BI (2): primeras medidas](dias/D33_2026-11-13.md) · C 150 / R 60 / M 20 min.

- [ ] **D34 · 14/11 sábado:** [Examen S05: ETL guiado completo y BI mínimo](dias/D34_2026-11-14.md) · C 200 / R 60 / M 20 min.

- [ ] **D35 · 15/11 domingo:** [Descanso real](dias/D35_2026-11-15.md) · C 0 / R 0 / M 0 min.


- [ ] Hito semana 5: ETL guiado completo (Puerta 5) y BI mínimo (Puerta 6) registrados con honestidad.


### Semana 6


- [ ] **D36 · 16/11 lunes:** [Caso nuevo C06 (0): contrato y plan](dias/D36_2026-11-16.md) · C 90 / R 45 / M 20 min.

- [ ] **D37 · 17/11 martes:** [C06 (1): extraer, Bronze y perfil](dias/D37_2026-11-17.md) · C 160 / R 60 / M 20 min.

- [ ] **D38 · 18/11 miércoles:** [C06 (2): Silver y rechazos](dias/D38_2026-11-18.md) · C 150 / R 60 / M 20 min.

- [ ] **D39 · 19/11 jueves:** [C06 (3): Gold y cuadres](dias/D39_2026-11-19.md) · C 150 / R 60 / M 20 min.

- [ ] **D40 · 20/11 viernes:** [C06 (4): SQLite, repetición y README](dias/D40_2026-11-20.md) · C 150 / R 60 / M 20 min.

- [ ] **D41 · 21/11 sábado:** [Examen S06: transferencia C06 y defensa](dias/D41_2026-11-21.md) · C 200 / R 60 / M 20 min.

- [ ] **D42 · 22/11 domingo:** [Descanso real](dias/D42_2026-11-22.md) · C 0 / R 0 / M 0 min.


- [ ] Hito semana 6: C06 y examen S06 (Puerta 7) registrados.



## Evaluación final

- [ ] 23 de noviembre: abrir enunciado y datos nuevos; contrato y perfilado.
- [ ] 24–26: adaptar tus funciones de C06, construir, cargar y conciliar un ETL propio con el contrato nuevo, sin código de IA ni referencias resueltas.
- [ ] 27: SQL independiente, segunda ejecución y entradas adversas.
- [ ] 28: README, informe e interpretación; ensayo de la defensa.
- [ ] 29: descanso.
- [ ] 30: defensa con observador (explicar, anticipar, reparar y modificar en vivo), corrector después de cerrar la entrega y rúbrica de autonomía.

**Carga:** 570 minutos netos (9,5 h), antes 750 (12,5 h); es un bloque posterior y explícito, no parte de las seis semanas ni de las 90 horas (detalle en [Carga estimada](CARGA_ESTIMADA.md)).

Guía completa: [Evaluación final](../09_EVALUACION_FINAL/ENUNCIADO.md). Estas fechas son objetivos: la evaluación final se toma cuando la Puerta 7 está cumplida; si no lo está, se registra la limitación y se refuerzan dos bases, sin declarar autonomía.
La habilidad se acredita con trabajo propio, cuadres y explicación. Si falta una puerta crítica, registra la limitación
y refuerza dos bases antes de una nueva variante; no declares una competencia que todavía no puedes demostrar.
