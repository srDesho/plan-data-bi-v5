# Cierre de secuencia pedagógica · Plan Data & BI v5

14 de octubre de 2026 · repositorio original · `main` · HEAD `6ac1af8`.

**APROBADO — PLAN DATA & BI V5 LISTO PARA ESTUDIAR.** Con observaciones no bloqueantes: las comprobaciones de aplicaciones requieren ejecutarlas realmente; no se acredita todavía el aprendizaje del alumno. No se reconstruyó el currículo ni se abrió otra fase.

## 1. Actividades y jornadas comprendidas

Se extrajeron **87 asignaciones BASE/REPASO/criterio, correspondientes a 84 IDs distintos**, en D01–D42. Incluyen seis exámenes y ocho hitos. J2 se repasa y N3/V4 vuelven a aparecer dentro de un examen: son asignaciones repetidas, no ejercicios nuevos ni minutos duplicados. Las tareas internas de cada examen se contrastan con su tabla de competencias y sus controles; no se vuelven a sumar como actividades independientes.

Antes de este cierre, `nucleo.json` clasificaba 81 asignaciones desde D03; D01/D02 conservaban nueve referencias heredadas sin clasificación individual completa. Se explicitan seis actividades BASE y tres ampliaciones: S10 y S9 como REFUERZO; C01 como OPCIONAL. El examen S01 ya excluía C01 y S9. La prioridad y el banco adicional de D01 se precisan desde los enunciados y las fuentes, conservando su guía.

| Área | Asignaciones obligatorias revisadas |
|---|---:|
| SQL | 18 |
| Python | 12 |
| Analítica/KPI | 18 |
| Exámenes | 6 |
| Hitos | 8 |
| Depuración | 1 |
| Pandas | 6 |
| ETL/proyectos | 14 |
| Excel | 1 |
| Power BI | 3 |
| **Total** | **87** |

Los domingos D07, D14, D21, D28, D35 y D42 mantienen cero obligaciones. Excel/BI se cuentan con el alcance BASE reducido expresamente en las guías; Power Query/M, correcciones regionales y BI avanzado que solo pertenecen a ampliación no se convierten en requisitos ocultos.

## 2. Método y alcance real

Se reutilizaron `nucleo.json`, `lecciones.json`, calendario, las 42 guías, índices, enunciados y `INFORME_CIERRE_FASE2.md`. La matriz histórica de 17 prerrequisitos se conserva como evidencia, sin repetir su auditoría. El anexo registra por actividad competencia, preparación obligatoria, orden, ejemplo y recuperación REDUCIDA.

La extracción y los controles recorren todas las asignaciones. La lectura directa se concentró en los sospechosos iniciales (S1/S2/S4/S6/S9/S10, P01–P07 y sus bases), el orden D10, recuperación D15–D16, KPI AN07, registros del ETL y el procedimiento de PB02. También se contrastaron los focos pertinentes de SQL intermedio, mini-ETL, transferencia, analítica, BI y tablas preparatorias de exámenes. La preparación Pandas y los 17 pares reutilizan además la revisión de Fase 2.

**No se afirma lectura exhaustiva individual de todos los enunciados o lecciones.** En el anexo, D significa lectura directa de las partes pertinentes, R evidencia semántica reutilizada de Fase 2 y M comprobación de metadatos/referencias. Detectar un encabezado de ejemplo automáticamente demuestra presencia; no sustituye evaluar su explicación. Se profundizó cuando el mapa mostró enseñanza posterior, REFUERZO usado como base, orden invertido o recuperación tardía. Se aceptaron competencias equivalentes, sin exigir que cada función apareciera literalmente en cada guía.

## 3. Casos correctos

- P04/P05: listas, diccionarios, conjuntos y orden antes de resolverlos; P06 combina `get`/actualización de claves de 7.9 con recorrido y contador persistente de 7.11. No se exige adelantar toda 7.12 para esa combinación.
- G3/G6, JOIN/LEFT JOIN y CTE/ventanas: las lecciones pertinentes preceden a la práctica del día; los exámenes reutilizan competencias anteriores.
- Pandas: PD-BASE precede a P22/P21; PD-AGR precede a la agrupación requerida por H03. Se mantienen catálogo único, huérfanos, tipos, nulos y conciliación introducidos en Fase 2.
- Mini-ETL: 19.3 antes de ME01; 19.2/5.2 antes de ME02; 5.3/19.4 antes de ME03. El ETL guiado y C06 aplican ese método con contratos diferentes.
- Estadística: 11.3 antes de AN08; 11.4/11.5 antes de AN13. Modelado precede a relaciones; 14.3 precede a las tres medidas BASE de PB03; 15.3 precede a EX01.
- S01–S06/H01–H08 conservan contratos, contenidos evaluados, puntuaciones y umbrales; se recalcularon sus controles aplicables.

## 4. Aclaraciones aplicadas

| Caso | Evidencia y aclaración mínima |
|---|---|
| S1/P01, D01 | Los índices y sus rótulos REFUERZO dejaban impreciso el recorrido inicial. Cada enunciado ofrece ahora un ejemplo explicado previo de tabla/consulta o variables/función. Juntos concretan 16 de los 20 min de teoría existentes. D01 no se edita. |
| P03, D02 | 7.5 sí enseña texto. Se hacen obligatorias sus secciones 3, 4 y 6 antes del intento, con ejemplo independiente de `split()` sin separador y texto intacto. Se contabilizan 12 min; no se acredita una pista como preparación. |
| S4, D03 | Se explicitan filtros combinados y sentido del orden con una tabla inventada, antes del intento. Sus 6 min se contabilizan; no se indica la consulta empresarial. |
| P06, D04 | La frase de 7.11 que parecía excluir todo conteo era demasiado tajante: se aclara la combinación contador + diccionario ya enseñada; 7.12 sigue desarrollando los patrones en D05. Cero minutos adicionales. |
| D10 | Se ordenan las lecturas 8.3 → 8.4 conforme al prerrequisito declarado. Mismos 47 min y mismas prácticas. |
| REDUCIDO D15–D16 | 9.3 debe recuperarse antes de 10.1/PD-BASE en D16, no esperar hasta P23. Se explicita la recuperación y la entrada de D16. Lectura ya presupuestada, cero minutos nuevos. |
| Registro del ETL | El README precisa que logging es rastro auditable de etapas, conteos y reglas por ejecución, que puede documentarse con los registros existentes. El módulo `logging` es ampliación de 5.4. No se rebajan cuadres ni validadores. |
| PB02, D32 | Se explica el procedimiento orientativo de marcar calendario y comprobar fecha, unicidad, vacíos y continuidad. Cuatro minutos de lectura nuevos; la ejecución y la evidencia en Desktop siguen pendientes del alumno. |

No se promocionaron lecciones completas de REFUERZO ni se exigieron funciones concretas cuando ya se enseñó a reconocer la competencia.

## 5. Defectos pedagógicos confirmados y corregidos

| Actividad | Antes | Ahora |
|---|---|---|
| S2, D02 | Valores únicos exigidos antes de 1.6, D03; las pistas no daban preparación obligatoria anterior al intento. | Puente de 7 min antes del problema: DISTINCT, unidad del resultado, combinaciones, límites y errores comunes. Muestrario inventado, sin tablas/columnas reales ni consulta completa de S2. 1.6 permanece en D03. |
| P02, D02 | 7.6 explica comparaciones/None, pero no un bloque ejecutable que decida qué operación se realiza; 7.10 llega D04. | Puente de 7 min sobre decisión, sangría y retorno temprano, con ejemplo de stock. La condición y el cálculo empresarial siguen a cargo del alumno. |
| AN07, D12 | Exigía cumplimiento/cobertura/efectividad y atribuía sus denominadores a 6.1; la explicación específica de 6.2 llega D25. | Definiciones y ejemplo independiente de agenda/ventas antes de pedirlas, 6 min; pista corregida. 6.2 sigue en D25 para profundizar. |

Son tres integraciones pequeñas y aclaraciones localizadas, no numerosos defectos graves que requieran reconstruir muchas jornadas. Por ello se completó el alcance mínimo ya autorizado.

## 6. Exploración intencional y ampliación

AN03, punto 3, pregunta explícitamente qué técnica todavía no se tiene para analizar ventas por ruta; solo pide formular la pregunta futura, no implementar un JOIN anticipadamente. Es exploración intencional de una necesidad. Los domingos, S9/S10 y el banco opcional no se convierten en defectos por incorporar contenidos adicionales: se conserva su carácter voluntario y se enlaza preparación antes de intentarlos.

## 7. S2, S9 y S10

- **S2:** BASE en D02; defecto confirmado y puente anterior de 7 min. DISTINCT no ordena ni elimina datos; cambiar las columnas seleccionadas cambia la unidad del resultado. No se entregó su solución.
- **S9:** la guía vigente ya lo marcaba «ampliación si queda tiempo». Se explicita REFUERZO en la fuente y se enlaza 1.3 antes del intento. IN/BETWEEN no son indispensables: comparaciones y AND/OR con paréntesis expresan la misma competencia. Sin obligación ni minutos nuevos BASE.
- **S10:** figura en D01 después de S1, bajo la regla de prioridades/banco adicional; faltaba clasificación individual. COUNT no se explica en el índice actual de capítulo 1. Se precisa REFUERZO y se enlazan los ejemplos 1–2 de 2.1 antes del intento (4 min voluntarios), manteniendo la lección completa en D04. Las casillas completadas no se usaron como prueba de enseñanza. No se convierte esta ampliación en requisito de avance ni en preparación imprescindible de S01.

## 8. Archivos de este cierre

Se modificaron 28 archivos existentes y se creó únicamente este informe como documento nuevo (29 archivos en este cierre; incluye el manifiesto). Se trabajó sobre los cambios previos, sin revertirlos:

- `01_PLAN_DIARIO/CARGA_ESTIMADA.md`.
- `01_PLAN_DIARIO/RUTAS.md`.
- `01_PLAN_DIARIO/calendario.csv`.
- `01_PLAN_DIARIO/calendario.json`.
- `01_PLAN_DIARIO/dias/D02_2026-10-13.md`.
- `01_PLAN_DIARIO/dias/D03_2026-10-14.md`.
- `01_PLAN_DIARIO/dias/D10_2026-10-21.md`.
- `01_PLAN_DIARIO/dias/D12_2026-10-23.md`.
- `01_PLAN_DIARIO/dias/D15_2026-10-26.md`.
- `01_PLAN_DIARIO/dias/D16_2026-10-27.md`.
- `01_PLAN_DIARIO/dias/D32_2026-11-12.md`.
- `01_PLAN_DIARIO/lecciones.json`.
- `01_PLAN_DIARIO/nucleo.json`.
- `02_TEORIA/07_Python_basico/11_for_while.md`.
- `03_EJERCICIOS/Analitico/AN07.md`.
- `03_EJERCICIOS/Casos/PB02.md`.
- `03_EJERCICIOS/Python/P01.md`.
- `03_EJERCICIOS/Python/P02.md`.
- `03_EJERCICIOS/Python/P03.md`.
- `03_EJERCICIOS/SQL/S1.md`.
- `03_EJERCICIOS/SQL/S10.md`.
- `03_EJERCICIOS/SQL/S2.md`.
- `03_EJERCICIOS/SQL/S4.md`.
- `03_EJERCICIOS/SQL/S9.md`.
- `05_PROYECTOS/etl/README.md`.
- `10_VALIDACION/MANIFIESTO_SHA256.json`.
- `herramientas/aplicar_nucleo.py`.
- `herramientas/verificar_etapa2.py`.
- `INFORME_CIERRE_SECUENCIA_PEDAGOGICA.md` (nuevo).

`preparaciones` en `nucleo.json` registra las ocho lecturas/predicciones previas; `dias_iniciales` aclara D01/D02. `lecciones.json` señala dónde se enseña la base mínima, manteniendo 47 NÚCLEO, 33 REFUERZO y 20 PROFUNDIZACIÓN. El generador y el verificador incorporan esa fuente; detectan preparación ausente/posterior, minutos discordantes, orden invertido y recuperación tardía.

Los 11 derivados diferentes se prepararon primero en una copia temporal; solo se trasladaron cuatro documentos/calendarios y siete guías afectadas: D02, D03, D10, D12, D15, D16 y D32. No se regeneraron masivamente las 42 guías del original. La prueba de sincronización sí ejecutó el generador completo en una copia para comprobar idempotencia. El CSV añade dos columnas de preparación y clasifica las prioridades iniciales; no altera fechas ni bloques originales de D01/D02.

## 9. Minutos y calendario

**5.400 min / 90 h de plan**, sin cambiar las seis semanas ni los domingos. Estimación BASE: **5.771 → 5.813 min**, incremento de **42 min**; aproximadamente **96,9 h**. La lectura L pasa de 1.197 a 1.239 min; ejercicios E permanecen en 2.399 min y criterio C en 435 min. La evaluación posterior sigue en 570 min / 9,5 h. Total estimado incluyendo esa evaluación: 6.383 min, aproximadamente 106,4 h; UAGRM aparte.

| Preparación | Tratamiento del tiempo |
|---|---:|
| S1/P01, D01 | 8 + 8 = 16 min dentro de los 20 min de teoría existentes; quedan 4 para contexto del entorno |
| S2/P02/P03, D02 | +7 +7 +12 = **26 min** |
| S4, D03 | **+6 min** |
| AN07, D12 | **+6 min** |
| PB02, D32 | **+4 min** |
| S10, voluntario | 4 min fuera de BASE |
| Reordenar D10/recuperar D15 | 0 min nuevos; preparación ya presupuestada |
| **Incremento BASE** | **42 min** |

Los 16 min iniciales concretan los mismos fundamentos que el objetivo de D01 ya destinaba a teoría; no se añaden otras tareas ni se restan minutos de práctica. En los demás casos la preparación se añade conservadoramente a la estimación, aunque parte del material existiera como consulta. D02 conserva íntegros sus bloques y pasa de 165 a 191 min estimados. REDUCIDO pospone entregas cuando falta base; no acredita una puerta ni convierte la preparación pendiente en aprendizaje realizado.

| Semana | Plan min | Estimación anterior | Estimación actual |
|---|---:|---:|---:|
| 1 | 900 | 956 | 988 |
| 2 | 900 | 968 | 974 |
| 3 | 900 | 977 | 977 |
| 4 | 900 | 960 | 960 |
| 5 | 900 | 975 | 979 |
| 6 | 900 | 935 | 935 |

## 10. Pruebas ejecutadas ahora y evidencia histórica

Entorno: `.venv`, Python **3.12.10**, `-B` y sin bytecode. Los ejemplos SQL se interpretan en papel en la preparación del alumno; para verificarlos aquí se construyeron tablas ficticias en SQLite **en memoria**, independientes de los datos empresariales.

| Comprobación actual | Resultado |
|---|---|
| Grupos pertinentes de `Verificador`: lecciones, jornadas, guías, prerrequisitos, ejercicios/lecciones, documentos, sincronización, actividades y exámenes/final | **9/9 OK**; se invocaron esos métodos, no se declara corrida completa del CLI |
| Preparación de secuencia | Ocho bloques obligatorios antes de sus actividades; 42 min nuevos y D01 sin doble conteo |
| Ejemplos añadidos | **6 bloques ejecutados** (3 SQL y 3 Python); predicciones, repetidos, condiciones, límites y texto original comprobados; aritmética independiente AN07 comprobada |
| Regresión dirigida en copia temporal | **15/15 incoherencias rechazadas**: ocho bloques eliminados, preparación S2 posterior, minutos discordantes, orden D10 invertido, recuperación D15 tardía, P02 sin decisión, AN07 sin definición y bloque S2 después del problema |
| AN/H | **42 cifras de control recalculadas**, 18 actividades analíticas y ocho hitos válidos |
| Exámenes | **35 controles recalculados**, seis exámenes y ocho hitos con condiciones conservadas |
| Referencias | Fuentes sin referencias inválidas; **333 destinos locales** de los Markdown modificados y las ocho anclas previas comprobados |
| Privacidad pública | Auditoría `auditar_artefactos` sin filtraciones detectadas; ningún acceso ni copia de respuestas reservadas |
| Integridad | D01 y los 13 archivos del conjunto personal/UAGRM/D01 idénticos a la instantánea; D02 idéntico fuera del único bloque nuevo, con sus 15 casillas conservadas |
| SHA256 | Manifiesto regenerado y comprobado, **590 archivos**, vigente |
| Git | `git diff --check` con salida **0**; sin commits, push, ramas nuevas ni operaciones destructivas |

La sincronización detectó primero descripciones de REFUERZO que propagaban cambios innecesarios a cuatro guías. Se conservaron esas descripciones y se documentó la preparación aparte. Una segunda comprobación señaló el texto derivado de D03 aún anterior a ese ajuste: se sincronizó y la comprobación final pasó. Esos fallos se corrigieron; no se presentan como aprobaciones previas.

**Evidencia histórica reutilizada, no ejecutada de nuevo:** la suite completa 26/26, los 621 bloques teóricos, las tres referencias técnicas, las 50 alteraciones de validadores y las 13 pruebas de privacidad de los cierres anteriores. Los seis archivos técnicos de Fase 1 conservan sus SHA256; las nueve lecciones corregidas en Fase 2 y los checkpoints Pandas también se conservan. No se repitieron ETL ni la batería general de mutaciones: los cambios actuales son preparación, fuentes y generación pedagógica. `10_VALIDACION/resultados_pruebas.json` conserva la corrida histórica saneada; esta corrida dirigida se documenta aquí, sin hacerla pasar por una suite completa nueva.

## 11. Preservación del trabajo y Git

La instantánea se tomó **antes de editar** y se respaldó el D02 vigente en una carpeta temporal. Antes de trasladar cada derivado se comparó su hash con la instantánea, impidiendo sobrescribir cambios concurrentes detectables. Al retirar el bloque `SECUENCIA:GUIA` añadido, el D02 final coincide **byte por byte** con ese respaldo: objetivos, ejercicios, notas, avances y estados de sus 15 casillas se conservan.

No se modificó ningún archivo de `mi_trabajo`, incluidos `mis_funciones.py`, `S2.sql` y `S7.sql`. Tampoco D01, materiales UAGRM, custodia externa, contratos de exámenes/hitos ni archivos de evaluación final. Los cambios personales ya presentes al inicio permanecen; no se comparan contra HEAD para exigir que desaparezcan. La verificación apropiada de esta sesión es la instantánea contemporánea. No se ejecutó como aprobación el control Git antiguo que exige todo `mi_trabajo` limpio.

Estado final comprobado: `main`, HEAD `6ac1af8`, **56 archivos rastreados modificados y siete nuevos**, nada preparado para commit. Incluye los cambios previos de Fases 1/2 y los cuatro cambios personales ya presentes; este cierre aporta 28 modificaciones y un informe respecto de su instantánea inicial. Las copias de generación y regresión se retiraron; queda únicamente el respaldo temporal y los registros pequeños de comprobación fuera del repositorio, en `C:\Users\ASUS\AppData\Local\Temp\secuencia_cierre_jw3sww79`.

## 12. Observaciones y bloqueos

**No queda bloqueo pedagógico demostrado en el alcance de esta comprobación.** La ruta proporciona preparación explícita antes de lo obligatorio y conserva recuperación antes de las puertas. Esto no certifica el aprendizaje personal: se acredita con entregas y defensa.

Excel, Power BI Desktop, SQL Server e importación a Notion siguen necesitando sus pruebas manuales cuando se utilicen; no se declaran aprobadas aquí. La exposición histórica del final permanece documentada en `INFORME_CIERRE_FASE1.md`: no se reescribió Git ni se convierte retrospectivamente aquella evaluación en una prueba ciega. Son observaciones no bloqueantes para estudiar el material.

## Anexo · Mapa ligero por actividad

Todas las filas siguientes son BASE/REPASO/criterio; la preparación indicada es obligatoria **antes del intento**, en una jornada anterior o tras la lectura inicial del mismo día. Los ejemplos se distinguen de la solución del ejercicio. D/R/M describe el alcance de comprobación, no un nivel de dominio del alumno. Las partes de exámenes repetidas no cuentan tiempo aparte. Los seis domingos sin obligaciones completan las 42 jornadas.

| Día / actividad | Competencia indispensable | Primera preparación explícita y obligatoriedad | Ejemplo / comprobación | REDUCIDO y recuperación | Evidencia |
|---|---|---|---|---|---|
| [D01 · S1](03_EJERCICIOS/SQL/S1.md) | Leer filas/columnas, seleccionar, ordenar y limitar | Bloque previo S1, D01; obligatorio antes del intento | Ejemplo independiente leído; ejecutado | Preparación antes de S1/P01; si no cabe, posponer entrega antes de D03. | D |
| [D01 · P01](03_EJERCICIOS/Python/P01.md) | Variables, tipos, llamada y retorno de función | Bloque previo P01, D01; obligatorio antes del intento | Ejemplo independiente leído; ejecutado | Preparación antes de S1/P01; si no cabe, posponer entrega antes de D03. | D |
| [D02 · S2](03_EJERCICIOS/SQL/S2.md) | Interpretar valores y combinaciones únicos | Bloque previo S2, D02; obligatorio antes del intento | Ejemplo independiente leído; ejecutado | Puente de lo que se intente; recuperar P02 antes D03/H01/S01 y texto antes P09. | D |
| [D02 · S7](03_EJERCICIOS/SQL/S7.md) | Detectar nulos sin confundirlos con cero | 1.4 D02; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Puente de lo que se intente; recuperar P02 antes D03/H01/S01 y texto antes P09. | M |
| [D02 · P02](03_EJERCICIOS/Python/P02.md) | Condición que evita una operación inválida; porcentaje/None | Bloque previo P02, D02; obligatorio antes del intento | Ejemplo independiente leído; ejecutado | Puente de lo que se intente; recuperar P02 antes D03/H01/S01 y texto antes P09. | D |
| [D02 · P03](03_EJERCICIOS/Python/P03.md) | Texto inmutable, separación, unión y formato | Bloque previo P03, D02; obligatorio antes del intento | Ejemplo independiente leído; ejecutado | Puente de lo que se intente; recuperar P02 antes D03/H01/S01 y texto antes P09. | D |
| [D03 · S4](03_EJERCICIOS/SQL/S4.md) | Combinar filtros y elegir sentido del orden | Bloque previo S4, D03; obligatorio antes del intento | Ejemplo independiente leído; ejecutado | S4/S6/P05 omitidos: recuperar antes D04. | D |
| [D03 · S6](03_EJERCICIOS/SQL/S6.md) | Buscar un patrón y ordenar | 1.6 D03; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | S4/S6/P05 omitidos: recuperar antes D04. | D |
| [D03 · P04](03_EJERCICIOS/Python/P04.md) | Construir un registro con claves | 7.8 D03; 7.9 D03; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | S4/S6/P05 omitidos: recuperar antes D04. | D |
| [D03 · P05](03_EJERCICIOS/Python/P05.md) | Unicidad, orden y origen intacto | 7.8 D03; 7.9 D03; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | S4/S6/P05 omitidos: recuperar antes D04. | D |
| [D03 · AN01](03_EJERCICIOS/Analitico/AN01.md) | ¿Qué estamos contando? | 1.6 D03; 7.9 D03; lectura obligatoria anterior o antes de la práctica del día | Unicidad en 1.6/7.9; diez observaciones permiten conteo manual en diccionario | S4/S6/P05 omitidos: recuperar antes D04. | D |
| [D04 · G3](03_EJERCICIOS/SQL/G3.md) | Agregar importes calculados por línea | 2.1 D04; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | G3 omitido: recuperar antes D05; P06 conserva 7.11. | D |
| [D04 · P06](03_EJERCICIOS/Python/P06.md) | Recorrer y actualizar cuentas por clave | 7.9 D03; 7.11 D04; lectura obligatoria anterior o antes de la práctica del día | get/actualización en 7.9 y contador persistente en 7.11: combinación equivalente | G3 omitido: recuperar antes D05; P06 conserva 7.11. | D |
| [D04 · AN02](03_EJERCICIOS/Analitico/AN02.md) | Hechos e hipótesis: los pedidos anulados | 2.1 D04; lectura obligatoria anterior o antes de la práctica del día | Reglas explican hecho verificable, hipótesis y dato para contrastarla; sin herramienta nueva | G3 omitido: recuperar antes D05; P06 conserva 7.11. | D |
| [D05 · G6](03_EJERCICIOS/SQL/G6.md) | Agrupar y filtrar grupos | 2.2 D05; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P07 y su base antes H01/S01. | D |
| [D05 · P07](03_EJERCICIOS/Python/P07.md) | Acumular registros que cumplen condición | 7.12 D05; 7.13 D05; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P07 y su base antes H01/S01. | D |
| [D05 · AN03](03_EJERCICIOS/Analitico/AN03.md) | ¿Qué es una ruta «grande»? | 2.2 D05; lectura obligatoria anterior o antes de la práctica del día | Ejemplos de conteos previos; pregunta exploratoria de JOIN sin exigir implementarlo | P07 y su base antes H01/S01. | D |
| [D06 · EXAMEN:S01](03_EJERCICIOS/EXAMENES/S01.md) | Fundamentos SQL, Python y KPI | Tabla de competencias y prácticas obligatorias anteriores del examen | Variantes tras enseñanza; controles recalculados | Evaluar solo tras recuperar la base de P1. | D |
| [D06 · H01](03_EJERCICIOS/Comprension/H01.md) | Hito de comprensión 1: consultar y calcular | 1.4 D02; 2.1 D04; 2.2 D05; 7.12 D05; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Evaluar solo tras recuperar la base de P1. | M |
| [D08 · P08](03_EJERCICIOS/Python/P08.md) | Función con contrato y límites | 7.10 D04; 8.1 D08; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | 7.7 omitida: recuperar antes D10. | M |
| [D09 · J2](03_EJERCICIOS/SQL/J2.md) | Unir claves, filtrar y sumar sin duplicar | 3.2 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | DB01/8.5/19.1 omitidos: antes D10. | M |
| [D09 · DB01](03_EJERCICIOS/Depuracion/DB01.md) | Leer un error y rechazar un valor | 8.5 D09; 19.1 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | DB01/8.5/19.1 omitidos: antes D10. | M |
| [D09 · AN04](03_EJERCICIOS/Analitico/AN04.md) | Cumplimiento: ¿a quién felicitas? | 2.3 D06; 3.2 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | DB01/8.5/19.1 omitidos: antes D10. | M |
| [D10 · P09](03_EJERCICIOS/Python/P09.md) | Convertir dinero y rechazar formatos inválidos | 7.7 D08; 8.5 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P13 omitido: antes P2. | D |
| [D10 · P13](03_EJERCICIOS/Python/P13.md) | Leer CSV como registros de texto | 8.3 D10; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P13 omitido: antes P2. | M |
| [D10 · AN05](03_EJERCICIOS/Analitico/AN05.md) | ¿El INNER JOIN pierde filas? | 3.2 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P13 omitido: antes P2. | M |
| [D11 · J5](03_EJERCICIOS/SQL/J5.md) | Conservar ausentes y situar filtros | 3.3 D11; 3.4 D11; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Variante mínima; ON temporal y cardinalidad antes P2. | M |
| [D11 · AN06](03_EJERCICIOS/Analitico/AN06.md) | Recomendación a gerencia: clientes sin compra | 3.3 D11; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Variante mínima; ON temporal y cardinalidad antes P2. | M |
| [D12 · P10](03_EJERCICIOS/Python/P10.md) | Interpretar fechas y rechazar inválidas | 8.4 D10; 8.5 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P11 antes S02; 9.2 antes P17; AN07 antes de intentarlo. | M |
| [D12 · P11](03_EJERCICIOS/Python/P11.md) | Validar entero sin truncar | 7.7 D08; 8.5 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | P11 antes S02; 9.2 antes P17; AN07 antes de intentarlo. | M |
| [D12 · AN07](03_EJERCICIOS/Analitico/AN07.md) | Elegir KPI, numerador, denominador y periodo | Bloque previo AN07, D12; obligatorio antes del intento | Caso independiente calculado | P11 antes S02; 9.2 antes P17; AN07 antes de intentarlo. | D |
| [D13 · EXAMEN:S02](03_EJERCICIOS/EXAMENES/S02.md) | JOIN, archivos y cuadre | Tabla de competencias y prácticas obligatorias anteriores del examen | Variantes tras enseñanza; controles recalculados | 11.3 omitida: antes AN08/D16. | D |
| [D13 · H02](03_EJERCICIOS/Comprension/H02.md) | Hito de comprensión 2: funciones, errores y JOIN | 7.7 D08; 8.5 D09; 3.2 D09; 3.3 D11; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | 11.3 omitida: antes AN08/D16. | M |
| [D15 · P17](03_EJERCICIOS/Python/P17.md) | Cargar tabla sin perder códigos de texto | 9.2 D12; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | 9.2 antes P17; 9.3 antes 10.1/PD-BASE/D16. | R |
| [D15 · J2](03_EJERCICIOS/SQL/J2.md) | Unir claves, filtrar y sumar sin duplicar | 3.2 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | 9.2 antes P17; 9.3 antes 10.1/PD-BASE/D16. | M |
| [D16 · PD-BASE](02_TEORIA/10_Pandas_transformaciones/01_columnas_nuevas.md) | Seleccionar, filtrar, convertir y preservar origen | 10.1 D16; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-BASE antes D17; estadística D13 antes AN08. | R |
| [D16 · P22](03_EJERCICIOS/Python/P22.md) | Duplicado exacto frente a conflicto | 9.5 D16; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-BASE antes D17; estadística D13 antes AN08. | R |
| [D16 · K1](03_EJERCICIOS/SQL/K1.md) | Cambiar grano de línea a pedido | 2.2 D05; 3.2 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-BASE antes D17; estadística D13 antes AN08. | D |
| [D16 · AN08](03_EJERCICIOS/Analitico/AN08.md) | ¿Cuál es el pedido típico? | 11.3 D13; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-BASE antes D17; estadística D13 antes AN08. | R |
| [D17 · PD-AGR](02_TEORIA/10_Pandas_transformaciones/02_groupby_agg.md) | Agrupar y reconciliar sin depender de merge | 10.2 D17; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-AGR y huérfanos antes H03/P3. | R |
| [D17 · P21](03_EJERCICIOS/Python/P21.md) | Unión muchos a uno, catálogo y huérfanos | 10.3 D17; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-AGR y huérfanos antes H03/P3. | R |
| [D17 · AN09](03_EJERCICIOS/Analitico/AN09.md) | Tendencia: ¿más pedidos o pedidos más grandes? | 10.2 D17; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PD-AGR y huérfanos antes H03/P3. | M |
| [D18 · V3](03_EJERCICIOS/SQL/V3.md) | CTE, total y acumulado antes del límite | 4.2 D18; 4.3 D18; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Ventanas/porcentajes omitidos: antes P3. | D |
| [D18 · AN10](03_EJERCICIOS/Analitico/AN10.md) | Concentración: ¿de cuántos clientes dependemos? | 4.3 D18; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Ventanas/porcentajes omitidos: antes P3. | D |
| [D19 · V4](03_EJERCICIOS/SQL/V4.md) | Acumulado anterior y clasificación por umbral | 2.5 D17; 4.3 D18; 6.5 D19; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | V4 omitido: antes P3. | D |
| [D19 · P23](03_EJERCICIOS/Python/P23.md) | Perfilar filas, tipos, nulos y duplicados | 9.3 D15; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | V4 omitido: antes P3. | R |
| [D19 · AN11](03_EJERCICIOS/Analitico/AN11.md) | ABC: qué hacer con cada clase | 6.5 D19; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | V4 omitido: antes P3. | M |
| [D20 · EXAMEN:S03](03_EJERCICIOS/EXAMENES/S03.md) | CTE, Pandas y calidad de datos | Tabla de competencias y prácticas obligatorias anteriores del examen | Variantes tras enseñanza; controles recalculados | No acreditar P3 con agrupación/uniones pendientes. | D |
| [D20 · H03](03_EJERCICIOS/Comprension/H03.md) | Hito de comprensión 3: Pandas, claves y ventanas | 10.3 D17; 9.5 D16; 4.3 D18; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | No acreditar P3 con agrupación/uniones pendientes. | R |
| [D22 · ME01](03_EJERCICIOS/Puente/ME01.md) | Extraer, preservar Bronze y perfilar | 19.3 D20; 9.5 D16; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Mini-ETL parcial no acredita P4. | D |
| [D23 · ME02](03_EJERCICIOS/Puente/ME02.md) | Convertir, validar y separar rechazos | 19.2 D23; 5.2 D23; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversión y validación pendientes: antes P4. | D |
| [D23 · AN12](03_EJERCICIOS/Analitico/AN12.md) | Rechazos: ¿problema de datos o señal de negocio? | 5.2 D23; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversión y validación pendientes: antes P4. | M |
| [D24 · ME03](03_EJERCICIOS/Puente/ME03.md) | Reconciliar, agregar y cargar repetiblemente | 5.3 D24; 19.4 D24; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | SQLite/Gold/cuadres pendientes: antes P4. | D |
| [D24 · H04](03_EJERCICIOS/Comprension/H04.md) | Hito de comprensión 4: el mini-ETL | 5.2 D23; 5.3 D24; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | SQLite/Gold/cuadres pendientes: antes P4. | M |
| [D25 · ETL-1](05_PROYECTOS/etl/README.md) | Contrato, extracción, Bronze, perfil y texto | 19.3 D20; 5.2 D23; lectura obligatoria anterior o antes de la práctica del día; ME01–ME03 ya realizados | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | ETL parcial no acredita P5a/P5. | D |
| [D26 · ETL-2](05_PROYECTOS/etl/README.md) | Fechas, cantidad y dinero exacto | 8.4 D10; 8.5 D09; lectura obligatoria anterior o antes de la práctica del día; ME01–ME03 ya realizados | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversión/claves pendientes: antes S04/P5a. | D |
| [D26 · ETL-3](05_PROYECTOS/etl/README.md) | Claves, conflictos y recuperación inequívoca | 9.5 D16; 10.3 D17; lectura obligatoria anterior o antes de la práctica del día; ME01–ME03 ya realizados | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversión/claves pendientes: antes S04/P5a. | D |
| [D26 · H05](03_EJERCICIOS/Comprension/H05.md) | Hito de comprensión 5: claves, duplicados y fechas | 5.3 D24; 6.2 D25; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversión/claves pendientes: antes S04/P5a. | M |
| [D27 · N2](03_EJERCICIOS/SQL/N2.md) | Cobertura de ejecución de visitas | 2.3 D06; 2.5 D17; 6.2 D25; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Evaluar solo preparación recuperada; P5 aún parcial. | D |
| [D27 · EXAMEN:S04](03_EJERCICIOS/EXAMENES/S04.md) | Hito del ETL: mini-ETL y ETL hasta claves y duplicados | Tabla de competencias y prácticas obligatorias anteriores del examen | Variantes tras enseñanza; controles recalculados | Evaluar solo preparación recuperada; P5 aún parcial. | D |
| [D29 · ETL-4](05_PROYECTOS/etl/README.md) | Validación Silver y causas de rechazo | 5.2 D23; 5.3 D24; lectura obligatoria anterior o antes de la práctica del día; ME01–ME03 ya realizados | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Validación y 15.3 pendientes: antes P5/EX01. | D |
| [D30 · ETL-5](05_PROYECTOS/etl/README.md) | Gold al grano cliente/mes | 10.1 D16; 10.2 D17; lectura obligatoria anterior o antes de la práctica del día; ME01–ME03 ya realizados | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Gold/SQLite/README pendientes: antes P5; 13.2 antes PB02. | D |
| [D30 · ETL-6](05_PROYECTOS/etl/README.md) | SQLite, repetición, cuadre SQL y README | 19.4 D24; 5.3 D24; lectura obligatoria anterior o antes de la práctica del día; ME01–ME03 ya realizados; plantilla README enlazada en la actividad | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Gold/SQLite/README pendientes: antes P5; 13.2 antes PB02. | D |
| [D30 · H06](03_EJERCICIOS/Comprension/H06.md) | Hito de comprensión 6: Gold, cuadre y repetición | 5.3 D24; 5.2 D23; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Gold/SQLite/README pendientes: antes P5; 13.2 antes PB02. | M |
| [D31 · E4](03_EJERCICIOS/SQL/E4.md) | Ventas entregadas por ruta | 2.2 D05; 3.2 D09; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Puede hacer solo E4; EX01/15.3 antes P6. | D |
| [D31 · EX01](03_EJERCICIOS/Casos/EX01.md) | Tabla dinámica y conciliación SQL | 15.3 D29; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Puede hacer solo E4; EX01/15.3 antes P6. | D |
| [D31 · AN14](03_EJERCICIOS/Analitico/AN14.md) | Cobertura frente a efectividad: ¿a quién ayudas? | 6.2 D25; 6.4 D31; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Puede hacer solo E4; EX01/15.3 antes P6. | D |
| [D32 · PB01](03_EJERCICIOS/Casos/PB01.md) | Importación y tipos/conteos | 14.1 D32; 13.2 D30; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PB02 y su procedimiento antes P6; sin Desktop, PENDIENTE. | D |
| [D32 · PB02](03_EJERCICIOS/Casos/PB02.md) | Relaciones y calendario marcado | Bloque previo PB02, D32; obligatorio antes del intento; 13.2 D30 y 14.1 D32 antes de relaciones | Procedimiento explicado; Desktop pendiente | PB02 y su procedimiento antes P6; sin Desktop, PENDIENTE. | D |
| [D32 · AN15](03_EJERCICIOS/Analitico/AN15.md) | Productividad: dos formas de medir una ruta | 6.4 D31; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | PB02 y su procedimiento antes P6; sin Desktop, PENDIENTE. | D |
| [D33 · PB03](03_EJERCICIOS/Casos/PB03.md) | Medidas, filtros y ticket contrastados | 14.3 D33; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Tres medidas núcleo antes P6; sin Desktop, PENDIENTE. | D |
| [D33 · H07](03_EJERCICIOS/Comprension/H07.md) | Hito de comprensión 7: BI mínimo | 14.3 D33; 13.2 D30; 15.3 D29; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Tres medidas núcleo antes P6; sin Desktop, PENDIENTE. | M |
| [D34 · N3](03_EJERCICIOS/SQL/N3.md) | Efectividad de las visitas realizadas | 2.3 D06; 2.5 D17; 6.2 D25; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Parte BI pendiente no acredita P6. | D |
| [D34 · EXAMEN:S05](03_EJERCICIOS/EXAMENES/S05.md) | ETL guiado completo y BI mínimo | Tabla de competencias y prácticas obligatorias anteriores del examen | Variantes tras enseñanza; controles recalculados | Parte BI pendiente no acredita P6. | D |
| [D34 · AN13](03_EJERCICIOS/Analitico/AN13.md) | Dispersión y atípicos: ¿qué pedido es «raro»? | 11.4 D25; 11.5 D27; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Parte BI pendiente no acredita P6. | R |
| [D36 · C06-0](03_EJERCICIOS/Casos/C06.md) | Leer un contrato nuevo y planificar | 17.1 D36; lectura obligatoria anterior o antes de la práctica del día; mini-ETL y ETL guiado anteriores | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Contrato/control pendiente antes P7. | D |
| [D37 · C06-1](03_EJERCICIOS/Casos/C06.md) | Adaptar conversiones, texto y pruebas | 8.4 D10; 8.5 D09; 17.1 D36; lectura obligatoria anterior o antes de la práctica del día; mini-ETL y ETL guiado anteriores | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversiones/pruebas pendientes antes P7. | D |
| [D37 · AN16](03_EJERCICIOS/Analitico/AN16.md) | C06: el problema de negocio antes del código | 17.1 D36; 10.3 D17; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Conversiones/pruebas pendientes antes P7. | D |
| [D38 · C06-2](03_EJERCICIOS/Casos/C06.md) | Claves, rechazos y conciliación | 17.2 D38; lectura obligatoria anterior o antes de la práctica del día; mini-ETL y ETL guiado anteriores | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Cuadres pendientes antes P7. | D |
| [D38 · AN17](03_EJERCICIOS/Analitico/AN17.md) | C06: ¿hay tendencia o ruido? | 17.2 D38; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Cuadres pendientes antes P7. | M |
| [D39 · C06-3](03_EJERCICIOS/Casos/C06.md) | Gold y KPI al grano del contrato | 10.2 D17; 17.2 D38; lectura obligatoria anterior o antes de la práctica del día; mini-ETL y ETL guiado anteriores | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Gold/KPI pendientes antes P7. | D |
| [D39 · AN18](03_EJERCICIOS/Analitico/AN18.md) | C06: el memo para gerencia | 6.6 D39; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Gold/KPI pendientes antes P7. | M |
| [D40 · C06-4](03_EJERCICIOS/Casos/C06.md) | Carga, auditoría, repetición y documentación | 16.2 D40; 19.4 D24; lectura obligatoria anterior o antes de la práctica del día; mini-ETL y ETL guiado anteriores | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Documentación, repetición y H08 antes P7. | D |
| [D40 · H08](03_EJERCICIOS/Comprension/H08.md) | Hito de comprensión 8: transferencia a un caso nuevo | 17.1 D36; 17.2 D38; 6.6 D39; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Documentación, repetición y H08 antes P7. | M |
| [D41 · N3](03_EJERCICIOS/SQL/N3.md) | Efectividad de las visitas realizadas | 2.3 D06; 2.5 D17; 6.2 D25; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Evaluar solo tras P7; final condicionado a puertas. | D |
| [D41 · V4](03_EJERCICIOS/SQL/V4.md) | Acumulado anterior y clasificación por umbral | 2.5 D17; 4.3 D18; 6.5 D19; lectura obligatoria anterior o antes de la práctica del día | Ejemplos detectados en teoría (presencia, no nueva prueba semántica) | Evaluar solo tras P7; final condicionado a puertas. | D |
| [D41 · EXAMEN:S06](03_EJERCICIOS/EXAMENES/S06.md) | Transferencia C06 y defensa | Tabla de competencias y prácticas obligatorias anteriores del examen | Variantes tras enseñanza; controles recalculados | Evaluar solo tras P7; final condicionado a puertas. | D |
