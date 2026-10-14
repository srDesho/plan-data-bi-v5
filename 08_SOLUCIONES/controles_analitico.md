# Controles de criterio analítico y de hitos de comprensión

Ábrelo **solo después** de escribir tu respuesta o terminar el hito. Compara cifras y razonamiento, no palabras: en estas actividades no hay una única redacción correcta.
Cada cifra se vuelve a calcular con `python herramientas/verificar_etapa2.py`, así que no depende de la memoria de nadie.

## AN01 · ¿Qué estamos contando?

**Qué debería aparecer en una buena respuesta**

- Una buena respuesta separa **cobertura** (¿a cuántos clientes de la cartera llegamos?) de **frecuencia** (¿cuántas veces a cada uno?). Falta, por ejemplo, saber si la visita se **realizó** y si terminó en pedido.

**Cifras de control**

- Con la lista del enunciado: visitas, clientes distintos y visitas por cliente. → `10 4 2.5 | [('C07', 3), ('C12', 4), ('C18', 1), ('C30', 2)]`

## AN02 · Hechos e hipótesis: los pedidos anulados

**Qué debería aparecer en una buena respuesta**

- Los hechos válidos salen de G1: pedidos entregados, pedidos anulados y su porcentaje sobre los registrados. «Los vendedores nuevos» es una **hipótesis**: la tabla no tiene motivo de anulación ni antigüedad del vendedor.

**Cifras de control**

- Columnas de la tabla pedidos: no hay motivo de anulación. → `pedido_id; cliente_id; vendedor_id; fecha; estado`
- Pedidos anulados sobre pedidos registrados (porcentaje con 2 decimales). → `158, 3600, 4.39`

## AN03 · ¿Qué es una ruta «grande»?

**Qué debería aparecer en una buena respuesta**

- Cuenta de clientes por ruta (control en el JSON). Con el criterio absoluto entran R01, R06 y R02; con el relativo (≥ 20 %) también R01, R06 y R02 (R02 queda justo en 20,0 %). El punto es que los dos criterios **coinciden hoy** y pueden dejar de coincidir.

**Cifras de control**

- Clientes por ruta y porcentaje sobre 120. → `R01, 26, 21.7; R06, 25, 20.8; R02, 24, 20.0; R05, 17, 14.2; R03, 14, 11.7; R04, 14, 11.7`

## AN04 · Cumplimiento: ¿a quién felicitas?

**Qué debería aparecer en una buena respuesta**

- Norte 90,0 %; Centro 122,5 %; Sur no calculable (meta 0). Centro tiene el porcentaje más alto con la **meta más pequeña**: felicitar sin mirar la meta es una conclusión débil.

**Cifras de control**

- Cumplimiento de las tres rutas del enunciado. → `90.0 122.5 None`

## AN05 · ¿El INNER JOIN pierde filas?

**Qué debería aparecer en una buena respuesta**

- En esta base los controles dan cero huérfanos y el INNER conserva las 16.178 líneas. Eso describe **este extracto**; un archivo nuevo puede traer líneas sin pedido y exige repetir el control.

**Cifras de control**

- Líneas sin pedido, pedidos sin líneas y filas del INNER. → `0, 0, 16178, 16178`

## AN06 · Recomendación a gerencia: clientes sin compra

**Qué debería aparecer en una buena respuesta**

- Total y reparto por ruta en el JSON de control. Una buena acción es acotada («llamar primero a las rutas con más clientes sin compra»), con una medida (cuántos compran en las dos semanas siguientes). Evita «los clientes se fueron a la competencia»: es una hipótesis.

**Cifras de control**

- Clientes sin pedido entregado en septiembre, por ruta. → `R01, 6; R02, 3; R03, 1; R04, 2; R05, 3; R06, 4`

## AN07 · Tres preguntas, tres KPI

**Qué debería aparecer en una buena respuesta**

- 1 → cumplimiento = ventas reales / meta (Bs); 2 → cobertura de ejecución = visitas realizadas / visitas planificadas; 3 → efectividad = visitas con pedido / visitas realizadas. Ejemplo de cuarta pregunta: «¿cuánto vende cada visita?» (productividad).

## AN08 · ¿Cuál es el pedido típico?

**Qué debería aparecer en una buena respuesta**

- La media es mayor que la mediana (distribución sesgada a la derecha). La moda no es única: hay dos valores con la misma frecuencia máxima. Para dimensionar transporte suele convenir la mediana o un percentil alto; para ventas totales, la media (suma / n).

**Cifras de control**

- n, media, mediana y modas del drop size de pedidos entregados. → `3442 426.76 354.0 [192.0, 326.0]`

## AN09 · Tendencia: ¿más pedidos o pedidos más grandes?

**Qué debería aparecer en una buena respuesta**

- El salto de septiembre se debe casi por completo al **número de pedidos**; el drop size promedio casi no cambia. Con seis meses no se puede afirmar estacionalidad: se necesita al menos un ciclo anual completo.

**Cifras de control**

- Pedidos, ventas y drop promedio por mes (entregados). → `2026-04, 568, 246380.0, 433.77; 2026-05, 589, 246941.5, 419.26; 2026-06, 563, 244671.0, 434.58; 2026-07, 515, 230982.0, 448.51; 2026-08, 485, 199028.0, 410.37; 2026-09, 722, 300922.0, 416.79`

## AN10 · Concentración: ¿de cuántos clientes dependemos?

**Qué debería aparecer en una buena respuesta**

- Los 15 principales suman un poco menos del 55 % de las ventas (12,5 % de la cartera). Hacen falta unos 41 clientes (34 % de la cartera) para llegar al 80 %: la regla 20/80 **no se cumple** de forma literal; hay concentración moderada, no extrema.

**Cifras de control**

- Clientes con venta, porcentaje de los 15 principales y clientes para llegar al 80 % (convención de V4). → `120, 54.95, 41`

## AN11 · ABC: qué hacer con cada clase

**Qué debería aparecer en una buena respuesta**

- V4 oficial: A 41 clientes (80,5 % de las ventas), B 37 (14,6 %), C 42 (4,9 %). La razón ventas/clientes de A es 2,4; la de C es 0,14. Una limitación válida: el ABC mira solo ventas pasadas; no ve potencial ni margen.

**Cifras de control**

- Clases ABC con la convención del curso (acumulado antes del cliente: < 80 % A, < 95 % B). → `A, 41, 80.5; B, 37, 14.6; C, 42, 4.9`

## AN12 · Rechazos: ¿problema de datos o señal de negocio?

**Qué debería aparecer en una buena respuesta**

- El archivo trae 24 filas, 2 duplicados exactos, 6 rechazos (fecha, unidades ×2, producto, precio, estado) y 16 en Silver. Seis de 22 filas únicas es 27 %. Con 24 filas no se puede concluir que la caja esté dañada: hay causas distintas, casi una fila por causa.

**Cifras de control**

- Conteos de la referencia del mini-ETL y rechazos por causa. → `24 2 6 16 | [('estado', 1), ('fecha', 1), ('precio', 1), ('producto', 1), ('unidades', 2)] | 27.3`

## AN13 · Dispersión y atípicos: ¿qué pedido es «raro»?

**Qué debería aparecer en una buena respuesta**

- Los valores de referencia están en el JSON de control. Hay una cola larga a la derecha: 141 pedidos (4,1 %) superan la valla superior. Son pedidos grandes legítimos; descartarlos borraría justo a los mejores clientes.

**Cifras de control**

- Desviación muestral, Q1, Q3, IQR, P10, P90, valla superior y cantidad de atípicos. → `307.74 214.125 555.75 341.625 128.0 819.0 | 1068.1875 141 4.1`

## AN14 · Cobertura frente a efectividad: ¿a quién ayudas?

**Qué debería aparecer en una buena respuesta**

- Ana: cobertura 90 %, efectividad 50 %. Beto: cobertura 50 %, efectividad 80 %. Carla: cobertura 100 %, efectividad 30 %. Beto visita poco pero vende al visitar; Carla visita todo y vende poco al visitar: necesitan ayuda distinta.

**Cifras de control**

- Cobertura, efectividad y pedidos por visita planificada de los tres vendedores. → `Ana 90.0 50.0 45.0 | Beto 50.0 80.0 40.0 | Carla 100.0 30.0 30.0`

## AN15 · Productividad: dos formas de medir una ruta

**Qué debería aparecer en una buena respuesta**

- Por ventas totales: R02, R05, R04, R01, R06, R03. Por ventas por cliente: R05, R02, R04, R03, R01, R06. R03 sube de última a cuarta y R01 y R06 caen: tienen muchos clientes que compran poco cada uno.

**Cifras de control**

- Ventas entregadas, clientes y ventas por cliente por ruta. → `R01, 211141.5, 26, 8120.8; R02, 396680.5, 24, 16528.4; R03, 138326.0, 14, 9880.4; R04, 221148.0, 14, 15796.3; R05, 341538.5, 17, 20090.5; R06, 160090.0, 25, 6403.6`

## AN16 · C06: el problema de negocio antes del código

**Qué debería aparecer en una buena respuesta**

- El diccionario indica que no hay impuestos, descuentos ni devoluciones: preguntas sobre margen, ventas netas o devoluciones no se pueden responder. Respondibles: ventas entregadas por cliente y mes, documentos por cliente, proporción de líneas anuladas. Riesgo típico: confundir ventas válidas (solo entregadas) con ventas brutas.

## AN17 · C06: ¿hay tendencia o ruido?

**Qué debería aparecer en una buena respuesta**

- Referencia: julio 251.089,03 Bs, agosto 252.866,30 Bs, septiembre 236.242,42 Bs; líneas anuladas 7,9 %, 4,5 % y 5,2 %. Septiembre cae un 6,6 % frente a agosto, pero con tres puntos no se puede hablar de tendencia.

**Cifras de control**

- Ventas entregadas y % de líneas anuladas por mes en la Silver de referencia de C06. → `2026-07 1368 251089.03 7.9 | 2026-08 1328 252866.3 4.5 | 2026-09 1304 236242.42 5.2`

## AN18 · C06: el memo para gerencia

**Qué debería aparecer en una buena respuesta**

- Cifras de referencia de C06: 4.048 filas de origen, 40 duplicados exactos, 8 rechazadas y 4.000 líneas válidas; ventas válidas 740.197,75 Bs en 1.000 documentos de 400 clientes. Las ventas excluyen anulados y no incluyen impuestos, descuentos ni devoluciones.

**Cifras de control**

- Cifras de auditoría de C06. → `4048 40 8 4000 1000 400 740197.75`

## H01 · Hito de comprensión 1: consultar y calcular

**Qué debería aparecer en una buena respuesta**

- Explica: NULL no es igual a nada, ni a sí mismo (se usa `IS NULL`); el denominador de un cumplimiento es la meta y con meta 0 el resultado es «no calculable» (`None`), porque 0 % diría que no se cumplió nada; los anulados no son venta pero sí son pedidos registrados.

**Cifras de control**

- Resultado de la predicción «Consulta 1 (mini-base)». → `12, 10`
- Resultado de la predicción «Consulta 2 (mini-base)». → `anulado, 2; entregado, 14`
- Resultado de la predicción «Bucle». → `13.5`
- Resultados esperados de porcentaje_anulados. → `25.0 None 100.0`
- Clientes de R05 por tipo de negocio. → `Tienda de barrio, 7; Minimarket, 5; Restaurante, 3; Kiosco, 2`

## H02 · Hito de comprensión 2: funciones, errores y JOIN

**Qué debería aparecer en una buena respuesta**

- Un `ValueError` hace visible el dato inválido y detiene el flujo; devolver 0 lo esconde. INNER conserva solo filas con pareja; LEFT conserva todas las de la izquierda. `int(float("2.5"))` da 2 sin avisar: se pierde media unidad.

**Cifras de control**

- Resultado de la predicción «Una función que rechaza». → `0.15 | 0.075 | error: fuera de rango: 120% | error: falta %: abc`
- Resultado de la predicción «INNER frente a LEFT (mini-base)». → `16`
- Resultado de la predicción «LEFT (mini-base)». → `19`
- Resultados esperados de peso_kg. → `12.5 | 0.0 | error | error | error`
- Clientes sin compras entregadas de Bebidas. → `4`

## H03 · Hito de comprensión 3: Pandas, claves y ventanas

**Qué debería aparecer en una buena respuesta**

- `many_to_one` falla si la clave de la derecha se repite: evita multiplicar filas en silencio. Duplicado exacto: toda la fila es igual, se elimina; conflicto: misma clave con contenido distinto, se detiene. Un acumulado sin orden suma en un orden cualquiera y su resultado no se puede interpretar.

**Cifras de control**

- Resultado de la predicción «Un merge con catálogo repetido». → `4 | 1`
- Resultado de la predicción «Acumulado (mini-base)». → `4, 320.0, 11.8; 7, 288.0, 22.3; 14, 225.0, 30.6`
- Clientes necesarios para llegar al 50 % de las ventas entregadas. → `12`
- Pedido de mayor monto y su porcentaje en el ejemplo. → `2 60.0 60.0`

## H04 · Hito de comprensión 4: el mini-ETL

**Qué debería aparecer en una buena respuesta**

- Para el archivo de seis líneas: Bronze 6; duplicados exactos 1 (T4); rechazadas 3 (T2 por unidades, T3 por fecha imposible, T5 por unidades); Silver 2 (T1 y T4); 6 = 1 + 3 + 2. Si la segunda T4 tuviera 5 unidades sería un conflicto de clave: se detiene antes de eliminar nada.

**Cifras de control**

- Con la regla de más de 8 unidades, sobre la Silver de referencia del mini-ETL. → `2 8 14 True`
- Conteos del archivo de seis líneas con el contrato del enunciado. → `6 1 [('T2', 'unidades'), ('T3', 'fecha'), ('T5', 'unidades')] ['T1', 'T4'] True`

## H05 · Hito de comprensión 5: claves, duplicados y fechas

**Qué debería aparecer en una buena respuesta**

- Duplicado exacto: toda la línea es igual, se elimina. Conflicto: misma clave con contenido distinto, se detiene y se revisa (no se elige una versión al azar). Recuperar un vendedor vale solo con una regla inequívoca (una ruta, un vendedor). Los decimales binarios acumulan errores de centavos.

**Cifras de control**

- Resultado de la predicción «Recuperar un vendedor». → `R01 V1 | R02 sin regla | R03 V4 | R05 sin regla`
- Resultados esperados de la función de fecha. → `2026-09-03 | 2026-09-03 | 2026-09-03 | error | error | error`

## H06 · Hito de comprensión 6: Gold, cuadre y repetición

**Qué debería aparecer en una buena respuesta**

- Gold de ejemplo: C1/julio (F1 entregado; F2 anulado no cuenta) = 1.500 centavos con 1 documento; C1/agosto = 450 con 1; C2/julio = 200 con 1; C2/agosto no aparece porque solo tiene una línea anulada. Son 3 filas y 2.150 centavos; el ticket medio por documento es 1.500, 450 y 200. Dos centavos de diferencia suelen venir de decimales o de un redondeo hecho en dos lugares.

**Cifras de control**

- Resultado de la predicción «Un Gold pequeño». → `3 | 2150 | {'cliente': 'C1', 'mes': '2026-07', 'ventas': 1500, 'documentos': 1}`
- Ticket medio por documento del Gold del ejemplo. → `[1500.0, 450.0, 200.0]`
- Filas y total del Gold del ejemplo. → `3 | 2150 | {'cliente': 'C1', 'mes': '2026-07', 'ventas': 1500, 'documentos': 1}`

## H07 · Hito de comprensión 7: BI mínimo

**Qué debería aparecer en una buena respuesta**

- Con R02: ventas 1.700, meta 2.000, razón 0,85. Con R02 y septiembre: 900, 1.000, 0,9. Sin filtros: 4.200, 4.400, 0,9545. El promedio de las razones por fila (0,8333; 1,25; 0,8; 0,9) da 0,9458: no es lo mismo que la razón de sumas. Las medidas se calculan en el contexto; las columnas calculadas, fila por fila.

**Cifras de control**

- Resultado de la predicción «Contexto de filtro con números». → `(1700, 2000, 0.85) | (900, 1000, 0.9) | (4200, 4400, 0.9545)`
- Pedidos anulados sobre registrados (control SQL). → `4.39`
- Contexto de filtro del ejemplo. → `(1700, 2000, 0.85) | (900, 1000, 0.9) | (4200, 4400, 0.9545) | 0.9458`

## H08 · Hito de comprensión 8: transferencia a un caso nuevo

**Qué debería aparecer en una buena respuesta**

- Para el archivo de seis líneas: Bronze 6; duplicados exactos 1 (L4); rechazadas 3 (L2 por SKU inexistente, L3 por cantidad, L5 por precio negativo); Silver 2 (L1 y L4); ventas en centavos 2.100 (solo L1 entregada; L4 es anulada). Ecuación: 6 = 1 + 3 + 2.

**Cifras de control**

- Conteos del archivo de seis líneas con el contrato del enunciado. → `6 1 [('L2', 'sku'), ('L3', 'cantidad'), ('L5', 'precio')] ['L1', 'L4'] 2100 True`
