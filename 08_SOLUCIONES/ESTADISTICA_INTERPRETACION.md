# Corrección de interpretación estadística

ST01–ST03: la cola de ventas grandes eleva la media sobre la mediana. La mediana describe
posición central; el ticket medio sigue siendo necesario para cuadrar ventas totales.
Un atípico no es sinónimo de error. La distribución del drop no debe asumirse normal.

ST04: población clientes 120; muestra aleatoria estratificada por las seis rutas.
Usa tamaños proporcionales, ajusta redondeos para llegar a 30 y conserva semilla en la selección.
La elección por facilidad sesga rutas; pedidos de un cliente son observaciones agrupadas.
Una correlación unidades/monto es parcialmente estructural (monto=cantidad×precio), no evidencia causal.

ST05: diferencia A−B=27.1333 Bs; Welch t=3.405793; p=0.00120523.
IC 95% media A=(204.9260,228.5406) Bs. Bajo el diseño simulado,
la prueba compara medias independientes; no generaliza a rutas reales sin un marco de muestreo.
Antes de recomendar la campaña incluye coste de la intervención y efecto esperado en margen.

ST06: chi²=7.552448, gl 1, p=0.00599286, V=0.250873.
Esperados=[[32.5, 27.5], [32.5, 27.5]]; son conteos suficientes para este ejemplo.
Hay asociación en el escenario simulado; la encuesta por sí misma no demuestra causa.

ST07: p es probabilidad del estadístico bajo H0/modelo, no probabilidad de H0 o éxito.
El intervalo estima la media, no garantiza rango de ventas individuales.
El caso de rutas con pedidos repetidos requiere tratar agrupación por cliente, muestreo o un diseño
adecuado; no justifica causalidad. Aprueba solo si estas tres distinciones se explican con palabras propias.
