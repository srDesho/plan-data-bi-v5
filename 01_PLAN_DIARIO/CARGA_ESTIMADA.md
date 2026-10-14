# Carga estimada por jornada (ruta BASE)

Estimación de **primera vez** para una persona que todavía depende de ayuda externa. **No es una medición**: los tiempos de cada ejercicio son los que declara su propio enunciado (punto medio del rango «Primera vez», que ya incluye leer el enunciado, equivocarse, depurar y verificar), y los multiplicadores de respaldo (SQL ×1,5–2,25; Python ×2–3,25; estadística ×2–2,5; casos ×1,75; Excel/Power BI ×2) y las tareas de proyecto estimadas a mano son supuestos con un error razonable de ±35 %. Todavía no existen mediciones reales: registra tus minutos en `mi_trabajo/progreso.csv` y corrige esta tabla con tus datos.

## Qué cuenta cada columna (sin dobles conteos)

| Columna | Qué incluye | Qué NO incluye |
|---|---|---|
| **L** | Lectura de las lecciones NÚCLEO del día (minutos del encabezado de cada lección) | La micropráctica de las lecciones (REFUERZO/EXTENDIDA) |
| **C** | Actividad de criterio analítico o hito de comprensión | Su revisión posterior con los controles (se hace dentro de la misma actividad) |
| **E** | Ejercicios OBLIGATORIOS y REPASO a tiempo de primera vez (incluye leer el enunciado, depurar y comprobar) | REFUERZO, OPCIONAL y notebooks; las tareas que son parte de un examen (N2, N3, V4…) no se suman otra vez |
| **X** | Examen 60 + corrección 25 + simulacro 30 = 115 min en los sábados de examen (tiempo fijo) | — |
| **F** | Empleo, postulaciones, LinkedIn y cierre (tiempo fijo del plan) | — |

Estimado = F + X + L + C + E. D01 conserva su diseño; D02 suma sus lecciones sugeridas sobre el bloque original. La ruta EXTENDIDA (voluntaria) no está incluida.

| Día | Fecha | Contenido | Plan (min) | L | C | E | X | F | Estimado (min) | Razón |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| D01 | 2026-10-12 | Entorno, filas y variables | 90 | 20 | 0 | 50 | 0 | 20 | 90 | 1,00 |
| D02 | 2026-10-13 | Filtros, NULL y texto | 160 | 35 | 0 | 95 | 0 | 35 | 165 | 1,03 |
| D03 | 2026-10-14 | Listas, diccionarios y clientes únicos | 150 | 55 | 15 | 84 | 0 | 20 | 174 | 1,16 |
| D04 | 2026-10-15 | Agrupación, bucles y media/mediana | 150 | 60 | 15 | 48 | 0 | 40 | 163 | 1,09 |
| D05 | 2026-10-16 | Condiciones, funciones cortas y KPIs | 150 | 73 | 15 | 56 | 0 | 20 | 164 | 1,09 |
| D06 | 2026-10-17 | Primer examen y cierre de fundamentos | 200 | 25 | 20 | 0 | 115 | 40 | 200 | 1,00 |
| D08 | 2026-10-19 | Funciones con contrato y condiciones | 90 | 45 | 0 | 28 | 0 | 20 | 93 | 1,03 |
| D09 | 2026-10-20 | Primer JOIN y errores visibles | 160 | 55 | 15 | 55 | 0 | 35 | 160 | 1,00 |
| D10 | 2026-10-21 | Funciones que convierten y archivos CSV | 150 | 47 | 15 | 97 | 0 | 20 | 179 | 1,19 |
| D11 | 2026-10-22 | Ausencia con LEFT JOIN | 150 | 45 | 15 | 48 | 0 | 40 | 148 | 0,99 |
| D12 | 2026-10-23 | Fechas, cantidades y leer un error | 150 | 25 | 15 | 103 | 0 | 20 | 163 | 1,09 |
| D13 | 2026-10-24 | Examen de JOIN y conciliación | 200 | 25 | 20 | 0 | 115 | 40 | 200 | 1,00 |
| D15 | 2026-10-26 | Primer DataFrame y perfilado | 90 | 40 | 0 | 40 | 0 | 20 | 100 | 1,11 |
| D16 | 2026-10-27 | Duplicados exactos y drop size | 160 | 42 | 15 | 83 | 0 | 35 | 175 | 1,09 |
| D17 | 2026-10-28 | Agrupar y unir con validación | 150 | 65 | 15 | 70 | 0 | 20 | 170 | 1,13 |
| D18 | 2026-10-29 | CTE y concentración de ventas | 150 | 40 | 15 | 65 | 0 | 40 | 160 | 1,07 |
| D19 | 2026-10-30 | ABC, perfilado y criterio | 150 | 25 | 15 | 107 | 0 | 20 | 167 | 1,11 |
| D20 | 2026-10-31 | Examen Pandas y SQL intermedio | 200 | 25 | 20 | 0 | 115 | 40 | 200 | 1,00 |
| D22 | 2026-11-02 | Mini-ETL (1): extraer y perfilar | 90 | 0 | 0 | 70 | 0 | 20 | 90 | 1,00 |
| D23 | 2026-11-03 | Mini-ETL (2): transformar con reglas y rechazos | 160 | 40 | 15 | 90 | 0 | 35 | 180 | 1,12 |
| D24 | 2026-11-04 | Mini-ETL (3): validar, cuadrar y cargar | 150 | 40 | 25 | 95 | 0 | 20 | 180 | 1,20 |
| D25 | 2026-11-05 | ETL guiado (1): contrato, Bronze y texto | 150 | 55 | 0 | 75 | 0 | 40 | 170 | 1,13 |
| D26 | 2026-11-06 | ETL guiado (2): fechas, cantidad, claves y duplicados | 150 | 0 | 20 | 115 | 0 | 20 | 155 | 1,03 |
| D27 | 2026-11-07 | Examen S04: mini-ETL y ETL hasta claves | 200 | 30 | 0 | 0 | 115 | 40 | 185 | 0,93 |
| D29 | 2026-11-09 | ETL guiado (3): Silver, validación y rechazos | 90 | 30 | 0 | 50 | 0 | 20 | 100 | 1,11 |
| D30 | 2026-11-10 | ETL guiado (4): Gold, carga y cuadre SQL | 160 | 25 | 20 | 110 | 0 | 35 | 190 | 1,19 |
| D31 | 2026-11-11 | Excel: tabla dinámica y cuadre | 150 | 20 | 15 | 120 | 0 | 20 | 175 | 1,17 |
| D32 | 2026-11-12 | Power BI (1): importar y relacionar | 150 | 30 | 15 | 95 | 0 | 40 | 180 | 1,20 |
| D33 | 2026-11-13 | Power BI (2): primeras medidas | 150 | 35 | 20 | 80 | 0 | 20 | 155 | 1,03 |
| D34 | 2026-11-14 | Examen S05: ETL guiado completo y BI mínimo | 200 | 0 | 15 | 0 | 115 | 40 | 170 | 0,85 |
| D36 | 2026-11-16 | Caso nuevo C06 (0): contrato y plan | 90 | 30 | 0 | 40 | 0 | 20 | 90 | 1,00 |
| D37 | 2026-11-17 | C06 (1): extraer, Bronze y perfil | 160 | 0 | 15 | 100 | 0 | 35 | 150 | 0,94 |
| D38 | 2026-11-18 | C06 (2): Silver y rechazos | 150 | 25 | 15 | 110 | 0 | 20 | 170 | 1,13 |
| D39 | 2026-11-19 | C06 (3): Gold y cuadres | 150 | 25 | 15 | 90 | 0 | 40 | 170 | 1,13 |
| D40 | 2026-11-20 | C06 (4): SQLite, repetición y README | 150 | 25 | 20 | 110 | 0 | 20 | 175 | 1,17 |
| D41 | 2026-11-21 | Examen S06: transferencia C06 y defensa | 200 | 25 | 0 | 0 | 115 | 40 | 180 | 0,90 |

| Semana | Plan (min) | Estimado BASE (min) | Estimado BASE (h) | Razón | Jornadas AJUSTADAS (razón > 1,15, sin exámenes) |
|---:|---:|---:|---:|---:|---|
| 1 | 900 | 956 | 15,9 | 1,06 | D03 |
| 2 | 900 | 943 | 15,7 | 1,05 | D10 |
| 3 | 900 | 972 | 16,2 | 1,08 | — |
| 4 | 900 | 960 | 16,0 | 1,07 | D24 |
| 5 | 900 | 970 | 16,2 | 1,08 | D30, D31, D32 |
| 6 | 900 | 935 | 15,6 | 1,04 | D40 |

**Total de las seis semanas (42 jornadas):** plan 5400 min (90,0 h); estimado BASE de primera vez 5736 min (95,6 h), razón 1,06. La diferencia de 336 min (5,6 h) es estimación, no medición: cabe dentro del margen de ±35 % y se absorbe con REDUCIDO en las jornadas AJUSTADAS; no se compensa con las horas voluntarias de EXTENDIDA.

Una razón por encima de 1,15 en una jornada la marca como AJUSTADA: usa el modo REDUCIDO (cada jornada define una entrega menor y realizable en `RUTAS.md`) y mueve el REFUERZO; no alargues el día. Si una semana queda por encima de 1,1, la puerta se corre sin acumular horas (ver `COMPETENCIAS.md`).

## Evaluación final: bloque posterior, NO incluido en las 90 horas

La evaluación final (23–30 de noviembre de 2026) ocurre **después** de las 42 jornadas y es una séptima semana de evaluación, no parte de las seis semanas. Antes reservaba 12,5 h; ahora reserva **9,5 h netas** (570 min), estimadas de primera vez y no medidas. La reducción de 3,0 h sale de sustituir trabajo que ya se hizo en C06 (D36–D40) y que el alumno puede reutilizar con su propio código: no se acorta la evidencia que se exige, se evita construirla dos veces desde cero.

| Fecha | Día | Antes (min) | Ahora (min) | Entrega comprobable | Qué se sustituyó |
|---|---|---:|---:|---|---|
| 2026-11-23 | lunes | 90 | 90 | Contrato propio y perfil de los datos nuevos (despachos de una ferretería mayorista) | Sin cambio: el contrato es nuevo y hay que leerlo; la clase UAGRM va aparte. |
| 2026-11-24 | martes | 120 | 90 | Funciones adaptadas a las reglas nuevas, pruebas de formatos y Bronze | Partes de tus funciones de C06 (permitido y explicable) en lugar de reescribir la extracción, Bronze y las pruebas básicas. |
| 2026-11-25 | miércoles | 120 | 90 | Silver con clave compuesta, catálogo, rechazos y cuadre de conteos | Reutilizas tu estructura de conflictos y duplicados de C06; solo se adapta la clave y las reglas. |
| 2026-11-26 | jueves | 120 | 90 | Gold por sucursal, mes y línea; SQLite y validación previa a publicar | Reutilizas tu carga repetible de C06; cambia el grano del Gold y se añade una medida. |
| 2026-11-27 | viernes | 90 | 60 | SQL independiente, segunda ejecución y cuatro entradas adversas | Las entradas adversas ya se practicaron en C06-4: aquí se repiten sobre el esquema nuevo con copias. |
| 2026-11-28 | sábado | 120 | 60 | README, informe de KPIs con tabla o gráfico, hallazgos y ensayo de la defensa | README e informe parten de lo que ya escribiste en C06; se elimina el bloque de ampliación. |
| 2026-11-29 | domingo | 0 | 0 | Descanso | Sin cambio. |
| 2026-11-30 | lunes | 90 | 90 | Defensa con observador (decisiones, predicción, reparación y modificación en vivo), corrector y rúbrica | Sin cambio: la defensa es la evidencia de autoría; la clase UAGRM va aparte. |
| **Total** | | **750** (12,5 h) | **570** (9,5 h) | | |

Total del programa: 90,0 h de plan en seis semanas (estimado 95,6 h) + 9,5 h de evaluación final = 99,5 h de plan (105,1 h estimadas). Si no puedes dedicar la evaluación final en esas fechas, no se declara autonomía: se reprograma sin acumular horas. La evaluación final solo se toma si la Puerta 7 está cumplida; si no, se reprograma sin acumular horas y no se declara autonomía.
