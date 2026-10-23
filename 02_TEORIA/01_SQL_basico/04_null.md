# 1.4 NULL: cuando falta el dato

> Tiempo estimado: 40 min (lectura 15 + práctica 25). Prerrequisito: [1.3 WHERE y operadores](03_where_operadores.md).

## Para qué sirve

En los datos reales hay campos vacíos: una tienda sin zona, un pedido sin fecha de entrega. SQL los marca con `NULL`. Si no entiendes cómo se comporta, tus filtros dejan filas fuera sin avisar y tus conteos no cuadran. Esta lección enseña a detectar, filtrar y razonar con datos faltantes.

## Términos nuevos

- **NULL** (ya lo conoces): marca de "dato desconocido o no registrado". No es 0 ni `''`.
- **IS NULL / IS NOT NULL**: la forma correcta de preguntar si un valor falta o no falta. Es el único modo de detectar NULL.
- **Lógica de tres valores**: en SQL una condición puede ser verdadera, falsa o **desconocida**. Comparar cualquier cosa con NULL (`zona = 'Norte'` cuando `zona` es NULL) da *desconocido*, y `WHERE` solo deja pasar las filas **verdaderas**.
- **Dato faltante**: un NULL u otro valor que significa "falta" (como texto vacío). Detectarlos es parte de la calidad de datos.

## Ejemplo paso a paso

Recordemos que en `tiendas` las tiendas 5 y 8 tienen la zona vacía.

**1. Mirar los NULL.**

```sql
SELECT tienda_id, nombre, zona FROM tiendas WHERE zona IS NULL;
```

```resultado
tienda_id | nombre | zona
5 |   Kiosco La Esquina  | NULL
8 | Farmacia Vida | NULL
```

`IS NULL` devuelve las filas donde `zona` falta. Y su opuesto, `IS NOT NULL`, las que sí la tienen.

**2. El error clásico: `= NULL`.**

```sql
SELECT tienda_id, nombre FROM tiendas WHERE zona = NULL;
```

```resultado
tienda_id | nombre
```

Resultado vacío. La razón: `zona = NULL` pregunta "¿es igual a algo desconocido?" y la respuesta es *desconocido*, no verdadero. Nunca escribas `= NULL` ni `<> NULL`.

**3. El filtro que pierde filas.** Queremos las tiendas "que no son del Norte":

```sql
SELECT tienda_id, nombre, zona FROM tiendas WHERE zona <> 'Norte';
```

```resultado
tienda_id | nombre | zona
2 | Kiosco El Faro | Centro
3 | Farmacia Salud | Centro
6 | Restaurante Sabor | Equipetrol
7 | Tienda Don Pepe | Plan 3000
9 | Minimarket Central | Centro
11 | Tienda Nueva Esperanza | Plan 3000
12 | Restaurante El Buen Gusto | Centro
```

Mira: faltan las tiendas 5 y 8. Para SQL, una zona desconocida no es "distinta de Norte", es *desconocida*, así que la fila queda fuera. Si el gerente preguntó por las tiendas fuera del Norte, probablemente quería esas dos también. Corrección explícita:

```sql
SELECT tienda_id, nombre, zona FROM tiendas WHERE zona <> 'Norte' OR zona IS NULL;
```

```resultado
tienda_id | nombre | zona
2 | Kiosco El Faro | Centro
3 | Farmacia Salud | Centro
5 |   Kiosco La Esquina  | NULL
6 | Restaurante Sabor | Equipetrol
7 | Tienda Don Pepe | Plan 3000
8 | Farmacia Vida | NULL
9 | Minimarket Central | Centro
11 | Tienda Nueva Esperanza | Plan 3000
12 | Restaurante El Buen Gusto | Centro
```

Ahora aparecen 9 tiendas: las 7 con otra zona más las 2 sin zona. Decidir si las tiendas sin zona van o no es una **decisión de negocio** que debes anotar, no un detalle técnico.

**4. NULL en cálculos.** Cualquier operación con NULL da NULL:

```sql
SELECT 10 + NULL AS suma, 10 * 2 AS producto;
```

```resultado
suma | producto
NULL | 20
```

Por eso un cálculo sobre una columna con vacíos puede devolver vacíos. En la lección de agregados verás que `SUM`, `AVG` y `COUNT(columna)` simplemente ignoran los NULL.

**5. NULL no es texto vacío.** Distingue:

```sql
SELECT '' IS NULL AS vacio_es_null, NULL IS NULL AS null_es_null;
```

```resultado
vacio_es_null | null_es_null
0 | 1
```

Un `0` en SQLite significa falso y un `1` verdadero. El texto vacío **no** es NULL. Una columna puede traer ambos tipos de "falta": revisa los dos.

Ejemplo comercial: el reporte de ventas por zona deja fuera dos tiendas sin zona. Si tu total no cuadra con el total de ventas, la causa más común es esta: las ventas de esas tiendas existen pero no tienen zona a la cual asignarse. Una forma de resolverlo es crear una categoría explícita "Sin zona" (lo harás con `COALESCE`, en la lección 2.5), en vez de perder las filas.

## Errores comunes

- **`= NULL` o `<> NULL`**: no devuelve nada. Usa `IS NULL` / `IS NOT NULL`.
- **Filtros de exclusión que botan los NULL**: `zona <> 'Norte'` pierde las zonas vacías.
- **Creer que NULL es cero**: un promedio que ignora NULL no es lo mismo que uno que cuenta ceros.
- **No contar los NULL antes de entregar**: ante un total que no cuadra, revisa primero los datos faltantes.
- **Rellenar NULL con un número sin avisar**: cambia el significado (ver 2.5).

## Para comprobar que entendiste

1. ¿Por qué `WHERE zona = NULL` no devuelve filas?
2. ¿Qué filas pierde `WHERE zona <> 'Norte'`?
3. ¿Cuánto da `5 + NULL`?
4. ¿El texto vacío es NULL?

<details><summary>Respuestas</summary>

1. Porque comparar con NULL da *desconocido*, y WHERE solo acepta verdadero.
2. Las que tienen la zona NULL.
3. NULL.
4. No.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Lista las tiendas con zona conocida (`IS NOT NULL`) de la ruta R03.
2. Escribe la consulta de las tiendas "que no son del Centro" **sin perder** las de zona desconocida.
3. En una frase, explica a un compañero por qué `zona = NULL` no sirve.

Cómo saber que está bien: la 1 devuelve 3 tiendas; la 2 devuelve 8 tiendas (todas menos las 4 del Centro).

<details><summary>Comprobación de la consulta 1</summary>

```sql
SELECT tienda_id, nombre, zona FROM tiendas WHERE zona IS NOT NULL AND ruta = 'R03';
```

```resultado
tienda_id | nombre | zona
6 | Restaurante Sabor | Equipetrol
9 | Minimarket Central | Centro
11 | Tienda Nueva Esperanza | Plan 3000
```

</details>

## Después, en los ejercicios

En la serie S de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) y en los siguientes bloques volverás a encontrar datos faltantes. Cuando un total no cuadre, pregúntate: ¿hay NULL en alguna columna que uso para filtrar o agrupar?

Siguiente: [1.5 ORDER BY y LIMIT](05_order_limit.md).
