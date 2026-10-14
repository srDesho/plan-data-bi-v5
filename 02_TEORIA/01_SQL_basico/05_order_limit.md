# 1.5 ORDER BY y LIMIT: ordenar y recortar

> Tiempo estimado: 40 min (lectura 15 + práctica 25). Prerrequisito: [1.3 WHERE y operadores](03_where_operadores.md).

## Para qué sirve

"Los 5 clientes con más ventas", "los artículos más caros", "las últimas 3 ventas". Todas son combinaciones de **ordenar** y **recortar**. Si ordenas mal, o si hay empates y no los resuelves, el "Top 5" que entregas puede cambiar de una ejecución a otra.

## Términos nuevos

- **ORDER BY**: cláusula que ordena las filas del resultado según una o más columnas.
- **ASC / DESC**: ascendente (de menor a mayor, de A a Z, de la fecha más antigua a la más nueva; es el valor por defecto) y descendente (lo contrario).
- **Criterio de desempate**: una segunda (o tercera) columna en el `ORDER BY` que decide el orden cuando la primera tiene valores iguales.
- **LIMIT n**: devuelve solo las primeras `n` filas del resultado ya ordenado.
- **OFFSET k**: salta las primeras `k` filas antes de aplicar el `LIMIT` (sirve para paginar).
- **Top N**: patrón "ordenar de mayor a menor y recortar a las N primeras filas".

## Ejemplo paso a paso

**1. Orden ascendente (por defecto).**

```sql
SELECT nombre, precio FROM articulos ORDER BY precio LIMIT 4;
```

```resultado
nombre | precio
Jabón | 3.5
Galletas | 4.5
Maní 80g | 5.0
Agua 2L | 6.0
```

Sin indicar nada, `ORDER BY precio` es de menor a mayor. Los cuatro más baratos aparecen primero porque además usamos `LIMIT 4`.

**2. Orden descendente: el Top 3 más caro.**

```sql
SELECT nombre, precio FROM articulos ORDER BY precio DESC LIMIT 3;
```

```resultado
nombre | precio
Detergente 1kg | 14.0
Yogurt 1L | 12.0
Gaseosa 2L | 11.5
```

El orden de las cláusulas importa: primero se ordena (`ORDER BY`) y recién después se recorta (`LIMIT`). `ORDER BY` va casi al final de la consulta y `LIMIT` al final de todo.

**3. Dos criterios.** Ordenar por categoría (A→Z) y, dentro de cada una, por precio de mayor a menor:

```sql
SELECT categoria, nombre, precio FROM articulos ORDER BY categoria, precio DESC;
```

```resultado
categoria | nombre | precio
Bebidas | Gaseosa 2L | 11.5
Bebidas | Jugo 1L | 9.0
Bebidas | Agua 2L | 6.0
Limpieza | Detergente 1kg | 14.0
Limpieza | Jabón | 3.5
Lácteos | Yogurt 1L | 12.0
Lácteos | Leche 1L | 8.0
Snacks | Papas 100g | 7.5
Snacks | Maní 80g | 5.0
Snacks | Galletas | 4.5
```

Se lee de izquierda a derecha: primero se ordena por la primera columna; solo cuando hay empate se usa la segunda. Cada columna lleva su propio `ASC`/`DESC`.

**4. El problema de los empates.** Mira las 5 líneas de venta con más unidades:

```sql
SELECT linea_id, venta_id, cantidad FROM venta_lineas ORDER BY cantidad DESC LIMIT 5;
```

```resultado
linea_id | venta_id | cantidad
9 | 4 | 20
18 | 7 | 20
27 | 11 | 20
32 | 14 | 18
10 | 4 | 15
```

Varias líneas tienen la misma cantidad (por ejemplo, 20): ¿cuál queda cuarta o quinta? SQL no lo garantiza. En esta base los dos resultados de este ejemplo salen iguales, pero solo el segundo está garantizado: el primero depende de cómo el motor recorra la tabla y puede cambiar si alguien añade un índice o cambia de versión. La solución es agregar un desempate único al final:

```sql
SELECT linea_id, venta_id, cantidad FROM venta_lineas ORDER BY cantidad DESC, linea_id LIMIT 5;
```

```resultado
linea_id | venta_id | cantidad
9 | 4 | 20
18 | 7 | 20
27 | 11 | 20
32 | 14 | 18
10 | 4 | 15
```

Con `linea_id` como último criterio, el orden queda totalmente determinado: a igual cantidad, primero la línea con menor `linea_id`. **Regla: todo Top N lleva un desempate único.**

**5. Paginar con OFFSET.** Artículos del 4.º al 6.º más baratos:

```sql
SELECT nombre, precio FROM articulos ORDER BY precio LIMIT 3 OFFSET 3;
```

```resultado
nombre | precio
Agua 2L | 6.0
Papas 100g | 7.5
Leche 1L | 8.0
```

`OFFSET 3` descarta las 3 primeras; `LIMIT 3` toma las 3 siguientes.

**6. Los NULL al ordenar.** En SQLite, con orden ascendente, los NULL salen **primero**:

```sql
SELECT tienda_id, zona FROM tiendas ORDER BY zona LIMIT 4;
```

```resultado
tienda_id | zona
5 | NULL
8 | NULL
2 | Centro
3 | Centro
```

Las tiendas 5 y 8 (sin zona) abren la lista. En otras bases de datos puede ser al revés, así que no supongas el orden de los NULL.

Ejemplo comercial: "las 3 ventas más recientes de la tienda 3" es `WHERE tienda_id = 3 ORDER BY fecha DESC, venta_id DESC LIMIT 3`. El `venta_id DESC` desempata dos ventas del mismo día.

## Errores comunes

- **Top N sin desempate**: el resultado "se mueve" entre ejecuciones y no puedes defenderlo.
- **Poner `LIMIT` esperando que ordene**: sin `ORDER BY`, `LIMIT 5` devuelve 5 filas cualquiera.
- **Ordenar texto que parece número**: `'10'` queda antes que `'9'` si la columna es TEXT. Revisa el tipo.
- **Olvidar `DESC`** en un "Top": devuelves los más pequeños.
- **Escribir el `ORDER BY` antes del `WHERE`**: el orden de las cláusulas es SELECT, FROM, WHERE, ORDER BY, LIMIT.

## Para comprobar que entendiste

1. ¿Qué pasa primero, el orden o el recorte?
2. ¿Para qué sirve el segundo criterio de `ORDER BY categoria, precio DESC`?
3. ¿Por qué un Top 5 con empates necesita un desempate?
4. ¿Dónde salen los NULL en SQLite al ordenar ascendente?

<details><summary>Respuestas</summary>

1. Primero se ordena y luego se recorta.
2. Ordena las filas que tienen la misma categoría.
3. Sin él, el motor puede devolver cualquiera de las filas empatadas.
4. Primero.

</details>

## Micropráctica

1. Los 2 artículos más baratos de la categoría Bebidas (nombre y precio).
2. Las 3 ventas más recientes que estén `entregado` (venta_id y fecha), con desempate por `venta_id DESC`.
3. Las 4 líneas con mayor `precio_unitario`, desempatadas por `linea_id`.

Cómo saber que está bien: la 1 empieza con Agua 2L; la 2 empieza con la venta 16; la 3 devuelve 4 filas y ninguna línea de precio 6,00.

<details><summary>Comprobación de la consulta 2</summary>

```sql
SELECT venta_id, fecha FROM ventas WHERE estado = 'entregado' ORDER BY fecha DESC, venta_id DESC LIMIT 3;
```

```resultado
venta_id | fecha
16 | 2026-09-29
15 | 2026-09-25
14 | 2026-09-22
```

</details>

## Después, en los ejercicios

Casi todos los enunciados con "primeros", "top" o "más recientes" de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) exigen un orden completo. Pregúntate siempre: ¿qué criterio resuelve el empate?

Siguiente: [1.6 DISTINCT y LIKE](06_distinct_like.md).
