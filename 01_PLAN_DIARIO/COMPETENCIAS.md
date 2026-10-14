# Competencias, puertas y cómo usar OBLIGATORIO / REFUERZO / OPCIONAL

Esta página reemplaza la idea de "avanzar porque llegó la fecha" por "avanzar porque demostré la base".
Las fechas del plan siguen siendo **objetivos**. Nada de lo que sigue promete que vayas a completar todo antes del 30 de noviembre.

## Cómo se clasifica cada ejercicio

| Etiqueta | Significado | Cuándo se hace |
|---|---|---|
| **OBLIGATORIO** | Núcleo del día. Sin esto la puerta no se cumple. | Siempre, en este orden. |
| **REPASO** | Un ejercicio de SQL que ya hiciste; lo rehaces de memoria en 10 minutos. | Cuando el día no tiene SQL nuevo. |
| **REFUERZO** | Práctica que fortalece la misma base. | Si la puerta no se cumplió, si te atascaste, o si sobró tiempo. |
| **OPCIONAL** | Enriquecimiento. | Solo con tiempo libre; nunca desplaza lo obligatorio. |

En el **modo REDUCIDO** haces solo lo que indica la sección "Haz solo" de la guía. En el **modo MÍNIMO** (20 minutos) rehaces una consulta conocida y explicas una decisión: sirve para no romper la racha, no para avanzar contenidos.
Lo que no hiciste no se suma al día siguiente. Si un OBLIGATORIO quedó pendiente, pasa a ser REFUERZO de la próxima sesión disponible.

## Las puertas

Cada puerta describe lo que debes poder demostrar, con evidencia, antes de pasar al bloque siguiente. "Explicar" significa decirlo en voz alta sin leer tu código.

| Puerta | Fecha objetivo | Qué demuestras | Evidencia | Si no se cumple |
|---|---|---|---|---|
| **P1 · Consultar y calcular** | D06 | SELECT/WHERE/GROUP BY/HAVING con el filtro correcto; un bucle con acumulador; numerador y denominador de un KPI | Examen S01 con 70/100 o más, o dos consultas y un bucle rehechos sin mirar; hito H01 | REFUERZO de D03–D05 en el próximo bloque práctico |
| **P2 · Funciones, errores y JOIN** | D13 | P09–P11 con `ValueError`; JOIN y LEFT JOIN explicados; leer CSV con el módulo estándar | P09–P11 y P13 aprobados; J1, J2 y J5 explicados; S02 con 70/100 o más; hito H02 | REFUERZO de D09–D11 antes de Pandas |
| **P3 · Pandas y calidad de datos** | D20 | DataFrame, `groupby`, merge `many_to_one` con `validate`, duplicados exactos frente a conflictos, perfilado | P17 y P20–P23 aprobados; K1, V3, V4; S03 con 70/100 o más; hito H03 | REFUERZO de D16–D19; el mini-ETL espera |
| **P4 · Mini-ETL** | D24 | Un ETL de cuatro funciones con rechazos, ecuación de conteos, carga repetible y conexión cerrada | ME01–ME03 aprobados con tu código; segunda ejecución igual; archivo SQLite renombrable (conexión cerrada); hito H04 | ME01–ME03 pasan a REFUERZO; el ETL grande no empieza |
| **P5a · Checkpoint ETL guiado** | D27 | El ETL de la distribuidora hasta claves y duplicados | Conteos de control (filas de origen, duplicados, vendedores recuperados); S04; hito H05 | Se completa en D29–D30; no se promueve a aprobado |
| **P5 · ETL guiado completo** | D30 (defensa en D34) | Gold, carga SQLite repetible, cuadre SQL independiente | `validar_etl_distribuidora.py` correcto; segunda ejecución; prueba de cantidad fraccionaria; cinco decisiones explicadas; hito H06 | Excel y Power BI se posponen; REFUERZO del ETL |
| **P6 · BI mínimo** | D34 | Tabla dinámica de Excel contra SQL; tablas, relaciones y tres medidas de Power BI contra SQL | Excel coincide con E4; las medidas coinciden con J2 y K1, o la parte que no ejecutaste queda registrada como PENDIENTE; hito H07 | El resto de BI pasa a REFUERZO después de P7; no retrasa C06 |
| **P7 · Transferencia C06** | D41 | Un ETL nuevo con tu código, validado y defendido | `validar_final.py --transferencia` correcto; repetición; pruebas adversas; defensa de cinco decisiones; hito H08 | Se registra la limitación y se refuerzan dos bases antes de cualquier variante |

La **evaluación final** (objetivo 23–30 de noviembre) se toma cuando P7 esté cumplida. Si en esa fecha no lo está, no se declara aprobación: se registra la limitación y se trabaja el refuerzo. Una prueba aprobada con ayuda no acredita autonomía.

## Qué hacer si una puerta no se cumple en su fecha

1. No avances al bloque siguiente; haz el REFUERZO que la guía del día propone.
2. Mueve la secuencia completa, incluidas las fechas de las puertas siguientes. El número de horas por semana (15 netas) no cambia.
3. No recuperes un día perdido en otro. Un día perdido se pierde; un OBLIGATORIO pendiente se convierte en REFUERZO.
4. Los domingos son descanso por defecto: nada es obligatorio. Si tienes energía, puedes dedicar 45–120 minutos, y solo a una opción, a recuperar un REFUERZO o a una lección de EXTENDIDA; no recuperes una jornada completa.
5. Si la Puerta 5 se retrasa, Excel y Power BI esperan; si la Puerta 6 se retrasa, el caso C06 no espera por ellas.
6. Registra el motivo en `mi_trabajo/errores.md` y la nueva fecha objetivo en `mi_trabajo/progreso.csv`.

## De Python básico al ETL: la ruta de cinco peldaños

1. **Función con contrato** (P01–P08, P09–P11): entra un dato, sale un valor o un `ValueError`.
2. **Función sobre una tabla** (P17–P23): lo mismo, con DataFrames y comprobaciones de cardinalidad.
3. **Leer un error** (DB01–DB03, capítulo 19 §1): saber qué dice un traceback y detectar los errores que no avisan.
4. **Mini-ETL** (ME01–ME04, 24 filas): extraer, transformar, validar y cargar con rechazos y cuadre.
5. **ETL guiado** (distribuidora, 16.378 filas) y luego **caso nuevo C06** sin plantilla.

## Estimaciones de carga (supuestos)

`CARGA_ESTIMADA.md` muestra el tiempo estimado por jornada: lectura de las lecciones NÚCLEO, criterio analítico y ejercicios OBLIGATORIOS, más empleo, examen y cierre. **No es una medición.** Cada enunciado declara un tiempo objetivo (para quien ya domina el tema) y un tiempo de **primera vez** realista para un principiante, con margen para leer, depurar y equivocarse; la estimación usa el punto medio de ese rango. Las tareas de proyecto (ETL guiado, C06) y las versiones reducidas de Excel y Power BI se estimaron a mano. El error razonable es de ±35 %.
Registra tus minutos reales en `mi_trabajo/progreso.csv`; después de dos semanas, ajusta el plan con tus propios datos. Un día con razón por encima de 1,2 es AJUSTADO: usa el modo REDUCIDO. Las semanas estimadas por encima de 1,1 del plan (15 h) corren la puerta sin acumular horas: el plan no promete que el estimado de primera vez quepa en 15 horas; promete que las 15 horas netas se dedican primero a lo NÚCLEO.

## Alcance reducido de Excel y Power BI

Siguen en el plan, con menos alcance: Excel (EX01, D31), Power BI en dos sesiones (PB01+PB02, D32, y PB03 con tres medidas, D33) y su comprobación en S05. PB04–PB06 y EX02–EX03 son REFUERZO u OPCIONAL y pueden hacerse después de la Puerta 7. El paquete no incluye un archivo PBIX ni se ejecutó Power BI Desktop al preparar este material: lo que no ejecutes tú queda registrado como PENDIENTE.

## Demostrar comprensión: los hitos H01–H08

Obtener un OK del corrector no demuestra que entiendes. Cada puerta tiene un **hito de comprensión** (`03_EJERCICIOS/Comprension/H01…H08`, 20–25 minutos, sin IA y sin abrir tus soluciones) con cuatro partes:

1. **Explicar** con tus palabras los conceptos de la puerta, sin leer tu código.
2. **Predecir** un resultado antes de ejecutarlo y anotar por qué coincidió o no.
3. **Resolver una variante nueva**, distinta de los ejercicios que ya resolviste.
4. **Justificar** una decisión comparando alternativas.

El hito se da por cumplido con tres de los cuatro criterios sostenidos oralmente. Si falla, la puerta pasa a REFUERZO de lo que faltó, igual que un examen por debajo del umbral. Las cifras de control de cada hito están en `08_SOLUCIONES/controles_analitico.md` y se recalculan con `herramientas/verificar_etapa2.py`.

| Hito | Puerta | Jornada | Qué comprueba |
|---|---|---|---|
| H01 | P1 | D06 | NULL, denominador de un cumplimiento, efecto de los anulados, bucle con acumulador |
| H02 | P2 | D13 | `ValueError` en conversiones, INNER frente a LEFT, peligro de truncar |
| H03 | P3 | D20 | `validate` del merge, duplicado frente a conflicto, acumulado ordenado |
| H04 | P4 | D24 | Cuatro funciones, ecuación de conteos, cierre de la conexión, regla nueva |
| H05 | P5a | D26 | Conflictos de clave, recuperación inequívoca, fechas, centavos |
| H06 | P5 | D30 | Gold, cuadre SQL independiente, repetición |
| H07 | P6 | D33 | Relaciones, medida frente a columna, contexto de filtro |
| H08 | P7 | D40 | El método frente a un caso nuevo, decisiones y límites |

## Criterio analítico empresarial

No quiero solamente calcular indicadores: quiero comprender qué significan y cuándo usarlos. Por eso las guías de martes a viernes incluyen una actividad de 15 minutos (`03_EJERCICIOS/Analitico/AN01…AN18`) que no tiene corrector: se evalúa tu razonamiento con una rúbrica y se contrasta con cifras de control después de escribirlo.

| Habilidad de criterio | Actividades | Conceptos |
|---|---|---|
| Definir el problema de negocio y la unidad de análisis | AN01, AN16 | cliente, visita, pedido y línea; qué decisión cambia |
| Separar hechos de hipótesis | AN02, AN06, AN09, AN12, AN15 | afirmaciones comprobables frente a causas por probar |
| Elegir el KPI y su denominador | AN03, AN04, AN07, AN14 | cumplimiento, cobertura, efectividad, productividad |
| Comparar resultados y descomponer una variación | AN08, AN09, AN15, AN17 | media, mediana y moda; volumen frente a tamaño |
| Medir dispersión y posición | AN08, AN13 | desviación estándar, cuartiles, IQR, percentiles, atípicos |
| Concentración y ABC | AN10, AN11 | Pareto 80/20, clases A/B/C |
| Reconocer datos insuficientes | AN05, AN12, AN16, AN17 | extractos pequeños, supuestos que no se comprobaron, campos que no existen |
| Recomendar a gerencia | AN06, AN10, AN11, AN18 | hecho, límite, hipótesis, acción medible |

## Perfil N1 (analista junior de datos)

N1 es el nivel de quien puede resolver, **sin copiar y con ayuda mínima**, tareas acotadas y repetibles de datos y explicar qué hizo. No es empleo asegurado ni autonomía profesional avanzada: es la base que este programa se propone demostrar con evidencia.

| Competencia N1 | Evidencia en el plan |
|---|---|
| Consultar datos con SQL (filtros, agregación, JOIN, CTE, ventanas) con el denominador correcto | P1–P3; S01–S03; AN03–AN05, AN10–AN11 |
| Escribir funciones Python con contrato y leer un error | P1–P2; P09–P13; H02; DB01 |
| Manipular tablas con Pandas y validar uniones y duplicados | P3; P17, P20–P23; H03 |
| Construir un ETL pequeño (Bronze, Silver, Gold) repetible, con rechazos y cuadres | P4–P5; ME01–ME03; ETL-1 a ETL-6; H04–H06 |
| Elegir y calcular KPIs y saber qué significan (cumplimiento, cobertura, efectividad, productividad, ABC) | AN04, AN07, AN11, AN14, AN15 |
| Describir datos con media, mediana, moda, dispersión y percentiles y elegir la medida adecuada | AN08, AN13; 11.3–11.5 |
| Cuadrar el mismo resultado entre herramientas (SQL, Python, Excel, BI) | P6; E4; PB03; H07 |
| Comunicar con hechos, hipótesis, límites y una acción | AN06, AN18; 6.6 |
| Transferir el método a un caso nuevo y defender las decisiones | P7; C06; H08 |

## Rutas de estudio

La ruta BASE de 15 horas, la EXTENDIDA y la clasificación de las 100 lecciones están en [`RUTAS.md`](RUTAS.md).
