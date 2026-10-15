# 1.6 DISTINCT y LIKE: valores únicos y búsquedas por patrón

> Tiempo estimado: 47 min (lectura 22 + práctica 25). Prerrequisito: [1.3 WHERE y operadores](03_where_operadores.md).

<!-- TEORIA:PREPARACION:INICIO -->
<a id="preparacion-s2"></a>

Esta sección es autocontenida. Sus 7 min están incluidos en los 22 min de lectura del encabezado; tras estudiarla, quedan 15 min de lectura del desarrollo restante. La guía asigna cada parte y evita contarla dos veces.

## Base inicial: valores únicos y unidad del resultado · 7 min

Interpreta este ejemplo en papel, con datos independientes de los archivos del curso. En un muestrario ficticio, la columna `tono` contiene `Azul`, `Rojo`, `Azul`. Listar todas las filas muestra tres muestras. Para conocer los valores diferentes:

```sqlplantilla
SELECT DISTINCT tono FROM muestrario;
```

`DISTINCT`, después de `SELECT`, conserva una fila por valor diferente de lo seleccionado: aquí, Azul y Rojo, sin un orden garantizado. **Una fila del resultado representa un tono**, no una muestra; no permite saber cuántas muestras tiene cada tono. No elimina datos de la tabla ni los ordena. Para ordenar ya tienes la preparación de S1.

Con varias columnas considera la **combinación completa**: si seleccionas también un código distinto en cada fila, pueden mantenerse las tres filas. No añadas columnas que cambien la unidad que quieres describir. Tampoco confundas diferencias de espacios o mayúsculas con duplicados idénticos.

Predice sin consultar los datos del ejercicio: ¿añadir otra muestra Azul cambia la lista de tonos? No. ¿Añadir Verde? Sí, aparece un tercer tono. Compruébalo en papel. Después resuelve el requerimiento empresarial por tu cuenta: el ejemplo no usa sus tablas ni sus columnas.

El desarrollo restante profundiza en combinaciones y búsquedas por patrón. Para este apartado basta la base inicial de [1.2](02_select_from_alias.md#preparacion-s1); el prerrequisito del encabezado corresponde al desarrollo completo.
<!-- TEORIA:PREPARACION:FIN -->

<a id="desarrollo"></a>

## Para qué sirve

Dos preguntas muy frecuentes: "¿qué valores distintos existen en esta columna?" (para conocer los datos antes de analizarlos) y "¿qué filas contienen cierto texto en el nombre?" (para buscar sin conocer el valor exacto). `DISTINCT` responde la primera y `LIKE` la segunda.

## Términos nuevos

- **DISTINCT**: elimina del resultado las filas repetidas. Va justo después de `SELECT`.
- **Valor distinto**: un valor diferente a los demás de la columna; `DISTINCT` deja uno solo de cada uno.
- **LIKE**: operador que compara texto con un **patrón**.
- **Patrón**: texto que contiene comodines. `%` representa "cualquier cantidad de caracteres (incluso ninguno)"; `_` representa "exactamente un carácter".
- **Comodín**: carácter con significado especial dentro de un patrón (`%` y `_`).

## Ejemplo paso a paso

**1. Valores únicos de una columna.** ¿Qué tipos de tienda existen?

```sql
SELECT DISTINCT tipo FROM tiendas ORDER BY tipo;
```

```resultado
tipo
Farmacia
Kiosco
Minimarket
Restaurante
Tienda de barrio
```

Sin `DISTINCT` verías las 12 filas con el tipo repetido; con `DISTINCT` quedan solo los valores diferentes. Sirve para explorar una columna antes de filtrarla: si luego escribes `WHERE tipo = 'Kiosko'` (con tilde mal puesta) sabrás por qué no devuelve nada.

**2. Combinaciones únicas.** Con varias columnas, `DISTINCT` considera la combinación completa:

```sql
SELECT DISTINCT ruta, zona FROM tiendas ORDER BY ruta, zona;
```

```resultado
ruta | zona
R01 | Centro
R01 | Norte
R01 | Plan 3000
R02 | NULL
R02 | Centro
R02 | Norte
R03 | NULL
R03 | Centro
R03 | Equipetrol
R03 | Plan 3000
```

Cada fila representa una pareja (ruta, zona) que existe en los datos. La pareja `R01, Norte` aparece una vez aunque dos tiendas la tengan. Observa que `NULL` también cuenta como un valor distinto y se muestra.

**3. Patrón al inicio, al final y en medio.**

```sql
SELECT tienda_id, nombre FROM tiendas WHERE nombre LIKE 'Farmacia%';
```

```resultado
tienda_id | nombre
3 | Farmacia Salud
8 | Farmacia Vida
```

`'Farmacia%'` significa "empieza con Farmacia y sigue con lo que sea". Otros patrones:

- `'%Luna'` termina en Luna.
- `'%Kiosco%'` contiene Kiosco en cualquier posición.
- `'R_1'` tiene tres caracteres: una R, un carácter cualquiera y un 1.

Ahora el que contiene la palabra en cualquier lugar:

```sql
SELECT tienda_id, nombre FROM tiendas WHERE nombre LIKE '%kiosco%';
```

```resultado
tienda_id | nombre
2 | Kiosco El Faro
5 |   Kiosco La Esquina 
10 | Kiosco Luna
```

Aparecen las tres tiendas con "Kiosco" aunque escribimos el patrón en minúscula: en SQLite `LIKE` **no distingue mayúsculas de minúsculas** para letras comunes. (El operador `=` sí las distingue.)

**4. La trampa de los espacios.** Probemos un patrón que empieza con "Kiosco":

```sql
SELECT tienda_id, nombre FROM tiendas WHERE nombre LIKE 'Kiosco%';
```

```resultado
tienda_id | nombre
2 | Kiosco El Faro
10 | Kiosco Luna
```

Faltó la tienda 5 (`'  Kiosco La Esquina '`): su nombre empieza con espacios, así que no *empieza* con "Kiosco". Los datos sucios rompen los filtros. En la lección 2.4 verás `TRIM` para limpiar espacios; por ahora sabe que `'%Kiosco%'` los salva y `'Kiosco%'` no.

**5. Un comodín de un solo carácter.** Rutas cuyo código es R seguido de cualquier carácter y un 1:

```sql
SELECT DISTINCT ruta FROM tiendas WHERE ruta LIKE 'R_1';
```

```resultado
ruta
R01
```

**6. Buscar el propio carácter `%`.** Si el texto contiene un `%` literal, hay que "escaparlo" con `ESCAPE`. No lo necesitarás en este curso; solo recuerda que `%` y `_` en un patrón nunca son literales.

Ejemplo comercial: el vendedor dice "búscame las farmacias". Sabes que los nombres empiezan con "Farmacia", así que un `LIKE 'Farmacia%'` es suficiente. Pero si pidieran "todo lo que tenga 'Mini' en el nombre", usarías `'%Mini%'`.

## Errores comunes

- **Usar `=` con comodines**: `nombre = 'Farmacia%'` busca el texto literal «Farmacia%», no un patrón. Para patrones usa `LIKE`.
- **Olvidar el `%`**: `LIKE 'Farmacia'` equivale a `=`: solo encuentra el nombre exacto.
- **Confiar en que `LIKE` ignora los espacios**: no los ignora.
- **`DISTINCT` en toda la consulta para "arreglar" duplicados**: puede esconder un error de JOIN o de granularidad. Úsalo para explorar, no para tapar un problema.
- **Pensar que `DISTINCT` aplica solo a la primera columna**: aplica a la combinación de todas las columnas del `SELECT`.
- **Buscar con `LIKE '%texto%'` en tablas enormes**: es lento porque revisa todas las filas.

## Para comprobar que entendiste

1. ¿Qué devuelve `SELECT DISTINCT ruta FROM tiendas;`?
2. ¿Qué significa el patrón `'%Central'`?
3. ¿Por qué `'Kiosco%'` no encontró la tienda 5?
4. ¿En qué se diferencia `%` de `_`?

<details><summary>Respuestas</summary>

1. Las rutas distintas (R01, R02, R03), una fila por ruta.
2. Un texto que termina en «Central».
3. Porque su nombre comienza con espacios, no con «Kiosco».
4. `%` reemplaza cero o más caracteres; `_` reemplaza exactamente uno.

</details>

## Micropráctica

1. Lista las categorías distintas de `articulos`.
2. Lista las tiendas cuyo nombre empiece con «Minimarket».
3. Lista los artículos cuyo nombre contenga «2L».
4. Pregunta: ¿cuántas parejas distintas (tipo, ruta) hay en `tiendas`? (Cuenta las filas del resultado de `SELECT DISTINCT tipo, ruta FROM tiendas`).

Cómo saber que está bien: la 1 devuelve 4 categorías; la 2, 2 tiendas; la 3, 2 artículos.

<details><summary>Comprobación de la consulta 3</summary>

```sql
SELECT nombre FROM articulos WHERE nombre LIKE '%2L%';
```

```resultado
nombre
Agua 2L
Gaseosa 2L
```

</details>

## Después, en los ejercicios

Los enunciados con «distintos», «únicos» o «que contienen» de [SQL](../../03_EJERCICIOS/SQL/INDICE.md) usan esta lección. Cuando uses `DISTINCT`, anota por qué hay duplicados; si no lo sabes, aún no entiendes la granularidad.

Siguiente capítulo: [2.1 Funciones agregadas](../02_SQL_agregados/01_funciones_agregadas.md).
