# 2.1 Funciones de agregación: contar, sumar, promediar

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: capítulo 1, en especial [1.4 NULL](../01_SQL_basico/04_null.md).

## Para qué sirve

Hasta ahora cada consulta devolvía filas de la tabla. Pero el gerente no pregunta "dame las 39 líneas de venta"; pregunta "¿cuánto vendimos?", "¿cuántas tiendas tenemos?", "¿cuál es el artículo más caro?". Esas preguntas se responden **resumiendo muchas filas en una sola cifra** con las funciones de agregación.

## Términos nuevos

- **Función de agregación**: una función que toma muchas filas y devuelve un solo valor. Las cinco básicas son `COUNT`, `SUM`, `AVG`, `MIN` y `MAX`.
- **COUNT(\*)**: cuenta filas, sin mirar sus valores.
- **COUNT(columna)**: cuenta las filas donde esa columna **no es NULL**.
- **COUNT(DISTINCT columna)**: cuenta los valores diferentes de la columna, sin repetir.
- **SUM(columna)**: suma los valores. Ignora los NULL.
- **AVG(columna)**: promedio = suma de los valores / cantidad de valores que **no son NULL**.
- **MIN / MAX**: menor y mayor valor. Funcionan con números, con texto (orden alfabético) y con fechas en formato `AAAA-MM-DD` (más antigua y más reciente).
- **Conjunto de filas**: las filas sobre las cuales actúa la función. Primero `WHERE` filtra y después la función resume lo que quedó.

## Ejemplo paso a paso

**1. Contar filas.** ¿Cuántas tiendas tenemos registradas?

```sql
SELECT COUNT(*) AS tiendas FROM tiendas;
```

```resultado
tiendas
12
```

Una sola fila con una sola cifra. `COUNT(*)` cuenta cada fila una vez, sin importar si tiene valores vacíos.

**2. COUNT(*) frente a COUNT(columna).** La columna `zona` tiene valores NULL. Mira la diferencia:

```sql
SELECT COUNT(*) AS filas, COUNT(zona) AS con_zona, COUNT(DISTINCT zona) AS zonas_distintas FROM tiendas;
```

```resultado
filas | con_zona | zonas_distintas
12 | 10 | 4
```

- `COUNT(*)` cuenta las 12 filas.
- `COUNT(zona)` cuenta solo las que **tienen** zona: 10 (las 2 NULL no entran).
- `COUNT(DISTINCT zona)` cuenta valores distintos no vacíos: Norte, Centro, Equipetrol y Plan 3000 son 4. Los NULL tampoco se cuentan.

Si alguien te pide "el número de tiendas", `COUNT(*)` es lo correcto aquí. Si pide "las tiendas con zona asignada", es `COUNT(zona)`. La palabra exacta del pedido decide la función.

**3. Sumar.** El importe de las líneas de la venta 7:

```sql
SELECT SUM(cantidad) AS unidades, SUM(cantidad * precio_unitario) AS importe_bs
FROM venta_lineas
WHERE venta_id = 7;
```

```resultado
unidades | importe_bs
38 | 288.0
```

Primero `WHERE` deja solo las tres líneas de la venta 7; luego `SUM` suma la columna `cantidad` y la columna calculada `cantidad * precio_unitario`. A mano: 12 + 6 + 20 = 38 unidades; 96 + 72 + 120 = Bs 288.

**4. Promedio, mínimo y máximo.**

```sql
SELECT AVG(precio) AS precio_promedio, MIN(precio) AS mas_barato, MAX(precio) AS mas_caro
FROM articulos;
```

```resultado
precio_promedio | mas_barato | mas_caro
8.1 | 3.5 | 14.0
```

Los diez precios suman 81 y 81 / 10 = 8,10. Con fechas, `MIN` y `MAX` dan el primer y el último día:

```sql
SELECT MIN(fecha) AS primera_venta, MAX(fecha) AS ultima_venta FROM ventas;
```

```resultado
primera_venta | ultima_venta
2026-08-03 | 2026-09-29
```

**5. El promedio ignora los NULL.** Para verlo con un ejemplo mínimo, construimos una tabla temporal de tres filas, una con valor vacío:

```sql
CREATE TEMP TABLE prueba (id INTEGER, valor REAL);
INSERT INTO prueba VALUES (1, 10), (2, 20), (3, NULL);
SELECT COUNT(*) AS filas, COUNT(valor) AS con_valor, SUM(valor) AS suma, AVG(valor) AS promedio FROM prueba;
```

```resultado
filas | con_valor | suma | promedio
3 | 2 | 30.0 | 15.0
```

El promedio es 15 y no 10: AVG hizo (10 + 20) / **2**, no / 3. Si en tu negocio el NULL significa "cero", el resultado correcto sería 10. Es una decisión de negocio: nunca la tomes en silencio. (La tabla temporal desaparece al cerrar la conexión y no toca tu base.)

**6. Un conjunto vacío.** Si `WHERE` no deja ninguna fila:

```sql
SELECT COUNT(*) AS filas, SUM(cantidad) AS suma, AVG(cantidad) AS promedio
FROM venta_lineas
WHERE venta_id = 999;
```

```resultado
filas | suma | promedio
0 | NULL | NULL
```

`COUNT` da 0, pero `SUM` y `AVG` dan NULL, no 0. Un reporte que muestra un vacío donde esperabas 0 suele venir de aquí.

**7. Dos funciones en una consulta con filtro.** Unidades y líneas de las ventas de la tienda 1:

```sql
SELECT COUNT(*) AS lineas, SUM(cantidad) AS unidades
FROM venta_lineas
WHERE venta_id IN (1, 5, 14);
```

```resultado
lineas | unidades
9 | 77
```

Ejemplo comercial: el jefe de ventas pide "cuántas ventas entregó el vendedor 2 y cuál fue la más reciente". `COUNT(*)` y `MAX(fecha)` en la misma consulta, con `WHERE vendedor_id = 2 AND estado = 'entregado'`.

## Errores comunes

- **Usar `COUNT(columna)` cuando querías contar filas**: los NULL desaparecen del conteo y el total no cuadra.
- **Creer que `AVG` cuenta los vacíos como cero**: no los cuenta.
- **Sumar el detalle cuando la pregunta es por venta**: `SUM(cantidad)` sobre `venta_lineas` cuenta unidades, no ventas.
- **Olvidar el filtro de estado**: sumar también las ventas anuladas infla los totales.
- **Mezclar una función de agregación con una columna normal sin `GROUP BY`**: SQLite no avisa y devuelve una fila cualquiera junto al resultado; otras bases de datos dan error. Evita escribirlo; la solución es `GROUP BY` (siguiente lección).
- **Esperar `0` donde sale NULL** en `SUM` o `AVG` de un conjunto vacío.
- **Redondear en el medio de un cálculo**: aplica `ROUND` solo al presentar (lección 2.4).

## Para comprobar que entendiste

1. ¿Por qué `COUNT(zona)` da 10 y `COUNT(*)` da 12?
2. En la tabla temporal `prueba`, ¿por qué el promedio es 15?
3. ¿Qué devuelve `SUM` si ninguna fila cumple el `WHERE`?
4. ¿Qué diferencia hay entre `COUNT(zona)` y `COUNT(DISTINCT zona)`?

<details><summary>Respuestas</summary>

1. `COUNT(*)` cuenta filas; `COUNT(zona)` solo las filas con zona no NULL.
2. Porque AVG divide entre los valores no NULL (2), no entre las 3 filas.
3. NULL.
4. El primero cuenta todas las filas con zona (con repetidas); el segundo, los valores diferentes.

</details>

<a id="micropractica"></a>

## Micropráctica

Sobre la mini-base escribe:

1. Cuántos artículos hay en total y cuál es el precio promedio de los de la categoría Bebidas.
2. El importe total en Bs de las líneas de las ventas 1, 2 y 3.
3. Cuántas visitas hay en `visitas_ej` y la fecha de la primera y de la última.
4. Cuántas ventas están en estado `anulado`.

Cómo saber que está bien: 1 → 10 artículos y un promedio de Bebidas de unos 8,83 (se redondea en la lección 2.4); 2 → antes de ejecutar, suma a mano el importe de la venta 1 (60 + 45 + 32 = 137) y comprueba que tu consulta, filtrando solo la venta 1, da lo mismo; 3 → 14 visitas; 4 → 2 ventas.

<details><summary>Comprobación</summary>

```sql
SELECT SUM(cantidad * precio_unitario) AS importe_bs FROM venta_lineas WHERE venta_id IN (1, 2, 3);
```

```resultado
importe_bs
414.0
```

```sql
SELECT COUNT(*) AS visitas, MIN(fecha) AS primera, MAX(fecha) AS ultima FROM visitas_ej;
```

```resultado
visitas | primera | ultima
14 | 2026-09-01 | 2026-09-05
```

</details>

## Después, en los ejercicios

La serie G de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) (G1–G8) y N2 empiezan aquí. Antes de cada una, escribe qué cuenta o suma cada columna del resultado y en qué unidad.

Siguiente: [2.2 GROUP BY y HAVING](02_group_by_having.md).
