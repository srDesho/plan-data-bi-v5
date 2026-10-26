# 13.3 La tabla de fechas (calendario)

> Tiempo estimado: 45 min (lectura 20 + práctica 25). Prerrequisitos: [13.2 El modelo estrella](02_modelo_estrella.md) y [9.6 Fechas en Pandas](../09_Pandas_basico/06_tipos_textos_fechas.md).

## Para qué sirve

Casi toda pregunta de negocio es «por mes», «por semana» o «contra el mes anterior». Para que eso funcione sin errores (y para que Power BI pueda calcular «mes anterior» o «acumulado del año») necesitas una **tabla de fechas**: una dimensión con **todos** los días del período, incluso los días sin ventas. Sin ella, un mes sin ventas «desaparece» del gráfico en lugar de mostrarse como cero, y los cálculos de períodos anteriores fallan.

## Términos nuevos

- **Tabla de fechas** (o *calendario*): una dimensión con una fila por cada día del período, con atributos como año, mes y día de la semana.
- **Sin huecos**: que no falte ningún día entre la primera y la última fecha.
- **Fecha única**: que cada día aparezca una sola vez, sin vacíos.
- **Atributo de fecha**: una columna derivada del día (año, número de mes, nombre del mes, trimestre, día de la semana).
- **Columna de ordenamiento**: una columna numérica (`mes_numero`) para ordenar las etiquetas de texto (los nombres de mes se ordenarían alfabéticamente: abril, agosto, enero...).
- **Granularidad diaria**: el nivel de un día; si el dato trae hora, debe truncarse al día antes de relacionar.
- **Marcar como tabla de fechas**: en Power BI, indicar cuál es la tabla calendario para que funcionen las funciones de inteligencia de tiempo (mes anterior, acumulado).

## Ejemplo paso a paso

**1. Por qué los días sin ventas importan.** En la mini-base, las ventas entregadas de septiembre están en 8 días distintos; el mes tiene 30:

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
entregadas = ventas[ventas["estado"] == "entregado"]
septiembre = entregadas[entregadas["fecha"].str.startswith("2026-09")]

print(septiembre["fecha"].nunique(), "días con ventas de 30")
```

```salida
8 días con ventas de 30
```

Un gráfico diario que use solo las fechas de la tabla de ventas dibujará 8 puntos y unirá con línea días que no son contiguos, ocultando que hubo 22 días sin venta. Un calendario completo muestra cada día.

**2. Construir el calendario con Pandas.**

```python
import pandas as pd

fechas = pd.date_range("2026-08-01", "2026-09-30", freq="D")
dim_fecha = pd.DataFrame({"fecha": fechas})
dim_fecha["anio"] = dim_fecha["fecha"].dt.year
dim_fecha["mes_numero"] = dim_fecha["fecha"].dt.month
dim_fecha["mes_id"] = dim_fecha["fecha"].dt.strftime("%Y-%m")
dim_fecha["dia_semana"] = dim_fecha["fecha"].dt.dayofweek + 1
dim_fecha["es_fin_de_semana"] = dim_fecha["dia_semana"] >= 6
dim_fecha["fecha_id"] = dim_fecha["fecha"].dt.strftime("%Y-%m-%d")

print(len(dim_fecha))
print(dim_fecha.head(3).to_string(index=False))
print(dim_fecha["fecha"].is_unique, dim_fecha["fecha"].isna().sum())
```

```salida
61
     fecha  anio  mes_numero  mes_id  dia_semana  es_fin_de_semana   fecha_id
2026-08-01  2026           8 2026-08           6              True 2026-08-01
2026-08-02  2026           8 2026-08           7              True 2026-08-02
2026-08-03  2026           8 2026-08           1             False 2026-08-03
True 0
```

`pd.date_range(inicio, fin, freq="D")` genera **todos** los días entre ambas fechas (61: 31 de agosto y 30 de septiembre). Atributos: `anio`, `mes_numero` (1-12, para ordenar), `mes_id` (`2026-08`, para relacionar con los meses), `dia_semana` (lunes = 1) y una marca de fin de semana. `fecha_id` es la misma fecha como texto ISO.

**3. Comprobar el calendario: sin huecos, sin duplicados, sin vacíos.**

```python
import pandas as pd

dim_fecha = pd.DataFrame({"fecha": pd.date_range("2026-08-01", "2026-09-30", freq="D")})

dias_esperados = (dim_fecha["fecha"].max() - dim_fecha["fecha"].min()).days + 1
print(len(dim_fecha) == dias_esperados)
print(dim_fecha["fecha"].is_unique)
print(dim_fecha["fecha"].diff().dropna().unique())
```

```salida
True
True
<TimedeltaArray>
['1 days']
Length: 1, dtype: timedelta64[ns]
```

Tres controles: la cantidad de filas coincide con los días entre el primero y el último; no hay repetidos; y la diferencia entre días consecutivos siempre es de **1 día** (sin huecos). Un calendario con un hueco hace que los cálculos de «mes anterior» fallen.

**4. El calendario debe cubrir los datos.** Si una venta cae fuera del calendario, quedará huérfana:

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas["fecha"] = pd.to_datetime(ventas["fecha"], format="%Y-%m-%d")
dim_fecha = pd.DataFrame({"fecha": pd.date_range("2026-08-01", "2026-09-30", freq="D")})

huerfanas = (~ventas["fecha"].isin(dim_fecha["fecha"])).sum()
print(ventas["fecha"].min().date(), ventas["fecha"].max().date(), huerfanas)
```

```salida
2026-08-03 2026-09-29 0
```

Las ventas van del 3 de agosto al 29 de septiembre, dentro del calendario: 0 huérfanas. Regla: el calendario empieza **antes** de la primera fecha de los datos y termina **después** de la última (a menudo se extiende al año completo).

**5. Relacionar y agregar por día (con ceros).** Con el calendario se puede obtener el importe de **cada día**, incluidos los días sin ventas (con cero):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1")
base = base[base["estado"] == "entregado"].copy()
base["fecha"] = pd.to_datetime(base["fecha"])

por_dia = base.groupby("fecha", as_index=False)["importe"].sum()
dim_fecha = pd.DataFrame({"fecha": pd.date_range("2026-09-01", "2026-09-10", freq="D")})
resultado = dim_fecha.merge(por_dia, on="fecha", how="left", validate="1:1")
resultado["importe"] = resultado["importe"].fillna(0)
print(resultado.assign(fecha=resultado["fecha"].dt.strftime("%m-%d")).to_string(index=False))
```

```salida
fecha  importe
09-01      0.0
09-02    202.0
09-03      0.0
09-04     70.0
09-05      0.0
09-06      0.0
09-07      0.0
09-08    220.0
09-09      0.0
09-10    165.0
```

El `LEFT JOIN` desde el calendario conserva todos los días; los días sin venta quedan con `NaN` y se rellenan con **0** (aquí el cero sí es correcto: «no se vendió nada ese día»). Es la diferencia entre un gráfico honesto y uno que oculta los vacíos. (Con un faltante de otro tipo, como una meta ausente, el cero sería incorrecto: lección 6.6.)

**6. Ordenar los nombres de mes.** Si el eje de un gráfico usa el texto del mes, se ordena alfabéticamente (agosto antes que septiembre, pero «abril» antes que «febrero»). Por eso se mantiene `mes_numero` o `mes_id` (`2026-08`) y se indica que **ordene** por esa columna (en Power BI: «Ordenar por columna»). En el caso del curso `mes_id` con formato `AAAA-MM` se ordena bien como texto.

**7. En Power BI.** Marcar la tabla como tabla de fechas (la columna de fecha de tipo Date, sin nulos y sin huecos), relacionarla en 1:* con la fecha de cada hecho, y ocultar las columnas técnicas. La función que calcula el mes anterior o el acumulado del año depende de este calendario. Esos pasos de la interfaz **no se ejecutaron automáticamente** en este paquete; se comprueban manualmente (capítulo 14).

**8. Si el dato trae hora.** Una fecha con hora (`2026-09-18 14:35`) no coincide con el calendario diario. Antes de relacionar, se trunca al día: `df["fecha"].dt.normalize()` (o `dt.date`).

Ejemplo comercial: el gráfico «ventas por día de septiembre» debe mostrar 30 puntos, con ceros donde no hubo ventas. Con 8 puntos unidos por una línea parecería una operación continua que no existió.

## Errores comunes

- **Usar solo las fechas que aparecen en las ventas** como calendario.
- **Calendario con huecos** o fechas duplicadas.
- **Calendario que no cubre** todas las fechas de los datos.
- **Fechas con hora** relacionadas con un calendario diario.
- **Ordenar los meses alfabéticamente.**
- **Rellenar con 0 los faltantes** que en realidad son «sin dato».
- **No marcar la tabla de fechas** en Power BI.

## Para comprobar que entendiste

1. ¿Por qué el calendario debe incluir los días sin ventas?
2. ¿Qué tres controles debe pasar un calendario?
3. ¿Qué función de Pandas genera todos los días entre dos fechas?
4. ¿Por qué se necesita una columna `mes_numero`?

<details><summary>Respuestas</summary>

1. Para que los gráficos y cálculos de períodos incluyan los días sin actividad (con cero).
2. Fechas únicas sin vacíos, sin huecos y cubriendo todos los datos.
3. `pd.date_range(inicio, fin, freq="D")`.
4. Para ordenar los nombres de mes cronológicamente y no alfabéticamente.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Construye un calendario del 1 de julio al 31 de octubre de 2026 con año, mes, día de la semana y fin de semana. Comprueba que no tiene huecos.
2. Cuenta cuántos sábados y domingos tiene.
3. Calcula las ventas entregadas por semana ISO (`dt.isocalendar().week`) incluyendo semanas sin ventas.

Cómo saber que está bien: el calendario tiene 123 días (31 + 31 + 30 + 31); en la 3, las ventas entregadas suman 2 332,5 Bs en total y la semana ISO 33, sin ventas entregadas, aparece con 0.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import pandas as pd

cal = pd.DataFrame({"fecha": pd.date_range("2026-07-01", "2026-10-31", freq="D")})
cal["dia_semana"] = cal["fecha"].dt.dayofweek + 1
cal["fin_de_semana"] = cal["dia_semana"] >= 6
print(len(cal), cal["fecha"].diff().dropna().nunique())
print(int(cal["fin_de_semana"].sum()))
```

```salida
123 1
35
```

</details>

## Después, en los ejercicios

El calendario del proyecto de Power BI se genera con el exportador y se prueba con estos controles. Siguiente capítulo: [Capítulo 14 — Power BI](../14_PowerBI_DAX.md).
