# 10.4 Tablas de resumen y exportación (CSV y SQLite)

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [10.2 groupby](02_groupby_agg.md), [8.3 Archivos](../08_Python_funciones_archivos/03_archivos_csv_json.md) y [8.5 Excepciones](../08_Python_funciones_archivos/05_excepciones.md) (`finally`).

## Para qué sirve

El resultado de tu análisis tiene que **salir** de Python: un CSV para Excel, una tabla en SQLite para Power BI o para otra persona. Exportar bien significa que el archivo se pueda abrir sin sorpresas (sin la columna de índice, con el separador y la codificación correctos) y que ejecutar el programa dos veces **no duplique** los datos. Y significa verificar, leyendo el archivo de vuelta, que lo que escribiste es lo que querías.

## Términos nuevos

- **Tabla de resumen** (o *tabla agregada*): una tabla con una fila por grupo (ruta, mes, categoría) y las medidas ya calculadas. Es lo que alimenta un reporte (la capa «Gold»).
- **`to_csv`**: escribe un DataFrame en un archivo CSV.
- **`to_sql`**: escribe un DataFrame como una tabla de una base de datos SQL (aquí SQLite).
- **Idempotente**: una operación que, ejecutada una o varias veces, deja el **mismo** resultado. Un proceso de carga idempotente no duplica datos al reejecutarse.
- **`if_exists`**: lo que hace `to_sql` si la tabla ya existe: `"fail"` (error), `"replace"` (la borra y la crea de nuevo) o `"append"` (agrega filas).
- **Orden determinista**: ordenar la tabla por una clave completa para que el archivo sea idéntico en cada ejecución.
- **Redondeo de presentación**: redondear al final, solo en la tabla que se entrega, nunca en cálculos intermedios.

## Ejemplo paso a paso

**1. Construir una tabla de resumen.** Ventas entregadas por ruta y mes:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")

lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
base = base[base["estado"] == "entregado"].copy()
base["mes"] = base["fecha"].str[:7]

gold = (
    base.groupby(["ruta", "mes"], as_index=False)
    .agg(ventas=("venta_id", "nunique"), importe_bs=("importe", "sum"))
    .sort_values(["ruta", "mes"])
    .reset_index(drop=True)
)
gold["importe_bs"] = gold["importe_bs"].round(2)
print(gold)
print(gold["importe_bs"].sum(), gold["ventas"].sum())
```

```salida
  ruta      mes  ventas  importe_bs
0  R01  2026-08       3       465.0
1  R01  2026-09       4       800.0
2  R02  2026-08       1       131.0
3  R02  2026-09       3       379.0
4  R03  2026-08       2       397.5
5  R03  2026-09       1       160.0
2332.5 14
```

Una fila por (ruta, mes), ordenada por la clave completa (orden determinista). Controles: el importe suma 2 332,5 y las ventas 14, igual que los totales que ya conocemos. **No exportes antes de comprobar el cuadre.**

**2. Exportar a CSV.**

```python
import pandas as pd

gold = pd.DataFrame({"ruta": ["R01", "R02"], "mes": ["2026-09", "2026-09"], "importe_bs": [800.0, 379.0]})
gold.to_csv("gold_ruta_mes.csv", index=False, encoding="utf-8")
print(open("gold_ruta_mes.csv", encoding="utf-8").read())
```

```salida
ruta,mes,importe_bs
R01,2026-09,800.0
R02,2026-09,379.0
```

Dos opciones que casi siempre quieres: **`index=False`** (sin ella, Pandas escribe el índice 0, 1, 2... como una primera columna sin nombre, que luego confunde) y **`encoding`** explícito. Si el archivo se abrirá en Excel de un equipo con configuración regional española/boliviana, el separador de lista puede ser `;` y el decimal `,`: en ese caso `to_csv(..., sep=";", decimal=",")`. Documenta la convención en el nombre o en un README.

**3. Leer el CSV de vuelta y verificar.**

```python
import pandas as pd

original = pd.DataFrame({"ruta": ["R01", "R02"], "importe_bs": [800.0, 379.5]})
original.to_csv("resumen.csv", index=False)
leido = pd.read_csv("resumen.csv")

print(leido.equals(original))
print(leido["importe_bs"].sum(), original["importe_bs"].sum())
print(list(leido.columns))
```

```salida
True
1179.5 1179.5
['ruta', 'importe_bs']
```

`equals` comprueba que ambas tablas son idénticas (valores y tipos). Leer de vuelta lo que escribiste y comparar es la prueba de que el archivo es correcto; un archivo que «se escribió sin error» puede estar mal.

**4. Exportar a SQLite.** `to_sql` crea una tabla desde un DataFrame. Importante en Windows: **cierra siempre la conexión** (lección 8.5, `finally`/`closing`); si queda abierta, no podrás borrar ni reemplazar el archivo:

```python
import sqlite3
from contextlib import closing

import pandas as pd

gold = pd.DataFrame({"ruta": ["R01", "R02", "R03"], "importe_bs": [1265.0, 510.0, 557.5]})

with closing(sqlite3.connect("reporte.db")) as con:
    gold.to_sql("gold_ruta", con, if_exists="replace", index=False)
    leido = pd.read_sql("SELECT ruta, importe_bs FROM gold_ruta ORDER BY ruta", con)

print(leido)
print(leido["importe_bs"].sum())
```

```salida
  ruta  importe_bs
0  R01      1265.0
1  R02       510.0
2  R03       557.5
2332.5
```

`closing(...)` garantiza que la conexión se cierre al terminar el bloque. `to_sql("gold_ruta", con, if_exists="replace", index=False)` crea la tabla `gold_ruta`; `read_sql` la lee de vuelta con una consulta SQL, que es la verificación.

**5. Idempotencia: ejecutarlo dos veces.** Con `if_exists="append"` cada ejecución **agrega** filas y duplica los datos; con `"replace"` el resultado es el mismo sin importar cuántas veces corras el programa:

```python
import sqlite3
from contextlib import closing

import pandas as pd

gold = pd.DataFrame({"ruta": ["R01", "R02"], "importe_bs": [800.0, 379.0]})

with closing(sqlite3.connect("prueba.db")) as con:
    for _ in range(2):
        gold.to_sql("append_mal", con, if_exists="append", index=False)
        gold.to_sql("replace_bien", con, if_exists="replace", index=False)
    print(pd.read_sql("SELECT COUNT(*) AS filas FROM append_mal", con)["filas"][0])
    print(pd.read_sql("SELECT COUNT(*) AS filas FROM replace_bien", con)["filas"][0])
```

```salida
4
2
```

Después de ejecutar dos veces, `append_mal` tiene 4 filas (¡duplicadas!) y `replace_bien` sigue en 2. La estrategia de este curso para las cargas es **reemplazar el conjunto completo** y documentarlo; una carga incremental más sofisticada queda para después. Asegúrate de poder repetir el programa y obtener el mismo archivo.

**6. Tipos al exportar a SQLite.** SQLite guarda fechas como texto; si exportas una columna `datetime`, conviértela antes a texto ISO para controlar el formato:

```python
import pandas as pd

df = pd.DataFrame({"fecha": pd.to_datetime(["2026-09-01", "2026-09-15"])})
df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
print(df["fecha"].tolist(), df["fecha"].dtype)
```

```salida
['2026-09-01', '2026-09-15'] object
```

**7. Una lista de verificación de salida.**

1. ¿Los totales de la tabla coinciden con los de la capa anterior? (cuadre)
2. ¿Sin columna de índice? ¿Nombres de columna claros y en minúsculas, sin espacios?
3. ¿Orden determinista (ordenado por la clave completa)?
4. ¿Redondeado una sola vez, al final?
5. ¿Codificación, separador y decimal declarados?
6. ¿Reejecutar da el mismo resultado? (idempotente)
7. ¿Leí el archivo de vuelta y lo comparé?

Ejemplo comercial: el gerente quiere abrir el resumen en Excel y vincularlo a Power BI. Entregas un CSV con `index=False`, `;` y coma decimal si su Excel así lo requiere, y una tabla en SQLite con el mismo contenido para el modelo. Ambos con los mismos totales, comprobados.

## Errores comunes

- **Exportar con el índice** (columna extra sin nombre).
- **No verificar el archivo leyéndolo de vuelta.**
- **`if_exists="append"` en una carga que se repite** (duplica datos).
- **Dejar abierta la conexión SQLite** (en Windows no podrás reemplazar el archivo).
- **Redondear antes de sumar.**
- **Sobrescribir el archivo de entrada.**
- **Ignorar el decimal y el separador** que espera quien abrirá el archivo.
- **Archivos de salida con orden distinto cada vez.**

## Para comprobar que entendiste

1. ¿Por qué se usa `index=False`?
2. ¿Qué significa que una carga sea idempotente?
3. ¿Qué diferencia hay entre `if_exists="append"` y `"replace"`?
4. ¿Cómo compruebas que el CSV que escribiste es correcto?

<details><summary>Respuestas</summary>

1. Para no escribir el índice de Pandas como una columna adicional.
2. Que ejecutarla una o varias veces deja el mismo resultado.
3. `append` agrega filas a la tabla existente; `replace` la borra y la vuelve a crear.
4. Leyéndolo de vuelta y comparándolo con el original (valores, tipos y totales).

</details>

<a id="micropractica"></a>

## Micropráctica

1. Construye una tabla de resumen: unidades e importe por categoría de artículo (ventas entregadas).
2. Expórtala a CSV sin índice y léela de vuelta para verificar que `equals` es verdadero.
3. Guárdala en una base SQLite (`resumen.db`) con `replace`, ejecuta el programa dos veces y comprueba que el número de filas no cambia.
4. Escribe en un comentario qué hace falta para que el archivo se abra bien en Excel con configuración regional boliviana.

Cómo saber que está bien: 4 categorías en el resumen; el conteo de filas es el mismo tras la segunda ejecución.

<details><summary>Comprobación de las partes 2 y 3</summary>

```python
import sqlite3
from contextlib import closing

import pandas as pd

resumen = pd.DataFrame({"categoria": ["Bebidas", "Lácteos"], "importe_bs": [1050.0, 528.0]})
resumen.to_csv("categorias.csv", index=False)
print(pd.read_csv("categorias.csv").equals(resumen))

for _ in range(2):
    with closing(sqlite3.connect("resumen.db")) as con:
        resumen.to_sql("categorias", con, if_exists="replace", index=False)

with closing(sqlite3.connect("resumen.db")) as con:
    print(pd.read_sql("SELECT COUNT(*) AS n FROM categorias", con)["n"][0])
```

```salida
True
2
```

</details>

## Después, en los ejercicios

La exportación de tablas Gold y la verificación por lectura de vuelta son parte del mini-ETL y del ETL final ([Proyectos](../../05_PROYECTOS/)). Siguiente: [10.5 Controles de calidad y reconciliación](05_controles_calidad.md).
