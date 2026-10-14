# 14.4 Medidas útiles de un tablero comercial y cómo controlarlas

> Tiempo estimado: 65 min (lectura 30 + práctica 35). Prerrequisitos: [14.3 DAX y contexto](03_dax_contexto.md) y [6.2 Cumplimiento, cobertura y efectividad](../06_KPIs/02_cumplimiento_cobertura_efectividad.md).
>
> **Estado de verificación:** el código DAX **no se ejecutó en Power BI Desktop**. Los valores esperados que se indican sí se calcularon con Python sobre la mini-base; úsalos para comprobar tu tablero.

## Para qué sirve

Un tablero comercial casi siempre usa las mismas siete medidas: ventas, pedidos, ticket, meta, cumplimiento, participación sobre el total y comparación con el mes anterior. Aquí tienes cada una con su fórmula DAX, lo que hace, el valor que debe mostrar y la trampa más común. Escríbelas **una por una**, comprobando cada valor antes de pasar a la siguiente.

## Términos nuevos

- **Medida base**: una medida simple que otras reutilizan (`Ventas Bs`, `Pedidos`, `Meta Bs`).
- **Medida derivada**: una medida construida a partir de otras (`Ticket`, `Cumplimiento`).
- **Participación del total**: el porcentaje que representa el valor visible sobre un total de referencia.
- **`ALLSELECTED`**: devuelve el conjunto de filas que el usuario tiene seleccionado en los segmentadores, ignorando las filas y columnas del visual. Sirve para «% de lo seleccionado».
- **`REMOVEFILTERS`** (o `ALL`): quita filtros por completo; el denominador pasa a ser el total absoluto.
- **`DATEADD`**: desplaza un conjunto de fechas en el tiempo (un mes atrás). Requiere una tabla de fechas completa y marcada.
- **Inteligencia de tiempo** (*time intelligence*): funciones que comparan períodos (mes anterior, acumulado del año).

## Ejemplo paso a paso

Se usan las siguientes tablas: `fact_ventas` (línea de venta con `estado`, `ruta`, `mes`, `monto_centavos`, `venta_id`), `fact_metas` (`mes`, `ruta`, `meta_centavos`), `dim_ruta`, `dim_mes` y `dim_fecha`.

**Medida 1 · Ventas Bs**

```text
Ventas Bs =
DIVIDE(CALCULATE(SUM(fact_ventas[monto_centavos]), fact_ventas[estado] = "entregado"), 100)
```

Valor esperado sin filtros: **2 332,5**. Trampa: olvidar el filtro de estado (daría 2 721,5).

**Medida 2 · Pedidos**

```text
Pedidos = CALCULATE(DISTINCTCOUNT(fact_ventas[venta_id]), fact_ventas[estado] = "entregado")
```

Esperado: **14**. Trampa: usar `COUNTROWS(fact_ventas)`, que contaría líneas (36).

**Medida 3 · Ticket Bs**

```text
Ticket Bs = DIVIDE([Ventas Bs], [Pedidos])
```

Esperado: **166,61**. Es una razón: no se suma.

**Medida 4 · Meta Bs**

```text
Meta Bs = DIVIDE(SUM(fact_metas[meta_centavos]), 100)
```

Esperado sin filtros: **2 400** (todas las rutas y los dos meses). Con septiembre: **1 350**. Con septiembre y R03: **300**. Trampa: si la meta se conectara con el hecho de ventas, o a nivel de tienda, se multiplicaría.

**Medida 5 · Cumplimiento %**

```text
Cumplimiento % = DIVIDE([Ventas Bs], [Meta Bs])
```

(se da formato porcentual en el modelo). Esperado en septiembre: **99,2 %** (1 339 / 1 350); R03: **53,3 %**. Trampa: convertir el `BLANK` en 0 cuando falta la meta.

**Medida 6 · % del total seleccionado**

```text
% de Ventas Seleccionadas =
DIVIDE([Ventas Bs], CALCULATE([Ventas Bs], ALLSELECTED(dim_ruta)))
```

En una tabla con las tres rutas, cada fila divide sus ventas entre el total de las rutas seleccionadas: R01 54,2 %, R02 21,9 %, R03 23,9 % (suman 100). Si el usuario selecciona solo R01 y R02, los porcentajes se recalculan sobre esas dos. Con `REMOVEFILTERS(dim_ruta)` en vez de `ALLSELECTED`, el denominador sería siempre el total de todas las rutas. **El título del visual debe decir cuál de los dos es.**

**Medida 7 · Ventas del mes anterior y variación**

```text
Ventas Mes Anterior Bs = CALCULATE([Ventas Bs], DATEADD(dim_fecha[fecha], -1, MONTH))
Variación % = DIVIDE([Ventas Bs] - [Ventas Mes Anterior Bs], [Ventas Mes Anterior Bs])
```

Esperado en septiembre: mes anterior **993,5**; variación **+34,8 %**. En agosto, el mes anterior no existe: `BLANK` y la variación también. Trampa: un corte parcial (mes incompleto) contra un mes completo exagera la variación; debe explicarse en el título.

**Cómo calcular todos los valores esperados.** Para tener las cifras de control en un solo lugar:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
fact["mes"] = fact["fecha"].str[:7]
fact["importe"] = fact["cantidad"] * fact["precio_unitario"]
ent = fact[fact["estado"] == "entregado"]

print("Ventas Bs:", ent["importe"].sum())
print("Pedidos:", ent["venta_id"].nunique(), "| COUNTROWS (líneas):", len(ent))
print("Ticket:", round(ent["importe"].sum() / ent["venta_id"].nunique(), 2))
print("Meta total:", metas["meta_bs"].sum(), "| sept:", metas[metas["mes"] == "2026-09"]["meta_bs"].sum())

sep = ent[ent["mes"] == "2026-09"]["importe"].sum()
ago = ent[ent["mes"] == "2026-08"]["importe"].sum()
print("Cumplimiento sept:", round(sep / 1350 * 100, 1))
print("Mes anterior:", ago, "| variación %:", round((sep - ago) / ago * 100, 1))

por_ruta = ent.groupby("ruta")["importe"].sum()
print((por_ruta / por_ruta.sum() * 100).round(1).to_dict())
```

```salida
Ventas Bs: 2332.5
Pedidos: 14 | COUNTROWS (líneas): 36
Ticket: 166.61
Meta total: 2400.0 | sept: 1350.0
Cumplimiento sept: 99.2
Mes anterior: 993.5 | variación %: 34.8
{'R01': 54.2, 'R02': 21.9, 'R03': 23.9}
```

Imprime exactamente los valores esperados que se anotaron arriba. Cópialos a una hoja de control y compáralos con las tarjetas de Desktop.

**Control cruzado entre herramientas.** La misma cifra debe obtenerse por tres caminos: SQL (`SUM` con JOIN y filtro de estado), Excel (tabla dinámica) y Power BI (medida). Si dos coinciden y una no, el problema está en esa herramienta: relaciones y filtros en Power BI; tipos y filtro en Excel; JOIN y `WHERE` en SQL.

**Orden de construcción recomendado:**

1. Cargar las tablas y comprobar filas y suma de `monto_centavos`.
2. Crear las relaciones (13.2) y marcar la tabla de fechas.
3. Crear `Ventas Bs` y compararla sin filtros con 2 332,5.
4. Crear `Pedidos` y `Ticket`. Comparar.
5. Crear `Meta Bs` y comprobar con septiembre y R03.
6. Crear `Cumplimiento %`.
7. Solo entonces los visuales.

**Qué no puede probar este paquete.** Que las relaciones estén bien creadas en tu `.pbix`, que los segmentadores filtren todas las tablas y que la actualización funcione en tu equipo. Eso lo compruebas tú siguiendo la lista del final del capítulo.

Ejemplo comercial: la tarjeta «Cumplimiento» debe mostrar 99,2 % en septiembre. Si muestra 24,8 %, probablemente la meta se sumó 4 veces (relación mal conectada); si muestra 100 %, se está usando una medida de ventas sin filtro de mes.

## Errores comunes

- **Crear todas las medidas antes de comprobar la primera.**
- **No tener las cifras esperadas** para comparar.
- **Usar `COUNTROWS` del hecho** para contar pedidos.
- **Confundir `ALLSELECTED` con `REMOVEFILTERS`** y no aclararlo en el título.
- **Calcular «mes anterior» sin una tabla de fechas completa y marcada.**
- **Meta conectada a un nivel que la multiplica.**
- **Convertir `BLANK` en 0.**
- **Presentar cifras sin haberlas cruzado con SQL o Excel.**

## Para comprobar que entendiste

1. ¿Por qué se usa `DISTINCTCOUNT` para los pedidos?
2. ¿Qué cambia entre `ALLSELECTED` y `REMOVEFILTERS` en el denominador?
3. ¿Qué mostraría `Ventas Mes Anterior` para el primer mes de los datos?
4. ¿Qué haces si dos herramientas dan el mismo número y la tercera no?

<details><summary>Respuestas</summary>

1. Porque el hecho tiene una fila por línea y cada pedido aparece varias veces.
2. `ALLSELECTED` respeta lo que el usuario seleccionó en los segmentadores; `REMOVEFILTERS` usa siempre el total absoluto.
3. `BLANK` (no hay mes anterior en los datos).
4. Reviso la herramienta discrepante: relaciones y filtros, tipos, o JOIN y `WHERE`.

</details>

## Micropráctica

1. Escribe en DAX las medidas `Visitas Planificadas`, `Visitas Realizadas` y `Cobertura de Ejecución %` para `fact_visitas`.
2. Calcula con Python los valores esperados (14, 11 y 78,6 %).
3. Escribe el título de un visual que muestre `% de Ventas Seleccionadas` aclarando la referencia del denominador.
4. Define qué cifras de control comparas después de cargar `fact_visitas`.

Cómo saber que está bien: tus valores esperados coinciden con 14, 11 y 78,6.

<details><summary>Comprobación de la parte 2</summary>

```python
import pandas as pd

v = pd.read_csv("04_DATASETS/mini_base/visitas.csv")
print(len(v), int(v["realizada"].sum()), round(v["realizada"].sum() / len(v) * 100, 1))
```

```salida
14 11 78.6
```

</details>

## Después, en los ejercicios

El archivo `medidas.dax` del proyecto de Power BI sigue este orden ([`05_PROYECTOS/powerbi/`](../../05_PROYECTOS/)). Siguiente: [14.5 Diseño del tablero y lista de comprobación manual](05_diseno_y_comprobacion.md).
