# Auditoría exhaustiva · Plan Data & BI v5

Fecha de la auditoría: 13 de octubre de 2026 (Día 2 del plan). Auditoría de solo lectura: **no se modificó ningún archivo del plan**. Las pruebas que escriben archivos se ejecutaron sobre una copia en un directorio temporal.

Convenciones: **[MEDIDO]** = lo comprobé ejecutando algo. **[LEÍDO]** = lo comprobé leyendo archivos. **[ESTIMADO]** = inferencia mía con supuestos declarados. **[NO VERIFICADO]** = no pude comprobarlo.

---

## A. Resumen ejecutivo

**¿Es viable el Plan v5 para ti tal como está? No. ¿Es viable corregido? Sí, con cambios acotados.**

Lo que está bien, con evidencia:

- El paquete es técnicamente sólido. Recalculé de forma independiente (Pandas sobre los CSV, sin usar las consultas SQL de referencia) 12 controles de negocio y todos coincidieron. Los hashes SHA256 de los 403 archivos del manifiesto coinciden. Los 389 enlaces internos funcionan y no hay archivos vacíos. **[MEDIDO]**
- La secuencia es sensata: SQL desde el día 1 y presente en las 6 semanas; Python antes de Pandas; los KPIs se definen antes de calcularse; la limpieza de datos preserva el original; hay rechazos con motivo; y el diseño admite abiertamente que ejecutar la referencia no prueba tu aprendizaje.
- El CV y las entrevistas te piden ser honesto sobre el apoyo de IA en la pasantía. Eso es correcto y poco común.

Lo que no está bien:

1. **La carga real supera con mucho las 15 h/semana, sobre todo en las semanas 4 y 5.** Mi estimación central es de 1,2× a 2,1× lo planificado según la semana, y la optimista de 1,06× a 1,5×. Los dos casos concuerdan en que las semanas 4–5 (ETL y Power BI) se desbordan. El plan dice "recorta lo extra, no hay deuda". Pero no define qué es núcleo, y los días dependen unos de otros: si no hiciste P09–P28, el ETL del día 22 no se puede construir.
2. **El paso crítico hacia tu meta está comprimido.** Tu objetivo es construir un ETL desde cero. El plan te da 4 sesiones guiadas (≈250 min de práctica) para el primer ETL y 4 sesiones (240 min) para el de transferencia. Mi estimación para una persona que depende de IA es de 9 h para el primero y de unas 8 h para el segundo.
3. **La evaluación final no es un conjunto de datos nuevo.** Tiene el mismo esquema, el mismo catálogo (byte a byte), el mismo diccionario y las mismas clases de defectos que el caso de transferencia C06 (3× más filas). Además, el enunciado enumera los defectos que debes encontrar. Mide "repetir C06 a mayor escala", no transferencia real.
4. **Las claves de respuesta de la evaluación final están dentro de tu carpeta de trabajo**, y esa carpeta tiene un remoto de GitHub (ver D.4). Con tu propia disciplina bastaría, pero el paquete afirma conservar la evaluación y no lo hace del todo.
5. **Hay un error reproducible en Windows 11.** 2 de las 13 pruebas del paquete fallan en tu máquina (ver D.2). El informe del autor dice "13/13 aprobadas": esa medición se hizo en otro sistema (Python 3.12.14).
6. **El material para principiantes es más delgado que su apariencia.** Los capítulos de Python tienen ~500 palabras cada uno. Los 30 ejercicios son funciones sueltas. Los correctores dicen *qué* falló pero no *dónde*. Las 81 soluciones SQL no tienen ningún comentario que explique el razonamiento.

**Veredicto corto:** el *contenido* es bueno y el *calendario* es optimista. Con 5 cambios críticos (sección J) pasa a ser razonable para tu meta, que es un ETL junior propio y defendible. Sin ellos, el riesgo principal no es que el material sea malo: es que las semanas 4–5 produzcan la misma frustración que te hizo abandonar otros planes.

---

## B. Evaluación global (0–10)

El puntaje evalúa el **diseño del programa**, no tu probabilidad de éxito ni de ser contratado. Para "Riesgo de sobrecarga", 10 = riesgo bajo.

| Criterio | Nota | Base de la nota |
|---|---:|---|
| Organización | 8,5 | 407 archivos, estructura clara, manifiesto íntegro, 0 enlaces rotos. Resta: soluciones y plan en el mismo repositorio, erratas en los exámenes. |
| Realismo del calendario | 4,0 | 25 de las 36 jornadas activas superan 1,5× según el modelo central (sección C). |
| Progresión pedagógica | 6,0 | Orden correcto, pero saltos en D08, D12, D22, D29 y D36. |
| Calidad técnica | 8,0 | Cifras verificadas de forma independiente. Resta: bug de Windows, pruebas débiles (P05 pasa por casualidad). |
| Calidad de los datasets | 7,0 | Íntegros y consistentes. Resta: esquema único y muy limpio, y el final es un clon del de transferencia. |
| Calidad de los ejercicios | 6,0 | Gradación y contratos buenos. Resta: pistas genéricas, enunciados de una línea, tiempos objetivo cortos. |
| Calidad de las soluciones | 6,0 | Correctas, pero sin explicación. Los correctores no localizan el fallo. |
| Preparación para ETL | 5,5 | Buenos principios (Bronze/Silver/Gold, rechazos, idempotencia). Poco tiempo y poco andamiaje antes del ETL desde cero. |
| Analítica empresarial y KPIs | 7,5 | 13 KPIs con definición, ejemplo, error común y práctica. Resta: pocas prácticas de recomendación a gerencia. |
| Estadística aplicada | 5,5 | Cobertura amplia (IQR, normalidad, IC, Welch, χ²) pero superficial y en días sobrecargados. |
| Preparación para entrevistas | 6,0 | Banco de 24 preguntas y 6 simulacros, todos de autoevaluación. Falta práctica con otra persona. |
| Preparación laboral | 6,5 | CV honesto y seguimiento. No incluye análisis de vacantes verificado. |
| Riesgo de sobrecarga (10 = bajo) | 3,5 | Semanas 4–5 son el punto crítico. |
| Posibilidad de aprendizaje autónomo | 5,0 | Buen método (intento, depuración, pista). Los correctores y las pistas no lo respaldan lo suficiente. |

---

## C. Análisis de los 42 días

### Supuestos de la estimación (leer antes de la tabla)

No hay datos empíricos de tu velocidad. La estimación es un modelo con supuestos:

- **Entrada:** el "tiempo objetivo" que cada ejercicio declara, sumando solo los ejercicios que la guía diaria lista como esenciales (sin los marcados "ampliación").
- **Multiplicadores (mi criterio):** SQL nivel 1/2/3 ×1,5/×1,75/×2,25; Python ×2,0/×2,5/×3,25; estadística ×2,0–2,5; casos ×1,75; Power BI/Excel (primera vez en la interfaz) ×2,0. Motivo: los "tiempos objetivo" parecen pensados para alguien que ya sabe la solución, y las pistas del plan tratan 10 min de intento más 10 min de depuración como lo normal.
- **Proyectos sin ejercicio propio:** el ETL guiado de la semana 4 (D22–D25) lo estimo en 540 min; C06 desde cero (D36–D39) en 490 min. Ambos son juicios míos para una persona con tu historial, con un margen de ±35 %.
- **Días de examen:** el tiempo planificado ×1,12 a ×1,35 (S04 y S05 son más exigentes que S01–S03).
- **Total del día estimado** = tiempo original − bloque de práctica + práctica estimada. Teoría, SQL de calentamiento, empleo y cierre se mantienen como están.
- **Clasificación:** REALISTA si el estimado ≤ 1,15× el original; AJUSTADA hasta 1,4×; SOBRECARGADA por encima de eso. REQUIERE PRERREQUISITOS se asigna aparte si el día usa un concepto que ninguna sesión anterior practicó.
- **Caso optimista** (todos los ejercicios ×1,3, proyectos al 60 %): semanas 1–6 = 1,06 / 1,21 / 1,18 / 1,44 / 1,50 / 1,32. **Caso central** (el de la tabla): 1,24 / 1,59 / 1,71 / 2,04 / 2,09 / 1,80.

### Tabla (6 domingos de descanso: D07, D14, D21, D28, D35, D42 = 0 min)

Dificultad: 1 (fácil) a 5 (muy difícil) para una persona con tu perfil. Minutos: original → estimado.

| Día | Contenido | Original | Estimado | Dific. | Clasificación / Riesgo | Recomendación |
|---|---|---:|---:|:-:|---|---|
| D01 lun 12/10 | Entorno, filas, variables · S1, S10, P01 | 90 | ~105 | 2 | AJUSTADA · bajo | Ya ocurrió. Si la instalación te consumió el bloque, la jornada se da por buena. |
| D02 mar 13/10 | NULL, filtros, texto · S2, S7, S9, P02, P03, C01 | 160 | ~212 | 2 | AJUSTADA · medio | Núcleo: S2, S7, P02, C01. Pasa S9 y P03 a opcional. |
| D03 mié 14/10 | Listas, dict, set · S3, S5, S6, P04, P05, C02 | 150 | ~184 | 3 | AJUSTADA · medio | Primer día con 3 conceptos nuevos de Python. Pasa C02 a D05 u opcional. |
| D04 jue 15/10 | GROUP BY, bucles, media/mediana · G1–G3, P06, ST01 | 150 | ~195 | 3 | AJUSTADA · medio | Núcleo: G1, G2, P06. Mueve ST01 a opcional (primera postulación cae este día). |
| D05 vie 16/10 | Condiciones, funciones, HAVING · G4–G6, P07, P08, C01 | 150 | ~192 | 3 | AJUSTADA · medio | C01 aparece otra vez (ya en D02 y luego D40). Quítalo aquí. |
| D06 sáb 17/10 | Examen S01 + simulacro · G7, G8 | 200 | ~224 | 3 | REALISTA · medio | El examen reutiliza P02, P06 y C01 ya practicados: mide retención, no transferencia. Está bien como primer hito. |
| D08 lun 19/10 | try/except, contratos · CL1, CL3, P09 | 90 | ~157 | 4 | REQUIERE PRERREQUISITOS · alto | `try/except`, `ValueError` y parseo de texto se leen el mismo día. En D01–D06 no se practicaron. Haz solo P09 (la versión simple) y deja CL1, CL3 para D11. |
| D09 mar 20/10 | Fechas, cantidades, **primer JOIN** · J1, J2, P10, P11 | 160 | ~242 | 3–4 | SOBRECARGADA · alto | JOIN y parseo de fechas en un mismo día. Núcleo: J1, J2, P10. P11 pasa a D11. |
| D10 mié 21/10 | JOIN+GROUP BY, módulo csv · J3, J4, P12, P13, C04 | 150 | ~292 | 3–4 | SOBRECARGADA · alto | C04 (40 min nominales) es un caso de conciliación completo: pásalo a D13. |
| D11 jue 22/10 | LEFT JOIN, errores · J5, J6, P14, P15 | 150 | ~237 | 4 | SOBRECARGADA · alto | J5 es un anti-join (difícil). Núcleo: J5 y P14. |
| D12 vie 23/10 | **Primer DataFrame**, percentiles · E1–E3, P16, P17, ST02, N01 | 150 | ~282 | 4 | SOBRECARGADA y REQUIERE PRERREQUISITOS · alto | Primer contacto con Pandas, además de estadística. Solo N01 + P17 + un ejercicio SQL. ST02 a opcional. |
| D13 sáb 24/10 | Examen S02 (JOIN) · E4–E8 | 200 | ~224 | 3 | REALISTA · medio | Incluye aquí C04 si lo sacaste de D10. |
| D15 lun 26/10 | Pandas: monto por línea · K1, K2a, P18, P19 | 90 | ~223 | 3–4 | SOBRECARGADA · muy alto | 90 min planificados contra ~220 estimados. Solo K1 + P19. |
| D16 mar 27/10 | CTE, merge validado · K2b, K3, P20, P21, N02 | 160 | ~272 | 4 | SOBRECARGADA y REQUIERE PRERREQUISITOS · alto | P21 (merge con `validate`) es nivel 3. Solo K3, P20, P21. |
| D17 mié 28/10 | Duplicados, perfilado · K4, K5, P22, P23, N03 | 150 | ~238 | 3–4 | SOBRECARGADA · alto | Núcleo: K4, P22, P23. |
| D18 jue 29/10 | Fechas, Gold, recencia · K6, V1, V2, P24, P25 | 150 | ~267 | 4 | SOBRECARGADA · alto | P25 (nivel 3) es el primer "Gold" en Pandas. Núcleo: V1, P24, P25. |
| D19 vie 30/10 | Ventanas, ABC, atípicos · V3, V4, P26, P27, ST03, N04 | 150 | ~312 | 4–5 | SOBRECARGADA · muy alto | El peor día de la semana 3: ventanas, ABC y IQR a la vez. Núcleo: V3, V4. P26/P27/ST03 a D20–D21 u opcional. |
| D20 sáb 31/10 | Examen S03 (CTE/ventanas/Pandas) · V5, X1, X2, P28 | 200 | ~224 | 4 | REALISTA, pero examen difícil | S03 exige P25 y P21 (nivel 3) desde cero, después de un D19 sobrecargado. |
| D22 lun 02/11 | **Diseño ETL**, Bronze · N8, CL4, P29, P30 | 90 | ~331 | 4 | REQUIERE PRERREQUISITOS · crítico | Un lunes de 90 min para arrancar el proyecto ETL. Ver F. |
| D23 mar 03/11 | ETL: texto, fechas, dinero · X3, X4, C05 | 160 | ~386 | 4 | SOBRECARGADA · crítico | Etapas 2–3 del ETL (Decimal, tres formatos de fecha) más C05 (45 min). |
| D24 mié 04/11 | ETL: duplicados, vendedores · X5, X6 | 150 | ~258 | 4 | SOBRECARGADA · alto | Etapa 4. |
| D25 jue 05/11 | ETL: Silver, Gold, carga SQLite · X7, X8, N1 | 150 | ~333 | 4 | SOBRECARGADA · crítico | Etapas 5–7, incluyendo carga repetible y cuadre SQL. |
| D26 vie 06/11 | Muestreo, piloto, cobertura · N2–N4, ST04, ST05, N05 | 150 | ~280 | 4 | SOBRECARGADA · alto | ST05 (Welch + IC) en un día con tres KPIs. ST05 a opcional. |
| D27 sáb 07/11 | Examen S04: ETL propio + modelo estrella · N10, N11 | 200 | ~250 | 4 | AJUSTADA · crítico | Exige haber terminado el ETL de D22–D25. Si no está, el examen no tiene objeto. |
| D29 lun 09/11 | Inferencia + **Power BI** · N7, N12, ST06, ST07, PB01 | 90 | ~355 | 4 | SOBRECARGADA y REQUIERE PRERREQUISITOS · crítico | 90 min contra 145 min nominales (4× el bloque de práctica). |
| D30 mar 10/11 | Relaciones, calendario · N13, N14, PB02, N07 | 160 | ~270 | 4 | SOBRECARGADA · alto | Primera vez con relaciones y tabla de fechas en Desktop. |
| D31 mié 11/11 | Medidas DAX, Excel · N5, N6, PB03, EX01 | 150 | ~330 | 3–4 | SOBRECARGADA · alto | Dos herramientas nuevas el mismo día. |
| D32 jue 12/11 | Contexto, presupuesto · N15, N16, PB04, EX02 | 150 | ~355 | 4 | SOBRECARGADA · crítico | `DATEADD`, filtros y presupuesto (ver D.5). |
| D33 vie 13/11 | Visuales, percentiles · J2, N9, PB05, EX03 | 150 | ~301 | 3 | SOBRECARGADA · alto | Núcleo: PB05. |
| D34 sáb 14/11 | Examen S05: Desktop + Excel · N1, N3 | 200 | ~270 | 4 | AJUSTADA · alto | Si no hay Desktop operativo, "pendiente" es la única respuesta honesta. |
| D36 lun 16/11 | Caso nuevo, contrato · V2, N7, P09, P11, N06 | 90 | ~274 | 4 | REQUIERE PRERREQUISITOS · alto | Lunes de 90 min para el contrato de C06. Hazlo en 25 min y deja el resto como repaso. |
| D37 mar 17/11 | C06 (1): perfilado, extracción · N8 | 160 | ~285 | 5 | SOBRECARGADA · crítico | C06 está presupuestado en 70 min este día. |
| D38 mié 18/11 | C06 (2): Silver, rechazos · N9 | 150 | ~285 | 5 | SOBRECARGADA · crítico | 80 min presupuestados. |
| D39 jue 19/11 | C06 (3): Gold, cuadres · N5, V4 | 150 | ~294 | 5 | SOBRECARGADA · crítico | 65 min presupuestados. |
| D40 vie 20/11 | Comunicación, entrevista · J5, N3, C01, C03 | 150 | ~255 | 3 | SOBRECARGADA · medio | C01 por tercera vez. Haz C03 y la entrevista. |
| D41 sáb 21/11 | Examen S06: C06 terminado + defensa · V4, N1 | 200 | ~230 | 4 | REALISTA solo si C06 está hecho | Exige C06 terminado. Con el calendario actual ese es el supuesto frágil. |

**Totales por semana, original → central / optimista:** S1 900 → 1112 / 954 · S2 900 → 1434 / 1090 · S3 900 → 1536 / 1064 · S4 900 → 1838 / 1297 · S5 900 → 1881 / 1350 · S6 900 → 1623 / 1189.

**¿Es viable el calendario con ~15 h/semana?** No como está escrito, en ninguno de los dos casos. Con el supuesto optimista, las semanas 1–3 son viables con recortes menores. Las semanas 4–5 no lo son en ningún escenario que probé: exigen entre 1,3 y 2,1 veces lo que cabe.

### El mecanismo de recorte del plan no resuelve el problema

El plan dice "al llegar al tiempo, guarda y recorta ampliación". Eso funciona si lo que recortas es de verdad prescindible. Pero:

- En los días con nominal > bloque de práctica, los ejercicios "esenciales" ya superan el bloque por sí solos (D08, D10, D12, D15, D16, D19, D22, D23, D26, D29–D33). No queda "ampliación" que recortar.
- Cada día depende del anterior (P09–P28 → ETL → C06 → final). Cortar un ejercicio de Python tiene un costo posterior que el plan no mide.
- Los hitos están atados a fechas de semana, no a "puertas" de competencia. La recuperación dice "reemplaza el siguiente bloque práctico", y eso desplaza el siguiente tema sin mover las fechas de los exámenes.

---

## D. Auditoría técnica

### D.1 Inventario [MEDIDO]

| Carpeta | Archivos | Notas |
|---|---:|---|
| 01_PLAN_DIARIO | 46 | 42 guías + plan + hitos + calendario CSV/JSON |
| 02_TEORIA | 25 | 18 capítulos, glosario, fuentes, 5 materiales UAGRM |
| 03_EJERCICIOS | 152 | 81 SQL (+ índice y contratos), 30 Python (+ plantilla), 7 estadística, 7 notebooks, 15 casos, 6 exámenes |
| 04_DATASETS | 20 | `comercial.db`, `distribuidora/` (CSV + DB + ETL raw), transferencia, piloto, encuesta, inventario… |
| 05_PROYECTOS | 19 | ETL (plantilla), Power BI (9 CSV, M, DAX), SQL |
| 06_ENTREVISTAS | 7 | |
| 07_LINKEDIN_EMPLEO | 5 | |
| 08_SOLUCIONES | 94 | 81 SQL, 4 Python, controles JSON, silver esperadas |
| 09_EVALUACION_FINAL | 6 | |
| 10_VALIDACION | 18 | |
| herramientas | 9 | |
| mi_trabajo | 2 | `progreso.csv` y `errores.md`, sin entradas (D01 todavía no registrado) |
| raíz | 4 | README, 2 requirements, .gitignore |
| **Total (sin `.venv` ni `.git`)** | **407** | `.venv`: 19.905 archivos, 405 MB |

- Archivos vacíos: **0**. Duplicados exactos: 4 pares, todos intencionales (las tablas del modelo BI repiten tablas de `distribuidora`, y el catálogo de transferencia y el final son idénticos, ver F).
- Rutas citadas que no existen: 1 falsa alarma ("10_Pandas_transformaciones.md" sin su carpeta, en un README del ETL).
- 389 enlaces internos comprobados, 0 rotos. 403/403 hashes del manifiesto coinciden con los archivos actuales.
- SQL: 81 ejercicios; 70 asignados a algún día. No asignados: S4 y CL2 (huérfanos) y los 9 `ES*` (usados en exámenes).
- Texto dañado: unas 8 palabras pegadas, concentradas en los exámenes S02–S06 y en una línea de `verificar_paquete.py`: "yunaprueba", "deconflicto", "laaprue", "introduceuna cantidad fraccionariaenunacopia", "oduplicación". Son pocas, pero están en el material de evaluación.
- `.git`: 1 commit ("initial commit"), 407 archivos rastreados (incluye los 94 de `08_SOLUCIONES`), remoto `origin` → `github.com/srDesho/plan-data-bi-v5`.

### D.2 Entorno [MEDIDO]

- `.venv`: Python 3.12.10 (el que instalaste), pandas 2.2.3, numpy 2.3.5, scipy 1.17.0, matplotlib 3.10.8, nbformat 5.11.1, ipykernel 7.4.0. Coincide con `requirements.txt`. `pip check`: sin conflictos.
- `versiones.json` registra Python 3.12.14 y SQLite 3.53.1; tu venv es 3.12.10. Es una diferencia menor, pero confirma que el informe del autor se midió en otro entorno.
- Tu intérprete por defecto en `py` es 3.14 (marcado `*`). El README usa `py -3.12`, lo cual evita el problema. Si algún día ejecutas `python` o `py` sin versión, usarás 3.14, que no tiene las dependencias del plan instaladas (no lo verifiqué). VS Code debe apuntar a `.venv`.
- `herramientas/comprobar_entorno.py` y `ejecutar_sql.py` de los comandos del README: **OK** en tu entorno.
- Dependencias UAGRM: `pip install --dry-run -r requirements_uagrm_opcional.txt` resuelve en Python 3.12 (seaborn 0.13.2, statsmodels 0.15.0, scikit-learn 1.9.1, summarytools, ucimlrepo). No se instaló nada. `versiones.json` indica scikit-learn 1.8.0: la versión resuelta hoy es otra (deriva menor).

### D.3 Pruebas ejecutadas

Ejecuté `herramientas/verificar_paquete.py` sobre una **copia** (el script escribe en `10_VALIDACION`, por eso no lo ejecuté sobre el original).

| # | Prueba del paquete | Resultado en tu Windows 11 |
|---|---|---|
| 1 | SQL completo y corrector negativo (81 actividades) | OK |
| 2 | Python: 30 contratos, casos límite | OK |
| 3 | Datos íntegros, cuadres CSV/SQL independientes | OK |
| 4 | ETL distribuidora, dos ejecuciones | OK |
| 5 | **ETL transferencia/final, oráculo fila por fila** | **ERROR** (PermissionError) |
| 6 | **Pruebas adversas y publicación segura** | **ERROR** (PermissionError) |
| 7 | Estadística con controles | OK |
| 8 | Modelo estrella (9 CSV) | OK |
| 9 | Notebooks del núcleo | OK |
| 10 | Calendario | OK |
| 11 | Inicializador de `mi_trabajo` | OK |
| 12 | Ejemplos Python de la teoría | OK |
| 13 | Rutas, Markdown, contratos | OK |

**Resultado: 11 OK, 2 ERROR.** El informe del autor dice 13/13.

### D.4 Errores y hallazgos técnicos

**Hallazgo 1 — [CRÍTICO] PermissionError (WinError 32) en el ETL de referencia en Windows**

| Campo | Detalle |
|---|---|
| Archivo | `08_SOLUCIONES/etl_nuevo_referencia.py`, líneas 76–81 |
| Error | `PermissionError: [WinError 32] … 'resultado.tmp.db'` al ejecutar `os.replace(tmp, dest)` |
| Causa | `with sqlite3.connect(tmp) as con:` **no cierra la conexión**; solo confirma la transacción. Windows no permite reemplazar un archivo abierto. Linux sí. |
| Cómo reproducirlo | `python herramientas/verificar_paquete.py` en Windows (pruebas 5 y 6). Se aísla llamando a `ejecutar(entrada, salida)` de ese módulo. |
| Impacto | (a) El informe de validación no se reproduce en tu máquina. (b) **Es el patrón que el curso te enseña** (`with sqlite3.connect(...)` en ETL y validadores). Si tu ETL propio hace `os.replace` o borra la base mientras la conexión sigue abierta, fallará igual, y tú sin experiencia lo vivirás como un error misterioso. |
| Corrección | Cerrar la conexión: añadir `con.close()` después del bloque `with`, o usar `contextlib.closing(sqlite3.connect(...))`. **Verificado**: con ese cambio aplicado solo en mi copia, las 13 pruebas pasan. Conviene además enseñarlo explícitamente en `05_calidad_ETL.md`. |

El mismo patrón `with sqlite3.connect(...) as con` aparece sin `close` en `validar_final.py`, `validar_etl_distribuidora.py` y `etl_distribuidora.py`. Hoy no falla, pero deja los archivos de base de datos bloqueados hasta que el recolector de basura libere el objeto.

**Hallazgo 2 — [IMPORTANTE] Los correctores no dicen *dónde* falló la entrada**

Pruebas hechas con errores típicos de un principiante:

| Prueba | Salida del corrector | Problema |
|---|---|---|
| P09 con `int(float(t)*100)` (el clásico error de coma flotante, 2,05 → 204) | `REVISAR P09: AssertionError: (204, 205)` | No indica cuál de los 7 casos de prueba falló ni la entrada. |
| P01 con `+` en vez de `*` | `AssertionError: (13, 30)` | No muestra los argumentos. |
| `S10` con filtro de más | `Resultado diferente: 1 filas, esperado 1` | Dice "1 vs 1" sin mostrar tu valor ni el esperado. Confunde: parecen iguales. |
| SQL con error de sintaxis | `OperationalError: near "clientes": syntax error` | Aceptable. |
| P05 con `list(set(codigos))` (sin ordenar) | **OK** (falso positivo) | Para enteros pequeños el orden de un `set` coincide con el orden ascendente. El test solo usa [3,1,3,2]. Pasaría un código incorrecto. |

La consigna del plan es "intenta, depura, pide una pista", pero la herramienta que debería ayudar a depurar solo da la mitad de la información.

**Hallazgo 3 — [IMPORTANTE] Las claves de respuesta de la evaluación final están al alcance**

Sin ejecutar ni reproducir el resultado final, verifiqué por lectura qué hay accesible dentro de tu carpeta (que es un repositorio con remoto GitHub):

- `08_SOLUCIONES/etl_nuevo_referencia.py`: la solución completa, que corre sobre los datos del final.
- `08_SOLUCIONES/controles_final.json` y `silver_final_esperada.csv`: la clave de respuestas completa.
- `10_VALIDACION/resultados_pruebas.json`: contiene las métricas finales, incluido el importe, **aunque `INFORME_VALIDACION.md` dice no publicarlo "para conservar la evaluación"**.
- `INFORME_VALIDACION.md`: publica los conteos del final.
- `herramientas/contratos_python.py` (prueba de P30): usa esos mismos conteos como datos de ejemplo.
- `02_TEORIA/04_SQL_CTE_ventanas.md` indica el resultado de V4 ("Da A=41, B=37, C=42").

**Nota de transparencia:** mientras verificaba esta fuga, una de mis búsquedas imprimió esos valores en la salida de herramienta de esta sesión. No los repito aquí. Si quieres que el examen conserve su valor, ese es un motivo adicional para generar una variante nueva (ver J).

El README pide no mirar las soluciones, y la regla es honesta. Pero para una persona que, por tus palabras, tiende a frustrarse y recurrir a la IA, dejar la solución a una carpeta de distancia es un riesgo de diseño, no solo de disciplina.

**Hallazgo 4 — [IMPORTANTE] Soluciones y proyecto en el mismo repositorio**

`git ls-files` incluye `08_SOLUCIONES` (94 archivos) y hay un remoto de GitHub. No pude ni quise comprobar si el repositorio es público. Si lo es, estás publicando las soluciones completas bajo tu nombre. En un proceso de selección eso se ve mal y contradice el CV honesto que el plan propone. Recomiendo repositorios separados (ver J).

**Hallazgo 5 — [IMPORTANTE] Posible error en la medida DAX `Crecimiento` (no verificado en Desktop)**

`Ventas Mes Anterior = CALCULATE([Ventas Bs], DATEADD(dim_fecha[fecha],-1,MONTH))` desplaza el contexto de `dim_fecha`. Pero `MODELO.md` dice que `dim_mes` filtra directamente a `fact_ventas[mes]` y que no hay relación `dim_mes → dim_fecha`. Si un visual usa `dim_mes` (por ejemplo, un segmentador), se aplican ambos filtros a la vez (mes seleccionado y mes anterior) y la intersección queda vacía: la medida devuelve vacío. **[Análisis por lectura, no ejecutado.]** Solo funcionaría si el eje del visual es `dim_fecha`. Como el paquete no incluye un `.pbix` y el autor lo declara pendiente, el riesgo es que lo descubras en D32 en pleno desbordamiento horario.

**Hallazgo 6 — [OPCIONAL] Otros detalles**

- V4: el enunciado dice "A = hasta 80 %". La referencia usa el acumulado *anterior* (el cliente que cruza el 80 % queda en A: 41 clientes). Con la lectura literal ("acumulado ≤ 80 %") salen 40. La teoría documenta la convención, pero el enunciado es ambiguo y el corrector rechazará la lectura literal.
- ES1B: pide "categorías con al menos cinco productos", pero las cinco categorías tienen exactamente 8 productos. El `HAVING` no filtra nada, así que el examen no detecta si lo omites.
- ES3C: el contrato nombra una columna como `ROUND(ventas,2)`.
- Las columnas de los contratos SQL N5/ES3C son expresiones, no alias.
- Los exámenes indican el número de filas esperado (p. ej. "30 filas"); es una pista, no un examen ciego.
- `ejecutar_sql.py` devuelve JSON. Para aprender SQL conviene una tabla legible (DBeaver o DB Browser, que el README menciona como opcionales).
- `S4` y `CL2` no se asignan a ningún día.
- N9 y K2a piden el mismo número (ticket medio).
- 81/81 soluciones SQL tienen **0 líneas de comentario**; `python_referencia.py` no explica el razonamiento.

### D.5 Cuadres de negocio verificados de forma independiente [MEDIDO]

Recalculé con Pandas sobre los CSV (sin ejecutar el SQL de referencia) y comparé con `controles_sql.json`:

| Control | Resultado |
|---|---|
| Integridad SQLite de `comercial.db` y `distribuidora.db`; `foreign_key_check` | OK, sin violaciones (las tablas no declaran PK/FK) |
| Huérfanos: ítems sin pedido, pedidos sin cliente | 0 y 0 |
| Ventas entregadas totales (CSV vs SQLite vs `drop_por_pedido`) | Coinciden |
| J3 ventas por categoría | OK |
| K2a drop medio, K3 cantidad de pedidos > media, K4 por tamaño | OK |
| V2 clientes inactivos > 60 días | OK |
| N1 cumplimiento mensual por ruta (36 filas) | OK |
| N2 cobertura, N3 efectividad, N4 cobertura de clientes | OK |
| N5 crecimiento mensual (valores de los 6 meses) | OK |
| N12 clientes activos y frecuencia | OK |
| V4 clasificación ABC | OK con la convención "acumulado anterior" documentada |

Observaciones sobre los datos: 120 clientes, 6 vendedores, 40 productos, 3.600 pedidos, 16.178 líneas, periodo 2026-04-01 a 2026-09-30. Solo la columna `zona` de `clientes` tiene nulos (6). Las visitas cubren solo septiembre (2026-09-01 a 2026-09-22). Los datos de la base SQL están muy limpios: toda la "suciedad" está en los archivos de ETL. Es una buena decisión pedagógica al principio y un riesgo después, porque en SQL nunca practicas con datos desordenados.

### D.6 Cobertura de funciones SQL en las soluciones asignadas [MEDIDO]

| Función | Primer día en que se usa | Ejercicios que la usan |
|---|---|---:|
| IS NULL | D02 | 9 |
| LIKE | D03 | 1 |
| GROUP BY | D04 | 49 |
| HAVING | D05 | 5 |
| Funciones de fecha | D06 | 14 |
| COALESCE | D08 | 7 |
| JOIN | D09 | 50 |
| LEFT JOIN | D11 | 13 |
| Subconsulta | D15 | 19 |
| CTE | D16 | 17 |
| CASE | D17 | 7 |
| Ventana (`OVER`) | D19 | 11 |
| LAG/RANK | D20 | 5 |

Ejercicios SQL por semana: 17 / 16 / 14 / 14 / 12 / 10. SQL está presente toda la formación. `HAVING` (5) y `LIKE` (1) están muy poco practicados, y las funciones de ventana aparecen recién en el día 19.

### D.7 UAGRM y notebooks [MEDIDO]

- Notebook de la Clase 1: **58/58 celdas de código se ejecutan sin error** en tu venv (usé una copia).
- Notebook de la Clase 2 (estadística): **no puede ejecutarse tal cual** en tu entorno. (a) Importa seaborn, summarytools, ucimlrepo, statsmodels y scikit-learn, que no están en tu venv (están en el archivo opcional, y su instalación resuelve bien en seco). (b) Hace `from functions.ml_eda_functions import *`, pero **no existe una carpeta `functions/`**: el archivo está en `02_TEORIA/UAGRM/04-ml_eda_functions.py`, así que el `import` falla. (c) Descarga datos de UCI por internet; no probé esa celda. El autor declara que su ejecución se detuvo en la celda 18 por la conexión.
- Los 7 notebooks propios del plan (N01–N07): se ejecutan con el método del paquete (celdas en proceso, sin kernel). Las celdas de práctica están vacías a propósito.
- Informe del autor sobre el PDF de la UAGRM: lo cita como revisado. Yo no lo abrí. **[NO VERIFICADO por mí.]**

---

## E. Auditoría pedagógica

### E.1 Lo que enseña el programa: comprender, practicar, aplicar, demostrar

| Área | Comprender | Practicar | Aplicar | Demostrar | Comentario |
|---|:-:|:-:|:-:|:-:|---|
| SQL (SELECT→ventanas) | Sí | **Sí (70 ejercicios, toda la formación)** | Parcial | Sí (exámenes, corrector) | La fortaleza del plan. Una sola base (120 clientes), así que se aprende el esquema más que a enfrentarse a uno nuevo. |
| Python básico | Parcial | Sí (P01–P08) | Parcial | Sí (corrector) | Teoría de ~930 palabras (caps. 07–08) para todo el bloque, pocos ejemplos resueltos. Depende de la clase UAGRM y de tu iniciativa. |
| Pandas | Parcial | Parcial (P17–P28, N01–N04) | Poco | Parcial | Teoría de ~740 palabras para dos capítulos; primera exposición en D12 y ETL solo 10 días después. |
| Analítica y KPIs | Sí (13 KPIs) | Sí (N1–N16, C01–C04) | Parcial | Parcial | Cumplimiento, cobertura, efectividad, drop size, ticket, frecuencia, recencia/inactivos, ABC, rotación, variaciones: todos con definición, ejemplo, error común y ejercicio. Falta más práctica de redactar recomendaciones (solo C01, C03, entrevistas). |
| Estadística empresarial | Parcial | Parcial (ST01–ST07) | Poco | Poco | Media/mediana/moda/dispersión/percentiles/IQR sí. Inferencia (IC, Welch, χ²) entra en días muy sobrecargados. No hay un capítulo de distribución normal ni de muestreo más allá de dos párrafos. |
| ETL / calidad / Medallion | Sí | Parcial | Parcial | Sí (S04, S06, final) | Buen contenido conceptual. Ver F sobre tiempo y andamiaje. |
| Modelo estrella / DW | Parcial | Poco | Poco | Poco | Un capítulo de ~400 palabras y un proyecto de 9 tablas, sin práctica de diseño propia. |
| Power BI / DAX | Parcial | Parcial | Poco | **No verificable** | Sin `.pbix`; el autor no ejecutó nada en Desktop. 6 sesiones guiadas de ~45–50 min nominales. |
| Excel | Poco | Poco | Poco | No | 1 capítulo de 386 palabras y 3 casos. Es una de las herramientas más pedidas en vacantes juniors y recibe la menor cobertura. |
| Git/GitHub | Parcial | Parcial | Parcial | Parcial | Capítulo corto; práctica indirecta. |
| Entrevistas | Parcial | Parcial | — | Parcial | 24 preguntas, 6 simulacros de autoevaluación; guía de corrección en la carpeta de soluciones. |
| SQL Server / PostgreSQL | Mínimo | No | No | No | Dos líneas sobre diferencias de dialecto (TOP vs LIMIT, fechas). Todo se practica en SQLite. |

### E.2 Hallazgos pedagógicos

1. **Los ejercicios están generados por plantilla.** Los 81 SQL comparten el mismo texto. Las "pistas graduales" 1 y 2 son casi iguales en todos ("Decide qué condición filtra filas (WHERE) y cuál filtra grupos (HAVING)" aparece incluso en S1, que no tiene ni WHERE ni HAVING). Los 30 de Python tienen una sola línea de contrato y las mismas dos pistas. Una pista que no depende del ejercicio no ayuda a nadie atascado.
2. **Los "tiempos objetivo" son cortos.** P25 (agrupar por cliente/mes con filtro y `nunique`) se declara en 20 min. P26 (ABC con acumulado anterior) también en 20. N1 (cumplimiento sin multiplicar el presupuesto por JOIN) en 20. Para una persona que depende de IA, son más bien 45–90 min.
3. **Los enunciados de la mayoría de ejercicios SQL (N, X, E, K…) son una frase.** Dependen del `DICCIONARIO.md` y de CONTRATOS para el resto. Es eficiente y reproduce el trabajo real, pero dificulta el aprendizaje cuando algo falla.
4. **Los 30 ejercicios de Python son funciones sueltas con contratos sobre *casos concretos*.** Entrenan el primer nivel (ejecutar y modificar funciones) y el segundo (completar una guía). No hay ningún ejercicio entre "escribir una función" y "construir un script con extracción, validación, carga, registro" hasta D22. Ese salto es el que deberías cubrir antes del ETL.
5. **Hay repetición útil.** V4, N1 y N3 aparecen 3 veces; J2, J5, V2, N7, N8, 2 veces. La repetición espaciada es una buena práctica. C01 se repite 3 veces (D02, D05, D40) y es un ejercicio que se resuelve con una división; conviene sustituirlo en D05 por otro.
6. **P09 pide rechazar entradas sin decir que debe ser `ValueError`.** P10 y P11 sí lo dicen. El corrector sí lo exige. Un error que costaría 20 minutos de frustración sin necesidad.
7. **Los exámenes miden retención, no transferencia.** S01 reutiliza P02, P06 y C01. S02 reutiliza P09/P11 y C04. S03 pide P25 y P21 otra vez. Está bien como hito de consolidación; no debe interpretarse como evidencia de autonomía.
8. **Las soluciones muestran, no explican.** 0 comentarios en 81 consultas. El método del plan ("consulta la referencia y explica la diferencia con tu código") necesita que la referencia ayude a explicarla.
9. **La teoría es de calidad profesional y muy densa.** Cada capítulo cabe en 400–500 palabras. Los conceptos que cuestan (granularidad, JOIN, `groupby`, `merge validate`) reciben uno o dos párrafos y un ejemplo. A un principiante se le puede escapar la idea. Los capítulos funcionan mejor como repaso que como primera exposición. La excepción es el de KPIs (1.288 palabras), mejor estructurado.
10. **El objetivo diario no siempre coincide con el título.** Por ejemplo D04: el título es "Agrupación, bucles y media/mediana", pero el objetivo de trabajo es "contar estados y explicar por qué anulados cambian las cifras. Primera postulación". Mezclar una acción de búsqueda de empleo con el objetivo técnico del día dificulta saber cuándo "se cumplió".

### E.3 Modos COMPLETO, REDUCIDO, MÍNIMO

- **MÍNIMO (20 min):** "rehacer una consulta conocida" y explicar una decisión. Es un buen mecanismo para **no romper la racha** y para ti es probablemente el más importante del plan. No avanza contenidos, y el plan lo admite.
- **REDUCIDO (45–60 min):** la guía dice "una consulta y un ejercicio esencial", pero no define cuáles. En la práctica es la modalidad que mejor encaja con tu realidad, y es la que menos soporte tiene. Si eliges REDUCIDO una semana completa (≈ 40 % menos de tiempo), el contenido queda a medio camino y los días siguientes asumen que lo hiciste.
- **COMPLETO:** como muestra la sección C, ni siquiera COMPLETO cabe en varias semanas. En la práctica el plan solo puede cumplirse con REDUCIDO si el "núcleo" de cada día es explícito.

El problema no es el sistema de modos. Es que el contenido no está marcado como núcleo/opcional: la elección del modo recae en ti cada día, que es justo el tipo de decisión que tiende a agotar la fuerza de voluntad.

---

## F. Evaluación del ETL

### F.1 Los cuatro niveles

| Nivel | ¿El plan lo cubre? | Dónde | Evidencia |
|---|---|---|---|
| 1. Ejecutar un ETL ya escrito | Sí | D22 (referencia en carpeta de soluciones) | `etl_distribuidora.py` corre en tu entorno. |
| 2. Modificar un ETL existente | Parcial | D23–D25, C05 | El plan no incluye un ejercicio de "modifica este ETL" con un cambio concreto. |
| 3. Desarrollar un ETL siguiendo una guía | Sí, comprimido | D22–D25 (≈250 min de práctica en el plan) | Plantilla de 4 funciones con `NotImplementedError` y tabla de 7 etapas con controles. |
| 4. Crear un ETL desde cero sin IA | Se evalúa, no se enseña específicamente | C06 (240 min) y final (12,5 h) | La ruta es "una guía, luego una transferencia, luego el examen". |

### F.2 ¿La ruta conduce al nivel 4?

**Parcialmente, y solo si cambia el calendario.** Qué hace bien:

- La arquitectura Bronze/Silver/Gold está aplicada correctamente: Bronze conserva el original; Silver conserva anulados y tipos; Gold por cliente/mes con documentos distintos; los rechazos son una salida auditada; la ecuación `Bronze = duplicados + rechazados + Silver` se exige.
- Las decisiones de diseño son las que haría un profesional junior: dinero en centavos enteros (o `Decimal`), rechazar en vez de truncar cantidades, catálogo duplicado detiene el proceso, conflicto de clave se detecta antes de eliminar duplicados, publicación mediante archivo temporal y reemplazo, repetición sin duplicar.
- Existe un método de ocho pasos (`17_Transferencia_debug.md`) y una prueba adversa de cuatro casos.
- Validé que la referencia de transferencia/final se ejecuta dos veces con resultados idénticos y que rechaza correctamente las cuatro entradas adversas (con la corrección de la conexión de D.4).

Qué impide llegar al nivel 4:

1. **Tiempo.** D22–D25 ofrece unos 250 min de práctica para 7 etapas (extraer, texto, tipos, claves, Silver, Gold, cargar con repetición). Mi estimación para una persona con tu perfil es de ~540 min. Después, C06 ofrece 240 min para construir *sin plantilla* un ETL equivalente con linea_id, catálogo y rechazos; yo estimo ~490.
2. **Salto de andamiaje.** El ETL guiado trae una plantilla de 4 funciones y una tabla de 7 etapas. C06 y el final no traen nada de eso. Falta un paso intermedio: un ETL pequeño (3 archivos de 20 filas) hecho a mano en la semana 3, y un "modifica este ETL" en la semana 4.
3. **Prerrequisitos de Python.** Pandas aparece por primera vez en D12. Entre D12 y D22 hay 10 días, de los cuales 4 son exámenes o domingos, para que `merge validate`, duplicados, fechas, `groupby`, funciones y archivos pasen a ser reflejos. No hay un ejercicio de depuración guiada (traceback → causa) hasta el caso C05.
4. **El final es el caso de transferencia más grande, no un caso nuevo.** Comprobado (mismas columnas, mismo catálogo byte a byte, mismo diccionario y mismas clases de defectos: formatos de fecha ISO y DD/MM/YYYY, rutas con espacios y mayúsculas, estados en distintas formas, precios con "Bs" y coma, cantidades decimales, `linea_id` duplicada, filas idénticas, SKU fuera del catálogo). Tiene 3× más filas. Quien haya hecho C06 con éxito ya tiene el esquema, las reglas y casi todas las funciones. Quien lo haya hecho *con ayuda de la referencia*, también.
5. **El enunciado dicta el trabajo.** Lista 10 puntos de trabajo propio con las reglas ya definidas. Real: un cliente te da un CSV y una frase. Descubrir el contrato forma parte de la habilidad que quieres demostrar y aquí se te entrega.
6. **Los datos son más limpios que los de un ERP real.** Ninguna fila tiene codificación rota, separadores mezclados, miles ("1.234,50"), cabeceras desplazadas ni columnas en blanco. Es normal para un curso de 6 semanas. Solo hay que decirlo para no sobreestimar lo que acredita.
7. **La evaluación de autonomía depende de tu honestidad** (el propio plan lo reconoce). El validador comprueba resultados, no autoría. La defensa de 10 puntos se auto-evalúa si nadie te observa.

### F.3 Qué cambiar

- Reservar 6 sesiones de ~2 h (no 4) para el ETL guiado, quitando Power BI/Excel de esas semanas (ver J).
- Insertar un mini-ETL a mano de 20 filas antes de D22 (en D19–D21).
- Añadir un ejercicio "modifica este ETL" (por ejemplo, añadir una regla de rechazo) en D26.
- Mantener C06 como práctica y **sustituir el final** por un conjunto con esquema, catálogo y defectos distintos, generado con una semilla que no esté en el paquete (J-3).
- Recortar el enunciado final a requerimiento de gerencia + criterios de aceptación; que el contrato y las reglas las escribas tú.
- Enseñar `with`/`closing` en SQLite (D.4).

---

## G. Comparación con el curso UAGRM

Lo que pude comparar: el notebook de la Clase 1 (94 celdas) y el de la Clase 2 (148 celdas), más `ml_eda_functions.py` (481 líneas, ML/EDA). El PDF no lo abrí.

| Tema UAGRM | Plan v5 | Observación |
|---|---|---|
| Clase 1: variables, tipos, casting | D01, D02 (P01–P03), cap. 07 | Cobertura coherente. |
| Listas, tuplas, strings, diccionarios, sets | D03 (P04, P05) | El plan los trata en un día. UAGRM los trata en secciones dedicadas con casos de negocio. **Aprovecha el notebook** como teoría. |
| Condicionales, bucles | D04–D05 (P06–P08) | Coherente. UAGRM incluye `while` y el caso "primer cliente en mora"; el plan no practica `while`. |
| Funciones | D05, D08 (P08, P09) | Coherente. |
| NumPy | Cap. 09 (sección corta) | UAGRM lo cubre más (arrays 2D, KPIs). |
| Ejercicios 1–5 de UAGRM (limpieza de nombres, ticket promedio, clasificar_cliente, stock crítico, KPIs) | Equivalentes: P03, P08, K1/K2 | Buen par de refuerzo. |
| Clase 2: estadística descriptiva (media, mediana, moda, rango, varianza, desviación, histogramas) | D04, D12, D19 (ST01–ST03), cap. 11 | Cubierto. El plan lo trata con sus datos de distribuidora y la clase con UCI Automobile y rendimiento escolar. |
| Calidad de datos, análisis de variables | D17 (perfilado), cap. 05 | Complementario. |
| `ml_eda_functions` (EDA/ML avanzado) | No | Correctamente fuera del núcleo. |
| Pandas (se usa en Clase 2) | D12+ | **Posible adelanto:** la Clase 2 usa DataFrames antes de que el plan los enseñe de forma guiada si la clase 2 cae en D08 (lunes 19/10), cuando el plan aún está en Python puro. No conozco el calendario de clases. |

**Contradicciones y huecos:**

- La Clase 2 necesita instalar las dependencias opcionales, crear la carpeta `functions/` y tener internet (D.7). Nadie lo avisa en la teoría; el LEEME de UAGRM solo dice "pueden requerir Colab".
- El plan trata ETL, SQL y KPIs que el curso no cubre. Para la UAGRM, el plan solo complementa lo que ya vas a ver.

**Cómo aprovechar los lunes:** la guía de los lunes (90 min de plan + 150 min de clase) es el día más corto del plan. Úsalo para **llegar con una pregunta sobre código propio**, como ya sugiere el plan. Sugiero además: el lunes por la tarde (13:00) hacer solo la parte del plan que prepare la clase (leer el notebook correspondiente, ejecutar tres celdas) y **dejar fuera del lunes cualquier ejercicio nuevo** (D15, D22, D29 y D36 son los lunes más sobrecargados).

---

## H. Preparación laboral

**Qué pude comprobar.** No existe en el paquete ni en las carpetas vecinas un análisis de vacantes verificado: `POSTULACIONES.md` lo dice ("el paquete no incluye vacantes verificadas"). La carpeta `obsidian/Data and BI` contiene solo configuración y un README. Hice dos búsquedas web: **no devolvieron vacantes de Santa Cruz, Bolivia**; solo ofertas de Colombia (Bogotá), Chile y México, y un perfil de freelancer de Cochabamba. Entonces:

- **Requisitos mencionados en los archivos:** SQL, Excel, Power BI, análisis empresarial (CV_Y_PERFIL, POSTULACIONES).
- **Información actual comprobada:** ninguna para Bolivia. Como referencia regional, las ofertas colombianas para "analista de datos junior / BI" piden Power BI, SQL (SQL Server frecuente), Excel avanzado (tablas dinámicas) y 1–2 años de experiencia. No es evidencia sobre Santa Cruz.
- **Inferencia mía (sin comprobar):** en Santa Cruz se parecería, con más peso de Excel y de sistemas ERP.

Fuentes consultadas, solo como referencia regional: [Computrabajo Colombia, analista junior Power BI/SQL](https://co.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-analista-junior-de-datos-power-bi-sql-en-bogota-dc-8ea1306aee10196061373e686dcf3405) · [Magneto365, analista BI SQL](https://www.magneto365.com/co/empleos/analista-bi-sql-1076923) · [Elempleo, analista BI](https://www.elempleo.com/co/ofertas-trabajo/analista-business-intelligence-1886732356).

### Valoración

- **Pertinencia del contenido:** SQL, Excel y Power BI son lo correcto. El plan asigna a SQL la mayor práctica; a Power BI, 6 sesiones; a Excel, 3 casos y un capítulo corto. Con la información regional, Excel está sub-cubierto.
- **Postular desde la semana 1:** es razonable *si* te presentas como lo que eres (el CV lo hace bien), a puestos de entrada de reportes, asistencia o soporte BI. No es razonable esperar entrevistas para analista de datos junior con Power BI/DAX demostrables hasta la semana 5–6.
- **CV:** el borrador es honesto. Pide no inventar SQL avanzado ni programación autónoma en la pasantía. La pasantía terminó el 8/10/2026 (según el propio CV).
- **Proyectos:** solo cuentan los terminados, con problema, fuente sintética, control y enlace. Pero tu repositorio contiene las soluciones. Debes separar.
- **Simulacros:** 6 sesiones de 30 min, autoevaluadas (grabación privada). Útiles para articular. No sustituyen una entrevista con otra persona. La guía de corrección está en la carpeta de soluciones.
- **Sostenibilidad:** 25–30 min de postulación 3 veces/semana más 2 publicaciones de LinkedIn ≈ 100–120 min/semana (≈ 12 % de las 15 h). Con la carga real de las semanas 4–5 esto es lo primero que cederá, y las dos publicaciones semanales son la exigencia más cuestionable: conviene bajarla a una.

### Puestos

| Puestos a los que puedes postular ya | Puestos que requieren más preparación |
|---|---|
| Asistente / auxiliar de reportes o de información | Analista de Datos Jr. con Power BI "intermedio" comprobable |
| Analista de reportes comerciales / inteligencia comercial (Excel + ERP) | Analista BI con SQL Server y modelado |
| Soporte funcional a ERP/POS con reportes | Ingeniero de datos / ETL (fuera del alcance del plan) |
| Asistente de BI en empresa de distribución (tu pasantía es directamente relevante) | Cualquier puesto que pida Python autónomo sin supervisión |

No es una promesa de empleo ni una garantía de que existan esas vacantes.

---

## I. Riesgos de abandono y cómo prevenirlos

Estos son riesgos de **diseño del programa**, no un diagnóstico sobre ti.

| # | Riesgo | Dónde ocurre | Prevención |
|---|---|---|---|
| 1 | **Acumulación silenciosa:** los días sobrecargados se resuelven "recortando", pero lo recortado es prerrequisito del siguiente. | D08–D12, D15–D19 | Marcar núcleo/opcional por día; puertas de competencia en lugar de fechas (ver J). |
| 2 | **Semana 4 (ETL) con 90 min un lunes y 160 un martes:** primer ETL, más tiempo del disponible, sin red de seguridad. | D22–D25 | Dar 6 sesiones al ETL; mover Power BI. |
| 3 | **Semana 5 con dos herramientas nuevas, sin validar:** Power BI y Excel se estudian por primera vez a la vez, y el autor no probó ninguno. | D29–D34 | Reducir a opcional o posponer a después del final. |
| 4 | **Un examen cada sábado.** 6 exámenes sin descanso entre ellos y cada uno sobre material de la semana, con "objetivo 70–80/100". Fallar uno desmoraliza. | D06, D13, D20, D27, D34, D41 | Que los exámenes semanales sean formativos y sin umbral hasta S04; que la nota solo informe qué reforzar. |
| 5 | **Ayuda sin fricción:** la solución está en la carpeta de al lado. Con un corrector que no localiza el error, la tentación de copiar o de pedirle a la IA aumenta. | Todos | Corregir feedback (D.4-2); sacar las soluciones del árbol de trabajo. |
| 6 | **Postulaciones y LinkedIn como presión.** Rechazos o silencio pueden desanimar en las semanas más duras. | D04+ | Una publicación/semana; postular solo con vacantes pertinentes. |
| 7 | **Falta de evidencia visible de progreso** en las primeras semanas. `progreso.csv` y `errores.md` están vacíos. | Ahora | Rellenar D01 hoy (aunque sea una línea). |
| 8 | **Concentración / distracciones.** El diseño ayuda en algo (bloques fijos, pausas de 10 min cada 45–50 min, "MÍNIMO" de 20 min), pero la sesión de 200 min de sábado es la más larga y con menos estructura. | Sábados | Dividir los sábados en 2 bloques con descanso largo. |
| 9 | **Primer error de entorno (Windows) sin explicación:** el PermissionError de D.4-1 puede aparecer en tu propio ETL. | D25, D38 | Enseñar `closing` antes de D22. |

### Recuperar días perdidos sin trasladar deuda

1. **Regla de oro:** un día perdido se pierde. No lo recuperes en el siguiente.
2. Tener una lista de "núcleo mínimo" por día (1 SQL + 1 Python + 1 explicación de 3 líneas), de 45 min. Si solo haces eso, el día cuenta como avanzado.
3. Usar un **calendario por puertas**: las 6 puertas del plan (S01..S06) se abren cuando demuestras la base, no cuando llega la fecha. Si en la fecha de S02 no tienes la puerta 1, se hace S02 una semana después, y se mueve toda la secuencia, incluyendo el final.
4. Si la puerta 3 (JOIN + merge) no se cumple, **no empieces el ETL**: ya lo dice el plan, pero necesita un mecanismo concreto para mover fechas.
5. Los domingos son de descanso total. Sin consultas y sin commits.
6. Si la semana 5 se retrasa, Power BI/Excel es lo primero que se mueve.

Respeto tu descanso y tus creencias; el análisis no los utiliza como justificación.

---

## J. Correcciones recomendadas

No he cambiado nada. Esta lista es para decidir contigo.

### CRÍTICO

| # | Cambio | Por qué | Esfuerzo |
|---|---|---|---|
| J-1 | **Reequilibrar las semanas 4–6.** Dar al ETL guiado 6 sesiones (no 4). Mover Power BI/Excel a "opcional" o a después del final; dejar en semana 5 la estadística de apoyo, el mini-ETL y el refuerzo de lo que falle. | Sección C: 1,3–2,1× lo disponible. La meta es un ETL propio, no un dashboard. | Medio (reordenar guías D26–D41) |
| J-2 | **Marcar núcleo/opcional en cada una de las 36 guías** y convertir los hitos en puertas (competencia demostrada), no fechas. | Sin esto, "recorta sin deuda" es una instrucción vacía. | Medio |
| J-3 | **Sustituir el final por una variante realmente nueva**: otro esquema, otro catálogo, otros defectos, preferiblemente generada con una semilla que tú no conozcas (por ejemplo, un amigo o una herramienta tuya ejecutada el 23/11). Mantener el actual como C06. Reducir el enunciado: requerimiento + criterios de aceptación, sin lista de defectos. | Sección F: hoy el final es un clon ampliado de C06. | Medio |
| J-4 | **Sacar de tu árbol de trabajo las claves de respuesta del final** (`controles_final.json`, `silver_final_esperada.csv`, `etl_nuevo_referencia.py`) y las cifras de `resultados_pruebas.json`, `INFORME_VALIDACION.md` y la prueba P30. Guardarlas comprimidas con clave o fuera del repositorio. | Hallazgo 3. | Bajo |
| J-5 | **Corregir el bug de Windows** (`con.close()` o `contextlib.closing`) en la referencia y en los validadores, y **enseñarlo** en el capítulo 05. Actualizar el informe: "11/13 en Windows; 13/13 tras la corrección". | Hallazgo 1. | Bajo |

### IMPORTANTE

| # | Cambio | Por qué |
|---|---|---|
| J-6 | **Mejorar los correctores:** mostrar el caso que falló (entrada, esperado, obtenido); para SQL, mostrar el nº de filas y las 3 primeras diferencias; endurecer P05 y otros tests débiles. | Hallazgo 2. |
| J-7 | **Pistas y enunciados específicos** por ejercicio, al menos para los de nivel 2–3 (≈ 40 ejercicios). Corregir P09 (decir `ValueError`) y V4 (decir la convención en el enunciado). | E.2 puntos 1, 6; D.4-6. |
| J-8 | **Duplicar los tiempos objetivo** de los ejercicios de nivel 2–3, o declarar dos columnas (con solución en mente / primera vez). | E.2-2. |
| J-9 | **Ampliar la teoría de Python/Pandas** con 3–4 ejemplos resueltos con salida visible por capítulo. Los capítulos 07–10 son compactos para quien depende de la IA. | E.2-9. |
| J-10 | **Añadir ejercicios-puente**: un mini-ETL a mano (D19–D21); un "modifica este ETL" (D26); una sesión de depuración dirigida (leer un traceback). | F.3. |
| J-11 | **Separar repositorios:** uno privado con el paquete y otro, tuyo, solo con `mi_trabajo` (código propio, README, resultados) que sí puedas mostrar. Comprobar la visibilidad del remoto actual. | Hallazgo 4. |
| J-12 | **Verificar DAX y Power BI en Desktop** antes de usarlos (especialmente `Crecimiento`), y añadir un capítulo ampliado de Excel (tablas dinámicas), dado el peso de Excel en vacantes. | Hallazgo 5; E.1. |
| J-13 | **Revisar los exámenes:** corregir texto dañado, quitar el nº de filas esperado, hacer que S01–S03 incluyan al menos una pregunta nueva, y rediseñar ES1B. | D.1, D.4-6. |
| J-14 | **Documentar el uso del notebook de Clase 2** (instalar opcionales, crear `functions/`, internet) y dejar una tabla UAGRM ↔ plan por fecha de clase. | D.7, G. |
| J-15 | **Comentar las soluciones SQL** (3–5 líneas con el razonamiento). | E.2-8. |
| J-16 | **Bajar las publicaciones de LinkedIn a una por semana** y dejar las postulaciones como "hasta 3/semana". | I-6. |

### OPCIONAL

- Asignar o retirar S4 y CL2. Fusionar K2a/N9.
- Incluir un `while` y un ejercicio con datos desordenados dentro de la base SQL.
- Añadir una página sobre diferencias SQLite ↔ SQL Server con 3–5 consultas traducidas.
- Sustituir `ejecutar_sql.py` por una salida tabulada.
- Regenerar el manifiesto SHA256 tras los cambios.
- Añadir una sesión de entrevista real o con un compañero.
- Escribir un ejercicio de redacción de recomendaciones a gerencia por KPI.
- Revisar la numeración de versiones en `versiones.json`.

---

## K. Dictamen profesional

1. **¿El programa es razonable para una persona de tu nivel?** El *contenido y el orden* sí. El *calendario* no lo es: supone que cada ejercicio se resuelve en el tiempo que declara. Con los cambios J-1 y J-2 pasa a ser razonable.

2. **¿Está demasiado cargado?** Sí. 25 de 36 jornadas activas superan 1,5× según mi modelo central, y las semanas 4 y 5 superan 1,3× incluso en el caso optimista (Sección C). Las semanas 1–2 son manejables.

3. **¿Puedo aprender SQL y Python de verdad con esta metodología?** SQL: sí, probablemente. Hay práctica diaria durante 6 semanas, un corrector inmediato y una sola base que permite concentrarte en el razonamiento. Python: parcialmente. El método (intento, depuración, pista, explicar) es el correcto, pero la teoría es muy breve, las pistas son genéricas y el corrector no localiza el error. El aprendizaje real dependerá en gran medida de que uses la clase de UAGRM y de que tú anotes por qué fallaste.

4. **¿Aprenderé analítica de negocio y KPIs?** Sí, es la parte mejor resuelta: 13 KPIs con fórmula, ejemplo, error común y ejercicio con datos que cuadran. Falta práctica de redacción de recomendaciones a gerencia.

5. **¿Aprenderé estadística empresarial práctica?** Descriptiva y percentiles/atípicos, sí. Inferencia (IC, Welch, χ²), solo de forma introductoria y en días muy cargados. Es razonable dejarla como opcional.

6. **¿Me ayudará con las clases de la UAGRM?** Sí en Python (Clase 1: D01–D05 cubren lo mismo con otra práctica) y en estadística descriptiva. La Clase 2 requiere preparar el entorno (D.7).

7. **¿Me preparará para entrevistas junior?** Para entrevistas de SQL, KPIs y explicar tus decisiones, sí, bastante. Para entrevistas con Power BI o Excel avanzado, no, porque ambos están menos cubiertos y el autor no ejecutó Desktop. Los simulacros son de autoevaluación.

8. **¿Podré crear un ETL nuevo sin IA a finales de noviembre, si demuestro los prerrequisitos?** Es posible para un ETL junior de alcance definido, pero con probabilidad moderada y bajo tres condiciones: (a) que las puertas de las semanas 2–4 se cumplan de verdad (JOIN, `merge validate`, funciones con `return` y errores, duplicados) aunque haya que mover fechas; (b) que C06 se haga sin abrir la referencia, aunque tarde más de 240 min; (c) que el final sea una variante nueva (J-3), porque el actual medirá sobre todo cuánto recuerdas de C06. Como está, aprobar el final no demostraría con suficiente certeza el nivel 4.

9. **¿Qué habilidades probablemente requerirán más tiempo?** (a) Leer un traceback y depurar sin IA; (b) pasar de escribir funciones a diseñar un programa de 150–300 líneas con extracción, validación y carga; (c) `merge`/`groupby` con control de cardinalidad en Pandas; (d) funciones de ventana y ABC; (e) DAX y contexto de filtro, si decides mantenerlo; (f) la interpretación estadística (p-valor, supuestos).

10. **¿Qué cambios son indispensables antes de comenzar?** Los cinco críticos de la sección J. Si solo puedes hacer algunos ahora: **J-2** (núcleo/opcional + puertas) y **J-1** (más tiempo al ETL; Power BI fuera de la ruta crítica). Los otros tres no te frenan hoy: J-5 debe estar antes de D22 (2/11), y J-3 y J-4 antes de D36 (16/11).

**Sobre el momento:** hoy es D02, así que las semanas 1–2 pueden seguir como están con los recortes que sugiere la tabla. Los cambios estructurales (J-1, J-2) pueden decidirse esta semana sin bloquear nada.

---

## L. Evidencias

### Comandos ejecutados (resumen)

```text
# Inventario y lectura
Get-ChildItem/find sobre el proyecto (sin .venv/.git); lectura de README, PLAN_V5, HITOS, 42 guías (extracción automática + lectura de D01, D04, D06, D23, D25),
teoría (01, 05, 06, 07–10, 17), ejercicios (S1, G1, X3, N1, P01–P30, C05, C06, ES*), exámenes S01–S06,
herramientas/*.py, 08_SOLUCIONES (lectura puntual), 09_EVALUACION_FINAL, 10_VALIDACION, 05_PROYECTOS/powerbi, 07_LINKEDIN_EMPLEO

# Entorno
.venv\Scripts\python.exe --version ; -m pip list ; -m pip check
.venv\Scripts\python.exe -m pip install --dry-run -r requirements_uagrm_opcional.txt   (sin instalar)
py -0p
.venv\Scripts\python.exe herramientas/comprobar_entorno.py
.venv\Scripts\python.exe herramientas/ejecutar_sql.py --consulta "SELECT COUNT(*) AS clientes FROM clientes;"

# Verificación del paquete (sobre COPIA en el directorio temporal)
python herramientas/verificar_paquete.py        → 11 OK, 2 ERROR (PermissionError WinError 32)
(mismo comando tras añadir con.close() solo en la copia)  → 13/13 OK

# Pruebas propias (lectura de los originales)
- PRAGMA integrity_check / foreign_key_check / conteos / nulos / duplicados / huérfanos en comercial.db y distribuidora.db
- Recálculo independiente en Pandas de J3, K2a, K3, K4, V2, V4, N1, N2, N3, N4, N5, N12 vs controles_sql.json
- Verificación de 403 hashes SHA256 del manifiesto; 389 enlaces internos; archivos vacíos; duplicados exactos
- Simulación de errores de principiante contra corregir_python.py y corregir_sql.py (copia)
- Perfil de clases de defectos de transferencia vs final (solo presencia/ausencia, no valores esperados)
- Ejecución en proceso de las 58 celdas de código de la Clase 1 UAGRM (copia)
- Comprobación de importaciones de la Clase 2 UAGRM
- Cobertura de funciones SQL por día en las soluciones; estimación de tiempos (scripts en el directorio temporal de la sesión)
- Dos búsquedas web de vacantes (sin resultados para Santa Cruz)
```

### Resultados relevantes

- 407 archivos; 0 vacíos; 403/403 hashes; 389 enlaces, 0 rotos.
- 12 controles de negocio recalculados de forma independiente: coinciden.
- `verificar_paquete.py`: 11/13 en Windows (2 fallos por conexión SQLite sin cerrar), 13/13 con la corrección.
- Final y transferencia: mismo esquema, catálogo idéntico, mismo diccionario y mismas clases de defectos.
- Clase 1 UAGRM: 58/58 celdas OK. Clase 2: no ejecutable sin instalar opcionales y crear `functions/`.

### Archivos revisados

Leídos de forma completa o casi completa: README, PLAN_V5, HITOS_Y_RECUPERACION, `01_SQL_basico`, `05_calidad_ETL`, `07`–`10`, `17`, parte de `06_KPIs`, `18`/`16`/`15` (solo encabezados), S1, G1, X3, N1, P01, P09, P17, P22, P29, P30, C05, C06, CASOS.md, ES1A–ES3C, S01, S04, S06 (S02/S03/S05 solo tareas y puntuación), todos los de `herramientas`, `ENUNCIADO`/`RUBRICA`/`DICCIONARIO` del final, `medidas.dax`, `cargar_csv.m`, `MODELO.md`, PB01, `INFORME_VALIDACION`, `DECISIONES_Y_CORRECCIONES`, `CV_Y_PERFIL`, `POSTULACIONES`, `CONTACTOS`, parte de `LINKEDIN_12_BORRADORES`.

Leídos solo parcialmente o por muestreo: el resto de las 42 guías (analizadas mediante extracción automática de título, objetivo, bloques y enlaces), el resto de la teoría, los ejercicios no citados (verificados mediante el análisis de tiempos, niveles y contratos), los siete notebooks N01–N07 (N01 y N05 inspeccionados), la guía de entrevistas y el banco de preguntas (muestreo).

### Limitaciones

1. **No hay mediciones de tu velocidad real.** Los tiempos de la sección C son un modelo con supuestos declarados; el error razonable es ±35 %. Registrar tus minutos reales en `progreso.csv` durante las dos primeras semanas es lo que mejorará esta estimación.
2. **No ejecuté Power BI Desktop ni Excel.** Los comentarios sobre DAX/M son análisis estático.
3. **No abrí el PDF de la UAGRM ni ejecuté la Clase 2** (dependencias y conexión a UCI).
4. **No probé SQL Server ni PostgreSQL.** Todo es SQLite.
5. **Vacantes:** no pude verificar vacantes de Santa Cruz; las fuentes que encontré son de otros países.
6. **Evaluación final:** la ejecución de `verificar_paquete.py` incluyó, sobre una copia temporal descartada, la ejecución de la referencia contra los datos del final (necesaria para validar el paquete); no conservé ni presento sus resultados. Una búsqueda de fuga imprimió cifras del final en la salida de mi sesión (D.4-3). No las uso en este informe.
7. **No leí todos los ejercicios uno por uno.** Las 42 guías, los 81 SQL, los 30 Python y los 15 casos se analizaron principalmente a través de plantillas, contratos y datos extraídos automáticamente; los casos individuales citados sí fueron leídos.
8. **No se modificó ningún archivo del plan.** La única creación es este informe; las pruebas y los scripts están en el directorio temporal de la sesión.
