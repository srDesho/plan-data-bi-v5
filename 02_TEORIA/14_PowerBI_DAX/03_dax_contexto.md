# 14.3 DAX: medidas y contexto de filtro

> Tiempo estimado: 70 min (lectura 35 + práctica 35). Prerrequisitos: [14.1](01_power_bi_desde_cero.md), [13.2 El modelo estrella](../13_Modelado/02_modelo_estrella.md) y [2.5 CASE](../02_SQL_agregados/05_case_coalesce.md).
>
> **Estado de verificación:** el código DAX de esta lección **no se ejecutó en Power BI Desktop**. Para que puedas comprobar lo que Desktop debería mostrar, cada medida tiene su resultado esperado calculado con Python sobre la mini-base (esas cifras sí están verificadas). Si Desktop da otro número, la diferencia es información valiosa: revisa relaciones, filtros y tipos.

## Para qué sirve

Una tabla de Excel guarda números; un tablero de Power BI **calcula** números según lo que el usuario está mirando. Cuando seleccionas la ruta R01 en un segmentador, «Ventas» pasa de mostrar el total a mostrar solo las de R01, sin que nadie reescriba la fórmula. Eso lo logra DAX con las **medidas** y el **contexto de filtro**. Entender el contexto es lo más importante de DAX: es la diferencia entre escribir fórmulas y entender por qué dan el resultado que dan.

## Términos nuevos

- **Medida**: una fórmula DAX que se calcula **al vuelo** según los filtros activos del visual. No guarda un valor por fila. Ejemplos: ventas totales, ticket medio, cumplimiento.
- **Columna calculada**: una columna cuyo valor se calcula **una vez por fila** al cargar el modelo y se guarda (ocupa memoria). Sirve para atributos (una etiqueta), no para totales.
- **Contexto de filtro**: el conjunto de filtros activos en el momento de calcular una medida: los segmentadores, las filas y columnas del visual, los filtros de página y de informe.
- **Contexto de fila**: el hecho de estar evaluando una fila concreta (en una columna calculada o dentro de un iterador como `SUMX`).
- **Agregador** (`SUM`, `COUNT`, `DISTINCTCOUNT`, `AVERAGE`, `MIN`, `MAX`): funciones que resumen una columna en el contexto de filtro actual.
- **Iterador** (`SUMX`, `AVERAGEX`): recorren una tabla fila por fila, evalúan una expresión y luego agregan.
- **`CALCULATE`**: la función que **modifica** el contexto de filtro: `CALCULATE(<medida>, <filtro>, ...)`.
- **`DIVIDE(a, b)`**: división segura: devuelve `BLANK()` si `b` es cero o vacío.
- **`BLANK()`**: el valor vacío de DAX (equivalente a NULL). No es lo mismo que 0.
- **`ALL` / `REMOVEFILTERS`**: quitan filtros del contexto. **`ALLSELECTED`**: quita los filtros de las filas y columnas del visual pero respeta los segmentadores.

## Ejemplo paso a paso

Modelo de ejemplo (lección 13.2): `fact_ventas` con `venta_id`, `tienda_id`, `ruta`, `articulo_id`, `mes`, `estado`, `cantidad` y `monto_centavos`; dimensiones `dim_tienda`, `dim_articulo`, etc.

**1. Una medida simple.**

```text
Ventas Bs =
DIVIDE(
    CALCULATE(SUM(fact_ventas[monto_centavos]), fact_ventas[estado] = "entregado"),
    100
)
```

Lectura de adentro hacia afuera:

1. `SUM(fact_ventas[monto_centavos])` suma la columna **en el contexto de filtro actual**.
2. `CALCULATE(..., fact_ventas[estado] = "entregado")` **agrega** el filtro «solo entregadas» a ese contexto.
3. `DIVIDE(..., 100)` convierte centavos en bolivianos, con protección ante un divisor vacío.

**2. Qué valor debería mostrar según el filtro.** Para entender el contexto, simulamos en Python lo que hace DAX: una función que calcula la medida **bajo un filtro** (las filas que el contexto deja pasar):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
fact["mes"] = fact["fecha"].str[:7]
fact["monto_centavos"] = (fact["cantidad"] * fact["precio_unitario"] * 100).round().astype(int)


def ventas_bs(contexto):
    """Simula: Ventas Bs = DIVIDE(CALCULATE(SUM(monto_centavos), estado = "entregado"), 100)"""
    filas = fact
    for columna, valor in contexto.items():
        filas = filas[filas[columna] == valor]
    filas = filas[filas["estado"] == "entregado"]
    total = filas["monto_centavos"].sum()
    return total / 100 if len(filas) else None


print("sin filtros:      ", ventas_bs({}))
print("ruta R01:         ", ventas_bs({"ruta": "R01"}))
print("mes 2026-09:      ", ventas_bs({"mes": "2026-09"}))
print("R01 y 2026-09:    ", ventas_bs({"ruta": "R01", "mes": "2026-09"}))
```

```salida
sin filtros:       2332.5
ruta R01:          1265.0
mes 2026-09:       1339.0
R01 y 2026-09:     800.0
```

Esto es lo que verías en una tarjeta de Power BI: sin segmentadores, 2 332,5; con la ruta R01 seleccionada, 1 265; con septiembre, 1 339; con ambos, 800. **La misma medida, cuatro resultados**: cada uno depende del contexto de filtro. No hay cuatro fórmulas; hay una, evaluada en cuatro contextos. En una matriz con ruta en las filas y mes en las columnas, **cada celda** es un contexto distinto.

**3. Medida frente a columna calculada.**

| | Columna calculada | Medida |
|---|---|---|
| Cuándo se calcula | al cargar/actualizar el modelo | al mostrar el visual |
| Dónde se guarda | en la tabla (ocupa memoria) | en ninguna parte (se recalcula) |
| Contexto | de fila | de filtro |
| Ejemplo adecuado | una etiqueta «alto/bajo» por artículo | ventas, ticket, cumplimiento |
| Ejemplo inadecuado | un total o un porcentaje | un atributo para usar en un segmentador |

Regla: **todo lo que se suma, se promedia o es una razón, es una medida.** Un ticket medio guardado como columna calculada no se «recalcula» al filtrar: sería el ticket de cada fila, no el del grupo.

**4. Medidas que se componen.** Las medidas se construyen unas sobre otras:

```text
Pedidos = CALCULATE(DISTINCTCOUNT(fact_ventas[venta_id]), fact_ventas[estado] = "entregado")
Ticket Bs = DIVIDE([Ventas Bs], [Pedidos])
```

`DISTINCTCOUNT` cuenta ventas **distintas** (no filas del hecho, que son líneas): el error de 3.4 y 10.2. El ticket es un cociente de dos medidas, así que se recalcula en cada contexto. Valores esperados (verificados con Python):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
fact["importe"] = fact["cantidad"] * fact["precio_unitario"]
ent = fact[fact["estado"] == "entregado"]

por_ruta = ent.groupby("ruta").agg(ventas_bs=("importe", "sum"), pedidos=("venta_id", "nunique"))
por_ruta["ticket_bs"] = (por_ruta["ventas_bs"] / por_ruta["pedidos"]).round(2)
total = pd.Series({"ventas_bs": ent["importe"].sum(), "pedidos": ent["venta_id"].nunique()})
total["ticket_bs"] = round(total["ventas_bs"] / total["pedidos"], 2)

print(por_ruta)
print(total.to_dict())
print(round(por_ruta["ticket_bs"].mean(), 2))
```

```salida
      ventas_bs  pedidos  ticket_bs
ruta                               
R01      1265.0        7     180.71
R02       510.0        4     127.50
R03       557.5        3     185.83
{'ventas_bs': 2332.5, 'pedidos': 14.0, 'ticket_bs': 166.61}
164.68
```

Una matriz por ruta mostraría: R01 1 265 / 7 pedidos / ticket 180,71; R02 510 / 4 / 127,50; R03 557,5 / 3 / 185,83; y el **total** 2 332,5 / 14 / **166,61**. Mira el total del ticket: **166,61** no es el promedio de los tres tickets de ruta (164,68). Porque la medida `Ticket` se evalúa en el contexto «sin filtros» como `DIVIDE(total ventas, total pedidos)`, no como promedio de las filas. Si hubieras guardado el ticket como columna, el total estaría mal. Esa es la ventaja de las medidas.

**5. `SUM` frente a `SUMX`.** `SUM(fact[monto])` suma una columna que ya existe. Si el importe no está guardado y hay que calcularlo fila por fila (`cantidad × precio`), se usa un iterador:

```text
Ventas Calculadas Bs =
CALCULATE(SUMX(fact_ventas, fact_ventas[cantidad] * fact_ventas[precio_unitario]), fact_ventas[estado] = "entregado")
```

`SUMX` recorre `fact_ventas` fila por fila (contexto de fila), multiplica y luego suma. El resultado debe ser **idéntico** a `Ventas Bs`: otra comprobación cruzada. (En este curso se exporta el monto en centavos para evitar el cálculo y el riesgo de redondeo.)

**6. `DIVIDE` y `BLANK`: no conviertas lo vacío en 0.** Si no hay meta para una ruta, `DIVIDE(ventas, meta)` devuelve `BLANK` y el visual muestra un espacio. Si lo cambiaras por 0 (`+ 0` o `COALESCE(..., 0)`), un «sin meta» pasaría a verse como «0 % de cumplimiento»: dos significados distintos (lección 6.6).

```text
Cumplimiento % = DIVIDE([Ventas Bs], [Meta Bs])
```

**7. Cómo leer una medida que no cuadra.** Procedimiento:

1. Pon la medida en una **tarjeta sin filtros** y compara con la cifra de control (2 332,5).
2. Si no coincide, revisa la medida: ¿filtra el estado? ¿divide entre 100?
3. Si coincide sin filtros pero no con un segmentador, el problema está en las **relaciones** (el filtro no llega al hecho) o en una dimensión con claves repetidas.
4. Si todo se multiplica, revisa la **unicidad de las dimensiones**.
5. Si una ruta cambia y el total no, revisa espacios y códigos en la unión.

Ejemplo comercial: el gerente selecciona «R03» y la tarjeta de ventas baja a 557,5 pero la de cumplimiento sigue mostrando el valor nacional. La causa: la meta está en una tabla que no está conectada a `dim_ruta`, así que el segmentador filtra las ventas pero no la meta. Es el caso de dimensiones conformadas de 13.2.

## Errores comunes

- **Guardar totales o porcentajes como columnas calculadas.**
- **Sumar medidas no aditivas** (tickets) en lugar de recalcularlas.
- **`COUNT` de filas del hecho** cuando se quieren documentos (`DISTINCTCOUNT`).
- **Convertir `BLANK` en 0** sin una regla de negocio.
- **No comprobar la medida en el contexto «sin filtros»** contra una cifra de control.
- **Relaciones que no propagan el filtro** a todas las tablas de hechos.
- **Confundir contexto de fila con contexto de filtro.**

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre una medida y una columna calculada?
2. ¿Por qué la misma medida da distintos valores en distintas celdas de una matriz?
3. ¿Qué hace `CALCULATE` con el contexto de filtro?
4. ¿Por qué el ticket total no es el promedio de los tickets de las rutas?

<details><summary>Respuestas</summary>

1. La medida se calcula al vuelo según los filtros; la columna calculada se calcula una vez por fila al cargar y se guarda.
2. Porque cada celda tiene un contexto de filtro distinto (otra ruta, otro mes).
3. Lo modifica: agrega, cambia o quita filtros para la expresión que envuelve.
4. Porque la medida divide el total de ventas entre el total de pedidos en ese contexto; promediar tickets de grupos de distinto tamaño da otro resultado.

</details>

## Micropráctica

1. Escribe en DAX la medida `Unidades Entregadas` (suma de `cantidad` de ventas entregadas).
2. Calcula con Python el valor esperado sin filtros, con la ruta R02 y con septiembre.
3. Escribe una medida `Pct Anuladas` = ventas anuladas / ventas totales (por documentos distintos). Calcula su valor esperado.
4. Explica qué verías en una tarjeta si el segmentador de ruta no estuviera conectado al hecho.

Cómo saber que está bien: sin filtros, las unidades entregadas son 323.

<details><summary>Comprobación de las partes 2 y 3</summary>

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
ent = fact[fact["estado"] == "entregado"]

print(ent["cantidad"].sum(), ent[ent["ruta"] == "R02"]["cantidad"].sum(), ent[ent["fecha"].str.startswith("2026-09")]["cantidad"].sum())
anuladas = fact[fact["estado"] == "anulado"]["venta_id"].nunique()
print(anuladas, fact["venta_id"].nunique(), round(anuladas / fact["venta_id"].nunique() * 100, 1))
```

```salida
323 80 186
2 16 12.5
```

</details>

## Después, en los ejercicios

Las medidas del proyecto de Power BI se escriben una por una a partir de `medidas.dax` ([`05_PROYECTOS/powerbi/`](../../05_PROYECTOS/)): selecciona el nombre y la expresión de cada bloque; el archivo es texto de referencia, no una importación automática. Siguiente: [14.4 Medidas útiles y su control](04_medidas_utiles.md).
