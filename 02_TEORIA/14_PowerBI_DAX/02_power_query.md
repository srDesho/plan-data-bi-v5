# 14.2 Power Query y el lenguaje M

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [14.1 Power BI desde cero](01_power_bi_desde_cero.md) y [9.6 Tipos, textos y fechas](../09_Pandas_basico/06_tipos_textos_fechas.md).
>
> **Estado de verificación:** el código M de esta lección **no se ejecutó en Power BI Desktop**; cada transformación tiene su equivalente en Pandas, que sí se ejecutó y sirve para comprobar el resultado esperado.

## Para qué sirve

Power Query es el «mini-ETL» de Power BI: cada vez que actualizas el informe, vuelve a ejecutar una lista de pasos sobre los datos de la fuente. Escribirlo bien significa que el informe se actualiza solo y sin sorpresas. Como conoces Pandas, lo más útil es entender qué hace cada paso de Power Query en términos de lo que ya sabes.

## Términos nuevos

- **Consulta** (*query*): una secuencia de pasos que obtiene y transforma una tabla.
- **Paso aplicado**: cada transformación de una consulta, guardada en orden. Si cambias un paso intermedio, los siguientes se vuelven a calcular.
- **Fórmula M**: el código que genera Power Query para cada paso. Se ve en el *Editor avanzado*.
- **`let ... in`**: la estructura de una consulta M: `let` define los pasos con nombre y `in` indica cuál es el resultado.
- **Tipo de columna**: el tipo asignado (número entero, decimal, texto, fecha). Se cambia con `Table.TransformColumnTypes`.
- **Cultura (`"es-BO"`, `"en-US"`)**: la configuración regional que se usa al convertir texto a número o fecha.
- **Combinar consultas** (*merge*): unir dos consultas por una clave (equivale a `merge`/`JOIN`). **Anexar** (*append*): apilar filas de dos tablas (equivale a `concat`/`UNION ALL`).
- **Plegado de consultas** (*query folding*): cuando Power Query traduce tus pasos a una consulta SQL que ejecuta la propia base de datos. Con CSV no existe.

## Ejemplo paso a paso

Partimos del archivo `ventas.csv` de la mini-base. El resultado que queremos: una tabla de ventas con tipos correctos, estado normalizado, mes y sin duplicados.

**1. La consulta completa en M** (texto de referencia):

```text
let
    Origen = Csv.Document(File.Contents("C:\datos\ventas.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {
        {"venta_id", Int64.Type}, {"tienda_id", Int64.Type}, {"vendedor_id", Int64.Type},
        {"fecha", type date}, {"estado", type text}}, "en-US"),
    EstadoLimpio = Table.TransformColumns(Tipos, {{"estado", each Text.Lower(Text.Trim(_)), type text}}),
    ConMes = Table.AddColumn(EstadoLimpio, "mes", each Date.ToText([fecha], "yyyy-MM"), type text),
    SinDuplicados = Table.Distinct(ConMes, {"venta_id"})
in
    SinDuplicados
```

Cada línea es un **paso**; cada uno recibe como entrada el resultado del paso anterior. Lectura: *Origen* abre el CSV (UTF-8, código 65001); *Encabezados* usa la primera fila como nombres; *Tipos* convierte columnas, y la cultura `"en-US"` al final indica que las fechas ISO y los números se leen con punto decimal; *EstadoLimpio* pasa a minúsculas y quita espacios; *ConMes* añade una columna `mes`; *SinDuplicados* deja una fila por `venta_id`. No pegues este código sin ajustar la ruta del archivo a tu equipo.

**2. El mismo resultado en Pandas** (esto sí se ejecuta, y fija el resultado esperado):

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas["fecha"] = pd.to_datetime(ventas["fecha"], format="%Y-%m-%d")
ventas["estado"] = ventas["estado"].str.strip().str.lower()
ventas["mes"] = ventas["fecha"].dt.strftime("%Y-%m")
ventas = ventas.drop_duplicates(subset=["venta_id"])

print(len(ventas))
print(ventas["estado"].value_counts().to_dict())
print(ventas["mes"].value_counts().sort_index().to_dict())
print(ventas.dtypes.astype(str).to_dict())
```

```salida
16
{'entregado': 14, 'anulado': 2}
{'2026-08': 7, '2026-09': 9}
{'venta_id': 'int64', 'tienda_id': 'int64', 'vendedor_id': 'int64', 'fecha': 'datetime64[ns]', 'estado': 'object', 'mes': 'object'}
```

Resultado de control: 16 filas, 14 `entregado` y 2 `anulado`, 7 ventas en agosto y 9 en septiembre. Cuando ejecutes la consulta M en Desktop, la vista previa y el pie de la tabla deben mostrar las mismas cifras. Si no, hay una diferencia de tipos, de cultura o de limpieza.

**3. La tabla de equivalencias.**

| Qué quieres hacer | Interfaz de Power Query | Función M | Pandas |
|---|---|---|---|
| usar la primera fila como encabezado | «Usar primera fila como encabezado» | `Table.PromoteHeaders` | `read_csv` ya lo hace |
| cambiar el tipo | clic en el icono del tipo | `Table.TransformColumnTypes` | `astype`, `to_numeric`, `to_datetime` |
| filtrar filas | filtro del encabezado | `Table.SelectRows` | `df[df["x"] == v]` |
| quitar columnas | «Quitar columnas» | `Table.RemoveColumns` | `df.drop(columns=...)` |
| quitar duplicados | «Quitar duplicados» | `Table.Distinct` | `drop_duplicates` |
| reemplazar valores | «Reemplazar valores» | `Table.ReplaceValue` | `replace` |
| columna condicional | «Columna condicional» | `if … then … else` | `np.where`, `np.select` |
| combinar consultas (join) | «Combinar consultas» | `Table.NestedJoin` | `merge` |
| anexar consultas | «Anexar consultas» | `Table.Combine` | `concat` |
| agrupar | «Agrupar por» | `Table.Group` | `groupby` |

**4. Una columna condicional (el `CASE` de M).** Sobre una consulta de artículos (`TiposArticulos` es el paso donde ya se fijaron los tipos de `articulos.csv`):

```text
ConSegmento = Table.AddColumn(TiposArticulos, "segmento",
    each if [precio] < 6 then "económico" else if [precio] <= 10 then "medio" else "alto", type text)
```

El equivalente en Pandas, para el resultado esperado (3 económicos, 4 medios, 3 altos, ya vistos en 2.5):

```python
import numpy as np
import pandas as pd

articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
articulos["segmento"] = np.select([articulos["precio"] < 6, articulos["precio"] <= 10], ["económico", "medio"], default="alto")
print(articulos["segmento"].value_counts().to_dict())
```

```salida
{'medio': 4, 'alto': 3, 'económico': 3}
```

**5. Combinar consultas: la trampa de siempre.** Al combinar `fact_ventas` con `dim_tienda` por `tienda_id`, Power Query ofrece los tipos de unión (interna, izquierda externa...). Para traer atributos de una dimensión a un hecho, usa **izquierda externa** y revisa después que (a) el número de filas del hecho no cambió y (b) no hay valores nulos en las columnas traídas (huérfanas). Es exactamente el control de `merge(..., validate="m:1", indicator=True)`.

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
r = ventas.merge(tiendas[["tienda_id", "zona"]], on="tienda_id", how="left", validate="m:1", indicator=True)
print(len(ventas), len(r), r["_merge"].value_counts().to_dict(), int(r["zona"].isna().sum()))
```

```salida
16 16 {'both': 16, 'left_only': 0, 'right_only': 0} 1
```

16 filas antes y después, ninguna huérfana; la columna `zona` trae 1 vacío porque la tienda 5 **no tiene zona** (un dato faltante de origen, no una huérfana). Distinguir ambos casos es importante: una huérfana es una clave sin pareja; una zona vacía es un atributo faltante.

**6. Actualización y errores.** Al actualizar, los pasos se repiten con los datos nuevos. Fallas típicas:

| Mensaje / síntoma | Causa probable | Qué revisar |
|---|---|---|
| «No se encontró la columna X» | cambió el nombre en el origen | encabezados del archivo |
| «No se puede convertir en Número» | un valor de texto en una columna numérica | la fila problemática; limpiar o rechazar |
| totales distintos tras actualizar | filas duplicadas nuevas o cambio de formato | duplicados y tipos |
| rutas que no funcionan en otro equipo | la ruta del archivo está escrita fija | usar parámetros de ruta |

Una columna que falla al convertir muestra «Error» en las celdas; **no las ocultes**: cuenta cuántas son y decide (corregir el origen, rechazarlas o quitarlas con justificación).

**7. Parámetros: la ruta no va escrita dentro.** En Power Query puedes crear un **parámetro** (por ejemplo `RutaDatos`) y usarlo en `File.Contents(RutaDatos & "ventas.csv")`. Así otra persona cambia el parámetro y no el código. Es el equivalente a recibir rutas como argumentos en tu ETL (lección 5.4).

Ejemplo comercial: la consulta de ventas se actualiza cada mañana con el CSV nuevo. Porque los tipos están fijados, el estado se normaliza y las duplicadas se quitan, el tablero no cambia sin que alguien lo note; y si el archivo llega con una columna menos, la actualización falla con un mensaje claro en lugar de mostrar cifras silenciosamente equivocadas.

## Errores comunes

- **Dejar el tipo «Cualquiera»** en columnas que deben ser números o fechas.
- **No fijar la cultura** al convertir.
- **Combinar con unión interna** y perder filas sin darte cuenta.
- **Ocultar los errores de conversión** en lugar de contarlos.
- **Rutas escritas dentro de la consulta.**
- **Transformar en Power Query lo que debió resolver el ETL.**
- **Cambiar un paso intermedio** sin revisar qué pasa con los siguientes.

## Para comprobar que entendiste

1. ¿Qué es un paso aplicado y cómo se relaciona con el siguiente?
2. ¿Qué equivalente de Pandas tiene «Combinar consultas»?
3. ¿Por qué se fija la cultura al convertir tipos?
4. ¿Cómo distingues una huérfana de un atributo faltante?

<details><summary>Respuestas</summary>

1. Una transformación guardada; cada paso recibe como entrada el resultado del anterior.
2. `merge` (con `how` y `validate`).
3. Para que decimales, miles y fechas se lean con las reglas correctas del archivo.
4. La huérfana es una clave sin pareja en la otra tabla; el atributo faltante es una fila emparejada cuyo atributo está vacío.

</details>

## Micropráctica

1. Escribe en papel la lista de pasos de Power Query que aplicarías a `venta_lineas.csv` (tipos, columna `importe_centavos`, quitar duplicados por `linea_id`).
2. Calcula con Pandas el resultado esperado (filas y suma de `importe_centavos`) para compararlo en Desktop.
3. Describe qué harías si el campo `cantidad` tuviera el texto `"3 uds"` en una fila.

Cómo saber que está bien: 39 filas y 272 150 centavos.

<details><summary>Comprobación de la parte 2</summary>

```python
import pandas as pd

l = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv").drop_duplicates(subset=["linea_id"])
l["importe_centavos"] = (l["cantidad"] * l["precio_unitario"] * 100).round().astype(int)
print(len(l), int(l["importe_centavos"].sum()))
```

```salida
39 272150
```

</details>

## Después, en los ejercicios

Aplica estas transformaciones en el proyecto de Power BI ([`05_PROYECTOS/powerbi/`](../../05_PROYECTOS/)). Siguiente: [14.3 DAX: medidas y contexto de filtro](03_dax_contexto.md).
