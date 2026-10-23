# 15.2 Funciones de Excel para cuadrar: condiciones, sumas y búsquedas

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisito: [15.1 Excel desde cero](01_excel_desde_cero.md).
>
> **Estado de verificación:** las fórmulas de esta lección **no se ejecutaron en Excel** al escribir el material. Para cada una se da el resultado esperado, calculado con Python sobre la mini-base; tú las pruebas en tu Excel y comparas.

## Para qué sirve

Cuatro familias de fórmulas resuelven casi todo el trabajo de cuadre: condicionales (`SI`), sumas y conteos con condición (`SUMAR.SI.CONJUNTO`, `CONTAR.SI.CONJUNTO`), búsquedas (`BUSCARX` o `INDICE`/`COINCIDIR`) y control de errores (`SI.ERROR`). Si entiendes cada una como equivalente de algo que ya sabes de SQL o Pandas, las aprendes en una hora.

## Términos nuevos

- **`SI(condición; si_verdadero; si_falso)`**: equivale a `CASE WHEN` / `np.where`.
- **`SUMAR.SI.CONJUNTO(rango_suma; rango_criterio1; criterio1; …)`**: suma los valores que cumplen **todos** los criterios (`SUM … WHERE … AND …`).
- **`CONTAR.SI.CONJUNTO`**: cuenta las filas que cumplen todos los criterios (`COUNT(*) … WHERE …`).
- **`PROMEDIO.SI.CONJUNTO`**: promedio con condiciones.
- **`BUSCARX(buscado; rango_donde; rango_resultado; si_no_se_encuentra)`**: busca un valor y devuelve otro de la misma posición (el `LEFT JOIN` de una columna). En versiones antiguas de Excel se usa `INDICE` + `COINCIDIR`.
- **`SI.ERROR(fórmula; valor_si_error)`**: devuelve un valor alternativo si la fórmula da error.
- **Criterio**: la condición de un `SI.CONJUNTO`: `"entregado"`, `">100"`, `"<>anulado"`.
- **Coincidencia exacta**: la búsqueda que solo acepta el valor idéntico (la que se quiere para claves).

## Ejemplo paso a paso

Hoja `tbl_ventas` con las columnas de `venta_lineas` unidas a `ventas` (línea, venta, tienda, estado, cantidad, importe).

**1. Un condicional: clasificar.**

```text
=SI([@importe]>=100;"grande";"normal")
```

Equivale a `np.where(importe >= 100, "grande", "normal")`. Resultado esperado:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
print((lineas["importe"] >= 100).sum(), (lineas["importe"] < 100).sum())
```

```salida
5 34
```

En Excel, un contador de la columna debe dar **5 «grande» y 34 «normal»**.

**2. Sumar con condiciones: el `GROUP BY` manual.** Importe de las líneas de ventas entregadas de la tienda 1:

```text
=SUMAR.SI.CONJUNTO(tbl_ventas[importe]; tbl_ventas[estado]; "entregado"; tbl_ventas[tienda_id]; 1)
```

Cada par `rango_criterio; criterio` se agrega con **Y** (todos deben cumplirse). Resultado esperado:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
t = lineas.merge(ventas, on="venta_id", validate="m:1")

print(t[(t["estado"] == "entregado") & (t["tienda_id"] == 1)]["importe"].sum())
print(t[(t["estado"] == "entregado")]["importe"].sum())
```

```salida
544.0
2332.5
```

La tienda 1 debe dar **544** y, sin el criterio de tienda, el total entregado **2 332,5**. Para una tabla por tienda, pones las tiendas en una columna y copias la fórmula con el criterio apuntando a la celda de al lado (`…; tbl[tienda_id]; $A2`).

**3. Contar con condiciones.** Cuántas líneas de ventas entregadas tiene la tienda 1:

```text
=CONTAR.SI.CONJUNTO(tbl_ventas[estado]; "entregado"; tbl_ventas[tienda_id]; 1)
```

Esperado: 9 líneas (3 ventas de 3 líneas cada una). Cuidado: esto cuenta **líneas**, no ventas distintas. Para contar ventas distintas en Excel moderno se combinan `UNICOS`/`CONTARA`, o más fácil, se hace en una tabla dinámica (lección 15.3). Es el mismo error de 3.4: contar filas del detalle como si fueran documentos.

**4. Promedio con condición.**

```text
=PROMEDIO.SI.CONJUNTO(tbl_ventas[importe]; tbl_ventas[estado]; "entregado")
```

Es el promedio **por línea** de las entregadas (no el ticket). Esperado:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
t = lineas.merge(ventas, on="venta_id", validate="m:1")
ent = t[t["estado"] == "entregado"]
print(round(ent["importe"].mean(), 4), round(ent["importe"].sum() / ent["venta_id"].nunique(), 2))
```

```salida
64.7917 166.61
```

El promedio por línea (64,79) es muy distinto al ticket (166,61). Si el pedido es el ticket, ese cociente se calcula con **suma de importes ÷ número de ventas distintas**, no con `PROMEDIO.SI.CONJUNTO` sobre las líneas.

**5. Buscar en un catálogo: `BUSCARX`.** Traer el nombre de la tienda a partir de su código:

```text
=BUSCARX([@tienda_id]; tbl_tiendas[tienda_id]; tbl_tiendas[nombre]; "REVISAR: tienda no existe")
```

Busca el `tienda_id` en el catálogo y devuelve el nombre de la misma fila; si no lo encuentra, escribe la etiqueta de revisión (y **no inventa** un valor). En versiones sin `BUSCARX`:

```text
=SI.ERROR(INDICE(tbl_tiendas[nombre]; COINCIDIR([@tienda_id]; tbl_tiendas[tienda_id]; 0)); "REVISAR: tienda no existe")
```

`COINCIDIR(…; 0)` busca la **posición** con coincidencia **exacta** (el `0` final es crucial) e `INDICE` devuelve el valor de esa posición. El equivalente en Pandas es el `merge(..., how="left", validate="m:1", indicator=True)` de la lección 10.3, y el control es el mismo: cuenta las filas con «REVISAR» (deben ser 0 en los datos de la mini-base).

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
r = ventas.merge(tiendas[["tienda_id", "nombre"]], on="tienda_id", how="left", validate="m:1", indicator=True)
print(int((r["_merge"] != "both").sum()))
```

```salida
0
```

**6. Una advertencia sobre los duplicados en el catálogo.** Si el catálogo trae dos filas con el mismo código, `BUSCARX` y `COINCIDIR` devuelven **solo la primera coincidencia**, sin avisar. Es el equivalente a un `merge` sin `validate`. Antes de buscar, comprueba que el código es único: *Datos → Quitar duplicados* (en una copia) o un `CONTAR.SI` mayor que 1:

```text
=CONTAR.SI(tbl_tiendas[tienda_id]; [@tienda_id])>1
```

**7. `SI.ERROR` con cuidado.** Envolver todo en `SI.ERROR(...; 0)` es tentador y peligroso: oculta errores reales (una división entre cero, un nombre mal escrito) y los reemplaza por un 0 que parece válido. Úsalo solo cuando sabes **qué error esperas** y qué valor alternativo es correcto (por ejemplo, una etiqueta de revisión, no un cero).

**8. Equivalencias para recordar.**

| Excel | SQL | Pandas |
|---|---|---|
| `SI` | `CASE WHEN` | `np.where` |
| `SUMAR.SI.CONJUNTO` | `SUM … WHERE` | `df[cond]["x"].sum()` |
| `CONTAR.SI.CONJUNTO` | `COUNT(*) … WHERE` | `len(df[cond])` |
| `BUSCARX` / `INDICE+COINCIDIR` | `LEFT JOIN` | `merge(how="left")` |
| tabla dinámica | `GROUP BY` | `groupby` / `pivot_table` |
| `SI.ERROR` | `COALESCE` / `CASE` | `fillna` (con cuidado) |

Ejemplo comercial: para cuadrar el reporte de una ruta, una hoja suma con `SUMAR.SI.CONJUNTO` por ruta y estado; el total debe igualar la consulta SQL. Si no coincide, antes de culpar a Excel se revisa que ambos usen el mismo estado, el mismo período y la misma unidad.

## Errores comunes

- **Olvidar el `0` de coincidencia exacta** en `COINCIDIR`.
- **Contar líneas como si fueran documentos.**
- **Usar `PROMEDIO.SI.CONJUNTO` sobre líneas** para obtener el ticket.
- **`SI.ERROR(…; 0)` que esconde errores.**
- **Catálogos con duplicados** que devuelven la primera coincidencia.
- **Criterios de texto con espacios** o mayúsculas distintas.
- **Rangos de distinto tamaño** en `SUMAR.SI.CONJUNTO`.
- **Fórmulas con rangos fijos** (`C2:C40`) en vez de tablas.

## Para comprobar que entendiste

1. ¿Qué función de Excel equivale a un `GROUP BY` con suma?
2. ¿Qué hace el `0` final en `COINCIDIR`?
3. ¿Por qué `PROMEDIO.SI.CONJUNTO` sobre líneas no da el ticket?
4. ¿Qué pasa si el catálogo tiene un código duplicado?

<details><summary>Respuestas</summary>

1. `SUMAR.SI.CONJUNTO` (o una tabla dinámica).
2. Pide coincidencia exacta.
3. Porque promedia líneas, no ventas; el ticket es suma de importes entre ventas distintas.
4. La búsqueda devuelve solo la primera coincidencia, sin avisar.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe la fórmula de Excel que sume las **unidades** (`cantidad`) de ventas entregadas de la tienda 3 y calcula con Python su valor esperado.
2. Escribe la fórmula que traiga la `ruta` de la tienda para cada venta con `BUSCARX` y una etiqueta de revisión.
3. Escribe la fórmula `SI` que clasifique cada venta en «septiembre» o «agosto» según su fecha (pista: `TEXTO` o comparar con `FECHA`).
4. Indica qué cifras de control compararías.

Cómo saber que está bien: las unidades entregadas de la tienda 3 son 50.

<details><summary>Cifra de control de la parte 1</summary>

```python
import pandas as pd

l = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
v = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
t = l.merge(v, on="venta_id", validate="m:1")
print(int(t[(t["estado"] == "entregado") & (t["tienda_id"] == 3)]["cantidad"].sum()))
```

```salida
50
```

</details>

## Después, en los ejercicios

Los casos EX01–EX03 ([`03_EJERCICIOS/Casos/`](../../03_EJERCICIOS/Casos/)) piden cuadrar con estas fórmulas. Siguiente: [15.3 Tablas dinámicas, estadística y el cuadre entre herramientas](03_tablas_dinamicas_cuadre.md).
