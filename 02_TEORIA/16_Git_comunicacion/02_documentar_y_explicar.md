# 16.2 Documentar y explicar tu trabajo: README, errores y decisiones

> Tiempo estimado: 45 min (lectura 25 + práctica 20). Prerrequisito: [6.6 Interpretar y recomendar](../06_KPIs/06_interpretar_y_recomendar.md).

Escribir un README no necesita comandos Git. [16.1](01_git_desde_cero.md) es consulta para versionar o publicar; preparar un commit no demuestra por sí solo que hayas aprendido Git.

## Para qué sirve

Un proyecto que solo tú entiendes no sirve para una entrevista ni para un equipo. La documentación hace que otra persona (o tú dentro de tres meses) pueda **reproducir** el trabajo, **entender sus reglas** y **confiar en sus cifras**. También es la prueba de que realmente lo hiciste tú: quien puede escribir por qué tomó una decisión, la tomó. Esta lección enseña tres documentos pequeños: el README, el registro de errores y el registro de decisiones.

## Términos nuevos

- **README**: el archivo de entrada de un proyecto: qué es, qué datos usa, cómo se instala, cómo se ejecuta, qué controles tiene y qué resultados da.
- **Reproducir**: que otra persona, con tu README y tus datos, obtenga los mismos resultados.
- **Registro de errores** (`errores.md`): una nota de cada error que tuviste: qué pasó, cómo lo encontraste, qué aprendiste.
- **Registro de decisiones**: la lista de decisiones no obvias (por ejemplo, «las anuladas se conservan en Silver») con su motivo.
- **Limitación**: algo que el proyecto no cubre o no puede afirmar. Escribirla aumenta la credibilidad.
- **Datos sintéticos**: datos inventados que se pueden publicar sin riesgo.
- **Informe de cuatro frases**: resultado → comparación → explicación comprobada o hipótesis → acción para investigar.

## Ejemplo paso a paso

**1. Las secciones de un README útil.**

```text
# Cumplimiento de rutas de una distribuidora (datos sintéticos)

## Problema
Una distribuidora ficticia quiere identificar las rutas con menor cumplimiento de su meta mensual.

## Datos
- Fuente: archivos CSV sintéticos de `04_DATASETS/` (inventados; no son datos reales).
- Período: agosto–septiembre de 2026. Granularidad: línea de venta.
- Indicadores: ventas entregadas, cumplimiento de meta, ticket medio (definiciones en `FICHAS_KPI.md`).

## Cómo reproducirlo
1. python -m venv .venv  y  activar el entorno
2. pip install -r requirements.txt
3. python etl/main.py --entrada datos/ --salida salida/

## Controles
- Bronze = duplicados + rechazadas + Silver (cuadre de filas)
- Importe Silver entregado = Gold (cuadre de valor)
- Segunda ejecución: mismas filas y totales

## Resultados
- Dos hallazgos con cifra y fuente.

## Limitaciones
- La ruta es la actual de cada cliente (sin historial de cambios).
- Sin descuentos ni devoluciones: «ventas entregadas», no «ventas netas».
```

Cada sección responde una pregunta que hará quien lo lea. Observa dos cosas: **no promete habilidades** que aún no puedes demostrar, y declara las limitaciones.

**2. Un README que se puede comprobar.** Una buena práctica: que los controles del README sean ejecutables. Por ejemplo, el cuadre de filas del ETL:

```python
bronze, duplicados, rechazadas, silver = 7, 1, 2, 4
cuadra = bronze == duplicados + rechazadas + silver
print("cuadre de filas:", "OK" if cuadra else "FALLA")
```

```salida
cuadre de filas: OK
```

Un README que dice «el cuadre cierra» con el número que lo demuestra vale más que uno que dice «los datos están validados».

**3. El registro de errores (`errores.md`).** Una entrada por error, con tres campos:

```text
## 2026-10-15 · P06 · KeyError

Qué pasó: el programa se detuvo con KeyError: 'estado'.
Cómo lo encontré: imprimí la fila antes de la línea que fallaba; el encabezado venía con un espacio ("estado ").
Qué aprendí: el nombre de columna puede venir sucio; limpiar los encabezados con .strip() al leer.
```

Reglas: escribe el **mensaje real** del error, el **camino** que seguiste (no solo la solución) y **una regla** que te sirva la próxima vez. Un registro así es la evidencia más honesta de que estás aprendiendo y es el material de una buena respuesta de entrevista.

**4. El registro de decisiones.** Para cada decisión de diseño que no es obvia:

| Decisión | Motivo | Alternativa descartada |
|---|---|---|
| Silver conserva las ventas anuladas | son hechos operativos; el filtro se aplica en Gold | descartarlas al limpiar |
| Importes en centavos enteros | evitar errores de decimales y de configuración regional | `float` en bolivianos |
| Conflicto de clave → detener | no se sabe cuál fila es correcta | conservar la primera |
| Ventana de actividad de 30 días | acordada con el área comercial | 60 días |

Cuando tengas que explicar tu ETL, esta tabla es tu guion.

**5. El informe de cuatro frases.** Resultado → comparación → explicación comprobada o hipótesis → acción para investigar. Ejemplo con cifras de la mini-base:

> «En septiembre las ventas entregadas fueron de Bs 1 339, un 34,8 % más que en agosto. La comparación con la meta global del mes da 99,2 %. No tenemos datos de promociones ni de stock, por lo que no atribuimos el cambio a una causa. Se sugiere revisar con el supervisor la ruta R03, que llegó al 53,3 % de su meta.»

Se puede **verificar cada cifra** (lección 6.6) y no afirma una causa. Separar el análisis de las recomendaciones y no atribuir causalidad a una correlación es parte de la honestidad del informe.

**6. Explicar una transformación con un ejemplo concreto.** En una entrevista o un examen sin ayuda, no basta decir «normalicé el estado». Se explica con una fila:

> «La fila `V2` llegó con estado `"Entregado "` (mayúscula y espacio). La regla de normalización (`strip` + minúsculas) la convierte en `"entregado"`. Si llegara `"pendiente"`, no es un estado permitido: va a rechazos con el motivo.»

El ejemplo concreto demuestra que entiendes lo que hizo el código.

**7. Lo que NO debe ir en la documentación pública.** Credenciales, datos del empleador, capturas con nombres de clientes reales, rutas de tu computadora con tu nombre. Usa los datos sintéticos de este paquete.

Ejemplo comercial: el README del proyecto SQL abre con el problema, lista las consultas, indica cómo ejecutarlas y muestra el cuadre con el total de control. Un lector decide en un minuto si el proyecto es serio.

## Errores comunes

- **README que promete lo que no demuestra.**
- **README sin comandos para reproducir.**
- **Sin limitaciones.**
- **Registro de errores que solo dice «ya lo arreglé».**
- **Decisiones no escritas** que nadie recuerda.
- **Publicar capturas con datos privados.**
- **Atribuir causalidad a una correlación** en el informe.
- **Cifras sin fuente ni control.**

## Para comprobar que entendiste

1. ¿Qué secciones mínimas tiene un README de proyecto de datos?
2. ¿Qué tres campos tiene una entrada de `errores.md`?
3. ¿Por qué se escriben las limitaciones?
4. ¿Qué debe tener una explicación de una transformación en una entrevista?

<details><summary>Respuestas</summary>

1. Problema, datos, cómo reproducirlo, controles, resultados y limitaciones.
2. Qué pasó (con el mensaje real), cómo lo encontré y qué aprendí.
3. Porque aumentan la credibilidad y evitan que se interpreten los resultados más allá de lo que permiten.
4. Un ejemplo concreto con una fila real y la regla aplicada.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe el README de tu proyecto SQL con las seis secciones.
2. Escribe tres entradas de `errores.md` con errores que ya tuviste.
3. Escribe cuatro decisiones de tu ETL en la tabla de decisiones.
4. Redacta un informe de cuatro frases con una cifra tuya y una limitación.

Cómo saber que está bien: cada afirmación de tu README tiene una cifra o un comando que la respalde.

<details><summary>Ejemplo de comprobación de una cifra del informe</summary>

```python
agosto, septiembre = 993.5, 1339.0
print(round((septiembre - agosto) / agosto * 100, 1))
```

```salida
34.8
```

</details>

## Después, en los ejercicios

La plantilla [`05_PROYECTOS/README_PLANTILLA.md`](../../05_PROYECTOS/README_PLANTILLA.md) parte de esta estructura. Siguiente: [16.3 Portafolio y empleo honesto](03_portafolio_y_empleo.md).
