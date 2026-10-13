# Rúbrica final: 100 puntos

|Componente|Puntos|Evidencia para puntaje completo|
|---|---:|---|
|Perfil y contrato|10|Granularidad, clave, formatos, reglas y KPIs no calculables|
|Transformación|30|Tipos, claves, catálogo, duplicados y rechazos trazables|
|Carga|15|Bronze/Silver/Gold íntegros y repetición sin duplicación|
|Validación|20|SQL independiente, filas/importes y entradas adversas|
|Analítica|10|KPIs posibles, unidad/periodo, tabla/gráfico y límites|
|Reproducción|5|Instalación/comando en README y logging útil|
|Defensa propia|10|Explicar cinco decisiones, tres errores y funciones sin copiar|

Objetivo: 80/100. Entre 75 y 79: una semana de refuerzo y variante nueva. Menos de 75: retomar
las dos bases más débiles; mantener postulaciones a roles de reportes/asistencia adecuados al nivel real.

Puertas críticas: dinero incorrecto, filas perdidas sin explicar, claves duplicadas o catálogo ambiguo,
segunda carga que duplica, incapacidad de explicar funciones o uso de IA/copia no declarado.
Cualquier puerta impide declarar autonomía aunque el puntaje total alcance 80.

Pruebas en copias: columna obligatoria ausente, clave de catálogo duplicada, misma linea_id con importe
distinto y cantidad fraccionaria. El proceso debe detener/rechazar explícitamente y preservar la salida
anterior si falla el contrato estructural. Registra comandos y resultados.
Los cuadres automáticos apoyan la evaluación; la regla sin IA requiere honestidad o un observador.
