# 6.4 Productividad, crecimiento y variaciones

> Tiempo estimado: 55 min (lectura 20 + práctica 35). Prerrequisitos: [6.1](01_que_es_un_kpi.md), [4.3 Funciones de ventana](../04_SQL_CTE_ventanas/03_ventanas.md) (LAG) y [8.1 Funciones con contrato](../08_Python_funciones_archivos/01_funciones_con_contrato.md).

## Para qué sirve

Dos preguntas de gestión: *¿cuánto produce cada vendedor (o ruta) por unidad de tiempo?* y *¿estamos mejor o peor que antes?* La primera es **productividad**; la segunda, **variación** (absoluta y porcentual). Las dos se calculan con una resta o una división, pero tienen trampas: comparar períodos distintos, dividir entre cero cuando antes no había nada, y confundir un incremento con una causa.

## Términos nuevos

- **Productividad**: la salida útil dividida entre el recurso empleado y el tiempo: ventas por vendedor por día, entregas por día, visitas realizadas por día. Hay que declarar **cuál** se usa.
- **Día efectivo**: un día en que hubo actividad (aquí, un día con al menos una venta entregada del vendedor). Otras fichas usan días hábiles; hay que escoger y declarar.
- **Variación absoluta**: valor actual − valor de referencia, en las mismas unidades (Bs, unidades).
- **Variación relativa (porcentual)**: variación absoluta / valor de referencia × 100.
- **Referencia (o base)**: el valor contra el que se compara (el mes anterior, la meta, el mismo mes del año pasado).
- **Base cero**: cuando la referencia es 0, la variación relativa **no está definida** (no se puede dividir entre cero).
- **Período comparable**: dos períodos con la misma duración, mismos días hábiles y mismos criterios.

## Ejemplo paso a paso

**1. Productividad por vendedor.** Importe entregado por vendedor y por día efectivo, usando la ficha de ventas entregadas:

```sql
SELECT vd.nombre AS vendedor,
       COUNT(DISTINCT v.fecha) AS dias_con_ventas,
       COUNT(DISTINCT v.venta_id) AS entregas,
       ROUND(SUM(l.cantidad * l.precio_unitario), 2) AS importe_bs,
       ROUND(SUM(l.cantidad * l.precio_unitario) / COUNT(DISTINCT v.fecha), 2) AS bs_por_dia
FROM venta_lineas AS l
INNER JOIN ventas AS v ON v.venta_id = l.venta_id
INNER JOIN vendedores_ej AS vd ON vd.vendedor_id = v.vendedor_id
WHERE v.estado = 'entregado'
GROUP BY vd.nombre
ORDER BY importe_bs DESC;
```

```resultado
vendedor | dias_con_ventas | entregas | importe_bs | bs_por_dia
Ana | 7 | 7 | 1265.0 | 180.71
Marta | 3 | 3 | 557.5 | 185.83
Luis | 4 | 4 | 510.0 | 127.5
```

Lectura: Ana vende más en total (1 265 Bs), pero Marta tiene el mayor importe por día con ventas (185,83 frente a 180,71). Observa tres cuidados:

1. Se **declaró** la medida: Bs por día con ventas (no «por día hábil»).
2. Se usó `COUNT(DISTINCT v.fecha)` y `COUNT(DISTINCT v.venta_id)` porque el JOIN al detalle repite las filas (lección 3.4).
3. El vendedor Pedro (id 4) **no aparece**: no tuvo ventas. Un reporte de productividad que lo omita está ocultando a alguien con productividad cero; si la lista de vendedores es la población, habría que usar un `LEFT JOIN` desde `vendedores_ej`.

**2. Variación absoluta y relativa entre dos meses.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1")
base = base[base["estado"] == "entregado"]
base["mes"] = base["fecha"].str[:7]

por_mes = base.groupby("mes")["importe"].sum()
anterior, actual = por_mes["2026-08"], por_mes["2026-09"]

absoluta = actual - anterior
relativa = absoluta / anterior * 100
print(anterior, actual)
print(absoluta)
print(round(relativa, 1))
```

```salida
993.5 1339.0
345.5
34.8
```

De 993,5 Bs en agosto a 1 339 Bs en septiembre: variación absoluta **+345,5 Bs** y relativa **+34,8 %**. Es el mismo resultado que el `LAG` de la lección 4.3. Dos reglas: la referencia va en el **denominador**, y se reportan **ambas** (un +34,8 % sobre una base pequeña puede ser poco dinero).

**3. Una función con contrato (y la base cero).**

```python
def variacion_pct(actual, referencia):
    """Variación porcentual respecto a la referencia, o None si la referencia es 0."""
    if referencia == 0:
        return None
    return (actual - referencia) / referencia * 100


print(variacion_pct(120000, 100000))
print(variacion_pct(80, 100))
print(variacion_pct(50, 0))
print(variacion_pct(0, 0))
```

```salida
20.0
-20.0
None
None
```

Si el mes anterior fue 0, la variación porcentual **no existe**: devuelve `None` (no «infinito» ni 100 %). En el reporte se escribe «n/c» (no calculable) y se informa la variación absoluta. Los ejemplos: de 100 000 a 120 000 Bs es +20 %; de 100 a 80 es −20 %.

**4. La asimetría de los porcentajes.** Una caída del 50 % y una subida del 50 % no se compensan:

```python
valor = 100.0
valor = valor * 0.5
print(valor)
valor = valor * 1.5
print(valor)
```

```salida
50.0
75.0
```

100 → 50 (−50 %) → 75 (+50 %): terminas en 75, no en 100. Para volver a 100 desde 50 hace falta +100 %. Por eso los porcentajes no se suman entre períodos; se encadenan multiplicando o se vuelve a calcular contra la base original.

**5. Períodos comparables.** Comparar «septiembre (30 días)» con «octubre hasta el día 12» muestra una caída que no existe. Dos soluciones: comparar contra el mismo tramo del mes anterior (los primeros 12 días de cada mes) o usar un indicador diario (Bs por día).

```python
import pandas as pd

ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
ventas["fecha"] = pd.to_datetime(ventas["fecha"])
entregadas = ventas[ventas["estado"] == "entregado"]

# Ventas entregadas en los primeros 15 días de cada mes (conteo), para comparar tramos iguales
primeros_15 = entregadas[entregadas["fecha"].dt.day <= 15]
print(primeros_15.groupby(primeros_15["fecha"].dt.strftime("%Y-%m")).size().to_dict())
```

```salida
{'2026-08': 3, '2026-09': 5}
```

En los primeros 15 días hubo 3 entregas en agosto y 5 en septiembre (+66,7 %), mientras que el mes completo muestra 6 contra 8 (+33,3 %). La dirección es la misma, pero la magnitud depende del tramo que compares. Antes de afirmar «crecimos un X %», confirma que comparas lo mismo.

**6. Variación contra la meta.** La brecha (lección 6.2) es una variación contra la referencia «meta»: `brecha = real − meta` (positiva = superó) y `variación relativa = brecha / meta`. Para R03 en septiembre: `160 − 300 = −140 Bs`, es decir `−46,7 %`; y el cumplimiento de 53,3 % es el complemento (`100 − 46,7`).

**7. Una variación no es una causa.** «Las ventas subieron 34,8 %»: ¿por una promoción, por un cliente grande, por más días hábiles, porque se registró tarde el mes anterior? El indicador describe; la explicación necesita datos adicionales y, para hablar de causa, un diseño comparativo (capítulo 12).

Ejemplo comercial: un vendedor «creció 200 %» porque el mes anterior estuvo de vacaciones y vendió casi nada. La variación relativa sobre una base minúscula exagera; la absoluta y la mediana de varios meses cuentan mejor la historia.

## Errores comunes

- **Dividir entre una referencia 0** y presentar un porcentaje.
- **Calcular la variación en el sentido contrario** (referencia en el numerador).
- **Sumar variaciones porcentuales** de períodos distintos.
- **Comparar períodos incompletos** o de distinta duración.
- **Reportar solo el porcentaje** y no la variación absoluta.
- **No declarar la medida de productividad** (por día, por hora, por visita).
- **Omitir a quienes tienen productividad cero** (INNER JOIN) y subestimar el problema.
- **Atribuir una causa** a la variación.

## Para comprobar que entendiste

1. ¿Cuál es la variación porcentual de 60 a 75? ¿Y de 75 a 60?
2. ¿Qué haces si la referencia es 0?
3. ¿Por qué los porcentajes de 100 → 50 → 75 no se «compensan»?
4. ¿Por qué se usa `COUNT(DISTINCT venta_id)` en la productividad?

<details><summary>Respuestas</summary>

1. +25 % y −20 %: la referencia cambia, y con ella el porcentaje.
2. La variación relativa no está definida: se reporta «n/c» y se informa la variación absoluta.
3. Porque cada porcentaje se calcula sobre una base distinta.
4. Porque el JOIN al detalle repite cada venta una vez por línea y `COUNT(*)` contaría líneas.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Calcula la productividad por **vendedor** medida como entregas por día con ventas.
2. Calcula la variación absoluta y relativa de las **entregas** (número de ventas entregadas) entre agosto y septiembre.
3. Calcula la variación de cada ruta entre agosto y septiembre (importe entregado), usando tu función `variacion_pct` y mostrando «n/c» cuando corresponda.

Cómo saber que está bien: de 6 a 8 entregas hay +33,3 %.

<details><summary>Comprobación de la parte 2</summary>

```python
agosto, septiembre = 6, 8
print(septiembre - agosto, round((septiembre - agosto) / agosto * 100, 1))
```

```salida
2 33.3
```

</details>

## Después, en los ejercicios

La productividad se practica en J4 y las variaciones en N5 y N1 de [SQL](../../03_EJERCICIOS/SQL/INDICE.md). Escribe la medida elegida, la referencia y qué haces con la base cero antes de consultar. Siguiente: [6.5 ABC, Pareto y rotación de inventario](05_abc_pareto_rotacion.md).
