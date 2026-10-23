# 16.3 Portafolio y búsqueda de empleo honesta desde la primera semana

> Tiempo estimado: 45 min (lectura 25 + práctica 20). Prerrequisitos: [16.2 Documentar y explicar](02_documentar_y_explicar.md).

## Para qué sirve

El objetivo final del curso es un puesto junior de datos o reportes. Buscar empleo no empieza al final: se prepara desde el principio con evidencia real, un CV honesto y un registro de postulaciones. Lo que ayuda a conseguir (y a conservar) un empleo es poder demostrar lo que dices, no parecer más experto de lo que eres.

## Términos nuevos

- **Portafolio**: el conjunto de proyectos terminados que puedes mostrar y defender.
- **Evidencia**: algo verificable que respalda una afirmación (un proyecto en un repositorio, un cuadre, una explicación).
- **CV honesto**: un currículum que describe lo que hiciste realmente, distinguiendo experiencia laboral de proyectos de formación.
- **Apoyo de IA**: uso de herramientas de inteligencia artificial para asistir una tarea. Debe declararse con precisión cuando se pregunta.
- **Registro de postulaciones**: una tabla con fecha, cargo, empresa, enlace, estado y próximo paso.
- **Borrador frente a publicación**: un texto escrito pero no publicado no cuenta como hecho.
- **Mínimo diario**: la cantidad mínima de práctica en un día de poca energía (una consulta y una explicación).

## Ejemplo paso a paso

**1. Qué se puede mostrar y qué no, hoy.** Distingue siempre tres niveles:

| Nivel | Qué es | Cómo se presenta |
|---|---|---|
| Experiencia laboral | lo que hiciste en una organización | tal como fue, con tus tareas reales y el apoyo recibido |
| Proyecto de formación | lo que construiste en el curso | por separado, **cuando esté terminado** y puedas defenderlo |
| En progreso | lo que estás aprendiendo | como «en formación», sin atribuirte la habilidad |

No inventes SQL avanzado ni programación autónoma en una pasantía donde no los usaste. Un proyecto de formación se describe aparte, como proyecto.

**2. Una presentación personal veraz.** Ejemplo de estructura (adapta a tus hechos reales):

> «Soy Técnico Superior en Sistemas Informáticos. Terminé una pasantía de seis meses en el área de BI de una empresa, trabajando con el ERP, Excel y reportes; utilicé herramientas de IA como apoyo para algunas automatizaciones. Estoy construyendo bases sólidas de SQL y Python y puedo mostrar los ejercicios que ya resolví y explicar sus controles. Busco una posición junior de datos o reportes.»

Tiene cuatro partes: formación, experiencia real (incluyendo el apoyo de IA), lo que estás haciendo ahora y lo que buscas. **Actualízala cuando termines proyectos.**

**3. «Entiendo cada línea» solo cuando es cierto.** No lo digas si todavía no puedes explicarlo. Una prueba sencilla antes de afirmar una habilidad: ¿puedo **reconstruir** una función desde cero, sin mirar, y **explicar** un JOIN con un ejemplo? Si la respuesta es no, escribe «en formación». Si te preguntan algo que excede tu experiencia: identifica lo que sí sabes y cómo comprobarías el resto.

**4. Qué aporta el apoyo de IA y cómo decirlo.** Si usaste IA como apoyo en la pasantía, dilo con precisión: *qué tareas* (por ejemplo, plantillas de automatización), *qué hiciste tú* (revisión, pruebas, ajustes) y *qué aprendiste*. No uses los resultados generados por herramientas del paquete como prueba de que tú ya adquiriste la habilidad: la evidencia es lo que puedes **hacer y explicar sin ayuda** (por eso existe la evaluación final sin código de IA).

**5. El registro de postulaciones.**

```python
import pandas as pd

registro = pd.DataFrame({
    "fecha": ["2026-10-20", "2026-10-22"],
    "cargo": ["Auxiliar de datos", "Asistente de reportes"],
    "empresa": ["(empresa 1)", "(empresa 2)"],
    "enlace": ["(url)", "(url)"],
    "estado": ["postulado", "pendiente"],
    "proximo_paso": ["esperar 7 días", "adaptar CV"],
})
print(registro[["fecha", "cargo", "estado", "proximo_paso"]].to_string(index=False))
print(registro["estado"].value_counts().to_dict())
```

```salida
     fecha                 cargo    estado   proximo_paso
2026-10-20     Auxiliar de datos postulado esperar 7 días
2026-10-22 Asistente de reportes pendiente     adaptar CV
{'postulado': 1, 'pendiente': 1}
```

Una tabla simple te dice cuántas postulaciones hay en cada estado y qué sigue. Busca puestos junior de BI, reportes, información, auxiliar o asistente de datos en tu ciudad; revisa los requisitos, **adapta dos líneas del CV** a cada puesto y registra todo. Este material no incluye vacantes inventadas ni garantiza contratación.

**6. LinkedIn sin exagerar.** Publica sobre un resultado **ya completado** (dos veces por semana es una meta razonable; una tercera, si hay evidencia y tiempo). Comparte la regla aprendida y un ejemplo con datos sintéticos, sin exagerar. Las interacciones y contactos son tareas breves que no reemplazan la práctica técnica. Un borrador no es una publicación realizada.

**7. Publicar en GitHub: lista de verificación manual.** Antes de hacer `git push` a un repositorio público:

| # | Revisión | ¿Hecho? |
|---|---|---|
| 1 | `.gitignore` excluye `.venv`, cachés, bases de datos y salidas grandes | ☐ |
| 2 | No hay credenciales, claves ni rutas personales en ningún archivo | ☐ |
| 3 | Los datos son sintéticos (nada del empleador) | ☐ |
| 4 | `git status` y `git diff` revisados; solo archivos concretos añadidos | ☐ |
| 5 | El README tiene problema, datos, reproducción, controles y limitaciones | ☐ |
| 6 | No se prometen habilidades que no puedes demostrar | ☐ |
| 7 | Las capturas no muestran información privada | ☐ |

La publicación es una **ejecución manual y deliberada**: este paquete no sube ni envía nada automáticamente.

**8. Un día de descanso o de poca energía.** El progreso no se mide por la cantidad de commits ni de publicaciones. Un día mínimo puede ser una consulta y una explicación. Lo que importa es poder reconstruir una función o explicar un JOIN sin mirar. Si un día es de recuperación, se registra como tal; no se compensa con culpa.

Ejemplo comercial: un reclutador pregunta «¿qué hiciste en tu pasantía y qué hiciste después?». Con el modelo de tres niveles, respondes en un minuto: lo que hiciste (con el apoyo de IA declarado), lo que construiste después (con el repositorio) y lo que estás aprendiendo.

## Errores comunes

- **Mezclar experiencia laboral con proyectos de formación.**
- **Inventar o inflar habilidades.**
- **Decir «entiendo cada línea»** sin poder explicarlo.
- **Ocultar el apoyo de IA** o, al revés, usarlo como prueba de habilidad propia.
- **Publicar sin revisar** qué se sube.
- **Contar un borrador como publicación.**
- **Medir el progreso por cantidad de actividad.**
- **Postular sin adaptar el CV.**

## Para comprobar que entendiste

1. ¿Cuáles son los tres niveles que distingues en un CV?
2. ¿Qué cuatro partes tiene una presentación personal veraz?
3. ¿Qué compruebas antes de hacer `push`?
4. ¿Cuál es una buena prueba antes de afirmar una habilidad?

<details><summary>Respuestas</summary>

1. Experiencia laboral, proyecto de formación y en progreso.
2. Formación, experiencia real (con apoyo de IA si lo hubo), lo que estás haciendo ahora y lo que buscas.
3. Que no haya credenciales ni datos privados, y qué archivos se suben exactamente.
4. Poder reconstruir la función sin mirar y explicar el JOIN con un ejemplo.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe tu presentación personal con las cuatro partes y solo hechos verdaderos.
2. Crea la tabla de postulaciones con tres filas ficticias de práctica y calcula cuántas hay por estado.
3. Completa la lista de verificación de publicación para un repositorio tuyo.
4. Redacta una publicación de LinkedIn de tres frases sobre un resultado ya completado.

Cómo saber que está bien: ninguna afirmación de tus textos es algo que no puedas demostrar hoy.

<details><summary>Ejemplo de la parte 2</summary>

```python
import pandas as pd

tabla = pd.DataFrame({"estado": ["postulado", "pendiente", "postulado"]})
print(tabla["estado"].value_counts().to_dict())
```

```salida
{'postulado': 2, 'pendiente': 1}
```

</details>

## Después, en los ejercicios

Usa la plantilla [`05_PROYECTOS/README_PLANTILLA.md`](../../05_PROYECTOS/README_PLANTILLA.md) y las guías de [`07_LINKEDIN_EMPLEO/`](../../07_LINKEDIN_EMPLEO/) para tu CV y tu registro de postulaciones. Siguiente capítulo: [Capítulo 17 — Transferencia y autonomía](../17_Transferencia_debug.md).
