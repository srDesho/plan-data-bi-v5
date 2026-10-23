# 14.1 Power BI desde cero: qué es, el flujo de trabajo y la configuración regional

> Tiempo estimado: 54 min (lectura 34 + práctica 20). Prerrequisitos: [13.2 El modelo estrella](../13_Modelado/02_modelo_estrella.md) y [9.2 Leer un CSV](../09_Pandas_basico/02_series_dataframe_csv.md).
>
> **Estado de verificación de este capítulo:** las cifras de control se calculan con Python sobre la mini-base y se comprueban automáticamente. Los pasos de la interfaz de Power BI Desktop, el código M y el código DAX **no se ejecutaron en Power BI Desktop** al escribir este material: son guía de referencia que tú debes probar en tu equipo (hay una lista de comprobación manual al final del capítulo). Los nombres de menús pueden variar según la versión.

<!-- TEORIA:PREPARACION:INICIO -->
<a id="preparacion-pb02"></a>

## Base inicial de tabla de fechas · 4 min

Lee esta base antes de realizar PB02 en Desktop. Sus 4 minutos forman parte de la lectura de esta lección. La tabla `dim_fecha` ya está incluida entre los CSV del modelo; aquí aprendes a reconocerla como calendario del modelo.

1. Selecciona `dim_fecha` y comprueba que su columna `fecha` tiene tipo **Fecha**. La tabla debe tener una fila por día, fechas únicas y ningún vacío.
2. Comprueba que cubre todos los días entre la primera y la última fecha: ordenar las fechas no basta si falta un día intermedio. Contrasta el número de filas con el número de días de ese intervalo, incluidos ambos extremos, y verifica también duplicados y vacíos.
3. Con `dim_fecha` seleccionada, busca **Marcar como tabla de fechas** entre las opciones de tabla o modelado; activa la opción, elige `fecha` como columna y confirma. El nombre y la ubicación del menú pueden variar según la versión de Desktop. Si la validación rechaza el calendario, revisa tipo, vacíos, duplicados y continuidad antes de continuar.
4. Comprueba que la marca quedó aplicada y que las relaciones usan la fecha y dirección indicadas en [MODELO.md](../../05_PROYECTOS/powerbi/MODELO.md). Conserva una captura o una nota de esas comprobaciones como evidencia de PB02.

Esta preparación explica el procedimiento; la evidencia se obtiene al ejecutarlo en Desktop dentro de la práctica.

El encabezado de esta lección incluye esta sección de 4 min. Si ya la estudiaste antes, quedan 30 min de lectura del desarrollo; no vuelvas a sumar esta sección. La práctica de 20 min se contabiliza por separado según la guía.
<!-- TEORIA:PREPARACION:FIN -->

<a id="desarrollo"></a>

## Para qué sirve

Power BI es la herramienta con la que muchas empresas muestran sus indicadores a gerencia. Un analista junior no necesita dominarla toda: necesita cargar datos limpios, conectar las tablas con relaciones correctas, escribir unas pocas medidas y construir un tablero con títulos claros. Lo más importante es saber **comprobar** que las cifras del tablero son las del SQL y las del Excel, porque un tablero bonito con una cifra equivocada hace más daño que ninguno.

## Términos nuevos

- **Power BI Desktop**: el programa gratuito de Windows donde se construye el informe.
- **Informe**: el archivo con las páginas de visualizaciones (`.pbix`).
- **Conjunto de datos** (*semantic model* o modelo): las tablas, relaciones y medidas que alimentan el informe.
- **Visual**: un gráfico, tarjeta, tabla o segmentador de una página.
- **Segmentador** (*slicer*): un control que filtra todo el informe (por ejemplo, ruta o mes).
- **Power Query**: la herramienta de Power BI para obtener y transformar datos. Cada transformación queda como un **paso aplicado**.
- **Lenguaje M**: el lenguaje que escribe Power Query detrás de cada paso.
- **DAX** (*Data Analysis Expressions*): el lenguaje de fórmulas para crear **medidas** y columnas calculadas en el modelo.
- **Configuración regional** (o cultura): las reglas del idioma/país para separador decimal, de miles y de lista, y formato de fecha.
- **Actualizar**: volver a ejecutar los pasos de Power Query con los datos actuales de la fuente.

## El flujo de trabajo, en cuatro etapas

```text
1. OBTENER   →  2. TRANSFORMAR  →  3. MODELAR        →  4. VISUALIZAR
 (CSV, BD)      (Power Query)       (relaciones + DAX)    (visuales, tablero)
```

1. **Obtener datos**: *Inicio → Obtener datos → Texto/CSV* (o SQLite mediante un conector/ODBC si lo tienes instalado). Se previsualiza el contenido.
2. **Transformar**: *Transformar datos* abre Power Query: tipos de columna, filtros, renombrar, combinar. Nada cambia el archivo original.
3. **Modelar**: en la vista *Modelo*, crear relaciones (1:*) y marcar la tabla de fechas; crear medidas con DAX.
4. **Visualizar**: en la vista *Informe*, arrastrar campos a los visuales.

**Principio de trabajo:** lo que se puede arreglar en el origen o en el ETL (Python/SQL) se arregla **ahí**; Power BI recibe tablas ya limpias y con claves únicas. Power Query sirve para ajustes finales, no para reemplazar el ETL.

## Ejemplo paso a paso

**1. Qué datos le entregas a Power BI.** El exportador del proyecto genera una carpeta de CSV: las dimensiones, los hechos y el calendario (lección 13.2), con **dinero en centavos enteros** y fechas ISO. Con la mini-base, así se vería el paquete de entrada:

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
ventas = pd.read_csv("04_DATASETS/mini_base/ventas.csv")

fact = lineas.merge(ventas, on="venta_id", validate="m:1")
fact["monto_centavos"] = (fact["cantidad"] * fact["precio_unitario"] * 100).round().astype(int)
fact = fact[["linea_id", "venta_id", "tienda_id", "articulo_id", "fecha", "estado", "cantidad", "monto_centavos"]]

print(fact.dtypes.to_dict())
print(len(fact), fact["monto_centavos"].sum())
print(fact.loc[fact["estado"] == "entregado", "monto_centavos"].sum() / 100)
```

```salida
{'linea_id': dtype('int64'), 'venta_id': dtype('int64'), 'tienda_id': dtype('int64'), 'articulo_id': dtype('int64'), 'fecha': dtype('O'), 'estado': dtype('O'), 'cantidad': dtype('int64'), 'monto_centavos': dtype('int64')}
39 272150
2332.5
```

Estas tres cifras son las **de control** para el tablero: 39 filas en el hecho; 272 150 centavos en total; y 2 332,5 Bs de ventas entregadas. Cuando cargues el CSV en Power BI, la suma de `monto_centavos` y el conteo de filas deben dar lo mismo.

**2. Por qué centavos enteros.** Si el CSV trae `6.5` y tu Windows interpreta la coma como decimal y el punto como separador de miles, Power BI puede leer `6.5` como el texto «6.5» o como el entero 65. Los **enteros** no tienen separador decimal y por eso viajan sin ambigüedad. Se divide entre 100 al mostrar.

**3. El problema regional, con un ejemplo que puedes reproducir.** Un mismo texto leído con dos reglas:

```python
import io
import pandas as pd

texto = "producto;precio\nAgua;6,5\nJugo;1.250,50\n"

mal = pd.read_csv(io.StringIO(texto), sep=";")
bien = pd.read_csv(io.StringIO(texto), sep=";", decimal=",", thousands=".")

print(mal["precio"].tolist())
print(bien["precio"].tolist())
print(mal["precio"].dtype, bien["precio"].dtype)
```

```salida
['6,5', '1.250,50']
[6.5, 1250.5]
object float64
```

Sin indicar las reglas, la columna queda como **texto** (`'6,5'`, `'1.250,50'`) y no se puede sumar. Indicando decimal con coma y miles con punto, se lee como números: 6,5 y 1250,5. En Power BI el equivalente es elegir la **configuración regional** correcta al cambiar el tipo de columna («Usando configuración regional…» → Español (Bolivia) o la que corresponda). No asumas que tu equipo y el archivo hablan el mismo idioma numérico.

**4. Qué cambia con el idioma de Windows.**

| Aspecto | Windows en español (Bolivia/España) típico | Archivo exportado «en inglés» |
|---|---|---|
| decimal | coma (`6,5`) | punto (`6.5`) |
| miles | punto (`1.250`) o espacio | coma (`1,250`) |
| separador de lista (funciones, CSV de Excel) | `;` | `,` |
| fechas | `dd/mm/aaaa` | `aaaa-mm-dd` o `mm/dd/aaaa` |

La combinación más peligrosa: un `.` de miles leído como decimal, que convierte 1.250 en 1,25. **Verifica la suma contra una cifra conocida inmediatamente después de cargar.** Las configuraciones concretas de tu equipo las confirmas tú: este material no las puede asumir.

**5. Buenas prácticas de la carga.**

1. Importa cada tabla como una consulta con nombre claro (`fact_ventas`, `dim_tienda`).
2. Establece el tipo de cada columna **explícitamente** (no aceptes el que Power BI infiere sin mirar).
3. Las claves y los códigos con ceros iniciales, como **texto**.
4. Las fechas como tipo **Fecha**.
5. Después de cargar, compara filas y suma de importes con las cifras de control.
6. Desactiva «Cargar» en las consultas auxiliares que no necesitas en el modelo.

**6. Qué NO hace Power BI por ti.** No arregla relaciones mal pensadas, no detecta que sumaste una meta repetida y no sabe cuál es tu definición de «venta». Un tablero correcto empieza en el modelo (capítulo 13), no en los gráficos.

Ejemplo comercial: el tablero muestra Bs 2 332,5 de ventas entregadas, igual que el SQL y que Excel. Esa coincidencia entre tres herramientas es la prueba de que el modelo, las relaciones y las medidas están bien.

## Errores comunes

- **No fijar la configuración regional** al convertir números y fechas.
- **Aceptar los tipos inferidos** sin revisarlos.
- **Cargar sin comparar con una cifra conocida.**
- **Hacer en Power Query lo que debía resolver el ETL.**
- **Confiar en las relaciones detectadas automáticamente.**
- **Decimales en el CSV** sin considerar el idioma de Windows (se evitan con centavos enteros).
- **Afirmar que un tablero está validado sin haber probado la actualización.**

## Para comprobar que entendiste

1. ¿Cuáles son las cuatro etapas del flujo de trabajo en Power BI?
2. ¿Por qué el dinero viaja en centavos enteros?
3. ¿Qué pasa si no indicas la configuración regional al leer `1.250,50`?
4. ¿Qué cifras de control comparas después de cargar?

<details><summary>Respuestas</summary>

1. Obtener, transformar, modelar y visualizar.
2. Porque los enteros no tienen separador decimal y evitan confusiones de idioma.
3. El valor queda como texto o se interpreta mal (por ejemplo 1,25).
4. El número de filas y la suma de importes del hecho.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Genera con Pandas el CSV del hecho de visitas de la mini-base y anota sus cifras de control (filas y visitas realizadas).
2. Reproduce el problema regional con un archivo de tres filas que tú inventes (con coma decimal) y corrígelo con `decimal=","`.
3. Escribe la lista de pasos que seguirás en Desktop para cargar `fact_ventas` y qué cifras compararás.

Cómo saber que está bien: en la parte 1, las visitas realizadas suman 11.

<details><summary>Comprobación de la parte 1</summary>

```python
import pandas as pd

visitas = pd.read_csv("04_DATASETS/mini_base/visitas.csv")
print(len(visitas), int(visitas["realizada"].sum()))
```

```salida
14 11
```

</details>

## Después, en los ejercicios

Continúa con [14.2 Power Query y el lenguaje M](02_power_query.md). El proyecto de Power BI está en [`05_PROYECTOS/powerbi/`](../../05_PROYECTOS/): sigue su guía y compara tus cifras con las de control.
