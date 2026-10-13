# JOIN: conectar tablas y controlar multiplicaciones

Una clave primaria identifica una fila; una clave foránea apunta a otra tabla. `pedidos.cliente_id` conecta cada pedido con un cliente. `pedido_items.pedido_id` conecta varias líneas con una cabecera. El JOIN combina filas que satisfacen la condición; no sabe cuál era tu intención empresarial.

```sql
SELECT p.pedido_id, c.nombre_negocio, p.estado
FROM pedidos AS p
INNER JOIN clientes AS c ON c.cliente_id = p.cliente_id;
```

INNER JOIN conserva coincidencias. LEFT JOIN conserva todas las filas de la izquierda y coloca NULL cuando no encuentra una coincidencia a la derecha. Para listar clientes sin compras entregadas en septiembre, conserva todos los clientes y limita los pedidos en la condición ON:

```sql
SELECT c.cliente_id
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id=c.cliente_id
  AND p.estado='entregado'
  AND p.fecha BETWEEN '2026-09-01' AND '2026-09-30'
WHERE p.pedido_id IS NULL;
```

Es un anti-join: busca ausencia. Si pasas `p.estado='entregado'` al WHERE, los clientes sin pedido quedan excluidos porque su estado es NULL. `NOT EXISTS` es otra manera útil de expresar ausencia y evita las sorpresas de `NOT IN` cuando la subconsulta contiene NULL.

## Uno a muchos y doble conteo

Un pedido de 300 Bs con tres líneas aparece tres veces después de unir a detalle. Sumar un total de cabecera en ese resultado produciría 900 Bs. Sumar `cantidad*precio_unitario` del detalle sí es correcto: cada línea tiene su propio monto. Para contar pedidos usa `COUNT(DISTINCT p.pedido_id)` o agrega el detalle por pedido antes de unirlo.

El presupuesto tiene una fila por mes y ruta. Si lo unes directamente a miles de ítems y lo sumas, lo multiplicas. La solución es agregar ventas por mes y ruta, y unir dos tablas que compartan esa granularidad. Esta misma regla se aplica a Pandas, Excel y Power BI.

## Tres controles antes de entregar

1. Cuenta filas antes y después: pedido→cliente debe conservar 3.600 filas; pedido→detalle produce 16.178 líneas.
2. Busca claves huérfanas con LEFT JOIN + IS NULL. No pierdas registros silenciosamente con INNER JOIN.
3. Verifica el total de ventas entregadas: 1.468.924,50 Bs, y que ventas por ruta, vendedor y categoría sumen lo mismo.

No unas por nombres de negocio: pueden repetirse, tener espacios o cambiar. No uses DISTINCT para ocultar un JOIN incorrecto; primero explica por qué aparecen duplicados. Si el catálogo contiene dos filas con la misma clave, corrígelo o detén la carga antes de combinarlo.

Práctica: J1–J6, E1–E8, N8 y N9. El proyecto SQL exige una nota sobre la cardinalidad de cada unión. Fuente: SQLite SELECT, FROM y procesamiento de JOIN.
