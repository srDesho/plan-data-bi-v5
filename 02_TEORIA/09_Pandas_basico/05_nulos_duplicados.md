# 9.5 Valores vacíos y filas duplicadas

> Tiempo estimado: 60 min (lectura 22 + práctica 38). Prerrequisitos: [9.3 Inspeccionar](03_inspeccionar.md) y [1.4 NULL en SQL](../01_SQL_basico/04_null.md).

## Para qué sirve

Dos problemas arruinan más reportes que cualquier error de fórmula: los **vacíos** (datos que faltan o que alguien escribió como «N/A») y los **duplicados** (la misma fila repetida, que infla los totales). Aquí aprendes a detectarlos, a distinguir un duplicado exacto de uno con conflicto, y a decidir qué hacer sin destruir información sin dejar rastro.

## Términos nuevos

- **Vacío** (`NaN`/`None`/`NA`): marca de dato faltante en Pandas. Equivale al `NULL` de SQL.
- **Marcador de faltante**: un texto que el sistema usa para decir «sin dato» (`N/A`, `-`, `sin dato`, `0` mal usado). Pandas no los reconoce como vacío si no le dices.
- **Política de faltantes**: la regla escrita sobre qué hacer con cada vacío: rechazar la fila, completar con un valor acordado o dejar el vacío.
- **Imputar**: reemplazar un faltante por un valor estimado o acordado (por ejemplo, la mediana). Cambia los datos; debe justificarse.
- **Duplicado exacto**: una fila idéntica a otra en todas las columnas.
- **Duplicado por clave**: dos filas con el mismo valor en la columna (o columnas) que debería ser única, aunque difieran en otras.
- **Conflicto**: duplicados por clave con valores distintos en otras columnas (dos importes diferentes para la misma línea). Es el caso peligroso.
- **Clave natural / de negocio**: la columna o combinación que identifica un registro en el negocio (`linea_id`, o `nro_pedido + producto`).

## Ejemplo paso a paso

Un CSV pequeño con problemas (inventado):

```python
import io
import pandas as pd

texto = """linea_id,cliente,estado,monto
1,Luna,entregado,120.5
2,Faro,entregado,80
3,,entregado,45
4,Salud,N/A,60
4,Salud,N/A,60
5,Palma,entregado,
6,Sol,anulado,90
6,Sol,entregado,95
"""
df = pd.read_csv(io.StringIO(texto))
print(df)
print(df.isna().sum().to_dict())
```

```salida
   linea_id cliente     estado  monto
0         1    Luna  entregado  120.5
1         2    Faro  entregado   80.0
2         3     NaN  entregado   45.0
3         4   Salud        NaN   60.0
4         4   Salud        NaN   60.0
5         5   Palma  entregado    NaN
6         6     Sol    anulado   90.0
7         6     Sol  entregado   95.0
{'linea_id': 0, 'cliente': 1, 'estado': 2, 'monto': 1}
```

**1. Detectar los vacíos.** `isna().sum()` cuenta por columna. Hay 1 `cliente` vacío (línea 3) y 1 `monto` vacío (línea 5). Pandas reconoció `N/A` como vacío automáticamente (su lista de marcadores incluye `N/A`, `NA`, `null` y cadenas vacías); por eso `estado` aparece con 2 faltantes, que son las líneas 4.

**2. Marcadores que Pandas no reconoce.** Si el archivo usa otro marcador, hay que decírselo:

```python
import io
import pandas as pd

texto = "clave,valor\na,10\nb,sin dato\nc,-\nd,30\n"
asi = pd.read_csv(io.StringIO(texto))
print(asi["valor"].tolist())

declarado = pd.read_csv(io.StringIO(texto), na_values=["sin dato", "-"])
print(declarado["valor"].tolist())
```

```salida
['10', 'sin dato', '-', '30']
[10.0, nan, nan, 30.0]
```

Sin declarar, la columna `valor` queda como texto (`'10'`, `'sin dato'`...), lo que impide calcular. Con `na_values=[...]` los marcadores pasan a `NaN` y la columna se vuelve numérica. **Ver el valor en `value_counts()` es la forma de descubrir estos marcadores.**

**2b. Vacíos que no son `NaN`: texto vacío y espacios.** A veces el dato falta pero llega como texto vacío o con espacios. `isna()` no los detecta:

```python
import pandas as pd

s = pd.Series(["Luna", "", "  ", None, "Faro"])
print(s.isna().tolist())
print(s.astype(str).str.strip().eq("").tolist())
print(bool(s.isna().any()), bool(s.astype(str).str.strip().eq("").any()))
```

```salida
[False, False, False, True, False]
[False, True, True, False, False]
True True
```

`isna()` solo marca el `None`. La segunda línea convierte a texto, quita espacios y compara con `""` (`eq("")`) para detectar tanto el texto vacío como los espacios. `.any()` resume: ¿hay **alguno**? (Atención: `astype(str)` convierte el `None` en el texto `"None"`; por eso se combinan ambas pruebas.) Un control de calidad de campo obligatorio debería usar las dos.

**3. Qué hacer con un vacío: la política.** Hay cuatro opciones; cada una es una decisión de negocio:

| Opción | Cuándo | Riesgo |
|---|---|---|
| **Rechazar** la fila (a la tabla de rechazos con motivo) | el campo es obligatorio (monto, clave) | pierdes la fila, pero queda explicada |
| **Completar con un valor acordado** (`"Sin cliente"`) | un campo descriptivo cuyo faltante tiene significado | ocultas la ausencia si no lo registras |
| **Imputar** (mediana, promedio) | análisis estadístico con pocos faltantes | inventas datos; sesgas la dispersión |
| **Dejar el vacío** | el faltante es información (aún no entregado) | las funciones lo omitirán en silencio |

La regla que no se rompe: **nunca rellenes con 0 un importe faltante sin una regla de negocio**; el 0 cambia el total.

```python
import io
import pandas as pd

texto = """linea_id,cliente,estado,monto
1,Luna,entregado,120.5
3,,entregado,45
5,Palma,entregado,
"""
df = pd.read_csv(io.StringIO(texto))

rechazadas = df[df["monto"].isna()].copy()
rechazadas["motivo"] = "monto vacío"
validas = df[df["monto"].notna()].copy()
validas["cliente"] = validas["cliente"].fillna("Sin cliente")

print(len(df), len(validas), len(rechazadas))
print(validas[["linea_id", "cliente", "monto"]])
print(rechazadas[["linea_id", "motivo"]])
```

```salida
3 2 1
   linea_id      cliente  monto
0         1         Luna  120.5
1         3  Sin cliente   45.0
   linea_id       motivo
2         5  monto vacío
```

El monto es obligatorio: la fila 5 se rechaza **con motivo** y no se pierde. El cliente es descriptivo: la fila 3 se conserva con la etiqueta «Sin cliente» (que aparece en el reporte). Control: `3 = 2 + 1`, entrada = válidas + rechazadas.

**4. Duplicados exactos.**

```python
import io
import pandas as pd

texto = """linea_id,cliente,estado,monto
4,Salud,entregado,60
4,Salud,entregado,60
7,Sol,entregado,25
"""
df = pd.read_csv(io.StringIO(texto))
print(df.duplicated().tolist())
print(df.duplicated().sum())
print(len(df.drop_duplicates()))
```

```salida
[False, True, False]
1
2
```

`duplicated()` marca como `True` la **segunda y siguientes** apariciones de una fila idéntica. `drop_duplicates()` elimina esas. Cuenta antes y después: 3 filas → 2. **Anota cuántas eliminaste.**

**5. Duplicados por clave con conflicto.** El caso peligroso: la misma `linea_id` con datos distintos.

```python
import io
import pandas as pd

texto = """linea_id,estado,monto
6,anulado,90
6,entregado,95
8,entregado,10
"""
df = pd.read_csv(io.StringIO(texto))
print(df.duplicated().sum())
repetidos = df[df.duplicated(subset=["linea_id"], keep=False)]
print(repetidos)
```

```salida
0
   linea_id     estado  monto
0         6    anulado     90
1         6  entregado     95
```

`duplicated()` sin parámetros da 0: las filas **no** son idénticas. Pero con `subset=["linea_id"]` (la clave) y `keep=False` (marcar **todas** las apariciones, no solo las repetidas) se ven las dos filas de la línea 6: una `anulado` por 90 y otra `entregado` por 95. ¿Cuál es la correcta? **No lo sabes.** Si eliminas «la segunda» con `drop_duplicates(subset=...)`, conservarías una arbitrariamente y quizá mantendrías la equivocada. Lo correcto: detectar el conflicto, **no resolverlo en silencio**, y mandarlo a revisión (o detener la carga si el contrato así lo exige).

**6. Una clave que parece única y no lo es.** La clave de un archivo puede ser una combinación:

```python
import io
import pandas as pd

texto = """nro_pedido,producto,cantidad
100,Agua,2
100,Agua,3
101,Agua,1
"""
df = pd.read_csv(io.StringIO(texto))
print(df.duplicated(subset=["nro_pedido", "producto"], keep=False).sum())
print(df["nro_pedido"].is_unique, df["nro_pedido"].nunique(), len(df))
```

```salida
2
False 2 3
```

La combinación `(nro_pedido, producto)` se repite en las dos primeras filas: ¿es un error o el cliente pidió dos veces el mismo producto en el mismo pedido? Depende del negocio. Las claves se definen en el **contrato de datos**, no se adivinan. `is_unique` comprueba rápido si una columna no tiene repetidos.

**7. El control de cuadre de una limpieza.** Siempre debe cumplirse:

`filas de entrada = filas válidas + filas rechazadas + duplicados eliminados`

Si esa igualdad no se cumple, desapareció algo sin explicación. Es el control que usarás en el ETL (capítulo 5).

Ejemplo comercial: el ERP exporta el mismo pedido dos veces por una caída de red. Si no detectas duplicados exactos, tus ventas suben artificialmente; si no distingues el conflicto (mismo pedido, distinto monto), eliges un valor al azar.

## Errores comunes

- **Rellenar con 0 los montos faltantes.**
- **No reconocer marcadores de faltantes** (`-`, `sin dato`) y dejar columnas numéricas como texto.
- **`dropna()` indiscriminado**: elimina filas por un vacío en una columna irrelevante.
- **`drop_duplicates()` sin saber qué eliminó** ni cuántas filas.
- **Quedarse con la primera aparición** cuando hay conflicto de valores.
- **Olvidar `keep=False`** al querer ver todas las filas repetidas.
- **Imputar sin documentar.**

## Para comprobar que entendiste

1. ¿Qué marca `duplicated()` por defecto: todas las filas repetidas o solo las segundas y siguientes?
2. ¿Qué parámetro muestra todas las apariciones de una clave repetida?
3. ¿Por qué es peligroso `drop_duplicates(subset=["id"])` cuando los montos difieren?
4. ¿Qué igualdad debe cumplir una limpieza?

<details><summary>Respuestas</summary>

1. Solo las segundas y siguientes apariciones.
2. `keep=False`.
3. Porque conserva una fila arbitraria y puede perder la correcta sin avisar.
4. Entrada = válidas + rechazadas + duplicados eliminados.

</details>

## Micropráctica

Crea (con `io.StringIO`) un CSV de 8 filas de ventas con: una fila con `monto` vacío, una con cliente vacío, un duplicado exacto y dos filas con la misma clave y montos distintos.

1. Cuenta vacíos por columna.
2. Separa en `validas`, `rechazadas` (con motivo) y `duplicados_exactos`.
3. Detecta el conflicto de clave y explica por qué no lo resuelves automáticamente.
4. Comprueba la igualdad de cuadre con tus números.

Cómo saber que está bien: tus cuatro conteos suman las 8 filas de entrada.

<details><summary>Un ejemplo de resolución (parte 1 y 3)</summary>

```python
import io
import pandas as pd

texto = """id,cliente,monto
1,Luna,10
2,Faro,
3,,30
4,Sol,40
4,Sol,40
5,Palma,50
6,Salud,60
6,Salud,65
"""
df = pd.read_csv(io.StringIO(texto))
print(df.isna().sum().to_dict())
print(df.duplicated().sum())
print(df[df.duplicated(subset=["id"], keep=False) & ~df.duplicated(keep=False)])
```

```salida
{'id': 0, 'cliente': 1, 'monto': 1}
1
   id cliente  monto
6   6   Salud   60.0
7   6   Salud   65.0
```

</details>

## Después, en los ejercicios

El tratamiento de vacíos y duplicados es el corazón del mini-ETL y de P21–P28 en [Python](../../03_EJERCICIOS/Python/). Define tu política antes de limpiar y regístrala. Siguiente: [9.6 Tipos, textos y fechas](06_tipos_textos_fechas.md).
