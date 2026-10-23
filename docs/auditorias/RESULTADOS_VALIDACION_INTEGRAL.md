# Resultados de validación integral · entrega de muestra V5

Estado: **muestra aplicada y validada; parada obligatoria esperando aprobación**. Base `8168909`, rama `correccion-pedagogica-definitiva`. No se declara completada la corrección de las 42 jornadas.

## Resultado comprobable

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Integridad, progreso, fuentes, orden, enlaces y tiempos | 496 comprobaciones, cero fallos | [JSON](VALIDACION_INTEGRIDAD_MUESTRA.json) |
| Regeneración y mutaciones | 13 grupos aprobados; incluye rechazo de requisitos voluntarios y orden publicado incorrecto | [JSON](PRUEBAS_REGENERACION_MUESTRA.json) |
| Idempotencia real de las ocho guías | Dos regeneraciones consecutivas, cero cambios de bytes; integridad tras cada una | [JSON con hashes](IDEMPOTENCIA_MUESTRA_APLICADA.json) |
| Historia D01–D03 | Bytes idénticos a copia base | [Protección](PROTECCION_BASE_8168909.json) |
| Progreso | 34 casillas conservadas; cinco vigentes en D04, G2 único y completado, con evidencia | [Integridad](VALIDACION_INTEGRIDAD_MUESTRA.json) |
| Archivos personales, datasets, contratos, proyectos, exámenes y empleo | Hashes originales conservados; bloques y minutos de empleo idénticos | [Integridad](VALIDACION_INTEGRIDAD_MUESTRA.json) |
| Obligaciones | 77 IDs históricos reconciliados; 19 reclasificados conservados (17 restituidos en fuente y S3/S5 acreditados); cero recursos originales ausentes | [Inventario](INVENTARIO_EJERCICIOS_ANTES_DESPUES.md) |
| Teoría | 629 bloques ejecutados; formato, enlaces, tiempos, términos, glosario y fugas aprobados | [Registro final](REGRESION_TEORIA_FINAL.json) |
| SQL | 81 contratos y control negativo aprobados | [Registro](REGRESION_CONTRATOS_FINAL.json) |
| Python/Pandas | 30 contratos, 69 casos y control negativo aprobados | [Registro](REGRESION_CONTRATOS_FINAL.json) |
| Estadística | Controles originales disponibles ST01/ST02/ST03/ST05/ST06 aprobados; no acredita al estudiante | [Registro](REGRESION_CONTRATOS_FINAL.json) |
| ETL/C06/adversos/validadores | Seis grupos técnicos de fase1 aprobados; dos privados omitidos por falta de custodia | [Registro inicial en copia](REGRESION_TECNICA_MUESTRA.json) |
| Privacidad y SQLite | 13 regresiones de privacidad y 5 grupos de cierre de conexiones aprobados | [Registro](REGRESION_TECNICA_MUESTRA.json) |

## Carga de muestra: sesiones retomables

Las horas incluyen empleo y cierre. Excluyen UAGRM y evaluación final privada. D04 informa trabajo pendiente al inicio de la corrección, sin repetir ni inventar minutos reales de realizaciones completadas.

| Guía | Minutos BASE | Horas estimadas |
|---|---:|---:|
| [D04](../../01_PLAN_DIARIO/dias/D04_2026-10-15.md) | 522 | 8 h 42 min |
| [D05](../../01_PLAN_DIARIO/dias/D05_2026-10-16.md) | 554 | 9 h 14 min |
| [D08](../../01_PLAN_DIARIO/dias/D08_2026-10-19.md) | 310 | 5 h 10 min |
| [D09](../../01_PLAN_DIARIO/dias/D09_2026-10-20.md) | 404 | 6 h 44 min |
| [D10](../../01_PLAN_DIARIO/dias/D10_2026-10-21.md) | 302 | 5 h 02 min |
| [D11](../../01_PLAN_DIARIO/dias/D11_2026-10-22.md) | 268 | 4 h 28 min |
| [D12](../../01_PLAN_DIARIO/dias/D12_2026-10-23.md) | 274 | 4 h 34 min |
| [D13](../../01_PLAN_DIARIO/dias/D13_2026-10-24.md) | 175 | 2 h 55 min |
| **Total muestra** | **2809** | **46 h 49 min** |

D05 incorpora práctica antes de S01; D13 conserva examen 60 + corrección 25 + simulacro 30 + H02 20 + empleo 30 + cierre 10 = 175 min. No se introdujo contenido obligatorio nuevo en ninguna jornada de examen. El total final BASE del curso aún no está determinado: la [distribución](DISTRIBUCION_PEDAGOGICA_FINAL.md) separa muestra, historia y propuesta global.

## Revisión pedagógica y práctica

La [revisión de las ocho guías](REVISION_MUESTRA_PEDAGOGICA.md) documenta los casos reales y las equivalencias. La [matriz](MATRIZ_PRERREQUISITOS_Y_COMPETENCIAS.md) establece preparación antes de práctica/evaluación. La [auditoría de suficiencia](AUDITORIA_SUFFICIENCIA_PRACTICA.md) cuenta 30 micros existentes, sus apartados, ejercicios autónomos, casos y evaluación; no cuenta lecturas ni ejemplos como autonomía.

Se proponen **6 actividades nuevas**: EX04/PQ01/DW01 (3 prácticas aplicadas) y CK-DA/CK-STI/CK-BI (3 checkpoints separados), por **360–525 min**. Se han creado **0 ejercicios autónomos nuevos**. Sus brechas y criterios están descritos individualmente; requieren aprobación antes de producirse.

ST05 es obligatorio en la propuesta futura, con preparación; ST06/chi-cuadrado/V de Cramér siguen disponibles voluntariamente. ST07 solo se propone obligatorio tras preparación adecuada. No se alteraron exámenes originales para introducir esos contenidos.

## Fallos anteriores y límites

El primer ensayo falló porque su copia excluía cachés protegidos y nueve obligaciones futuras estaban solo en propuesta. Se corrigió el arnés para incluir los archivos y se restituyeron las obligaciones en fuentes; las pruebas se repitieron y pasan. Se conserva [el intento fallido](PRUEBAS_REGENERACION_INTENTO_01.json). La primera regresión de teoría detectó dos tiempos de índices desfasados: están corregidos y la [ejecución final](REGRESION_TEORIA_FINAL.json) pasa. No se cambiaron valores esperados ni correctores originales.

El control por defecto de duplicados D04–D42 **falla correctamente en 25 jornadas fuera de muestra**, con 57 pares recurso/jornada repetidos heredados. [Registro completo](DUPLICADOS_FUERA_MUESTRA_PENDIENTES.json). D01–D03 están expresamente excluidos de unicidad y protegidos por hash; sus duplicaciones históricas se conservan sin crear tareas nuevas. Cero duplicados corresponde a las ocho jornadas autorizadas, no al curso entero.

Las guías restantes, calendarios generales y RUTAS/CARGA anteriores no se regeneraron. Su desajuste transitorio frente a fuentes/propuestas está declarado en README, distribución y estado. Las suites curriculares globales y el manifiesto general del paquete no se presentan como aprobados durante esta entrega parcial. Excel/Power BI Desktop y referencia privada del final no se ejecutaron. La revisión de material y los controles no acreditan autonomía del estudiante.

## Copia y parada

Copia externa verificada: `D:\Course Python\Claude\GPT\Respaldos_Plan_Data_BI_v5\8168909_pre_correccion_4b762330`, con 2.267 archivos y Git. Manifiesto SHA-256 `a2c2493c398370f6f1a656840fbad12d6363fd016a147bba2e19f7581dfcca65`. No hubo commits, push, publicaciones ni modificación del trabajo personal.

**Detenerse aquí.** Esperar aprobación explícita de la muestra antes de regenerar las demás jornadas y aprobación del volumen propuesto antes de crear el lote nuevo. [Estado recuperable](ESTADO_IMPLEMENTACION.md).
