# 9.3 Inspeccionar los datos antes de usarlos (perfilado)

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisito: [9.2 Series, DataFrame y CSV](02_series_dataframe_csv.md).

## Para qué sirve

«Se ve bien en las primeras cinco filas» es la frase que precede a la mayoría de los reportes con errores. Antes de calcular nada, un analista **perfila** los datos: cuántas filas, qué tipos, cuántos vacíos, qué valores existen en cada columna categórica y si los números tienen sentido. Es el equivalente de revisar un almacén antes de hacer el inventario. Este hábito es la primera etapa de cualquier ETL.

## Términos nuevos

- **Perfilado de datos** (*profiling*): el examen sistemático de un conjunto de datos para conocer su estructura, tipos, vacíos, valores distintos y rangos, antes de transformarlo.
- **`info()`**: el método que muestra las columnas, la cantidad de datos no vacíos y el tipo de cada una.
- **`describe()`**: estadísticas rápidas de las columnas numéricas (y, si se pide, de las de texto).
- **`value_counts()`**: cuenta cuántas veces aparece cada valor de una columna.
- **`nunique()`**: cuántos valores distintos hay en una columna.
- **Cardinalidad de una columna**: cuántos valores distintos tiene. Una columna de `id` tiene tantos como filas; una de `estado` tiene muy pocos.
- **Valor inesperado**: uno fuera de lo que el diccionario de datos permite (un estado «entregdo», una cantidad negativa).
- **Diccionario de datos**: el documento que dice qué significa cada columna, su tipo y los valores válidos.

## Ejemplo paso a paso

**1. Las cuatro primeras preguntas (forma, tipos, vacíos, muestra).**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
print(lineas.shape)
lineas.info()
print(lineas.head(3))
```

```salida
(39, 5)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 39 entries, 0 to 38
Data columns (total 5 columns):
 #   Column           Non-Null Count  Dtype  
---  ------           --------------  -----  
 0   linea_id         39 non-null     int64  
 1   venta_id         39 non-null     int64  
 2   articulo_id      39 non-null     int64  
 3   cantidad         39 non-null     int64  
 4   precio_unitario  39 non-null     float64
dtypes: float64(1), int64(4)
memory usage: 1.7 KB
   linea_id  venta_id  articulo_id  cantidad  precio_unitario
0         1         1            1        10              6.0
1         2         1            4         6              7.5
2         3         1            9         4              8.0
```

`info()` lista las 5 columnas con su cantidad de valores **no vacíos** (39 en todas: no hay faltantes) y el tipo. Si una columna mostrara menos de 39, tendría vacíos. `head` es solo una muestra: no te dice nada sobre las otras 36 filas.

**2. Estadísticas numéricas.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
print(lineas[["cantidad", "precio_unitario"]].describe().round(2))
```

```salida
       cantidad  precio_unitario
count     39.00            39.00
mean       9.33             8.21
std        4.64             3.20
min        2.00             3.50
25%        6.00             6.00
50%        8.00             8.00
75%       12.00            11.50
max       20.00            14.00
```

Mira `min` y `max`: la cantidad va de 2 a 20 y el precio de 3,5 a 14. Si viera una cantidad de −5 o de 5000, tendría que investigarlo. `describe` es un detector de valores imposibles.

**3. Valores de las columnas categóricas.**

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
print(ventas["estado"].value_counts(dropna=False))
print(ventas["estado"].nunique())
```

```salida
estado
entregado    14
anulado       2
Name: count, dtype: int64
2
```

`value_counts(dropna=False)` incluye los vacíos en el conteo, para no ocultarlos. Aquí solo hay dos estados (`entregado`, `anulado`), que es lo que el diccionario permite. Esta es la forma de descubrir `Entregado`, `entregado ` (con espacio) o `ENTREGADO` como valores distintos.

**4. Datos sucios: lo que el perfilado encuentra.** Creamos un CSV con problemas típicos:

```python
import io
import pandas as pd

texto = """venta_id,fecha,estado,monto
1,2026-09-01,entregado,120.50
2,2026-09-02,Entregado,80
3,2026-09-02,entregado ,abc
4,2026-09-03,anulado,
4,2026-09-03,anulado,
5,,entregado,15000
"""
crudo = pd.read_csv(io.StringIO(texto))
crudo.info()
print(crudo["estado"].value_counts(dropna=False))
```

```salida
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 6 entries, 0 to 5
Data columns (total 4 columns):
 #   Column    Non-Null Count  Dtype 
---  ------    --------------  ----- 
 0   venta_id  6 non-null      int64 
 1   fecha     5 non-null      object
 2   estado    6 non-null      object
 3   monto     4 non-null      object
dtypes: int64(1), object(3)
memory usage: 324.0+ bytes
estado
entregado     2
anulado       2
Entregado     1
entregado     1
Name: count, dtype: int64
```

Qué ve un analista atento:

- `monto` salió de tipo **`object`** (texto), no numérico: algún valor no es número (`abc`). Tiene solo 4 no vacíos de 6 (`abc` es texto, no vacío, pero hay dos montos realmente vacíos).
- `fecha` tiene 5 no vacíos de 6: **falta una fecha**.
- `estado` tiene **tres variantes de «entregado»**: `entregado`, `Entregado` y `entregado ` (con espacio al final). Para Pandas son valores distintos.
- La venta 4 aparece **dos veces** (duplicado exacto).

**5. Una función de perfilado reutilizable.**

```python
import io
import pandas as pd


def perfil(df):
    resumen = pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "no_vacios": df.notna().sum(),
        "vacios": df.isna().sum(),
        "distintos": df.nunique(),
    })
    resumen["duplicados_totales"] = df.duplicated().sum()
    return resumen


texto = """venta_id,fecha,estado,monto
1,2026-09-01,entregado,120.50
2,2026-09-02,Entregado,80
3,2026-09-02,entregado ,abc
4,2026-09-03,anulado,
4,2026-09-03,anulado,
5,,entregado,15000
"""
print(perfil(pd.read_csv(io.StringIO(texto))))
```

```salida
            tipo  no_vacios  vacios  distintos  duplicados_totales
venta_id   int64          6       0          5                   1
fecha     object          5       1          3                   1
estado    object          6       0          4                   1
monto     object          4       2          4                   1
```

Una tabla compacta con tipo, vacíos y valores distintos de cada columna, y la cantidad de filas duplicadas. Es el tipo de resumen que guardas como evidencia en el ETL («Bronze tenía X vacíos y Y duplicados»).

**6. Listar el valor imposible.**

```python
import io
import pandas as pd

texto = """venta_id,fecha,estado,monto
1,2026-09-01,entregado,120.50
2,2026-09-02,entregado,80
4,2026-09-03,anulado,45
5,2026-09-04,entregado,15000
"""
df = pd.read_csv(io.StringIO(texto))
print(df["monto"].describe().round(1))
print(df.loc[df["monto"] > 1000])
```

```salida
count        4.0
mean      3811.4
std       7459.1
min         45.0
25%         71.2
50%        100.2
75%       3840.4
max      15000.0
Name: monto, dtype: float64
   venta_id       fecha     estado    monto
3         5  2026-09-04  entregado  15000.0
```

`describe` muestra un máximo de 15 000 con una media de 3 811: algo no cuadra. `df.loc[df["monto"] > 1000]` lista las filas sospechosas para revisarlas (¿15000 en lugar de 150.00? ¿una venta mayorista?). El perfilado **no decide**: encuentra y muestra; la decisión viene después, documentada.

**7. La lista de preguntas del perfilado.**

1. ¿Cuántas filas y columnas? ¿Coincide con lo esperado?
2. ¿Qué tipo tiene cada columna? ¿Es el que dice el diccionario?
3. ¿Cuántos vacíos tiene cada columna? ¿Alguno en un campo obligatorio?
4. ¿Cuántos valores distintos tiene cada columna? ¿La clave es única?
5. ¿Qué valores existen en las columnas categóricas? ¿Algún valor inesperado o variante de escritura?
6. ¿Qué rango tienen las numéricas? ¿Hay negativos, ceros o extremos?
7. ¿Hay filas duplicadas exactas o por clave?
8. ¿Las fechas están dentro del período esperado?

Ejemplo comercial: te entregan el archivo mensual de ventas. Antes de sumar, respondes las 8 preguntas y las guardas en una nota. Si el mes siguiente el perfil cambia (otro número de columnas, nuevo estado), lo detectas antes de que llegue a un reporte.

## Errores comunes

- **Confiar en `head()`.**
- **Ignorar el tipo `object` en una columna que debería ser numérica.**
- **Contar vacíos solo como `NaN`** sin revisar cadenas vacías o textos como «N/A», «-», «sin dato».
- **No mirar las variantes de escritura** de las categorías.
- **Borrar filas sospechosas sin documentar.**
- **Perfilar una sola vez**, sin repetir en cada carga.
- **No comparar con el diccionario de datos.**

## Para comprobar que entendiste

1. ¿Qué te dice que una columna de montos tenga tipo `object`?
2. ¿Qué hace `value_counts(dropna=False)` distinto a `value_counts()`?
3. ¿Qué indica `nunique()` en una columna de ids que debería ser única?
4. ¿Por qué `head()` no basta para perfilar?

<details><summary>Respuestas</summary>

1. Que al menos un valor no es número (texto, símbolo o vacío mal leído).
2. Incluye los vacíos en el conteo.
3. Que si es igual al número de filas, no hay ids repetidos.
4. Porque muestra solo unas filas, y los problemas suelen estar en otras.

</details>

## Micropráctica

1. Perfila `tiendas.csv`: forma, tipos, vacíos por columna, valores distintos y lista de tipos de tienda.
2. Perfila `visitas.csv` (mini-base): ¿qué columnas son 0/1? ¿Qué rango tiene la fecha?
3. Crea un CSV en memoria con 6 filas que contenga **tres** problemas distintos y escribe qué comando los detecta.

Cómo saber que está bien: `tiendas.csv` tiene 2 vacíos en `zona`; `visitas.csv` tiene fechas del 2026-09-01 al 2026-09-05.

<details><summary>Comprobación de la parte 1</summary>

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(tiendas.shape)
print(tiendas.isna().sum().to_dict())
print(tiendas.nunique().to_dict())
print(tiendas["tipo"].value_counts().to_dict())
```

```salida
(12, 6)
{'tienda_id': 0, 'nombre': 0, 'tipo': 0, 'zona': 2, 'ruta': 0, 'fecha_alta': 0}
{'tienda_id': 12, 'nombre': 12, 'tipo': 5, 'zona': 4, 'ruta': 3, 'fecha_alta': 12}
{'Tienda de barrio': 3, 'Kiosco': 3, 'Farmacia': 2, 'Minimarket': 2, 'Restaurante': 2}
```

</details>

## Después, en los ejercicios

El perfilado es el primer paso del mini-ETL y de P17–P20 en [Python](../../03_EJERCICIOS/Python/): guarda su resultado como evidencia en tu carpeta de trabajo. Siguiente: [9.4 Seleccionar y filtrar](04_seleccion_filtros.md).
