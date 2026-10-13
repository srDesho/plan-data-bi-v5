# Informe · corrección integral de consistencia pedagógica (rama `fix/auditoria-v5`)

Fecha: 13 de octubre de 2026. **Sin commits, sin merge, sin push; `main` intacta.** Este informe complementa `INFORME_CAMBIOS_AUDITORIA_V5.md` (primera fase). No se tocó `mi_trabajo`: solo lo leí en modo lectura para comprobar tu `S1.sql` y tu `S10.sql` (ver sección 8).

## 1. El defecto, medido

Comprobé el hallazgo de la revisión independiente sobre la rama `main`:

| Medición en los 72 ejercicios SQL ordinarios de `main` | Resultado |
|---|---|
| Misma frase «Caso laboral: el gerente requiere este resultado…» | **72 de 72** |
| Misma primera pista («Identifica la tabla y la granularidad antes de escribir SELECT») | **72 de 72** |
| Segunda pista sobre WHERE/HAVING (idéntica) | **18** |
| Segunda pista sobre JOIN y pedidos distintos (idéntica) | **54** |
| Enunciados que listan las columnas pedidas | **0** (solo «N filas y M columnas»; había que ir a `CONTRATOS.md`) |

Causa de tu bloqueo con S1: el enunciado decía «Resultado de referencia: 10 filas y 6 columnas» sin nombrarlas, sin decir qué son «primeras diez» y sin ordenar, y las pistas hablaban de WHERE/HAVING aunque S1 no tiene ni uno. Tu `S1.sql` actual tiene una sola columna (`cliente_id`): el corrector la rechaza con «Cantidad u orden de columnas distinto del contrato», exactamente el error que el enunciado antiguo producía.

Hallazgos adicionales de la auditoría de enunciados: **información que solo estaba en el corrector** (redondeos a 2 o 1 decimales, etiquetas exactas como «Pequeño» con tilde, convención del ABC, nombres de tabla y columnas del mini-ETL y de C06, `ValueError` en P09), **respuestas publicadas** (ST01–ST03 y ST06 traían las cifras de control en los criterios; la teoría traía el resultado de V4 y de G1/G3; los ejemplos de teoría reproducían J1 y J5), **funciones usadas sin enseñarse** (`strftime`, `CASE`, `TRIM`, `UPPER`, `UNION ALL`, vistas temporales) y **exámenes que evaluaban algo no preparado** (S02 pedía C04, que era REFUERZO; S03 pedía P25 y `RANK`).

## 2. Archivos modificados y nuevos

`git status` (sin contar tus archivos en `mi_trabajo`): unos 200 archivos modificados y 22 nuevos, entre ellos 34 guías diarias, 83 archivos de `03_EJERCICIOS/SQL` (81 enunciados, `INDICE.md` y `CONTRATOS.md`) y 31 de `03_EJERCICIOS/Python` (30 enunciados e `INDICE.md`); el resto se resume a continuación.

| Grupo | Archivos | Motivo |
|---|---|---|
| Enunciados SQL | `03_EJERCICIOS/SQL/` — 81 enunciados reescritos uno a uno, `INDICE.md`, `CONTRATOS.md` | Defecto principal (sección 3). |
| Referencias y controles SQL | `08_SOLUCIONES/sql/`: 25 referencias modificadas (22 con `ORDER BY` coherente con el enunciado, alias en N5 y ES3C, y contenido nuevo en ES1B y ES3C); `controles_sql.json` regenerado | El enunciado pide un orden reproducible; solo cambian resultados donde se indica (sección 4). |
| Python | `03_EJERCICIOS/Python/`: 30 enunciados + `INDICE.md`; `herramientas/contratos_python.py` (caso extra en P05) | Firma, entradas, salidas, reglas, errores, ejemplos verificados contra la referencia, tres pistas y tiempos. P05 aprobaba un `set` sin ordenar por casualidad. |
| Estadística | `03_EJERCICIOS/Estadistica/ST01–ST07` | Se quitaron las cifras de control, se definieron entregables y método, tres pistas propias. |
| Casos, Excel y Power BI | `03_EJERCICIOS/Casos/` (C01–C06, EX01–EX03, PB01–PB06), `CASOS.md` (ahora índice) | Situación, entregables, definiciones, pistas propias, criterios propios; PB03 alineado con la jornada reducida; C06 con su contrato de salida. |
| Puente y depuración | `03_EJERCICIOS/Puente/ME03.md`, `ME01–ME04` (tiempos), `03_EJERCICIOS/Depuracion/DB01–DB03` (3 pistas, criterios) | Tiempos de primera vez coherentes con la estimación; columnas de Gold del mini-ETL declaradas. |
| Notebooks | `03_EJERCICIOS/Notebooks/N01–N07` | Ejemplos guiados específicos; N01 y N03 ya no dependen de ejercicios de REFUERZO. |
| Exámenes | `03_EJERCICIOS/EXAMENES/S01–S06` | Tareas alineadas con lo preparado; erratas corregidas en las líneas editadas. |
| Teoría y datos | `02_TEORIA/02_SQL_agregados.md` (sección de funciones nueva), `03_SQL_joins.md`, `04_SQL_CTE_ventanas.md`, `04_DATASETS/DICCIONARIO.md` | Prerrequisitos faltantes, ejemplos que copiaban ejercicios, respuestas publicadas, nota de calidad de datos. |
| Plan | `01_PLAN_DIARIO/` (34 guías, `PLAN_V5.md`, `COMPETENCIAS.md`, `HITOS_Y_RECUPERACION.md`, `CARGA_ESTIMADA.md`, `nucleo.json`, `calendario.csv/json`), `05_PROYECTOS/etl/README.md`, `README.md` | Reparto con tiempos honestos y sincronización. |
| Herramientas | Nuevas: `auditar_enunciados.py`, `regenerar_manifiesto.py`; modificadas: `aplicar_nucleo.py` (usa los tiempos declarados), `verificar_paquete.py` (+3 pruebas) | Pruebas automáticas (sección 7). |
| Validación | `10_VALIDACION/MANIFIESTO_SHA256.json`, `evidencia_sql.json`, `INFORME_VALIDACION.md` y `DECISIONES_Y_CORRECCIONES.md` (anexos), nuevos `COMPROBACION_81_SQL.md` y `resultados_pruebas_5_1.json` | Evidencia y manifiesto vigentes. |

`D01_2026-10-12.md` y `D02_2026-10-13.md` no se tocaron. Sus ejercicios vinculados (S1, S10, S2, S7, S9, P01–P03, C01) se reescribieron para que se entiendan, **sin cambiar objetivos ni subir la exigencia** (las mismas consultas, los mismos resultados).

## 3. Defectos pedagógicos corregidos

1. **81 enunciados SQL sin plantilla:** cada uno tiene situación propia, tablas con columnas y relaciones, qué representa una fila, columnas numeradas con su significado, reglas de filtro, orden, límite y redondeo, tres pistas distintas (orientación, concepto SQL, depuración), criterios propios y tiempo de primera vez. Ninguna pista incluye una consulta completa (comprobado por regla automática).
2. **Contratos como ayuda:** `CONTRATOS.md` se presenta como tabla de comprobación y la regenera una prueba desde los controles; el enunciado ya no depende de él.
3. **Información escondida en el corrector** ahora está en el enunciado: redondeos, etiquetas exactas, convención ABC (V4), nombres «tal como están guardados» (algunos traen espacios), salida de C06 (tablas, columnas, formatos, `auditoria.json`), tablas y columnas del mini-ETL, `ValueError` en P09.
4. **Orden reproducible:** donde el enunciado fija un orden o un «primeras N», la referencia lo declara (S1 usa `ORDER BY cliente_id`); el corrector sigue ignorando el orden salvo cuando decide qué filas entran.
5. **Prerrequisitos de teoría:** la sección «Funciones que usarás desde G4» del capítulo 02 enseña `ROUND`, `strftime`, `CASE`, `TRIM`, `UPPER`, `UNION ALL` y vistas temporales, con ejemplos que no repiten ejercicios y que se ejecutan en la prueba.
6. **Ejemplos que copiaban ejercicios** (J1 y J5 en el capítulo 03): sustituidos por casos con otras tablas.
7. **Respuestas publicadas retiradas:** cifras de control en ST01–ST03 y ST06, resultados de V4, G1 y G3 en la teoría; una prueba compara los controles contra todos los enunciados.
8. **Pistas repetidas:** Python (30), estadística (7), casos (15), depuración y mini-ETL tienen pistas propias; hay una regla que falla si dos ejercicios comparten la misma pista.
9. **Dependencias:** ningún ejercicio OBLIGATORIO exige leer teoría aún no asignada ni depende de «tu Pxx» que sea REFUERZO (ETL-4, ETL-5, ME03, N01 y N03 se corrigieron).
10. **Exámenes:** cada ejercicio mencionado en S01–S06 está preparado como OBLIGATORIO o REPASO antes de la fecha; ES1B no filtraba nada (ahora discrimina); ES3C evaluaba `RANK`, que ningún obligatorio practicaba (ahora usa porcentaje sobre el total con función de ventana, como V3).

## 4. Las seis inconsistencias que señalaste

| # | Inconsistencia | Resolución |
|---|---|---|
| 1 | S02 evalúa C04, que quedó como REFUERZO | S02 ya no menciona C04: pide conciliar por escrito «todas las líneas» frente a J2 y justificar el LEFT JOIN de ES2B (J2 y J5 son obligatorios). La prueba de exámenes lo verifica. |
| 2 | DB01 después de ME01–ME03 | DB01 es OBLIGATORIO en **D12**, diez días antes de ME01 (D22). DB02 y DB03 son REFUERZO del mini-ETL. |
| 3 | Tiempos de ME01–ME03 distintos de lo declarado | Los enunciados declaran «Primera vez: 60–80 / 80–100 / 80–110 min» y la carga estimada usa ese rango (antes fijaba 30 / 70 / 60). Para que cupieran, ME01 pasó al lunes D22, ME02 a D23 y ME03 a D24; la Puerta 4 se movió a D24. |
| 4 | ME04 sin ubicación | OBLIGATORIO en **D31**, junto a Excel, después de terminar el ETL guiado y antes de C06 (D36). |
| 5 | S01–S06 deben evaluar lo preparado | Prueba automática: todo ID de las tareas de cada examen aparece como OBLIGATORIO o REPASO en un día anterior o igual. |
| 6 | PB03 frente a la jornada reducida | PB03 define un núcleo de tres medidas (Ventas Bs, Pedidos Entregados, Ticket Bs) y deja Clientes Compradores y Frecuencia como REFUERZO; S05 y D33 dicen lo mismo y el ticket se comprueba contra K1, que es obligatorio. |

## 5. Ejemplos ANTES / DESPUÉS

### S1 · Primeros diez clientes

**ANTES** (`main`): título «Primeras 10 filas de clientes». «Caso laboral: el gerente requiere este resultado…». «Resultado de referencia: 10 filas y 6 columnas. El orden no se evalúa cuando hay empates.» Pista 1: «Identifica la tabla y la granularidad antes de escribir SELECT». Pista 2: «Decide qué condición filtra filas (WHERE) y cuál filtra grupos (HAVING)». Referencia: `SELECT * FROM clientes LIMIT 10;`.

**DESPUÉS:**

> *Situación.* Acabas de entrar al equipo comercial y quieres ver cómo luce el maestro de clientes antes de trabajar con él. Tu jefa te pide una muestra: los diez clientes con el código más bajo.
> *Una fila representa:* un cliente. *Columnas, en este orden:* 1 `cliente_id` — código · 2 `nombre_negocio` — nombre comercial, tal como está guardado · 3 `tipo` · 4 `zona` (puede estar vacía) · 5 `ruta` · 6 `fecha_alta`.
> *Reglas.* Las seis columnas, en el orden de la tabla. «Primeras diez filas» = los diez clientes con menor `cliente_id` (1 a 10), de menor a mayor. Una tabla no garantiza un orden si no lo pides.
> *Pistas.* (1) Abre el diccionario, fila `clientes`: ahí están las seis columnas; decide si las escribes o usas el atajo de «todas las columnas». (2) Tres ideas del capítulo 01: elegir columnas, ordenar y recortar con LIMIT; LIMIT corta después de ordenar. (3) Mira el primer y el último `cliente_id`: deben ser 1 y 10.
> *Criterios.* Seis columnas; exactamente 10 filas con `cliente_id` de 1 a 10; el orden está definido en la consulta. *Primera vez:* 20–35 min.
> Referencia: `… ORDER BY cliente_id LIMIT 10;` (mismos 10 clientes que el control anterior).

### S7 · Clientes sin zona

**ANTES:** el **título era la pista** («… Con "= NULL" no funciona porque NULL no es un valor…»); pista 1 genérica; sin columnas.
**DESPUÉS:** título neutro («Clientes sin zona registrada»); situación de calidad de datos; seis columnas con significado; «`zona` no tiene dato»; pistas: (1) el dato está ausente, no es un texto ni un cero; (2) un NULL no es igual a nada, ni a sí mismo: el capítulo 01 explica cómo preguntar por él; (3) con 0 filas probaste la igualdad con NULL, con más de 6 revisa si tratas texto vacío como NULL. Criterio propio: «Puedes explicar por qué la comparación con `=` no funciona».

### G4 · Rango de precios por categoría

**ANTES:** «5 filas y 4 columnas» sin decir cuáles; el redondeo a 2 decimales **no estaba escrito** y el corrector compara el valor exacto (un `AVG` sin `ROUND` fallaba sin explicación).
**DESPUÉS:** las cuatro columnas nombradas y descritas (`categoria`, `precio_prom` «redondeado a 2 decimales», `precio_min`, `precio_max`); «el corrector compara el valor exacto»; una fila por categoría; orden alfabético. Pista 2: AVG/MIN/MAX por grupo con GROUP BY y ROUND (capítulo 02, sección nueva).

### J1 · Pedidos con el nombre del cliente

**ANTES:** pista sobre «detalle y cabecera, pedidos distintos» (irrelevante: J1 no suma) y teoría con un ejemplo casi idéntico a la respuesta.
**DESPUÉS:** tablas `pedidos` y `clientes` con su relación `pedidos.cliente_id = clientes.cliente_id`; columnas `pedido_id`, `fecha`, `nombre_negocio` «tal como está guardado» (algunos nombres traen espacios: «no lo limpies»); 3.600 filas, de cualquier estado; orden por `pedido_id`. Pistas: (1) el nombre vive en otra tabla; (2) JOIN … ON y alias de tabla; (3) si no son 3.600 filas, revisa que la condición compare `cliente_id` con `cliente_id`. El ejemplo del capítulo 03 ahora une pedidos con vendedores.

### V4 · Clasificación ABC (ejercicio avanzado)

**ANTES:** el título decía «A = hasta 80 %», pero la referencia usa otra convención (el porcentaje **antes** de sumar al cliente) y la teoría revelaba el resultado («Da A=41, B=37, C=42»). Quien leía el título literalmente obtenía un resultado distinto del control.
**DESPUÉS:** la convención está en el enunciado («si el acumulado antes de sumar al cliente es menor que 80 % es A… así el cliente que cruza el 80 % queda en A»); tres tablas y relaciones; tres columnas con `pct_ventas` a 1 decimal; pistas progresivas (pasos → acumulado menos la propia venta → comprobar que las clases cubren 120 clientes y 100 % de las ventas); se retiró el resultado de la teoría.

## 6. Comprobación de los 81 ejercicios SQL

Tabla completa en `10_VALIDACION/COMPROBACION_81_SQL.md` (generada con `python herramientas/auditar_enunciados.py --tabla RUTA`). Para cada ejercicio se verificó automáticamente:

- las columnas del enunciado coinciden con las del contrato y las del control (nombres y orden): **81/81**;
- el número de filas citado en criterios y pistas coincide con el control: **81/81**;
- la referencia produce exactamente el control (mediante el corrector): **81/81**;
- tres pistas, una situación única y al menos un criterio propio: **81/81**;
- las tablas y columnas citadas existen en `comercial.db` y el diccionario coincide con la base (nombres y conteo de filas): **sin discrepancias**.

**Prueba independiente del enunciado:** escribí, solo a partir del texto de los enunciados, diez soluciones (S1, S6, G4, G7, J5, K4, V3, V4, X5, N1). Las diez pasaron el corrector.

**Cambios en referencias o controles** (todos justificados por el enunciado, no por las pruebas):
- 22 referencias ganaron un `ORDER BY` coherente con el orden pedido; los resultados no cambiaron (comparación fila a fila de los 81 controles contra la versión anterior).
- N5 y ES3C: alias legible en una columna que se llamaba `ROUND(ventas,2)` (solo cambia el nombre).
- **ES1B:** el filtro «al menos cinco productos» no filtraba nada (las cinco categorías tienen 8 productos); ahora «precio medio mayor a 9 Bs» (5 → 2 filas).
- **ES3C:** el examen evaluaba `RANK`, que ningún obligatorio practica; ahora porcentaje sobre el total con función de ventana (competencia de V3). Control nuevo.

## 7. Auditoría de las demás actividades

**Python (30).** Todos reescritos: firma, qué recibe y devuelve, reglas con el tipo de excepción, ejemplos **ejecutados contra la referencia** al generar los enunciados, tres pistas propias, criterios y primera vez. Hallazgos: P09 no decía `ValueError` aunque el corrector lo exige; P05 aprobaba `list(set(...))` por la casualidad del orden de enteros pequeños (nuevo caso de prueba; el corrector ahora lo rechaza); los enunciados no traían ningún ejemplo (los nuevos se ejecutan contra la referencia y no repiten los casos del corrector); las pistas eran idénticas en los 30. La regla automática exige que cualquier función que el corrector obligue a lanzar `ValueError` lo diga en su enunciado.

**Estadística (7).** ST01, ST02, ST03 y ST06 publicaban sus cifras de control; ST04 y ST07 recibían pistas sobre `ddof` y percentiles que no tenían relación. Ahora cada uno define datos, entregables y método (interpolación lineal, muestral frente a poblacional, α fijado antes) y no contiene ninguna cifra de `controles_estadistica.json` (prueba automática). ST03 a ST07 pasaron a REFUERZO/OPCIONAL por capacidad (ST01 y ST02 siguen obligatorios).

**Casos (15) y Excel/Power BI.** Las pistas «separa agenda, pedido y venta entregada» aparecían en PB01, EX03 o C05, donde no tienen sentido. C01 pedía «tres razones» en el criterio, pero el enunciado pedía cuatro frases; C04 exigía conciliar «por estado» sin decir cómo; PB03 contenía en el criterio las cifras de control; C06 no decía qué tablas, columnas y formatos validaba el corrector (`bronze/silver/rechazos/gold`, `auditoria.json`, `ruta` en mayúsculas, `monto_centavos`…). Todo se corrigió; los valores esperados de Power BI quedan en `VALIDACION_MANUAL.md` (lista de verificación, no enunciado).

**Depuración y mini-ETL.** DB01–DB03 tenían una sola pista; ahora tres. ME03 no declaraba las columnas de Gold ni las tablas que el corrector exigía, y pedía reutilizar P30 (REFUERZO): ahora es autosuficiente.

**Exámenes.** Ver sección 3, punto 10. Además se corrigieron las palabras pegadas («yunaprueba», «deconflicto»…) en todas las líneas editadas y el texto de S01–S02.

## 8. Flujo D01 → evaluación final

Reparto actual de lo OBLIGATORIO nuevo (D01 y D02 no cambian; ver `01_PLAN_DIARIO/nucleo.json`):

| Semana | Contenido | Carga estimada (obligatorio) / plan |
|---|---|---|
| 1 (D03–D06) | listas y diccionarios, GROUP BY/HAVING, bucles, condiciones; S01 | 711 / 650 min (D01–D02 no incluidos) |
| 2 (D08–D13) | funciones con errores, JOIN y LEFT JOIN, CSV, primer DataFrame, estadística descriptiva, DB01; S02 | 1.010 / 900 |
| 3 (D15–D20) | Pandas (monto, ticket, merge validado, duplicados, perfilado), CTE, ventanas, clientes inactivos, ABC; S03 | 1.002 / 900 |
| 4 (D22–D27) | mini-ETL (D22–D24, Puerta 4), ETL guiado hasta claves, N2; S04 (hito) | 978 / 900 |
| 5 (D29–D34) | ETL guiado hasta la carga (Puerta 5), Excel, ME04, Power BI en dos sesiones, N3; S05 | 1.000 / 900 |
| 6 (D36–D41) | C06 en cinco bloques; S06 | 970 / 900 |

La razón estimada/plan queda entre 1,08 y 1,12 por semana (antes de esta fase, ya con tiempos más optimistas, rozaba 1,0; los tiempos declarados en los enunciados son más honestos). Tres jornadas superan 1,2 (D20 1,24, D22 1,22, D31 1,21): para ellas, REDUCIDO. **La estimación sigue siendo un modelo con ±35 % de error, no una medición.**

Verificado automáticamente: cada OBLIGATORIO exige solo teoría ya asignada; ninguno depende de un REFUERZO/OPCIONAL; los exámenes evalúan lo preparado; todo ejercicio del banco SQL, Python y estadística sigue ubicado en algún día. Ni Excel, ni Power BI, ni estadística, ni ETL, ni KPIs se eliminaron.

## 9. Resultado de las pruebas

Todas sobre copias (el script escribe evidencia en `10_VALIDACION`). Windows 11, Python 3.12.10.

| Prueba | Resultado |
|---|---|
| `verificar_paquete.py` (20 grupos: los 13 originales, 4 de la fase 1 y 3 nuevos) | **20 de 20 correctos, 0 fallos** (`10_VALIDACION/resultados_pruebas_5_1.json`) |
| `auditar_enunciados.py` (6 familias de comprobaciones) | 0 problemas: SQL 81, Python 30, otros 29, fugas, dependencias y exámenes, índices y contratos |
| Control negativo: tres ejercicios con el mismo texto | el auditor lo detecta («repetida en 3 ejercicios») |
| Control negativo del defecto original | contra los 81 enunciados de `main` el auditor reporta 802 problemas, entre ellos **pista 1 repetida en 72 ejercicios, pista 2 repetida en 54 y otra en 18** (exactamente las cifras de la revisión independiente); contra la rama, 0 |
| `prueba_sqlite_cierre.py` | 5 de 5 |
| `regenerar_manifiesto.py --comprobar` | manifiesto vigente (435 archivos) |
| Corrector SQL sobre 10 soluciones escritas solo desde el enunciado | 10 de 10 |
| Corrector SQL sobre tu `S1.sql` y `S10.sql` (lectura) | S1: rechazado (una sola columna, como lo habría causado el enunciado antiguo); S10: correcto |
| D01, D02, datasets originales | sin cambios (`git status`) |

Nuevas pruebas automáticas dentro de `verificar_paquete.py`: **enunciados específicos / sin plantillas / sin fugas / exámenes alineados** (con control negativo), **guías, calendario y carga sincronizados con `nucleo.json`** (regenera las guías en una copia y exige igualdad byte a byte) y **manifiesto SHA256 vigente**.

## 10. No pude verificar

- **Power BI Desktop y Excel:** los enunciados y la lista de verificación se revisaron por lectura; nada se ejecutó en esas aplicaciones. La medida DAX `Crecimiento` sigue sin probarse (queda en PB04, REFUERZO).
- **Tiempos reales de «primera vez»:** son estimaciones mías para un principiante; no los medí con una persona. Los de ETL-1…6, C06-0…4 y EX01/PB01–PB03 reducidos los fijé yo a mano.
- **Aprendizaje:** que los enunciados sean completos no demuestra que ahora los resuelvas solo. Es una condición necesaria, no suficiente.
- **Teoría de D01 y D02 y los capítulos de Python/Pandas** no se ampliaron en esta fase (siguen siendo compactos); si lo quieres, es una decisión para la fase 2.
- **UAGRM:** el PDF y el notebook de la Clase 2 no se abrieron ni ejecutaron en esta fase.
- **Evaluación final:** no se tocó; las claves de respuesta siguen en el árbol de trabajo (pendiente J-3/J-4 de la fase 2).

## 11. Decisiones para revisar juntos

1. **N1 (cumplimiento mensual por ruta, 60–100 min)** pasó a REFUERZO: con tiempos honestos ninguna jornada lo soporta como obligatorio sin superar 1,25. El concepto lo practican C01 (D02) y, como refuerzo, N1, EX02 y PB04.
2. **Power BI:** las medidas núcleo (PB03) siguen obligatorias, pero PB04–PB06 y EX02–EX03 son REFUERZO/OPCIONAL.
3. **El mini-ETL ocupa más** (D22–D24 en lugar de D18–D22); el ETL guiado comienza en D25.
4. **ES1B y ES3C cambiaron de contenido** (sección 6): si prefieres conservar los originales como material, se puede dejar el control anterior como variante aparte.
5. **`mi_trabajo/sql/S1.sql`:** no lo toqué. Con el enunciado nuevo, la corrección es añadir las cinco columnas que faltan y el orden.

No haré commit, merge ni push hasta que lo autorices.
