# 13.2 El modelo estrella: relaciones y varios hechos

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisito: hechos, dimensiones y granularidad, introducidos a continuación; [13.1 Hechos y dimensiones](01_hechos_dimensiones.md) queda como REFUERZO.

## Para qué sirve

Cuando ya tienes hechos y dimensiones, hay que **conectarlos** de forma que filtrar por una dimensión filtre bien todos los hechos, sin multiplicar nada ni crear caminos ambiguos. La forma que lo logra se llama modelo estrella. Es el diseño que usarás en Power BI y que explica por qué las cifras de presupuesto y ventas se pueden mostrar juntas sin duplicarse.

## Términos nuevos

- **Tabla de hechos**: registra eventos medibles y las claves que permiten describirlos. En `fact_ventas`, una fila es una línea de venta; cantidad e importe son sus medidas.
- **Tabla de dimensión**: describe el contexto de esos eventos. En `dim_tienda`, una fila es una tienda con clave única y atributos como nombre o zona; esa tienda puede aparecer en muchas líneas del hecho.
- **Granularidad o grano**: qué representa exactamente una fila. Se decide antes de relacionar: una línea de venta, una visita o una meta por ruta y mes son granos distintos.
- **Modelo estrella** (*star schema*): un diseño con una o más tablas de hechos en el centro y sus dimensiones alrededor, como los puntos de una estrella. Cada relación va de una dimensión (lado «uno») al hecho (lado «muchos»).
- **Relación uno a muchos (1:*)**: una fila de la dimensión corresponde a muchas filas del hecho.
- **Dirección del filtro**: el sentido en que un filtro viaja entre tablas. Lo normal es de la dimensión hacia el hecho (en un solo sentido).
- **Dimensión conformada**: una dimensión que se comparte entre varios hechos (`dim_ruta` conecta metas, ventas y visitas), de modo que un mismo filtro afecta a todos.
- **Relación muchos a muchos**: ambas tablas tienen claves repetidas. Puede ocultar un defecto de claves y se evita en este diseño.
- **Camino ambiguo**: cuando dos rutas distintas conectan las mismas tablas; el motor no sabe cuál usar y el resultado es impredecible.
- **Copo de nieve** (*snowflake*): variante donde las dimensiones se dividen en subdimensiones. En este curso se usa el diseño estrella simple.

## Ejemplo paso a paso

**Antes de dibujar relaciones: distinguir evento, contexto y grano.** Con las tablas de la mini-base, explica sin mirar el párrafo siguiente qué representa una fila de `venta_lineas`, de `tiendas` y de `metas`. ¿Cuál registra el evento que sumas, cuál lo describe y en cuál necesitas dos columnas para identificar una fila? Predice qué ocurriría si copiaras una meta mensual en cada línea de venta de su ruta.

Comprobación: `venta_lineas` prepara el hecho de ventas con grano de línea; `tiendas` prepara una dimensión con una fila por tienda y clave `tienda_id`; `metas` prepara otro hecho con una cifra por pareja `(mes, ruta)`. La meta no pertenece a cada línea: repetirla allí inflaría su suma. Mantener los hechos separados y conectarlos por dimensiones compartidas conserva su significado.

Modelo del curso (adaptado a la mini-base):

```text
dim_tienda ─────┐
dim_articulo ───┤
dim_vendedor ───┼──► fact_ventas   (granularidad: línea de venta)
dim_fecha ──────┘

dim_ruta ───────┬──► fact_ventas   (por medio de la ruta de la tienda)
                ├──► fact_metas    (granularidad: ruta y mes)
                └──► fact_visitas  (granularidad: visita planificada)
dim_mes ────────┬──► fact_ventas
                └──► fact_metas
```

**1. ¿Por qué `dim_ruta` y `dim_mes` aparte?** Porque las metas tienen granularidad **ruta + mes**. Para filtrar ventas y metas con el mismo selector de ruta o de mes, ambas deben relacionarse con **la misma dimensión**: `dim_ruta` y `dim_mes`. Así un segmentador de «ruta R01» afecta ventas, metas y visitas a la vez.

**2. Construirlas.**

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")

dim_ruta = pd.DataFrame({"ruta": sorted(tiendas["ruta"].unique())})
dim_mes = pd.DataFrame({"mes": sorted(ventas["fecha"].str[:7].unique())})

print(dim_ruta["ruta"].tolist(), dim_ruta["ruta"].is_unique)
print(dim_mes["mes"].tolist(), dim_mes["mes"].is_unique)
print(len(metas), metas.duplicated(subset=["mes", "ruta"]).sum())
```

```salida
['R01', 'R02', 'R03'] True
['2026-08', '2026-09'] True
6 0
```

Las dimensiones nuevas tienen una fila por elemento y clave única; `metas` tiene 6 filas y **ningún par (mes, ruta) repetido**, así que su relación con `dim_ruta` y `dim_mes` es de muchos a uno.

**3. La prueba de que las metas no se multiplican.** Calcular el vendido por ruta y mes desde el hecho, y la meta desde su hecho, y compararlos **por las dimensiones**:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
fact["mes"] = fact["fecha"].str[:7]
fact["importe"] = fact["cantidad"] * fact["precio_unitario"]
entregado = fact[fact["estado"] == "entregado"]

vendido = entregado.groupby(["mes", "ruta"], as_index=False)["importe"].sum()
tabla = metas.merge(vendido, on=["mes", "ruta"], how="left", validate="1:1")
tabla["importe"] = tabla["importe"].fillna(0)

print(tabla[["mes", "ruta", "meta_bs", "importe"]])
print(metas["meta_bs"].sum(), tabla["meta_bs"].sum())
```

```salida
       mes ruta  meta_bs  importe
0  2026-08  R01    450.0    465.0
1  2026-08  R02    280.0    131.0
2  2026-08  R03    320.0    397.5
3  2026-09  R01    600.0    800.0
4  2026-09  R02    450.0    379.0
5  2026-09  R03    300.0    160.0
2400.0 2400.0
```

La suma de metas antes (2 400) y después de combinar (2 400) es la misma: la combinación a nivel **(mes, ruta)** no multiplica la meta. En Power BI, el equivalente es que un segmentador de mes y ruta filtre ambas tablas de hechos a través de las dimensiones compartidas.

**4. Qué relaciones NO crear.** No conectar `dim_ruta` con `dim_tienda` **y** con `fact_ventas` a la vez, porque habría dos caminos para llegar a las ventas desde la ruta: uno directo y otro por tienda. Un camino ambiguo genera resultados impredecibles. Regla: **un solo camino entre dos tablas**. En este diseño se agrega al hecho de ventas su propia columna `ruta` (copiada de la tienda al construir el hecho, como hicimos en el paso 3), de modo que `dim_ruta → fact_ventas` es una relación directa y `dim_tienda` mantiene sus atributos sin relacionarse con `dim_ruta`.

**5. Dirección del filtro y cardinalidad.** Todas las relaciones van de la dimensión («uno») al hecho («muchos») con filtro en **un sentido**. Un filtro en ambos sentidos puede crear ambigüedad y es más lento. Una relación muchos a muchos casi siempre indica un defecto de claves (una dimensión con claves repetidas): arregla la clave en lugar de aceptar la relación.

**6. Probar el modelo antes de usarlo.** Una lista de verificación (en Pandas, antes de abrir Power BI):

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
articulos = pd.read_csv("04_DATASETS/mini_base/articulos.csv")
lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")

controles = {
    "tienda_id único": tiendas["tienda_id"].is_unique,
    "articulo_id único": articulos["articulo_id"].is_unique,
    "linea_id único": lineas["linea_id"].is_unique,
    "sin huérfanas de tienda": bool(ventas["tienda_id"].isin(tiendas["tienda_id"]).all()),
    "sin huérfanas de artículo": bool(lineas["articulo_id"].isin(articulos["articulo_id"]).all()),
    "sin huérfanas de venta": bool(lineas["venta_id"].isin(ventas["venta_id"]).all()),
}
for nombre, ok in controles.items():
    print("OK  " if ok else "FALLA", nombre)
print("total de líneas:", len(lineas))
```

```salida
OK   tienda_id único
OK   articulo_id único
OK   linea_id único
OK   sin huérfanas de tienda
OK   sin huérfanas de artículo
OK   sin huérfanas de venta
total de líneas: 39
```

Después de cargar en Power BI se vuelve a verificar el **mismo total** (cantidad de filas del hecho y suma de importes) contra estas cifras: si no coinciden, hay un problema de relaciones. Las relaciones dentro de Power BI **no se prueban automáticamente en este paquete**: se comprueban manualmente en Desktop.

**7. Límites del diseño.** Este modelo usa la **ruta actual** de cada tienda: no registra que una tienda cambió de ruta. Para comparar períodos históricos se necesitaría una fecha de vigencia o la ruta del evento. No presentes como histórico un atributo maestro actual.

Ejemplo comercial: el gerente filtra «ruta R03, septiembre» y ve en la misma pantalla ventas, meta y visitas de R03 sin que ninguna cifra se duplique; eso es lo que garantizan dimensiones conformadas y relaciones uno a muchos.

## Errores comunes

- **Relaciones muchos a muchos** aceptadas sin investigar claves.
- **Caminos ambiguos** entre dos tablas.
- **Filtros en ambos sentidos** sin necesidad.
- **Unir metas con ventas a nivel de línea.**
- **Aceptar las relaciones que Power BI infiere automáticamente** sin revisarlas.
- **No probar el modelo** (claves únicas, huérfanas, totales).
- **Presentar atributos actuales como si fueran históricos.**

## Para comprobar que entendiste

1. ¿Qué es una dimensión conformada y para qué sirve?
2. ¿Por qué se evita una relación muchos a muchos?
3. ¿Qué significa «un solo camino» entre dos tablas?
4. ¿Qué cuatro cosas pruebas antes de abrir Power BI?

<details><summary>Respuestas</summary>

1. Una dimensión compartida por varios hechos; permite que un mismo filtro afecte a todos.
2. Porque suele esconder claves repetidas y produce resultados ambiguos.
3. Que no existan dos rutas de relaciones distintas entre las mismas tablas.
4. Claves únicas, huérfanos, filas del hecho y total de ventas.

</details>

## Micropráctica

1. Dibuja el modelo estrella para la mini-base con tres hechos (ventas, metas, visitas) y marca las dimensiones conformadas.
2. Explica por qué `fact_visitas` se conecta a `dim_tienda` y a `dim_fecha` pero no a `fact_ventas`.
3. Escribe la lista de controles que aplicarías a `fact_visitas`.

Cómo saber que está bien: tu dibujo no tiene ciclos y cada hecho se conecta solo a dimensiones.

<details><summary>Comprobación de la parte 3</summary>

```python
import pandas as pd

visitas = pd.read_csv("04_DATASETS/mini_base/visitas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
print(visitas["visita_id"].is_unique, bool(visitas["tienda_id"].isin(tiendas["tienda_id"]).all()))
print(visitas["fecha"].min(), visitas["fecha"].max())
```

```salida
True True
2026-09-01 2026-09-05
```

</details>

## Después, en los ejercicios

El proyecto de Power BI ([`05_PROYECTOS/`](../../05_PROYECTOS/)) y el ejercicio de modelado parten de este diseño. Siguiente: [13.3 La tabla de fechas](03_tabla_de_fechas.md).
