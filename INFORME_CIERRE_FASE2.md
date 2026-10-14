# Cierre definitivo · Fase 2 · Plan Data & BI v5

Fecha: 14 de octubre de 2026. Rama `main`, HEAD `6ac1af8`. Trabajo en el repositorio original, conservando los cambios de Fase 1 sin commits ni push.

**Dictamen: APROBADO CON OBSERVACIONES NO BLOQUEANTES. El proceso de construcción queda terminado; el Plan está listo para estudiar.** Las observaciones son las pruebas manuales pendientes, la exposición histórica documentada y los cambios concurrentes de progreso personal descritos al final. No justifican otro rediseño.

## Revisión de los 17 prerrequisitos

La lista corresponde exactamente a los 17 pares de la sección 6 de `INFORME_FASE2_ETAPA2_CALENDARIO.md`. Se contrastó con las fuentes, los enunciados, la teoría y las modalidades actuales. «Primera actividad» identifica la primera tarea que debe entregar o demostrar el alumno; la preparación puede enseñarse antes de ella en la misma jornada. Lo exigido **al entrar** debe proceder de una jornada anterior.

Resultado: **2 CUBIERTO, 11 ACLARACIÓN NECESARIA y 4 INTEGRACIÓN NECESARIA**. Son clasificaciones del problema encontrado; las cuatro integraciones ya están aplicadas. No se reclasificó ninguna lección completa: permanecen **47 NÚCLEO, 33 REFUERZO y 20 PROFUNDIZACIÓN**.

| Prerrequisito | Competencia | Primera actividad obligatoria que lo necesita | Preparación anterior | Clasificación | Corrección aplicada | Impacto en minutos |
|---|---|---|---|---|---|---|
| 3.2 ← 3.1 | Claves primaria/foránea, lado único y cardinalidad | J2, D09 | Agregación previa; ahora 3.2 define claves y exige comprobar unicidad antes de unir | INTEGRACIÓN NECESARIA | Definiciones y comprobación en `03_SQL_joins/02_inner_join.md`; relación venta→tienda corregida a N:1. REDUCIDO conserva 3.2 y J2 | +5 lectura |
| 3.4 ← 3.1 | Detectar multiplicación por una clave repetida | J2 D09; aplicación en J5 D11 y P21 D17 | 3.2 y J2 D09 preparan claves, conteos y sumas antes de 3.4 | ACLARACIÓN NECESARIA | Cobertura por J2; se deja de acreditar J1 REFUERZO. Si se omite 3.4, recuperar su control antes del merge completo/P3 | 0 |
| 4.2 ← 4.1 | Usar un resultado intermedio con nombre | V3, D18 | 4.2 enseña WITH y pasos antes de V3; no exige resolver subconsultas anidadas | CUBIERTO | Se conserva 4.1 REFUERZO. REDUCIDO practica el CTE y deja ventanas pendientes antes de P3 | 0 |
| 5.3 ← 10.5 | Validar reglas y reconciliar filas/rechazos/importes | P21 D17 parcialmente; reconciliación integral ME03 D24 | P21/P22; 19.3 D20 explica validar y conteos; ME02 D23 prueba filas calculadas a mano | ACLARACIÓN NECESARIA | Cobertura anterior por 19.3 y ME02; ME03 se identifica como práctica del día. Su REDUCIDO no acredita P4 sin validar/Gold | 0 |
| 6.6 ← 6.3 | Interpretar importe por pedido, hechos y límites | K1/AN08 D16; recomendación AN18 D39 | K1 y AN08 calculan e interpretan pedidos; PB03 D33 practica ticket | ACLARACIÓN NECESARIA | Nota de alcance corregida: 6.6 no exige todo el repertorio de 6.3. Si se pospone 6.6, recuperarla antes de AN18 | 0 |
| 9.2 ← 9.1 | Reconocer Series/DataFrame y cargar una tabla | P17, D15 | CSV estándar D10; 9.2 explica directamente tablas, columnas, tipos y operaciones | ACLARACIÓN NECESARIA | NumPy pasa explícitamente a consulta opcional. 9.2 se lee en D12; D15 exige recuperarla si se omitió en REDUCIDO | 0 netos: 20 de D15 a D12 |
| 10.1 ← 9.1 | Operar sobre columnas sin exigir arreglos NumPy | PD-BASE D16; columnas usadas al entrar a D17 | 9.2 D12 introduce operaciones por columna; 10.1 explica sus usos de NumPy | ACLARACIÓN NECESARIA | Requisitos concretos, sin exigir «capítulo 9 completo» ni promover 9.1. REDUCIDO recupera PD-BASE antes de D17 | 0 |
| 10.1 ← 9.4 | Seleccionar columnas, construir máscaras y trabajar con copias | PD-BASE D16, antes de P22 y P21 | Nuevo puente al inicio de 10.1, leído antes de 9.5; demostración sobre tres filas inventadas | INTEGRACIÓN NECESARIA | PD-BASE exige predecir, seleccionar, filtrar y preservar el origen. D17 acredita esa práctica, no solo la lectura. 9.4 sigue REFUERZO | +15 compartidos con 9.6: 5 lectura y 10 práctica |
| 10.1 ← 9.6 | Convertir números/fechas y reconocer NaN/NaT | PD-BASE D16, antes de las transformaciones posteriores | P09–P11 aportan conversiones escalares; el puente enseña conversiones por columna, formato y faltantes | INTEGRACIÓN NECESARIA | Mismo checkpoint exige detectar inválidos con causa y derivar importe/mes solo de válidos. P24 REFUERZO no se usa como preparación | 0 adicionales: incluidos en la fila anterior |
| 10.3 ← 3.1 | Unir muchos a uno, detectar catálogo repetido y huérfanos | P21, D17 | 3.2/J2 D09, AN05 D10, 3.4/J5 D11 y PD-BASE D16; 10.3 enseña validate/indicator antes de P21 | ACLARACIÓN NECESARIA | Prerrequisitos precisados; groupby no es condición para unir. REDUCIDO recupera huérfanos y agrupación antes de H03/S03 | 0 |
| 11.3 ← 11.1 | Declarar la observación y elegir media/mediana/moda | AN08, D16 | AN01 D03 enseña unidad de análisis; G6 frecuencias; 11.3 D13 enseña las medidas que AN08 calcula | ACLARACIÓN NECESARIA | No se atribuye población/muestra a AN01 ni se exige inferencia. Entrada D16 obliga a recuperar 11.3 si se omitió en D13 reducido | 0: lectura ya presupuestada |
| 13.2 ← 13.1 | Distinguir hecho/dimensión, medidas/contexto y grano | PB01/PB02, D32 | Claves, uniones y ETL previos; ahora 13.2 introduce y comprueba los conceptos antes del diagrama | INTEGRACIÓN NECESARIA | Definiciones y clasificación activa en 13.2. 13.1 sigue REFUERZO; D32 exige recuperar 13.2 si se omitió en D30 reducido | +5 lectura |
| 15.3 ← 15.2 | Crear tabla dinámica y cuadrar con SQL | EX01, D31 | 15.3 D29 enseña importación/pivot/cuadre; E4 aporta SQL | ACLARACIÓN NECESARIA | SUMAR.SI/BUSCARX quedan como ampliación. Entrada D31 exige 15.3 para EX01; REDUCIDO puede hacer E4 y posponer Excel sin acreditar P6 | 0 |
| 16.2 ← 16.1 | Documentar ejecución, reglas, errores y límites | ETL-6 D30; ampliación C06-4 D40 | Plantilla README existente, ahora enlazada en ETL-6; 16.2 enseña documentación de forma autosuficiente | ACLARACIÓN NECESARIA | Git no es requisito funcional del README ni una casilla prueba enseñanza. REDUCIDO D40 reutiliza README/plantilla; publicación/versionado consultan 16.1 | 0: se enlaza la plantilla dentro de la tarea existente |
| 17.1 ← 10.5 | Adaptar controles y planificar un ETL distinto | C06-0, D36 | 19.3 D20, ME01–ME03 D22–24, 5.3, ETL-4/ETL-6 D29–30 y P5 | CUBIERTO | Mantener 10.5 REFUERZO y dejar explícita la preparación efectiva. Recuperar los cuadres del contrato antes de transformar/acreditar P7 | 0 |
| 17.2 ← 8.7 | Probar normal/límite/inválido y reducir un error | P09 D10; ME02 D23 y C06-1 D37 | 8.1 D08 enseña casos y assert; DB01 D09, P09 y ME02/03 exigen pruebas y explicación | ACLARACIÓN NECESARIA | Cobertura por P09/DB01/ME02; DB02/DB03 REFUERZO no acreditan preparación. Puertas P2/P4 obligan a recuperar lo omitido | 0 |
| 17.2 ← 10.6 | Detectar errores silenciosos con cardinalidad, tipos y cuadres | P21 D17; H03 D20 y ME03 D24 | 9.5/P22, 10.3/P21, H03, ME02/03 y ETL-6 D30 demuestran controles reales | ACLARACIÓN NECESARIA | Sustituir DB02/DB03/C05 por evidencias obligatorias. REDUCIDO recupera huérfanos antes de P3 y cuadres antes de P4/P5 | 0 |

Los pares eliminados del encabezado de una lección no desaparecen de esta revisión histórica. El generador actual registra tres lecturas recomendadas restantes; su suficiencia se revisó aquí, no se dedujo del simple estado «recomendada».

## Preparación Pandas y modalidades

- Selección/filtros, conversiones, faltantes y columnas: **10.1 + PD-BASE D16**, con predicción, inválidos trazables y origen intacto, antes de P22/P21.
- Agrupación: **10.2 + PD-AGR D17**, sin depender todavía de merge; agrupar y reconciliar antes de P21 y H03. Esta práctica de **10 minutos** complementa la matriz anterior y explica el incremento restante de carga.
- Uniones: **10.3 + P21 D17**; catálogo repetido y huérfanos. Los ejemplos de 10.2 que integran merge se retoman después de 10.3.

Los checkpoints se identifican dentro de las microprácticas: 10 min BASE y 25 min REFUERZO en 10.1; 10 min BASE y 30 min REFUERZO en 10.2. La guía cuenta esos 20 min una sola vez como ejercicios, nunca también como lectura. REDUCIDO mantiene una entrega menor y declara qué recuperar antes de cada puerta; no acredita lo omitido.

S01–S06 y H01–H08 conservan contratos, puntuación y umbrales. AN08/AN13 siguen exigiendo cálculo e interpretación descriptivos; ST01/ST02 siguen REFUERZO. No se añadió un examen de estadística.

## Carga resultante

**90 h BASE planificadas**; **5.771 min = 96,18 h (96,2 h redondeadas) estimadas**, frente a 5.736 min anteriores. Incremento: **35 min** = 15 de lectura (claves SQL, puente Pandas y modelado: 5 cada uno) + 20 de práctica obligatoria (dos checkpoints). No se redujeron los tiempos de los ejercicios existentes.

Mover 9.2 de D15 a D12 tras CSV (D10) redistribuye 20 min reales entre semanas, sin eliminar lectura ni añadir una obligación nueva. El movimiento respeta conversiones D08 y archivos D10. D15 conserva 9.3 y P17; la recuperación explícita protege la modalidad REDUCIDA.

| Semana | Plan BASE, min | Estimación anterior, min | Estimación final, min |
|---|---:|---:|---:|
| 1 | 900 | 956 | 956 |
| 2 | 900 | 943 | 968 |
| 3 | 900 | 972 | 977 |
| 4 | 900 | 960 | 960 |
| 5 | 900 | 970 | 975 |
| 6 | 900 | 935 | 935 |

La evaluación final conserva **570 min = 9,5 h posteriores**, fuera de las seis semanas. Total: **99,5 h de plan y 105,7 h estimadas**, UAGRM aparte. Son estimaciones de primera vez con margen de ±35 %, no mediciones ni promesas de terminar en fecha. Si falta una base o una puerta, se recupera y se corre la secuencia sin acumular horas.

## Archivos modificados en esta fase

- Fuentes: `01_PLAN_DIARIO/nucleo.json`, `lecciones.json`.
- Derivados: `calendario.json/csv`, `CARGA_ESTIMADA.md`, `RUTAS.md` y guías **D09, D12, D15, D16, D17, D20, D30 y D31**.
- Lecciones: **3.2, 9.2, 10.1, 10.2, 10.3, 11.3, 13.2, 15.3 y 16.2**; índices de capítulos **3, 9, 10 y 13**, más `02_TEORIA/INDICE.md`. Son integraciones o referencias puntuales, no una reconstrucción de las 100 lecciones.
- Herramientas: `aplicar_nucleo.py`, `verificar_etapa2.py`, `pruebas_mutaciones_ruta.py` y `controles_examenes.py`.
- Evidencia/cierre: `10_VALIDACION/resultados_pruebas.json`, `MANIFIESTO_SHA256.json`, `PROGRESO_FASE2.md` y este informe.

El generador reconoce los dos checkpoints, distingue sus minutos BASE/REFUERZO y sincroniza tiempos de índices. Una prueba previa detectó que desmarcaba dos casillas de D02; el traslado se detuvo antes de tocar el original. Se corrigió la preservación de casillas. Los subprocesos aislados de comprobación conservan TEMP/TMP y usan `-B`: así sus fixtures no se crean en el repositorio y no escriben bytecode. Se retiraron únicamente dos fixtures temporales propios identificados; no se borró trabajo personal.

## Pruebas realmente ejecutadas

Entorno: `.venv`, **Python 3.12.10**, pandas **2.2.3**. Custodia externa disponible; no se copió ni se publicaron sus respuestas. Se usaron copias/salidas temporales y `PYTHONDONTWRITEBYTECODE=1`.

| Verificación | Resultado |
|---|---|
| Generador en temporal, seguido de sincronización de derivados | D01/D02 idénticos a la instantánea contemporánea; solo se trasladaron derivados diferentes autorizados |
| `verificar_etapa2.py` en original | **9/10**: nueve grupos pedagógicos correctos; el control Git personal detectó cambios concurrentes en `mi_trabajo` |
| `verificar_etapa2.py` dentro de la suite temporal | **10/10**, con comparación Git omitida explícitamente por ser copia sin `.git`; no se confunde con prueba de integridad personal |
| `pruebas_mutaciones_ruta.py` | **14/14** incoherencias detectadas: 12 anteriores y dos que eliminan PD-BASE/PD-AGR |
| `verificar_paquete.py` completo, copia temporal sin `.venv`/`.git` | **26/26 grupos OK, 0 fallos, 0 omisiones**: los 24 anteriores y dos de privacidad |
| Teoría, dentro de la suite completa | **7/7 grupos**, **621 bloques ejecutados**; formato, enlaces, tiempos, términos, glosario y fugas correctos |
| Regresión técnica de Fase 1, dentro de la suite completa | **3 referencias aprobadas, 50 alteraciones rechazadas** (45 anteriores + cinco NULL Gold); privacidad conservada |
| Exámenes/hitos dentro de Etapa 2 | Seis exámenes, ocho hitos y 35 controles recalculados; AN/H mantienen 42 cifras de control |

La evidencia pública se sustituyó por la corrida completa saneada. Comprobaciones finales ejecutadas:

- Tabla: **17 filas únicas**, mismos 17 pares históricos, siete columnas completas, clasificaciones 2/11/4 y suma de impacto de 35 min incluyendo la práctica complementaria de agrupación.
- Contabilidad: 5.400 min de plan, 5.771 estimados, 1.197 de lectura y 2.399 de ejercicios; evaluación posterior de 570 min. Las fuentes y los documentos derivados coinciden.
- Manifiesto: regenerado y comprobado, **590 archivos, «Manifiesto vigente»**.
- `git diff --check`: **código de salida 0**. Los avisos LF/CRLF de Git no son errores de espacios ni cambios aplicados por el comando.
- Integridad: D01, UAGRM y los diez archivos de custodia sin cambios respecto del inicio; privacidad pública comprobada sin filtraciones detectadas.

## Protección, límites y estado final de Git

D01, UAGRM y la custodia se contrastan por SHA256 con la instantánea inicial; sus contenidos no se modifican. No se editaron los archivos de la evaluación privada ni sus validadores técnicos de Fase 1 durante esta fase.

Durante la sesión aparecieron cambios externos en **D02**, `mi_trabajo/python/mis_funciones.py`, `mi_trabajo/sql/S2.sql` y `mi_trabajo/sql/S7.sql`. Se preservan íntegramente: no se revierten, corrigen ni incorporan a las modificaciones del currículo. Por ello no se declara que todo el árbol personal sea idéntico al inicio ni que el control Git del original haya aprobado. Cada traslado del generador excluyó estrictamente D01 y D02.

Permanecen pendientes de ejecución manual **Excel, Power BI Desktop (M/DAX/relaciones/actualización), SQL Server e importación a Notion**. Las simulaciones y los ejemplos ejecutados no equivalen a usar esas aplicaciones. La aprobación del material tampoco acredita la autonomía del alumno: esa evidencia sigue dependiendo de sus entregas y defensa.

La exposición histórica de resultados del final en `6ac1af8` permanece documentada en `INFORME_CIERRE_FASE1.md`; sanear la evidencia actual no borra ese historial ni convierte la custodia en una prueba ciega. No se modificó el historial Git.

Rama `main`, HEAD `6ac1af8`, sin commits, push ni ramas nuevas y nada preparado para commit. Al cierre, Git muestra **41 archivos rastreados modificados y seis nuevos**: incluye cambios de ambas fases y los cuatro cambios concurrentes personales identificados. La Fase 2 aporta 36 archivos modificados/nuevos respecto del cierre de Fase 1, excluidos los cambios externos. El usuario decide qué revisar y guardar. **No queda otra fase de construcción propuesta.**
