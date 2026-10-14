# 10.6 Errores silenciosos: los que no avisan

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: lecciones 10.1 a 10.5.

## Para qué sirve

Los errores que se ven (un traceback) se corrigen en minutos. Los peligrosos son los que **no producen ningún mensaje** y entregan un número equivocado con apariencia de correcto. Esta lección es un catálogo de los más frecuentes en Pandas, cada uno con su demostración, la señal que lo delata y el control que lo detecta. Léela como una lista de revisión antes de entregar cualquier cifra.

## Términos nuevos

- **Error silencioso**: un fallo que no detiene el programa ni emite aviso, pero produce un resultado incorrecto.
- **Señal de alarma**: un síntoma que delata el error (un total que no cuadra, un `NaN` inesperado, un conteo mayor al de la tabla).
- **Control de cuadre**: la comparación entre dos cifras que deben coincidir por construcción.
- **Dato de prueba mínimo**: una tabla de pocas filas, calculable a mano, con la que compruebas que una transformación hace lo que crees.
- **Efecto de borde**: un comportamiento especial en los extremos o en casos raros (vacíos, ceros, repetidos).

## Ejemplo paso a paso

**1. Merge que duplica importes.** (Ya visto en 10.3; aquí el catálogo.)

```python
import pandas as pd

ventas = pd.DataFrame({"venta_id": [1, 2], "importe": [100.0, 50.0]})
estados = pd.DataFrame({"venta_id": [1, 2, 2], "estado": ["ok", "ok", "ok"]})

r = ventas.merge(estados, on="venta_id", how="left")
print(ventas["importe"].sum(), r["importe"].sum())
```

```salida
150.0 200.0
```

**Señal:** el total subió de 150 a 200. **Control:** compara la suma antes y después, y usa `validate="m:1"`.

**2. Alineación por índice que produce `NaN`.**

```python
import pandas as pd

ventas = pd.DataFrame({"importe": [10.0, 20.0, 30.0, 40.0]})
grandes = ventas[ventas["importe"] > 15]
descuento = pd.Series([1.0, 2.0, 3.0])

print((grandes["importe"] - descuento).tolist())
print((grandes["importe"].values - descuento.values).tolist())
```

```salida
[nan, 18.0, 27.0, nan]
[19.0, 28.0, 37.0]
```

`grandes` conserva las etiquetas de índice 1, 2, 3; `descuento` tiene 0, 1, 2. La resta por etiqueta empareja la etiqueta 1 con 1 y la 2 con 2, y deja `NaN` en las otras. La resta por **posición** (`.values`) da otro resultado, que es el que se quería. **Señal:** `NaN` donde no esperabas. **Control:** `reset_index(drop=True)` después de filtrar, o trabajar con columnas de la misma tabla.

**3. `groupby` que descarta las claves vacías.**

```python
import pandas as pd

df = pd.DataFrame({"zona": ["Norte", None, "Centro", None], "importe": [10, 20, 30, 40]})
print(df.groupby("zona")["importe"].sum().sum())
print(df.groupby("zona", dropna=False)["importe"].sum().sum())
print(df["importe"].sum())
```

```salida
40
100
100
```

Sin `dropna=False` el resumen por zona suma 40 y el total real es 100: se perdieron 60 Bs de ventas sin zona. **Señal:** los grupos no suman el total. **Control:** `dropna=False` y comparar la suma de los grupos con la de la tabla.

**4. Una columna de texto que «suma» como texto.**

```python
import pandas as pd

montos = pd.Series(["10", "20", "5"])
print(montos.sum())
print(pd.to_numeric(montos).sum())
```

```salida
10205
35
```

Con la columna en texto, `sum()` **concatena**: `"10205"`. Con la columna numérica, 35. **Señal:** un total absurdamente grande o un número con aspecto de texto. **Control:** revisar `dtypes` antes de sumar.

**5. Sumas de decimales con restos.**

```python
import pandas as pd

precios = pd.Series([0.1] * 10)
print(precios.sum())
print(precios.sum() == 1.0)
print(round(precios.sum(), 2) == 1.0)
```

```salida
1.0
True
True
```

Diez veces 0,1 no suma exactamente 1,0 en `float`. Un control `suma == total_esperado` con decimales puede **fallar sin que haya error de negocio** (o, peor, pasar por casualidad). **Control:** comparar con tolerancia (`abs(a - b) < 0.01`), trabajar en centavos enteros o redondear de forma declarada.

**6. Modificar una copia (y creer que modificaste la original).**

```python
import pandas as pd

df = pd.DataFrame({"estado": ["a", "b", "a"], "valor": [1, 2, 3]})
subconjunto = df[df["estado"] == "a"].copy()
subconjunto["valor"] = 0
print(df["valor"].tolist())
print(subconjunto["valor"].tolist())
```

```salida
[1, 2, 3]
[0, 0]
```

Cambiar `subconjunto` no tocó `df` (porque era una copia). Si lo que querías era cambiar `df`, debías usar `df.loc[df["estado"] == "a", "valor"] = 0`. A veces el problema es el inverso: modificas una "vista" y Pandas avisa con `SettingWithCopyWarning`. **Señal:** el cambio «no pega» o aparece esa advertencia. **Control:** `.copy()` explícito cuando quieres una tabla independiente y `.loc[filas, columna] = valor` cuando quieres modificar la original.

**7. Comparaciones con `NaN`.**

```python
import numpy as np
import pandas as pd

x = pd.Series([1.0, np.nan, 3.0])
print((x == np.nan).tolist())
print(x.isna().tolist())
print((x > 2).tolist())
print((x <= 2).tolist())
```

```salida
[False, False, False]
[False, True, False]
[False, False, True]
[True, False, False]
```

`NaN == NaN` es **falso**: nada es igual a `NaN`, ni siquiera `NaN`. Y `x <= 2` y `x > 2` son ambos falsos para el `NaN`, así que un filtro «mayor que 2» y su complemento «menor o igual a 2» **no suman todas las filas**. **Control:** usar `isna()` para los vacíos y contar que las partes suman el todo.

**8. Ordenar texto que parece número.**

```python
import pandas as pd

codigos = pd.Series(["10", "9", "100", "2"])
print(codigos.sort_values().tolist())
print(codigos.astype(int).sort_values().tolist())
```

```salida
['10', '100', '2', '9']
[2, 9, 10, 100]
```

Como texto, `"100"` va antes que `"2"` (orden alfabético). Como número, el orden es el esperado. **Señal:** un «top 5» con valores extraños. **Control:** verificar el tipo antes de ordenar.

**9. `value_counts()` y `nunique()` que ignoran vacíos.**

```python
import pandas as pd

estados = pd.Series(["entregado", "anulado", None, "entregado"])
print(estados.value_counts().sum(), len(estados))
print(estados.value_counts(dropna=False).sum())
print(estados.nunique(), estados.nunique(dropna=False))
```

```salida
3 4
4
2 3
```

Por defecto los vacíos no se cuentan: los conteos suman 3 de 4 filas. Para reconciliar, usa `dropna=False`.

**10. Fechas leídas con el formato equivocado.**

```python
import pandas as pd

texto = pd.Series(["03/04/2026"])
print(pd.to_datetime(texto, format="%d/%m/%Y")[0].strftime("%Y-%m-%d"))
print(pd.to_datetime(texto, format="%m/%d/%Y")[0].strftime("%Y-%m-%d"))
```

```salida
2026-04-03
2026-03-04
```

El mismo texto es 3 de abril o 4 de marzo según el formato. Un reporte con el formato equivocado «funciona» y está mal. **Control:** el formato sale del contrato del dato y se escribe en el código; compara una fecha conocida.

**11. El método de defensa: la tabla mínima.** Para cada transformación nueva, arma una tabla de 3 a 5 filas con los casos raros (vacío, repetido, extremo), calcula a mano el resultado esperado y comprueba que tu código lo reproduce. Si funciona ahí, aumenta el tamaño.

Ejemplo comercial: el reporte de ventas por zona sumaba Bs 61 000 y el total del sistema era Bs 68 400. La diferencia (Bs 7 400) eran las ventas de clientes sin zona, que `groupby` había descartado. Un solo control («los grupos suman el total») lo habría detectado el primer día.

## Errores comunes

- **Confiar en que «no hubo error» significa «está correcto».**
- **No tener un total independiente** con el cual comparar.
- **Probar solo con datos «buenos»** y no con casos de borde.
- **Ignorar las advertencias** (`SettingWithCopyWarning`, `FutureWarning`).
- **Comparar decimales con `==`.**
- **No revisar `dtypes` antes de sumar u ordenar.**
- **Corregir el síntoma (cambiar el total) en lugar de la causa.**

## Para comprobar que entendiste

1. ¿Por qué un `groupby` puede dar un total menor que el real?
2. ¿Qué devuelve `pd.Series(["10", "20"]).sum()`?
3. ¿Por qué `x == np.nan` no sirve para encontrar vacíos?
4. ¿Cuál es el control más universal contra errores silenciosos?

<details><summary>Respuestas</summary>

1. Porque descarta por defecto las filas cuya clave de grupo es vacía.
2. El texto `"1020"` (concatena).
3. Porque `NaN` no es igual a nada, ni a sí mismo; se usa `isna()`.
4. Comparar el resultado con un total o conteo calculado por otro camino (cuadre).

</details>

## Micropráctica

1. Construye una tabla de 6 filas con una clave repetida en el catálogo y demuestra que un merge sin `validate` infla el importe.
2. Construye una tabla con un vacío en la columna de agrupación y demuestra que `groupby` pierde importe. Corrígelo.
3. Para cada uno de los errores 2, 7 y 8 de la lección, escribe una frase con la señal y el control.
4. Elige una cifra de un ejemplo anterior de este curso y escribe el control por otro camino que la verificaría.

Cómo saber que está bien: puedes explicar, para cada caso, qué cifra no cuadraba y cómo lo detectaste.

<details><summary>Comprobación de la parte 2</summary>

```python
import pandas as pd

df = pd.DataFrame({"zona": ["A", "A", None, "B", None, "B"], "importe": [10, 20, 30, 40, 50, 60]})
print(df.groupby("zona")["importe"].sum().sum(), df["importe"].sum())
print(df.groupby("zona", dropna=False)["importe"].sum().sum())
```

```salida
130 210
210
```

</details>

## Después, en los ejercicios

Tras cada ejercicio P21–P28 y cada etapa del mini-ETL, aplica estos controles antes de pasar el corrector y registra en tu `errores.md` los silenciosos que encuentres. Siguiente capítulo: [Capítulo 6 — Indicadores (KPIs)](../06_KPIs.md).
