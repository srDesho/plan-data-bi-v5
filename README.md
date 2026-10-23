# Plan Data & BI v 5

Programa de seis semanas para construir bases de SQL, Python y BI con práctica autónoma.
Formación: **12 de octubre–22 de noviembre de 2026**. Evaluación final: **23–30 de noviembre**.
Todos los datos comerciales son sintéticos. El objetivo es un ETL junior propio, validado y explicable;
la ejecución de las referencias del paquete no demuestra que tú ya adquiriste esa habilidad.

## Abrir el programa

1. Extrae todo el ZIP a una carpeta, por ejemplo `C:\Plan_Data_BI_v5_Completo`.
2. Abre esa carpeta en VS Code; no abras únicamente un archivo suelto.
3. Lee [el Plan v5](01_PLAN_DIARIO/PLAN_V5.md) y después [el Día 1](01_PLAN_DIARIO/dias/D01_2026-10-12.md).
4. Elige COMPLETO, REDUCIDO o MÍNIMO antes de empezar. Cada guía diaria calcula su carga desde sus actividades: las 42 jornadas suman **157 h 32 min de trabajo BASE** (ver [`CARGA_ESTIMADA.md`](01_PLAN_DIARIO/CARGA_ESTIMADA.md)); las jornadas que superan su máximo se dividen en **sesiones retomables** que puedes repartir en más de un día real sin cambiar la fecha académica, y los domingos son descanso (0 min obligatorios). La clase UAGRM del lunes 19:30–22:00 va aparte. Una obligación omitida en REDUCIDO o MÍNIMO permanece **OBLIGATORIO PENDIENTE** hasta recuperarla.

5. Trabaja en `mi_trabajo`, creada con el comando indicado abajo. Las referencias están separadas
   en `08_SOLUCIONES`; consulta después de intentar y depurar, nunca durante los exámenes.

## Instalar en Windows 11

Usa Python 3.12 y VS Code. Power BI Desktop y Excel se utilizan en la semana 5, no el primer día.
Puedes instalar DBeaver/DB Browser para una interfaz SQLite, pero el ejecutor incluido funciona sin ellos.
SQLite viene con Python; no necesitas servidor, Docker, cloud, Airflow ni una suscripción adicional.
La instalación de dependencias necesita internet; la práctica central usa archivos locales.

En PowerShell, dentro de la raíz de esta carpeta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe herramientas/comprobar_entorno.py
.\.venv\Scripts\python.exe herramientas/crear_espacio.py
```

No es necesario activar el entorno para usar estos comandos. En las guías, `python ...` significa
el intérprete de ese entorno: sustituye `python` por `.\.venv\Scripts\python.exe` en PowerShell.
En VS Code selecciona Python: Select Interpreter y elige `.venv`; instala las extensiones Python/Jupyter
si quieres ejecutar notebooks. Alternativa para SQL: el script siguiente, sin aplicación gráfica.

```powershell
.\.venv\Scripts\python.exe herramientas/ejecutar_sql.py --consulta "SELECT COUNT(*) AS clientes FROM clientes;"
```

Resultado esperado: 120 clientes. Si `py -3.12` no existe, instala Python 3.12 y repite;
no cambies las dependencias sin comprobar su compatibilidad. Las versiones exactas probadas
están en `10_VALIDACION/versiones.json`. Las dependencias opcionales UAGRM van en un archivo separado.

## Día 1: una entrega pequeña

- [ ] Entorno comprobado y carpeta de trabajo creada.
- [ ] Lee el concepto de granularidad en SQL y variables en Python.
- [ ] Escribe S1 tú mismo en `mi_trabajo/sql`, ejecuta y explica qué representa una fila. S10 practica `COUNT(*)`: conserva cualquier realización ya registrada y, si aún falta, inténtalo después de estudiar agregación en 2.1; no es un segundo requisito de inicio.
- [ ] Calcula una venta con cantidad y precio en un script propio (P01).
- [ ] Registra un error o aprendizaje; antes de mirar la solución prueba otra entrada.

Si el 12 ya es tarde, usa MÍNIMO: 15 minutos de una consulta y cinco de explicación; prioriza la clase
y descanso. El martes sigue su bloque; no debes recuperar una jornada completa.

## Corregir sin copiar

```powershell
.\.venv\Scripts\python.exe herramientas/corregir_sql.py S1 mi_trabajo/sql/S1.sql
.\.venv\Scripts\python.exe herramientas/corregir_python.py P01 mi_trabajo/python/mis_funciones.py
```

El corrector Python espera funciones con los nombres del contrato. Al principio puedes resolver
con variables y bucles en un script; al estudiar funciones adapta la solución a la firma pedida.
Copia `03_EJERCICIOS/Python/plantilla.py` a tu carpeta y completa una función por vez.
`NotImplementedError` en una plantilla significa trabajo deliberadamente sin resolver, no un pipeline terminado.

Método: intento propio diez minutos → ejecutar/comprobar → depurar diez minutos → pedir una pista
→ consultar referencia y explicar la diferencia. Aprueba únicamente lo que puedes repetir y defender.
Los ejercicios SQL tienen contratos de columnas y comparación del resultado completo; algunos planes
EXPLAIN varían según SQLite y se interpretan en lugar de exigir un texto idéntico.

## Qué es obligatorio y qué es voluntario (revisión pedagógica v6)

Cada guía diaria separa la **teoría NÚCLEO** (sección A, antes de cualquier ejercicio), la **práctica BASE obligatoria** (sección C, agrupada por competencia y dificultad, con SQL de recuperación frecuente) y el **REFUERZO voluntario** (sección D: ejercicios diferentes de los obligatorios y sobre contenidos ya enseñados, sin teoría nueva). Avanzas por puertas de competencia, no por fecha: las fechas son objetivos. Lee [Competencias y puertas](01_PLAN_DIARIO/COMPETENCIAS.md), [Hitos y recuperación](01_PLAN_DIARIO/HITOS_Y_RECUPERACION.md) y la [carga estimada](01_PLAN_DIARIO/CARGA_ESTIMADA.md) (estimación, no medición).

## Lecciones, criterio analítico y hitos de comprensión

Las 100 lecciones de `02_TEORIA` tienen una sola clase: **NÚCLEO** (87, programadas en la ruta BASE), **COMPLEMENTARIA** (10, material de consulta) o **EMPLEO** (3, dentro del bloque de empleo). No existe una ruta EXTENDIDA. La clasificación y el día de cada lección están en [`RUTAS.md`](01_PLAN_DIARIO/RUTAS.md).

Además de calcular, debes **entender y poder decidir**: cada jornada de martes a viernes incluye una actividad de criterio analítico (`03_EJERCICIOS/Analitico/AN01…AN18`: definir el problema, elegir el KPI, comparar, separar hechos de hipótesis, reconocer datos insuficientes y recomendar) y cada puerta exige un hito de comprensión (`03_EJERCICIOS/Comprension/H01…H08`: explicar, predecir, resolver una variante nueva y justificar). Un OK del corrector no basta.

Antes del ETL de la distribuidora hay un puente: `19_Puente_Python_a_ETL.md`, tres ejercicios de depuración (`03_EJERCICIOS/Depuracion`) y un mini-ETL de 24 filas (`03_EJERCICIOS/Puente`).

```powershell
.\.venv\Scripts\python.exe herramientas/corregir_mini_etl.py ME01 mi_trabajo/mini_etl/mini_etl.py
.\.venv\Scripts\python.exe herramientas/corregir_depuracion.py DB01 mi_trabajo/depuracion/DB01.py
```

## Qué carpeta abrir

| Carpeta | Uso |
|---|---|
|01_PLAN_DIARIO|Plan con casillas, 42 guías diarias (secciones A–H: lecciones NÚCLEO, práctica BASE, REFUERZO, REDUCIDO, MÍNIMO y empleo), puertas de competencia, [lecciones y rutas](01_PLAN_DIARIO/RUTAS.md), carga estimada y calendario CSV/JSON|
|02_TEORIA|19 capítulos con 100 lecciones (cada una con ejemplos ejecutados, errores comunes y micropráctica), el puente a ETL (cap. 19), [índice](02_TEORIA/INDICE.md), glosario, fuentes y complemento UAGRM|
|03_EJERCICIOS|99 SQL (incluye SQ01–SQ17 y KP01), 39 Python, 5 de mini-ETL, 4 de depuración, 13 de estadística, 7 notebooks, 24 casos (incluye Excel, Power Query, Power BI, modelado y Git), 6 exámenes, 18 actividades de criterio analítico (`Analitico/`) y 8 hitos de comprensión (`Comprension/`)|
|04_DATASETS|Datos v 3 reutilizados, base comercial ampliada, mini-ETL de 24 filas, caso de transferencia y `mini_base/` (datos inventados solo para los ejemplos de la teoría)|
|05_PROYECTOS|Estructuras de SQL/ETL/BI, plantilla README, CSV de modelo, M y DAX|
|06_ENTREVISTAS|24 preguntas y 6 simulacros con rúbrica|
|07_LINKEDIN_EMPLEO|CV/perfil, seguimiento y borradores de publicaciones (se publica solo un entregable terminado y verificado)|
|08_SOLUCIONES|Referencias y controles separados; no abrir antes del intento|
|09_EVALUACION_FINAL|Datos nuevos, enunciado, registro y rúbrica sin IA|
|10_VALIDACION|Informe, evidencias JSON, correcciones y originales conservados|
|herramientas|Ejecutores, correctores, validadores y pruebas reproducibles|

Las ampliaciones voluntarias no acumulan deuda. Los ejercicios obligatorios conservan su condición de
**OBLIGATORIO PENDIENTE** si interrumpes una sesión: retómalos antes de la actividad o evaluación que los necesita.
Si un hito falla, recupera esa base antes de continuar. Conserva los bloques de empleo y cierre.
No avances a un ETL completo si todavía no puedes explicar una función o un JOIN.

## Proyectos y pruebas

Tu SQL utiliza `04_DATASETS/comercial.db`; la base original permanece intacta en `04_DATASETS/distribuidora`.
El ETL original se reutiliza con rutas adaptadas y comprobaciones más claras; no se reemplazaron los datos.
La transferencia C06 se resuelve con código propio durante la semana 6 y la evaluación final (contrato distinto) en un bloque posterior. La referencia de la evaluación final no está en este paquete (custodia aparte); el validador compara con huellas. Los correctores comprueban filas, claves y agrupaciones, no solo totales, y el corrector numérico no prueba por sí solo la autonomía.

```powershell
.\.venv\Scripts\python.exe herramientas/validar_etl_distribuidora.py mi_trabajo/etl/etl_salida.db
.\.venv\Scripts\python.exe 05_PROYECTOS/powerbi/exportar_modelo.py
.\.venv\Scripts\python.exe herramientas/validar_final.py mi_trabajo/transferencia/salida --transferencia
.\.venv\Scripts\python.exe herramientas/validar_final.py mi_trabajo/final/salida
```

Para comprobar que los enunciados son específicos (sin plantillas, pistas repetidas ni resultados publicados) y que los exámenes evalúan lo preparado: `python herramientas/auditar_enunciados.py`.
Para comprobar que ninguna herramienta deja abierta una conexión SQLite (error `WinError 32` en Windows): `python herramientas/prueba_sqlite_cierre.py`.
Para comprobar la teoría (ejecuta los ejemplos SQL y Python de las lecciones y compara con la salida mostrada; revisa enlaces, tiempos, términos, glosario y que ningún ejemplo coincida con una solución): `python herramientas/verificar_teoria.py`.
Para comprobar el diseño pedagógico v6 (42 jornadas, minutos, lecciones y prerrequisitos, guías generadas, ejercicios nuevos, actividades acreditadas y archivos protegidos): `python herramientas/verificar_diseno_v6.py diseno`, `... guias --dias 1-42`, `... ejercicios --todos`, `... progreso` y `... proteccion`. Para regenerar las guías y los documentos derivados sin cambios (idempotencia): `python herramientas/aplicar_nucleo.py --todos --comprobar`.
Para comprobar que los validadores rechazan resultados incorrectos conocidos (alteraciones en copias temporales): `python herramientas/pruebas_validadores.py` (la evaluación final solo se prueba si indicas `--custodia`).
Los ejercicios nuevos (SQ, KP, RP, PD, PT, RD, RS, REL1, PE01) se corrigen con `python herramientas/corregir_nuevos.py ID archivo`; el repositorio de portafolio con `herramientas/verificar_portafolio.py` y los diseños de modelo con `herramientas/validar_modelo.py`.
`herramientas/verificar_paquete.py`, `verificar_etapa2.py` y `pruebas_mutaciones_ruta.py` pertenecen al diseño anterior (calendario de 15 h semanales) y ya no describen este plan: no los uses como control de la ruta.

## Power BI y Excel

Abre `05_PROYECTOS/powerbi/MODELO.md`, importa los CSV incluidos y crea relaciones/medidas en Desktop.
No se entrega un PBIX simulado: M/DAX son archivos de referencia que requieren aplicación y prueba manual.
El informe identifica esta limitación. Los CSV/modelo y sus totales sí se probaron mediante Python/SQL.
Excel usa los casos EX01–EX04 y RE01 con importación, fórmulas y tablas dinámicas propias; no hay pruebas de interfaz
de Excel realizadas aquí. Los ejemplos de fórmulas contemplan tu separador de argumentos y la configuración local.

## Notion, GitHub y registro

Notion: importa el Markdown del plan para las casillas; sus enlaces relativos pueden necesitar ajuste después
de importar. VS Code/GitHub conservan esos enlaces dentro del árbol de carpetas. No se probó la importación a Notion.
Guarda código propio, README, resultados y límites en tus repositorios. No subas datos privados de Cruzimex,
credenciales ni la solución de referencia como si la hubieras construido. Revisa `git status` antes de cada envío.
El CV y GitHub se preparan desde D01 y la primera postulación real es en D11 (22 de octubre); los borradores de LinkedIn se publican solo cuando el ejercicio se completó de verdad.
El paquete no envía postulaciones, mensajes ni publicaciones automáticamente.

## Evidencia y límites

Consulta [INFORME_VALIDACION.md](10_VALIDACION/INFORME_VALIDACION.md). Distingue código ejecutado,
datos/formato comprobados y tareas manuales pendientes. No se declara adquisición de habilidad ni ejecución
de Desktop por haber producido los archivos. El historial completo del otro chat no se recuperó directamente;
se utilizaron documentos de contexto y planes v 3/v 4 accesibles y tus instrucciones actuales.
