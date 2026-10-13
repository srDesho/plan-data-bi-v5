# Informe de cambios · rama `fix/auditoria-v5`

Fecha: 13 de octubre de 2026. **Nada está confirmado (sin commits), nada se subió (sin push) y `main` no se tocó.**
Los cambios están en el árbol de trabajo de la rama `fix/auditoria-v5`, listos para revisarlos con `git diff main`.
Este informe está sin rastrear (igual que `AUDITORIA_EXHAUSTIVA_PLAN_V5.md`); bórralo o inclúyelo según decidas.

## 1. Cumplimiento de tus condiciones

| # | Condición | Estado |
|---|---|---|
| 1 | Rama `fix/auditoria-v5`, sin push, sin tocar la principal | Cumplido. `git branch --show-current` = `fix/auditoria-v5`; `git log` solo muestra el commit inicial; sin commits nuevos. |
| 2 | Conservar originales, datasets, soluciones y `mi_trabajo` | Cumplido. `git status` no marca cambios en `mi_trabajo`, `10_VALIDACION`, datasets originales ni ejercicios SQL/Python. En `08_SOLUCIONES` solo se corrigieron dos referencias de ETL (cierre de conexión) y se añadieron archivos nuevos. |
| 3 | J-1 y J-2: redistribuir carga, marcar OBLIGATORIO / REFUERZO / OPCIONAL, competencias | Hecho en las 34 jornadas activas de D03 a D41 (sección 3). |
| 4 | Mantener SQL, Python, Pandas, ETL, KPIs, estadística, Excel y Power BI | Mantenidos. Excel y Power BI con alcance reducido (sección 3.3). Nada se eliminó; lo desplazado figura como REFUERZO u OPCIONAL. |
| 5 | Transición Python básico → mini-ETL → ETL completo | Hecho: capítulo 19, 3 ejercicios de depuración, mini-ETL de 4 ejercicios y correctores (sección 4). |
| 6 | J-5: conexiones SQLite abiertas en Windows con pruebas reproducibles | Hecho y probado (sección 5). |
| 7 | No tocar Día 1 y Día 2 | Cumplido: `D01` y `D02` sin cambios; sus ejercicios (S1, S10, P01, S2, S7, S9, P02, P03, C01) y los capítulos 01 y 07 no se modificaron. |
| 8 | No cambiar fechas ni prometer; hitos de competencia | Cumplido: fechas y minutos por día y semana idénticos (900 por semana). Las puertas están en `COMPETENCIAS.md` con la advertencia explícita de que no se promete terminar antes del 30 de noviembre. |
| 9 | Ejecutar pruebas después de los cambios | Ejecutadas (sección 6): 17 de 17 grupos correctos sobre una copia del árbol modificado. |
| 10 | Informe de cambios | Este documento. |

## 2. Resultado en una frase

Para las semanas 2–6, el estimado central de la parte **obligatoria** pasa de 1,6–2,1× lo planificado (cifras de la auditoría) a 1,04–1,12×. La semana 1 suma 639 de 650 min en D03–D06 (D01 y D02 no se tocan).
Es un reordenamiento de prioridades, no un milagro de velocidad: el REFUERZO y el OPCIONAL (incluidos PB04–PB06, EX02–EX03, ST03–ST07 y varias series SQL) quedan fuera de esa cifra.
La estimación sigue siendo un modelo con supuestos (error razonable de ±35 %), no una medición.

## 3. J-1 y J-2: redistribución, clasificación y puertas

### 3.1 Qué cambió y por qué

- Cada jornada D03–D41 (menos los domingos) tiene ahora las secciones **OBLIGATORIO** (con estimación), **REPASO**, **REFUERZO** y **OPCIONAL**, un **prerrequisito** («Antes de empezar»), un **«Haz solo»** para el modo REDUCIDO y, en 8 jornadas (D06, D13, D20, D22, D27, D30, D34 y D41), una **puerta de competencia**. Motivo: la auditoría mostró que «recorta ampliación» no tenía nada que recortar en los días con más carga.
- Los minutos de cada día y semana no cambian. Cambia **qué** se hace en cada día.
- La secuencia que más cambia es Pandas → mini-ETL → ETL guiado: el mini-ETL ocupa D18, D19 y D22; el ETL de la distribuidora se divide en 6 sesiones (D23–D26, D29–D30) en lugar de 4; el caso C06 pasa a 5 bloques (D36–D40) en lugar de 4; Excel y Power BI se mueven a D31–D33, después de la Puerta 5.
- Se desplazaron a REFUERZO u OPCIONAL, entre otros: P12, P14–P16, P18, P24–P28 (P24, P25 y P28 son la versión pequeña de etapas del ETL), C04, C05, ST03–ST07, PB04–PB06, EX02–EX03, varias de las series K, X y N. Ninguno se eliminó: la prueba «Núcleo, puertas y carga estimada coherentes» comprueba que todo ejercicio SQL, Python y de estadística del banco siga ubicado en algún día.
- Fuente de los datos: `01_PLAN_DIARIO/nucleo.json`. `herramientas/aplicar_nucleo.py` regenera guías, calendario y `CARGA_ESTIMADA.md` de forma idempotente (dos ejecuciones seguidas dan el mismo resultado) y nunca toca D01 ni D02.

### 3.2 Distribución por jornada

| Día | Fecha | Contenido | OBLIGATORIO | REFUERZO | OPCIONAL | Puerta |
|---|---|---|---|---|---|---|
| D03 | 10-14 | Listas, diccionarios y clientes únicos | S3, S5, S6, P04, P05 | S4 | C02 |  |
| D04 | 10-15 | Agrupación, bucles y media/mediana | G1, P06, ST01 | G2, G3 | — |  |
| D05 | 10-16 | Condiciones, funciones cortas y KPIs | G4, G5, G6, P07, P08 | — | C01 |  |
| D06 | 10-17 | Primer examen y cierre de fundamentos | G7, G8, examen S01 | — | S8 | P1 |
| D08 | 10-19 | Funciones y formatos: errores visibles | P09 | CL1, CL3, CL2 | — |  |
| D09 | 10-20 | Fechas, cantidades y primer JOIN | J1, J2, P10 | — | — |  |
| D10 | 10-21 | Ventas agrupadas y archivos CSV | J3, J4, P13 | P12, C04 | — |  |
| D11 | 10-22 | Ausencia, errores y catálogo por ruta | J5, J6, P11 | P14, P15 | — |  |
| D12 | 10-23 | Primer DataFrame y estadística del drop | P17, ST02, N01 | P16, E1, E2 | E3 |  |
| D13 | 10-24 | Examen de JOIN y conciliación | E4, E6, examen S02 | E5 | E7, E8 | P2 |
| D15 | 10-26 | Pandas y monto por línea | P19 | K2a, P18 | — |  |
| D16 | 10-27 | Ticket y agrupación en Pandas | K1, K3, P20 | K2b | — |  |
| D17 | 10-28 | Subconsultas y merge validado | P21, P22, N02 | K4 | — |  |
| D18 | 10-29 | Duplicados, perfilado y primer paso del mini-ETL | P23, ME01, N03 | K4, K5, K6, V1 | — |  |
| D19 | 10-30 | Mini-ETL (2): transformar con reglas y rechazos | ME02, V3 | P26, P27, ST03, N04 | — |  |
| D20 | 10-31 | Examen Pandas y SQL intermedio | V4, examen S03 | V5, V1 | X1, X2 | P3 |
| D22 | 11-02 | Mini-ETL (3): validar, cuadrar y cargar | ME03 | DB01, P29, P30, CL4, N8 | — | P4 |
| D23 | 11-03 | ETL guiado (1): contrato, Bronze y texto | ETL-1, DB01 | DB02, N8 | — |  |
| D24 | 11-04 | ETL guiado (2): fechas, cantidad y dinero | ETL-2, V2 | C05, DB02 | — |  |
| D25 | 11-05 | ETL guiado (3): claves, duplicados y vendedores | ETL-3, X7 | N7, X4, DB03 | X3, X5, X6 |  |
| D26 | 11-06 | ETL guiado (4): Silver, validación y rechazos | ETL-4, N1 | P28, X8, ST04 | N4 |  |
| D27 | 11-07 | Examen S04: mini-ETL y ETL hasta Silver | N2, examen S04 | N4, N8 | N10, N11 | P5a |
| D29 | 11-09 | ETL guiado (5): Gold | ETL-5 | P24, P25, N7 | ST05, N05 |  |
| D30 | 11-10 | ETL guiado (6): carga, repetición y cuadre SQL | ETL-6 | N9, N12 | ST06 | P5 |
| D31 | 11-11 | Excel: importar, tabla dinámica y cuadre | EX01 | N5, N6, EX02 | EX03 |  |
| D32 | 11-12 | Power BI (1): importar y relacionar | PB01, PB02 | N12, N14, PB04, N07 | N13, N15, N16 |  |
| D33 | 11-13 | Power BI (2): primeras medidas | PB03 | PB05, N6 | ST07 |  |
| D34 | 11-14 | Examen S05: ETL guiado completo y BI mínimo | N3, examen S05 | PB06, EX03 | N15 | P6 |
| D36 | 11-16 | Caso nuevo C06 (0): contrato y plan | C06-0 | ME04, N7, N06 | N9 |  |
| D37 | 11-17 | C06 (1): extraer, Bronze y perfil | C06-1 | N8 | — |  |
| D38 | 11-18 | C06 (2): Silver y rechazos | C06-2 | ST07 | — |  |
| D39 | 11-19 | C06 (3): Gold y cuadres | C06-3 | N5 | — |  |
| D40 | 11-20 | C06 (4): SQLite, repetición y README | C06-4 | C03, C01, J5 | N16 |  |
| D41 | 11-21 | Último examen y preparación del final | V4, examen S06 | N1 | — | P7 |

`D01` y `D02` no figuran porque no cambiaron. El REPASO (10 min de SQL ya hecho) está en cada guía. Los títulos nuevos están sincronizados en `PLAN_V5.md` y `calendario.json/csv`.

### 3.3 Excel y Power BI: alcance reducido, no eliminado

| Antes (v5) | Ahora | Motivo |
|---|---|---|
| PB01–PB06 y EX01–EX03 entre D29 y D34, junto con inferencia y modelo estrella | EX01 (D31: solo tabla dinámica y cuadre contra E4); PB01+PB02 (D32: importar y relacionar); PB03 (D33: tres medidas); comprobación mínima en S05 (D34). PB04–PB06 y EX02–EX03 son REFUERZO/OPCIONAL. | La auditoría estimó 2,0–2,4× en esa semana. El ETL es la ruta crítica y se declara qué parte de BI puede esperar. |

Límites: sigue sin existir un archivo PBIX, y no se ejecutó Power BI Desktop ni Excel al preparar este material. La medida DAX `Crecimiento` (hallazgo 5 de la auditoría) **no se modificó**: queda en PB04 (REFUERZO); verifícala en Desktop antes de usarla.

## 4. Puente Python → mini-ETL → ETL guiado

| Archivo | Motivo |
|---|---|
| `02_TEORIA/19_Puente_Python_a_ETL.md` | Capítulo nuevo con ejemplos ejecutables: leer un traceback, rechazar con `ValueError`, programa de cuatro funciones con cuadre, SQLite en Windows. Sus bloques de código se ejecutan en la prueba «Ejemplos Python de los apuntes». |
| `03_EJERCICIOS/Puente/` (ME01–ME04 e índice) | Mini-ETL guiado de 24 filas: extraer y perfilar, transformar con rechazos, validar/cargar/cuadrar, y modificar con una regla nueva. Cada enunciado trae tiempo objetivo y tiempo realista de primera vez. |
| `03_EJERCICIOS/Depuracion/` (DB01–DB03, índice y 3 scripts rotos) | Leer un error, un total que no cuadra por truncar y un JOIN que multiplica ventas. |
| `04_DATASETS/mini_etl/` | Datos sintéticos nuevos (raw, variante v2, catálogo y diccionario). No reutiliza datos del caso de transferencia ni del final. |
| `05_PROYECTOS/etl/plantilla_mini_etl.py` | Esqueleto con `NotImplementedError`, como la plantilla del ETL grande. |
| `herramientas/corregir_mini_etl.py`, `herramientas/corregir_depuracion.py` | Correctores nuevos. A diferencia de los existentes, indican **la clave y la columna** que fallan («clave T002, columna `tienda`: obtuviste X y se esperaba Y»), avisan cuando la conexión SQLite sigue abierta y no muestran la solución. |
| `08_SOLUCIONES/mini_etl_referencia.py`, `controles_mini_etl.json`, `depuracion_referencia.py` | Referencias y controles. El total de ventas de la referencia (28.265 centavos) lo comprobé a mano fila por fila. |
| `05_PROYECTOS/etl/README.md` | Columna «Jornada (objetivo)» por etapa y mención del mini-ETL previo. |
| `03_EJERCICIOS/Casos/C06.md`, `03_EJERCICIOS/CASOS.md` | C06 pasa de 240 a ≈ 450 min en cinco bloques (D36–D40), según la estimación. |
| `03_EJERCICIOS/EXAMENES/S03–S06.md` | Tareas y puntajes alineados con la nueva secuencia: S03 ya no pide P25; S04 es un hito (mini-ETL y ETL hasta Silver); S05 pasa a ETL guiado completo más BI mínimo; S06 aclara qué hacer si C06 no está terminado. En las líneas reescritas se corrigieron las palabras pegadas; las demás erratas del paquete no se tocaron. |

## 5. J-5: conexiones SQLite abiertas en Windows

**Causa:** `with sqlite3.connect(...) as con:` confirma la transacción pero no cierra la conexión; en Windows, `os.replace` o borrar un archivo abierto falla con `WinError 32`.
**Corrección:** `contextlib.closing(sqlite3.connect(...))` en las 8 llamadas originales del paquete (las herramientas nuevas ya nacen con `closing`).

| Archivo | Cambio |
|---|---|
| `08_SOLUCIONES/etl_nuevo_referencia.py` | `closing(...)` antes de `os.replace` (causa de las pruebas 5 y 6 fallidas). |
| `08_SOLUCIONES/etl_distribuidora.py` | `closing(...)` en la carga. |
| `herramientas/corregir_sql.py` | `closing(...)`. **Hallazgo adicional:** `consulta()` también dejaba bloqueado el archivo de la base de datos; la prueba nueva lo reproduce. |
| `herramientas/validar_final.py`, `validar_etl_distribuidora.py`, `comprobar_entorno.py` | `closing(...)` en la lectura. |
| `05_PROYECTOS/powerbi/exportar_modelo.py` | `closing(...)` al leer `comercial.db`. |
| `herramientas/verificar_paquete.py` | `closing(...)` en su prueba de datos y cuatro pruebas nuevas (sección 6). |
| `02_TEORIA/05_calidad_ETL.md` | Se enseña la regla (una frase y referencia al capítulo 19). |
| `herramientas/prueba_sqlite_cierre.py` (nuevo) | Prueba reproducible: (1) reproduce el `PermissionError` con el patrón malo y comprueba el bueno; (2) `corregir_sql.consulta`, el ETL de transferencia con su validador y el ETL de la distribuidora deben dejar el archivo renombrable y borrable; (3) revisión estática con `ast`: todo `sqlite3.connect` va dentro de `closing(...)`. |

**Control negativo:** el mismo script sobre el código original de `main` falla en 4 de 5 grupos con `WinError 32`; sobre la rama corregida pasa 5 de 5.
`10_VALIDACION/originales/07-etl_referencia.py` (archivo histórico) conserva el patrón original a propósito.

## 6. Pruebas ejecutadas

Todas sobre **copias** del árbol (`verificar_paquete.py` escribe sus evidencias en `10_VALIDACION`, y no quise sobrescribir las originales). Windows 11, Python 3.12.10 del `.venv`.

| Prueba | Resultado |
|---|---|
| `python herramientas/verificar_paquete.py` (copia del árbol modificado) | **17 de 17 grupos correctos, 0 fallos** (13 existentes + 4 nuevos: conexiones SQLite, mini-ETL, depuración, núcleo/puertas/carga) |
| El mismo script sobre el árbol original (copia, antes de los cambios) | 11 de 13 (fallaban las pruebas 5 y 6 por `WinError 32`) |
| `python herramientas/prueba_sqlite_cierre.py` sobre el árbol modificado | 5 de 5 |
| Idem sobre el código original de `main` | 1 de 5 (reproduce el error) |
| Correctores nuevos | ME01–ME04 y DB01–DB03 aprobados con la referencia. Rechazadas: unidades truncadas, tienda sin normalizar, conflicto de clave ignorado, regla nueva ausente, conexión SQLite abierta (detectable solo en Windows), plantilla sin resolver y los 3 scripts rotos |
| Idempotencia de `aplicar_nucleo.py` | Dos ejecuciones seguidas producen contenido idéntico |
| Humo en el árbol real: `comprobar_entorno.py`, `ejecutar_sql.py` | OK |
| D01, D02, `mi_trabajo`, `10_VALIDACION`, datasets y ejercicios SQL/Python originales | `git status` sin cambios |

**No ejecutado ni verificado:** Power BI Desktop y Excel; el notebook de la Clase 2 de la UAGRM; ningún estudiante real ha usado todavía los ejercicios nuevos, así que sus tiempos objetivo son estimaciones mías. Los correctores comprueban resultados, no autoría.
No ejecuté `verificar_paquete.py` en el árbol real a propósito: habría reescrito `10_VALIDACION/resultados_pruebas.json` y `evidencia_sql.json`.

## 7. Archivos modificados (`git status`)

**Modificados:** `01_PLAN_DIARIO/` (HITOS_Y_RECUPERACION, PLAN_V5, calendario.csv y .json, y 34 guías diarias), `02_TEORIA/05_calidad_ETL.md`, `03_EJERCICIOS/CASOS.md`, `Casos/C06.md`, `EXAMENES/S03` a `S06`, `05_PROYECTOS/etl/README.md`, `05_PROYECTOS/powerbi/exportar_modelo.py`, `08_SOLUCIONES/etl_distribuidora.py` y `etl_nuevo_referencia.py`, `README.md`, y en `herramientas/`: comprobar_entorno, corregir_sql, crear_espacio, validar_etl_distribuidora, validar_final, verificar_paquete.
**Nuevos:** `01_PLAN_DIARIO/` (COMPETENCIAS, CARGA_ESTIMADA, nucleo.json), `02_TEORIA/19_Puente_Python_a_ETL.md`, `03_EJERCICIOS/Puente/`, `03_EJERCICIOS/Depuracion/`, `04_DATASETS/mini_etl/`, `05_PROYECTOS/etl/plantilla_mini_etl.py`, `08_SOLUCIONES/` (mini_etl_referencia.py, controles_mini_etl.json, depuracion_referencia.py), `herramientas/` (aplicar_nucleo, corregir_mini_etl, corregir_depuracion, prueba_sqlite_cierre) y los dos informes.
`crear_espacio.py` ahora también crea `mi_trabajo/mini_etl` y `mi_trabajo/depuracion` (sin sobrescribir nada; no lo ejecuté sobre tu carpeta).
`README.md`: solo se añadió la sección «Obligatorio, refuerzo y opcional», se actualizaron cuatro filas de la tabla de carpetas y una línea de pruebas; **la sección «Día 1» no cambió**.

## 8. Limitaciones y decisiones que debes revisar

1. **No implementé** J-3 (reemplazar la evaluación final), J-4 (sacar las claves de respuesta del final), J-6 (mejorar los correctores existentes) ni el resto de la lista, porque no los autorizaste. Los correctores nuevos sí dan retroalimentación específica.
2. **`10_VALIDACION` está desactualizada:** `MANIFIESTO_SHA256.json`, `CIERRE_PAQUETE.json`, `INFORME_VALIDACION.md` y `resultados_pruebas.json` describen el paquete v5 original. No los regeneré para no mezclar evidencia antigua y nueva. Conviene regenerar el manifiesto cuando confirmemos los cambios.
3. **El mini-ETL y C06 comparten tipos de defecto** (espacios, formatos de fecha, `Bs` y coma, cantidades fraccionarias, duplicados, claves en conflicto). Es intencional (andamiaje), pero el mini-ETL no es «un problema nuevo»: la transferencia real sigue siendo C06 y la evaluación final.
4. **La carga estimada es un modelo.** Los multiplicadores son los de la auditoría; los tiempos de las tareas de proyecto (ETL-1…6, C06-0…4, ME01–ME03, PB y EX01) los fijé yo. La reducción de 1,6–2,1× a ≈ 1,1× proviene de **mover** ejercicios a REFUERZO/OPCIONAL y de reducir el alcance de BI y Excel, no de suponer que aprenderás más rápido. Registra tus minutos reales y corrige `CARGA_ESTIMADA.md`.
5. **Algunas jornadas siguen ajustadas** (razón ≥ 1,17 en D12, D13, D23, D27 y D34): para esas, usa el modo REDUCIDO que la guía define explícitamente.
6. **Contenido que pierde protagonismo** (decidimos juntos si algo debe volver): ST03–ST07 pasan a REFUERZO/OPCIONAL (sigue obligatorio ST01 y ST02, y las medidas de dispersión se retoman en C03); P26 y P27 (ABC y atípicos en Pandas) pasan a REFUERZO, mientras V3 y V4 (SQL) siguen obligatorios; de Excel solo EX01 es obligatorio; Power BI queda en tres medidas.
7. **Los exámenes S04 y S05 cambiaron de sentido** (hito de ETL; ETL guiado más BI mínimo). Si prefieres conservar los originales como material y crear versiones aparte, se puede.
8. **Saltos de línea:** Git avisa «LF will be replaced by CRLF» en los archivos editados (configuración `core.autocrlf` de tu equipo). No afecta al contenido; conviene revisar `.gitattributes` antes del commit.
9. **Si ya estudiaste D01–D02:** nada cambia para ti. D03 en adelante tiene la nueva forma; en D03–D06 el cambio es de clasificación: C01 (repetido) y C02 pasan a OPCIONAL, y ST01 pasa a obligatorio en D04.

## 9. Cómo revisar

```powershell
git diff --stat main                                       # resumen
git diff main -- 01_PLAN_DIARIO/dias/D19_2026-10-30.md     # ejemplo de una guía
.\.venv\Scripts\python.exe herramientas/aplicar_nucleo.py --comprobar   # estimación por día
.\.venv\Scripts\python.exe herramientas/prueba_sqlite_cierre.py          # prueba J-5 en tu equipo
```

Para deshacer todo: `git checkout main`, borrar la rama y quitar los archivos nuevos sin rastrear (revisa antes con `git clean -n`).
No haré commit, merge ni push hasta que lo autorices.
