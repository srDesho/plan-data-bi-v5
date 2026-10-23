# 11.7 Correlación y causalidad

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [11.4 Dispersión](04_dispersion.md) y [11.6 Puntaje z](06_distribuciones_histograma_z.md).

## Para qué sirve

«Las tiendas que reciben más visitas venden más». ¿Entonces hay que visitar más a todas? La correlación mide **si dos variables se mueven juntas**, pero no dice **por qué**. Saber calcularla y, sobre todo, saber qué no puedes concluir de ella, evita decisiones caras basadas en coincidencias.

## Términos nuevos

- **Relación entre variables**: cuando los valores de una variable tienden a cambiar junto con los de otra.
- **Diagrama de dispersión** (*scatter plot*): un gráfico donde cada punto es una unidad, con una variable en cada eje.
- **Covarianza**: el promedio de los productos de las desviaciones de dos variables respecto a sus medias. Su signo indica si se mueven en el mismo sentido (+) o en sentidos opuestos (−), pero su tamaño depende de las unidades.
- **Coeficiente de correlación de Pearson (`r`)**: la covarianza «estandarizada» para que quede entre −1 y +1: `r = Σ(dx · dy) / √(Σdx² · Σdy²)`, donde `dx = x − x̄` y `dy = y − ȳ`. Mide la fuerza de una relación **lineal**.
- **Correlación positiva / negativa**: cuando una sube la otra tiende a subir / a bajar.
- **Variable confusora**: una tercera variable que influye en las dos y crea una correlación que no es causal.
- **Causalidad**: que un cambio en una variable *produce* el cambio en la otra. La correlación por sí sola no la demuestra.
- **Experimento**: un estudio en el que **tú** asignas el tratamiento al azar; es la forma más fiable de acercarse a la causalidad.

## Ejemplo paso a paso

Datos inventados: visitas semanales recibidas por 6 tiendas (`x`) y sus ventas semanales en Bs (`y`):

| Tienda | Visitas `x` | Ventas `y` |
|---|---|---|
| A | 2 | 190 |
| B | 4 | 210 |
| C | 5 | 330 |
| D | 7 | 340 |
| E | 8 | 470 |
| F | 10 | 440 |

**1. Calcular `r` a mano.**

1. Medias: `x̄ = 36 / 6 = 6`; `ȳ = 1980 / 6 = 330`.
2. Desviaciones y productos:

| Tienda | `dx = x − 6` | `dy = y − 330` | `dx · dy` | `dx²` | `dy²` |
|---|---|---|---|---|---|
| A | −4 | −140 | 560 | 16 | 19 600 |
| B | −2 | −120 | 240 | 4 | 14 400 |
| C | −1 | 0 | 0 | 1 | 0 |
| D | 1 | 10 | 10 | 1 | 100 |
| E | 2 | 140 | 280 | 4 | 19 600 |
| F | 4 | 110 | 440 | 16 | 12 100 |
| **Suma** | 0 | 0 | **1530** | **42** | **65 800** |

3. `r = 1530 / √(42 × 65 800) = 1530 / √2 763 600 = 1530 / 1662,4 = 0,920`.

Control: las columnas `dx` y `dy` suman 0.

**2. Verificar con Python.**

```python
import numpy as np
import pandas as pd

visitas = [2, 4, 5, 7, 8, 10]
ventas = [190, 210, 330, 340, 470, 440]
print(round(np.corrcoef(visitas, ventas)[0, 1], 3))
print(round(pd.Series(visitas).corr(pd.Series(ventas)), 3))
```

```salida
0.92
0.92
```

Los dos dan 0,920, igual que a mano.

**3. Cómo se interpreta `r`.**

| Valor de r sin signo | Lectura orientativa |
|---|---|
| 0,0 – 0,2 | casi sin relación lineal |
| 0,2 – 0,5 | relación débil |
| 0,5 – 0,8 | relación moderada |
| 0,8 – 1,0 | relación fuerte |

Son guías, no reglas. El **signo** dice el sentido (positivo: juntas suben; negativo: una sube y la otra baja). `r = 0,92` es una relación lineal positiva fuerte en estas 6 tiendas. `r²` (aquí 0,846) se lee como «la proporción de la variación de las ventas que acompaña linealmente a las visitas»; no es una relación causal.

**4. `r = 0` no significa «sin relación».** Pearson solo detecta relaciones **lineales**:

```python
import numpy as np

x = [-3, -2, -1, 0, 1, 2, 3]
y = [9, 4, 1, 0, 1, 4, 9]
print(round(np.corrcoef(x, y)[0, 1], 3))
```

```salida
0.0
```

Aquí `y = x²` es una relación perfecta (una curva), pero `r` da 0. Por eso **primero se mira el diagrama de dispersión** y después se calcula `r`.

**5. Un solo punto puede cambiarlo todo.** Añadimos una tienda atípica (muchas visitas, pocas ventas):

```python
import numpy as np

visitas = [2, 4, 5, 7, 8, 10]
ventas = [190, 210, 330, 340, 470, 440]
print(round(np.corrcoef(visitas, ventas)[0, 1], 3))

visitas2 = visitas + [12]
ventas2 = ventas + [100]
print(round(np.corrcoef(visitas2, ventas2)[0, 1], 3))
```

```salida
0.92
0.122
```

De 0,92 baja a 0,12 con una sola tienda adicional. La correlación es sensible a los atípicos (como la media); revisa siempre el gráfico.

**6. Correlación no es causalidad.** Que visitas y ventas suban juntas puede deberse a:

1. **Causa directa**: más visitas generan más pedidos.
2. **Causa inversa**: se visita más a las tiendas que ya compran mucho (los vendedores priorizan a los buenos clientes).
3. **Variable confusora**: las tiendas **grandes** reciben más visitas y también venden más; el tamaño explica ambas cosas.
4. **Coincidencia**: con pocos datos, dos series pueden correlacionar por azar.

Un ejemplo clásico fuera del negocio: las ventas de helados y los ahogamientos en piscinas correlacionan positivamente; la variable confusora es el calor. Nadie concluiría que los helados causan ahogamientos.

**7. ¿Cómo acercarse a la causalidad?** Con un **experimento**: asignar al azar un grupo de tiendas a recibir una visita extra y otro grupo no, y comparar (capítulo 12). Si las tiendas «tratadas» se escogieran a mano, la comparación mediría tu criterio de selección, no el efecto de la visita.

Ejemplo comercial: antes de pedir más visitadores, pregunta si la relación se mantiene **dentro** de cada tamaño de tienda (por ejemplo, solo entre tiendas pequeñas), si se visita más a quien ya vende más, y si hay un piloto con asignación al azar.

## Errores comunes

- **Concluir causalidad** de una correlación.
- **Calcular `r` sin mirar el diagrama de dispersión.**
- **Creer que `r = 0` significa independencia** (puede haber curva).
- **Ignorar los atípicos** que dominan el resultado.
- **Interpretar `r` fuerte con muy pocos datos** como algo establecido.
- **Correlacionar variables categóricas codificadas con números** (códigos de ruta).
- **Olvidar las variables confusoras** (tamaño, zona, temporada).

## Para comprobar que entendiste

1. ¿Entre qué valores se mueve `r` y qué indican sus extremos?
2. ¿Por qué `r` puede ser 0 aunque exista una relación clara?
3. Da un ejemplo de variable confusora en el contexto de la distribuidora.
4. ¿Qué tipo de estudio permite acercarse a la causalidad?

<details><summary>Respuestas</summary>

1. Entre −1 y +1; los extremos indican relación lineal perfecta (positiva o negativa) y 0 ausencia de relación lineal.
2. Porque Pearson mide solo relaciones lineales; una curva puede dar 0.
3. El tamaño de la tienda: influye en las visitas que recibe y en lo que vende.
4. Un experimento con asignación al azar.

</details>

<a id="micropractica"></a>

## Micropráctica

Con las temperaturas máximas diarias (°C) y las unidades vendidas de bebidas en un puesto durante 6 días: `x = [24, 27, 29, 31, 33, 35]` e `y = [40, 52, 55, 70, 74, 90]`:

1. Calcula `r` **a mano** con la tabla de desviaciones.
2. Verifica con Python.
3. Escribe tres posibles explicaciones de la relación, incluyendo una que no sea causal.

Cómo saber que está bien: `r` es positivo y mayor que 0,95.

<details><summary>Comprobación de la parte 2</summary>

```python
import numpy as np

x = [24, 27, 29, 31, 33, 35]
y = [40, 52, 55, 70, 74, 90]
print(round(np.corrcoef(x, y)[0, 1], 3))
```

```salida
0.982
```

</details>

## Después, en los ejercicios

El caso C03 y ST04 de [Estadística](../../03_EJERCICIOS/Estadistica/) piden interpretar relaciones; tu respuesta debe separar lo que muestran los datos de lo que no pueden probar. Siguiente: [11.8 Muestreo](08_muestreo.md).
