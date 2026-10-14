# 2.5 CASE y COALESCE: condiciones dentro de la consulta y valores faltantes

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: [2.2 GROUP BY](02_group_by_having.md) y [1.4 NULL](../01_SQL_basico/04_null.md).

## Para qué sirve

Muchas veces no basta con filtrar: necesitas **clasificar** (precio económico, medio o alto), **contar solo cierto tipo de filas dentro de un grupo** (cuántas ventas anuladas por vendedor) o **poner una etiqueta** donde falta el dato («Sin zona»). `CASE` hace lo primero y lo segundo; `COALESCE` lo tercero.

## Términos nuevos

- **CASE**: una expresión que devuelve un valor distinto según condiciones. Se escribe `CASE WHEN condición THEN valor ... ELSE valor_por_defecto END`.
- **Evaluación en orden**: `CASE` revisa las condiciones de arriba hacia abajo y usa la **primera** que sea verdadera; las demás se ignoran.
- **COALESCE(a, b, ...)**: devuelve el primer valor que **no** es NULL de la lista.
- **Agregación condicional**: sumar `1` o `0` según una condición, por ejemplo `SUM(CASE WHEN estado = 'anulado' THEN 1 ELSE 0 END)`, para contar solo algunas filas dentro de cada grupo.
- **Etiqueta**: un texto que representa un valor faltante o una clase (por ejemplo, «Sin zona»). Es una decisión de presentación, no una corrección del dato.

## Ejemplo paso a paso

**1. Clasificar con CASE.** Clasificamos los artículos según su precio: menos de 6 es «económico», de 6 a 10 es «medio» y más de 10 es «alto»:

```sql
SELECT nombre, precio,
       CASE WHEN precio < 6 THEN 'económico'
            WHEN precio <= 10 THEN 'medio'
            ELSE 'alto'
       END AS segmento
FROM articulos
ORDER BY precio, nombre;
```

```resultado
nombre | precio | segmento
Jabón | 3.5 | económico
Galletas | 4.5 | económico
Maní 80g | 5.0 | económico
Agua 2L | 6.0 | medio
Papas 100g | 7.5 | medio
Leche 1L | 8.0 | medio
Jugo 1L | 9.0 | medio
Gaseosa 2L | 11.5 | alto
Yogurt 1L | 12.0 | alto
Detergente 1kg | 14.0 | alto
```

Cómo se evalúa cada fila: si `precio < 6`, es «económico». Si no, se prueba la segunda condición `precio <= 10`: como ya sabemos que no es menor que 6, esta captura de 6 a 10. Lo que no cumple ninguna cae en `ELSE`. El **Agua 2L (Bs 6,00)** es «medio» porque 6 no es menor que 6: los bordes son justamente donde conviene mirar con cuidado. Si omites `ELSE`, las filas que no cumplen ninguna condición quedan con NULL.

**2. El orden de los WHEN importa.** Si cambias las dos primeras condiciones:

```sql
SELECT nombre, precio,
       CASE WHEN precio <= 10 THEN 'medio'
            WHEN precio < 6 THEN 'económico'
            ELSE 'alto'
       END AS segmento_mal
FROM articulos
WHERE nombre IN ('Jabón', 'Agua 2L', 'Detergente 1kg')
ORDER BY precio;
```

```resultado
nombre | precio | segmento_mal
Jabón | 3.5 | medio
Agua 2L | 6.0 | medio
Detergente 1kg | 14.0 | alto
```

El Jabón (Bs 3,50) queda «medio», porque `precio <= 10` es verdadero y se usa primero; la condición `< 6` nunca se llega a evaluar para él. Ordena de la más específica a la más general.

**3. Agregación condicional: contar solo algunas filas por grupo.** Por vendedor, cuántas ventas fueron entregadas y cuántas anuladas:

```sql
SELECT vendedor_id,
       COUNT(*) AS ventas,
       SUM(CASE WHEN estado = 'entregado' THEN 1 ELSE 0 END) AS entregadas,
       SUM(CASE WHEN estado = 'anulado' THEN 1 ELSE 0 END) AS anuladas
FROM ventas
GROUP BY vendedor_id
ORDER BY vendedor_id;
```

```resultado
vendedor_id | ventas | entregadas | anuladas
1 | 7 | 7 | 0
2 | 5 | 4 | 1
3 | 4 | 3 | 1
```

`CASE` produce 1 o 0 por fila y `SUM` los suma en cada grupo: es un conteo condicional. Control: `entregadas + anuladas = ventas` en cada fila. Con una sola consulta obtienes columnas que de otro modo requerirían varias.

**4. Un porcentaje con CASE.** El porcentaje de ventas anuladas por vendedor:

```sql
SELECT vendedor_id,
       COUNT(*) AS ventas,
       ROUND(100.0 * SUM(CASE WHEN estado = 'anulado' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_anuladas
FROM ventas
GROUP BY vendedor_id
ORDER BY vendedor_id;
```

```resultado
vendedor_id | ventas | pct_anuladas
1 | 7 | 0.0
2 | 5 | 20.0
3 | 4 | 25.0
```

Numerador: ventas anuladas del vendedor. Denominador: todas sus ventas. El `100.0` evita la división entera, como viste en 2.3.

**5. Etiquetar faltantes con COALESCE.** Tiendas por zona, con una etiqueta para las que no tienen:

```sql
SELECT COALESCE(zona, 'Sin zona') AS zona_reporte, COUNT(*) AS tiendas
FROM tiendas
GROUP BY zona_reporte
ORDER BY tiendas DESC, zona_reporte;
```

```resultado
zona_reporte | tiendas
Centro | 4
Norte | 3
Plan 3000 | 2
Sin zona | 2
Equipetrol | 1
```

`COALESCE(zona, 'Sin zona')` devuelve la zona si existe y `'Sin zona'` si es NULL. Ahora el grupo de las 2 tiendas sin zona tiene nombre y no pasa desapercibido. **Esto no corrige el dato en la base**: solo cambia cómo aparece en esta consulta.

**6. No rellenar con cero sin pensar.** `COALESCE` también sirve con números, pero cambia el significado:

```sql
CREATE TEMP TABLE prueba (id INTEGER, valor REAL);
INSERT INTO prueba VALUES (1, 10), (2, 20), (3, NULL);
SELECT AVG(valor) AS promedio_con_null, AVG(COALESCE(valor, 0)) AS promedio_con_cero FROM prueba;
```

```resultado
promedio_con_null | promedio_con_cero
15.0 | 10.0
```

Con NULL, el promedio ignora el dato faltante (15). Con `COALESCE(valor, 0)`, el faltante cuenta como cero y el promedio baja a 10. Cuál es correcto depende de si «falta» significa «no se midió» o «fue cero». Esa decisión es del negocio; anótala.

Ejemplo comercial: el jefe de ventas quiere ver, por ruta, cuántas visitas hubo, cuántas fueron realizadas y en cuántas se tomó pedido. Dos columnas de `SUM(CASE ...)` o `SUM(realizada)` con su porcentaje responden sin consultas separadas.

## Errores comunes

- **Olvidar el `END`** de un `CASE`: error de sintaxis.
- **Condiciones que se solapan o en mal orden**: la primera verdadera gana.
- **Omitir `ELSE`** y recibir NULL sin darte cuenta.
- **Rellenar con 0 los faltantes** sin una regla de negocio.
- **Creer que `COALESCE` arregla el dato**: solo lo disfraza en esa consulta.
- **No comprobar que las partes suman el todo** (`entregadas + anuladas = ventas`).
- **Usar `WHERE` cuando querías una columna condicional**: `WHERE estado = 'anulado'` elimina las demás filas; `SUM(CASE...)` conserva todas.

## Para comprobar que entendiste

1. ¿Qué devuelve `COALESCE(NULL, NULL, 5, 7)`?
2. ¿Qué pasa si una fila no cumple ninguna condición de un `CASE` sin `ELSE`?
3. ¿Qué diferencia hay entre filtrar con `WHERE estado = 'anulado'` y `SUM(CASE WHEN estado = 'anulado' THEN 1 ELSE 0 END)`?
4. ¿Por qué `AVG(COALESCE(valor, 0))` puede dar menos que `AVG(valor)`?

<details><summary>Respuestas</summary>

1. 5, el primero que no es NULL.
2. Devuelve NULL.
3. El `WHERE` descarta las otras filas; el `SUM(CASE…)` las mantiene y cuenta solo las anuladas, así puedes tener varias columnas condicionales a la vez.
4. Porque los NULL pasan a ser ceros y entran en el denominador.

</details>

## Micropráctica

1. Clasifica las tiendas por el año de su `fecha_alta`: antes de 2026 → «antigua», 2026 en adelante → «reciente» (puedes usar `fecha_alta < '2026-01-01'`). Muestra nombre, fecha y clase.
2. Cuenta tiendas por clase (consulta anterior agrupada).
3. Para `visitas_ej`, por fecha: visitas, realizadas, pedidos tomados y la efectividad (`pedido_tomado` entre `realizada`) con `NULLIF` y redondeo a 1 decimal.

Cómo saber que está bien: la 1 muestra 12 filas; la 2 devuelve 2 filas que suman 12 (hay 2 tiendas de 2026); en la 3, el 2026-09-03 tiene 3 visitas realizadas y 2 pedidos.

<details><summary>Comprobación de las consultas 2 y 3</summary>

```sql
SELECT CASE WHEN fecha_alta < '2026-01-01' THEN 'antigua' ELSE 'reciente' END AS clase,
       COUNT(*) AS tiendas
FROM tiendas
GROUP BY clase
ORDER BY clase;
```

```resultado
clase | tiendas
antigua | 10
reciente | 2
```

```sql
SELECT fecha,
       COUNT(*) AS visitas,
       SUM(realizada) AS realizadas,
       SUM(pedido_tomado) AS pedidos,
       ROUND(100.0 * SUM(pedido_tomado) / NULLIF(SUM(realizada), 0), 1) AS efectividad_pct
FROM visitas_ej
GROUP BY fecha
ORDER BY fecha;
```

```resultado
fecha | visitas | realizadas | pedidos | efectividad_pct
2026-09-01 | 4 | 3 | 2 | 66.7
2026-09-02 | 3 | 2 | 1 | 50.0
2026-09-03 | 3 | 3 | 2 | 66.7
2026-09-04 | 3 | 2 | 1 | 50.0
2026-09-05 | 1 | 1 | 1 | 100.0
```

</details>

## Después, en los ejercicios

`CASE` y `COALESCE` aparecen desde G4 y en varios N (indicadores) de [SQL](../../03_EJERCICIOS/SQL/INDICE.md). Cuando un enunciado pida «clasificar», «etiquetar» o «contar solo los…», piensa primero en `CASE`.

Siguiente capítulo: [3.1 Claves y relaciones](../03_SQL_joins/01_claves_relaciones.md).
