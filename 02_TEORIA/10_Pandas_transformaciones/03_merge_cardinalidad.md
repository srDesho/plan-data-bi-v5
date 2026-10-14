# 10.3 merge: unir tablas y controlar la cardinalidad

> Tiempo estimado: 65 min (lectura 25 + práctica 40). Prerrequisitos: [3.2 Claves y JOIN](../03_SQL_joins/02_inner_join.md), [3.4 Cuando el JOIN duplica](../03_SQL_joins/04_duplicacion_por_join.md) y [10.1 Selección, tipos y columnas](01_columnas_nuevas.md).

Agrupar no es un requisito para unir: el REDUCIDO puede practicar este merge y recuperar después PD-AGR con 10.2, antes de H03/S03. Las claves se prepararon en 3.2 y J2; 3.1 queda como consulta adicional.

## Para qué sirve

Es el `JOIN` de Pandas y trae los mismos peligros que en SQL: una unión mal planteada **duplica filas y multiplica importes sin dar ningún error**. Pandas te ofrece dos defensas (`validate` e `indicator`) que convierten ese error silencioso en un error ruidoso. Esta lección enseña a usarlas siempre.

## Términos nuevos

- **`merge`**: une dos tablas por una o más columnas clave.
- **`on`**: la columna (o lista de columnas) clave, con el mismo nombre en ambas tablas. Si se llaman distinto: `left_on` y `right_on`.
- **`how`**: el tipo de unión: `inner` (solo coincidencias), `left` (todas las de la izquierda), `right`, `outer` (todas).
- **`validate`**: comprueba la cardinalidad que esperas: `"one_to_one"` (`"1:1"`), `"one_to_many"` (`"1:m"`), `"many_to_one"` (`"m:1"`). Si no se cumple, **falla con un error** en lugar de duplicar.
- **`indicator=True`**: agrega una columna `_merge` que dice, para cada fila, si hubo coincidencia (`both`), solo en la izquierda (`left_only`) o solo en la derecha (`right_only`).
- **Clave huérfana**: una clave de la tabla de detalle (la de las líneas, que tiene más filas) que no existe en el catálogo (se detecta con `left_only`).
- **Sufijos** (`_x`, `_y`): lo que Pandas añade a columnas con el mismo nombre en ambas tablas, si no son la clave.
- **Cardinalidad esperada**: lo que sabes de antemano de la relación (muchas líneas → una venta es `m:1`).

## Ejemplo paso a paso

**1. Un merge seguro: muchas líneas → una venta (`m:1`).**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")

unido = lineas.merge(ventas[["venta_id", "estado", "tienda_id"]], on="venta_id", how="left", validate="m:1", indicator=True)
print(len(lineas), len(unido))
print(unido["_merge"].value_counts().to_dict())
print(unido[["linea_id", "venta_id", "estado", "tienda_id"]].head(3))
```

```salida
39 39
{'both': 39, 'left_only': 0, 'right_only': 0}
   linea_id  venta_id     estado  tienda_id
0         1         1  entregado          1
1         2         1  entregado          1
2         3         1  entregado          1
```

Los tres controles de la lección 3.4 en acción:

1. **`validate="m:1"`** no falló: cada `venta_id` es único en `ventas`, como suponíamos.
2. **Filas antes y después**: 39 y 39. Como la relación es muchos a uno y la tabla de la izquierda es la de detalle, el número de filas no debe cambiar.
3. **`_merge`**: las 39 filas son `both`: ninguna línea quedó sin venta (cero huérfanas).

Usar `how="left"` desde la tabla de detalle y revisar `_merge` evita descartar filas en silencio (un `inner` las habría perdido sin avisar).

**2. `validate` convierte una duplicación en un error.** Imaginemos que el catálogo de ventas trae una clave repetida (un error de la fuente):

```python
import pandas as pd

lineas = pd.DataFrame({"linea_id": [1, 2], "venta_id": [10, 20], "importe": [100.0, 50.0]})
catalogo = pd.DataFrame({"venta_id": [10, 20, 20], "estado": ["entregado", "entregado", "anulado"]})

unido = lineas.merge(catalogo, on="venta_id", how="left", validate="m:1")
```

```error
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

Pandas **detiene el proceso**: el catálogo tiene dos filas para `venta_id = 20`, así que una unión normal duplicaría la línea 2 (con dos estados distintos y el doble de importe). El error dice dónde está el problema: *las claves del lado derecho no son únicas*. Corrige el catálogo (o detén la carga) antes de seguir.

**3. Sin `validate`, el mismo caso duplica sin aviso.**

```python
import pandas as pd

lineas = pd.DataFrame({"linea_id": [1, 2], "venta_id": [10, 20], "importe": [100.0, 50.0]})
catalogo = pd.DataFrame({"venta_id": [10, 20, 20], "estado": ["entregado", "entregado", "anulado"]})

unido = lineas.merge(catalogo, on="venta_id", how="left")
print(len(lineas), len(unido))
print(unido)
print(lineas["importe"].sum(), unido["importe"].sum())
```

```salida
2 3
   linea_id  venta_id  importe     estado
0         1        10    100.0  entregado
1         2        20     50.0  entregado
2         2        20     50.0    anulado
150.0 200.0
```

Pasaron de 2 a 3 filas y el importe total de **150** pasó a **200**: la línea 2 (importe 50) aparece dos veces. Nadie recibió error. Esto es **exactamente** el error de «importes duplicados por un merge incorrecto» que ocurre en la vida real, y la comprobación `150 ≠ 200` lo detecta.

**4. Detectar huérfanos con `indicator`.** Línea con una venta que no existe:

```python
import pandas as pd

lineas = pd.DataFrame({"linea_id": [1, 2, 3], "venta_id": [10, 20, 99]})
ventas = pd.DataFrame({"venta_id": [10, 20, 30], "estado": ["entregado", "anulado", "entregado"]})

r = lineas.merge(ventas, on="venta_id", how="outer", indicator=True)
print(r)
print(r["_merge"].value_counts().to_dict())
```

```salida
   linea_id  venta_id     estado      _merge
0       1.0        10  entregado        both
1       2.0        20    anulado        both
2       NaN        30  entregado  right_only
3       3.0        99        NaN   left_only
{'both': 2, 'left_only': 1, 'right_only': 1}
```

Con `how="outer"` y `indicator=True` ves las tres situaciones:

- `both`: coinciden (ventas 10 y 20);
- `left_only`: la línea 3 apunta a la venta **99**, que no existe en `ventas` → **huérfana**;
- `right_only`: la venta 30 no tiene líneas (una venta sin detalle).

Cada caso es una decisión de negocio (rechazar, investigar), pero ahora lo **sabes**.

**5. Columnas con el mismo nombre: sufijos.**

```python
import pandas as pd

a = pd.DataFrame({"id": [1, 2], "estado": ["x", "y"]})
b = pd.DataFrame({"id": [1, 2], "estado": ["p", "q"]})
r = a.merge(b, on="id", suffixes=("_origen", "_catalogo"))
print(list(r.columns))
```

```salida
['id', 'estado_origen', 'estado_catalogo']
```

Si las dos tablas tienen una columna `estado` que no es la clave, Pandas la renombra con sufijos. Es mejor **elegir las columnas** que necesitas de la tabla derecha (`catalogo[["id", "nombre"]]`) y, si hace falta, renombrarlas a propósito, en lugar de aceptar `_x` y `_y`.

**6. Unir por una clave que no es única: el caso de las metas.** Como en 3.4, unir `tiendas` con `metas` por `ruta` (clave repetida 4 veces en tiendas):

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")
metas_sep = metas[metas["mes"] == "2026-09"]

print(metas_sep["meta_bs"].sum())
unido = tiendas[["tienda_id", "ruta"]].merge(metas_sep[["ruta", "meta_bs"]], on="ruta", how="left")
print(len(tiendas), len(unido))
print(unido["meta_bs"].sum())
```

```salida
1350.0
12 12
5400.0
```

La meta total real es 1 350 (600 + 450 + 300). Después del merge, cada ruta se repite en sus 4 tiendas y la suma de metas da **5 400** (cuatro veces más). Con `validate="m:1"` (muchas tiendas → una meta por ruta) habría **pasado**, porque la relación sí es m:1; el problema no es la unión sino **sumar la meta después de unirla a un nivel más detallado**. Moraleja: `validate` protege contra duplicados de clave, pero también debes pensar en qué columna sumas y en qué granularidad.

**7. La solución: agregar al mismo nivel antes de unir.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
base = base[(base["estado"] == "entregado") & (base["fecha"].str.startswith("2026-09"))]

vendido = base.groupby("ruta", as_index=False)["importe"].sum()
meta_sep = metas[metas["mes"] == "2026-09"][["ruta", "meta_bs"]]
resultado = vendido.merge(meta_sep, on="ruta", validate="1:1")
resultado["cumplimiento_pct"] = (resultado["importe"] / resultado["meta_bs"] * 100).round(1)
print(resultado)
```

```salida
  ruta  importe  meta_bs  cumplimiento_pct
0  R01    800.0    600.0             133.3
1  R02    379.0    450.0              84.2
2  R03    160.0    300.0              53.3
```

Primero se lleva lo vendido a **una fila por ruta** y las metas ya están a una fila por ruta; entonces la unión es **`1:1`** y `validate="1:1"` lo confirma. Ese patrón (agregar al mismo nivel, luego unir) es el correcto para comparar ventas con presupuesto en Pandas, en SQL y en Power BI.

**8. Lista de verificación antes de dar por buena una unión.**

1. ¿Cuál es la clave y es única del lado que debe serlo? (`validate`)
2. ¿Cuántas filas había y cuántas hay? ¿Es lo esperado?
3. ¿Hay huérfanas (`left_only`) o catálogos sin uso (`right_only`)?
4. ¿Suma lo que sumaba antes, por otro camino? (total de control)
5. ¿Qué granularidad tiene el resultado y sumo columnas a esa granularidad?

Ejemplo comercial: «ventas contra presupuesto por ruta» exige agregar las ventas a ruta-mes antes de unirlas al presupuesto, que ya está a ruta-mes. Si el reporte va a Power BI, la misma regla se aplica a las relaciones del modelo.

## Errores comunes

- **No usar `validate`** y descubrir los duplicados en el reporte final.
- **`how="inner"`** que descarta huérfanas en silencio.
- **Sumar una columna de nivel superior** (meta, saldo) tras unir con un nivel más detallado.
- **No revisar el número de filas** antes y después.
- **Aceptar columnas `_x`/`_y`** sin entender por qué aparecen.
- **Unir por nombres de negocio** en lugar de por claves.
- **Resolver un duplicado de catálogo con `drop_duplicates`** sin investigar cuál fila es la correcta.

## Para comprobar que entendiste

1. ¿Qué hace `validate="m:1"`?
2. ¿Qué indica `left_only` en la columna `_merge`?
3. En el caso de las metas, ¿por qué `validate` no detectó el problema?
4. ¿Cuál es el patrón correcto para comparar ventas con metas?

<details><summary>Respuestas</summary>

1. Verifica que la clave sea única en el lado derecho; si no, lanza un error.
2. Que la fila de la izquierda no encontró pareja en la derecha (huérfana).
3. Porque la relación sí era muchos a uno; el error fue sumar la meta después de repetirla en un nivel más detallado.
4. Agregar las ventas al nivel de la meta (ruta y mes) y unir dos tablas con la misma granularidad.

</details>

## Micropráctica

1. Une `ventas` con `tiendas` (para traer `zona`) con `validate="m:1"` y comprueba que el número de filas no cambia (16).
2. Une `tiendas` con las ventas por `tienda_id` en un `outer` con `indicator` y encuentra las tiendas sin ninguna venta (deben ser 3).
3. Construye un caso con una clave duplicada en el catálogo y comprueba que `validate` lo detecta.
4. Compara, para septiembre, ventas (importe de entregadas) contra la meta por ruta, agregando antes de unir.

Cómo saber que está bien: 16 filas; 3 tiendas sin ventas; en la 4 el cumplimiento de las rutas se ve distinto entre sí.

<details><summary>Comprobación de la parte 2</summary>

```python
import pandas as pd

tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas_por_tienda = ventas.groupby("tienda_id", as_index=False).size()

r = tiendas.merge(ventas_por_tienda, on="tienda_id", how="outer", indicator=True)
print(r[r["size"].isna()][["tienda_id", "nombre"]])
print(r["_merge"].value_counts().to_dict())
```

```salida
    tienda_id                     nombre
7           8              Farmacia Vida
10         11     Tienda Nueva Esperanza
11         12  Restaurante El Buen Gusto
{'both': 9, 'left_only': 3, 'right_only': 0}
```

</details>

## Después, en los ejercicios

Practica el `merge` con `validate` e `indicator` en P21–P28 y en el mini-ETL de [Python](../../03_EJERCICIOS/Python/): en cada uno, comprueba tú mismo que no se pierdan ni se dupliquen filas. Siguiente: [10.4 Tablas de resumen y exportación](04_resumen_y_exportacion.md).
