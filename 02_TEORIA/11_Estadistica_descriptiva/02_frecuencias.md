# 11.2 Frecuencias: contar y expresar en porcentaje

> Tiempo estimado: 45 min (lectura 20 + práctica 25). Prerrequisito: [11.1 Población, muestra y variables](01_poblacion_muestra_variables.md).

## Recorrido inicial sin Pandas

La tabla manual del primer ejemplo y las microprácticas existentes se pueden resolver antes de aprender DataFrame. Abre los CSV como texto, conserva una marca por observación y cuenta por categoría. Frecuencia relativa = conteo de la categoría dividido entre el número total de observaciones; porcentaje = esa fracción por 100. Comprueba que los conteos sumen el total y las proporciones sumen 1, admitiendo el redondeo al presentar porcentajes.

Para los intervalos de precios de la micropráctica conserva los límites indicados: `(0, 5]` incluye 5 y excluye 0; `(5, 10]` incluye 10 y excluye 5. Acumula solamente cuando existe un orden. Mientras aún no conozcas Pandas, las tablas impresas permiten comprobar el método; `value_counts`, `pd.cut` y la reproducción con Pandas se retoman después de D15 (9.2) y no se acreditan por haber leído el código.

## Para qué sirve

La forma más simple y más usada de describir datos es **contar**: cuántas tiendas hay de cada tipo, cuántas ventas cayeron en cada estado, cuántos días estuvieron en cada rango de ventas. Una tabla de frecuencias convierte una columna de miles de filas en pocas líneas que se pueden leer, comparar y graficar.

## Términos nuevos

- **Frecuencia absoluta**: cuántas veces aparece un valor (o categoría). La suma de todas es el total de observaciones `n`.
- **Frecuencia relativa**: la frecuencia absoluta dividida entre `n`. Es una fracción entre 0 y 1; suma 1.
- **Porcentaje**: la frecuencia relativa multiplicada por 100. Suma 100 %.
- **Frecuencia acumulada**: la suma de las frecuencias hasta una categoría (solo tiene sentido si las categorías tienen orden).
- **Tabla de frecuencias**: la tabla que lista cada categoría con sus frecuencias.
- **Intervalo de clase** (o *bin*): un tramo de valores, como «de 0 a 10», usado para agrupar una variable numérica.
- **Moda**: el valor más frecuente.

## Ejemplo paso a paso

**1. Cálculo a mano con una variable categórica.** Los 12 tipos de tienda de `tiendas.csv`, contados:

| Tipo | Frecuencia absoluta | Frecuencia relativa | Porcentaje |
|---|---|---|---|
| Tienda de barrio | 3 | 3/12 = 0,25 | 25,0 % |
| Kiosco | 3 | 3/12 = 0,25 | 25,0 % |
| Farmacia | 2 | 2/12 = 0,1667 | 16,7 % |
| Minimarket | 2 | 2/12 = 0,1667 | 16,7 % |
| Restaurante | 2 | 2/12 = 0,1667 | 16,7 % |
| **Total** | **12** | **1,0000** | **100,1 %** (por redondeo) |

Observa la última fila: los porcentajes redondeados suman 100,1 %, no 100. Es un efecto de redondear tres veces 16,67 a 16,7; no es un error de conteo. Cuando presentes una tabla así, aclara «los porcentajes pueden no sumar 100 por redondeo». Las dos modas son «Tienda de barrio» y «Kiosco» (empatan con 3).

**2. La misma tabla con Pandas.** `value_counts` cuenta las apariciones:

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
conteo = tiendas["tipo"].value_counts()
print(conteo)
print(round(tiendas["tipo"].value_counts(normalize=True) * 100, 1))
```

```salida
tipo
Tienda de barrio    3
Kiosco              3
Farmacia            2
Minimarket          2
Restaurante         2
Name: count, dtype: int64
tipo
Tienda de barrio    25.0
Kiosco              25.0
Farmacia            16.7
Minimarket          16.7
Restaurante         16.7
Name: proportion, dtype: float64
```

El primer resultado son las frecuencias absolutas; el segundo (`normalize=True`) las relativas, que multiplicamos por 100 para ver porcentajes. **Compara con tu tabla a mano**: tienen que coincidir. Si hay valores vacíos, `value_counts` los **omite** por defecto; para verlos usa `dropna=False`:

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas["zona"].value_counts(dropna=False))
```

```salida
zona
Centro        4
Norte         3
NaN           2
Plan 3000     2
Equipetrol    1
Name: count, dtype: int64
```

Aquí la zona vacía aparece como `NaN` con 2 tiendas. Un conteo que omite los vacíos suma 10, no 12: decide y escribe si los vacíos van o no en el denominador.

**3. Frecuencia de una variable numérica: agrupar en intervalos.** Cantidades de las 39 líneas de venta. Con una variable numérica, contar cada valor distinto no ayuda; se agrupan en tramos. Elegimos tramos de ancho 5:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
tramos = pd.cut(lineas["cantidad"], bins=[0, 5, 10, 15, 20], right=True)
tabla = tramos.value_counts(sort=False)
print(tabla)
print(tabla.sum())
```

```salida
cantidad
(0, 5]       7
(5, 10]     21
(10, 15]     7
(15, 20]     4
Name: count, dtype: int64
39
```

Con `right=True` cada tramo **incluye el límite derecho** y excluye el izquierdo: `(5, 10]` contiene 6, 7, 8, 9 y 10. Comprobación obligatoria: la suma de frecuencias debe ser 39, el total de líneas. Si no suma, algún valor cayó fuera de los tramos (por ejemplo, una cantidad de 25 quedaría excluida y aparecería como valor perdido).

**4. Frecuencia acumulada.** Para variables ordenadas, ¿qué porcentaje de las líneas tiene 10 unidades o menos?

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
tramos = pd.cut(lineas["cantidad"], bins=[0, 5, 10, 15, 20])
absoluta = tramos.value_counts(sort=False)
acumulada = absoluta.cumsum()
print(acumulada)
print(round(acumulada / absoluta.sum() * 100, 1))
```

```salida
cantidad
(0, 5]       7
(5, 10]     28
(10, 15]    35
(15, 20]    39
Name: count, dtype: int64
cantidad
(0, 5]       17.9
(5, 10]      71.8
(10, 15]     89.7
(15, 20]    100.0
Name: count, dtype: float64
```

La última acumulada siempre es el total (39, o 100 %). La acumulada responde preguntas del tipo «¿qué proporción está por debajo de X?».

**5. Cuidado con la lectura.** «Hay 3 kioscos y 2 farmacias» es una **frecuencia**, no una importancia: no dice quién vende más. Para eso necesitarías otra variable (ventas) agrupada por tipo. Y un porcentaje sin su `n` engaña: «50 % de los clientes compró» no es lo mismo con n = 2 que con n = 200.

Ejemplo comercial: la distribución de ventas por estado (entregado/anulado) es una tabla de frecuencias. Si el porcentaje de anuladas sube de un mes a otro, el primer paso es ver las frecuencias absolutas para saber si es un cambio real o de pocas ventas.

## Errores comunes

- **Mostrar porcentajes sin el total `n`.**
- **Ignorar los valores vacíos** en el conteo sin decirlo.
- **Elegir intervalos que dejen valores fuera** o que se solapen.
- **No saber si el límite del intervalo se incluye** (`right=True` o `False`).
- **Pensar que los porcentajes redondeados deben sumar exactamente 100.**
- **Interpretar la frecuencia de categorías como importancia comercial.**
- **Calcular acumuladas de una variable sin orden** (zona, ruta).

## Para comprobar que entendiste

1. Si una categoría aparece 6 veces entre 40 observaciones, ¿cuál es su frecuencia relativa y su porcentaje?
2. ¿Por qué la suma de los porcentajes puede dar 100,1 %?
3. ¿Qué pasa con los valores vacíos en `value_counts()`?
4. En `pd.cut` con `right=True`, ¿a qué tramo pertenece el valor 10 si los tramos son (5, 10] y (10, 15]?

<details><summary>Respuestas</summary>

1. 6/40 = 0,15; 15 %.
2. Por el redondeo de cada porcentaje individual.
3. Se omiten por defecto; con `dropna=False` se muestran.
4. Al tramo (5, 10], porque el límite derecho se incluye.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Construye **a mano** la tabla de frecuencias (absoluta, relativa y porcentaje) de `categoria` en `articulos.csv`. Después verifícala con `value_counts`.
2. Calcula el porcentaje de ventas por estado (`ventas.csv`) y comprueba que suma 100.
3. Agrupa `precio` de `articulos.csv` en tramos [0–5, 5–10, 10–15] y construye la tabla con frecuencia acumulada. Comprueba que el total es 10.

Cómo saber que está bien: 1 → Bebidas 3 (30 %), Snacks 3 (30 %), Limpieza 2 (20 %), Lácteos 2 (20 %); 2 → 14 entregadas (87,5 %) y 2 anuladas (12,5 %).

<details><summary>Comprobación de las partes 2 y 3</summary>

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
print(ventas["estado"].value_counts(normalize=True) * 100)

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
tramos = pd.cut(articulos["precio"], bins=[0, 5, 10, 15])
absoluta = tramos.value_counts(sort=False)
print(absoluta)
print(absoluta.cumsum())
```

```salida
estado
entregado    87.5
anulado      12.5
Name: proportion, dtype: float64
precio
(0, 5]      3
(5, 10]     4
(10, 15]    3
Name: count, dtype: int64
precio
(0, 5]       3
(5, 10]      7
(10, 15]    10
Name: count, dtype: int64
```

</details>

## Después, en los ejercicios

Los conteos y porcentajes aparecen en ST01–ST04 de [Estadística](../../03_EJERCICIOS/Estadistica/) y en el caso C03. Siguiente: [11.3 Media, mediana y moda](03_media_mediana_moda.md).
