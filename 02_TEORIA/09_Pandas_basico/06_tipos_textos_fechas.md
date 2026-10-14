# 9.6 Convertir tipos, limpiar texto y trabajar con fechas

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [7.7 Conversiones](../07_Python_basico/07_conversiones.md), [8.4 Módulos (datetime)](../08_Python_funciones_archivos/04_modulos_imports.md) y [9.5 Nulos y duplicados](05_nulos_duplicados.md).

## Para qué sirve

Los archivos llegan con montos como texto (`"Bs 1.250,50"`), fechas escritas de tres formas y nombres con espacios. Antes de calcular hay que convertirlo todo a tipos de verdad y **registrar lo que no se pudo convertir**. Hacerlo mal produce errores silenciosos: una fecha `03/04/2026` leída como 4 de marzo en vez de 3 de abril, o un monto cien veces más grande.

## Términos nuevos

- **`astype`**: convierte una columna a otro tipo (`astype(int)`); falla si hay valores que no encajan.
- **`pd.to_numeric`**: convierte texto a número. Con `errors="coerce"` los valores inválidos pasan a `NaN` en lugar de provocar un error.
- **`pd.to_datetime`**: convierte texto a fecha. Con `format=` se le dice cómo está escrita; con `errors="coerce"` las inválidas pasan a `NaT`.
- **`NaT`**: «not a time»: el vacío de las fechas, equivalente a `NaN`.
- **Accesor `.str`**: los métodos de texto aplicados a toda una columna (`.str.strip()`, `.str.replace()`).
- **Accesor `.dt`**: los métodos de fecha aplicados a toda una columna (`.dt.year`, `.dt.month`).
- **Formato de fecha**: los códigos que describen su escritura: `%d` día, `%m` mes, `%Y` año de 4 cifras.
- **Ambigüedad de fecha**: que un texto se pueda interpretar de dos maneras (`03/04/2026` ¿3 de abril o 4 de marzo?). Se resuelve con el contrato del dato, no adivinando.
- **Centavos enteros**: representar dinero como número entero de centavos (Bs 12,50 = 1250) para evitar errores de decimales.

## Ejemplo paso a paso

**1. Convertir texto a número y encontrar lo inválido.**

```python
import pandas as pd

montos = pd.Series(["120.5", "80", "abc", "", "45.25"])
numeros = pd.to_numeric(montos, errors="coerce")
print(numeros.tolist())
print(numeros.isna().sum())
print(montos[numeros.isna()].tolist())
```

```salida
[120.5, 80.0, nan, nan, 45.25]
2
['abc', '']
```

`errors="coerce"` convirtió `abc` y el texto vacío en `NaN`. **No termina ahí:** la última línea recupera los textos originales de las filas que fallaron, para mandarlos a la tabla de rechazos con su valor. Cuenta cuántos fallaron antes de seguir. Sin `coerce`, `pd.to_numeric` se detiene en el primer valor malo con un `ValueError`, lo que a veces es preferible (si los datos deben estar limpios).

**2. Limpiar texto antes de convertir.** Un monto como `"Bs 1.250,50"`:

```python
import pandas as pd

crudo = pd.Series(["Bs 1.250,50", " Bs 80,00", "Bs 45,5 "])
limpio = (
    crudo.str.replace("Bs", "", regex=False)
    .str.strip()
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
print(limpio.tolist())
print(pd.to_numeric(limpio).tolist())
```

```salida
['1250.50', '80.00', '45.5']
[1250.5, 80.0, 45.5]
```

Los pasos, en orden: quitar el símbolo `Bs`, quitar espacios, **quitar el punto de los miles**, cambiar la coma decimal por punto. El orden es crucial: si cambias la coma por punto antes de quitar el punto de miles, `1.250,50` quedaría `1.250.50`. Solo apliques estas reglas si el contrato del dato confirma que el punto es separador de miles. **No elimines separadores que el contrato nunca definió.**

**3. Fechas con formato explícito.**

```python
import pandas as pd

textos = pd.Series(["03/04/2026", "15/09/2026", "31/02/2026", "texto"])
fechas = pd.to_datetime(textos, format="%d/%m/%Y", errors="coerce")
print(fechas.tolist())
print(fechas.isna().sum())
```

```salida
[Timestamp('2026-04-03 00:00:00'), Timestamp('2026-09-15 00:00:00'), NaT, NaT]
2
```

`format="%d/%m/%Y"` dice: día/mes/año. Se interpretó `03/04/2026` como **3 de abril**. `31/02/2026` (no existe) y `texto` pasaron a `NaT`. Si hubieras omitido `format`, Pandas intenta adivinar y puede equivocarse en fechas ambiguas, o dar advertencias. **Pasa siempre `format` cuando el contrato lo define.**

**4. Fechas mezcladas: separar por formato.** Si en la misma columna conviven `2026-09-01` y `01/09/2026`, aplica una máscara por formato:

```python
import pandas as pd

textos = pd.Series(["2026-09-01", "01/09/2026", "2026-09-15", "15/09/2026"])
es_iso = textos.str.fullmatch(r"\d{4}-\d{2}-\d{2}")
fechas = pd.Series(pd.NaT, index=textos.index, dtype="datetime64[ns]")
fechas[es_iso] = pd.to_datetime(textos[es_iso], format="%Y-%m-%d")
fechas[~es_iso] = pd.to_datetime(textos[~es_iso], format="%d/%m/%Y")
print(fechas.dt.strftime("%Y-%m-%d").tolist())
```

```salida
['2026-09-01', '2026-09-01', '2026-09-15', '2026-09-15']
```

Cada grupo se convierte con **su** formato; así nada se interpreta con el formato equivocado. (`fullmatch` con una expresión regular `\d{4}-\d{2}-\d{2}` pregunta si el texto completo tiene la forma año-mes-día.)

**5. Usar las partes de una fecha.**

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas["fecha"] = pd.to_datetime(ventas["fecha"], format="%Y-%m-%d")
ventas["mes"] = ventas["fecha"].dt.strftime("%Y-%m")
ventas["dia_semana"] = ventas["fecha"].dt.day_name()

print(ventas["fecha"].dtype)
print(ventas.groupby("mes").size().to_dict())
print(ventas[["fecha", "dia_semana"]].head(3))
print((pd.Timestamp("2026-09-30") - ventas["fecha"]).dt.days.head(3).tolist())
```

```salida
datetime64[ns]
{'2026-08': 7, '2026-09': 9}
       fecha dia_semana
0 2026-08-03     Monday
1 2026-08-05  Wednesday
2 2026-08-07     Friday
[58, 56, 54]
```

Con la columna ya como fecha de verdad (`datetime64`), `.dt` da partes (`year`, `month`, `day_name()`), `strftime` genera textos, y restar fechas da una duración (`.dt.days`). El conteo por mes (`7` en agosto, `9` en septiembre) coincide con el SQL de la lección 2.4: **comprueba tus conversiones contra una cifra conocida**.

**6. Dinero en centavos enteros.** Para evitar errores de decimales en sumas largas:

```python
from decimal import Decimal

print(0.1 + 0.2)
print(Decimal("0.1") + Decimal("0.2"))
print(int(round(Decimal("12.50") * 100)))
print(sum([1250, 800, 45]) / 100)
```

```salida
0.30000000000000004
0.3
1250
20.95
```

`0.1 + 0.2` en `float` da `0.30000000000000004`; con `Decimal` desde texto da exactamente `0.3`. Una práctica habitual en pipelines: convertir el texto a `Decimal`, multiplicar por 100 y guardar un entero de **centavos**; los totales son sumas de enteros y se dividen entre 100 solo al presentar. En el proyecto final se pide esta forma.

**7. Categorías limpias: texto con mayúsculas y espacios.**

```python
import pandas as pd

estados = pd.Series(["entregado", "Entregado", "entregado ", "ANULADO", "anulado"])
print(estados.value_counts().to_dict())

limpios = estados.str.strip().str.lower()
print(limpios.value_counts().to_dict())
```

```salida
{'entregado': 1, 'Entregado': 1, 'entregado ': 1, 'ANULADO': 1, 'anulado': 1}
{'entregado': 3, 'anulado': 2}
```

Antes de normalizar hay 5 variantes en 4 valores; después, 2 estados: `entregado` (3) y `anulado` (2). **Normaliza solo lo que el contrato permite normalizar**: un estado desconocido (`"pendiente"`) no se convierte en uno conocido, se envía a rechazo.

**8. Ceros a la izquierda y códigos.** Si `007` debe seguir siendo `007`, léelo como texto (9.2) o rellénalo: `"7".zfill(3)` da `"007"`.

Ejemplo comercial: el ERP entrega `fecha` como `DD/MM/YYYY`, `monto` con coma decimal y `estado` con mayúsculas variadas. Tu limpieza convierte cada una con una regla escrita, cuenta lo que no pudo convertir y verifica el total contra el del sistema.

## Errores comunes

- **Dejar que Pandas adivine el formato de fecha.**
- **Convertir con `errors="coerce"` y no contar los `NaN` resultantes.**
- **Quitar la coma de un monto** y multiplicar su valor por 100.
- **Cambiar la coma por punto antes de quitar el punto de miles.**
- **Aplicar `astype(int)`** a una columna con vacíos.
- **Comparar fechas como texto en formato `DD/MM/AAAA`**: no ordenan cronológicamente.
- **Usar `float` para sumar dinero** sin una regla de redondeo.
- **Normalizar valores desconocidos a valores válidos.**

## Para comprobar que entendiste

1. ¿Qué hace `errors="coerce"` y qué debes hacer después?
2. ¿Por qué se pasa `format="%d/%m/%Y"`?
3. ¿Cuál es el orden correcto para limpiar `"Bs 1.250,50"`?
4. ¿Qué es `NaT`?

<details><summary>Respuestas</summary>

1. Convierte lo inválido en vacío en vez de fallar; después hay que contar y apartar esas filas con su motivo.
2. Para que Pandas no adivine y no confunda día con mes.
3. Quitar `Bs`, quitar espacios, quitar el punto de miles y cambiar la coma por punto.
4. El valor vacío de las fechas.

</details>

## Micropráctica

1. Convierte `["15,5", "8", "abc", "1.200,75"]` a números (decide el formato y documenta tu supuesto) y separa los inválidos.
2. Convierte `["2026-08-31", "31/08/2026", "08/31/2026", "x"]` a fechas siguiendo las reglas: ISO o DD/MM/AAAA; cualquier otra cosa es inválida.
3. Calcula los días entre cada fecha de `ventas.csv` y el corte `2026-09-30` y muestra los 3 más antiguos de ventas entregadas (compara con SQL 2.4).

Cómo saber que está bien: en la 3 la venta 1 tiene 58 días.

<details><summary>Comprobación de la parte 3</summary>

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas["fecha"] = pd.to_datetime(ventas["fecha"], format="%Y-%m-%d")
ventas["dias"] = (pd.Timestamp("2026-09-30") - ventas["fecha"]).dt.days
entregadas = ventas[ventas["estado"] == "entregado"]
print(entregadas.sort_values(["dias", "venta_id"], ascending=[False, True])[["venta_id", "dias"]].head(3))
```

```salida
   venta_id  dias
0         1    58
1         2    56
2         3    54
```

</details>

## Después, en los ejercicios

Conversiones, fechas y dinero son el núcleo de P09–P12 y P21–P28 en [Python](../../03_EJERCICIOS/Python/) y del mini-ETL. Declara tu regla para cada formato antes de convertir. Siguiente capítulo: [Capítulo 10 — Pandas: transformar, unir y validar](../10_Pandas_transformaciones.md).
