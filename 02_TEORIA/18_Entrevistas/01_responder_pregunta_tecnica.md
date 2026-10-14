# 18.1 Cómo responder una pregunta técnica en cuatro pasos

> Tiempo estimado: 50 min (lectura 25 + práctica 25). Prerrequisitos: capítulos 1 a 4 (SQL) y [3.4 Cuando el JOIN duplica](../03_SQL_joins/04_duplicacion_por_join.md).

## Para qué sirve

Una entrevista técnica evalúa tu razonamiento, tu comunicación y tus límites, además de tu sintaxis. Quien responde con seguridad una consulta que no entiende pierde frente a quien dice «primero aclaro qué es una fila de este resultado». Esta lección te da un método fijo de cuatro pasos para cualquier pregunta técnica, y lo aplica en vivo a un caso de SQL y a uno de Python.

## Términos nuevos

- **Reformular**: repetir el pedido con tus palabras y con precisión («una fila por ruta y mes con ventas entregadas»).
- **Población, granularidad, denominador**: las tres cosas que dices antes de escribir una consulta (de quién, qué es una fila, contra qué se divide).
- **Ejemplo a mano**: resolver el problema con dos o tres filas inventadas antes de escribir código.
- **Verificación independiente**: comprobar el resultado con un total calculado por otro camino.
- **Pregunta aclaratoria**: una pregunta al entrevistador que evita asumir una regla en silencio («¿incluyo las anuladas?»).
- **Pensar en voz alta**: decir lo que haces mientras lo haces, para que el entrevistador vea tu método.
- **Límite de conocimiento**: reconocer lo que no sabes e indicar cómo lo comprobarías.

## El método de cuatro pasos

1. **Reformula el pedido**: «Entonces necesito una fila por ruta y mes con las ventas entregadas».
2. **Define tablas, claves y filtros**: qué tablas uso, cómo se unen y qué estados cuentan.
3. **Resuelve un ejemplo de dos pedidos a mano y escribe el código**: primero la lógica, luego la sintaxis.
4. **Verifica con un total independiente y explica limitaciones**: ¿el total cuadra? ¿qué no cubre mi solución?

Antes de escribir una consulta, di la **población**, la **granularidad** y el **denominador**. Si falta presupuesto, no puedes calcular cumplimiento: dilo. Si hay anuladas, aclara su tratamiento. **Una buena pregunta al entrevistador suele ser mejor que asumir una regla en silencio.**

## Ejemplo paso a paso

**Pregunta 1 (SQL): «¿Por qué el conteo de ventas subió después de unir con el detalle?»**

*Paso 1 · Reformula.* «Contaba ventas y, al unir con las líneas, el conteo aumentó. Quiero entender por qué.»

*Paso 2 · Tablas y claves.* «`ventas` tiene una fila por venta (clave `venta_id`); `venta_lineas` tiene una fila por línea. La relación es 1:N.»

*Paso 3 · Ejemplo a mano.* «Una venta con tres líneas aparece tres veces tras unir. Un `COUNT(*)` cuenta tres, no uno.» Lo demuestro con los datos de práctica:

```sql
SELECT COUNT(*) AS filas_tras_unir,
       COUNT(DISTINCT v.venta_id) AS ventas_distintas
FROM ventas AS v
INNER JOIN venta_lineas AS l ON l.venta_id = v.venta_id;
```

```resultado
filas_tras_unir | ventas_distintas
39 | 16
```

*Paso 4 · Verifico y explico.* «39 filas tras unir pero 16 ventas distintas: el detalle repite cada venta una vez por línea. Se corrige contando `DISTINCT venta_id`, o agregando el detalle antes de unir. **Usar `DISTINCT` sobre toda la tabla sin entender el JOIN puede ocultar el error** en vez de resolverlo.»

**Pregunta 2 (Python): «Escribe una función que devuelva el porcentaje de visitas realizadas, con el caso de cero visitas.»**

*Reformula:* «Recibe `realizadas` y `planificadas`; devuelve un porcentaje; si no hay planificadas, el resultado no está definido.»

*Aclaro:* «¿Qué devuelvo en ese caso: `None`, 0 o un error?» (Una buena pregunta: el entrevistador decide la regla.) Supongamos que responde `None`.

*Ejemplo a mano:* 11 de 14 → 78,57; 0 de 0 → `None`.

```python
def pct_realizadas(realizadas, planificadas):
    if planificadas == 0:
        return None
    return realizadas / planificadas * 100


assert round(pct_realizadas(11, 14), 2) == 78.57
assert pct_realizadas(0, 0) is None
assert pct_realizadas(0, 5) == 0
print(round(pct_realizadas(11, 14), 2), pct_realizadas(0, 0))
```

```salida
78.57 None
```

*Verificación y límites:* «Probé el caso normal, el de denominador cero y el de cero realizadas. No valida que `realizadas` ≤ `planificadas`; si el contrato lo exige, lanzaría `ValueError`.»

**Pregunta 3 (conceptual): «¿Eliminarías un valor atípico?»** Respuesta modelo: «Primero reviso si es un error de captura o un caso real del negocio. Cuantifico el efecto: calculo el resultado con y sin él. Si es un error comprobado, lo corrijo en el origen; si es real, lo conservo y uso medidas robustas como la mediana. No lo elimino sin documentar el motivo.»

**Pregunta 4 (DAX/BI): «¿Qué diferencia hay entre una medida y una columna calculada?»** Respuesta modelo: «La columna calculada tiene un valor por fila, se calcula al cargar y ocupa memoria; la medida se evalúa según el contexto de filtro del visual. El ticket medio debe ser una medida porque es un cociente que se recalcula por ruta o período; guardado como columna no se recalcula al filtrar.»

**Cuando no sabes algo.** Di lo que sí sabes y cómo lo comprobarías: «No recuerdo la sintaxis exacta de esa función de ventana; sé que necesito numerar las filas dentro de cada tienda ordenadas por fecha, y lo comprobaría en la documentación de SQLite». Eso demuestra método, que vale más que fingir memoria.

**Verificar en voz alta.** Una frase que siempre suma puntos: «Para comprobar mi resultado, calcularía el total por otro camino y comprobaría que ambos coinciden».

**Lo que NO hacer.**

- Escribir la consulta antes de reformular.
- Asumir en silencio qué estados cuentan.
- Decir «entiendo cada línea» de un código que no escribiste.
- Responder con seguridad algo de lo que no estás seguro.

Ejemplo comercial: te piden «las ventas por ruta del último mes». Respondes con preguntas: «¿entregadas o también pedidas? ¿mes calendario o últimos 30 días? ¿la ruta es la del cliente actual?». Esas tres preguntas, que son la ficha del KPI (lección 6.1), muestran más madurez que una consulta rápida.

## Errores comunes

- **Escribir código en silencio** sin explicar.
- **No preguntar** por las reglas ambiguas.
- **No verificar** el resultado con un total independiente.
- **Usar `DISTINCT`** para «arreglar» duplicados sin entender su causa.
- **Memorizar respuestas** en vez de entender el método.
- **Fingir** conocimiento que no tienes.
- **No mencionar limitaciones.**

## Para comprobar que entendiste

1. ¿Cuáles son los cuatro pasos del método?
2. ¿Qué tres cosas dices antes de escribir una consulta?
3. ¿Cómo respondes cuando no recuerdas la sintaxis?
4. ¿Por qué puede ser peligroso usar `DISTINCT` tras un JOIN?

<details><summary>Respuestas</summary>

1. Reformular; definir tablas, claves y filtros; resolver un ejemplo a mano y escribir el código; verificar con un total independiente y explicar limitaciones.
2. La población, la granularidad y el denominador.
3. Digo lo que sé de la lógica y cómo comprobaría la sintaxis en la documentación.
4. Porque puede ocultar un JOIN incorrecto en vez de corregirlo.

</details>

## Micropráctica

1. Elige una consulta que ya hayas escrito en los ejercicios y explícala en voz alta con los cuatro pasos (grábate o escríbelo).
2. Practica la pregunta: «¿Por qué mi total de ventas es mayor que el del sistema?». Escribe tu respuesta con el orden de revisión de 15.3.
3. Resuelve «porcentaje de clientes inactivos» planteando antes tres preguntas aclaratorias.
4. Escribe tu respuesta de 30 segundos a «¿qué harías con un atípico?».

Cómo saber que está bien: cada respuesta tiene reformulación, un ejemplo y una verificación.

<details><summary>Ejemplo de la parte 3: las preguntas aclaratorias</summary>

1. ¿Qué significa «inactivo»: sin compras en cuántos días y hasta qué fecha de corte?
2. ¿El denominador son todos los clientes o solo los que alguna vez compraron?
3. ¿Se cuentan las ventas anuladas como compras?

Con esas tres respuestas se puede calcular un porcentaje defendible (lección 6.3).

</details>

## Después, en los ejercicios

Practica con los simulacros del banco de preguntas de [`06_ENTREVISTAS/`](../../06_ENTREVISTAS/): cada simulacro usa una rúbrica de exactitud, validación, explicación y honestidad. Siguiente: [18.2 Banco de preguntas y respuestas modelo](02_banco_de_preguntas.md).
