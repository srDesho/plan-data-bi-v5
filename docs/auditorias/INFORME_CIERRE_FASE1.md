# Cierre técnico · Fase 1 · Plan Data & BI v5

Fecha: 14 de octubre de 2026. Repositorio original, rama `main`, commit inicial `6ac1af8`.
Autorización: «AUTORIZO FASE 1 — Implementación y pruebas». La Fase 2 no se inició.

## Defectos reproducidos

Antes de editar el validador se generó una referencia del ETL guiado en un directorio temporal. La referencia aprobó con **36 comprobaciones**. Sobre cinco copias independientes se ejecutó `UPDATE gold_ventas_cliente_mes SET <columna> = NULL WHERE rowid = 1`, comprobando que cada mutación afectase exactamente una fila.

| Columna Gold obligatoria | Comportamiento anterior |
|---|---|
| `cliente` | Aprobaba incorrectamente con 30 comprobaciones |
| `mes` | Aprobaba incorrectamente con 30 comprobaciones |
| `pedidos` | Aprobaba incorrectamente con 30 comprobaciones |
| `unidades` | Aprobaba incorrectamente con 30 comprobaciones |
| `ventas_bs` | Aprobaba incorrectamente con 30 comprobaciones |

La condición de ausencia de nulos omitía seis controles Gold sin registrar un fallo. Los guardas de Silver y del otro validador revisados registraban fallos antes de omitir controles dependientes; no se justificó modificarlos.

La evidencia pública existente contenía resultados reservados dentro de `evidencia.final`, devueltos directamente por `final_con_custodia()`. Se verificó la estructura sin reproducir las respuestas en este informe. También se identificaron diagnósticos de mutaciones potencialmente sensibles y controles esperados literales en las herramientas.

## Exposición histórica conocida

`10_VALIDACION/resultados_pruebas.json` ya forma parte del commit `6ac1af8` con la exposición descrita. Sanear el árbol actual impide que las ejecuciones corregidas vuelvan a publicarla, pero **no elimina las respuestas de ese commit ni de copias anteriores**. No se reescribió el historial ni se afirma confidencialidad retrospectiva. Los resultados de la variante antigua se distinguen de esta exposición de la evaluación nueva.

## Correcciones aplicadas y archivos modificados

| Archivo | Cambio |
|---|---|
| `herramientas/validar_etl_distribuidora.py` | Registra y rechaza explícitamente NULL en las cinco columnas Gold obligatorias, identificando las columnas afectadas antes de omitir controles dependientes. |
| `herramientas/pruebas_validadores.py` | Cinco regresiones SQL independientes, conservando las 45 mutaciones existentes. La ejecución privada final captura sus salidas y elimina los detalles de errores del resultado publicable. |
| `herramientas/verificar_paquete.py` | La evidencia final contiene exclusivamente nombres de controles y estados. Protege errores y salidas de grupos privados; sustituye un conteo esperado literal por una relación calculada. Añade `--fase1` para ejecutar solo ocho grupos técnicos. |
| `herramientas/privacidad_final.py` | Protección común de stdout, stderr, logging y excepciones; esquema público y nombres permitidos; detección de evidencia reservada en informes, JSON, documentos y archivos generados. |
| `herramientas/pruebas_privacidad_final.py` | 13 regresiones de privacidad con datos ficticios, sin consultar respuestas privadas. |
| `herramientas/auditar_enunciados.py` | Sustituye la lista literal de respuestas esperadas por controles de estructura y artefactos públicos. No se ejecutó su auditoría pedagógica en esta fase. |
| `10_VALIDACION/resultados_pruebas.json` | Sustituye la evidencia anterior por la corrida técnica realmente ejecutada: ocho grupos, sin respuestas reservadas. |
| `10_VALIDACION/MANIFIESTO_SHA256.json` | Hashes actualizados después de los cambios y la evidencia. |
| `PROGRESO_FASE2.md` | Nuevo estado vigente: Fase 1 terminada y Fase 2 pendiente de autorización expresa. |
| `INFORME_CIERRE_FASE1.md` | Este informe, con reproducción, cambios, pruebas y exposición histórica. |

No se modificaron `validacion_comun.py` ni `validar_final.py`: la revisión de sus guardas no demostró el mismo defecto.

## Pruebas ejecutadas

Entorno: `.venv`, Python **3.12.10**, pandas **2.2.3**. Se desactivó la escritura de bytecode, incluida la de los módulos privados, con `-B` y `PYTHONDONTWRITEBYTECODE=1`.

| Prueba | Resultado ejecutado |
|---|---|
| Reproducción anterior a la corrección, en salidas temporales | Referencia: 36 controles; los cinco NULL aprobaban indebidamente con 30 controles. |
| `pruebas_validadores.py --custodia <custodia externa>` | **3 referencias correctas aprobadas y 50 alteraciones rechazadas**: C06 16, ETL guiado 11 anteriores + 5 NULL, evaluación final 18. Ninguna omitida. |
| Regresiones de privacidad con referencias ficticias | **13/13**. Demuestran que la devolución anterior publicaba un centinela y la actual no; incluyen stdout, stderr, logging preexistente, errores, omisiones, nombres manipulados, campos adicionales, JSON y logs generados. |
| `verificar_paquete.py --fase1`, en copia temporal de los componentes técnicos | **8/8 grupos OK, 0 fallos y 0 omisiones**, con la referencia privada externa disponible. |
| Auditoría de artefactos sobre la salida recién generada y sobre el repositorio tras publicarla | Sin filtraciones detectadas. La evidencia final y los errores solo publican estados y controles permitidos. |
| Integridad mediante SHA256 contra una instantánea inicial | Planificación completa, teoría completa, jornadas, `mi_trabajo` y los archivos de custodia sin cambios. |
| `regenerar_manifiesto.py` y `regenerar_manifiesto.py --comprobar` | Manifiesto regenerado para **590 archivos**; comprobación: **Manifiesto vigente**. |
| Sintaxis de los seis archivos Python modificados o nuevos y `git diff --check` | Correctas, sin errores de sintaxis ni de espacios. |

Los ocho grupos son: dos ejecuciones del ETL guiado; C06 y su validador; referencias y mutaciones de los validadores; referencia final y repetición; adversas C06; adversas finales; regresiones de privacidad; artefactos públicos. Incluyen segunda ejecución sin duplicación y preservación de la salida anterior ante fallos estructurales.

La copia temporal del verificador incluyó únicamente `herramientas`, datasets, soluciones de referencia, evaluación y validación; no incluyó el calendario ni las lecciones. Las salidas privadas de pruebas fueron temporales. Solo se trasladó al repositorio el informe público ya comprobado.

La primera comprobación auxiliar posterior al verificador falló al buscar una clave con tilde por la codificación de la consola. No se publicó ese intento. Se corrigió la comprobación y se repitió la ejecución dirigida hasta obtener el resultado anterior, con código de salida 0.

No se ejecutó el verificador completo de 24 grupos ni se atribuyen sus resultados históricos a esta corrida. No se ejecutaron generadores del calendario, verificadores pedagógicos, ejemplos teóricos ni notebooks.

## Estado final

**Fase 1 técnica completada.** Manifiesto regenerado y comprobado después de actualizar la evidencia y el progreso; sintaxis y `git diff --check` correctos. Este informe, como los demás informes sueltos de la raíz, está excluido del manifiesto por su regla existente.

Rama `main`, HEAD `6ac1af8`, sin commits, push ni operaciones destructivas. Cambios esperados: siete archivos rastreados modificados y tres nuevos, todos enumerados arriba; nada preparado para commit. La Fase 2 queda pendiente de autorización expresa.

## Límites

Las pruebas usan `.venv` con Python 3.12.10 y salidas temporales. No se ejecuta la evaluación personal del estudiante. La referencia privada solo se utiliza como oráculo de pruebas, sin publicar sus respuestas ni modificar la custodia externa.

No se regeneró el calendario ni se revisaron los 17 prerrequisitos. No se modifican las lecciones, las jornadas, `mi_trabajo`, D01, D02 ni los materiales originales UAGRM. Excel, Power BI Desktop, SQL Server y la autonomía real del alumno conservan sus límites previos; no se declaran comprobados por esta fase técnica.
