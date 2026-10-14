# 14.5 Diseño del tablero y lista de comprobación manual

> Tiempo estimado: 45 min (lectura 25 + práctica 20). Prerrequisitos: [14.4 Medidas útiles](04_medidas_utiles.md) y [6.6 Interpretar y recomendar](../06_KPIs/06_interpretar_y_recomendar.md).
>
> **Estado de verificación:** esta lección es de criterio de diseño y de comprobación manual. El paquete **no contiene un `.pbix` construido ni medidas declaradas como ejecutadas**: construir el tablero en Power BI Desktop y probarlo es tu trabajo.

## Para qué sirve

Un tablero útil responde decisiones, no muestra todo lo que se pueda graficar. Esta lección te da la estructura de un tablero comercial laboral, las reglas de diseño que lo hacen legible y la **lista de comprobación manual** que debes pasar antes de entregarlo, porque ninguna parte de la interfaz de Power BI se prueba automáticamente en este paquete.

## Términos nuevos

- **Página de informe**: una pantalla del tablero con un propósito (comercial, operativa).
- **Tarjeta**: un visual que muestra un solo número (ventas, pedidos).
- **Título descriptivo**: un título que dice **qué se ve, en qué unidad y para qué período**: «Ventas entregadas por ruta, septiembre 2026 (Bs)».
- **Jerarquía visual**: el orden de importancia en que se lee la página (lo principal arriba a la izquierda).
- **Interacción entre visuales**: que seleccionar un elemento en un visual filtre los demás.
- **Lista de comprobación manual**: los pasos que una persona ejecuta en Desktop y marca como hechos.
- **Hallazgo**: una conclusión con cifra que el tablero debe poder mostrar de un vistazo.

## Ejemplo paso a paso

**1. Estructura sugerida (dos páginas).**

| Página | Tarjetas | Visuales | Pregunta que responde |
|---|---|---|---|
| **Comercial** | Ventas entregadas, Pedidos, Ticket | línea por fecha; barras por ruta; tabla mes × ruta con ventas, meta y cumplimiento | ¿cuánto vendimos y cómo vamos contra la meta? |
| **Operativa** | Cobertura de ejecución, Efectividad, Clientes inactivos | barras de visitas por ruta; lista de clientes inactivos | ¿cómo está la ejecución y a quién visitar? |

Segmentadores comunes a las dos páginas: mes y ruta.

**2. Reglas de diseño.**

1. **Un título por visual** que diga qué mide, la unidad y el período. «Ventas» no es un título; «Ventas entregadas por ruta (Bs), sept. 2026» sí.
2. **Los números principales arriba**, los detalles abajo. Máximo 5 a 7 visuales por página.
3. **Colores consistentes**: la misma ruta con el mismo color en todos los visuales.
4. **Ejes que empiezan en cero** en barras (si no, exageras las diferencias).
5. **Una escala de rojo/amarillo/verde solo si los umbrales están definidos** (lección 6.6).
6. **Sin gráficos de adorno**: cada visual debe servir a una decisión.
7. **Dos o tres hallazgos** escritos en un cuadro de texto («R03 cumplió 53,3 % de su meta de septiembre»).

**3. Un tablero que se puede defender.** Las cifras del tablero deben poder explicarse:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
fact["mes"] = fact["fecha"].str[:7]
fact["importe"] = fact["cantidad"] * fact["precio_unitario"]
sep = fact[(fact["estado"] == "entregado") & (fact["mes"] == "2026-09")]

tabla = sep.groupby("ruta", as_index=False)["importe"].sum().merge(
    metas[metas["mes"] == "2026-09"][["ruta", "meta_bs"]], on="ruta", validate="1:1")
tabla["cumplimiento_pct"] = (tabla["importe"] / tabla["meta_bs"] * 100).round(1)
tabla["brecha_bs"] = tabla["meta_bs"] - tabla["importe"]
print(tabla)
print(round(tabla["importe"].sum()), round(tabla["importe"].sum() / tabla["meta_bs"].sum() * 100, 1))
```

```salida
  ruta  importe  meta_bs  cumplimiento_pct  brecha_bs
0  R01    800.0    600.0             133.3     -200.0
1  R02    379.0    450.0              84.2       71.0
2  R03    160.0    300.0              53.3      140.0
1339 99.2
```

Esa tabla es exactamente la «tabla mes × ruta con presupuesto y cumplimiento» de la página comercial, para septiembre. Los tres hallazgos del recuadro de texto salen de ella: R01 superó la meta (133,3 %), R03 es la de mayor brecha (140 Bs), y el total del mes alcanza el 99,2 %.

**4. La lista de comprobación manual** (marca cada paso en tu equipo):

| # | Qué comprobar | Cómo | ¿Hecho? |
|---|---|---|---|
| 1 | Importación | cada CSV carga con los tipos correctos; filas = 39 en el hecho, 12 tiendas, 10 artículos | ☐ |
| 2 | Cultura | los importes en centavos son enteros; las fechas son Fecha | ☐ |
| 3 | Claves | claves únicas en las dimensiones (columna → «Distintos» = «Total») | ☐ |
| 4 | Relaciones | todas 1:*; filtro en un sentido; sin ambigüedades; sin relaciones automáticas no revisadas | ☐ |
| 5 | Tabla de fechas | marcada como tabla de fechas; sin huecos | ☐ |
| 6 | Medidas | cada una en una tarjeta sin filtros = valor de control | ☐ |
| 7 | Segmentadores | ruta y mes filtran ventas, metas y visitas | ☐ |
| 8 | Un cruce | una ruta y una categoría contra SQL | ☐ |
| 9 | Títulos | cada visual con unidad y período | ☐ |
| 10 | Actualización | reemplazar el CSV por una versión modificada y actualizar: las cifras cambian como se espera | ☐ |
| 11 | Privacidad | el archivo no contiene datos privados ni credenciales | ☐ |

**5. Si algo no cuadra.** Orden de diagnóstico:

1. Si el **total** cuadra y una **ruta** no: revisa relaciones y el campo del segmentador (¿usa `dim_ruta` o la ruta de otra tabla?).
2. Si **todo se multiplica**: una dimensión tiene claves repetidas.
3. Si un total es **menor**: filas huérfanas o un filtro de estado de más.
4. Si aparece **«(en blanco)»** en un visual: claves del hecho sin pareja en la dimensión.

**6. Cómo comunicar el tablero.** Al presentarlo, tres frases: *qué muestra*, *qué hallazgo destaca* y *qué limitación tiene*. Ejemplo: «Muestra ventas entregadas y cumplimiento por ruta de agosto y septiembre. El hallazgo principal es que R03 quedó en 53,3 % de su meta de septiembre. Los datos son inventados y no incluyen descuentos ni devoluciones.» Sin la tercera frase, el tablero parece más seguro de lo que es.

**7. Lo que no entra en este curso.** Seguridad por filas, publicación en el servicio de Power BI, actualización programada con puerta de enlace y modelos compuestos quedan fuera: son temas de un siguiente nivel y requieren una cuenta de organización.

Ejemplo comercial: el gerente abre el tablero el lunes. En treinta segundos debe saber si el mes va bien (tarjetas), dónde está el problema (barras por ruta) y a quién visitar (lista de inactivos). Si necesita más de un minuto para entender el título de un gráfico, el diseño falló.

## Errores comunes

- **Un tablero sin pregunta** (muchos gráficos, ninguna decisión).
- **Títulos genéricos** sin unidad ni período.
- **Ejes truncados** que exageran.
- **Colores distintos para la misma ruta** en cada gráfico.
- **No comprobar cifras** contra SQL o Excel.
- **No probar la actualización** con datos modificados.
- **Entregar sin escribir las limitaciones.**
- **Declarar «probado» algo que no se ejecutó.**

## Para comprobar que entendiste

1. ¿Qué debe decir el título de un visual?
2. ¿Qué haces si el total cuadra pero una ruta no?
3. ¿Por qué se prueba la actualización con un CSV modificado?
4. ¿Por qué hay una lista de comprobación manual?

<details><summary>Respuestas</summary>

1. Qué se mide, en qué unidad y para qué período.
2. Reviso las relaciones y el campo que usa el segmentador de ruta.
3. Para confirmar que el informe recalcula como se espera cuando cambian los datos.
4. Porque la interfaz de Power BI no se prueba automáticamente en este paquete.

</details>

## Micropráctica

1. Dibuja a mano una página «Operativa» con tres tarjetas y dos visuales; escribe los títulos completos.
2. Redacta tres hallazgos para el cuadro de texto usando los valores de la tabla del paso 3.
3. Completa la lista de comprobación del paso 4 para tu propio `.pbix` (cuando lo tengas) y anota los pasos que no puedas hacer todavía.

Cómo saber que está bien: cada hallazgo menciona una cifra y una ruta; la lista marca solo lo que realmente comprobaste.

<details><summary>Comprobación de las cifras del paso 3 para agosto</summary>

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
tiendas = pd.read_csv("04_DATASETS/mini_base/tiendas.csv")
metas = pd.read_csv("04_DATASETS/mini_base/metas.csv")

fact = lineas.merge(ventas, on="venta_id", validate="m:1").merge(tiendas[["tienda_id", "ruta"]], on="tienda_id", validate="m:1")
ago = fact[(fact["estado"] == "entregado") & (fact["fecha"].str.startswith("2026-08"))]
t = ago.groupby("ruta", as_index=False)["cantidad"].sum()
print(t.values.tolist())
```

```salida
[['R01', 67], ['R02', 19], ['R03', 51]]
```

</details>

## Después, en los ejercicios

El proyecto de Power BI ([`05_PROYECTOS/powerbi/`](../../05_PROYECTOS/)) trae `MODELO.md`, los CSV del modelo, el código M y el DAX de referencia, y una lista manual de verificación (`VALIDACION_MANUAL.md`). Completa la lista y registra qué pasos pudiste ejecutar. Siguiente capítulo: [Capítulo 15 — Excel](../15_Excel_cuadres.md).
