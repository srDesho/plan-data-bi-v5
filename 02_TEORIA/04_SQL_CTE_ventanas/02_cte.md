# 4.2 CTE: dividir una consulta larga en pasos con nombre

> Tiempo estimado: 45 min (lectura 15 + práctica 30). Prerrequisito: [4.1 Subconsultas](01_subconsultas.md).

## Para qué sirve

Una consulta con tres subconsultas anidadas es difícil de leer, de revisar y de corregir. Una **CTE** te deja escribir cada paso con un nombre propio, de arriba hacia abajo, como lo explicarías en voz alta: «primero el importe por venta, luego el importe por ruta, luego lo comparo con la meta». Es la herramienta para volver legibles los cálculos de varios pasos.

## Términos nuevos

- **CTE** (*Common Table Expression*, expresión de tabla común): un resultado con nombre, definido con `WITH nombre AS (SELECT ...)`, que existe **solo durante esa consulta** y que puedes usar como si fuera una tabla.
- **WITH**: la palabra que abre la lista de CTE al comienzo de la consulta.
- **Paso**: cada CTE de la lista. Se separan con comas y cada una puede usar las anteriores.
- **Legibilidad**: que otra persona (o tú dentro de un mes) pueda entender la consulta sin adivinar.

## Ejemplo paso a paso

**1. El ticket promedio con una CTE.** Es la misma pregunta de 4.1 (promedio por venta), ahora en dos pasos con nombre:

```sql
WITH por_venta AS (
    SELECT venta_id, SUM(cantidad * precio_unitario) AS importe_venta
    FROM venta_lineas
    GROUP BY venta_id
)
SELECT COUNT(*) AS ventas, ROUND(AVG(importe_venta), 2) AS ticket_promedio_bs
FROM por_venta;
```

```resultado
ventas | ticket_promedio_bs
16 | 170.09
```

Cómo se lee:

1. `WITH por_venta AS ( ... )` define un resultado llamado `por_venta`: una fila por venta con su importe.
2. El `SELECT` final usa `por_venta` como si fuera una tabla.
3. Es el mismo resultado que con la subconsulta en `FROM`, pero ahora el nombre `por_venta` dice qué es.

Una CTE **no es una tabla guardada** ni hace la consulta más rápida automáticamente: es una forma de organizar. Desaparece cuando termina la consulta.

**2. Varias CTE encadenadas.** Queremos, por ruta, el importe vendido y su peso sobre el total entregado:

```sql
WITH importe_entregado AS (
    SELECT v.tienda_id, SUM(l.cantidad * l.precio_unitario) AS importe
    FROM venta_lineas AS l
    INNER JOIN ventas AS v ON v.venta_id = l.venta_id
    WHERE v.estado = 'entregado'
    GROUP BY v.tienda_id
),
por_ruta AS (
    SELECT t.ruta, SUM(i.importe) AS importe_bs
    FROM importe_entregado AS i
    INNER JOIN tiendas AS t ON t.tienda_id = i.tienda_id
    GROUP BY t.ruta
)
SELECT ruta,
       importe_bs,
       ROUND(100.0 * importe_bs / (SELECT SUM(importe_bs) FROM por_ruta), 1) AS pct_del_total
FROM por_ruta
ORDER BY ruta;
```

```resultado
ruta | importe_bs | pct_del_total
R01 | 1265.0 | 54.2
R02 | 510.0 | 21.9
R03 | 557.5 | 23.9
```

Tres pasos, cada uno con un nombre y una sola idea:

1. `importe_entregado`: una fila por tienda con lo vendido (solo ventas entregadas).
2. `por_ruta`: sube de tienda a ruta (une con `tiendas` y suma).
3. El `SELECT` final divide el importe de cada ruta entre el total (una subconsulta escalar sobre `por_ruta`).

Control: los porcentajes suman 100 (con redondeo, 100,0 o muy cerca), y los importes coinciden con los de la lección 3.2 (R01 1265, R02 510, R03 557,5). **Cada paso se puede ejecutar por separado para revisarlo**: es la gran ventaja para depurar.

**3. Usar la misma CTE dos veces.** Una subconsulta tendría que repetirse; la CTE se escribe una vez. Ventas que superan el ticket promedio:

```sql
WITH por_venta AS (
    SELECT venta_id, SUM(cantidad * precio_unitario) AS importe_venta
    FROM venta_lineas
    GROUP BY venta_id
)
SELECT venta_id, importe_venta
FROM por_venta
WHERE importe_venta > (SELECT AVG(importe_venta) FROM por_venta)
ORDER BY importe_venta DESC, venta_id;
```

```resultado
venta_id | importe_venta
4 | 320.0
7 | 288.0
14 | 225.0
10 | 220.0
8 | 202.0
5 | 182.0
```

`por_venta` aparece dos veces: una para listar y otra para calcular el promedio.

**4. Depurar por pasos.** Cuando un resultado no cuadre, no leas toda la consulta de golpe. Cambia temporalmente el `SELECT` final por `SELECT * FROM paso_intermedio;` y verifica ese paso. Si el paso 1 está bien, pasa al 2.

Ejemplo comercial: el cálculo «ventas contra presupuesto por ruta» se plantea con dos CTE (ventas por ruta y mes; presupuesto por ruta y mes) y un `JOIN` final entre ellas, con la misma granularidad. Eso evita la duplicación de 3.4 y deja el razonamiento a la vista.

## Errores comunes

- **Creer que la CTE guarda los datos** o los acelera siempre: es solo un nombre dentro de una consulta.
- **Olvidar la coma entre CTE** o ponerla después de la última.
- **Darles nombres vagos** (`t1`, `tmp`): pierde el sentido de las CTE.
- **Un paso que hace demasiado**: si una CTE tiene tres joins y dos agrupaciones, divídela.
- **No revisar cada paso por separado.**
- **Pensar que una CTE se puede usar en otra consulta aparte**: solo vive dentro de su propio `WITH ... SELECT`.

## Para comprobar que entendiste

1. ¿Qué es una CTE y cuánto tiempo existe?
2. ¿Cómo se separan dos CTE en la misma consulta?
3. ¿Qué ventaja tiene sobre una subconsulta en `FROM` cuando necesitas el mismo resultado dos veces?
4. ¿Cómo depuras una consulta con tres CTE?

<details><summary>Respuestas</summary>

1. Un resultado con nombre definido con `WITH`; existe solo durante esa consulta.
2. Con una coma; la última no lleva coma.
3. Se escribe una vez y se usa dos veces.
4. Ejecutando un `SELECT *` de cada paso por separado.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Reescribe con una CTE: «unidades totales por tienda de ventas entregadas, y la tienda con más unidades» (primero la CTE de unidades por tienda; luego el `SELECT` que ordena y toma 1).
2. Con dos CTE: visitas realizadas por tienda (`visitas_ej`) y ventas entregadas por tienda (`ventas`), unidas con LEFT JOIN desde `tiendas` para ver las 12 tiendas con ambas cifras (0 donde no haya datos). Usa `COALESCE`.

Cómo saber que está bien: en la 1, la tienda con más unidades es la 1 (77 unidades); en la 2 aparecen las 12 tiendas y ninguna cifra es NULL.

<details><summary>Comprobación de la consulta 1</summary>

```sql
WITH unidades_tienda AS (
    SELECT v.tienda_id, SUM(l.cantidad) AS unidades
    FROM venta_lineas AS l
    INNER JOIN ventas AS v ON v.venta_id = l.venta_id
    WHERE v.estado = 'entregado'
    GROUP BY v.tienda_id
)
SELECT tienda_id, unidades
FROM unidades_tienda
ORDER BY unidades DESC, tienda_id
LIMIT 1;
```

```resultado
tienda_id | unidades
1 | 77
```

</details>

## Después, en los ejercicios

Las series K, V y X de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) combinan varios pasos. Si tu consulta ya tiene dos niveles de subconsulta, pásala a CTE antes de depurarla.

Siguiente: [4.3 Funciones de ventana](03_ventanas.md).
