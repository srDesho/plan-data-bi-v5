# 18.2 Banco de preguntas frecuentes y respuestas modelo

> Tiempo estimado: 60 min (lectura 30 + práctica 30). Prerrequisito: [18.1 Responder una pregunta técnica](01_responder_pregunta_tecnica.md).

## Para qué sirve

En las entrevistas de nivel junior las preguntas se repiten. Conocer las más frecuentes, con una respuesta modelo corta y la trampa que busca el entrevistador, te permite practicar con tus propias palabras. **No es para memorizar frases**: cada respuesta se apoya en una lección de este material y debes poder explicarla con un ejemplo y demostrarla con un cálculo.

## Términos nuevos

- **Respuesta modelo**: una respuesta correcta, breve, que te sirve de guía; la tuya debe usar tus palabras.
- **Trampa**: el error típico que la pregunta busca detectar.
- **Pregunta de seguimiento**: la que el entrevistador hace después para comprobar si entendiste.
- **Ejemplo de respaldo**: un caso concreto, con cifras, que sostiene tu respuesta.
- **Respuesta honesta**: la que reconoce un límite y propone cómo resolverlo.

## Ejemplo paso a paso

**1. SQL.**

| Pregunta | Respuesta modelo | Trampa | Lección |
|---|---|---|---|
| ¿Diferencia entre `WHERE` y `HAVING`? | `WHERE` filtra filas antes de agrupar; `HAVING` filtra grupos ya calculados (condiciones sobre agregados). | poner `COUNT(*) > 3` en `WHERE` | 2.2 |
| ¿Qué hace `LEFT JOIN` y cuándo se usa? | Conserva todas las filas de la izquierda y pone NULL si no hay pareja; sirve para hallar ausentes (anti-join) o no perder registros. | filtrar la derecha en `WHERE` y perder las filas sin pareja | 3.3 |
| ¿Por qué subió mi conteo tras un JOIN? | El detalle repite la cabecera una vez por línea; se cuenta con `DISTINCT` o se agrega antes de unir. | esconderlo con `DISTINCT` global | 3.4 |
| ¿`COUNT(*)` o `COUNT(columna)`? | El primero cuenta filas; el segundo, las no vacías de esa columna. | ignorar los NULL | 2.1 |
| ¿Qué es una función de ventana? | Calcula sobre un conjunto de filas relacionadas sin colapsarlas (`OVER`, `PARTITION BY`). | filtrarla en `WHERE` | 4.3 |
| ¿`NOT IN` o `NOT EXISTS`? | `NOT EXISTS` es más seguro porque `NOT IN` no devuelve filas si la lista tiene NULL. | confiar en `NOT IN` | 4.1 |

Demostración de la última fila (que puedes ejecutar):

```sql
SELECT
  (SELECT COUNT(*) FROM tiendas WHERE tienda_id NOT IN (SELECT tienda_id FROM ventas)) AS no_in_correcto,
  (SELECT COUNT(*) FROM tiendas t WHERE NOT EXISTS (SELECT 1 FROM ventas v WHERE v.tienda_id = t.tienda_id)) AS no_exists;
```

```resultado
no_in_correcto | no_exists
3 | 3
```

Con datos sin NULL ambos dan 3 tiendas sin ventas. La diferencia aparecería si `ventas.tienda_id` tuviera algún NULL: `NOT IN` devolvería 0. Poder **demostrarlo** con una tabla temporal (lección 4.1) es mejor que solo decirlo.

**2. Python y Pandas.**

| Pregunta | Respuesta modelo | Trampa | Lección |
|---|---|---|---|
| ¿Lista, tupla, diccionario y set? | Lista: secuencia mutable ordenada; tupla: inmutable; diccionario: pares clave-valor; set: únicos sin orden. | decir «son todos iguales» | 7.8–7.9 |
| ¿Qué es mutable? | Lo que se puede modificar sin crear otro objeto (lista, diccionario); el texto y la tupla no. | no explicar el alias | 7.8 |
| ¿`print` o `return`? | `return` entrega un valor que se puede usar; `print` solo muestra. | funciones que solo imprimen | 7.4 |
| ¿Cómo manejas un error de datos? | `try/except` del error esperado; registro de la fila rechazada con motivo; error de estructura detiene el proceso. | `except: pass` | 8.5 |
| ¿Qué hace `merge(validate=…)`? | Falla si la cardinalidad no es la esperada, evitando duplicados silenciosos. | no usarlo | 10.3 |
| ¿Por qué `groupby` pierde filas? | Descarta las claves vacías por defecto; se usa `dropna=False`. | no comparar con el total | 10.2 |
| ¿`apply` o vectorizar? | Vectorizar es más rápido y claro; `apply` solo si no hay alternativa. | usar `apply` por costumbre | 10.1 |

**3. Estadística.**

| Pregunta | Respuesta modelo | Trampa | Lección |
|---|---|---|---|
| ¿Media o mediana? | Con cola larga o atípicos, la mediana; la media si necesitas el total. | usar siempre la media | 11.3 |
| ¿Por qué `n − 1`? | Corrige el sesgo de estimar la dispersión de la población con la media de la propia muestra. | no distinguir poblacional y muestral | 11.4 |
| ¿Qué es el p-valor? | La probabilidad de ver un resultado al menos tan extremo **si `H0` fuera cierta**. | decir que es la probabilidad de que `H0` sea cierta | 12.4 |
| ¿Significativo es importante? | No: se debe reportar el tamaño del efecto y el intervalo. | solo el p-valor | 12.7 |
| ¿Correlación implica causa? | No: puede haber confusores o causa inversa; se necesita un experimento. | afirmar causa | 11.7 |
| ¿Cuándo usas chi-cuadrado y cuándo `t`? | Chi-cuadrado para categorías (conteos); `t` para comparar promedios. | usar `t` con categorías | 12.5–12.6 |

Demostración de la primera fila:

```python
import statistics

tickets = [100, 105, 110, 98, 102, 5000]
print(round(statistics.mean(tickets), 1), statistics.median(tickets))
```

```salida
919.2 103.5
```

Un ticket atípico de 5 000 lleva la media a 919, mientras la mediana sigue en 103,5. «Con este dato el promedio no describe al cliente típico; reportaría la mediana y también la media si necesito proyectar el total.»

**4. ETL y calidad de datos.**

| Pregunta | Respuesta modelo | Trampa | Lección |
|---|---|---|---|
| ¿ETL o ELT? | ETL transforma antes de cargar; ELT carga primero y transforma en el destino. Ninguno garantiza calidad. | decir que uno es mejor | 5.1 |
| ¿Qué son Bronze, Silver y Gold? | Crudo, limpio y validado, y resúmenes para el negocio. | mezclar capas | 5.1 |
| ¿Cómo sabes que tu ETL es correcto? | Contrato de datos, rechazos con motivo, cuadre de filas y de valor, y reejecución idempotente. | «porque no dio error» | 5.3–5.4 |
| ¿Qué haces con un duplicado? | Exacto: se elimina y se cuenta; conflicto de clave: se detiene o se revisa. | conservar «el primero» | 5.3 |
| ¿Qué es idempotencia? | Ejecutar varias veces deja el mismo resultado. | `append` en cada ejecución | 5.4 |
| ¿Qué haces si falta una columna? | Error legible que detiene si es obligatoria; si es opcional, se ignora explícitamente. | seguir con datos rotos | 17.1 |

**5. Power BI, DAX y Excel.**

| Pregunta | Respuesta modelo | Trampa | Lección |
|---|---|---|---|
| ¿Qué es el contexto de filtro? | El conjunto de filtros activos al evaluar una medida; `CALCULATE` lo modifica. | confundir con contexto de fila | 14.3 |
| ¿Medida o columna calculada? | Medida para totales y razones; columna para atributos por fila. | guardar el ticket como columna | 14.3 |
| ¿Cómo evitas que la meta se multiplique? | Relacionando por dimensiones conformadas a su propia granularidad. | meta en cada línea | 13.2 |
| ¿Por qué `DIVIDE`? | Controla el denominador cero y devuelve `BLANK`. | convertir `BLANK` en 0 | 14.4 |
| ¿Qué función usas para buscar un código? | `BUSCARX` o `INDICE`/`COINCIDIR` con coincidencia exacta; etiqueta de revisión si no existe. | catálogo con duplicados | 15.2 |
| ¿Por qué SQL y Excel no coinciden? | Reviso período, estado, tabla, unidad, tipos y claves, en ese orden. | culpar a la herramienta | 15.3 |

**6. Preguntas de seguimiento típicas.**

- «¿Puedes darme un ejemplo con números?» → ten uno por cada respuesta.
- «¿Qué pasa si hay NULL?» → casi siempre cambia algo; piensa en `COUNT`, `AVG`, filtros y uniones.
- «¿Cómo lo verificarías?» → un total independiente.
- «¿Qué haría diferente con más tiempo?» → una limitación honesta y una mejora concreta.

Ejemplo comercial: la mejor preparación es enseñar cada respuesta a otra persona (o grabarte) con un ejemplo de la mini-base. Si no puedes dar el ejemplo, la respuesta todavía es memoria, no comprensión.

## Errores comunes

- **Memorizar frases** sin poder dar un ejemplo.
- **Responder más de lo que preguntan.**
- **No conocer la trampa** que la pregunta busca.
- **No tener un ejemplo con cifras.**
- **Fingir conocimiento** de una herramienta que no usaste.
- **Olvidar las limitaciones** al presentar tu solución.
- **No practicar en voz alta.**

## Para comprobar que entendiste

1. Elige tres preguntas y da, de cada una, la respuesta, la trampa y un ejemplo con números.
2. ¿Qué dices cuando te preguntan por una herramienta que nunca usaste?
3. ¿Qué haces si la pregunta es ambigua?
4. ¿Por qué se practica en voz alta?

<details><summary>Respuestas</summary>

1. Por ejemplo: `LEFT JOIN`; la trampa es filtrar la derecha en `WHERE`; ejemplo: 12 tiendas, 9 con ventas, 3 sin ellas.
2. Digo que no la usé, qué herramienta parecida conozco y cómo aprendería a usarla.
3. Hago una pregunta aclaratoria antes de responder.
4. Porque explicar en voz alta revela lo que todavía no entiendes.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Graba (o escribe) la respuesta a cinco preguntas de este banco con un ejemplo de la mini-base cada una.
2. Para cada una, escribe la pregunta de seguimiento que te harían.
3. Agrega al banco tres preguntas propias basadas en errores que tuviste (`errores.md`).
4. Practica con un compañero y pídele que apunte dónde dudaste.

Cómo saber que está bien: cada respuesta incluye un ejemplo con cifras y una limitación.

<details><summary>Ejemplo de respaldo numérico para «mediana frente a media»</summary>

```python
import statistics

ventas = [120, 135, 140, 150, 160, 1800]
print(round(statistics.mean(ventas), 1), statistics.median(ventas))
```

```salida
417.5 145.0
```

</details>

## Después, en los ejercicios

El banco de preguntas, los seis simulacros y los casos empresariales están en [`06_ENTREVISTAS/`](../../06_ENTREVISTAS/); la guía de respuestas se revisa después del intento. Siguiente: [18.3 Preguntas de comportamiento y honestidad](03_conductuales_y_honestidad.md).
