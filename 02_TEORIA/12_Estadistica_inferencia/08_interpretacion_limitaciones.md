# 12.8 Interpretar, comunicar y no equivocarse

> Tiempo estimado: 55 min (lectura 30 + práctica 25). Prerrequisitos: lecciones 12.1 a 12.5. Las lecciones 12.6 (chi-cuadrado) y 12.7 (tamaño del efecto) son complementarias: aquí solo se mencionan como referencia y no hace falta haberlas estudiado.

## Para qué sirve

Saber calcular un p-valor es la mitad del trabajo. La otra mitad es **decir lo que los datos permiten decir, y no más**. Los errores más caros en estadística aplicada no son de fórmula sino de interpretación: probar muchas cosas hasta que una «sale significativa», hablar de causa sin experimento, o presentar un resultado con una seguridad que los datos no tienen. Esta lección reúne los controles y la forma de comunicar.

## Términos nuevos

- **Comparaciones múltiples**: hacer muchas pruebas sobre los mismos datos. Cada una tiene un 5 % de falsas alarmas, así que al hacer muchas aumenta la probabilidad de encontrar alguna «significativa» solo por azar.
- **p-hacking**: probar subgrupos, variables o criterios hasta obtener p < 0,05 y presentar solo ese resultado.
- **Corrección de Bonferroni**: un ajuste simple para comparaciones múltiples: usar `α / m` como umbral, donde `m` es el número de pruebas.
- **Sesgo de publicación / de selección de resultados**: reportar solo lo que salió «bien».
- **Generalización**: extender la conclusión de la muestra a la población; solo es válida si el muestreo lo permite.
- **Replicación**: repetir el estudio con datos nuevos para confirmar el hallazgo.
- **Supuesto**: una condición que la prueba necesita para ser fiable.

## Ejemplo paso a paso

**1. El peligro de las comparaciones múltiples.** Hacemos 20 comparaciones entre grupos de **la misma población** (no hay ninguna diferencia real) y contamos cuántas salen «significativas»:

```python
import random
from scipy import stats

poblacion = [20 + (i * 37 % 90) for i in range(1000)]
azar = random.Random(21)

pvalores = []
for _ in range(20):
    a = azar.sample(poblacion, 15)
    b = azar.sample(poblacion, 15)
    pvalores.append(stats.ttest_ind(a, b, equal_var=False).pvalue)

significativos = sum(1 for p in pvalores if p < 0.05)
print(significativos, "de 20 significativos")
print(round(min(pvalores), 4))
```

```salida
2 de 20 significativos
0.0441
```

Con 20 pruebas esperamos, en promedio, **1** falsa alarma (5 % de 20); aquí aparecieron **2**, y el p-valor más pequeño fue 0,044. Si alguien presentara solo la comparación «ganadora» («los kioscos del Norte venden más con p = 0,044») sin decir que hizo 20 pruebas, estaría engañando, aun sin querer. **Antes de mirar los datos, declara cuántas comparaciones harás.**

**2. Corrección de Bonferroni.** Para controlar el riesgo global, el umbral de cada prueba se divide entre el número de pruebas: con 20 pruebas, `α = 0,05 / 20 = 0,0025`.

```python
alpha = 0.05
pruebas = 20
print(alpha / pruebas)
```

```salida
0.0025
```

Con ese umbral, p = 0,044 ya no es significativo. Es una corrección sencilla y conservadora; existen otras más finas, pero la idea es la misma: **cuantas más preguntas, más exigencia**.

**3. Lista de verificación antes de concluir.**

| Pregunta | Qué revisar |
|---|---|
| ¿De quién son los datos? | población, marco, unidad de análisis |
| ¿Cómo se escogieron? | aleatorio, estratificado, conveniencia; sesgos posibles |
| ¿Cuántos datos hay? | `n` por grupo; potencia |
| ¿Cumple los supuestos? | independencia, forma, atípicos, esperados ≥ 5 |
| ¿Cuántas pruebas se hicieron? | comparaciones múltiples |
| ¿Cuál es la magnitud? | diferencia, intervalo (y, si ya estudiaste 12.7, tamaño del efecto) |
| ¿Qué dice en negocio? | traducción, costo-beneficio |
| ¿Qué NO puede afirmarse? | causalidad, generalización, período |

**4. Lenguaje correcto.**

| En lugar de... | Escribe... |
|---|---|
| «La visita extra **causa** más pedidos» | «Las tiendas con visita extra tuvieron en promedio 5,5 pedidos más; como la asignación fue [aleatoria / no aleatoria], [se puede / no se puede] atribuir la diferencia a la visita» |
| «Se demostró que...» | «Los datos son compatibles con / aportan evidencia de...» |
| «No hay diferencia (p = 0,12)» | «No se detectó una diferencia con estos datos (p = 0,12); con 6 tiendas por grupo la prueba tiene poca potencia» |
| «El resultado es significativo» | «p = 0,03; diferencia de 8 minutos (IC 95 %: 1 a 15)» |

**5. Plantilla de informe de una comparación.**

> **Pregunta de negocio:** ¿La visita extra aumenta los pedidos mensuales por tienda?
> **Datos:** 4 tiendas con visita extra y 4 sin ella, en septiembre. Asignación: [aleatoria/no aleatoria].
> **Resultado descriptivo:** medias 30,5 y 25,0 pedidos (diferencia 5,5).
> **Prueba:** `t` de Welch, bilateral, `α = 0,05`: `t = 2,57`, `gl = 5,6`, p = 0,045. IC 95 % de la diferencia: 0,2 a 10,8.
> **Tamaño del efecto** (opcional; se estudia en la lección complementaria 12.7): `d = 1,8` (grande, pero estimado con muy pocos datos). Si no la estudiaste, omite esta línea y describe la magnitud con la diferencia y su intervalo.
> **Conclusión:** hay indicios de que la visita extra aumenta los pedidos, pero la evidencia es frágil.
> **Limitaciones:** muestra de 8 tiendas, un solo mes, intervalo muy ancho, [la asignación no fue aleatoria].
> **Recomendación:** repetir con al menos 20 tiendas por grupo, asignadas al azar, antes de extender a todas las rutas.

**6. Cuando algo no encaja con tu expectativa.** Si el resultado contradice lo que esperabas, no lo ocultes ni busques otro análisis hasta que «salga». Documenta el análisis que planeaste, cuántos cambios hiciste y por qué. Un resultado inesperado y bien documentado es más valioso que uno «bonito» e inventado por filtrado.

**7. Resumen del capítulo en una ruta de decisión.**

1. ¿Qué pregunta de negocio y qué población?
2. ¿Qué tipo de variable? (numérica → medias; categórica → proporciones, con la prueba chi-cuadrado de la lección complementaria 12.6)
3. Plantear `H0`, `H1`, `α` (y cuántas pruebas harás).
4. Verificar muestreo y supuestos.
5. Calcular: estadístico, p-valor, intervalo (y tamaño del efecto si ya estudiaste 12.7).
6. Traducir a negocio con costos.
7. Declarar limitaciones y recomendar el siguiente paso (más datos, experimento).

Ejemplo comercial: el gerente quiere saber si «las rutas del Norte rinden mejor». Se miran 5 indicadores en 4 zonas y una combinación sale con p = 0,03. La respuesta honesta: «se hicieron 20 comparaciones; una sola significativa a 0,03 no resiste la corrección de múltiples comparaciones; se sugiere definir una hipótesis y probarla con datos nuevos».

## Errores comunes

- **Reportar solo la prueba que «salió».**
- **Hablar de causa sin asignación aleatoria.**
- **Afirmar «no hay diferencia» con pocos datos.**
- **Dar solo el p-valor** sin magnitud ni intervalo.
- **Generalizar a una población que no fue muestreada.**
- **Cambiar `α` o la dirección de la prueba después de ver los datos.**
- **Ocultar los análisis que no salieron** o mezclar descubrimiento y confirmación.

## Para comprobar que entendiste

1. ¿Cuántas falsas alarmas esperas al hacer 40 pruebas con `α = 0,05` cuando no hay efectos?
2. ¿Qué umbral usa Bonferroni para 10 pruebas?
3. Reescribe «se demostró que la promoción funciona (p = 0,04)» con lenguaje correcto.
4. ¿Qué se necesita para hablar de causalidad?

<details><summary>Respuestas</summary>

1. Unas 2 (5 % de 40).
2. 0,05 / 10 = 0,005.
3. Por ejemplo: «los clientes con promoción compraron en promedio X más (p = 0,04, IC 95 % ...); como [no se asignó al azar], no puede atribuirse con certeza a la promoción».
4. Un experimento con asignación aleatoria (o un diseño que controle los confusores) y supuestos razonables.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Un analista prueba 12 subgrupos de clientes y encuentra uno con p = 0,02. Escribe un párrafo corto explicando por qué ese resultado no es concluyente y qué haría falta.
2. Completa la plantilla de informe con los datos de las rutas R_A y R_B de 12.5 (puedes usar los números de las lecciones anteriores).
3. Reescribe estas dos frases con lenguaje correcto: «El nuevo horario reduce el tiempo de entrega» y «No hay diferencia entre las rutas».

Cómo saber que está bien: tu párrafo menciona las comparaciones múltiples y la necesidad de replicar con datos nuevos; tus frases separan lo observado de lo que se infiere.

<details><summary>Ejemplo de respuesta para la parte 1</summary>

Con 12 subgrupos, esperaríamos en promedio 0,6 falsas alarmas (5 % de 12) aunque no hubiera ningún efecto real; encontrar un subgrupo con p = 0,02 es compatible con el azar. Con la corrección de Bonferroni el umbral sería 0,05 / 12 ≈ 0,004. Para confirmarlo hay que formular la hipótesis de ese subgrupo antes y probarla con datos nuevos.

</details>

## Después, en los ejercicios

Todos los ejercicios ST05–ST07 y el caso C03 de [Estadística](../../03_EJERCICIOS/Estadistica/) se evalúan también por la calidad de la interpretación. Usa la plantilla de esta lección y termina siempre con limitaciones y siguiente paso. Siguiente capítulo: [Capítulo 13 — Modelado](../13_Modelado.md).
