# 11.1 Población, muestra y tipos de variables

> Tiempo estimado: 50 min (lectura 25 + práctica 25). Prerrequisitos: capítulos 9 y 10 (leer un CSV con Pandas) o, como mínimo, [7.13 Registros](../07_Python_basico/13_registros_listas_de_diccionarios.md).

## Para qué sirve

Antes de calcular un promedio o un porcentaje hay que responder dos preguntas: **¿de quién son estos datos?** y **¿qué tipo de dato es cada columna?** Con la primera sabes si tu resultado describe a todos los clientes o solo a una parte; con la segunda eliges el cálculo correcto (no se promedia una zona, ni se hace un gráfico de barras con montos continuos como si fueran categorías). Es el cimiento de toda la estadística del curso.

## Términos nuevos

- **Estadística descriptiva**: resume y describe los datos que tienes (tablas, promedios, gráficos). No va más allá de ellos. La **inferencia** (capítulo 12) sí intenta concluir sobre algo más grande.
- **Unidad de análisis**: lo que representa cada fila de tus datos (una tienda, una venta, una visita). Es la **granularidad** de la tabla.
- **Población**: el conjunto completo de unidades sobre el que quieres hablar (todas las tiendas de la distribuidora).
- **Muestra**: un subconjunto de la población que realmente observas. Una muestra puede servir para opinar sobre la población solo si fue escogida con cuidado.
- **Censo**: cuando observas a **toda** la población, no a una parte.
- **Parámetro**: una cifra que describe a la población completa (el precio promedio de *todos* los artículos). Normalmente se desconoce.
- **Estadístico**: una cifra calculada con una muestra (el precio promedio de 4 artículos escogidos). Se usa para estimar el parámetro.
- **Variable estadística**: una característica que se mide en cada unidad (zona, monto, número de visitas). Equivale a una columna de la tabla. (No es lo mismo que una variable de programación, que es un nombre que guarda un valor.)
- **Variable cualitativa** (o categórica): describe una cualidad. Puede ser **nominal** (sin orden: zona, ruta) u **ordinal** (con orden natural: tamaño pequeño/mediano/grande).
- **Variable cuantitativa** (o numérica): describe una cantidad. Puede ser **discreta** (cuenta enteros: número de visitas) o **continua** (puede tomar decimales: monto en Bs, peso).

## Ejemplo paso a paso

**1. La unidad de análisis.** Mira la tabla de tiendas de la mini-base (12 filas):

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas.shape)
print(tiendas.head(3))
```

```salida
(12, 6)
   tienda_id           nombre              tipo    zona ruta  fecha_alta
0          1  Tienda La Palma  Tienda de barrio   Norte  R01  2025-02-10
1          2   Kiosco El Faro            Kiosco  Centro  R01  2025-03-01
2          3   Farmacia Salud          Farmacia  Centro  R02  2025-03-15
```

Cada fila es **una tienda**: esa es la unidad de análisis. Hay 12 filas y 6 columnas. Si estas 12 tiendas son *todas* las que tiene la distribuidora, tienes un **censo**; si son solo 12 de cientos, es una **muestra**. La misma tabla puede ser una u otra según cómo la pregunta defina la población, y eso cambia lo que puedes concluir.

**2. Clasificar las variables.**

| Columna | Qué mide | Tipo de variable | ¿Por qué? |
|---|---|---|---|
| `tienda_id` | identificador | cualitativa nominal | es un código; promediarlo no tiene sentido |
| `tipo` | tipo de negocio | cualitativa nominal | categorías sin orden |
| `zona`, `ruta` | ubicación | cualitativa nominal | categorías sin orden |
| `fecha_alta` | cuándo se registró | fecha (temporal) | se ordena en el tiempo; se trata aparte |
| `precio` (en `articulos`) | Bs | cuantitativa continua | puede tener decimales |
| `cantidad` (en `venta_lineas`) | unidades | cuantitativa discreta | cuenta enteros |
| nivel de stock «bajo/medio/alto» | clasificación | cualitativa ordinal | tiene un orden natural |

Un detalle que engaña: `tienda_id` y `ruta` son **números o códigos** pero no son cantidades. Un código como `R01` o un id `7` solo identifica; su promedio no significa nada.

**3. Parámetro frente a estadístico.** El catálogo `articulos` tiene 10 artículos. Si esos 10 son **toda** la población, su precio promedio es un **parámetro**:

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
print(articulos["precio"].mean())
```

```salida
8.1
```

Ahora imaginamos que solo pudimos revisar 4 artículos (una muestra) y calculamos su promedio, que es un **estadístico**:

```python
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
muestra = articulos.sample(n=4, random_state=3)
print(muestra[["nombre", "precio"]])
print(muestra["precio"].mean())
```

```salida
       nombre  precio
5    Maní 80g     5.0
4    Galletas     4.5
1     Jugo 1L     9.0
2  Gaseosa 2L    11.5
7.5
```

El estadístico (promedio de la muestra) no coincide con el parámetro (8,1): **una muestra da una estimación, no el valor exacto**. Con otra muestra el resultado sería otro. Esa variación entre muestras es la razón de ser de la inferencia (capítulo 12). (`random_state=3` fija el azar para que obtengas la misma muestra; sin él cada ejecución escogería otra.)

**4. El tipo importa para el cálculo.**

| Tipo | Resumen apropiado | Gráfico apropiado |
|---|---|---|
| cualitativa nominal | conteo, porcentaje, moda | barras |
| cualitativa ordinal | conteo, porcentaje, mediana | barras ordenadas |
| cuantitativa discreta/continua | media, mediana, desviación y otras medidas de posición | histograma, caja |

Calcular la «media de la ruta» no tiene sentido, pero contar cuántas tiendas hay en cada ruta, sí.

**5. Comprobar tipos en Pandas.** `dtypes` muestra cómo interpretó Pandas cada columna:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
print(lineas.dtypes)
```

```salida
linea_id             int64
venta_id             int64
articulo_id          int64
cantidad             int64
precio_unitario    float64
dtype: object
```

`int64` son enteros y `float64` decimales. Cuidado: Pandas no sabe que `venta_id` es un identificador y no una cantidad; lo trata como número. **Tú** decides qué columnas son medidas y cuáles códigos.

Ejemplo comercial: «el ticket promedio de nuestros clientes es de Bs 170» ¿habla de todos los clientes o solo de los que compraron en septiembre? Esa es la diferencia entre población y muestra, y cambia lo que se puede afirmar.

## Errores comunes

- **No definir la población** antes de interpretar un resultado.
- **Tratar un código (id, ruta, teléfono) como cantidad** y calcular promedios.
- **Confundir muestra con población** y presentar una estimación como una verdad exacta.
- **Usar el mismo cálculo para todos los tipos de variable.**
- **Creer que una muestra grande siempre es buena** aunque se haya escogido mal (se verá en 11.8).
- **Olvidar la unidad de análisis** y mezclar, por ejemplo, filas de líneas con filas de ventas.
- **Tratar una variable ordinal como si tuviera distancias iguales** entre categorías.

## Para comprobar que entendiste

1. ¿Qué es la unidad de análisis de la tabla `venta_lineas`?
2. ¿El precio de un artículo es discreto o continuo? ¿Y la cantidad vendida?
3. ¿Cuál es la diferencia entre parámetro y estadístico?
4. ¿Por qué no tiene sentido promediar `ruta`?

<details><summary>Respuestas</summary>

1. Una línea de venta: un artículo dentro de una venta.
2. El precio es continuo (admite decimales); la cantidad es discreta (unidades enteras).
3. El parámetro describe a toda la población; el estadístico se calcula con una muestra y la estima.
4. Porque es una categoría (código), no una cantidad.

</details>

## Micropráctica

1. Clasifica estas variables: número de visitas por semana, nombre del vendedor, temperatura de la cámara de frío, calificación del servicio (mala/regular/buena), código de producto.
2. Lee `ventas.csv` de la mini-base y di cuál es la unidad de análisis y cuántas unidades hay.
3. Toma una muestra de 5 filas de `venta_lineas` con `random_state=11` y compara el promedio de `cantidad` de la muestra con el de las 39 filas. ¿Coinciden? ¿Por qué?

Cómo saber que está bien: 1 → discreta, nominal, continua, ordinal, nominal; 2 → una venta, 16 unidades; en la 3 el promedio de la muestra es distinto al de la población.

<details><summary>Comprobación de las partes 2 y 3</summary>

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
print(len(ventas))

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
print(round(lineas["cantidad"].mean(), 2))
print(round(lineas.sample(n=5, random_state=11)["cantidad"].mean(), 2))
```

```salida
16
9.33
15.2
```

</details>

## Después, en los ejercicios

Los ejercicios de estadística ST01–ST04 ([`03_EJERCICIOS/Estadistica/`](../../03_EJERCICIOS/Estadistica/)) empiezan preguntando de qué población son los datos y de qué tipo son sus columnas. Anótalo antes de calcular. Siguiente: [11.2 Frecuencias y tablas](02_frecuencias.md).
