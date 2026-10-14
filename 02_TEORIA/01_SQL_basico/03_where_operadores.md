# 1.3 WHERE: filtrar filas con operadores

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisito: [1.2 SELECT, FROM y alias](02_select_from_alias.md).

## Para qué sirve

`SELECT` decide qué *columnas* ves; `WHERE` decide qué *filas* entran al resultado. Casi toda pregunta de negocio filtra: "solo la ruta R01", "solo las ventas entregadas", "artículos de más de Bs 8", "ventas de septiembre". Un filtro mal escrito no da error: da un número equivocado que parece correcto.

## Términos nuevos

- **Condición**: una afirmación sobre una fila que resulta verdadera o falsa. La fila entra al resultado solo si es verdadera.
- **WHERE**: la cláusula que contiene la condición. Se escribe después de `FROM`.
- **Operador de comparación**: `=` (igual), `<>` o `!=` (distinto), `<` (menor), `>` (mayor), `<=` (menor o igual), `>=` (mayor o igual). En SQL se usa un solo `=` para comparar; no existe `==`.
- **Operador lógico**: `AND` (se cumplen las dos condiciones), `OR` (se cumple al menos una), `NOT` (invierte una condición).
- **IN**: pregunta si un valor está dentro de una lista: `ruta IN ('R01', 'R03')`.
- **BETWEEN**: pregunta si un valor está entre dos límites, **incluyendo ambos**: `precio BETWEEN 5 AND 9`.
- **Precedencia**: el orden en que SQL resuelve operadores cuando hay varios. `AND` se resuelve antes que `OR`; los paréntesis fuerzan el orden que tú quieres.

## Ejemplo paso a paso

**1. Una condición de igualdad.** Tiendas de la ruta R01:

```sql
SELECT tienda_id, nombre, ruta FROM tiendas WHERE ruta = 'R01';
```

```resultado
tienda_id | nombre | ruta
1 | Tienda La Palma | R01
2 | Kiosco El Faro | R01
7 | Tienda Don Pepe | R01
10 | Kiosco Luna | R01
```

SQL recorre las 12 filas de `tiendas`, evalúa `ruta = 'R01'` en cada una y se queda con las verdaderas. El texto va entre comillas simples y se distingue entre mayúsculas y minúsculas: `'r01'` no sería igual a `'R01'`.

**2. Comparar números.** Artículos que cuestan Bs 8 o más:

```sql
SELECT nombre, precio FROM articulos WHERE precio >= 8;
```

```resultado
nombre | precio
Jugo 1L | 9.0
Gaseosa 2L | 11.5
Detergente 1kg | 14.0
Leche 1L | 8.0
Yogurt 1L | 12.0
```

El 8 queda adentro porque usamos `>=`. Con `> 8` la Leche 1L (precio 8) desaparecería. Cuando cuentes o sumes, ese borde cambia el resultado.

**3. Dos condiciones con AND.** Ventas entregadas de la tienda 1:

```sql
SELECT venta_id, tienda_id, fecha, estado
FROM ventas
WHERE tienda_id = 1 AND estado = 'entregado';
```

```resultado
venta_id | tienda_id | fecha | estado
1 | 1 | 2026-08-03 | entregado
5 | 1 | 2026-08-19 | entregado
14 | 1 | 2026-09-22 | entregado
```

Con `AND` la fila debe cumplir **ambas**. Cada condición completa lleva su propia comparación completa: no se escribe `tienda_id = 1 AND estado = 'entregado'` como `tienda_id = 1 AND 'entregado'`.

**4. IN en vez de varios OR.**

```sql
SELECT nombre, categoria FROM articulos WHERE categoria IN ('Bebidas', 'Lácteos');
```

```resultado
nombre | categoria
Agua 2L | Bebidas
Jugo 1L | Bebidas
Gaseosa 2L | Bebidas
Leche 1L | Lácteos
Yogurt 1L | Lácteos
```

Equivale a `categoria = 'Bebidas' OR categoria = 'Lácteos'`, pero se lee mejor y evita errores.

**5. BETWEEN para rangos.** Ventas de la segunda quincena de septiembre:

```sql
SELECT venta_id, fecha FROM ventas WHERE fecha BETWEEN '2026-09-16' AND '2026-09-30';
```

```resultado
venta_id | fecha
13 | 2026-09-18
14 | 2026-09-22
15 | 2026-09-25
16 | 2026-09-29
```

Las fechas están guardadas como texto `AAAA-MM-DD`; ese formato se ordena igual que el calendario, por eso `BETWEEN` funciona. Ambos extremos están incluidos: la venta del 29 de septiembre entra; si el último día fuera `'2026-09-29'` también entraría.

**6. La trampa de AND y OR juntos.** Queremos artículos de Snacks o Bebidas que cuesten más de Bs 7. Compara:

```sql
SELECT nombre, categoria, precio
FROM articulos
WHERE categoria = 'Snacks' OR categoria = 'Bebidas' AND precio > 7;
```

```resultado
nombre | categoria | precio
Jugo 1L | Bebidas | 9.0
Gaseosa 2L | Bebidas | 11.5
Papas 100g | Snacks | 7.5
Galletas | Snacks | 4.5
Maní 80g | Snacks | 5.0
```

```sql
SELECT nombre, categoria, precio
FROM articulos
WHERE (categoria = 'Snacks' OR categoria = 'Bebidas') AND precio > 7;
```

```resultado
nombre | categoria | precio
Jugo 1L | Bebidas | 9.0
Gaseosa 2L | Bebidas | 11.5
Papas 100g | Snacks | 7.5
```

La primera consulta se resuelve como `Snacks OR (Bebidas AND precio > 7)`, porque `AND` va antes que `OR`: devuelve *todos* los snacks, incluso los baratos (Galletas Bs 4,50). La segunda, con paréntesis, aplica el precio a ambas categorías. La regla práctica: **si mezclas AND con OR, pon paréntesis siempre**, aunque creas que no hacen falta.

Ejemplo comercial: "entregas de las rutas R01 y R03 en septiembre" es `ruta IN (...) AND fecha BETWEEN ...`. Si olvidas que `anulado` también existe como estado, estás contando ventas que no ocurrieron: el estado también es un filtro.

## Errores comunes

- **Usar `==`** en lugar de `=`: da error de sintaxis en SQLite.
- **Comillas faltantes en texto**: `WHERE ruta = R01` busca una *columna* llamada R01 y falla con `no such column`.
- **Mayúsculas distintas**: `'norte'` no coincide con `'Norte'`. Comprueba cómo está escrito el dato.
- **Mezclar AND y OR sin paréntesis**: es el error silencioso más común. El resultado parece plausible pero trae filas de más.
- **Pensar que BETWEEN excluye los extremos**: los incluye.
- **Olvidar un filtro de negocio** (como el estado `anulado`): la consulta corre bien y cuenta ventas que se cancelaron.
- **Comparar con NULL usando `=`**: no funciona. Se explica en la próxima lección.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre `precio > 8` y `precio >= 8`?
2. ¿Por qué `WHERE ruta = R01` falla?
3. Escribe con `IN` la condición "categoría Limpieza o Lácteos".
4. ¿Cómo se resuelve `A OR B AND C`?

<details><summary>Respuestas</summary>

1. El segundo incluye los artículos que cuestan exactamente Bs 8.
2. Sin comillas, SQL cree que `R01` es el nombre de una columna.
3. `categoria IN ('Limpieza', 'Lácteos')`.
4. Como `A OR (B AND C)`: primero el AND.

</details>

## Micropráctica

Con la mini-base, escribe y ejecuta:

1. Las tiendas del tipo `'Kiosco'` (nombre y zona).
2. Los artículos de la categoría Snacks con precio menor a Bs 7 (nombre y precio).
3. Las ventas entregadas de las tiendas 3 o 9 (usa `IN` y paréntesis si hace falta).
4. Las líneas de venta de las ventas 1 a 3 con cantidad mayor a 5.

Cómo saber que está bien: la 1 devuelve 3 filas (una tiene espacios en el nombre, es normal); la 2 devuelve 2; la 3 devuelve 4; la 4 devuelve 6 líneas.

<details><summary>Comprobación de las consultas 2 y 3</summary>

```sql
SELECT nombre, precio FROM articulos WHERE categoria = 'Snacks' AND precio < 7;
```

```resultado
nombre | precio
Galletas | 4.5
Maní 80g | 5.0
```

```sql
SELECT venta_id, tienda_id, estado FROM ventas WHERE tienda_id IN (3, 9) AND estado = 'entregado';
```

```resultado
venta_id | tienda_id | estado
3 | 3 | entregado
9 | 3 | entregado
12 | 9 | entregado
16 | 3 | entregado
```

</details>

## Después, en los ejercicios

Los enunciados S de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) combinan filtros por texto, número, fecha y estado. Antes de cada uno, escribe en una frase qué fila debe quedar dentro y cuál afuera.

Siguiente: [1.4 NULL: cuando falta el dato](04_null.md).
