# 2.4 Redondeo, texto y fechas: preparar los datos para el reporte

> Tiempo estimado: 50 min (lectura 20 + práctica 30). Prerrequisitos: [2.1](01_funciones_agregadas.md) y [1.6 DISTINCT y LIKE](../01_SQL_basico/06_distinct_like.md).

## Para qué sirve

Los datos reales no vienen listos: los nombres traen espacios, las fechas son texto, los promedios tienen diez decimales. Tres familias de funciones lo arreglan: **redondeo** (presentar números), **texto** (limpiar y unir nombres) y **fecha** (sacar el mes, medir días entre dos fechas). Las vas a usar en casi todo ejercicio de SQL y de ETL.

## Términos nuevos

- **Función escalar**: una función que recibe un valor por fila y devuelve otro valor por fila (a diferencia de las de agregación, que resumen muchas filas).
- **ROUND(valor, n)**: redondea `valor` a `n` decimales.
- **TRIM(texto)**: quita espacios al principio y al final. **UPPER / LOWER** pasan a mayúsculas o minúsculas. **LENGTH** cuenta caracteres. **SUBSTR(texto, inicio, largo)** extrae un pedazo. **REPLACE(texto, buscado, nuevo)** cambia un trozo de texto por otro.
- **Concatenar**: unir textos. En SQLite se usa el operador `||`.
- **strftime(formato, fecha)**: extrae partes de una fecha. `'%Y-%m'` da año y mes (`2026-09`), `'%Y'` solo el año.
- **julianday(fecha)**: convierte una fecha en un número de días; restar dos de ellos da los días entre fechas.
- **Fecha de corte**: la fecha fija contra la que mides un indicador (por ejemplo «al 30 de septiembre»). Con una fecha fija el resultado es repetible; si usaras «hoy», cambiaría cada día.

## Ejemplo paso a paso

**1. Redondear solo al presentar.** Precio promedio por categoría:

```sql
SELECT categoria, AVG(precio) AS promedio_crudo, ROUND(AVG(precio), 2) AS promedio_2dec
FROM articulos
GROUP BY categoria
ORDER BY categoria;
```

```resultado
categoria | promedio_crudo | promedio_2dec
Bebidas | 8.833333333333334 | 8.83
Limpieza | 8.75 | 8.75
Lácteos | 10.0 | 10.0
Snacks | 5.666666666666667 | 5.67
```

La columna cruda muestra todos los decimales; la redondeada es la que irá al reporte. Redondea en la **última** operación: si redondeas cada paso intermedio, los errores se acumulan. `ROUND(x, 0)` redondea al entero, `ROUND(x)` también.

**2. Limpiar espacios con TRIM.** La tienda 5 tiene espacios sobrantes:

```sql
SELECT tienda_id,
       '[' || nombre || ']' AS original,
       '[' || TRIM(nombre) || ']' AS limpio,
       LENGTH(nombre) AS largo_original,
       LENGTH(TRIM(nombre)) AS largo_limpio
FROM tiendas
WHERE tienda_id IN (4, 5);
```

```resultado
tienda_id | original | limpio | largo_original | largo_limpio
4 | [Minimarket Sol Naciente] | [Minimarket Sol Naciente] | 23 | 23
5 | [  Kiosco La Esquina ] | [Kiosco La Esquina] | 20 | 17
```

Los corchetes `[ ]` hacen visibles los espacios. `||` pega textos. La tienda 5 pasa de 20 a 17 caracteres (3 espacios menos). Con el nombre limpio, el patrón que antes fallaba funciona:

```sql
SELECT tienda_id, TRIM(nombre) AS nombre
FROM tiendas
WHERE TRIM(nombre) LIKE 'Kiosco%'
ORDER BY tienda_id;
```

```resultado
tienda_id | nombre
2 | Kiosco El Faro
5 | Kiosco La Esquina
10 | Kiosco Luna
```

Ahora aparecen las tres tiendas Kiosco, incluida la 5. **Regla**: limpia antes de comparar o agrupar, y deja la limpieza explícita en la consulta.

**3. Mayúsculas, extraer y reemplazar.**

```sql
SELECT nombre,
       UPPER(nombre) AS en_mayusculas,
       SUBSTR(nombre, 1, 4) AS primeras_4_letras,
       REPLACE(nombre, ' ', '_') AS con_guiones
FROM articulos
LIMIT 3;
```

```resultado
nombre | en_mayusculas | primeras_4_letras | con_guiones
Agua 2L | AGUA 2L | Agua | Agua_2L
Jugo 1L | JUGO 1L | Jugo | Jugo_1L
Gaseosa 2L | GASEOSA 2L | Gase | Gaseosa_2L
```

`SUBSTR(nombre, 1, 4)` toma 4 caracteres a partir de la posición 1 (la primera). En SQL las posiciones empiezan en 1, no en 0 como en Python.

**4. Agrupar por mes con strftime.** Ventas por mes:

```sql
SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS ventas
FROM ventas
GROUP BY mes
ORDER BY mes;
```

```resultado
mes | ventas
2026-08 | 7
2026-09 | 9
```

`strftime('%Y-%m', fecha)` convierte `2026-08-03` en `2026-08`. Las fechas guardadas como texto `AAAA-MM-DD` se ordenan y se agrupan bien porque año, mes y día van de mayor a menor. Una fecha escrita `03/08/2026` **no** se ordenaría como calendario.

**5. Días entre dos fechas.** Antigüedad de las tres primeras tiendas al 30 de septiembre de 2026:

```sql
SELECT tienda_id,
       fecha_alta,
       CAST(julianday('2026-09-30') - julianday(fecha_alta) AS INTEGER) AS dias_de_antiguedad
FROM tiendas
WHERE tienda_id <= 3
ORDER BY tienda_id;
```

```resultado
tienda_id | fecha_alta | dias_de_antiguedad
1 | 2025-02-10 | 597
2 | 2025-03-01 | 578
3 | 2025-03-15 | 564
```

`julianday` convierte cada fecha en un número de días; restarlos da los días entre ambas. `CAST(... AS INTEGER)` descarta los decimales. La fecha de corte está escrita en la consulta, no es `'now'`, para que el resultado sea el mismo mañana.

**6. Sumar o restar tiempo.**

```sql
SELECT fecha,
       date(fecha, '+7 days') AS una_semana_despues,
       date(fecha, 'start of month') AS inicio_de_mes
FROM ventas
WHERE venta_id IN (1, 8);
```

```resultado
fecha | una_semana_despues | inicio_de_mes
2026-08-03 | 2026-08-10 | 2026-08-01
2026-09-02 | 2026-09-09 | 2026-09-01
```

`date(fecha, '+7 days')` suma 7 días; `'start of month'` lleva al primer día del mes.

**Nota sobre SQL Server.** Las funciones de fecha cambian entre motores. En SQL Server el equivalente de `strftime` son `YEAR()`, `MONTH()` y `FORMAT`, el de `julianday` es `DATEDIFF(day, inicio, fin)`, la concatenación se hace con `CONCAT` o `+` y en lugar de `LIMIT` se usa `TOP`. Aquí solo se practica SQLite; los equivalentes de SQL Server son referencia conceptual y no se ejecutaron en este curso.

Ejemplo comercial: el reporte mensual de ventas por ruta necesita el mes como columna: `strftime('%Y-%m', fecha)`. Los nombres de cliente que vienen con espacios deben limpiarse con `TRIM` antes de agrupar, o «Kiosco Luna» y «Kiosco Luna » aparecerían como dos clientes.

## Errores comunes

- **Redondear antes de calcular** (por ejemplo, redondear cada precio y luego sumar).
- **Pensar que `ROUND` cambia el valor guardado**: solo cambia lo que se muestra en esa consulta.
- **Comparar texto sucio sin `TRIM`**: dos nombres que parecen iguales no lo son.
- **Empezar a contar posiciones desde 0 en `SUBSTR`.**
- **Usar `'now'` como fecha de corte** en un ejercicio que debe dar el mismo resultado siempre.
- **Guardar fechas en formato local (`DD/MM/AAAA`) como texto**: no se ordenan ni se comparan bien.
- **Olvidar que `||` con un NULL da NULL**: si alguna parte del nombre falta, todo el texto unido desaparece.

## Para comprobar que entendiste

1. ¿Cuándo conviene aplicar `ROUND`: al principio o al final?
2. ¿Qué hace `TRIM` y por qué ayudó con el patrón `'Kiosco%'`?
3. ¿Qué devuelve `strftime('%Y-%m', '2026-09-18')`?
4. ¿Por qué se escribe la fecha de corte en vez de usar `'now'`?

<details><summary>Respuestas</summary>

1. Al final, justo para presentar.
2. Quita los espacios de los extremos; sin ellos el nombre sí empieza con «Kiosco».
3. `2026-09`.
4. Para que el resultado sea reproducible: con `'now'` cambiaría cada día.

</details>

## Micropráctica

1. Calcula el importe promedio por línea de `venta_lineas` redondeado a 2 decimales.
2. Devuelve las tiendas con su nombre limpio (`TRIM`) en mayúsculas, solo las de la ruta R03.
3. Cuenta cuántas ventas hubo por mes **y** por estado.
4. Para las ventas entregadas, calcula los días entre cada fecha y la fecha de corte 2026-09-30, y muestra las 3 ventas más antiguas.

Cómo saber que está bien: la 2 muestra 4 filas y ninguna con espacios; la 3 tiene 4 filas (agosto/septiembre × entregado/anulado); la 4 empieza con la venta 1 (58 días).

<details><summary>Comprobación de las consultas 1 y 4</summary>

```sql
SELECT ROUND(AVG(cantidad * precio_unitario), 2) AS importe_promedio_linea FROM venta_lineas;
```

```resultado
importe_promedio_linea
69.78
```

```sql
SELECT venta_id, fecha, CAST(julianday('2026-09-30') - julianday(fecha) AS INTEGER) AS dias
FROM ventas
WHERE estado = 'entregado'
ORDER BY dias DESC, venta_id
LIMIT 3;
```

```resultado
venta_id | fecha | dias
1 | 2026-08-03 | 58
2 | 2026-08-05 | 56
3 | 2026-08-07 | 54
```

</details>

## Después, en los ejercicios

Las funciones de redondeo, texto y fecha se usan desde G4 en adelante en [SQL](../../03_EJERCICIOS/SQL/INDICE.md) y en el ETL de limpieza. Si un enunciado dice «mes», «antigüedad» o «nombre limpio», esta lección es la referencia.

Siguiente: [2.5 CASE y COALESCE](05_case_coalesce.md).
