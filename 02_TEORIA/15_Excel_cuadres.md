# Excel como segundo camino de validación

Excel sirve para reconciliar un resultado y comunicarlo, siempre que controles tipos y granularidad. Importa `drop_por_pedido.csv` con Datos→Desde texto/CSV; fija UTF-8 y decimal con punto según el archivo. No abras un CSV a ciegas si tu configuración usa coma decimal: podrías convertir montos a texto.

Una tabla dinámica sobre drop (una fila por pedido entregado) debe sumar `drop_bs` y contar `pedido_id`. Agrupa por ruta y luego por mes. Resultado general: suma 1.468.924,50 y conteo 3.442. Compara promedio como suma/conteo; el promedio de promedios de rutas sería incorrecto.

## Fórmulas y ejemplo pequeño

En una hoja, escribe ventas reales de 80.000 y presupuesto de 100.000. `=SI(B3=0,"",B2/B3)` da 80% al formatear como porcentaje. Para desviación absoluta usa real−presupuesto; desviación relativa `(real−presupuesto)/presupuesto` es −20%. Evita escribir 80 y además aplicar formato porcentaje, porque aparecería 8.000%.

Para comparar un código de cliente con el catálogo usa BUSCARX en versiones que la incluyen. Si un código no existe, escribe una etiqueta de revisión con el argumento si_no_se_encuentra; no asignes una ruta inventada. Para versiones anteriores usa INDICE/COINCIDIR. Duplicados en el catálogo requieren revisión porque una búsqueda puede devolver solo la primera coincidencia.

Estadística: `PROMEDIO`, `MEDIANA`, `DESVEST.M` y `PERCENTIL.INC`. En el drop Q1=214,125 y Q3=555,75 antes de redondear. Marca atípicos con límites de IQR, conserva la fila y documenta motivo de investigación. Formato condicional ayuda a detectar diferencias; no sustituye la comprobación numérica.

Los ejemplos escritos usan coma como separador de argumentos conforme a tu entorno. Excel puede requerir punto y coma según Windows: si rechaza la fórmula, cambia solo el separador de argumentos. Los nombres localizados se muestran en español; los archivos XLSX guardan nombres internos en inglés. No alteres simultáneamente separador decimal y de argumentos.

## Caso de discrepancia

Si SQL da 1.468.924,50 y Excel 1.534.625, probablemente incluiste anulados o calculaste sobre todos los ítems. La diferencia es 65.700,50 Bs. Antes de culpar a Excel, fija mismo periodo, estado, tabla y unidad. Si una sola ruta cambia, revisa código y espacios en la unión. Registra el cuadre y una captura sin datos privados.

Práctica EX01: tabla dinámica de rutas y comparación con SQL E4. EX02: presupuesto por mes/ruta comparado con N1. EX03: percentiles con comparación contra ST02. Sus criterios y resultados están en `03_EJERCICIOS/CASOS.md`. Las acciones de interfaz Excel quedan como comprobación manual.
