# 08 · Plan técnico del generador y de las validaciones (no implementado)

## Principios

1. Una sola fuente por dato: `nucleo.json` (jornadas), `lecciones.json` (lecciones), registro de progreso y metadatos de ejercicios nuevos. Todo lo demás (guías, RUTAS, CARGA_ESTIMADA, COMPETENCIAS, calendario, README) se **deriva** y se regenera idempotentemente.
2. Cero adaptadores especiales para D01/D02: todas las jornadas pasan por el mismo camino; el progreso viene de un registro por ID, no de leer las casillas de la guía anterior.
3. Sin sello de tiempo ni orden dependiente del sistema: dos ejecuciones seguidas producen bytes idénticos.

## Fuentes que cambian (Fase 3, con aprobación)

| Archivo | Cambio |
|---|---|
| `01_PLAN_DIARIO/nucleo.json` | Esquema v2 generado desde `docs/diseno_v6/plan_v6.json`: por jornada, lecciones (id, parte, lectura, micropráctica y apartados obligatorios), grupos de práctica ordenados por competencia y nivel, SQL de recuperación, criterio, empleo, REFUERZO, sesiones y tipo (normal, lunes, examen, domingo). Se eliminan las listas `refuerzo/opcional/EXTENDIDA` heredadas y las obligaciones «pendientes» incrustadas por Codex. |
| `01_PLAN_DIARIO/lecciones.json` | `tipo` ∈ NÚCLEO · COMPLEMENTARIA · EMPLEO; partes y minutos por parte; se retiran `dia_ext`, `cobertura.por` como criterio de clase y la categoría REFUERZO/PROFUNDIZACIÓN para lecciones. |
| `01_PLAN_DIARIO/progreso_acreditado.json` (nuevo) | Construido desde `matriz_34.json`; el generador lo aplica y nunca marca actividades nuevas. |
| `herramientas/aplicar_nucleo.py` | Renderizadores A–H para jornada normal y lunes; renderizador de examen y de domingo; tabla de sesiones; enlaces validados al construirse; derivados regenerados. Sin sección EXTENDIDA. |
| `03_EJERCICIOS/**`, `herramientas/corregir_*.py`, `CONTRATOS.md` | Solo **se añaden** los 44 ejercicios nuevos y sus registros de corrección; los existentes no se modifican. |

## Formato de salida de cada jornada normal

`# Día NN` · resumen (objetivo, total y sesiones) · **A. Qué estudiar · lecciones NÚCLEO** (todas, con ID, título, enlace, minutos y competencia, antes de cualquier ejercicio) · **B. Distribución neta** (teoría, microprácticas, ejercicios autónomos, SQL de recuperación, comprobaciones, empleo) · **C. Práctica y archivos** (todos los obligatorios juntos, por competencia y de menor a mayor nivel) · **D. REFUERZO — voluntario** · **E. Comprobar y entregar** · **F. REDUCIDO** · **G. MÍNIMO** · **H. Empleo y clase**. Exámenes y domingos conservan su estructura especial.

## Validaciones

| Comprobación | Dónde | Estado |
|---|---|---|
| 42 jornadas, fechas originales, domingos en 0, exámenes sin teoría | `verificar_diseno_v6.py diseno` | implementada |
| Aritmética de minutos y sesiones retomables ≤ 215 min | idem | implementada |
| 100 lecciones clasificadas una vez; NÚCLEO programadas; complementarias no programadas | idem | implementada |
| Prerrequisitos de lección (declarados) y de ejercicio (cabecera + revisión semántica), con excepciones documentadas | idem | implementada |
| IDs accionables únicos; obligatorios originales presentes; REFUERZO sin teoría nueva ni repetición de BASE | idem | implementada |
| SQ01–SQ17 completas, en orden y con SQL en todas las jornadas normales salvo excepciones | idem | implementada |
| Preparación de S01–S06 anterior a cada examen | idem | implementada |
| Las 34 actividades acreditadas | `verificar_diseno_v6.py progreso` | implementada |
| Archivos protegidos sin cambios | `verificar_diseno_v6.py proteccion` | implementada |
| Orden de secciones A–H, ausencia de EXTENDIDA y teoría antes de ejercicios **en el Markdown generado** | verificador de guías | Fase 3 |
| Enlaces Markdown existentes y anclas válidas | verificador de guías | Fase 3 |
| Tabla «Distribución neta» igual a la suma de las actividades de la guía | verificador de guías | Fase 3 |
| Regeneración idempotente (dos ejecuciones, cero bytes distintos) | prueba de regeneración | Fase 3 |
| Mutaciones: mover una lección tras su ejercicio, duplicar un ID, borrar una casilla `[x]`, alterar un tiempo, añadir EXTENDIDA | pruebas de mutación | 14 sobre la especificación ya hechas; las de guías en Fase 3 |
| Exámenes, proyectos, correctores y datasets con el mismo hash | `proteccion` | implementada |

## Qué se reutiliza del trabajo sin confirmar de Codex

Solo el *enfoque* de pruebas (integridad por ID, mutaciones, idempotencia, línea base de hashes). No se reutilizan sus guías, `nucleo.json`, `lecciones.json` ni `aplicar_nucleo.py`; algunas de sus lecturas previas de teoría pueden aprovecharse tras revisarlas una a una en la Fase 3.

## Orden propuesto y puntos de parada

Fase 3: ejercicios nuevos de D01–D05 → fuentes v2 → generador → piloto D01–D05 → **parada**. Fase 4: semanas completas con revisión entre ellas. Fase 5: regresión final. Ningún commit ni push sin aprobación.
