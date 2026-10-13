# Agregar sin perder el significado

Una agregación resume varias filas. `SUM` suma, `AVG` promedia, `MIN` y `MAX` buscan extremos. `GROUP BY` establece qué combinación identifica una fila del resumen. Si agrupas clientes por ruta, obtienes una fila por ruta; si agrupas por ruta y tipo, obtienes una fila por combinación. Explica ese cambio de granularidad antes de interpretar el resultado.

```sql
SELECT ruta, COUNT(*) AS clientes
FROM clientes
GROUP BY ruta
HAVING COUNT(*) > 20
ORDER BY clientes DESC, ruta;
```

`WHERE` filtra filas antes de agrupar. `HAVING` filtra grupos después de calcular sus agregados. Aquí se conservan rutas con más de veinte clientes. Para contar solo kioscos por ruta, añade `WHERE tipo='Kiosco'`; cambiarlo por HAVING puede producir resultados ambiguos. Selecciona únicamente claves de agrupación y expresiones agregadas. SQLite permite algunas columnas sueltas que otros motores rechazan, pero no debes depender de esa permisividad.

## El denominador decide qué pregunta respondes

Tres pedidos tienen montos 100, 200 y 600: el promedio es 300. Si sus detalles tienen 2, 3 y 10 líneas, el promedio por línea es otra cosa. `AVG(cantidad*precio_unitario)` aplicado al detalle mide el valor medio de una línea; no el ticket medio. Primero suma por pedido o usa ventas totales/pedidos distintos.

Un promedio de promedios tampoco suele ser correcto. Una ruta con un pedido de 100 y otra con nueve pedidos de 500 tienen promedio general 460, no 300. Para combinar grupos conserva el numerador y el denominador; calcula `SUM(ventas)/SUM(pedidos)`. No promedies porcentajes de rutas con tamaños diferentes para obtener un cumplimiento nacional.

La división entre enteros puede truncarse en SQLite. Usa `100.0 * realizados / NULLIF(planificados,0)`. `NULLIF` transforma un denominador cero en NULL: significa "no calculable", no 0% de desempeño. `ROUND` se aplica para presentar; evita redondear cada subtotal prematuramente.

## Cuadre empresarial

Si el gerente pide ventas entregadas, sumar todo el detalle incluye anulados. G3 vale 1.534.625 Bs y no es la cifra final comercial. Necesitas unir a pedidos y filtrar su estado: eso llegará con JOIN. Una consulta puede ser válida y responder la pregunta incorrecta.

Un buen control verifica: cantidad de grupos, suma de sus numeradores y unidad de medida. G5 produce seis rutas y sus clientes suman 120. G1 produce 158 anulados y 3.442 entregados; juntos suman 3.600 pedidos. Comprueba ambos caminos. Cuando un control no coincide, revisa primero el filtro y la granularidad, luego la sintaxis.

Práctica: G1–G8; N2 introduce un porcentaje con datos de visitas. Guarda una tabla y dos frases: qué mide y qué no puedes concluir. Fuente: SQLite SELECT, generación de grupos y agregados.
