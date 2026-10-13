# Transferencia y autonomía: resolver datos que cambian

Aprender un ETL de memoria no demuestra que puedas construir otro. La práctica de transferencia cambia nombres de columnas, claves, catálogo y formatos. Antes de escribir código abre una muestra y crea un diccionario: qué representa una fila, qué identifica una línea, qué valores son válidos y qué cifras deben cuadrar.

## Proceso de ocho pasos

1. Copia la entrada a Bronze y registra nombres, tamaños y conteos.
2. Perfila todas las columnas: tipos observados, nulos, categorías, duplicados y formatos.
3. Distingue estructura inválida, conflictos de clave y filas rechazables.
4. Escribe funciones pequeñas y pruébalas con tres ejemplos.
5. Aplica transformaciones y conserva rechazos con motivos.
6. Une el catálogo con validación de cardinalidad y busca huérfanos.
7. Calcula Gold y cuadra conteos/importes mediante SQL independiente.
8. Ejecuta de nuevo, documenta y explica límites a gerencia.

Cuando no cuadra, reduce el problema. Si Bronze−duplicados−rechazos no coincide con Silver, revisa filtros y joins. Si las filas coinciden pero el dinero no, busca cantidades truncadas, precios mal interpretados, estados incorrectos o un presupuesto multiplicado. Compara importes por documento para localizar el primer desvío.

## Cambios adversos

Una nueva columna no obligatoria puede conservarse en Bronze e ignorarse explícitamente en Silver. Una columna obligatoria ausente debe producir un error legible. Un SKU duplicado con descripciones contradictorias debe detener el JOIN. Si faltan campos para un KPI, documenta "no calculable" y solicita el dato; no construyas un sustituto bajo el mismo nombre.

La prueba de repetición verifica idempotencia lógica: dos ejecuciones generan iguales claves, filas y ventas. No exige que el archivo SQLite tenga iguales bytes internos. Es distinto de carga incremental, que aquí no forma parte del examen.

## Evaluación sin código de IA

Puedes consultar documentación oficial y tus definiciones conceptuales; no copiar soluciones del paquete ni pedir a una IA que programe. Registra las páginas consultadas y el motivo. Explica cada transformación con un ejemplo concreto. Si una función falla, depúrala tú antes de pedir ayuda en el estudio; durante el examen registra el bloqueo y continúa con tareas independientes.

Autonomía se evidencia con un programa reproducible, cuadres y explicación. Si no superas un hito, el plan recorta extras y reserva una sesión para esa base; no crea una deuda acumulada. El objetivo de noviembre es un ETL junior funcional y defendible, no autonomía profesional avanzada garantizada.

Práctica: C06 y evaluación final. No abras `08_SOLUCIONES/controles_final.json` ni la referencia hasta terminar el intento integral.
