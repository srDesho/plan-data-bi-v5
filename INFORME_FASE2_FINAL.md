# Informe final de la Fase 2 · Etapa 3

Fecha: 2026-10-14. Rama `main`, HEAD `559e612`. Sin commits, push ni operaciones destructivas de Git. `mi_trabajo`, D02 y el contenido de D01 sin tocar (las casillas marcadas en D01 y D02 son progreso del estudiante, no cambios míos).
Entorno de todas las pruebas: Windows 11 (10.0.26200), `.venv` con Python 3.12.10, pandas 2.2.3, numpy 2.3.5, SQLite 3.49.1.

## 1. Dictamen

**APTO PARA CONTINUAR.** El material está listo para estudiar: los validadores rechazan los resultados incorrectos conocidos, los prerrequisitos y las modalidades son coherentes, la carga declarada corresponde al trabajo exigido (con su margen explícito), los exámenes evalúan lo practicado y la evaluación final comprueba transferencia con un contrato distinto.

Esto acredita que **el material está preparado**, no que **tú ya eres autónomo**: eso solo lo acreditan tus evaluaciones resueltas y defendidas (sección 7). No queda ningún bloqueo para empezar (sección 8).

## 2. Cambios y hallazgos priorizados (10)

| # | Problema resuelto | Dónde | Evidencia |
|---|---|---|---|
| 1 | **Falsos positivos de los validadores.** Aprobaban un Gold con clientes inexistentes, meses inválidos y documentos alterados; dos importes de Silver cambiados en sentidos opuestos; y un Gold del ETL guiado con ventas permutadas. La causa: comparaban conteos y sumas, y la Silver esperada ni siquiera incluía `monto_centavos`. | `herramientas/validacion_comun.py`, `validar_final.py`, `validar_etl_distribuidora.py`, `construir_huellas.py`; huellas en `08_SOLUCIONES/huellas_c06.json`, `huellas_etl_distribuidora.json` y `09_EVALUACION_FINAL/verificacion/huellas_final.json` | Ahora revisan Bronze (texto exacto), Silver fila por fila y con la fórmula del importe, Gold recalculado desde tu propia Silver y comparado con el esperado, CSV frente a SQLite, auditoría y entrada intacta. Ejecutados con los validadores **antiguos** (`git show HEAD`), las alteraciones aprobaban; con los nuevos: 45 de 45 alteraciones rechazadas y 3 de 3 referencias correctas aprobadas (`pruebas_validadores.py`). |
| 2 | **Prerrequisitos que se contradecían.** D04 exigía dominar un bucle con acumulador «aprendido en D03»; D05 exigía WHERE/HAVING antes de 2.2; D09 pedía explicar `raise` antes de 8.5; D11 exigía LEFT JOIN y leer un traceback que se enseñan ese día; además `G1` (GROUP BY) estaba en D04 y 2.2 en D05. | `01_PLAN_DIARIO/nucleo.json` (campo `entra`), `lecciones.json`, 34 guías regeneradas | Cada requisito de entrada cita una lección NÚCLEO o un OBLIGATORIO de una jornada **anterior** y el generador se niega a producir la guía si no es así. G1 pasó a D05; D04 usa G3, que además era el comparador de J2. |
| 3 | **Modalidad REDUCIDA que no era realizable.** D17 mantenía P21 sin leer 10.3 (`merge`); D05 conservaba P07 sin 7.12/7.13. En las 34 jornadas el REDUCIDO era el mismo ejercicio con menos minutos y la frase genérica «SQL 15 + teoría 10…». | `nucleo.json` (`reducido_lecciones`, `reducido_min`, `reducido_entrega`), `aplicar_nucleo.py`, tabla «Modo REDUCIDO de cada jornada» en `RUTAS.md` | Cada jornada define una lectura mínima y una **entrega menor**, qué pasa a REFUERZO y qué no acredita. El generador exige que el REDUCIDO incluya las lecciones del día que cita su ejercicio y que sume ≤ plan + 10 min. MÍNIMO ya no promete contenido nuevo. |
| 4 | **Dependencias ocultas.** 3 REFUERZO colocados antes de la lección que citan (P14, P18, P27) y otro (CL3); S01 evaluaba AND/BETWEEN y C01, que solo eran REFUERZO u OPCIONAL; simulacros, AN02/03/05/15 apoyados en G1/G5/J1/C0x. | `nucleo.json`, `AN02/03/05/15`, `06_ENTREVISTAS/SIMULACRO_01–05`, `lecciones.json` (1.3 cubierta por S4, ahora OBLIGATORIO) | `auditar_enunciados.py` (7 grupos): la tabla de preparación de cada examen y cada simulacro solo cita lo preparado; control negativo ejecutado (detecta P20 y G1 inyectados). |
| 5 | **Promesa de SQL diario sin actividad exigible** (D08, D12, D22…). | `RUTAS.md` (tabla «SQL por semana»), `COMPETENCIAS.md`, guías | Según tu aclaración: sin obligación artificial. Hay SQL exigible o integrado (examen, ETL-6, C06-4) donde corresponde y repaso opcional de 10 min en D08, D10, D12 y D17, que no suma a la carga. |
| 6 | **Carga mal declarada.** CARGA_ESTIMADA daba 99,2 h frente a 90 h; D17 estimaba 195 min y D25 190 sobre 150; había dobles conteos (N2, N3, V4 sumados además de los 60 min de examen: 116 min). | `CARGA_ESTIMADA.md`, `nucleo.json` | Ahora **95,6 h estimadas** frente a 90 h (razón 1,06; semanas entre 1,04 y 1,08); D17 170 min, D25 170 min. Se movieron a REFUERZO S3, G5, J1 y P20 (cuya idea comprueba H03). Las jornadas por encima de 1,15 (D03, D10, D24, D30, D31, D32, D40) tienen REDUCIDO definido. Todo es estimación de primera vez, no medición. |
| 7 | **Exámenes S01–S06 sin trazabilidad.** | `03_EJERCICIOS/EXAMENES/S01–S06.md`, `herramientas/controles_examenes.py`, `08_SOLUCIONES/controles_examenes.json/.md` (35 controles) | Cada examen tiene la tabla competencia → preparación obligatoria → tarea → evidencia → puntos (suman 100), puntuación parcial, mínimo del 60 % por competencia, fallos críticos, variantes nuevas, diagnóstico de errores, predicción, y para cada fallo la base concreta y una variante de recuperación. Umbral de S03 unificado en 75. S05 puntúa aparte ETL (56/75) y BI (19/25, lo no ejecutado vale 0). |
| 8 | **Hitos que se aprobaban sin resolver la variante** (3 de 4 criterios); H06 pedía `ventas_centavos` en un ETL que usa `ventas_bs` y `monto`. | `03_EJERCICIOS/Comprension/H01–H08.md`, `COMPETENCIAS.md` | A (variante resuelta y comprobada) y B (explicación de tu solución) son necesarias, más dos de tres valoraciones; añadida la regla de autoría. H06 usa el esquema real y explica las unidades (Bs con dos decimales frente a centavos). |
| 9 | **Final = C06 con más filas** (misma referencia resolvía ambos) y con la solución dentro del paquete. | `09_EVALUACION_FINAL/` (ENUNCIADO, RUBRICA, `datos/despachos_raw.csv`, `articulos.csv`, `DICCIONARIO.md`), custodia fuera del paquete | Contrato nuevo: clave compuesta `(nro_doc, item)`, fecha compacta, precio con miles, descuento con redondeo al centavo, estado `devuelto`, Gold por sucursal/mes/línea. Debes escribir una transformación nueva, adaptar una regla y reparar un error en la defensa. La referencia, el generador y la verdad están en `Plan_Data_BI_v5_CUSTODIA_FINAL` (fuera del repositorio); la referencia reproduce la verdad calculada de los datos limpios. |
| 10 | **Afirmaciones técnicas erróneas.** | `02_TEORIA/01_SQL_basico/03_where_operadores.md`; `02_TEORIA/14_PowerBI_DAX/03_dax_contexto.md` | `==` **no** da error en SQLite 3.49 (comprobado); sí en otros motores. En DAX, un filtro de `CALCULATE` sobre una columna ya filtrada **sobrescribe** el existente, no lo intersecta; `KEEPFILTERS` es la excepción (documentación de Microsoft, función CALCULATE). La lección declara el alcance de la simulación en Python y que DAX no se ejecutó. |

## 3. Carga BASE resultante y tratamiento de la evaluación final

| | Plan | Estimado de primera vez |
|---|---:|---:|
| Seis semanas (42 jornadas) | 90,0 h | **95,6 h** (15,6–16,2 h por semana) |
| Evaluación final (23–30 nov), **posterior y no incluida en las 90 h** | antes 12,5 h → ahora **9,5 h** | 9,5 h |

- La evaluación final es una **séptima semana de evaluación explícita** (570 min); no se disfraza dentro de las 90 h ni se añade otra semana obligatoria. La reducción de 180 min viene de reutilizar tu propio código de C06 (extracción, Bronze, pruebas básicas, carga repetible) en vez de construirlo dos veces; el detalle por día está en `CARGA_ESTIMADA.md` y en el ENUNCIADO (comprobado por `verificar_etapa2.py`).
- La incompatibilidad que sí queda: no se puede integrar dentro de las 42 jornadas porque los datos se abren el 23 y D41 está ocupado por S06. Si no puedes dedicar esas 9,5 h, se reprograma sin acumular horas.
- Las horas voluntarias (EXTENDIDA) no se usan como requisito encubierto.

Cobertura efectiva (disponible → practicado → evaluado):

| Área | Disponible | Practicado en BASE | Evaluado |
|---|---|---|---|
| SQL | 20 lecciones (11 NÚCLEO) | 15 ejercicios OBLIGATORIO/REPASO | S01–S03 (ES1–ES3, variantes), N2, N3, V4 |
| Python y Pandas | 32 lecciones (18 NÚCLEO) | P01–P11, P13, P17, P21–P23 | S01, S02, S03 |
| ETL | 8 lecciones | ME01–ME03, ETL-1…6, C06-0…4 | S04, S05, S06 y la final |
| KPIs y estadística descriptiva | 6 + 9 lecciones | AN04–AN18 (con cifras de control); sin ejercicio ST obligatorio | S01 (cumplimiento), N3 (efectividad); media/mediana/dispersión/percentiles/ABC solo con rúbrica y controles de AN/H, **sin examen propio** |
| Inferencia estadística | 8 lecciones | — | no se evalúa (PROFUNDIZACIÓN) |
| Excel y Power BI | 3 + 8 lecciones | EX01, PB01–PB03 | S05 Parte B (PENDIENTE si no hay herramienta) |

## 4. Pruebas ejecutadas

**Comprobado por ejecución** (todas con el `.venv`; las que escriben se corrieron en copias temporales):

| Comando | Resultado |
|---|---|
| `herramientas/verificar_paquete.py` (copia temporal del paquete, con custodia) | **24 de 24** pruebas OK, 0 fallos (incluye validadores, ETL de C06, final con referencia privada, adversas, notebooks, enlaces y manifiesto) |
| `herramientas/verificar_etapa2.py` | **10 de 10** grupos OK (nuevo grupo: exámenes, hitos y evaluación final) |
| `herramientas/pruebas_mutaciones_ruta.py` | **12 de 12** incoherencias inyectadas detectadas (umbral, puntos, hitos, H06, calendario de la final, rúbrica, control alterado, requisito del mismo día, REDUCIDO sin lección, guía y carga editadas a mano, lección con otro día) |
| `herramientas/pruebas_validadores.py --custodia …` | 3 referencias correctas aprueban; **45 alteraciones rechazadas** (C06 16, ETL guiado 11, final 18), incluidas las tres de la auditoría |
| `herramientas/auditar_enunciados.py` | 7 grupos OK (81 SQL, 30 Python, 29 otros, fugas, dependencias y exámenes, custodia, índices) |
| `herramientas/verificar_teoria.py` | 7 grupos OK (620 bloques de ejemplo ejecutados) |
| `herramientas/prueba_sqlite_cierre.py` | 5 de 5 grupos (renombrar y borrar sin WinError 32) |
| `herramientas/controles_examenes.py --comprobar` | 35 controles recalculados |
| `herramientas/regenerar_manifiesto.py --comprobar` | vigente (588 archivos) |

Se conservan las pruebas de segunda ejecución sin duplicación, duplicados exactos frente a conflictos, catálogo ambiguo, cantidad fraccionaria, rechazos trazables y preservación de la salida anterior ante un fallo estructural, ahora también sobre la referencia del final.

**Comprobado por inspección, no por ejecución:** el manejo de rutas y de fin de línea para Linux (`as_uri`, hashes con CRLF normalizado); no se ejecutó nada en Linux, así que **no declaro reproducido un 21/21 en ese sistema**. Las dos diferencias que viste en Linux (representación de rutas de Windows y fin de línea de un JSON reescrito) se trataron como diferencias de plataforma, no pedagógicas.

**Pendiente de prueba manual (no ejecutado):** Excel (EX01, tablas dinámicas), Power BI Desktop (M, relaciones, filtros, medidas DAX y actualización; `05_PROYECTOS/powerbi/VALIDACION_MANUAL.md`) y los ejemplos de SQL Server. Una simulación en Python o la lectura del código **no** equivalen a esas ejecuciones.

**Estimado pedagógicamente (no medido):** todos los minutos de `CARGA_ESTIMADA.md`, los del modo REDUCIDO y los 9,5 h de la evaluación final.

## 5. Decisiones y límites que debes conocer

- **La custodia no es una prueba ciega por sí misma.** La carpeta `D:\Course Python\Claude\GPT\Plan_Data_BI_v5_CUSTODIA_FINAL` está en tu disco, junto al paquete. Solo es custodia si la guarda **otra persona** hasta tu defensa. Las huellas dicen qué claves coinciden, no los valores, pero podrían contrastarse con valores adivinados. Si no hay otra persona, la prueba mide cumplimiento del contrato y honestidad declarada; el ENUNCIADO lo dice y no se debe presentar como ciega.
- Los exámenes S01–S05 son puertas formativas de honor con explicación oral; solo la final tiene huellas y observador.
- **Archivos retirados:** `09_EVALUACION_FINAL/datos/transacciones_raw.csv` y `catalogo.csv`, `08_SOLUCIONES/controles_final.json` y `silver_final_esperada.csv` (el final antiguo). Siguen en el historial de Git (`git show 559e612:…`).
- **Cambios que no pediste por nombre:** `P20` pasa a REFUERZO (su idea se comprueba con la variante de H03); `S3`, `G5` y `J1` pasan a REFUERZO por repetir lo que hacen S7, G6 y J2; `S4` y `G3` pasan a OBLIGATORIO; `11.4`, `11.5`, `6.2`, `2.5`, `19.1` cambian de día. No se modificó ninguno de los 81 enunciados SQL ni ningún enunciado de Python.
- ST01/ST02 siguen en REFUERZO (decisión abierta de la Etapa 2): la estadística descriptiva se practica con AN08/AN13 y se evalúa con rúbrica y cifras de control, no con un examen.
- D01 y D02: solo cambian porque marcaste casillas; `verificar_etapa2.py` ahora lo tolera y sigue comprobando que su contenido es el original.
- No comparé este paquete con los ZIP de la carpeta superior; trabajé sobre los contenidos reales del repositorio.

## 6. Qué pasa si fallas una evaluación

No se repite la semana por defecto. Cada examen (S01–S06) y la rúbrica final traen una tabla «si fallaste X → recupera esta base → demuestra con esta variante nueva (20–30 min)»; las cifras de esas variantes están en `08_SOLUCIONES/controles_examenes.md`.

## 7. Criterio para declarar tu autonomía

Se declara autonomía en esta etapa solo si se cumplen **todas**:

1. S06 con 80/100 y sin puerta crítica, y los S01–S05 aprobados con sus umbrales (70, 70, 75, 75 y 56/75) y sin fallo crítico.
2. Hitos H01–H08 cumplidos con la variante resuelta y la explicación de tu solución.
3. `validar_final.py` sin fallos sobre la evaluación final (una sola ejecución, al cerrar la entrega).
4. Rúbrica final ≥ 80/100 sin puertas críticas (dinero, filas perdidas, segunda carga, explicar el código, ayuda no declarada).
5. Defensa superada en sus cuatro pasos delante de otra persona: explicar, anticipar, reparar y modificar en vivo.
6. Ninguna ayuda externa sin declarar. Si la hubo, esa parte se repite con otra variante.

## 8. Bloqueos y mejoras opcionales

**Bloqueos reales para empezar: ninguno.**

**Antes de la evaluación final (no bloquean el estudio):** entregar la carpeta de custodia a otra persona; decidir quién será el observador de la defensa; tener Excel y Power BI Desktop si quieres que la Parte B de S05 no quede pendiente.

**Mejoras opcionales (no abrir otra ronda):** medir tus minutos reales durante dos semanas y corregir `CARGA_ESTIMADA.md`; si la semana 5 resulta pesada, usar REDUCIDO en D30–D32; añadir un examen de estadística descriptiva si más adelante lo quieres como competencia evaluada.
