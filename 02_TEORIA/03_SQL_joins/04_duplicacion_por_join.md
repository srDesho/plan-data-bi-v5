# 3.4 Cuando el JOIN duplica: el error silencioso más caro

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [3.1](01_claves_relaciones.md), [3.2](02_inner_join.md) y [3.3](03_left_join_ausentes.md).

## Para qué sirve

Un JOIN mal planteado no da error: devuelve más filas de las que debería, y cualquier suma que hagas después queda inflada. El reporte se entrega, el número parece grande y razonable, y nadie lo cuestiona. Esta es la causa más común de cifras equivocadas en SQL, Pandas, Excel y Power BI. Esta lección te enseña a detectarlo antes de entregar.

## Términos nuevos

- **Duplicación por JOIN** (o *fan-out*): cuando una fila de la tabla izquierda se empareja con varias de la derecha y por eso se repite en el resultado.
- **Doble conteo**: sumar o contar un dato de nivel «uno» (por ejemplo, una meta o un total de cabecera) sobre filas que se repitieron por el JOIN.
- **Agregar antes de unir**: reducir primero una de las tablas a la granularidad de la otra (con `GROUP BY`) y recién entonces unir.
- **Control de filas**: comparar el número de filas antes y después de unir, y el total antes y después.

## Ejemplo paso a paso

**1. El caso inofensivo: sumar un dato del detalle.** Unir ventas con sus líneas repite cada venta una vez por línea. Eso **no** es un problema cuando sumas un dato que vive en cada línea:

```sql
SELECT COUNT(*) AS filas_unidas, SUM(l.cantidad * l.precio_unitario) AS importe_bs
FROM ventas AS v
INNER JOIN venta_lineas AS l ON l.venta_id = v.venta_id
WHERE v.estado = 'entregado';
```

```resultado
filas_unidas | importe_bs
36 | 2332.5
```

Hay una fila por línea (no por venta) y el importe es correcto, porque `cantidad * precio_unitario` pertenece a cada línea.

**2. El caso peligroso: contar ventas.** Con las mismas filas, `COUNT(*)` ya no cuenta ventas:

```sql
SELECT COUNT(*) AS conteo_erroneo, COUNT(DISTINCT v.venta_id) AS ventas_reales
FROM ventas AS v
INNER JOIN venta_lineas AS l ON l.venta_id = v.venta_id
WHERE v.estado = 'entregado';
```

```resultado
conteo_erroneo | ventas_reales
36 | 14
```

`COUNT(*)` cuenta líneas (como cada venta se repite por línea) y da bastante más que las ventas reales. `COUNT(DISTINCT v.venta_id)` cuenta cada venta una sola vez. **Cuenta siempre la clave de lo que quieres contar, con `DISTINCT` si hay un JOIN al detalle.**

**3. El caso grave: sumar un dato de nivel «uno».** La tabla `metas` tiene la meta en Bs de cada ruta y mes. Meta de septiembre de 2026 por ruta, sin unir nada:

```sql
SELECT ruta, SUM(meta_bs) AS meta_bs
FROM metas
WHERE mes = '2026-09'
GROUP BY ruta
ORDER BY ruta;
```

```resultado
ruta | meta_bs
R01 | 600.0
R02 | 450.0
R03 | 300.0
```

Ahora unimos las metas a las tiendas por ruta, pensando en «ver la meta junto a cada tienda», y sumamos:

```sql
SELECT t.ruta, SUM(m.meta_bs) AS meta_inflada
FROM tiendas AS t
INNER JOIN metas AS m ON m.ruta = t.ruta
WHERE m.mes = '2026-09'
GROUP BY t.ruta
ORDER BY t.ruta;
```

```resultado
ruta | meta_inflada
R01 | 2400.0
R02 | 1800.0
R03 | 1200.0
```

La meta de cada ruta se multiplicó por 4, porque cada ruta tiene 4 tiendas y la meta (un dato por ruta) se repitió en cada una. **Nadie recibió error.** Las cifras son cuatro veces más grandes y, de no haber hecho el control contra la consulta anterior, habrías reportado metas imposibles. Fíjate en la causa: se unió por `ruta`, que en `tiendas` **no es única** (se repite 4 veces). La relación no es 1:1 sino 1:N.

**4. La solución: agregar antes de unir.** Si necesitas comparar ventas con metas, reduce ambas tablas a la misma granularidad (ruta y mes) y recién entonces únelas:

```sql
SELECT m.ruta, m.meta_bs, ROUND(v.importe_bs, 2) AS vendido_bs
FROM metas AS m
INNER JOIN (
    SELECT t.ruta, SUM(l.cantidad * l.precio_unitario) AS importe_bs
    FROM venta_lineas AS l
    INNER JOIN ventas AS vv ON vv.venta_id = l.venta_id
    INNER JOIN tiendas AS t ON t.tienda_id = vv.tienda_id
    WHERE vv.estado = 'entregado' AND vv.fecha BETWEEN '2026-09-01' AND '2026-09-30'
    GROUP BY t.ruta
) AS v ON v.ruta = m.ruta
WHERE m.mes = '2026-09'
ORDER BY m.ruta;
```

```resultado
ruta | meta_bs | vendido_bs
R01 | 600.0 | 800.0
R02 | 450.0 | 379.0
R03 | 300.0 | 160.0
```

Esta consulta usa una **subconsulta** en el `FROM` (un resultado que se usa como si fuera una tabla); la explicaremos en el capítulo 4. Lo que debes ver ahora es la idea: la subconsulta deja **una fila por ruta**, igual que `metas` para un mes, y por eso la unión es 1:1 y no multiplica nada.

**5. Una clave que se repite.** Otro caso: unir tiendas con vendedores por ruta, porque «cada ruta tiene un vendedor»:

```sql
SELECT COUNT(*) AS filas_tras_unir
FROM tiendas AS t
INNER JOIN vendedores_ej AS vd ON vd.ruta = t.ruta;
```

```resultado
filas_tras_unir
16
```

Hay 12 tiendas, pero salen 16 filas: la ruta R01 tiene dos vendedores (Ana y Pedro) y cada tienda de R01 se repite dos veces. La suposición «una ruta, un vendedor» era falsa y el JOIN no avisó.

**Los tres controles antes de entregar** (cámbialos a rutina):

1. **Filas antes y después**: ¿la unión conserva el número de filas esperado? Si unes por una clave que es única en un lado, el número debe coincidir con el del otro lado.
2. **Claves huérfanas**: con `LEFT JOIN … IS NULL` busca filas que no encontraron pareja; no pierdas registros en silencio.
3. **Un total conocido**: compara el total de la consulta con el total calculado por otro camino (sin la unión). Si difieren, hay duplicación o pérdida.

Y dos prohibiciones: no unas por nombres de negocio (pueden repetirse, tener espacios o cambiar), y **no uses `DISTINCT` para ocultar un JOIN incorrecto**: primero explica por qué aparecen duplicados.

Ejemplo comercial: «ventas contra presupuesto por ruta y mes» es el caso 3-4. Si unes el presupuesto al detalle de ventas y sumas, multiplicas el presupuesto por el número de líneas de venta. La regla se repite en Pandas (`merge`), Excel (`BUSCARV`) y Power BI (relaciones).

## Errores comunes

- **Unir por una columna que no es única** (ruta, categoría, nombre).
- **Sumar un dato de nivel superior** (meta, total de cabecera, saldo) después de unir con el detalle.
- **Usar `COUNT(*)`** después de unir con un detalle para contar entidades.
- **Esconder duplicados con `DISTINCT`** sin entender su causa.
- **No comparar con un total independiente.**
- **Suponer 1:1 cuando la relación es 1:N** o N:M.

## Para comprobar que entendiste

1. ¿Por qué se multiplicó la meta por 4?
2. ¿Cuándo es correcto sumar `cantidad * precio_unitario` tras unir ventas con líneas?
3. ¿Qué cuenta `COUNT(DISTINCT v.venta_id)` frente a `COUNT(*)` después del JOIN?
4. ¿Cómo evitas el doble conteo al combinar ventas con metas?

<details><summary>Respuestas</summary>

1. Porque se unió por `ruta`, que se repite 4 veces en `tiendas`, y la meta (un dato por ruta) se repitió en cada tienda.
2. Siempre que ese importe pertenezca a cada línea (es un dato de la línea) y no repitas líneas.
3. El primero cuenta ventas distintas; el segundo, filas del resultado (líneas).
4. Agregando ventas por ruta y mes primero, y uniendo dos tablas con la misma granularidad.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Une `ventas` con `venta_lineas` y calcula cuántas ventas entregadas tienen más de 2 líneas (usa `GROUP BY` y `HAVING`).
2. Un compañero sumó `metas.meta_bs` después de unir `metas` con `tiendas` por `ruta` **para el mes de agosto** y obtuvo una cifra enorme. Sin ejecutar nada, explica cuál es el factor de multiplicación por ruta y por qué.
3. Escribe una consulta de control que compare el total de `venta_lineas` entregado calculado (a) sin unir tiendas y (b) uniendo con tiendas, y verifica que coinciden.

Cómo saber que está bien: en la 2 el factor es 4 (tiendas por ruta); en la 3 los dos totales son iguales.

<details><summary>Comprobación de la consulta 1</summary>

```sql
SELECT v.venta_id, COUNT(*) AS lineas
FROM ventas AS v
INNER JOIN venta_lineas AS l ON l.venta_id = v.venta_id
WHERE v.estado = 'entregado'
GROUP BY v.venta_id
HAVING COUNT(*) > 2
ORDER BY v.venta_id;
```

```resultado
venta_id | lineas
1 | 3
3 | 3
5 | 3
7 | 3
8 | 3
10 | 3
14 | 3
16 | 3
```

</details>

## Después, en los ejercicios

Las series J y E de [SQL](../../03_EJERCICIOS/SQL/INDICE.md), y los casos con presupuesto o metas, exigen estos controles. En el proyecto SQL deja por escrito la cardinalidad de cada unión y el control de totales que hiciste.

Siguiente capítulo: [4.1 Subconsultas](../04_SQL_CTE_ventanas/01_subconsultas.md).
