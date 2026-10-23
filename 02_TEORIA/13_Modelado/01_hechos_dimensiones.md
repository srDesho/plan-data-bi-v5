# 13.1 Hechos, dimensiones y granularidad

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [3.1 Claves y cardinalidad](../03_SQL_joins/01_claves_relaciones.md) y [10.3 merge](../10_Pandas_transformaciones/03_merge_cardinalidad.md).

## Para qué sirve

Los reportes (SQL, Excel, Power BI) responden preguntas sobre eventos del negocio: ventas, visitas, pedidos. Un modelo bien diseñado separa **qué ocurrió** (los eventos medibles) de **cómo describirlos** (cliente, producto, fecha), y deja claro qué representa cada fila. Con ese diseño las cifras se pueden filtrar y combinar sin multiplicarse, que es exactamente el problema que viste en 3.4 y 10.3.

## Términos nuevos

- **Modelo de datos**: la forma en que se organizan las tablas y sus relaciones para responder preguntas.
- **Tabla de hechos** (*fact*): una tabla donde cada fila es un **evento medible** (una línea de venta, una visita) y las columnas son medidas (cantidad, importe) y claves hacia las dimensiones.
- **Tabla de dimensión** (*dim*): una tabla que **describe** el contexto del evento (cliente, producto, vendedor, fecha). Cada fila es una cosa distinta, con una clave única, y se usa para filtrar y agrupar.
- **Medida**: un valor numérico del evento que se suma o promedia (cantidad, importe, duración).
- **Atributo**: una característica descriptiva en una dimensión (zona, categoría).
- **Granularidad del hecho**: qué representa exactamente una fila de la tabla de hechos. Es la **primera decisión** del modelo.
- **Clave sustituta / identificador**: un número que identifica una fila sin significado de negocio (`tienda_id`).
- **Aditiva**: una medida que se puede sumar entre todas las dimensiones (importe, cantidad). **No aditiva**: no se puede sumar (porcentajes, tickets, promedios): se recalcula en cada contexto.

## Ejemplo paso a paso

**1. Empezar por la pregunta y la granularidad.** Queremos responder: «ventas entregadas por ruta, categoría de artículo, vendedor y mes». Los eventos son **las líneas de venta**. Decisión de granularidad: *una fila del hecho = una línea de producto dentro de una venta*. Con ella:

- Las **medidas** son `cantidad` e `importe` (cantidad × precio).
- El **estado** de la venta se guarda también (para no perder las anuladas).
- Las **claves** hacia las dimensiones son: venta (cabecera), artículo, tienda, vendedor y fecha.

**2. Identificar las dimensiones.** Todo lo que sirve para describir o filtrar una línea:

| Dimensión | Clave | Atributos |
|---|---|---|
| `dim_tienda` | `tienda_id` | nombre, tipo, zona, ruta |
| `dim_articulo` | `articulo_id` | nombre, categoría |
| `dim_vendedor` | `vendedor_id` | nombre, ruta |
| `dim_fecha` | `fecha` | año, mes, nombre del mes, día de la semana (lección 13.3) |

Cada fila de una dimensión es **única** (una tienda, un artículo) y aparece muchas veces en el hecho. Esa es la relación **uno a muchos**: una tienda tiene muchas líneas de venta.

**3. Construir el hecho en Pandas.** Se une el detalle con la cabecera para traer tienda, vendedor, fecha y estado; el importe se calcula:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")

fact_ventas = lineas.merge(ventas, on="venta_id", how="left", validate="m:1")
fact_ventas["importe_centavos"] = (fact_ventas["cantidad"] * fact_ventas["precio_unitario"] * 100).round().astype(int)
fact_ventas = fact_ventas[["linea_id", "venta_id", "tienda_id", "articulo_id", "vendedor_id", "fecha", "estado", "cantidad", "importe_centavos"]]

print(len(lineas), len(fact_ventas))
print(fact_ventas["linea_id"].is_unique)
print(fact_ventas.head(3))
```

```salida
39 39
True
   linea_id  venta_id  tienda_id  ...     estado  cantidad importe_centavos
0         1         1          1  ...  entregado        10             6000
1         2         1          1  ...  entregado         6             4500
2         3         1          1  ...  entregado         4             3200

[3 rows x 9 columns]
```

Controles inmediatos: 39 líneas antes y después (la unión es m:1, no se pierde ni duplica nada); `linea_id` es única (clave del hecho). El importe se guarda en **centavos enteros** (lección 5.3), con `round()` antes de convertir a entero para evitar errores de coma flotante.

**4. Construir las dimensiones.**

```python
import pandas as pd

dim_tienda = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
dim_articulo = pd.read_csv("04_DATASETS/mini_base/articulos.csv")[["articulo_id", "nombre", "categoria"]]
dim_vendedor = pd.read_csv("04_DATASETS/mini_base/vendedores.csv")

for nombre, dim, clave in [("dim_tienda", dim_tienda, "tienda_id"), ("dim_articulo", dim_articulo, "articulo_id"), ("dim_vendedor", dim_vendedor, "vendedor_id")]:
    print(nombre, len(dim), dim[clave].is_unique, dim[clave].isna().sum())
```

```salida
dim_tienda 12 True 0
dim_articulo 10 True 0
dim_vendedor 4 True 0
```

Cada dimensión tiene su clave **única y sin vacíos**. Si una clave se repitiera, cualquier relación hacia el hecho multiplicaría las filas.

**5. Probar las relaciones: huérfanas y cobertura.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
fact = lineas.merge(ventas, on="venta_id", validate="m:1")

dims = {
    "tienda_id": pd.read_csv("04_DATASETS/mini_base/tiendas.csv")["tienda_id"],
    "articulo_id": pd.read_csv("04_DATASETS/mini_base/articulos.csv")["articulo_id"],
    "vendedor_id": pd.read_csv("04_DATASETS/mini_base/vendedores.csv")["vendedor_id"],
}
for clave, valores in dims.items():
    huerfanas = (~fact[clave].isin(valores)).sum()
    sin_uso = (~valores.isin(fact[clave])).sum()
    print(clave, "huérfanas:", huerfanas, "| elementos de la dimensión sin ventas:", sin_uso)
```

```salida
tienda_id huérfanas: 0 | elementos de la dimensión sin ventas: 3
articulo_id huérfanas: 0 | elementos de la dimensión sin ventas: 0
vendedor_id huérfanas: 0 | elementos de la dimensión sin ventas: 1
```

Dos preguntas por relación:

- **¿Hay huérfanas?** Claves del hecho que no existen en la dimensión (0 aquí: todas las líneas apuntan a una tienda, artículo y vendedor reales). Con huérfanas, Power BI mostraría una fila «(en blanco)» y los totales no cuadrarían.
- **¿Hay elementos de la dimensión sin hechos?** Tiendas sin ventas (3) y un vendedor sin ventas (1). No es un error: son datos reales que un reporte puede querer mostrar.

**6. Medidas aditivas y no aditivas.**

| Medida | ¿Aditiva? | Cómo se calcula en cualquier contexto |
|---|---|---|
| `cantidad` | sí | suma |
| `importe_centavos` | sí | suma |
| número de ventas | **no** | contar ventas **distintas** (`nunique`), no filas del hecho |
| ticket medio | **no** | importe total / ventas distintas, en ese contexto |
| % de cumplimiento | **no** | ventas reales / meta, recalculado |

Si sumaras los tickets de cada ruta para dar el ticket nacional, el resultado sería incorrecto. Las razones se **recalculan** en cada contexto con numerador y denominador (lección 2.3).

**7. Qué NO va en el hecho de ventas.** Una **meta por ruta y mes** no pertenece a una fila de línea de venta: tiene otra granularidad. Si la copiaras en cada línea y la sumaras, la multiplicarías (3.4). Va en **su propia tabla de hechos** (`fact_metas`), con las dimensiones que comparte (ruta, mes). Lo mismo ocurre con las visitas: son otro evento, con otra granularidad (`fact_visitas`). En la lección 13.2 se conectan sin multiplicarlas.

Ejemplo comercial: «¿cuánto vendimos en la zona Centro, en la categoría Bebidas, en septiembre?» es un filtro sobre tres dimensiones (`zona` de tienda, `categoria` de artículo, mes de fecha) y una suma del hecho. Cada dimensión aporta un filtro; el hecho aporta el número.

## Errores comunes

- **No decidir la granularidad antes de diseñar.**
- **Mezclar hechos de distinta granularidad en una sola tabla** (meta en cada línea).
- **Dimensiones con claves repetidas o vacías.**
- **Sumar medidas no aditivas** (tickets, porcentajes).
- **No revisar huérfanas.**
- **Usar nombres de negocio como claves.**
- **Dejar fuera el estado** y perder las anulaciones.

## Para comprobar que entendiste

1. ¿Cuál es la granularidad del hecho de ventas de esta lección?
2. ¿Qué diferencia hay entre un hecho y una dimensión?
3. ¿Por qué el ticket medio no se suma?
4. ¿Qué es una clave huérfana y por qué importa?

<details><summary>Respuestas</summary>

1. Una línea de producto dentro de una venta.
2. El hecho registra eventos medibles; la dimensión describe su contexto con una fila por elemento y clave única.
3. Porque es un cociente; se recalcula con numerador y denominador en cada contexto.
4. Una clave del hecho que no existe en la dimensión; provoca filas «en blanco» y totales que no cuadran.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Define la granularidad, las medidas, las dimensiones y las claves para un hecho de **visitas** (`visitas.csv`).
2. Explica por qué las visitas y las ventas no pueden ir en la misma tabla de hechos.
3. Construye `fact_visitas` en Pandas, comprueba que la clave `visita_id` es única y busca tiendas huérfanas.

Cómo saber que está bien: 14 filas, 0 huérfanas respecto de `dim_tienda`.

<details><summary>Comprobación de la parte 3</summary>

```python
import pandas as pd

fact_visitas = pd.read_csv("04_DATASETS/mini_base/visitas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")

print(len(fact_visitas), fact_visitas["visita_id"].is_unique)
print((~fact_visitas["tienda_id"].isin(tiendas["tienda_id"])).sum())
```

```salida
14 True
0
```

</details>

## Después, en los ejercicios

El diseño del modelo es la base del ejercicio de modelado y del proyecto de Power BI ([`05_PROYECTOS/`](../../05_PROYECTOS/)). Antes de abrir Power BI, prueba claves únicas, huérfanos, filas del hecho y total de ventas. Siguiente: [13.2 El modelo estrella](02_modelo_estrella.md).
