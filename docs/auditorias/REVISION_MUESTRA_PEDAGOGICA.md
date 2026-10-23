# Revisión de la muestra pedagógica V5

Base: `8168909`. Alcance aplicado exclusivamente: D04, D05 y D08–D13. La muestra queda entregada para aprobación; no se autoriza con este informe la regeneración de las demás jornadas ni el lote de recursos nuevos.

## Archivos para recorrer como estudiante

| Jornada | Guía resultante | Revisión semántica efectuada |
|---|---|---|
| D04 | [Fundamentos y progreso conservado](../../01_PLAN_DIARIO/dias/D04_2026-10-15.md) | Recuperación SQL/Python posterior al historial protegido. Cinco casillas vigentes completadas, con evidencias explícitas; las micros pendientes no heredan la marca de la lectura. G2 aparece una sola vez y sigue completado. |
| D05 | [Agrupación, denominadores, acumuladores y estadística](../../01_PLAN_DIARIO/dias/D05_2026-10-16.md) | GROUP BY/HAVING y micro antes de G1/G5/G6/G7; denominadores antes de S01; acumuladores/registros antes de P07. Población, frecuencias y centro con cálculo manual antes de automatizar. |
| D08 | [Texto, conversiones, contratos y dispersión](../../01_PLAN_DIARIO/dias/D08_2026-10-19.md) | Texto y conversiones antes de funciones compuestas; finitud se distingue de conversión exitosa. Varianza y desviación muestral/poblacional con método manual antes de ST01. UAGRM conserva su bloque independiente. |
| D09 | [Fechas SQL, JOIN y depuración](../../01_PLAN_DIARIO/dias/D09_2026-10-20.md) | ROUND/fechas y micro 2.4 antes de G8 y J2; cardinalidad/INNER y micro antes de J1/J2/J3. Excepciones y lectura de traceback antes de DB01. |
| D10 | [Archivos, precios y conciliación](../../01_PLAN_DIARIO/dias/D10_2026-10-21.md) | CSV/módulos y sus micros antes de P13; Decimal, no finitos y traducción de errores antes de P09. La regla de siglo 20AA se prepara antes de P10, sin cambiar su contrato. |
| D11 | [LEFT JOIN y estadística de entregas](../../01_PLAN_DIARIO/dias/D11_2026-10-22.md) | Ausencias/duplicaciones y micro antes de J5; ST01 obligatorio después de enseñanza manual y módulo statistics. No se atribuye un intento estadístico completado a D04. |
| D12 | [Fechas, cantidades, KPI y DataFrame](../../01_PLAN_DIARIO/dias/D12_2026-10-23.md) | KPI con csv/diccionarios y SQL antes de Pandas; la reproducción merge espera a 10.3. Asignación de columnas explicada antes de micro 9.2. N01 íntegro se reserva después de groupby; ST02 después de percentiles. |
| D13 | [S02 original y cierre](../../01_PLAN_DIARIO/dias/D13_2026-10-24.md) | Solo corrección editorial y de duplicaciones. Lectura 11.3 anticipada a D05; S02, H02 y simulacro originales íntegros. Sesiones 60+25+30+20+30+10=175 min. No introduce contenido obligatorio nuevo. |

Cada guía establece qué estudiar, qué resolver, qué entregar, cómo comprobarlo y dónde retomar. Las sesiones referencian actividades; no crean nuevas casillas. En REDUCIDO/MÍNIMO las obligaciones omitidas conservan la condición OBLIGATORIO PENDIENTE.

## Comprobaciones adicionales solicitadas

| Caso | Resultado de inspección real | Resolución aplicada o estado |
|---|---|---|
| J2/K1/V3/V4 y ROUND | J2 exige redondeo antes de su enseñanza anterior. K1/V3/V4 requieren después esa misma base. | Enseñanza y micro 2.4 en D09 antes de J2. Preparación anterior disponible para los ejercicios posteriores; sus guías fuera de muestra no se regeneran. |
| G7 | Su contrato cuenta combinaciones tipo/zona; no exige ROUND. | Se conserva después de GROUP BY. No se corrigió un defecto inexistente. |
| K2a/K2b y pistas posteriores | Pistas con subconsulta/CTE antes de 4.1/4.2 en su oferta anterior. | Oferta canónica reubicada a D18 con requisitos 4.1/4.2; material y pistas intactos. Guías D15/D16 originales pendientes de la fase global. |
| G6 y HAVING | 2.2 ya explicaba HAVING antes de G6. | Se conserva y hace obligatoria su micropráctica antes de G6. |
| 2.3 y S01 | Primera enseñanza previa estaba en D06, mismo día del examen, con micro voluntaria. | Enseñanza y micro completas anticipadas a D05; D06 y S01 permanecen intactos. El ajuste editorial de D06 espera aprobación global. |
| D04/D05 títulos | Título D04 prometía media/mediana sin enseñanza; D05 no describía su contenido real. | Títulos y objetivos concretos coherentes con las actividades asignadas. |
| S10 en README | Inicio pedía COUNT antes de estudiar agregación. | Inicio exige S1; S10 se sitúa después de 2.1 si está pendiente y conserva cualquier realización ya registrada. |
| P10 y año corto | `%y` puede interpretar 69–99 como siglo XX; el contrato exige 20AA. | Explicación, ejemplo distinto y ampliación de micro 8.4 antes de P10. Contrato y corrector originales conservados. |
| 6.1 antes de merge | Ejemplo y práctica exigían Pandas antes de aprenderlo. | Ruta con csv/diccionarios/SQL; demostración original Pandas preservada para después de 10.3. |
| Micro 9.2 | Pedía crear columna sin explicar previamente su asignación. | Ejemplo de copia y asignación antes de la práctica original. |

## Práctica y conservación

La [auditoría de suficiencia](AUDITORIA_SUFFICIENCIA_PRACTICA.md) cuenta los apartados reales de 30 micros existentes y los relaciona con ejercicios autónomos originales, variantes y evaluaciones. No se cuentan ejemplos resueltos ni notebooks guiados como ejercicios autónomos. Los complementos de ejemplos y casos límite forman parte de lecciones/micros existentes; no se creó un lote de nuevos ejercicios.

El [inventario](INVENTARIO_EJERCICIOS_ANTES_DESPUES.md) reconcilia 352 recursos/subrecursos y 77 IDs históricos alguna vez obligatorios. Los 19 recursos reclasificados se conservan: 17 restituidos en fuentes y S3/S5 acreditados históricamente, sin deuda nueva. Restaurar la clasificación futura no significa que su guía esté ya implementada.

D01–D03 conservan sus bytes; D04 conserva cinco realizaciones vigentes. Los archivos personales, progreso, datasets, proyectos, contratos/correctores, exámenes, hitos y material privado permanecen protegidos por hashes. Los bloques y filas de empleabilidad se comparan literalmente con la copia base.

## Verificación ejecutada y límites

- [Integridad de la muestra](VALIDACION_INTEGRIDAD_MUESTRA.json): 496 comprobaciones, cero fallos; incluye dependencias obligatorias, orden publicado, enlaces/anclas, evidencias y tres representaciones de minutos.
- [Pruebas de regeneración y mutaciones](PRUEBAS_REGENERACION_MUESTRA.json): 13 grupos, cero fallos. Las mutaciones de duplicado, marca perdida, tiempo falso, micro omitida, orden cambiado y requisito voluntario se rechazan.
- [Idempotencia aplicada](IDEMPOTENCIA_MUESTRA_APLICADA.json): dos regeneraciones consecutivas de las ocho guías con cero cambios de bytes; integridad verificada después de cada una. También se ensayó desde guías base en copia con una nota personal adicional.
- [Teoría final](REGRESION_TEORIA_FINAL.json): 629 bloques ejecutados y siete grupos de comprobación aprobados.
- [Contratos](REGRESION_CONTRATOS_FINAL.json): 81 SQL; 30 Python/Pandas, 69 casos; controles estadísticos originales y pruebas negativas aprobados.
- [Regresión técnica en copia](REGRESION_TECNICA_MUESTRA.json): ETL/C06, validadores, adversos, privacidad y cierre de conexiones. Las dos pruebas con referencia final privada se omiten por falta de custodia. La primera comprobación teórica falló en dos tiempos de índices; el registro final acredita su corrección.

El [barrido global de duplicados](DUPLICADOS_FUERA_MUESTRA_PENDIENTES.json) falla correctamente en 25 jornadas fuera de la muestra. Es una deuda de implementación global conservada y visible; no se declara que las 42 jornadas estén corregidas. D01–D03 se excluyen expresamente de la prueba de unicidad, pero se protegen byte por byte.

La revisión semántica evalúa la preparación del material; no acredita dominio del estudiante. Excel y Power BI Desktop no se ejecutaron. Las seis propuestas nuevas de Excel, Power Query, DW y checkpoints requieren aprobación antes de crearse. Las suites curriculares globales y el manifiesto general del paquete no se presentan como aprobados/sincronizados durante esta entrega parcial.

Los minutos son estimaciones iniciales del trabajo asignado. D04 muestra trabajo pendiente al inicio de la corrección; no inventa minutos reales de lo ya realizado. Si el estudiante completa actividades después, debe registrar sus minutos y pendientes: el presupuesto de fuente es una estimación inicial, no un cronómetro que disminuya automáticamente.

## Parada

Muestra implementada y validada. Esperar aprobación explícita de la muestra y del volumen de nuevos recursos antes de ampliar el trabajo. No hay commits, push ni publicaciones.
