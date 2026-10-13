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
| **P1 · Consultar y calcular** | D06 | SELECT/WHERE/GROUP BY/HAVING con el filtro correcto; un bucle con acumulador; numerador y denominador de un KPI | Examen S01 con 70/100 o más, o dos consultas y un bucle rehechos sin mirar | REFUERZO de D03–D05 en el próximo bloque práctico |
| **P2 · Funciones, errores y JOIN** | D13 | P09–P11 con `ValueError`; JOIN y LEFT JOIN explicados; leer CSV con el módulo estándar | P09–P11 y P13 aprobados; J1, J2 y J5 explicados; S02 con 70/100 o más | REFUERZO de D09–D11 antes de Pandas |
| **P3 · Pandas y calidad de datos** | D20 | DataFrame, `groupby`, merge `many_to_one` con `validate`, duplicados exactos frente a conflictos, perfilado | P17, P19–P23 aprobados; K1, K3, V3, V4; S03 con 70/100 o más | REFUERZO de D16–D18; el mini-ETL espera |
| **P4 · Mini-ETL** | D24 | Un ETL de cuatro funciones con rechazos, ecuación de conteos, carga repetible y conexión cerrada | ME01–ME03 aprobados con tu código; segunda ejecución igual; archivo SQLite renombrable (conexión cerrada) | ME01–ME03 pasan a REFUERZO; el ETL grande no empieza |
| **P5a · Checkpoint ETL guiado** | D27 | El ETL de la distribuidora hasta claves y duplicados | Conteos de control (filas de origen, duplicados, vendedores recuperados); S04 | Se completa en D29–D30; no se promueve a aprobado |
| **P5 · ETL guiado completo** | D30 (defensa en D34) | Gold, carga SQLite repetible, cuadre SQL independiente | `validar_etl_distribuidora.py` correcto; segunda ejecución; prueba de cantidad fraccionaria; cinco decisiones explicadas | Excel y Power BI se posponen; REFUERZO del ETL |
| **P6 · BI mínimo** | D34 | Tabla dinámica de Excel contra SQL; tablas, relaciones y tres medidas de Power BI contra SQL | Excel coincide con E4; las medidas coinciden con J2 y K1, o la parte que no ejecutaste queda registrada como PENDIENTE | El resto de BI pasa a REFUERZO después de P7; no retrasa C06 |
| **P7 · Transferencia C06** | D41 | Un ETL nuevo con tu código, validado y defendido | `validar_final.py --transferencia` correcto; repetición; pruebas adversas; defensa de cinco decisiones | Se registra la limitación y se refuerzan dos bases antes de cualquier variante |

La **evaluación final** (objetivo 23–30 de noviembre) se toma cuando P7 esté cumplida. Si en esa fecha no lo está, no se declara aprobación: se registra la limitación y se trabaja el refuerzo. Una prueba aprobada con ayuda no acredita autonomía.

## Qué hacer si una puerta no se cumple en su fecha

1. No avances al bloque siguiente; haz el REFUERZO que la guía del día propone.
2. Mueve la secuencia completa, incluidas las fechas de las puertas siguientes. El número de horas por semana (15 netas) no cambia.
3. No recuperes un día perdido en otro. Un día perdido se pierde; un OBLIGATORIO pendiente se convierte en REFUERZO.
4. Los domingos siguen siendo descanso: sin estudio, sin consultas, sin commits.
5. Si la Puerta 5 se retrasa, Excel y Power BI esperan; si la Puerta 6 se retrasa, el caso C06 no espera por ellas.
6. Registra el motivo en `mi_trabajo/errores.md` y la nueva fecha objetivo en `mi_trabajo/progreso.csv`.

## De Python básico al ETL: la ruta de cinco peldaños

1. **Función con contrato** (P01–P08, P09–P11): entra un dato, sale un valor o un `ValueError`.
2. **Función sobre una tabla** (P17–P23): lo mismo, con DataFrames y comprobaciones de cardinalidad.
3. **Leer un error** (DB01–DB03, capítulo 19 §1): saber qué dice un traceback y detectar los errores que no avisan.
4. **Mini-ETL** (ME01–ME04, 24 filas): extraer, transformar, validar y cargar con rechazos y cuadre.
5. **ETL guiado** (distribuidora, 16.378 filas) y luego **caso nuevo C06** sin plantilla.

## Estimaciones de carga (supuestos)

`CARGA_ESTIMADA.md` muestra el tiempo estimado de lo OBLIGATORIO por jornada. **No es una medición.** Cada enunciado declara un tiempo objetivo (para quien ya domina el tema) y un tiempo de **primera vez** realista para un principiante, con margen para leer, depurar y equivocarse; la estimación usa el punto medio de ese rango. Las tareas de proyecto (ETL guiado, C06) y las versiones reducidas de Excel y Power BI se estimaron a mano. El error razonable es de ±35 %.
Registra tus minutos reales en `mi_trabajo/progreso.csv`; después de dos semanas, ajusta el plan con tus propios datos. Un día con razón por encima de 1,2 es AJUSTADO: usa el modo REDUCIDO.

## Alcance reducido de Excel y Power BI

Siguen en el plan, con menos alcance: Excel (EX01, D31), Power BI en dos sesiones (PB01+PB02, D32, y PB03 con tres medidas, D33) y su comprobación en S05. PB04–PB06 y EX02–EX03 son REFUERZO u OPCIONAL y pueden hacerse después de la Puerta 7. El paquete no incluye un archivo PBIX ni se ejecutó Power BI Desktop al preparar este material: lo que no ejecutes tú queda registrado como PENDIENTE.
