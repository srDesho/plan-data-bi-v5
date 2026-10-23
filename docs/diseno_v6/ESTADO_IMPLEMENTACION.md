# Estado de la implementación (punto de recuperación)

Última actualización: 2026-10-18 · **Fase 3 terminada, Fase 5 ejecutada y ajustes finales de cierre aplicados** (aprobación provisional del usuario). Las 42 jornadas, los 44 ejercicios nuevos y los documentos derivados están generados y verificados. Total BASE: **9.452 min = 157 h 32 min**. Pendiente: preparar el commit final (propuesta; sin commits ni push hasta nueva orden). Las enmiendas de cierre están en [ENMIENDAS_FASE3.md](ENMIENDAS_FASE3.md).
Reglas vigentes: sin commits ni push; rama `correccion-pedagogica-definitiva`; no tocar `mi_trabajo/`, exámenes S01–S06 (enunciados ni contratos), hitos, proyectos C06, datasets ni evaluación final; las 34 realizaciones y las 42 fechas se conservan; respaldo externo en `D:\Course Python\Claude\GPT\Respaldos_Plan_Data_BI_v5\8168909_arbol_codex_sin_commit_20261017_2101` (no sobrescribir).

## Tablero

| Bloque | Jornadas | Estado |
|---|---|---|
| 1 | D01–D05 | terminado y verificado |
| 2 | D06–D14 | terminado y verificado |
| 3 | D15–D21 | terminado y verificado |
| 4 | D22–D28 | terminado y verificado |
| 5 | D29–D35 | terminado y verificado |
| 6 | D36–D42 | terminado y verificado |
| Auditoría integral | D01–D42 | **ejecutada** (resultados abajo) |

## Cómo verificar todo (desde la raíz, con `.venv\Scripts\python.exe`)

| Comando | Resultado del 2026-10-18 |
|---|---|
| `herramientas/aplicar_nucleo.py --todos --comprobar` | 0 cambios (42 guías + calendario, CARGA_ESTIMADA, RUTAS, COMPETENCIAS, HITOS, PLAN_V5, índices de capítulo y mapa UAGRM idempotentes) |
| `herramientas/verificar_diseno_v6.py diseno` | 1169 pruebas, 0 fallos, 1 aviso (D39: sesión de 195 min, dentro del máximo de 215 pero sobre 185) |
| `herramientas/verificar_diseno_v6.py guias --dias 1-42` | 1060 pruebas, 0 fallos |
| `herramientas/verificar_diseno_v6.py ejercicios --todos` | 44/44 enunciados, 710 pruebas, 0 fallos (formato, pistas, controles, contratos, referencias, correctores citados y lecciones citadas ya enseñadas) |
| `herramientas/verificar_diseno_v6.py correctores` | 115 correctores ejecutados contra su referencia, 0 fallos |
| `herramientas/verificar_diseno_v6.py progreso` | 34 casillas `[x]`, 0 fallos |
| `herramientas/verificar_diseno_v6.py proteccion` | 400 archivos inmutables, 0 cambiados, 0 ausentes; 1 excepción autorizada aplicada (`09_EVALUACION_FINAL/ENUNCIADO.md`, líneas 5 y 7) |
| `herramientas/pruebas_mutaciones_v6.py todo` | 0 mutantes aceptados indebidamente: 110 mutantes rechazados (94 de correctores y 16 de guías/progreso) más una matriz PE01 de 16 casos con expectativa explícita (incluye soluciones válidas distintas que deben aprobarse) |
| `herramientas/verificar_teoria.py`, `auditar_enunciados.py` (ahora valida la duración vigente, no «90 horas»), `prueba_sqlite_cierre.py`, `comprobar_entorno.py`, `pruebas_validadores.py` | OK (la evaluación final se omite por custodia) |
| `herramientas/regenerar_manifiesto.py --comprobar` | «Manifiesto vigente» (725 archivos) en el momento del cierre; repetir `regenerar_manifiesto.py` si se modifica cualquier archivo |

## Herramientas

Vigentes: `aplicar_nucleo.py` (+ `derivados_v6.py`), `verificar_diseno_v6.py` (subcomandos `diseno`, `guias`, `ejercicios`, `correctores`, `progreso`, `proteccion`), `pruebas_mutaciones_v6.py`, `corregir_nuevos.py` (+ `contratos_v6.py`), `verificar_portafolio.py`, `validar_modelo.py`, `anclas_teoria_v6.py` y `construir_fuentes_v6.py` (arranque único; **no volver a ejecutar**, pisaría `nucleo.json`/`lecciones.json`).
Obsoletas (pertenecen al diseño anterior de 15 h semanales y no se ejecutan): `verificar_etapa2.py`, `pruebas_mutaciones_ruta.py`, `verificar_paquete.py`, y las del intento no aprobado de Codex `inventariar_pedagogia.py`, `pruebas_correccion_pedagogica.py`, `ruta_pedagogica.py`, `verificar_integridad_pedagogica.py`. `docs/auditorias/` es material de Codex sin aprobar y describe una muestra anterior; no se modificó.

## Archivos creados o modificados en la Fase 3

- **Fuentes y generador:** `01_PLAN_DIARIO/nucleo.json`, `lecciones.json` (v2), `progreso_acreditado.json` (nuevo); `herramientas/aplicar_nucleo.py` (reescrito), `derivados_v6.py`, `construir_fuentes_v6.py`, `verificar_diseno_v6.py`, `pruebas_mutaciones_v6.py`, `auditar_enunciados.py` (parche para el esquema v2).
- **Guías y derivados:** `01_PLAN_DIARIO/dias/D01…D42`, `calendario.csv/json`, `CARGA_ESTIMADA.md`, `RUTAS.md`, `COMPETENCIAS.md`, `HITOS_Y_RECUPERACION.md`, `PLAN_V5.md`; columna «Tipo» de los índices de capítulo `02_TEORIA/NN_*.md`; mapa de `02_TEORIA/UAGRM/LEEME.md`; `02_TEORIA/INDICE.md`; `README.md`.
- **Evaluación final (excepción autorizada):** `09_EVALUACION_FINAL/ENUNCIADO.md`, solo líneas 5 y 7 (duración informativa); ver [ENMIENDAS_FASE3.md](ENMIENDAS_FASE3.md).
- **Teoría:** anclas `#micropractica` (70 lecciones) y `#seccion-inicial` en 14.5; referencias de día corregidas en 11.1, 11.2, 11.3, 14.1; 12.8 declara como complementarias 12.6 y 12.7 (ya no las exige como prerrequisito).
- **Ejercicios nuevos (44):** SQL `SQ01–SQ17`, `KP01`; Python `RP01–RP05`, `PD01`, `RD01`, `RD02`, `PT01`; estadística `RS01–RS06`; ETL `REL1`; depuración `PE01` (+ `PE01_roto.py`, `PE01_ventas.csv`); casos `GIT01`, `EX04`, `RE01`, `PQ01`, `RQ01`, `PB07`, `RB01`, `MD01`, `RM01`; índices `INDICE.md`/`CONTRATOS.md`/`CASOS.md` ampliados.
- **Correctores y soluciones nuevas:** `herramientas/corregir_nuevos.py`, `contratos_v6.py`, `verificar_portafolio.py`, `validar_modelo.py`; `08_SOLUCIONES/controles_sql_v6.json`, `sql/SQ01–SQ17.sql`, `sql/KP01.sql`, `python_referencia_v6.py`, `pruebas_PT01_referencia.py`, `depuracion_PE01_referencia.py`, `mini_etl_rel1_referencia.py`, `modelo_MD01_referencia.md`, `modelo_RM01_referencia.md`, `controles_manuales_v6.md`.
- **Especificación:** `docs/diseno_v6/*` (solo este estado se actualiza durante la implementación).
- Ningún archivo de `mi_trabajo/`, de los exámenes, proyectos, datasets, hitos, correctores o soluciones originales ni de `09_EVALUACION_FINAL` se modificó.

## Cambios de esta sesión (después del Bloque 5)

- D36–D42 y sus ejercicios (`SQ14–SQ17`, `PE01`, `RS04–RS06`) generados y verificados.
- **PE01:** el mutante «sin validate ni control categoría» que se aceptaba era en realidad una solución válida (quitaba `validate` pero conservaba el `assert` de categoría, que también detiene la función). Se reprodujo, se rediseñó la matriz de mutación con expectativa explícita (aceptar/rechazar) y se endureció el corrector: ahora exige **al menos dos controles de cuadre** (`assert` o `raise`) dentro de `resumen`, además de las pruebas con catálogo repetido, zona vacía y producto desconocido. Controles tautológicos (`assert True`) con el defecto presente siguen rechazados por el comportamiento.
- **Inferencia estadística:** RS06 pedía el `d` de Cohen (lección complementaria 12.7, no enseñada en la ruta); se sustituyó por la diferencia relativa en % (`dif_relativa_pct`) y se remite a 12.8. El verificador de ejercicios ahora comprueba que toda lección citada en un enunciado esté enseñada a más tardar el día del ejercicio (en REFUERZO, ya leída completa). 12.5 pasa a leerse antes de 12.8 (el generador ordena las lecciones de un mismo capítulo por número).
- Documentos derivados regenerados con las cifras reales (156 h 32 min BASE, 25 jornadas sobre su máximo por más de 4 min, sesiones retomables) y sin EXTENDIDA/15 h semanales; puerta P7 ya no dice «fuera de las 90 horas».
- `contratos_v6.py` abría SQLite sin `closing` (lo detectó `prueba_sqlite_cierre.py`); corregido.

## Ajustes de cierre (aprobación provisional, 2026-10-18)

1. **RS04 y RS05 pasan a BASE** (D37 y D38): son la única práctica autónoma con corrector de error estándar/IC, `H0`/`H1` y p-valor por permutación; ST05 y ST07 cubren Welch, supuestos e interpretación. D37 330 min, D38 335 min, total 9.452 min (157 h 32 min), promedio martes–viernes 310 min. RS06 sigue como REFUERZO. Derivados regenerados.
2. **Evaluación final:** sustitución textual mínima de «90 horas» por «157 h 32 min» en las líneas 5 y 7 de `ENUNCIADO.md`; excepción registrada en `EXCEPCIONES_AUTORIZADAS` del verificador (solo vale el SHA-256 autorizado).
3. **SQ13 a** se verifica además con filas de prueba añadidas en memoria (`LTRIM`/`RTRIM` rechazados). **SQ09 c**: `NULLIF` no cambia el resultado en SQLite (dividir entre 0 da NULL), por eso el corrector exige su uso por texto; no se afirma que se detecte por comportamiento.
4. Cierre técnico: verificaciones repetidas (ver tabla), 34 actividades acreditadas conservadas, 42 fechas y exámenes intactos, enlaces e idempotencia correctos.

## Desviaciones respecto a la especificación

- RS04 y RS05 son BASE (ver «Ajustes de cierre»).
- PD01: firma `filtrar_entregas(pedidos, clientes, ruta, mes)` (la ruta vive en `clientes`).
- SQ06 b: «pedidos entregados con al menos un producto de Bebidas» para que `COUNT(DISTINCT)` sea necesario (mismo contrato 5×2).
- SQ08: se añade el apartado d (total corregido) para que la corrección del error sea verificable.
- REL1: se agregan dos filas de prueba (T027, T028) para observar la regla «monto > Bs 5.000 → monto».
- RS06: sin d de Cohen (ver arriba). Los ejercicios de estadística nuevos se corrigen con funciones (`corregir_nuevos.py`) y una rúbrica de decisión en el enunciado, no con un JSON como ST01–ST07.
- KP01: se añade el apartado c (marzo→abril, base 0) porque con los datos reales no existe base 0 en agosto→septiembre.
- Objetivo de D08 sin «retomar SQL básico» (esa jornada no tiene SQL de recuperación); texto de carga de lunes que superan 150 min corregido.

## Advertencias y limitaciones conocidas

1. **Carga:** 9.452 min BASE (157 h 32 min); promedio martes–viernes 310 min; 25 jornadas superan su máximo y se dividen en sesiones retomables (la mayor, D39-S1, 195 min). Es una excepción aceptada del diseño, no una promesa de 240 min diarios.
2. **Ejercicios sin corrector automático:** Excel, Power Query, Power BI/DAX, GIT01 (tiene lista de verificación) y la parte interpretativa de RS/KP/SQ se evalúan con rúbrica y cifras de `08_SOLUCIONES/controles_manuales_v6.md`; este paquete no ejecuta esas aplicaciones.
3. **Comprobaciones por texto:** quitar `NULLIF` en SQ09 c es indistinguible por resultado en SQLite (dividir entre 0 devuelve NULL); el corrector lo exige por texto. `LTRIM`/`RTRIM` en SQ13 a sí se detectan con las filas de prueba en memoria.
4. **Estadística inferencial:** BASE = RS04 (D37), RS05 (D38), ST05 (D39) y ST07 (D40) más las microprácticas; RS06 es voluntario. No hay práctica BASE de chi-cuadrado ni tamaño del efecto (12.6–12.7 son complementarias).
5. **`09_EVALUACION_FINAL/ENUNCIADO.md`** es el único archivo protegido modificado, con autorización expresa y alcance de dos líneas informativas.
6. Los complementos `docs/auditorias/` y las herramientas obsoletas quedan como están.
7. Las pruebas de mutación de guías modifican temporalmente una guía y la restauran byte a byte; si se interrumpen, ejecutar `aplicar_nucleo.py --todos` restaura el estado generado (las casillas `[x]` se conservan).

## Cómo continuar si se interrumpe

1. Leer este archivo y ejecutar los comandos de la tabla «Cómo verificar todo».
2. Si algún `--comprobar` marca cambios, ejecutar `aplicar_nucleo.py --todos` y revisar `git diff` de lo que cambió.
3. Antes de cualquier commit, esperar la aprobación del usuario: la propuesta de commits queda para después de la aprobación de la fase. No hacer commit ni push.
4. Si se modifica este archivo o cualquier otro del paquete, regenerar el manifiesto: `herramientas/regenerar_manifiesto.py`.
