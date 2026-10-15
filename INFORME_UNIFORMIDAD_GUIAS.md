# Cierre editorial de las guías · Plan Data & BI v5

2026-10-15 · repositorio original · rama `main` · referencia inicial `00b6f1c`, limpia.
Corrección editorial localizada y comprobación de dependencias; sin reconstrucción curricular.
La uniformidad del 14 de octubre ya estaba incorporada. Este informe registra las comprobaciones
nuevas; las pruebas históricas de fases anteriores no se cuentan como ejecutadas ahora.

## Referencias y correcciones

Se leyeron D01, D02, D05, D12 y D18; los informes de organización didáctica y uniformidad;
`nucleo.json`, `lecciones.json` y el generador. Se contrastaron nueve ejercicios con su teoría,
RUTAS y clasificación; las otras 40 jornadas recibieron una comprobación automática ligera.

D01/D02 conservan su estructura organizada: objetivo/modalidades → teoría → distribución →
prerrequisitos y competencias → práctica por prioridad → comprobación → REDUCIDO/MÍNIMO → empleo.
No se inventaron actividades de criterio ni EXTENDIDA para esas jornadas.

- Preparaciones de S1/S2/P01/P02/P03: ahora utilizan el mismo nombre y destino que la guía.
  Los índices quedan como consulta; las secciones iniciales no obligan a adelantar lecciones completas.
- P03 identifica explícitamente que «7.5 · Texto: limpieza, inmutabilidad y partir/unir» abre la sección
  «Base inicial de texto»: **una sola lectura de 12 min**, dentro de los 34 de 7.5; quedan 22 de desarrollo.
- S7 enlaza directamente 1.4. P02 enlaza 7.6 antes de su sección de decisiones de 7.10.
- C01 atribuía sus definiciones a un índice. Ahora apunta a **6.2 → Términos nuevos** y ofrece como
  consulta voluntaria el primer mini-informe de 6.6, sin exigir sus ejemplos SQL/Pandas.
- D01/D02 señalan la preparación de S10, S9 y C01 dentro de REFUERZO/OPCIONAL; no se añade a BASE.
  S10 abre directamente los ejemplos 1 y 2 de 2.1, conservando sus aproximadamente 4 min voluntarios.
- D02 distingue **61 min de lectura asignada** (35 NÚCLEO + 26 de secciones previas) del bloque
  planificado de teoría de 30 min. Mantiene reducción de entrega y recuperación antes del ejercicio.

| Actividad | Clasificación conservada | Teoría antes del intento |
|---|---|---|
| S1 | D01 · BASE | 1.2, preparación de tabla/selección/orden/límite, 8 min |
| P01 | D01 · BASE | 7.4, variables/tipos/función/retorno, 8 min |
| S10 | D01 · REFUERZO | 2.1, solo ejemplos 1–2 |
| S2 | D02 · BASE | 1.6, introducción de DISTINCT, 7 min |
| S7 | D02 · BASE | 1.4, NULL, 15 min |
| P02 | D02 · BASE | 7.6, 20 min; después introducción de decisiones de 7.10, 7 min |
| P03 | D02 · BASE | 7.5, sección inicial de texto, 12 min |
| S9 | D02 · REFUERZO | 1.3, condiciones y operadores |
| C01 | D02 · OPCIONAL | Definiciones de 6.2; mini-informe de 6.6 como consulta voluntaria |

Las seis actividades BASE tenían enseñanza suficiente: no fue necesario añadir ni reescribir teoría.
Las pistas conservan su función posterior al intento; soluciones y comprobaciones siguen separadas.

## D12, D32 y alcance conservado

**D12:** división intencional de 6.1: 6 min iniciales + 25 restantes = 31. Con 9.2 son 51 min de lectura
asignada; el bloque de 45 corresponde a 25 + 20, y los 6 iniciales ya estaban en la estimación BASE.
Se aclara esa diferencia y el uso de `#desarrollo`, antes de AN07; no cambian competencia ni jornada.

**D32:** REDUCIDO anunciaba 30 min restantes de 14.1 pero abría la lectura completa de 34.
Ahora enlaza `#desarrollo` y recuerda recuperar los 4 min de calendario antes de PB02 si se aplazó.
Es el único enlace de lectura reducida con este defecto entre las 40 jornadas revisadas.

Las **38 guías fuera de D01/D02/D12/D32**, incluidas D05 y D18, permanecen idénticas.
Se conservan domingos, exámenes, proyectos, hitos, UAGRM y las recuperaciones anteriores.
Fuentes, calendarios, índices, RUTAS, carga y las 100 lecciones no requieren cambios.
Permanecen **5400 min / 90 h planificadas**, **5813 min / 96,9 h estimadas** y **570 min / 9,5 h** de
evaluación posterior; los 42 min de preparaciones adicionales anteriores no se duplican.

## Comprobaciones ejecutadas en este cierre

Entorno `.venv`, Python **3.12.10**, sin bytecode ni resultados de pruebas escritos en el repositorio.
Instantánea y respaldos anteriores a la edición guardados fuera del repositorio.

- **705 enlaces locales válidos, 36 con fragmento:** 528/19 en las 42 guías; 13/8 en nueve ejercicios;
  52/1 en 13 archivos teóricos relacionados; 112/8 en RUTAS. No se comprobaron páginas externas.
- **7/7 grupos dirigidos** existentes: lecciones, jornadas, guías, preparación/secuencia,
  ejercicios/lecciones, documentos y sincronización. Ocho preparaciones conservadas en teoría;
  179 enunciados Markdown sin clases reintroducidas. No se ejecutó la suite general.
- Dos pasadas completas en copia temporal: **368 archivos, cero diferencias** en la segunda pasada.
  Se trasladaron solo 12 diferencias editoriales revisadas; no se regeneraron las 42 guías originales.
- **571 casillas de las 42 guías**, incluidas las 10 de D01 y las 15 de D02, con líneas, orden y estados
  idénticos a la instantánea actual. También se conservaron las casillas de los nueve ejercicios.
- Cuerpos de los nueve problemas intactos desde «Situación», salvo la corrección del puntero documental
  de C01. Reglas, datos, ejemplos, pistas, aceptación y entrega conservados; sin soluciones modificadas.
- SHA256 confirma intactos los ocho archivos personales, toda la teoría, soluciones, datos,
  evaluaciones, fuentes y carga. Objetivos/fechas intactos; sin acceso a custodia privada.
- Manifiesto SHA256 regenerado y vigente (**590 archivos**); `git diff --check`, salida 0.

No se repitieron las regresiones históricas, suites técnicas ETL, exámenes ni toda la teoría.
El control heredado que limita D01/D02 a cambios dentro de «Qué estudiar» conserva su restricción
anterior; no se modificó ni se volvió a ejecutar. La conservación se comprobó contra la instantánea
actual, incluyendo las secciones de práctica autorizadas. Los validadores permanecen intactos.

## Archivos realmente modificados y Git

**15 archivos existentes modificados; ninguno nuevo:** cuatro guías (D01, D02, D12, D32), ocho
enunciados (S1, S2, S7, S10, P01, P02, P03, C01), `herramientas/aplicar_nucleo.py`,
`10_VALIDACION/MANIFIESTO_SHA256.json` y este informe. S9 se revisó y quedó intacto.
El generador solo necesita aclarar D12 y dirigir la lectura parcial de REDUCIDO al desarrollo.

Git permanece en `main`, HEAD `00b6f1c`, con esas 15 modificaciones sin preparar para commit.
Sin commits, push, ramas ni operaciones destructivas. Trabajo detenido para revisión del usuario.
