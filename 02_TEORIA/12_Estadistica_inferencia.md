# Inferencia: incertidumbre antes de afirmar diferencias

La inferencia usa una muestra para razonar sobre una población bajo supuestos. Un p-valor no es la probabilidad de que la hipótesis nula sea verdadera. Es la probabilidad, suponiendo la hipótesis y el modelo, de obtener un estadístico tan extremo o más que el observado.

## Intervalo de confianza para una media

Con n observaciones independientes, media m y desviación muestral s, error estándar = s/√n. Si el modelo t resulta adecuado, IC 95% = `m ± t(0,975,n−1)×s/√n`. La desviación describe variabilidad individual; el error estándar describe incertidumbre de la media. Un intervalo del 95% se refiere a la cobertura del procedimiento en repeticiones, no a una probabilidad del 95% de que una media fija esté dentro del intervalo calculado.

El archivo `experimento_piloto.csv` tiene una tienda ficticia por fila y etiquetas A/B construidas para ilustrar un diseño de dos grupos independientes. No se realizó un experimento real ni se verificó aleatorización empírica. Es un caso didáctico, no evidencia del desempeño de Cruzimex. Primero revisa tamaño de muestra, distribución y extremos. Si se repiten tiendas o hay selección sesgada, el cálculo simple requiere reconsideración.

## Welch t de Student, dos grupos

H0: ambas medias poblacionales son iguales; H1: difieren. Elige alfa=0,05 antes de ver datos. Usa `scipy.stats.ttest_ind(a,b,equal_var=False)` para la prueba de Welch: admite varianzas distintas, pero sigue requiriendo independencia y condiciones adecuadas del modelo. Reporta diferencia de medias en Bs, tamaños de muestra, p-valor y límites del diseño. Un efecto diminuto puede ser significativo con n grande y poco útil económicamente.

No reutilices automáticamente el t=8,81 de rutas R05/R06 como evidencia causal: aquellos datos repiten pedidos de clientes y no constituyen asignación aleatoria. Puedes reproducir el número como demostración computacional, pero no interpretar sus supuestos como comprobados. El caso piloto evita esa confusión en el ejercicio central.

## Chi-cuadrado de independencia

Compara dos variables categóricas mediante una tabla de conteos. H0: son independientes. El ejemplo `encuesta_canales.csv` tiene una respuesta por tienda, grupo A/B y compra sí/no. La tabla es `[[40,20],[25,35]]`; los esperados son suficientes para la demostración. Calcula `chi2_contingency(tabla,correction=False)`. La decisión de aplicar corrección de continuidad en una tabla 2×2 cambia el resultado; aquí la convención está declarada.

Revisa esperados antes de confiar en la aproximación. Una celda pequeña puede requerir otro método, como Fisher para 2×2. No uses valores monetarios como conteos de chi-cuadrado ni cada ítem de un mismo pedido como observación independiente. V de Cramér = √(chi²/[n×min(filas−1, columnas−1)]) añade magnitud de asociación.

## Correlación y decisión gerencial

`pearsonr` resume asociación lineal; outliers y relaciones curvas pueden ocultar estructura. Dibuja primero. Para recomendar una campaña, considera coste, tamaño del efecto, incertidumbre, posibles variables confundentes y diseño. "p<0,05" por sí solo no justifica contratar, reducir visitas ni eliminar un canal.

Práctica ST05–ST07 y notebook N05. La solución muestra cálculo e interpretación, incluida una conclusión prudente. Fuentes: SciPy ttest_ind, chi 2_contingency y t.
