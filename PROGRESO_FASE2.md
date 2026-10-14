# PROGRESO FASE 2 — Plan Data & BI v5

Última actualización: 2026-10-13 (cierre de la Etapa 2).

## Estado de las etapas

| Etapa | Estado |
|---|---|
| Etapa 1 — Reconstrucción de la teoría (`02_TEORIA`) | **COMPLETA** (informe: `INFORME_FASE2_ETAPA1_TEORIA.md`) |
| Etapa 2 — Integración pedagógica, calendario y modalidades de estudio | **COMPLETA, pendiente de revisión del usuario** (informe: `INFORME_FASE2_ETAPA2_CALENDARIO.md`) |
| Etapa 3 — Exámenes, evaluación final y validación completa | **PENDIENTE** (no autorizada; requiere la frase exacta «AUTORIZO ETAPA 3») |

## Última tarea completada

Cierre de la Etapa 2:

- **Teoría**: las 100 lecciones están clasificadas una a una en `01_PLAN_DIARIO/lecciones.json` (47 NÚCLEO con día, 33 REFUERZO, 20 PROFUNDIZACIÓN). Los índices de capítulo muestran la clase y el día. Todas siguen disponibles como consulta.
- **Jornadas**: `aplicar_nucleo.py` genera las 42 guías (D02 solo con un bloque informativo de lecciones, D01 intacta) con lecciones NÚCLEO y minutos de lectura, bloques Lecciones/SQL/Práctica/Criterio, EXTENDIDA voluntaria y domingos flexibles (45–120 min). También genera `calendario.json/csv`, `CARGA_ESTIMADA.md`, `RUTAS.md` (BASE/EXTENDIDA, teoría frente a práctica, prerrequisitos, 42 jornadas) y la columna «Tipo» de los capítulos.
- **Criterio analítico y comprensión**: `03_EJERCICIOS/Analitico/AN01–AN18` y `03_EJERCICIOS/Comprension/H01–H08`; controles en `08_SOLUCIONES/controles_analitico.json/.md` (42 cifras recalculables).
- **Integración**: P02 y P07 reparados y, con ellos, 27 enunciados de Python, 28 de SQL (solo el puntero) y el formato de los criterios de ST01–ST07; orden de los capítulos 5 y 6 documentado en `INDICE.md`; N1 y mapa UAGRM escritos; 484 min de ejercicios pasaron de OBLIGATORIO a REFUERZO/OPCIONAL y 12 ejercicios cambiaron de día (detalle en el informe).
- **Verificación**: `herramientas/verificar_etapa2.py` (9 grupos; 20 de 20 mutaciones detectadas), `verificar_teoria.py`, `auditar_enunciados.py` y `verificar_paquete.py` (21 de 21 en copia temporal), todos con el `.venv` (Python 3.12.10, pandas 2.2.3). Manifiesto SHA256 regenerado.

## Próxima tarea exacta

**Detenerse y esperar la revisión del usuario.** No iniciar la Etapa 3 sin la frase exacta «AUTORIZO ETAPA 3». Decisiones abiertas para el usuario (informe, sección 10): (1) aceptar BASE = 15 h planificadas y ≈ 16,5 h estimadas, o mover más ejercicios a REFUERZO (implica ajustar exámenes en la Etapa 3); (2) si alguna de las 17 lecturas «recomendadas» debe ser NÚCLEO; (3) si ST01/ST02 vuelven a ser obligatorios.

Cuando se autorice la Etapa 3: mejorar S01–S06 (alinear con hitos H01–H08 y con los OBLIGATORIOS actuales), rediseñar la evaluación final (nuevo esquema/dominio, claves privadas fuera del repositorio, sin reescribir historial), validación completa, sincronización final e `INFORME_FASE2_FINAL.md`.

## Restricciones y decisiones vigentes

- Rama única `main`. Sin commits, merges, rebase, reset destructivo ni push. Sin ramas nuevas.
- No tocar `mi_trabajo`, D01 ni los objetivos/ejercicios/tiempos de D02. No cambiar los 81 enunciados SQL salvo el puntero a la lección cuando estaba desactualizado (hecho). No se modificaron los exámenes.
- Fuente única de la ruta: `01_PLAN_DIARIO/nucleo.json` (jornadas, ejercicios, lecciones del día, criterio) y `01_PLAN_DIARIO/lecciones.json` (clasificación y cobertura de prerrequisitos). Todo lo demás (guías, calendario, carga, rutas, columna «Tipo») se regenera con `python herramientas/aplicar_nucleo.py`.
- Los ejemplos de las lecciones usan `04_DATASETS/mini_base/`; la teoría no publica resultados de ejercicios; los enunciados `AN`/`H` tampoco (`verificar_etapa2.py` lo comprueba).
- El código DAX/M y los pasos de Power BI Desktop, de Excel y los ejemplos de SQL Server **no se ejecutaron**; H07 lo declara.
- Los tiempos son estimaciones de primera vez (±35 %), no mediciones.
- Usar siempre el intérprete del `.venv` (3.12.10, pandas 2.2.3) para verificar: el `python` del sistema es 3.14 con pandas 3.0.3 y da resultados distintos.
- Escribir guías o documentos con Python desde Bash en Windows: los heredocs alteran las barras invertidas; guardar el script en un archivo antes de ejecutarlo.
- Etapa 3 (no autorizada): mejorar exámenes S01–S06, rediseñar la evaluación final, validación completa, sincronización final e `INFORME_FASE2_FINAL.md`.
