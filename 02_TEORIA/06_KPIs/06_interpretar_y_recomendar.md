# 6.6 Interpretar, recomendar y qué hacer cuando faltan datos

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: lecciones 6.1 a 6.5.

## Para qué sirve

Calcular un KPI es la mitad del trabajo; la otra mitad es **decir qué significa y qué conviene hacer**, sin exagerar lo que los datos permiten afirmar. Un reporte de indicadores útil tiene una estructura fija: *hallazgo, evidencia, interpretación, recomendación y límites*. Y cuando faltan datos (metas ausentes, devoluciones no registradas), lo correcto es decir «no calculable», no inventar un valor.

## Términos nuevos

- **Hallazgo**: lo que muestran los números, dicho en una frase.
- **Evidencia**: la cifra (y su fuente) que sostiene el hallazgo.
- **Interpretación**: qué significa el hallazgo para el negocio, con las salvedades.
- **Recomendación**: la acción concreta que se sugiere y quién la ejecuta.
- **Límites**: lo que los datos **no** permiten afirmar (causas, generalización, períodos).
- **Cobertura de datos**: qué proporción de lo que debería haber está realmente registrado (cuántas rutas tienen meta, cuántas ventas tienen fecha).
- **No calculable** («n/c»): el estado correcto de un indicador al que le falta el dato necesario.
- **Semáforo**: una forma de presentar un indicador con rangos (verde/amarillo/rojo) definidos **de antemano** en la ficha.

## Ejemplo paso a paso

**1. La estructura del mini-informe.** Con las cifras de las lecciones anteriores, un informe de septiembre sobre la ruta R03:

> **Hallazgo.** La ruta R03 vendió Bs 160 en septiembre frente a una meta de Bs 300: cumplimiento de 53,3 %, la brecha más alta de las tres rutas (R01: 133,3 %; R02: 84,2 %).
> **Evidencia.** Ventas entregadas de las tiendas de R03 (`ventas` + `venta_lineas` + `tiendas`) contra la meta de `metas` para 2026-09. Total de las tres rutas: Bs 1 339 sobre Bs 1 350 de meta (99,2 %).
> **Interpretación.** El cumplimiento global está en la meta, pero hay desigualdad entre rutas: R01 compensa lo que R03 no alcanza. El indicador no dice por qué R03 vendió menos: puede deberse a menos visitas, menor efectividad o una meta más exigente.
> **Recomendación.** Revisar para R03 la cobertura de ejecución y la efectividad antes de tomar una medida; comparar la meta de R03 con su venta histórica.
> **Límites.** Dos meses de datos inventados; una sola ruta con 4 tiendas; sin información de visitas por ruta.

Cada párrafo responde una pregunta distinta. El de **límites** es el que protege tu credibilidad.

**2. Verificar las cifras del informe contra los datos** (nada se escribe sin sostén):

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
base = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
base = base[(base["estado"] == "entregado") & (base["fecha"].str.startswith("2026-09"))]

vendido = base.groupby("ruta", as_index=False)["importe"].sum()
tabla = metas[metas["mes"] == "2026-09"].merge(vendido, on="ruta", validate="1:1")
tabla["cumpl_pct"] = (tabla["importe"] / tabla["meta_bs"] * 100).round(1)
print(tabla[["ruta", "meta_bs", "importe", "cumpl_pct"]])
print(round(tabla["importe"].sum() / tabla["meta_bs"].sum() * 100, 1))
```

```salida
  ruta  meta_bs  importe  cumpl_pct
0  R01    600.0    800.0      133.3
1  R02    450.0    379.0       84.2
2  R03    300.0    160.0       53.3
99.2
```

Las cifras del informe salen de aquí: R03 53,3 %, total 99,2 %. **Si cambias el análisis, vuelves a verificar el informe.**

**3. Cuando falta la meta de una ruta.** Quitamos la meta de R02 para ver cómo se comporta el informe:

```python
import pandas as pd

vendido = pd.DataFrame({"ruta": ["R01", "R02", "R03"], "importe": [800.0, 379.0, 160.0]})
metas = pd.DataFrame({"ruta": ["R01", "R03"], "meta_bs": [600.0, 300.0]})

tabla = vendido.merge(metas, on="ruta", how="left", validate="1:1")
tabla["cumpl_pct"] = (tabla["importe"] / tabla["meta_bs"] * 100).round(1)
print(tabla)
print(tabla["cumpl_pct"].isna().sum())
```

```salida
  ruta  importe  meta_bs  cumpl_pct
0  R01    800.0    600.0      133.3
1  R02    379.0      NaN        NaN
2  R03    160.0    300.0       53.3
1
```

El `LEFT JOIN` conserva a R02, y su cumplimiento queda `NaN` (**no calculable**), no 0 % ni 100 %. Un reporte correcto muestra «n/c» para R02 y avisa: *«La ruta R02 no tiene meta cargada para septiembre; su cumplimiento no se puede calcular. El cumplimiento global de las rutas con meta es X»*. Calcular el global con la meta de R02 considerada cero (o ignorando su venta) cambiaría la cifra sin que nadie lo sepa.

```python
import pandas as pd

tabla = pd.DataFrame({"ruta": ["R01", "R02", "R03"], "importe": [800.0, 379.0, 160.0], "meta_bs": [600.0, None, 300.0]})
con_meta = tabla.dropna(subset=["meta_bs"])
print(round(con_meta["importe"].sum() / con_meta["meta_bs"].sum() * 100, 1))
print(len(con_meta), "de", len(tabla), "rutas con meta")
```

```salida
106.7
2 de 3 rutas con meta
```

El cumplimiento de las rutas con meta (R01 y R03) es 106,7 %, calculado sobre **2 de 3 rutas**. Esa última frase, la **cobertura de datos**, es obligatoria: sin ella el número parece completo.

**4. Los datos faltantes más comunes y qué hacer.**

| Falta... | No hagas | Haz |
|---|---|---|
| la meta de una ruta | tomarla como 0 | indicar «n/c» y calcular con las rutas con meta, informando la cobertura |
| devoluciones y descuentos | llamar «neta» a la venta | llamar «entregada» y anotarlo |
| la fecha de una venta | asignarle una fecha cualquiera | rechazarla del período y contarla aparte |
| el stock inicial | suponer 0 | rotación «n/c» para ese producto |
| el denominador (0) | mostrar 0 % o infinito | «n/c» y la variación absoluta |
| el cliente de una venta | borrarla | «sin cliente» como categoría y avisar |

**5. Un semáforo con reglas de antemano.** Si se usa, los rangos se definen en la ficha, no después de ver los datos:

```python
def semaforo(cumplimiento):
    if cumplimiento is None:
        return "n/c"
    if cumplimiento >= 100:
        return "verde"
    if cumplimiento >= 80:
        return "amarillo"
    return "rojo"


for valor in (133.3, 99.2, 84.2, 53.3, None):
    print(valor, semaforo(valor))
```

```salida
133.3 verde
99.2 amarillo
84.2 amarillo
53.3 rojo
None n/c
```

Regla (inventada para el ejemplo): verde ≥ 100 %, amarillo 80–99,9 %, rojo < 80 %, y «n/c» si no hay dato. Un semáforo sin umbrales escritos es una opinión disfrazada.

**6. Qué NO puedes afirmar con estos indicadores.**

- Que un indicador **causa** otro (la efectividad baja no explica por sí sola la meta no cumplida).
- Que lo observado en dos meses **se mantendrá**.
- Que la mini-base **representa** a una distribuidora real.
- Que una mejora sea **mérito** de alguien sin comparar con un grupo similar.

Ejemplo comercial: «R03 está en rojo» se convierte en una buena decisión cuando el informe dice *cuánto*, *por qué podría ser*, *qué se revisará primero* y *qué no se sabe*.

## Errores comunes

- **Entregar números sin interpretación** ni recomendación.
- **Interpretar con más certeza que la que dan los datos.**
- **Rellenar con 0 o con promedios** lo que falta.
- **Omitir la cobertura de datos** en un indicador calculado con partes.
- **Definir los rangos del semáforo después de ver los resultados.**
- **Confundir correlación con causa** en la interpretación.
- **No volver a verificar las cifras** del informe tras cambiar el análisis.

## Para comprobar que entendiste

1. ¿Cuáles son las cinco partes de un mini-informe?
2. ¿Cómo se muestra un indicador al que le falta la meta?
3. ¿Por qué hay que informar la cobertura de datos?
4. ¿Qué es mejor: «R03 falló» o «R03 cumplió 53,3 % y se revisará su cobertura»?

<details><summary>Respuestas</summary>

1. Hallazgo, evidencia, interpretación, recomendación y límites.
2. Como «n/c» (no calculable), con aviso, no como cero.
3. Porque un indicador calculado con una parte de los datos parece completo si no se dice.
4. La segunda: describe, no acusa, y propone una acción verificable.

</details>

## Micropráctica

1. Escribe un mini-informe de cinco párrafos sobre la **efectividad comercial** de la mini-base (63,6 %), usando las cifras de la lección 6.2.
2. Define un semáforo para la efectividad (con umbrales escritos de antemano) y clasifica el valor.
3. Imagina que `visitas` no tuviera el campo `pedido_tomado` para las visitas del día 4: ¿qué cambiarías en el informe? Escribe el aviso de cobertura.

Cómo saber que está bien: tu informe incluye una limitación y no atribuye causas.

<details><summary>Ejemplo de la parte 2</summary>

```python
def semaforo_efectividad(pct):
    if pct is None:
        return "n/c"
    if pct >= 70:
        return "verde"
    if pct >= 50:
        return "amarillo"
    return "rojo"


print(semaforo_efectividad(63.6), semaforo_efectividad(None))
```

```salida
amarillo n/c
```

</details>

## Después, en los ejercicios

Cada entrega de los casos (C01–C06 en [`03_EJERCICIOS/Casos/`](../../03_EJERCICIOS/Casos/)) y las respuestas de los indicadores deben cerrar con interpretación, recomendación y límites. Siguiente capítulo: [Capítulo 7 — Python básico](../07_Python_basico.md) (o, en el orden del plan, [Capítulo 5 — Calidad de datos y ETL](../05_calidad_ETL.md)).
