# Estado de implementación integral V5

Fecha académica de registro: 17/10/2026. Base: `816890969e3963ffa8c1bb10b2a444c09eb3e748`, rama `correccion-pedagogica-definitiva`.

## Alcance autorizado y paradas

Autorizada la implementación hasta la muestra D04, D05 y D08–D13. Se requiere aprobación explícita para regenerar otras jornadas y para producir masivamente el lote de ejercicios nuevos. Las propuestas globales no equivalen a guías implementadas ni a competencias acreditadas.

D01–D03 son inmutables byte por byte. Conservar las 34 realizaciones, cinco de D04, los archivos personales, datasets, contratos, empleabilidad, exámenes S01–S06, H01–H08, C06 y evaluación privada. No añadir contenido obligatorio en D06/D13/D20/D27/D34/D41. ST05 obligatorio; ST06/chi-cuadrado/V de Cramér voluntarios; ST07 solo con preparación.

## Copia y protección verificadas

- Copia externa: `D:\Course Python\Claude\GPT\Respaldos_Plan_Data_BI_v5\8168909_pre_correccion_4b762330`.
- Incluye `.git` y material personal; 2.267 archivos copiados y verificados individualmente. Solo excluye `.venv`, entorno reinstalable.
- Manifiesto externo: `MANIFIESTO_SHA256.json`, SHA-256 `a2c2493c398370f6f1a656840fbad12d6363fd016a147bba2e19f7581dfcca65`.
- Instantánea local de protección: `PROTECCION_BASE_8168909.json`, 631 hashes y 34 casillas completadas. No incluye contenido de respuestas privadas.

## Fase actual

**MUESTRA IMPLEMENTADA Y VALIDADA. PARADA OBLIGATORIA ESPERANDO APROBACIÓN.** Ocho guías D04, D05 y D08–D13 aplicadas; seis documentos requeridos terminados. 496 comprobaciones de integridad y 13 grupos de regeneración/mutaciones aprobados; dos regeneraciones consecutivas sobre las guías aplicadas sin cambios de bytes. Teoría final: 629 bloques y siete grupos aprobados. Revisión semántica independiente completada. Seis recursos nuevos solo propuestos, cero ejercicios autónomos nuevos creados. La corrección global sigue pendiente.

## Trabajo asignado

- Inventario reproducible y procedencia histórica de recursos: `herramientas/inventariar_pedagogia.py` e informe INVENTARIO.
- Fuentes, enseñanza preparatoria y secuencia de muestra: `nucleo.json`, `lecciones.json`, teoría necesaria, matriz y auditoría de práctica.
- Generador: selección explícita de jornadas, preservación del progreso, unicidad, minutos y sesiones.
- Integridad: prueba por ID accionable, hashes, obligaciones, empleo, exclusión histórica, regresión e idempotencia en copias.

## Comandos y resultados hasta ahora

- Lectura de instrucciones aplicables: sin AGENTS.md encontrado en repositorio/ancestros.
- `git --no-optional-locks status`: limpio antes de editar; rama/HEAD esperados.
- Copia externa y doble comprobación SHA-256 origen/destino: aprobada.
- Extracción de protección desde copia: 631 archivos y 34 casillas, aprobada.
- Generación parcial aplicada; ver evidencias actualizadas y cronología de ensayos. Las afirmaciones de los intentos antiguos no sustituyen los resultados finales.

## Próximo paso

**Esperar aprobación explícita del usuario. No ejecutar más regeneraciones ni crear el lote de ejercicios nuevos.** Tras aprobación: retomar propuestas globales y sus requisitos, completar fuentes futuras y validadores curriculares globales, aplicar únicamente el alcance que se autorice. No repetir diagnóstico, inventario original ni backup; comprobar cambios posteriores antes de reanudar.

## Ensayo de integración 1

Se generó la muestra únicamente en copia temporal. Pasaron extracción de IDs, mutaciones de duplicado/progreso/tiempo/micropráctica, protección global y orden/coherencia de las actividades. Fallaron dos grupos por: (a) la copia de prueba omitía cuatro cachés protegidos ya existentes; se corrigió el arnés para copiarlos también, sin excluirlos de protección; (b) nueve obligaciones históricas fuera de muestra estaban solo en propuesta global y se están restituyendo en las listas canónicas como pendientes. Evidencia: PRUEBAS_REGENERACION_INTENTO_01.json. No se ejecutó generación global ni se alteraron guías fuera de muestra.

Regresión técnica en copia: fase1 aprobada (6 grupos OK y 2 privados omitidos por falta de custodia); privacidad 13 regresiones OK; cierre SQLite 5 grupos OK. Teoría ejecutó 626 bloques, sin error de ejemplos; fallaron dos filas de tiempos de índices tras ampliar conversiones/excepciones. Se corrigieron sus tiempos y totales; se repetirá la comprobación.

## Continuación tras restablecimiento de cuota

Se releyeron estado, diff, inventario y pruebas; se verificaron otra vez los 2.267 archivos del backup y su manifiesto, sin diferencias. Se conservaron los cambios locales. No hubo reset, restore, stash, commits ni push.

Los dos grupos fallidos del primer intento quedaron corregidos y se repitieron: los nueve recursos históricos están ahora en listas obligatorias inequívocas; S3/S5 siguen acreditados sin deuda nueva. Los archivos personales/cachés se copian íntegros en los ensayos. PRUEBAS_REGENERACION_INTENTO_01.json conserva la evidencia anterior.

Comandos aprobados más recientes:

- `python -B herramientas/aplicar_nucleo.py --dias 4,5,8,9,10,11,12,13`: ocho guías aplicadas, ninguna otra.
- `python -B herramientas/verificar_integridad_pedagogica.py --dias 4,5,8,9,10,11,12,13 --salida docs/auditorias/VALIDACION_INTEGRIDAD_MUESTRA.json`: 496 comprobaciones, cero fallos.
- `python -B herramientas/pruebas_correccion_pedagogica.py --salida docs/auditorias/PRUEBAS_REGENERACION_MUESTRA.json`: 13 grupos OK, doble regeneración y mutaciones detectadas.
- `python -B herramientas/inventariar_pedagogia.py --baseline <backup>/repositorio --escribir`: 352 recursos/subrecursos; unión histórica 77; cero recursos ausentes, cero obligaciones perdidas en fuentes, muestra aplicada.
- Regresión adicional en copia: 81 SQL con control negativo, 30 Python/Pandas (69 casos) con control negativo y controles estadísticos originales: aprobados, REGRESION_CONTRATOS_FINAL.json. No acredita al alumno.

Archivos principales modificados: nucleo.json, lecciones.json, generador parcial y módulo ruta_pedagogica.py; siete guías integrales y D13 editorial; teoría preparatoria y sus índices; README; herramientas de inventario/verificación/pruebas y artefactos de auditoría. Los contratos y correctores originales siguen intactos.

Correcciones semánticas adicionales: KPI 6.1 se puede ejecutar con csv/diccionarios antes de Pandas; la reproducción merge queda después de 10.3. La lección 9.2 explica asignar una columna antes de pedirlo. La lección 8.4 enseña el siglo explícito 20AA antes de P10; 7.7/8.5 preparan no finitos y Decimal. Se explicitan las cinco evidencias D04 y se comprueban dependencias obligatorias y orden publicado, además de IDs.

## Cierre verificable de la muestra

- `REGRESION_TEORIA_FINAL.json`: ejecución final en copia, código 0, 629 bloques, siete grupos OK. La discrepancia de índices del primer intento quedó corregida.
- `VALIDACION_INTEGRIDAD_MUESTRA.json`: 496 comprobaciones, cero fallos; incluye 34 marcas, cinco vigentes en D04, evidencias, tiempos visibles, sesiones, fuente y orden publicado.
- `PRUEBAS_REGENERACION_MUESTRA.json`: 13 grupos aprobados.
- `IDEMPOTENCIA_MUESTRA_APLICADA.json`: dos regeneraciones consecutivas en workspace, cero archivos cambiados; integridad verificada tras cada una.
- `INVENTARIO_EJERCICIOS_ANTES_DESPUES.*`: 352 recursos/subrecursos, unión histórica 77, cero recursos ausentes y cero obligaciones históricas perdidas en fuentes. Los destinos fuera de muestra siguen sin regenerar.
- `DISTRIBUCION_PEDAGOGICA_FINAL.{md,json}`: 42 jornadas con estados diferenciados; muestra 2.809 min (46 h 49 min), D04 solo pendiente. Total final del curso sin inventar, aún pendiente de implementación global.
- `AUDITORIA_SUFFICIENCIA_PRACTICA.md`: 30 micros existentes, 1.000 min; seis propuestas por 360–525 min, creadas 0.
- `REVISION_MUESTRA_PEDAGOGICA.md` y `RESULTADOS_VALIDACION_INTEGRAL.{md,json}`: resultados, archivos y límites listos para revisar.
- `DUPLICADOS_FUERA_MUESTRA_PENDIENTES.json`: barrido por defecto D04–D42 devuelve código 1, correctamente: duplicaciones heredadas en 25 jornadas sin permiso de regeneración. Las ocho jornadas aplicadas tienen cero duplicaciones; D01–D03 excluidas de unicidad y protegidas byte por byte. No presentar esto como curso globalmente reparado.
- `git diff --check`: sin errores de espacios. Solo avisos Git de conversión futura LF/CRLF; no se normalizó el historial protegido. HEAD sigue 8168909; sin commits/push.

Protecciones reiteradas: personales/progreso, datos, exámenes S01–S06, H01–H08, proyectos, correctores/contratos y material privado conservan hashes. Empleabilidad conserva texto/minutos. Excel/Power BI Desktop no ejecutados; dos pruebas con custodia final omitidas. Suites curriculares globales, manifiesto general y calendario/rutas antiguos pendientes de aprobación y extensión.
