# 18.3 Preguntas de comportamiento, apoyo de IA y honestidad

> Tiempo estimado: 45 min (lectura 25 + práctica 20). Prerrequisitos: [16.3 Portafolio y empleo honesto](../16_Git_comunicacion/03_portafolio_y_empleo.md) y [18.2 Banco de preguntas](02_banco_de_preguntas.md).

## Para qué sirve

Además de lo técnico, una entrevista evalúa cómo trabajas: cómo manejas los errores, los plazos, a los compañeros y tus propios límites. Para una persona que empieza, la pregunta más delicada es siempre la misma: *«¿qué hiciste tú?»*. Esta lección te enseña a contestar con hechos, a separar lo que hiciste de lo que generó una herramienta y a convertir un límite honesto en una fortaleza.

## Términos nuevos

- **Pregunta conductual**: la que pide un ejemplo real de una situación pasada («cuéntame de una vez que…»).
- **Método STAR**: una estructura para responder: **S**ituación, **T**area, **A**cción (la tuya) y **R**esultado.
- **Acción propia**: lo que tú hiciste, distinto de lo que hizo el equipo o una herramienta.
- **Apoyo de IA**: el uso de herramientas de inteligencia artificial como ayuda; se describe con precisión (qué tarea, qué aportó, qué hiciste tú).
- **Límite honesto**: reconocer que algo excede tu experiencia y explicar cómo lo resolverías.
- **Simulacro**: una práctica de entrevista con una rúbrica.
- **Rúbrica**: los criterios con que se evalúa un simulacro: exactitud, validación, explicación y honestidad.

## Ejemplo paso a paso

**1. El método STAR con un ejemplo de depuración.**

| Parte | Contenido (ejemplo) |
|---|---|
| **Situación** | «En un ejercicio de ETL, el total de ventas no coincidía con la fuente de control.» |
| **Tarea** | «Debía encontrar la causa antes de entregar el cuadre.» |
| **Acción (propia)** | «Comparé las filas por etapa y luego los importes por documento; vi que solo duplicaba las ventas de una tienda; revisé el catálogo y encontré una fila repetida. Corregí el catálogo, agregué `validate` al merge y escribí una prueba.» |
| **Resultado** | «El total cuadró y la prueba evita que se repita. Lo documenté en mi registro de errores.» |

Es una historia **real y pequeña**. Un error bien depurado y explicado vale más que un éxito sin detalles.

**2. Prepara tres historias reales.**

1. **Un error y su depuración** (como la de arriba).
2. **Un plazo**: cómo organizaste el trabajo cuando el tiempo era corto, qué dejaste fuera y por qué.
3. **Colaboración con un supervisor o compañero**: cómo pediste una aclaración o recibiste una corrección.

Separa siempre lo que realizaste de lo que generó una herramienta. **Un resultado válido también puede ser detectar un dato faltante y comunicarlo a tiempo.**

**3. «¿Qué hiciste en tu pasantía?»: una respuesta veraz.** La estructura de la lección 16.3 aplicada:

> «Hice una pasantía de seis meses en el área de BI: trabajé con el ERP, Excel y reportes, y usé herramientas de IA como apoyo para algunas automatizaciones; yo revisaba y ajustaba lo que generaban. Después de la pasantía decidí construir bases sólidas por mi cuenta: estoy resolviendo ejercicios de SQL y Python con correctores y puedo mostrarlos y explicar sus controles.»

Qué tiene de bueno: no oculta el apoyo de IA, no se atribuye un conocimiento que no tenía en ese momento, y orienta la conversación a lo que puedes demostrar hoy.

**4. Preguntas difíciles y cómo contestarlas con honestidad.**

| Pregunta | Mala respuesta | Mejor respuesta |
|---|---|---|
| «¿Dominas SQL?» | «Sí, todo.» | «Resuelvo consultas con JOIN, agregaciones y ventanas, y verifico los totales con un segundo camino; las puedo mostrar. Todavía no he trabajado con bases muy grandes.» |
| «¿Escribiste ese código tú?» | «Sí» (si no es cierto) | «Lo escribí yo con apoyo de documentación; el ETL final lo construí sin ayuda de IA y puedo explicar cada función con un ejemplo.» |
| «¿Qué no sabes?» | «Nada importante.» | «No he usado Spark ni nube; sé cómo aprendería: empezaría por... y lo probaría con...». |
| «¿Qué harías si no sabes algo en el trabajo?» | «Preguntaría a alguien.» | «Reproduzco el problema en pequeño, reviso la documentación, anoto lo que probé y, si sigo bloqueado, pregunto con ese resumen.» |
| «Tu mayor error» | «Ninguno.» | Una historia real de depuración y la regla que aprendiste. |

**5. No uses los resultados del paquete como prueba de tu habilidad.** Si presentas un cuadre generado por el material de práctica, no lo presentes como prueba de que *tú* adquiriste la habilidad. La prueba es lo que haces y explicas sin ayuda: por eso existe la evaluación final sin código de IA y por eso un buen portafolio contiene solo lo que puedes defender.

**6. Un simulacro con rúbrica.** Seis simulacros del banco de `06_ENTREVISTAS/`, cada uno con cuatro criterios:

| Criterio | Qué se evalúa | Puntos (0–2) |
|---|---|---|
| Exactitud | ¿la solución es correcta? | |
| Validación | ¿comprobaste con un total independiente? | |
| Explicación | ¿se entiende tu razonamiento, con un ejemplo? | |
| Honestidad | ¿reconociste límites y no inventaste? | |

Guarda una respuesta de voz de dos minutos (o un texto breve) de cada simulacro y revísala con la guía **después** del intento, no antes.

```python
import pandas as pd

simulacros = pd.DataFrame({
    "simulacro": ["S1", "S2", "S3"],
    "exactitud": [2, 1, 2],
    "validacion": [1, 1, 2],
    "explicacion": [2, 2, 1],
    "honestidad": [2, 2, 2],
})
simulacros["total"] = simulacros[["exactitud", "validacion", "explicacion", "honestidad"]].sum(axis=1)
print(simulacros[["simulacro", "total"]].to_string(index=False))
print(simulacros[["exactitud", "validacion", "explicacion", "honestidad"]].mean().round(2).to_dict())
```

```salida
simulacro  total
       S1      7
       S2      6
       S3      7
{'exactitud': 1.67, 'validacion': 1.33, 'explicacion': 1.67, 'honestidad': 2.0}
```

Al promediar por criterio ves **dónde mejorar** (aquí, la validación): ese es el sentido de la rúbrica, no el total.

**7. Actualiza tu presentación cuando completes proyectos.** Cada hito cierra una frase nueva y verdadera: «Construí un ETL de [dominio] con Bronze, Silver y Gold, cuadres de filas y de valor, y lo puedo ejecutar y explicar». Hasta que no lo hayas hecho y puedas explicarlo, la frase se mantiene en «estoy construyendo».

**8. Si una pregunta excede tu experiencia.** Tres pasos: reconoce el límite («eso no lo he hecho»); di lo que sí sabes que se relaciona; explica cómo lo comprobarías o aprenderías. Esa respuesta no pierde puntos; mentir sí.

Ejemplo comercial: te preguntan por Power BI y solo lo has usado en un ejemplo guiado. Respondes: «Construí un modelo estrella con una tabla de hechos y tres dimensiones, y escribí las medidas básicas siguiendo una guía; las cifras las cuadré con SQL. No he publicado en el servicio ni configurado seguridad por filas». Es una respuesta verificable.

## Errores comunes

- **Atribuirte lo que hizo una herramienta.**
- **Ocultar el apoyo de IA** o, al revés, presentarlo como habilidad propia.
- **Decir «entiendo cada línea»** sin poder explicarlo.
- **Historias inventadas o exageradas.**
- **Responder «ningún error»** a la pregunta del mayor error.
- **No practicar en voz alta.**
- **Revisar la guía de respuestas antes del intento.**

## Para comprobar que entendiste

1. ¿Qué significa cada letra de STAR?
2. ¿Qué tres historias reales conviene preparar?
3. ¿Cómo respondes si te preguntan por una herramienta que no conoces?
4. ¿Cuándo se revisa la guía de un simulacro?

<details><summary>Respuestas</summary>

1. Situación, Tarea, Acción (propia) y Resultado.
2. Un error y su depuración, un plazo y una colaboración con un supervisor o compañero.
3. Reconozco el límite, digo lo relacionado que sí sé y cómo lo aprendería.
4. Después del intento.

</details>

## Micropráctica

1. Escribe tu historia STAR de un error con tus propios hechos (usa tu `errores.md`).
2. Escribe tu respuesta de 30 segundos a «¿qué hiciste en tu pasantía?» con apoyo de IA declarado.
3. Responde por escrito a «¿qué no sabes?» con un plan concreto.
4. Realiza un simulacro y puntúate con la rúbrica; anota el criterio más bajo y qué harás.

Cómo saber que está bien: tu historia tiene una acción tuya concreta y un resultado verificable.

<details><summary>Ejemplo de seguimiento de la rúbrica</summary>

```python
puntajes = {"exactitud": 2, "validacion": 1, "explicacion": 2, "honestidad": 2}
mas_bajo = min(puntajes, key=puntajes.get)
print(mas_bajo, sum(puntajes.values()))
```

```salida
validacion 7
```

</details>

## Después, en los ejercicios

Los simulacros y casos empresariales están en [`06_ENTREVISTAS/`](../../06_ENTREVISTAS/). Siguiente capítulo: [Capítulo 19 — Puente de Python a ETL](../19_Puente_Python_a_ETL.md).
