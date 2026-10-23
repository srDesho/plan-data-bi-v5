# 1.7 Del requerimiento a la consulta: un método de cinco preguntas

> Tiempo estimado: 40 min (lectura 15 + práctica 25). Prerrequisitos: lecciones 1.1 a 1.6.

## Para qué sirve

En el trabajo nadie te dicta el `SELECT`. Te dicen una frase: "necesito las ventas anuladas de septiembre para revisarlas". Convertir esa frase en una consulta correcta es la habilidad real. Esta lección junta lo que ya sabes en un método de cinco preguntas que puedes repetir con cualquier pedido, y que además te sirve para explicar tu consulta a otra persona.

## Términos nuevos

- **Requerimiento**: lo que pide una persona del negocio, escrito en lenguaje de negocio, no de bases de datos.
- **Criterio de verificación**: una comprobación que haces después de ejecutar para saber que el resultado tiene sentido (por ejemplo, que la fecha mínima del resultado esté dentro del período pedido).
- **Valor límite** (o *borde*): el primer o último valor que cumple un filtro. Son los puntos donde más errores se cometen (`>` contra `>=`).

## Ejemplo paso a paso

Requerimiento: *"Necesito revisar las ventas anuladas de septiembre de 2026."*

**Pregunta 1: ¿qué representa una fila de mi resultado?** Una venta. La tabla que tiene una fila por venta es `ventas` (la de `venta_lineas` tiene una fila por artículo).

**Pregunta 2: ¿qué filtros dice el pedido?** Dos: el estado es `anulado` y la fecha está en septiembre de 2026. Septiembre de 2026 va del `2026-09-01` al `2026-09-30`, ambos incluidos.

**Pregunta 3: ¿qué columnas necesita quien lo va a leer?** Para revisar una venta anulada: el número, la tienda, el vendedor, la fecha y el estado.

**Pregunta 4: ¿en qué orden?** Del más antiguo al más reciente, con desempate por número de venta.

**Pregunta 5: ¿cómo sé que está bien?** Reviso que todas las fechas caigan dentro de septiembre, que todos los estados sean `anulado` y que no falte nada comparando con una consulta más amplia.

Escribimos la consulta uniendo las respuestas:

```sql
SELECT venta_id, tienda_id, vendedor_id, fecha, estado
FROM ventas
WHERE estado = 'anulado'
  AND fecha BETWEEN '2026-09-01' AND '2026-09-30'
ORDER BY fecha, venta_id;
```

```resultado
venta_id | tienda_id | vendedor_id | fecha | estado
13 | 9 | 3 | 2026-09-18 | anulado
```

Y la verificación (pregunta 5): miramos **todas** las anuladas sin filtro de fecha para confirmar que no nos dejamos nada de septiembre fuera por un error de borde:

```sql
SELECT venta_id, fecha, estado
FROM ventas
WHERE estado = 'anulado'
ORDER BY fecha, venta_id;
```

```resultado
venta_id | fecha | estado
4 | 2026-08-12 | anulado
13 | 2026-09-18 | anulado
```

Hay dos ventas anuladas en total: la 4 (agosto) y la 13 (septiembre). La consulta pedida devuelve solo la 13: es correcto. Este tipo de contraste, "filtro estrecho contra filtro amplio", es una verificación muy barata.

**Cuando una tabla no alcanza.** Otro requerimiento: *"Las ventas anuladas de las tiendas de tipo Minimarket"*. La pregunta 1 dice: una venta. Pero el tipo de tienda no está en `ventas`; está en `tiendas`. Con una sola tabla no puedes responder: necesitas **unir** las dos (capítulo 3). Reconocer a tiempo que te falta información es parte del método; la respuesta correcta aquí es "necesito otra tabla", no inventar una condición.

**Cuando el pedido es ambiguo.** *"Dame las mejores tiendas."* ¿Mejores por qué? ¿Ventas, número de visitas, crecimiento? ¿En qué período? Una consulta que adivina responde con seguridad algo que nadie preguntó. Antes de escribir, devuelve la ambigüedad como pregunta concreta: "¿Mejores en ventas en Bs de septiembre?".

Ejemplo comercial: el gerente comercial escribe por mensaje "pásame los artículos de limpieza y lácteos del más caro al más barato". Las cinco preguntas dan: fila = artículo; filtro = categoría en esas dos; columnas = nombre, categoría y precio; orden = precio descendente (desempate por nombre); verificación = ninguna fila de otra categoría.

```sql
SELECT nombre, categoria, precio
FROM articulos
WHERE categoria IN ('Limpieza', 'Lácteos')
ORDER BY precio DESC, nombre;
```

```resultado
nombre | categoria | precio
Detergente 1kg | Limpieza | 14.0
Yogurt 1L | Lácteos | 12.0
Leche 1L | Lácteos | 8.0
Jabón | Limpieza | 3.5
```

## Errores comunes

- **Empezar por el código** sin responder qué es una fila: el 80 % de los errores nace aquí.
- **Filtrar por la columna equivocada**: por ejemplo, pedir "ventas de septiembre" y filtrar por `fecha_alta` de la tienda.
- **No pensar en los bordes**: el último día de un período, el valor exactamente igual al límite.
- **Dar por buena la primera ejecución**: que no dé error no significa que sea correcto. Siempre contrasta con una consulta amplia.
- **Resolver una ambigüedad en silencio**: anota la interpretación que usaste.
- **Ignorar los filtros de negocio implícitos**: «ventas» casi siempre excluye las anuladas.

## Para comprobar que entendiste

1. Menciona las cinco preguntas del método.
2. ¿Por qué se compara la consulta con una versión sin filtro de fecha?
3. ¿Qué haces si el pedido no se puede responder con una sola tabla?
4. ¿Qué es un valor límite y por qué importa?

<details><summary>Respuestas</summary>

1. Qué es una fila; qué filtros; qué columnas; qué orden; cómo verifico.
2. Para comprobar que el filtro de fecha no dejó fuera filas que sí cumplían.
3. Reconozco que necesito unir tablas (capítulo 3) y no invento una condición.
4. El primer o último valor que cumple el filtro; los errores `>` vs `>=` se manifiestan ahí.

</details>

<a id="micropractica"></a>

## Micropráctica

Aplica las cinco preguntas, por escrito, a este requerimiento y luego escribe y ejecuta la consulta:

*"Quiero ver las líneas de venta de la venta 7, con el artículo, la cantidad y el subtotal, de la línea más grande a la más pequeña."*

1. ¿Qué es una fila? ¿Qué tabla usas?
2. Filtro, columnas, orden.
3. ¿Cómo verificas el subtotal de la primera fila a mano?

Cómo saber que está bien: la consulta devuelve 3 filas; el mayor subtotal es el de Agua 2L (20 unidades a Bs 6,00 son Bs 120).

<details><summary>Comprobación</summary>

```sql
SELECT articulo_id, cantidad, precio_unitario, cantidad * precio_unitario AS subtotal
FROM venta_lineas
WHERE venta_id = 7
ORDER BY subtotal DESC, articulo_id;
```

```resultado
articulo_id | cantidad | precio_unitario | subtotal
1 | 20 | 6.0 | 120.0
9 | 12 | 8.0 | 96.0
10 | 6 | 12.0 | 72.0
```

La columna `articulo_id` es el código del artículo; el nombre está en otra tabla (`articulos`) y necesitarías unirla, como en el segundo ejemplo de esta lección.

</details>

## Después, en los ejercicios

Al abrir cualquier enunciado de [SQL](../../03_EJERCICIOS/SQL/INDICE.md), antes de escribir código responde las cinco preguntas en un comentario `-- ...`. Tu corrector te dirá si el resultado coincide, pero el método es lo que te hace autónomo.

Siguiente capítulo: [2.1 Funciones agregadas](../02_SQL_agregados/01_funciones_agregadas.md).
