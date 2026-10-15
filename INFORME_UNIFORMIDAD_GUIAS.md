# Uniformidad de las guías diarias

Fecha: 2026-10-14. Repositorio original, rama `main`; referencia inicial `4909893`.
Al iniciar no había cambios pendientes. Ajuste exclusivamente editorial, tomando D05 como referencia.

## Organización resultante

D01/D02 combinaban índices genéricos, lecturas previas y práctica sin separación visual de prioridades.
D02 además repetía los enlaces a 1.4 y 7.6 en un bloque añadido de lecciones.

- **D01:** preparación BASE de 1.2 y 7.4 antes de S1/P01; consulta como REFUERZO; distribución original;
  «Antes de empezar» y «Se aprende hoy»; S1/P01 OBLIGATORIOS y S10 REFUERZO, aunque esté realizado.
- **D02:** una sola secuencia de teoría: sección de DISTINCT → texto → 1.4 NULL → 7.6 booleanos,
  comparaciones y None → sección de condicionales. S2/S7/P02/P03 son BASE, S9 REFUERZO y C01 OPCIONAL.
  Cada lectura precede a su ejercicio; se conservan recuperación y descuentos por lectura parcial.
- En ambos se conservaron comprobación, entrega, REDUCIDO, MÍNIMO, empleo y las indicaciones de UAGRM.
  No se añadieron tareas, puertas ni modalidades inexistentes para imitar D05.

**D03–D42: ninguna modificación.** La revisión ligera comprobó sus 40 guías, incluidas seis de examen
y seis domingos flexibles: encabezados y orden, fechas/nombres, lecciones, prioridades, modalidades,
asignaciones contra `nucleo.json`, recuperaciones y particularidades. No aparecieron defectos verificables.

## Conservación y generación

Se conservaron literalmente las **10 casillas de D01 y las 15 de D02**, con sus estados asociados a cada
actividad. Los 42 objetivos permanecen iguales; en D01/D02 también son idénticos los bloques de tiempo
y todo el contenido desde «Comprobar y entregar» hasta el cierre.

El generador migra la presentación heredada sin reconstruir las guías personales. Mueve cada actividad
con sus notas, mantiene las notas de estudio y respeta las ediciones posteriores. Al regenerar valida
lecturas y categorías contra las fuentes; una discordancia se detiene explícitamente para evitar borrar
avance personal o aparentar sincronización. No vuelve a publicar el bloque antiguo de D02.

La generación se probó primero en una copia temporal: solo difirieron D01, D02 y una frase de `RUTAS.md`.
Se trasladaron únicamente esas diferencias al original. Dos pasadas consecutivas fueron idénticas en
los **368 archivos** de la copia, incluidos calendario, fuentes e índices.

Sin cambios en `nucleo.json`, `lecciones.json`, calendario JSON/CSV ni `CARGA_ESTIMADA.md`:
**5400 min / 90 h BASE**, estimación **5813 min / 96,9 h**, 42 min adicionales ya contabilizados y
evaluación final separada de **570 min / 9,5 h**. Ningún cambio en obligaciones o prerrequisitos corregidos.

## Comprobaciones ejecutadas ahora

Con `.venv`, Python **3.12.10**, sin generar resultados de pruebas en el repositorio:

- 42 guías: **524 enlaces locales**, **15 con anclas**, todos válidos. No fue necesario corregir rutas
  ni anclas; se eliminó la duplicación editorial de las lecturas 1.4/7.6 en D02.
- **18 regresiones editoriales** en memoria: notas dentro de los bloques heredados, notas asociadas a
  ejercicios, notas junto a casillas NÚCLEO, estado `X`, avance posterior e idempotencia; rechazo de
  cambios discordantes de minutos, categorías, asignación NÚCLEO, eliminación, traslado u orden de preparaciones.
- **7/7 grupos pertinentes** del verificador existente: `lecciones`, `jornadas`, `guias`,
  `preparacion_secuencia`, `ejercicios_y_lecciones`, `documentos` y `sincronizacion`.
  Incluyen las ocho preparaciones conservadas en teoría y 179 enunciados Markdown sin clases reintroducidas.
- Comparación SHA256 con la instantánea inicial: intactos D03–D42, los siete archivos de `mi_trabajo`,
  teoría, ejercicios, soluciones, evaluaciones, proyectos, validadores, datasets y materiales UAGRM.
- Manifiesto SHA256 regenerado y comprobado: **590 archivos**. `git diff --check`: sin errores.

**Limitación del control heredado:** se ejecutó por separado `sin_cambios_en_mi_trabajo` como diagnóstico.
Detecta «D01: cambio fuera de orientación» porque aún prohíbe modificar la presentación de «Práctica».
Se mantuvo el validador intacto, conforme al alcance autorizado. Para esta tarea se comprobó conservación
contra la instantánea de sesión, incluyendo casillas, actividades, tiempos, entrega y trabajo personal.
No se declara aprobada la suite completa. No se repitieron pruebas ETL, privadas, de exámenes ni la suite
completa de teoría; los resultados históricos de fases anteriores no se cuentan como pruebas de este ajuste.

## Archivos y estado final

Modificados: `herramientas/aplicar_nucleo.py`, `01_PLAN_DIARIO/dias/D01_2026-10-12.md`,
`01_PLAN_DIARIO/dias/D02_2026-10-13.md`, `01_PLAN_DIARIO/RUTAS.md` y
`10_VALIDACION/MANIFIESTO_SHA256.json`. Nuevo: este informe.

Git permanece en `main`, commit `4909893`: **cinco archivos modificados y un informe nuevo**, sin preparar
para commit. No se hicieron commits, push, ramas ni operaciones destructivas de Git. Se detiene el trabajo
para revisión del usuario.
