# 15.3 Tablas dinámicas, estadística en Excel y el cuadre entre herramientas

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisitos: [15.2 Funciones para cuadrar](02_funciones_para_cuadrar.md), [11.4 Dispersión](../11_Estadistica_descriptiva/04_dispersion.md) y [11.5 Percentiles](../11_Estadistica_descriptiva/05_percentiles_atipicos.md).
>
> **Estado de verificación:** las acciones de interfaz de Excel y las fórmulas **no se ejecutaron automáticamente** en este paquete. Los valores esperados se calcularon con Python y sirven para que compares tu Excel.

## Para qué sirve

La tabla dinámica es la herramienta de Excel para resumir miles de filas en segundos, y el mejor segundo camino para verificar un `GROUP BY`. Pero solo sirve de prueba si compara contra SQL **lo mismo**: mismo período, mismo estado, misma tabla y misma unidad. Esta lección enseña a construir la tabla dinámica, a replicar en Excel las medidas estadísticas con el mismo método que Python y a **diagnosticar** una discrepancia entre herramientas.

## Términos nuevos

- **Tabla dinámica**: un resumen interactivo de una tabla: arrastras campos a *Filas*, *Columnas*, *Valores* y *Filtros*.
- **Campo de valor**: el campo que se resume (suma, cuenta, promedio).
- **Recuento distinto**: en la tabla dinámica, el conteo de valores únicos (requiere agregar la tabla al *Modelo de datos*).
- **`PERCENTIL.INC` / `PERCENTIL.EXC`**: percentiles con interpolación inclusiva (igual a NumPy y Pandas) o exclusiva (igual a `statistics.quantiles` por defecto).
- **`DESVEST.M` / `DESVEST.P`**: desviación estándar de muestra (`n − 1`) o de población (`n`).
- **Cuadre entre herramientas**: comprobar que SQL, Python, Excel y Power BI dan la misma cifra para la misma pregunta.
- **Discrepancia**: la diferencia entre dos cifras que deberían coincidir. Su diagnóstico sigue un orden fijo.
- **Registro del cuadre**: la nota (con fecha y capturas sin datos privados) donde se anotan las cifras comparadas.

## Ejemplo paso a paso

**1. Construir la tabla dinámica.** Con la tabla `tbl_ventas` (líneas unidas a la cabecera, con `ruta`, `estado` e `importe`):

1. *Insertar → Tabla dinámica*, origen `tbl_ventas`.
2. Arrastra `ruta` a *Filas*, `estado` a *Filtros* (selecciona solo `entregado`), `importe` a *Valores* (suma).
3. Agrega `importe` otra vez a *Valores* con **recuento** si quieres contar líneas.
4. Para contar ventas distintas: marca *Agregar estos datos al Modelo de datos* al crear la tabla y usa *Recuento distinto* de `venta_id`.

Resultado esperado (calculado con Python):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
t = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
t["importe"] = t["cantidad"] * t["precio_unitario"]
ent = t[t["estado"] == "entregado"]

resumen = ent.groupby("ruta").agg(importe=("importe", "sum"), lineas=("linea_id", "size"), ventas=("venta_id", "nunique"))
print(resumen)
print(resumen.sum().to_dict())
```

```salida
      importe  lineas  ventas
ruta                         
R01    1265.0      19       7
R02     510.0      10       4
R03     557.5       7       3
{'importe': 2332.5, 'lineas': 36.0, 'ventas': 14.0}
```

La tabla dinámica debe mostrar R01 1 265 (19 líneas, 7 ventas), R02 510 (10 líneas, 4 ventas) y R03 557,5 (7 líneas, 3 ventas), con **total general 2 332,5** y 14 ventas. Compara contra el SQL de 3.2. Con un promedio en *Valores*, la tabla dinámica calcula el promedio **por línea**, no el ticket (suma ÷ ventas distintas): para el ticket usa un campo calculado o, mejor, una medida.

**2. El promedio de promedios en la tabla dinámica.** Si pides «Promedio de importe» por ruta y luego miras el «Total general», este no es el promedio de los tres promedios de arriba: es el promedio de **todas las líneas**. Eso está bien; pero si tú sumaras o promediaras las tres cifras a mano, estarías haciendo el error de la lección 2.3.

**3. Estadística en Excel con el mismo método que Python.** Con los datos de 11.5 (entregas por repartidor: `12, 15, 15, 18, 20, 22, 25, 28, 30, 55`), en las celdas `A1:A10`:

| Qué calculas | Fórmula Excel | Valor esperado |
|---|---|---|
| media | `=PROMEDIO(A1:A10)` | 24 |
| mediana | `=MEDIANA(A1:A10)` | 21 |
| desviación de muestra | `=DESVEST.M(A1:A10)` | 12,36 |
| desviación de población | `=DESVEST.P(A1:A10)` | 11,73 |
| Q1 (inclusivo) | `=PERCENTIL.INC(A1:A10;0,25)` | 15,75 |
| Q3 (inclusivo) | `=PERCENTIL.INC(A1:A10;0,75)` | 27,25 |
| Q1 (exclusivo) | `=PERCENTIL.EXC(A1:A10;0,25)` | 15 |
| Q3 (exclusivo) | `=PERCENTIL.EXC(A1:A10;0,75)` | 28,5 |

Verificación con Python (los mismos números, por otro camino):

```python
import statistics
import numpy as np

datos = [12, 15, 15, 18, 20, 22, 25, 28, 30, 55]
print(statistics.mean(datos), statistics.median(datos))
print(round(statistics.stdev(datos), 2), round(statistics.pstdev(datos), 2))
print(np.percentile(datos, [25, 75]).tolist())
print(statistics.quantiles(datos, n=4))
```

```salida
24 21.0
12.36 11.73
[15.75, 27.25]
[15.0, 21.0, 28.5]
```

`PERCENTIL.INC` coincide con NumPy (15,75 y 27,25) y `PERCENTIL.EXC` con `statistics.quantiles` por defecto (15 y 28,5). Igual que en Python: **escribe qué método usaste**. Los límites de atípicos (`Q1 − 1,5·IQR` y `Q3 + 1,5·IQR`) se calculan en celdas auxiliares; marca el atípico con **formato condicional**, pero **conserva la fila** y anota el motivo de revisión. El formato condicional ayuda a ver diferencias; no sustituye la comprobación numérica.

**4. Los separadores en estas fórmulas.** Si tu Excel usa coma como separador de argumentos, escribe `=PERCENTIL.INC(A1:A10,0.25)`; con configuración regional de coma decimal, el 0,25 se escribe `0,25` y el separador de argumentos es `;`. No cambies a la vez el decimal y el separador.

**5. Diagnóstico de una discrepancia.** SQL da 2 332,5 y Excel da 2 721,5. La diferencia es 389. Orden de revisión:

| Pregunta | Si la respuesta es «no» o «sí» |
|---|---|
| ¿Mismo **período**? | filtra el mismo rango de fechas |
| ¿Mismo **estado**? | Excel incluyó anuladas (389 Bs son las anuladas) |
| ¿Misma **tabla/nivel**? | ¿líneas contra ventas? ¿se sumó la cabecera repetida? |
| ¿Misma **unidad**? | ¿centavos contra Bs? ¿miles? |
| ¿Mismos **tipos**? | ¿algún monto importado como texto? |
| ¿Mismas **claves**? | ¿espacios o códigos distintos en la unión? |

En el ejemplo, 389 es exactamente el importe de las ventas anuladas: el Excel olvidó filtrar `estado = "entregado"`. Se confirma:

```python
import pandas as pd

l = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
v = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
t = l.merge(v, on="venta_id", validate="m:1")
t["importe"] = t["cantidad"] * t["precio_unitario"]
print(t["importe"].sum(), t[t["estado"] == "entregado"]["importe"].sum(), t[t["estado"] == "anulado"]["importe"].sum())
```

```salida
2721.5 2332.5 389.0
```

**Antes de culpar a Excel, fija mismo período, estado, tabla y unidad.** Si una sola ruta cambia y el total no, revisa el código y los espacios de la unión.

**6. El registro del cuadre.** Una tabla corta en una hoja «Cuadre»:

| Cifra | SQL | Python | Excel | Power BI | ¿Cuadra? |
|---|---|---|---|---|---|
| Ventas entregadas (Bs) | 2 332,5 | 2 332,5 | 2 332,5 | (lo que muestre tu tarjeta) | ☐ |
| Pedidos entregados | 14 | 14 | 14 | | ☐ |
| Ticket (Bs) | 166,61 | 166,61 | 166,61 | | ☐ |

Anota la fecha y la versión de los datos. Si una captura incluye datos privados, no la guardes.

Ejemplo comercial: el jefe pregunta si el reporte de Power BI «está bien». La respuesta no es «sí», sino una tabla de cuadre: tres herramientas, tres cifras iguales, y la fecha en que se comprobó.

## Errores comunes

- **Comparar cifras de períodos, estados o tablas distintas.**
- **Promediar los promedios de la tabla dinámica.**
- **Tomar el «promedio» de la tabla dinámica por el ticket.**
- **Usar `PERCENTIL.EXC` y comparar contra Python sin saber la diferencia.**
- **Mezclar `DESVEST.M` y `DESVEST.P`.**
- **Eliminar la fila atípica** en vez de marcarla.
- **Culpar a la herramienta** antes de revisar los criterios.
- **No guardar el registro del cuadre.**

## Para comprobar que entendiste

1. ¿Qué tipo de promedio calcula la tabla dinámica por defecto sobre líneas?
2. ¿Qué fórmula de Excel coincide con `np.percentile`?
3. Si Excel da 2 721,5 y SQL 2 332,5, ¿qué estado se olvidó filtrar?
4. ¿Qué debe contener el registro del cuadre?

<details><summary>Respuestas</summary>

1. El promedio de las líneas (no el ticket).
2. `PERCENTIL.INC`.
3. El de las ventas anuladas (389 Bs).
4. Las cifras comparadas por herramienta, la fecha, la versión de los datos y si cuadran.

</details>

## Micropráctica

1. Construye una tabla dinámica de unidades entregadas por categoría de artículo (necesitas traer la categoría) y compárala con SQL.
2. Calcula en Excel `PERCENTIL.INC` y `DESVEST.M` de la columna `precio` de `articulos.csv` y compáralos con Python.
3. Prepara un registro de cuadre de tres cifras de la mini-base.
4. Provoca a propósito una discrepancia (quita el filtro de estado) y diagnostícala con la tabla del paso 5.

Cómo saber que está bien: el total de unidades entregadas es 323.

<details><summary>Cifras de control de la parte 2</summary>

```python
import numpy as np
import statistics

precios = [6.0, 9.0, 11.5, 7.5, 4.5, 5.0, 14.0, 3.5, 8.0, 12.0]
print(np.percentile(precios, [25, 75]).tolist(), round(statistics.stdev(precios), 3))
```

```salida
[5.25, 10.875] 3.51
```

</details>

## Después, en los ejercicios

EX01 (tabla dinámica de rutas y comparación con SQL), EX02 (presupuesto por mes y ruta) y EX03 (percentiles) en [`03_EJERCICIOS/Casos/`](../../03_EJERCICIOS/Casos/) se resuelven con esta lección; sus criterios están allí. Las acciones de interfaz de Excel son comprobación manual. Siguiente capítulo: [Capítulo 16 — Git y comunicación](../16_Git_comunicacion.md).
