# Cierre de organización didáctica · Plan Data & BI v5

14 de octubre de 2026 · repositorio original · rama `main` · commit de seguridad **`a6b20f3`**.

**APROBADO — guía diaria → teoría explicada → ejercicio autónomo → evaluación.** El plan conserva su contenido, duración y evaluaciones. La corrección termina aquí, sin commits, push, ramas ni versiones alternativas.

## Alcance y defecto corregido

La búsqueda localizada en `03_EJERCICIOS` encontró ocho bloques `SECUENCIA:PREPARACION`: S1, S2, S4, P01, P02, P03, AN07 y PB02. Eran enseñanza desarrollada dentro de enunciados. Se trasladaron realmente a ocho lecciones existentes de `02_TEORIA`; no se resolvió cambiando su encabezado.

Se comprobó automáticamente la separación en **179 archivos Markdown**. Los títulos de tablas preparatorias de exámenes, los ejemplos que explican el formato de entrada/salida, los datos y las pistas progresivas son legítimos y se conservan. No se repitió la auditoría general ni el análisis de los 17 pares; solo se inspeccionaron los ocho casos y sus dependencias de generación.

S9/S10 ya tenían referencias breves de preparación y carácter REFUERZO, sin clase incrustada. Se verificaron sus rutas y se conservaron sus archivos íntegros. Solo se modificaron **tres enunciados SQL y cinco enunciados de otras áreas**, no los bancos completos.

## Traslados y lectura anterior al intento

Cada ancla indica únicamente la sección necesaria; `#desarrollo` permite continuar con el resto sin repetirla. Las guías asignan la lectura antes de abrir el ejercicio, con recuperación de la base en REDUCIDO.

| Ejercicio | Preparación retirada del enunciado | Ubicación definitiva en teoría | Guía actualizada | Momento previo al intento | Minutos preservados | Prueba de coherencia |
|---|---|---|---|---|---:|---|
| [S1](03_EJERCICIOS/SQL/S1.md) | Explicación, ejemplo independiente, interpretación y comprobación | [1.2: tabla, selección, orden y alias](02_TEORIA/01_SQL_basico/02_select_from_alias.md#preparacion-s1) | [D01](01_PLAN_DIARIO/dias/D01_2026-10-12.md) | Primero sección 1.2, después 7.4; antes de S1 | 8; dentro de los 20 de D01 | Ancla, referencia previa, contenido preservado y crédito verificados |
| [S2](03_EJERCICIOS/SQL/S2.md) | Explicación, ejemplo independiente, interpretación y comprobación | [1.6: únicos, combinaciones y granularidad](02_TEORIA/01_SQL_basico/06_distinct_like.md#preparacion-s2) | [D02](01_PLAN_DIARIO/dias/D02_2026-10-13.md) | Antes de S2; desarrollo restante de 1.6 en D03 | 7; preservados | Ancla, referencia previa, contenido preservado y crédito verificados |
| [S4](03_EJERCICIOS/SQL/S4.md) | Explicación, ejemplo independiente, interpretación y comprobación | [1.3: filtros, comparaciones y orden](02_TEORIA/01_SQL_basico/03_where_operadores.md#preparacion-s4) | [D03](01_PLAN_DIARIO/dias/D03_2026-10-14.md) | Antes del desarrollo de 1.6 y de S4 | 6; preservados | Ancla, referencia previa, contenido preservado y crédito verificados |
| [P01](03_EJERCICIOS/Python/P01.md) | Explicación, ejemplo independiente, interpretación y comprobación | [7.4: variables, tipos, función y retorno](02_TEORIA/07_Python_basico/04_primera_funcion.md#preparacion-p01) | [D01](01_PLAN_DIARIO/dias/D01_2026-10-12.md) | Después de 1.2 y antes de P01 | 8; dentro de los 20 de D01 | Ancla, referencia previa, contenido preservado y crédito verificados |
| [P02](03_EJERCICIOS/Python/P02.md) | Explicación, ejemplo independiente, interpretación y comprobación | [7.10: decisiones, sangría y retornos](02_TEORIA/07_Python_basico/10_condicionales.md#preparacion-p02) | [D02](01_PLAN_DIARIO/dias/D02_2026-10-13.md) | Después de 7.6 y antes de P02 | 7; preservados | Ancla, referencia previa, contenido preservado y crédito verificados |
| [P03](03_EJERCICIOS/Python/P03.md) | Explicación, ejemplo independiente, interpretación y comprobación | [7.5: métodos de texto y origen intacto](02_TEORIA/07_Python_basico/05_texto.md#preparacion-p03) | [D02](01_PLAN_DIARIO/dias/D02_2026-10-13.md) | Antes de 7.6/P03; recuperar antes de P09 si se omite | 12; preservados | Ancla, referencia previa, contenido preservado y crédito verificados |
| [AN07](03_EJERCICIOS/Analitico/AN07.md) | Explicación, ejemplo independiente, interpretación y comprobación | [6.1: KPI, fracciones, periodo e interpretación](02_TEORIA/06_KPIs/01_que_es_un_kpi.md#preparacion-an07) | [D12](01_PLAN_DIARIO/dias/D12_2026-10-23.md) | Sección inicial y luego 25 min restantes; antes de AN07 | 6; preservados | Ancla, referencia previa, contenido preservado y crédito verificados |
| [PB02](03_EJERCICIOS/Casos/PB02.md) | Explicación, ejemplo independiente, interpretación y comprobación | [14.1: calendario, relaciones y validación](02_TEORIA/14_PowerBI_DAX/01_power_bi_desde_cero.md#preparacion-pb02) | [D32](01_PLAN_DIARIO/dias/D32_2026-11-12.md) | 30 min restantes de 14.1, sección de calendario; después PB01/PB02 | 4; preservados | Ancla, referencia previa, contenido preservado y crédito verificados |

También se actualiza D04 para leer el desarrollo restante de 7.10: sus primeros 7 min ya se prepararon en D02. Ningún ejercicio cambia de día, modalidad, contrato o criterio de aceptación.

## Separación y conservación de contenido

- **01_PLAN_DIARIO:** ordena las lecturas exactas. D01 enlaza 1.2 → 7.4. D02 ordena secciones de 1.6/7.5 → 1.4/7.6 → decisiones de 7.10. D03 prepara filtros antes de continuar 1.6. D12 enlaza la base de KPI antes de AN07. D32 ordena el desarrollo de Power BI, el procedimiento de calendario y los ejercicios.
- **02_TEORIA:** contiene explicaciones, sintaxis, ejemplos, errores y predicciones/microprácticas. Conserva los ejemplos independientes trasladados y las secciones originales de cada lección. La introducción autocontenida prepara la competencia mínima; el desarrollo posterior mantiene su alcance original. P03 integra la introducción de texto sin copiar de nuevo sus antiguos ejemplos 3/4/6 ni dejar una instrucción circular.
- **03_EJERCICIOS:** conserva título, tiempo, situación, datos, tablas, columnas, granularidad, reglas, comprobación, pistas y aceptación. Queda un requisito breve enlazado; desaparecen los ocho bloques y sus marcadores. Solo los punteros de P02/AN07 necesitaron adaptación dentro de sus pistas.
- **Evaluaciones y soluciones:** sin cambios; siguen después de la práctica. No se abrieron ni copiaron respuestas de la custodia externa.

La comparación contra respaldo confirmó que los **ocho cuerpos teóricos anteriores** coinciden exactamente al retirar la sección trasladada, el ancla nueva y el ajuste de tiempo del encabezado. Los seis fragmentos SQL/Python trasladados conservan su código; la tabla de tres KPI conserva sus filas y el procedimiento de PB02 conserva sus cuatro pasos, con su referencia al modelo convertida en enlace válido. Las adaptaciones corresponden a ubicación, referencias y contabilización, no a eliminar conceptos o comprobaciones.

Los tres ejemplos SQL de tablas inventadas siguen identificados como ejemplos de papel y usan la convención existente `sqlplantilla`. Se ejecutaron además sobre fixtures SQLite en memoria para comprobar su resultado; no requieren modificar la mini-base ni enseñar DDL en D01. Los ejemplos Python son ejecutables y conservan sus predicciones.

## Fuentes, generación y minutos

`nucleo.json` ahora apunta desde cada preparación a su lección/ancla en `02_TEORIA` y conserva la ruta del ejercicio como destino posterior. `lecciones.json` identifica sus secciones previas. El generador distingue **lectura completa**, **lectura previa ya contabilizada** y **lectura restante**; el verificador exige ubicación en teoría, enlace previo desde la guía y requisito breve desde el ejercicio.

| Lección | Lectura completa | Sección previa | Lectura restante |
|---|---:|---:|---:|
| 1.2 | 23 | 8 | 15 |
| 1.6 | 22 | 7 | 15 |
| 1.3 | 26 | 6 | 20 |
| 7.4 | 28 | 8 | 20 |
| 7.10 | 27 | 7 | 20 |
| 7.5 | 34 | 12 | 22 |
| 6.1 | 31 | 6 | 25 |
| 14.1 | 34 | 4 | 30 |

**Incremento de carga por este traslado: 0 min.** Permanecen **5.400 min / 90 h BASE planificadas**, **5.813 min / aproximadamente 96,9 h estimadas** y **570 min / 9,5 h posteriores de evaluación**. Se conservan los 42 min adicionales del cierre de secuencia y los 16 min iniciales dentro de los 20 de teoría de D01. L sigue en 1.239 min, E en 2.399 y C en 435. `CARGA_ESTIMADA.md` permanece idéntico byte por byte.

El inventario físico de las 100 lecciones pasa de 5.480 a 5.538 min al incluir los **58 min que antes estaban dentro de enunciados**: es traslado de material ya contabilizado, no tiempo nuevo del curso. Los índices muestran el encabezado completo y las guías descuentan la parte previa. Se mantienen **100 lecciones: 47 NÚCLEO, 33 REFUERZO y 20 PROFUNDIZACIÓN**; las lecturas completas de 1.6/7.10 conservan D03/D04.

REDUCIDO mantiene la preparación de la actividad que intenta y recupera lo omitido antes de la puerta que lo necesita. Se conservan las recuperaciones de Pandas y las prácticas PD-BASE/PD-AGR, así como el resto de dependencias corregidas en Fase 2.

## Pruebas ejecutadas en esta tarea

Entorno: `.venv`, **Python 3.12.10**, `-B`, sin bytecode. Las operaciones de generación y las mutaciones se probaron primero en copias temporales.

| Comprobación | Resultado ejecutado |
|---|---|
| Métodos afectados de `Verificador`: lecciones, jornadas, guías, prerrequisitos, ejercicios/lecciones, documentos, sincronización, actividades e integridad Git personal | **9/9 OK**; se invocaron esos métodos, no se afirma corrida completa del CLI |
| Separación pedagógica | **179 Markdown** comprobados; cero bloques o encabezados de clase extensa detectados en enunciados |
| Conservación del traslado | **8/8** secciones conservadas; cuerpos originales de teoría y de los problemas intactos, salvo requisitos/punteros documentados |
| Ejemplos de las ocho lecciones afectadas | **58 bloques ejecutables**, sin errores |
| Ejemplos independientes trasladados | **6 fragmentos comprobados**: tres SQL de papel ejecutados en memoria y tres Python; estos últimos ya están incluidos entre los 58, no se suman como bloques distintos |
| Regresión ligera de organización/secuencia | **16 variantes inválidas rechazadas y un ejemplo legítimo aceptado**: ausencia de secciones, marcadores/clases reinsertadas, encabezados renombrados, ubicación en ejercicios, guía sin referencia y crédito eliminado |
| Idempotencia | **Dos pasadas completas en copia**, 368 archivos comparados, cero diferencias byte por byte y cero enunciados escritos por el generador |
| Fuentes y derivados | Sincronizados; índices/tiempos y enlaces locales/anclas comprobados |
| Analítica e hitos | **42 cifras de control recalculadas**; 18 AN y ocho H conservados |
| Horas | 5.813 min estimados, 5.400 planificados, 42 min adicionales anteriores conservados; sin doble conteo |
| D01/D02 | Solo orientación de estudio; **10 y 15 casillas**, respectivamente, con líneas y estados idénticos al respaldo; contenido exterior idéntico byte por byte |
| Privacidad e integridad | Auditoría pública sin filtraciones detectadas; trabajo personal, datasets, UAGRM, exámenes/hitos y evaluación final sin cambios |
| Manifiesto | Regenerado y comprobado; **590 archivos**, vigente |
| Git | `git diff --check` con salida **0**; sin commits ni push |

La primera copia de prueba omitía README, que necesitaba el control documental; se completó el fixture. La sincronización también identificó D04 como derivado necesario por el crédito previo de 7.10: se actualizó únicamente su referencia/lectura restante y la comprobación final pasó. No se trasladaron fallos de esas pruebas preliminares al original.

No se repitieron la suite completa ETL, las 50 alteraciones técnicas ni las pruebas generales de privacidad: sus componentes permanecen idénticos y su evidencia anterior se reutiliza explícitamente. Tampoco se ejecutaron de nuevo los cientos de ejemplos de las lecciones no afectadas ni los 35 controles de exámenes; sus enunciados y contratos conservan sus hashes. La revisión actual no pretende ser otra auditoría general.

La regresión queda incorporada a `organizacion_enunciados()` y se ejecuta desde `preparacion_secuencia()`: prohíbe marcadores propios de clases incrustadas y detecta encabezados de enseñanza extensa, sin prohibir ejemplos de datos o pistas legítimas.

## Archivos modificados y diferencias de Git

**35 archivos existentes modificados y un informe nuevo (36 en total).** La mayor parte son los ocho pares teoría/enunciado, sus referencias y sus derivados. Se trasladaron 14 derivados revisados desde una copia: calendarios/RUTAS, seis guías y cinco índices. No se regeneraron las 42 guías del original.

- `01_PLAN_DIARIO/RUTAS.md`.
- `01_PLAN_DIARIO/calendario.csv`.
- `01_PLAN_DIARIO/calendario.json`.
- `01_PLAN_DIARIO/dias/D01_2026-10-12.md`.
- `01_PLAN_DIARIO/dias/D02_2026-10-13.md`.
- `01_PLAN_DIARIO/dias/D03_2026-10-14.md`.
- `01_PLAN_DIARIO/dias/D04_2026-10-15.md`.
- `01_PLAN_DIARIO/dias/D12_2026-10-23.md`.
- `01_PLAN_DIARIO/dias/D32_2026-11-12.md`.
- `01_PLAN_DIARIO/lecciones.json`.
- `01_PLAN_DIARIO/nucleo.json`.
- `02_TEORIA/01_SQL_basico.md`.
- `02_TEORIA/01_SQL_basico/02_select_from_alias.md`.
- `02_TEORIA/01_SQL_basico/03_where_operadores.md`.
- `02_TEORIA/01_SQL_basico/06_distinct_like.md`.
- `02_TEORIA/06_KPIs.md`.
- `02_TEORIA/06_KPIs/01_que_es_un_kpi.md`.
- `02_TEORIA/07_Python_basico.md`.
- `02_TEORIA/07_Python_basico/04_primera_funcion.md`.
- `02_TEORIA/07_Python_basico/05_texto.md`.
- `02_TEORIA/07_Python_basico/10_condicionales.md`.
- `02_TEORIA/14_PowerBI_DAX.md`.
- `02_TEORIA/14_PowerBI_DAX/01_power_bi_desde_cero.md`.
- `02_TEORIA/INDICE.md`.
- `03_EJERCICIOS/Analitico/AN07.md`.
- `03_EJERCICIOS/Casos/PB02.md`.
- `03_EJERCICIOS/Python/P01.md`.
- `03_EJERCICIOS/Python/P02.md`.
- `03_EJERCICIOS/Python/P03.md`.
- `03_EJERCICIOS/SQL/S1.md`.
- `03_EJERCICIOS/SQL/S2.md`.
- `03_EJERCICIOS/SQL/S4.md`.
- `10_VALIDACION/MANIFIESTO_SHA256.json`.
- `herramientas/aplicar_nucleo.py`.
- `herramientas/verificar_etapa2.py`.
- `INFORME_CIERRE_ORGANIZACION_DIDACTICA.md` (nuevo).

El estado inicial estaba limpio: no había cambios personales pendientes sin commit. El commit de seguridad `a6b20f3` permanece como HEAD en `main`; al cierre las 35 modificaciones y el informe están sin preparar para commit. No se modificó configuración global de Git, historial, ramas, custodia ni trabajo personal.

## Protección y límite del dictamen

Antes de editar se registraron hashes de la instantánea y se respaldaron los archivos afectados en `C:\Users\ASUS\AppData\Local\Temp\organizacion_didactica_ad95m0m3\backup_antes`, además de copias directas de D01/D02. Cada traslado comprobó el contenido actual para evitar sobrescribir cambios concurrentes. Los dos adaptadores de orientación de D01/D02 comprueban también cambios durante su lectura/escritura.

Se conservan exactamente objetivos, ejercicios asignados, fechas, notas y avance de D01/D02. No se modificó `mi_trabajo`, incluidos `mis_funciones.py`, `S2.sql` y `S7.sql`. Tampoco se modificaron materiales UAGRM, datasets, validadores técnicos, custodia, soluciones, evaluaciones, hitos, las nueve lecciones corregidas en Fase 2 ni sus checkpoints Pandas. Los campos de jornadas, actividades iniciales, actividades personalizadas y evaluación final de `nucleo.json` coinciden con el respaldo.

**No queda bloqueo de organización didáctica demostrado.** Excel/Power BI Desktop, SQL Server e importación a Notion mantienen las comprobaciones manuales que corresponden cuando se usen; no se declaran ejecutadas aquí. El procedimiento PB02 se revisó como material, no como una ejecución en Desktop. La exposición histórica del final sigue documentada en Fase 1 y no se reescribió Git.

Las copias de generación/regresión se retiran después de validar; se conservan fuera del repositorio solo los respaldos autorizados y los registros pequeños. La secuencia de estudio queda lista: **guía → teoría → ejercicio autónomo → evaluación**.
