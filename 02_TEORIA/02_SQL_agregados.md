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

## Funciones que usarás desde G4: redondeo, texto, fecha y condición

Estas herramientas aparecen en los ejercicios y no se explican en ningún otro capítulo. Los ejemplos usan tablas distintas a las de los ejercicios.

```sql
-- ROUND(valor, n) redondea a n decimales; strftime('%Y-%m', fecha) extrae año y mes de una fecha ISO como texto 'AAAA-MM'.
SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS visitas, ROUND(100.0 * SUM(realizada) / COUNT(*), 1) AS pct_realizadas
FROM visitas
GROUP BY mes;
```

```sql
-- CASE devuelve una etiqueta según condiciones, evaluadas en orden; TRIM quita espacios de los extremos; UPPER pasa a mayúsculas.
SELECT producto_id,
       CASE WHEN stock_final > stock_inicial THEN 'sube'
            WHEN stock_final = stock_inicial THEN 'igual'
            ELSE 'baja' END AS tendencia,
       UPPER(TRIM('  ejemplo  ')) AS texto_limpio
FROM inventario
LIMIT 5;
```

```sql
-- UNION ALL apila resultados que tienen las mismas columnas. Una consulta puede empezar con una vista temporal (desaparece al cerrar la conexión).
CREATE TEMP VIEW productos_baratos AS SELECT producto_id, nombre FROM productos WHERE precio_unitario < 4;
SELECT 'baratos' AS grupo, COUNT(*) AS filas FROM productos_baratos
UNION ALL
SELECT 'vendedores', COUNT(*) FROM vendedores;
```

Una condición de CASE se evalúa de arriba abajo y la primera verdadera gana; sin ELSE, los casos no cubiertos quedan NULL. Para contar solo algunas filas dentro de un grupo, suma 1 o 0 con `SUM(CASE WHEN … THEN 1 ELSE 0 END)`. Las funciones de ventana (`OVER`) se explican en el capítulo 04.

## Cuadre empresarial

Si el gerente pide ventas entregadas, sumar todo el detalle incluye anulados. G3 suma también las líneas de pedidos anulados, así que no es la cifra final comercial y será mayor que las ventas que calcularás en J2. Necesitas unir a pedidos y filtrar su estado: eso llegará con JOIN. Una consulta puede ser válida y responder la pregunta incorrecta.

Un buen control verifica: cantidad de grupos, suma de sus numeradores y unidad de medida. G5 produce una fila por ruta y sus clientes deben sumar 120. G1 produce una fila por estado y sus dos cifras deben sumar el total de pedidos de la tabla. Comprueba ambos caminos. Cuando un control no coincide, revisa primero el filtro y la granularidad, luego la sintaxis.

Práctica: G1–G8; N2 introduce un porcentaje con datos de visitas. Guarda una tabla y dos frases: qué mide y qué no puedes concluir. Fuente: SQLite SELECT, generación de grupos y agregados.
