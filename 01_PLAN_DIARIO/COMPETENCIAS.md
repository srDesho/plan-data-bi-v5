# Competencias, puertas y cómo usar BASE / REFUERZO

Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json` y `lecciones.json`; no lo edites a mano.

Esta página reemplaza la idea de «avanzar porque llegó la fecha» por «avanzar porque demostré la base». Las fechas del plan son **objetivos académicos**, no plazos: nada de lo que sigue promete completar todo antes del 30 de noviembre.

## Cómo se clasifica cada actividad

| Etiqueta | Significado | Cuándo se hace |
|---|---|---|
| **Lección NÚCLEO** | Teoría indispensable de la jornada (sección A) | Primero, antes de abrir cualquier ejercicio |
| **Micropráctica esencial** | Solo los apartados obligatorios de la micropráctica de una lección NÚCLEO | Después de la teoría, dentro de la sección C |
| **BASE** (obligatorio, sección C) | Ejercicios y casos del día, agrupados por competencia y de menor a mayor dificultad | Siempre, después de toda la teoría |
| **SQL de recuperación** | Variante breve de SQL ya enseñado (SQ01–SQ17, KP01) | En las jornadas normales, para no olvidar SQL |
| **Criterio / hito** | Actividad de criterio analítico (AN) o hito de comprensión (H) | Dentro de la jornada, antes de cerrar |
| **REFUERZO** (sección D) | Ejercicios **diferentes** de los obligatorios, sobre lo ya enseñado; voluntarios, no suman al tiempo BASE, no enseñan nada nuevo y **no sustituyen** una actividad pendiente | Si una puerta falló, te atascaste o sobra tiempo |
| **REDUCIDO** (sección F) | Sesión corta de ≈ 60 min con lo primero de la jornada | Si ese día no puedes hacer el BASE completo; lo que no hagas sigue pendiente |
| **MÍNIMO** (sección G) | 20 minutos: 15 de práctica ya conocida y 5 de cierre | Para no romper la racha; no acredita contenidos nuevos ni avanza una puerta |

Lo que no hiciste no se suma al día siguiente: un obligatorio pendiente se retoma en el siguiente bloque disponible. Los domingos son descanso (0 min obligatorios); la recuperación voluntaria (45–120 min) nunca es obligatoria.

## Las puertas

Cada puerta describe lo que debes poder demostrar, con evidencia, antes de pasar al bloque siguiente. «Explicar» significa decirlo en voz alta sin leer tu código. Cada documento de examen indica qué base concreta recuperar y qué variante nueva la demuestra (S01–S06 y `08_SOLUCIONES/controles_examenes.md`).

| Puerta | Jornada | Fecha objetivo | Qué demuestras y con qué evidencia |
|---|---|---|---|
| **P1** | D06 | 2026-10-17 | Puerta 1 · Consultar y calcular. Evidencia: S01 con 70/100 o más, el 60 % de cada competencia y sin fallo crítico; explicas numerador y denominador de un KPI; hito de comprensión H01 cumplido (variante resuelta y explicación de tu solución como condiciones necesarias, más dos valoraciones). Si no se cumple, el próximo bloque práctico es REFUERZO de D03–D05 con la variante de recuperación de S01 (no se añade un día). |
| **P2** | D13 | 2026-10-24 | Puerta 2 · Funciones, errores y JOIN. Evidencia: P09–P11 y P13 aprobados; J2 y J5 explicados (INNER frente a LEFT); lees un CSV con el módulo estándar; S02 con 70/100 o más, el 60 % de cada competencia y sin fallo crítico; hito H02 cumplido. Si no se cumple: REFUERZO de D09–D12 antes de empezar Pandas en serio (D15). |
| **P3** | D20 | 2026-10-31 | Puerta 3 · Pandas y calidad de datos. Evidencia: P17 y P21–P23 aprobados; la agrupación por pedido (P20 o su variante en H03) explicada; merge `many_to_one` con `validate` explicado; K1, V3 y V4 correctos; S03 con 75/100 o más y sin fallo crítico; hito H03 cumplido (incluida la variante resuelta y explicada). Si no se cumple, el mini-ETL (D22) se reemplaza por REFUERZO de D16–D19. |
| **P5a** | D27 | 2026-11-07 | Puerta 5a · Checkpoint del ETL. Evidencia: mini-ETL defendido y ETL de la distribuidora hasta claves y duplicados (etapas 1–4 del README del proyecto) con los conteos de control (16.378 filas de origen, 200 duplicados exactos, 301 vendedores recuperados); hito H05 cumplido; S04 con 75/100 o más, el 60 % de cada bloque y sin fallo crítico. Si falta una etapa, se registra y se completa en D29–D30; no se promueve el examen a aprobado. |
| **P6** | D34 | 2026-11-14 | Puerta 6 · BI mínimo. Evidencia: tabla dinámica de Excel que coincide con E4; en Power BI Desktop, las tablas importadas, las relaciones y las tres medidas núcleo de PB03 que coinciden con SQL (o la parte registrada como PENDIENTE si no hay Desktop; no se aprueba lo que no se ejecutó); hito H07 cumplido. S05 puntúa aparte la Parte A (ETL, 56/75, decide la Puerta 5) y la Parte B (BI, 19/25, decide esta puerta); lo no ejecutado puntúa 0. Si no se cumple, el resto de BI pasa a REFUERZO después de la Puerta 7; no retrasa el caso de transferencia. |
| **P7** | D41 | 2026-11-21 | Puerta 7 · Transferencia C06. Evidencia: `validar_final.py --transferencia` correcto después de cerrar tu intento, segunda ejecución igual, prueba de columna ausente / catálogo duplicado / clave en conflicto / cantidad fraccionaria, y defensa de cinco decisiones sin leer (hito H08); S06 con 80/100 y sin puerta crítica. La evaluación final (objetivo 23–30 de noviembre, bloque posterior de 9,5 h, fuera de las 42 jornadas) se toma cuando esta puerta esté cumplida; si no lo está, se registra la limitación y se refuerzan dos bases. |

## Qué hacer si una puerta no se cumple en su fecha

1. No avances al bloque siguiente; haz el REFUERZO que propone la guía.
2. Mueve la secuencia completa, incluidas las fechas de las puertas siguientes. No se acumulan horas.
3. No recuperes un día perdido en otro. Un día perdido se pierde; un obligatorio pendiente sigue siendo obligatorio.
4. Los domingos son descanso por defecto; si tienes energía, dedica 45–120 minutos a UNA opción y no recuperes una jornada completa.

## Competencias y dónde se entrenan

| Competencia | Lecciones NÚCLEO | Jornadas | Lectura NÚCLEO (min) |
|---|---|---|---:|
| Consultas SQL de lectura: SELECT, filtros, NULL y orden | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 | D01–D03 | 121 |
| Agregación y denominadores en SQL | 2.1, 2.2, 2.3, 2.4, 2.5 | D04–D17 | 105 |
| JOIN, cardinalidad y conciliación | 3.1, 3.2, 3.3, 3.4 | D09–D11 | 90 |
| Consultas analíticas: subconsultas, CTE y ventanas | 4.1, 4.2, 4.3 | D18 | 60 |
| ETL: contrato, calidad, rechazos y cargas repetibles | 5.1, 5.2, 5.3, 5.4, 5.5 | D22–D24 | 130 |
| KPIs: definición, numerador y denominador | 6.1, 6.2, 6.3, 6.4, 6.5, 6.6 | D12–D38 | 161 |
| Fundamentos de Python | 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13 | D01–D08 | 302 |
| Funciones, archivos, errores y pruebas | 8.1, 8.3, 8.4, 8.5, 8.6, 8.7 | D08–D12 | 140 |
| Pandas: lectura, perfilado y limpieza | 9.2, 9.3, 9.4, 9.5, 9.6 | D15–D23 | 112 |
| Pandas: transformar, agrupar, unir y validar | 10.1, 10.2, 10.3, 10.4, 10.5, 10.6 | D16–D26 | 140 |
| Estadística descriptiva | 11.1, 11.2, 11.3, 11.4, 11.5, 11.8 | D09–D32 | 155 |
| Estadística inferencial introductoria | 12.1, 12.2, 12.3, 12.4, 12.5, 12.8 | D36–D39 | 175 |
| Modelado dimensional | 13.1, 13.2, 13.3 | D26–D32 | 75 |
| Power BI, Power Query y DAX | 14.1, 14.2, 14.3, 14.4, 14.5 | D30–D33 | 136 |
| Excel como segundo camino de cuadre | 15.1, 15.2, 15.3 | D30–D31 | 80 |
| Git, documentación y portafolio | 16.1, 16.2 | D05–D40 | 45 |
| Transferencia y depuración autónoma | 17.1, 17.2 | D36–D38 | 55 |
| Entrevistas técnicas | 18.1 | D40 | 25 |

## Práctica BASE por competencia

| Grupo | Ejercicios BASE | Minutos | Primer día | Último día |
|---|---:|---:|---|---|
| SQL | 16 | 535 | D01 | D31 |
| Python | 14 | 440 | D01 | D19 |
| SQL de recuperación | 17 | 280 | D10 | D40 |
| Git y portafolio | 1 | 30 | D10 | D10 |
| Pandas | 8 | 250 | D15 | D37 |
| ETL | 14 | 1055 | D22 | D40 |
| Estadística | 6 | 300 | D25 | D40 |
| KPIs | 1 | 30 | D29 | D29 |
| Excel · Power Query · BI · modelo | 8 | 420 | D30 | D33 |
