# 17.3 Resolver sin ayuda externa: método, evidencia y honestidad

> Tiempo estimado: 45 min (lectura 30 + práctica 15). Prerrequisitos: [17.1](01_ocho_pasos_caso_nuevo.md), [17.2](02_cuando_no_cuadra.md) y [16.3 Portafolio y empleo honesto](../16_Git_comunicacion/03_portafolio_y_empleo.md).

## Para qué sirve

El objetivo del curso es que seas **autónomo**: que puedas resolver un problema de datos nuevo con tu propio razonamiento, documentación oficial y tu criterio. Si parte de tu trabajo anterior se hizo con ayuda de herramientas de IA, eso no es un pecado, pero tampoco prueba que sepas hacerlo tú. Esta lección explica qué se evalúa, cómo se demuestra la autonomía y cómo trabajar cuando algo se bloquea, sin depender de que otro escriba el programa por ti.

## Términos nuevos

- **Autonomía**: la capacidad de construir y defender una solución sin que otra persona o herramienta escriba el código por ti.
- **Evidencia de autonomía**: un programa reproducible, cuadres que cierran y una explicación propia de cada decisión.
- **Documentación oficial**: los manuales del lenguaje o la biblioteca (Python, Pandas, SQLite). Se puede consultar, y se registra qué se consultó y por qué.
- **Registro de consultas**: una lista de las páginas consultadas, la fecha y el motivo.
- **Bloqueo**: una situación en la que no avanzas con el problema actual.
- **Tarea independiente**: otra parte del trabajo que puedes avanzar mientras un bloqueo se resuelve.
- **Hito**: un punto de control del plan (por ejemplo, «el mini-ETL cuadra»).
- **Deuda acumulada**: tareas pendientes que se apilan sin resolverse; el plan evita crearla recortando extras.

## Ejemplo paso a paso

**1. Qué se permite y qué no en la evaluación sin código de IA.**

| Permitido | No permitido |
|---|---|
| consultar documentación oficial | copiar soluciones del paquete |
| usar tus propias notas y definiciones conceptuales | pedir a una IA que escriba el programa |
| ejecutar y depurar tu propio código | usar el ETL de referencia antes de terminar el intento |
| registrar las páginas consultadas y el motivo | ocultar qué consultaste |

Si una función falla, **tú la depuras** (lección 8.7). Durante una evaluación, si te bloqueas, **registras el bloqueo y continúas con las tareas independientes**; no se trata de resolverlo todo, sino de mostrar tu método.

**2. El método de trabajo para cada problema.**

1. **Intento (10 min):** lee el enunciado, escribe a mano un ejemplo, intenta una primera versión.
2. **Comprobar:** ejecuta y compara con tu ejemplo.
3. **Depurar (10 min):** reduce el problema (17.2), imprime valores, cambia una sola cosa.
4. **Primera pista:** solo cuando agotaste los pasos anteriores.
5. **Solución con explicación propia:** si llegas a ver una solución, **explícala con tus palabras y escríbela de nuevo sin mirar** al día siguiente.

El tiempo de intento no es castigo: es el entrenamiento. Quien ve la solución al minuto dos no aprende a depurar.

**3. El registro de consultas** (para las evaluaciones y para tu propio aprendizaje):

```python
import pandas as pd

consultas = pd.DataFrame({
    "fecha": ["2026-11-24", "2026-11-24"],
    "fuente": ["docs.python.org – módulo csv", "pandas.pydata.org – merge"],
    "motivo": ["confirmar el parámetro newline", "revisar el significado de validate"],
    "resultado": ["lo usé en extraer()", "agregué validate='m:1' al merge de catálogo"],
})
print(consultas[["fuente", "motivo"]].to_string(index=False))
print(len(consultas), "consultas registradas")
```

```salida
                      fuente                             motivo
docs.python.org – módulo csv     confirmar el parámetro newline
   pandas.pydata.org – merge revisar el significado de validate
2 consultas registradas
```

Un registro así muestra que consultaste para **entender**, no para copiar.

**4. Explicar una transformación con un ejemplo concreto.** La prueba real de autonomía es esta: ante una línea de tu código, ¿puedes decir qué recibe, qué devuelve y qué pasaría con una fila concreta?

```python
def limpiar_estado(texto):
    return texto.strip().lower()


entradas = [" Entregado", "ANULADO ", "pendiente"]
print([limpiar_estado(e) for e in entradas])
```

```salida
['entregado', 'anulado', 'pendiente']
```

Explicación propia (la que darías oralmente): «`limpiar_estado` recibe un texto, le quita los espacios de los extremos y lo pasa a minúsculas. `" Entregado"` queda `"entregado"`; `"ANULADO "` queda `"anulado"`. `"pendiente"` queda igual, pero después la regla de validación lo rechaza porque no es un estado permitido.» Si no puedes decir algo así de una línea de tu programa, esa línea todavía no es tuya.

**5. Cómo se evidencia la autonomía.** Una lista de verificación para tu proyecto final:

| Evidencia | ¿La tienes? |
|---|---|
| un programa que se ejecuta de punta a punta con un comando | ☐ |
| el cuadre de filas y de valor que cierra | ☐ |
| rechazos con motivo y un log con conteos | ☐ |
| una segunda ejecución que produce lo mismo | ☐ |
| un README con límites | ☐ |
| puedes explicar cada función con un ejemplo | ☐ |
| `errores.md` con los errores que tuviste | ☐ |
| registro de lo que consultaste | ☐ |

**6. Qué hacer si no superas un hito.** El plan no crea deuda: **recorta extras y reserva una sesión** para esa base antes de seguir. Eso es mejor que arrastrar un hito a medias. Repetir una práctica no es retroceder; es consolidar.

**7. Expectativas honestas.** El objetivo de noviembre es un **ETL junior funcional y defendible**, no una autonomía profesional avanzada garantizada. Una semana intensa no reemplaza un año de práctica. Lo que sí puedes tener al final del plan es evidencia verificable de que construiste y entiendes un pipeline pequeño. Si algo del plan no se cumple en una fecha, el plan se ajusta; no se promete lo que no se puede garantizar.

**8. Cuando usar ayuda es legítimo.** Durante el **estudio** (no en la evaluación), pedir una explicación de un concepto o de un mensaje de error, y luego **escribir tú** la solución, es un uso razonable. Lo que no cuenta como evidencia es copiar código que no puedes explicar. Tu regla personal puede ser: «puedo usar ayuda para entender; el código que entrego lo escribo y lo explico yo».

Ejemplo comercial: en la entrevista te piden resolver en vivo un ejercicio de SQL. Te bloqueas en un `HAVING`. Dices: «Voy a probar con una consulta más simple para ver los grupos y después agrego el filtro», y avanzas por pasos. Mostrar el método vale más que acertar a la primera.

## Errores comunes

- **Ver la solución antes de agotar el intento.**
- **Copiar código que no puedes explicar.**
- **No registrar las consultas** a la documentación.
- **Quedarse bloqueado** en lugar de avanzar en tareas independientes.
- **Arrastrar un hito incumplido** hasta que se acumula.
- **Prometer autonomía avanzada** que no está demostrada.
- **Confundir «lo entiendo cuando lo veo»** con «puedo escribirlo».

## Para comprobar que entendiste

1. ¿Qué se permite consultar y qué no durante la evaluación sin código de IA?
2. ¿En qué orden aplicas el método intento → comprobar → depurar → pista?
3. ¿Qué evidencia demuestra autonomía?
4. ¿Qué haces si no superas un hito?

<details><summary>Respuestas</summary>

1. Se permite documentación oficial y tus definiciones; no copiar soluciones ni pedir a una IA que programe.
2. Intento 10 min, comprobar, depurar 10 min, recién después una pista.
3. Un programa reproducible, cuadres que cierran y una explicación propia de cada decisión.
4. Recorto extras y reservo una sesión para esa base, en lugar de acumular deuda.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe tu propio acuerdo de uso de ayuda durante el estudio (qué usarás y qué no).
2. Toma una función tuya de un ejercicio y explícala por escrito con un ejemplo concreto de una fila.
3. Completa la lista de evidencia del paso 5 con lo que hoy sí tienes y lo que falta.
4. Reconstruye sin mirar una función que ya pasó el corrector y compara.

Cómo saber que está bien: tu explicación menciona una fila concreta y tu lista marca solo lo que realmente tienes.

<details><summary>Ejemplo de la parte 2</summary>

```python
def es_valida(cantidad):
    return cantidad > 0


print(es_valida(3), es_valida(0), es_valida(-2))
```

```salida
True False False
```

Explicación: «`es_valida` recibe una cantidad y devuelve `True` solo si es mayor que cero: con 3 devuelve `True`, con 0 y con −2, `False`».

</details>

## Después, en los ejercicios

La práctica de este capítulo es el caso de transferencia **C06** y la evaluación final. No abras `08_SOLUCIONES/etl_nuevo_referencia.py` ni los controles de C06 hasta terminar el intento (la evaluación final no tiene referencia en el paquete: ver su enunciado) integral ([`03_EJERCICIOS/Casos/`](../../03_EJERCICIOS/Casos/)). Siguiente capítulo: [Capítulo 18 — Entrevistas](../18_Entrevistas.md).
