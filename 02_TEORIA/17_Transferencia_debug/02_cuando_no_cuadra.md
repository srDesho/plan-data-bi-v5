# 17.2 Cuando no cuadra: reducir el problema hasta encontrar el primer desvío

> Tiempo estimado: 60 min (lectura 25 + práctica 35). Prerrequisitos: [8.7 Pruebas y depuración](../08_Python_funciones_archivos/07_pruebas_y_depuracion.md), [10.6 Errores silenciosos](../10_Pandas_transformaciones/06_errores_silenciosos.md) y [17.1 Los ocho pasos](01_ocho_pasos_caso_nuevo.md).

## Para qué sirve

Tarde o temprano tu ETL terminará sin errores y con un total que no coincide con el esperado. Mirar el código «a ver qué pasa» no funciona. Lo que sí funciona es un método de **reducción**: comprobar capa por capa dónde aparece la primera diferencia, y luego documento por documento, hasta que el desvío se reduce a una o dos filas que sí puedes explicar.

## Términos nuevos

- **Primer desvío**: la primera etapa (o el primer documento) donde lo obtenido deja de coincidir con lo esperado.
- **Reducción** (o *bisección*): dividir el problema en partes y descartar la mitad que está bien, repetidamente.
- **Comparación por documento**: calcular el total de cada documento (venta, pedido) en ambas versiones y comparar uno a uno.
- **Cuadre de filas / de valor**: las dos igualdades de control (lección 5.3).
- **Diagnóstico**: la hipótesis de la causa, apoyada en una comprobación.
- **Síntoma / causa**: lo que se ve (un total mayor) y lo que lo produce (un merge que duplicó).
- **Regresión**: un error que reaparece al cambiar algo (lección 8.7).

## Ejemplo paso a paso

**El síntoma:** el ETL de ventas entregó un total de **Bs 2 050** y la fuente de control dice **Bs 1 150**. Hay Bs 900 de diferencia. Datos mínimos (inventados) para reproducir el problema: ventas con sus líneas y un catálogo de tiendas.

**Paso 0 · Congelar los datos y reproducir.**

```python
import pandas as pd

lineas = pd.DataFrame({
    "linea_id": [1, 2, 3, 4, 5],
    "venta_id": ["V1", "V1", "V2", "V3", "V4"],
    "importe": [200, 300, 250, 400, 100],
})
ventas = pd.DataFrame({
    "venta_id": ["V1", "V2", "V3", "V4"],
    "tienda": ["Luna", "Faro", "Luna", "Sol"],
    "estado": ["entregado", "entregado", "entregado", "anulado"],
})
catalogo = pd.DataFrame({
    "tienda": ["Luna", "Faro", "Sol", "Luna"],
    "ruta": ["R01", "R02", "R03", "R01"],
})

control = lineas.merge(ventas, on="venta_id", validate="m:1")
control = control[control["estado"] == "entregado"]["importe"].sum()
print("fuente de control:", control)

unido = lineas.merge(ventas, on="venta_id", validate="m:1").merge(catalogo, on="tienda", how="left")
etl = unido[unido["estado"] == "entregado"]["importe"].sum()
print("resultado del ETL:", etl)
print("diferencia:", etl - control)
```

```salida
fuente de control: 1150
resultado del ETL: 2050
diferencia: 900
```

Se reproduce el síntoma: el ETL da **2 050**, el control **1 150** y la diferencia es **900**. Lo primero es poder reproducirlo con datos mínimos, congelados, para que el problema no cambie mientras lo buscas.

**Paso 1 · Cuadre de filas por etapa.** ¿En qué paso cambió el número de filas?

```python
import pandas as pd

lineas = pd.DataFrame({"linea_id": [1, 2, 3, 4, 5], "venta_id": ["V1", "V1", "V2", "V3", "V4"], "importe": [200, 300, 250, 400, 100]})
ventas = pd.DataFrame({"venta_id": ["V1", "V2", "V3", "V4"], "tienda": ["Luna", "Faro", "Luna", "Sol"], "estado": ["entregado", "entregado", "entregado", "anulado"]})
catalogo = pd.DataFrame({"tienda": ["Luna", "Faro", "Sol", "Luna"], "ruta": ["R01", "R02", "R03", "R01"]})

paso1 = lineas.merge(ventas, on="venta_id", validate="m:1")
paso2 = paso1.merge(catalogo, on="tienda", how="left")
print("líneas:", len(lineas), "| tras unir ventas:", len(paso1), "| tras unir catálogo:", len(paso2))
```

```salida
líneas: 5 | tras unir ventas: 5 | tras unir catálogo: 8
```

Las filas pasan de 5 a 5 (primera unión: correcta) y de 5 a **8** en la segunda. **Ahí está el primer desvío:** el segundo merge multiplicó filas. El control de filas localizó la etapa en un solo paso.

**Paso 2 · Comparación por documento.** ¿Qué ventas se duplicaron?

```python
import pandas as pd

lineas = pd.DataFrame({"linea_id": [1, 2, 3, 4, 5], "venta_id": ["V1", "V1", "V2", "V3", "V4"], "importe": [200, 300, 250, 400, 100]})
ventas = pd.DataFrame({"venta_id": ["V1", "V2", "V3", "V4"], "tienda": ["Luna", "Faro", "Luna", "Sol"], "estado": ["entregado", "entregado", "entregado", "anulado"]})
catalogo = pd.DataFrame({"tienda": ["Luna", "Faro", "Sol", "Luna"], "ruta": ["R01", "R02", "R03", "R01"]})

antes = lineas.merge(ventas, on="venta_id").groupby("venta_id")["importe"].sum()
despues = lineas.merge(ventas, on="venta_id").merge(catalogo, on="tienda", how="left").groupby("venta_id")["importe"].sum()

comparacion = pd.DataFrame({"antes": antes, "despues": despues})
comparacion["diferencia"] = comparacion["despues"] - comparacion["antes"]
print(comparacion[comparacion["diferencia"] != 0])
```

```salida
          antes  despues  diferencia
venta_id                            
V1          500     1000         500
V3          400      800         400
```

Solo las ventas **V1** (500 → 1 000) y **V3** (400 → 800), las de la tienda «Luna», cambian: se duplican exactamente, y la suma de esas diferencias (500 + 400) es justo los 900 que sobran. Ambas pertenecen a la tienda que aparece **dos veces** en el catálogo. La pista pasó de «algo del merge» a «las ventas de Luna».

**Paso 3 · Formular la hipótesis y comprobarla con una consulta.**

```python
import pandas as pd

catalogo = pd.DataFrame({"tienda": ["Luna", "Faro", "Sol", "Luna"], "ruta": ["R01", "R02", "R03", "R01"]})
print(catalogo[catalogo.duplicated(subset=["tienda"], keep=False)])
print(catalogo["tienda"].is_unique)
```

```salida
  tienda ruta
0   Luna  R01
3   Luna  R01
False
```

Hipótesis: **el catálogo repite la tienda «Luna»** (una fila duplicada exacta), así que `merge` sin `validate` duplicó sus ventas. Se confirma. La causa raíz es un duplicado en el catálogo; el síntoma era un total mayor.

**Paso 4 · Corregir la causa (no el síntoma).** No se resta el exceso del total. Se corrige la unión: se deduplica el catálogo (si es un duplicado exacto) o se detiene el proceso (si hubiera contradicción), y se agrega `validate`:

```python
import pandas as pd

lineas = pd.DataFrame({"linea_id": [1, 2, 3, 4, 5], "venta_id": ["V1", "V1", "V2", "V3", "V4"], "importe": [200, 300, 250, 400, 100]})
ventas = pd.DataFrame({"venta_id": ["V1", "V2", "V3", "V4"], "tienda": ["Luna", "Faro", "Luna", "Sol"], "estado": ["entregado", "entregado", "entregado", "anulado"]})
catalogo = pd.DataFrame({"tienda": ["Luna", "Faro", "Sol", "Luna"], "ruta": ["R01", "R02", "R03", "R01"]})

catalogo_limpio = catalogo.drop_duplicates()
assert catalogo_limpio["tienda"].is_unique, "el catálogo tiene tiendas con rutas contradictorias"

unido = lineas.merge(ventas, on="venta_id", validate="m:1").merge(catalogo_limpio, on="tienda", how="left", validate="m:1")
print(len(unido), unido[unido["estado"] == "entregado"]["importe"].sum())
```

```salida
5 1150
```

Ahora las filas se mantienen en 5 y el total entregado es **1 150**, igual al de control. La frase final del diagnóstico: «El catálogo repetía la tienda Luna; se eliminó el duplicado exacto, se agregó `validate="m:1"` y el cuadre de valor cierra».

**Paso 5 · Prevenir: convertir el hallazgo en un control permanente.** Lo aprendido se vuelve una prueba que se ejecuta siempre:

```python
import pandas as pd


def verificar_catalogo(catalogo):
    repetidas = catalogo[catalogo.duplicated(subset=["tienda"], keep=False)]
    if len(repetidas):
        raise ValueError(f"catálogo con tiendas repetidas: {sorted(set(repetidas['tienda']))}")


verificar_catalogo(pd.DataFrame({"tienda": ["Luna", "Faro"], "ruta": ["R01", "R02"]}))
try:
    verificar_catalogo(pd.DataFrame({"tienda": ["Luna", "Luna"], "ruta": ["R01", "R02"]}))
except ValueError as e:
    print(e)
```

```salida
catálogo con tiendas repetidas: ['Luna']
```

Este control habría detenido el proceso la primera vez, con un mensaje claro.

**Catálogo de causas según el síntoma.**

| Síntoma | Causas frecuentes | Primer chequeo |
|---|---|---|
| filas no cuadran | filtros distintos; joins que multiplican o descartan; duplicados mal contados | filas por etapa |
| filas cuadran, dinero no | cantidades truncadas; precios mal interpretados (coma/punto); estados mal tratados; **presupuesto multiplicado** | total por documento |
| un solo grupo (una ruta) no cuadra | espacios o mayúsculas en la clave; catálogo con claves distintas | diferencia por grupo |
| el total es menor | huérfanas descartadas por `inner`; `groupby` que pierde claves vacías | `indicator`, `dropna=False` |
| el total es mayor | duplicados; unión por clave no única | `validate`, duplicados |

Orden de trabajo: **(1) reproducir con pocos datos, (2) cuadre de filas por etapa, (3) comparación por documento, (4) hipótesis, (5) corregir la causa, (6) convertirla en control.**

Ejemplo comercial: «el reporte de Power BI da 3 % más que el de SQL». Reproduces con una ruta, comparas filas por etapa y por documento, y descubres que el catálogo de clientes tenía una fila duplicada. Se corrige el catálogo en el origen y se agrega la prueba al ETL.

## Errores comunes

- **Restar la diferencia** del total para «cuadrar».
- **Cambiar varias cosas a la vez.**
- **Buscar con todos los datos** en lugar de reducir.
- **No convertir el hallazgo en un control permanente.**
- **Culpar a la herramienta sin comparar por documento.**
- **No documentar el diagnóstico.**
- **Resolver un conflicto de claves eligiendo la primera fila.**

## Para comprobar que entendiste

1. ¿Qué es el primer desvío y cómo se encuentra?
2. Si las filas cuadran pero el dinero no, ¿qué comparas?
3. ¿Por qué no se corrige restando la diferencia?
4. ¿Qué haces después de corregir la causa?

<details><summary>Respuestas</summary>

1. La primera etapa o documento donde lo obtenido deja de coincidir; se encuentra comparando filas y totales etapa por etapa.
2. Los importes por documento entre ambas versiones.
3. Porque se esconde el síntoma y la causa sigue produciendo errores.
4. Convertir el hallazgo en un control permanente (prueba o validación).

</details>

## Micropráctica

1. Construye un caso con un total que no cuadra por una causa que tú inventes (por ejemplo, una cantidad truncada) y aplica los cinco pasos.
2. Escribe el diagnóstico en una frase: síntoma, causa, corrección y control.
3. Provoca el error de «un solo grupo no cuadra» con una clave con espacios y diagnostícalo.

Cómo saber que está bien: tu reducción pasa de «el total» a «una o dos filas» y tu corrección es sobre la causa.

<details><summary>Ejemplo de la parte 3</summary>

```python
import pandas as pd

ventas = pd.DataFrame({"ruta": ["R01", "R01 ", "R02"], "importe": [100, 50, 70]})
catalogo = pd.DataFrame({"ruta": ["R01", "R02"], "zona": ["Norte", "Centro"]})
r = ventas.merge(catalogo, on="ruta", how="left", indicator=True)
print(r["_merge"].value_counts().to_dict())
print(r[r["_merge"] == "left_only"]["ruta"].tolist())
```

```salida
{'both': 2, 'left_only': 1, 'right_only': 0}
['R01 ']
```

</details>

## Después, en los ejercicios

Aplica este método en DB02 y DB03 ([`03_EJERCICIOS/Depuracion/`](../../03_EJERCICIOS/Depuracion/)), en el mini-ETL y en el caso C06. Registra cada diagnóstico en `errores.md`. Siguiente: [17.3 Resolver sin ayuda externa](03_resolver_sin_ia.md).
