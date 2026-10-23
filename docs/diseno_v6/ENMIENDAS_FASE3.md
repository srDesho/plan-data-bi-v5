# Enmiendas aprobadas durante la Fase 3 (prevalecen sobre los documentos 01–08 de la Fase 2)

Los documentos `01`–`08`, `micropracticas.json`, `matriz_34.json` y `PROTECCION_HASHES.json` son la especificación aprobada en la Fase 2. `plan_v6.json` y `micropracticas.json` ya incorporan las enmiendas 1 y 2; las tablas en Markdown (`01_DISTRIBUCION_D01_D42.md`, `04_INVENTARIO_EJERCICIOS.csv`, `05_...`, `06_...`) **no se reescribieron** y quedan como registro histórico: donde difieren, vale esta página, `plan_v6.json` y `01_PLAN_DIARIO/nucleo.json`.

## 1. RS04 y RS05 pasan de REFUERZO a BASE (aprobado el 2026-10-18)

- **RS04** (intervalo de confianza del drop medio de R05 y comparación con una meta) pasa a la práctica BASE de **D37**, después de leer 12.2 y hacer su micropráctica. **RS05** (prueba de permutación R01 frente a R04, con `H0`, `H1` y `α` escritos antes de calcular) pasa a la práctica BASE de **D38**, después de 12.3 (D37) y 12.4 (D38).
- Motivo: en la ruta BASE original, 12.2 (D37) y 12.4 (D38) solo tenían microprácticas pequeñas, sin ejercicio autónomo con corrector hasta ST05 (D39), que es una comparación de grupos con Welch y solo calcula un intervalo de la media de un grupo. Quedaban sin práctica autónoma propia: el error estándar y el intervalo como habilidad independiente, la formulación de `H0`/`H1`, y el p-valor calculado de verdad (permutación). ST05 y ST07 siguen cubriendo Welch, supuestos, interpretación del p-valor y conclusión de negocio. C06 no practica inferencia (su criterio es de ETL).
- RS06 (Welch con intervalo de la diferencia) **sigue siendo REFUERZO**: se solapa con ST05.
- Efecto en horas: D37 300 → 330 min y D38 305 → 335 min (+60). Total BASE **9.452 min = 157 h 32 min** en esta enmienda (antes 9.392 = 156 h 32 min); la enmienda 4 lo deja en 9.457 min = **157 h 37 min**. Exceso total sobre el máximo: 1.033 min; promedio martes–viernes 310 min; máximo normal 340 min (sin cambio). Sesiones: D37-S1 185 min, D38-S1 180 min (≤ 215). REFUERZO: D37 72 → 42 min, D39 82 → 52 min.
- Cambios de fuente: `plan_v6.json`, `nucleo.json` (`dias`, `resumen`, `ejercicios_nuevos`, `refuerzo_dia_minimo`), `lecciones.json` y `micropracticas.json` (12.2, apartado 2 → RS04), enunciados `RS04.md`/`RS05.md`. Documentos derivados regenerados con `aplicar_nucleo.py --todos`.

## 2. Excepción autorizada a la protección por hash: `09_EVALUACION_FINAL/ENUNCIADO.md`

- Autorizada por el usuario el 2026-10-18 **exclusivamente** para corregir la duración informativa «90 horas» por la duración BASE definitiva.
- Sustitución textual mínima, comprobada por el script: solo cambian las líneas 5 y 7.
  - Línea 5: `## Este bloque no está incluido en las 90 horas` → `## Este bloque no está incluido en las 157 h 32 min de las 42 jornadas`.
  - Línea 7: `Las 42 jornadas suman 90 horas de plan (seis semanas).` → `Las 42 jornadas suman 157 h 32 min de trabajo BASE (seis semanas).` El resto de la línea (570 minutos netos, 9,5 h, enlace y reglas) no cambia.
- Sin tocar: preguntas, respuestas, puntuaciones, rúbrica, criterios, `datos/`, `verificacion/` ni archivos de custodia. SHA-256 antes: `e0807347f71cec04e06d124cc6a0ccc693690d7d580d9bcbb2f99a7050e77bbe`; después: `d953f1d80896998bca29b9cea589bc2a3f8757b92ea656be02e46378835b65cc`.
- `verificar_diseno_v6.py proteccion` registra la excepción en `EXCEPCIONES_AUTORIZADAS`: solo acepta el contenido con ese hash; cualquier otro cambio del archivo vuelve a contar como CAMBIADO. `auditar_enunciados.py` ya no depende del literal «90 horas»: calcula la duración desde `nucleo.json` y exige que el enunciado la cite y que no conserve «90 horas».

## 3. Correctores SQL: SQ13 a y SQ09 c

- **SQ13 a** (`TRIM` frente a `LTRIM`/`RTRIM`): los 8 nombres con espacio de `comercial.db` lo tienen al inicio, así que los tres dan el mismo resultado. Ahora el corrector ejecuta además la consulta sobre una **copia en memoria** de la base con dos clientes de prueba añadidos (uno con espacio solo al final y otro solo al inicio) y compara con el resultado esperado (10). `comercial.db` no se modifica. `LTRIM` y `RTRIM` quedan rechazados.
- **SQ09 c** (`NULLIF`): SQLite devuelve `NULL` al dividir entre 0, de modo que quitar `NULLIF` **no cambia el resultado con ningún dato**; ningún dato de prueba lo distingue. El enunciado ahora lo declara y el corrector exige por texto que la consulta use `NULLIF`. Es una comprobación de práctica, no de comportamiento.

## 4. Secuencia G1 y ROUND antes de S01 (aprobado el 2026-10-23, tras diagnóstico independiente)

**G1 (`GROUP BY` antes de enseñarse).** G1 pedía agrupar pedidos por estado en D04, pero `GROUP BY` se enseña en la lección 2.2 (D05), y D05 exigía G1 como requisito de entrada. Se traslada **G1 a D05**, como BASE obligatorio, después de leer 2.2 y de su micropráctica; D04 deja de exigirlo y D05 ya no lo pide para entrar. En la micropráctica 2.1 el apartado 4 («cuántas ventas están anuladas», sin agrupar) pasa de «→ G1» a autocomprobación. G1, G3, G5 y G6 no se modifican.

**ROUND antes de S01.** ES1B (examen S01, D06) exige `ROUND(AVG(...), 2)`, pero la lección 2.4 estaba entera en D11 y 2.1 solo la nombraba. La lección 2.4 se divide: la **base inicial de ROUND** (6 min de lectura, autocontenida y sin `GROUP BY`, con el ejemplo paso a paso de un promedio redondeado) se lee en **D04** justo después de 2.1, junto con el apartado 1 de su micropráctica (5 min, «importe promedio por línea redondeado a 2 decimales»); en **D11** queda el desarrollo restante (14 min de lectura y los apartados 2, 3 y 4). Cambios en teoría: `02_TEORIA/02_SQL_agregados/04_redondeo_texto_fechas.md` (anclas `preparacion-redondeo` y `desarrollo`). ES1B, S01, sus criterios, correctores y puntuaciones no se tocan.

**Horas.** D04 321 → 312 min, D05 296 → 316 min, D11 308 → 302 min. Total BASE **9.457 min = 157 h 37 min** (+5 min). Exceso total sobre el máximo 1.038 min; promedio martes–viernes 311 min; máximo normal 340 min (sin cambio).

**Fuentes y derivados.** `plan_v6.json`, `nucleo.json`, `lecciones.json` y `micropracticas.json`; guías D04, D05, D08, D09 y D11 (D08 y D09 citan los requisitos y ejercicios de D05); `CARGA_ESTIMADA`, `RUTAS`, `PLAN_V5`, `calendario` y el índice del capítulo 2. El generador (`aplicar_nucleo.py`) conoce ahora la sección inicial de 2.4, y rotula en cada micropráctica dividida dónde se hace el resto de sus apartados.

**Evaluación final (autorizado).** `09_EVALUACION_FINAL/ENUNCIADO.md`, líneas 5 y 7: solo cambia la cifra «157 h 32 min» → «157 h 37 min». SHA-256 con saltos LF del contenido autorizado: `847dda8e939e96277f4f88b4e4f59c33603234a1a12850130d0ce3da36ed1a7f` (registrado en `EXCEPCIONES_AUTORIZADAS`).

**Protección y saltos de línea.** Tras el commit, git con `autocrlf` deja los archivos con CRLF en el árbol de trabajo. `verificar_diseno_v6.py proteccion` compara ahora cada archivo con la línea base tanto con sus bytes como con los saltos normalizados a LF, para no marcar como cambiados los archivos que solo difieren en el final de línea (p. ej. las cuatro herramientas de Codex ya incorporadas); cualquier cambio de contenido sigue contando como cambiado.
