# 2.2 GROUP BY y HAVING: una cifra por grupo

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisito: [2.1 Funciones de agregación](01_funciones_agregadas.md).

## Para qué sirve

Con `COUNT` o `SUM` sin más obtienes una cifra para toda la tabla. Pero las preguntas reales piden **una cifra por grupo**: ventas por ruta, tiendas por zona, pedidos por vendedor. `GROUP BY` parte las filas en grupos y aplica la función de agregación a cada grupo por separado. `HAVING` filtra esos grupos ya resumidos.

## Términos nuevos

- **Grupo**: el conjunto de filas que comparten el mismo valor en la columna de agrupación.
- **GROUP BY**: la cláusula que indica por cuáles columnas se forman los grupos. El resultado tiene **una fila por grupo**.
- **Columna de agrupación**: la que va en `GROUP BY`. Debe aparecer también en `SELECT` para saber a qué grupo pertenece cada cifra.
- **HAVING**: filtra grupos después de agrupar y calcular. Se usa con condiciones sobre funciones de agregación (por ejemplo `COUNT(*) >= 3`).
- **Orden lógico de una consulta**: `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`. Es el orden en que SQL *piensa*, distinto al orden en que lo escribes.

## Ejemplo paso a paso

**1. Contar por grupo.** Tiendas por ruta:

```sql
SELECT ruta, COUNT(*) AS tiendas
FROM tiendas
GROUP BY ruta
ORDER BY ruta;
```

```resultado
ruta | tiendas
R01 | 4
R02 | 4
R03 | 4
```

Cómo lo piensa SQL: toma las 12 filas, las reparte en tres grupos (R01, R02, R03) según el valor de `ruta` y para cada grupo calcula `COUNT(*)`. Resultado: **una fila por ruta**. Control inmediato: 4 + 4 + 4 = 12, el total de tiendas. **Las cifras de los grupos deben sumar el total**; si no suman, hay filas con NULL en la columna de agrupación o un filtro que no recordabas.

**2. Varias funciones por grupo.** Por categoría de artículo: cuántos hay, el más barato y el más caro:

```sql
SELECT categoria, COUNT(*) AS articulos, MIN(precio) AS minimo, MAX(precio) AS maximo
FROM articulos
GROUP BY categoria
ORDER BY categoria;
```

```resultado
categoria | articulos | minimo | maximo
Bebidas | 3 | 6.0 | 11.5
Limpieza | 2 | 3.5 | 14.0
Lácteos | 2 | 8.0 | 12.0
Snacks | 3 | 4.5 | 7.5
```

**3. Sumar un cálculo por grupo.** Importe por venta; las cinco más grandes:

```sql
SELECT venta_id, SUM(cantidad * precio_unitario) AS importe_bs
FROM venta_lineas
GROUP BY venta_id
ORDER BY importe_bs DESC, venta_id
LIMIT 5;
```

```resultado
venta_id | importe_bs
4 | 320.0
7 | 288.0
14 | 225.0
10 | 220.0
8 | 202.0
```

Aquí el grupo es la venta: sus líneas se suman y la tabla pasa de 39 filas (líneas) a 16 (ventas), de las cuales vemos 5. Es un cambio de **granularidad**: de "una línea" a "una venta". Verifícalo con la venta 7 que ya conoces: Bs 288.

**4. Agrupar por dos columnas.** Ventas por vendedor y estado:

```sql
SELECT vendedor_id, estado, COUNT(*) AS ventas
FROM ventas
GROUP BY vendedor_id, estado
ORDER BY vendedor_id, estado;
```

```resultado
vendedor_id | estado | ventas
1 | entregado | 7
2 | anulado | 1
2 | entregado | 4
3 | anulado | 1
3 | entregado | 3
```

Cada combinación (vendedor, estado) que existe es un grupo. Los vendedores 2 y 3 aparecen con dos filas cada uno porque tuvieron ventas entregadas y anuladas.

**5. HAVING: filtrar grupos.** Las zonas con al menos 3 tiendas:

```sql
SELECT zona, COUNT(*) AS tiendas
FROM tiendas
GROUP BY zona
HAVING COUNT(*) >= 3
ORDER BY tiendas DESC, zona;
```

```resultado
zona | tiendas
Centro | 4
Norte | 3
```

`HAVING COUNT(*) >= 3` se evalúa **después** de formar los grupos: no puede ir en `WHERE`, porque cuando `WHERE` actúa todavía no existen grupos ni conteos.

**6. WHERE y HAVING juntos.** Vendedores con al menos 4 ventas **entregadas**:

```sql
SELECT vendedor_id, COUNT(*) AS entregadas
FROM ventas
WHERE estado = 'entregado'
GROUP BY vendedor_id
HAVING COUNT(*) >= 4
ORDER BY vendedor_id;
```

```resultado
vendedor_id | entregadas
1 | 7
2 | 4
```

Orden de pensamiento: `WHERE` descarta las ventas anuladas **antes** de agrupar; luego se cuenta por vendedor; luego `HAVING` descarta a quien tiene menos de 4. La regla de oro: **si la condición es sobre una fila, va en `WHERE`; si es sobre un resultado de agrupar, va en `HAVING`**.

**7. El grupo NULL.** ¿Qué pasa con las tiendas sin zona?

```sql
SELECT zona, COUNT(*) AS tiendas FROM tiendas GROUP BY zona ORDER BY zona;
```

```resultado
zona | tiendas
NULL | 2
Centro | 4
Equipetrol | 1
Norte | 3
Plan 3000 | 2
```

Los NULL forman **su propio grupo** y aparecen como una fila con zona vacía. No desaparecen, pero son fáciles de pasar por alto. En 2.5 aprenderás a ponerles una etiqueta.

Ejemplo comercial: "ventas por ruta y por mes" es `GROUP BY ruta, mes`; "solo las rutas con más de 3 clientes sin compra" es un `HAVING COUNT(*) > 3`. La pregunta que te guía siempre es: **¿qué representa una fila de mi resultado?** Aquí, un grupo.

## Errores comunes

- **Poner en `SELECT` una columna que no está en `GROUP BY` ni dentro de una función**: SQLite no da error pero devuelve un valor cualquiera del grupo. Otras bases sí fallan. Todo lo que no es agregado debe estar en `GROUP BY`.
- **Usar `WHERE COUNT(*) > 3`**: da error (`misuse of aggregate`). Es un caso de `HAVING`.
- **Filtrar con `HAVING` algo que es condición de fila** (`HAVING estado = 'entregado'`): funciona a veces, es lento y confunde. Debe ser `WHERE`.
- **Agrupar por la columna equivocada** (por ejemplo, `tienda_id` cuando la pregunta es por ruta): el resultado es correcto pero responde otra pregunta.
- **No comprobar que los grupos suman el total.**
- **Olvidar el grupo NULL** al presentar un reporte por zona.
- **Ordenar con una columna que no está en el resultado**: puede funcionar, pero hace difícil de leer lo que ordenas.

## Para comprobar que entendiste

1. ¿Cuántas filas devuelve una consulta con `GROUP BY ruta` si hay 3 rutas distintas?
2. ¿Dónde va la condición «solo ventas entregadas»: `WHERE` o `HAVING`?
3. ¿Dónde va «grupos con más de 5 filas»?
4. ¿Qué pasa con los NULL en la columna de agrupación?

<details><summary>Respuestas</summary>

1. Tres filas (una por grupo).
2. `WHERE`, porque es una condición sobre cada fila.
3. `HAVING`, porque depende del conteo del grupo.
4. Forman un grupo propio.

</details>

## Micropráctica

1. Cuenta las ventas por estado (`ventas`).
2. Para `venta_lineas`, suma las unidades por artículo (`articulo_id`) y deja solo los artículos con 30 unidades o más, ordenados de mayor a menor.
3. Cuenta las visitas de `visitas_ej` por fecha y cuántas fueron realizadas en cada fecha (`SUM(realizada)`).

Cómo saber que está bien: la 1 devuelve 2 filas que suman 16; la 2 solo trae artículos con `unidades >= 30`; la 3 devuelve 5 filas (5 fechas) y las visitas por fecha suman 14.

<details><summary>Comprobación de las consultas 1 y 3</summary>

```sql
SELECT estado, COUNT(*) AS ventas FROM ventas GROUP BY estado ORDER BY estado;
```

```resultado
estado | ventas
anulado | 2
entregado | 14
```

```sql
SELECT fecha, COUNT(*) AS visitas, SUM(realizada) AS realizadas
FROM visitas_ej
GROUP BY fecha
ORDER BY fecha;
```

```resultado
fecha | visitas | realizadas
2026-09-01 | 4 | 3
2026-09-02 | 3 | 2
2026-09-03 | 3 | 3
2026-09-04 | 3 | 2
2026-09-05 | 1 | 1
```

</details>

## Después, en los ejercicios

Los ejercicios G de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) piden resúmenes por grupo. Antes de cada consulta anota: «una fila de mi resultado representa ___». Al terminar comprueba que las cifras por grupo suman el total que esperabas.

Siguiente: [2.3 Granularidad y denominadores](03_granularidad_denominadores.md).
