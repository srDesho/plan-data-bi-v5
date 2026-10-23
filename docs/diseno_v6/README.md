# Diseño pedagógico v6 · especificación (Fase 2)

> **Enmiendas de la Fase 3:** ver [ENMIENDAS_FASE3.md](ENMIENDAS_FASE3.md) (RS04 y RS05 pasan a BASE; G1 pasa a D05 y ROUND se enseña en D04: total 9.457 min = 157 h 37 min; excepción autorizada en la evaluación final; correctores SQ13/SQ09). Donde difieran, prevalecen esas enmiendas y `plan_v6.json`.

Estado: **especificación y protección. No se ha modificado ninguna guía, el generador, los enunciados, correctores, contratos de examen ni archivos personales.** Rama `correccion-pedagogica-definitiva`, referencia estable `8168909`. Respaldo externo verificado: `D:\Course Python\Claude\GPT\Respaldos_Plan_Data_BI_v5\8168909_arbol_codex_sin_commit_20261017_2101` (2.409 archivos, 0 discrepancias SHA-256).

## Documentos

| Archivo | Contenido |
|---|---|
| `01_DISTRIBUCION_D01_D42.md` | Tabla de las 42 jornadas, empleo por jornada y sesiones retomables de las que superan su techo |
| `02_LECCIONES_Y_SECUENCIA.md` | Contabilidad de las 100 lecciones, cinco cuestiones de secuencia resueltas, lecciones por día y matriz «enseñar antes de usar» |
| `03_MICROPRACTICAS.md` | Revisión individual de cada micropráctica (apartados obligatorios, integrados y minutos) |
| `04_INVENTARIO_EJERCICIOS.md/.csv` | Clasificación de todos los ejercicios (original, promovido, nuevo, REFUERZO, complementario, examen) |
| `05_ESPECIFICACION_EJERCICIOS_NUEVOS.md` | 26 BASE nuevos y 18 REFUERZO nuevos: finalidad, prerrequisitos, datos, entregable, corrección |
| `06_REFUERZO_Y_COMPLEMENTARIOS.md` | REFUERZO por día, recursos complementarios y banco sin jornada |
| `07_PROGRESO_34_EQUIVALENCIAS.md` + `matriz_34.json` | Matriz individual de las 34 actividades completadas, brechas nuevas y recuperación de S01 |
| `08_GENERADOR_Y_VALIDACIONES.md` | Plan técnico del generador y de las pruebas |
| `plan_v6.json` | Especificación máquina-legible (fuente que leerá el generador en la Fase 3) |
| `obligatorios_originales.json`, `micropracticas.json` | Datos de apoyo |
| `PROTECCION_HASHES.json` | Línea base SHA-256 de los archivos protegidos al inicio de la Fase 2 |

## Cifras

| | Propuesta 1B | Fase 2 | Diferencia |
|---|---:|---:|---:|
| Teoría NÚCLEO (min) | 2.125 | 2.177 | +52 |
| Micropráctica obligatoria (min) | 1.240 (incluía 15 de entorno) | 1.635 | +395 |
| Ejercicios + criterio/hitos + entorno (min) | 3.370 | 3.445 | +75 |
| SQL de recuperación (min) | 245 | 280 | +35 |
| Empleo, cierre y examen (min) | 1.855 | 1.855 | 0 |
| **Total BASE** | **8.835 (147 h 15 min)** | **9.392 (156 h 32 min)** | **+557** |

Martes–viernes: promedio 308 min, máximo 340 min. 27 jornadas superan su techo por 973 min en total; las que pasan de 270 min tienen sesiones retomables. Ningún día normal baja de 210 min.

Qué explica la diferencia con 1B: la revisión apartado por apartado de las microprácticas (+395: la propuesta 1B subestimaba las de Python, Pandas, estadística y BI), las lecciones 8.6, 19.3, 14.4, 11.8, 12.8 y la sección inicial de 14.5 (+52), los ejercicios PT01, KP01, PE01 y PB07 menos el repaso de J2 y con 15 min de entorno ya separados de la micropráctica (+75) y la duración realista de SQ01, SQ02, SQ04, SQ10 y SQ16 (+35).

## Verificación

Con el Python del `.venv` (`.venv\Scripts\python.exe`):

- `herramientas/verificar_diseno_v6.py diseno` — comprueba fechas, minutos, sesiones, clasificación de lecciones, prerrequisitos (declarados y revisados), IDs únicos, obligatorios originales, REFUERZO, SQL frecuente, ausencia de EXTENDIDA, empleo y contratos de los seis exámenes.
- `herramientas/verificar_diseno_v6.py progreso [--carpeta DIR]` — las 34 actividades siguen acreditadas.
- `herramientas/verificar_diseno_v6.py proteccion` — ningún archivo protegido cambió respecto a la línea base.

Estas pruebas comprueban estructura y secuencia; **no sustituyen la revisión semántica de cada enunciado**, que se hace al generar cada jornada (Fase 3).

## Pendiente de aprobación para la Fase 3

1. Crear los 26 ejercicios BASE y 18 REFUERZO nuevos, sus datos, controles y registros de corrector (sin modificar los existentes).
2. Mover la fuente de verdad a `nucleo.json`/`lecciones.json` (esquema v2) y reescribir el generador.
3. Piloto D01–D05 con el formato A–H.
4. Decisiones abiertas: carga (promedio 308 min en martes–viernes), micropráctica (1.635 min), banco de REFUERZO sin jornada, y los dos ejercicios complementarios por prudencia (V2, P20).
