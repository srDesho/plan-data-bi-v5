# 15.1 Excel desde cero: datos limpios, tablas y la configuración regional

> Tiempo estimado: 45 min (lectura 25 + práctica 20). Prerrequisitos: [6.1 Qué es un KPI](../06_KPIs/01_que_es_un_kpi.md) y [14.1 Configuración regional](../14_PowerBI_DAX/01_power_bi_desde_cero.md).
>
> **Estado de verificación:** las acciones de interfaz de Excel (menús, tablas dinámicas, formato) **no se ejecutaron automáticamente** en este paquete; son comprobación manual. Las cifras de control sí se calcularon con Python sobre la mini-base.

## Para qué sirve

Excel es el segundo camino con el que se valida un resultado de SQL o Python, y la herramienta con la que se comunica a quien no usa código. Si lo usas bien (datos importados con los tipos correctos, tablas y fórmulas claras) es una comprobación rápida e independiente; si lo usas mal (un CSV abierto a ciegas con coma decimal) conviertes montos en texto y obtienes sumas equivocadas sin ningún mensaje. Aquí aprendes lo mínimo para usarlo como instrumento de cuadre.

## Términos nuevos

- **Libro / hoja / celda**: un archivo de Excel contiene hojas; una hoja es una cuadrícula de celdas, cada una con una dirección (`B3`).
- **Fórmula**: una celda que empieza con `=` y calcula un valor.
- **Referencia relativa / absoluta**: `B2` cambia al copiar la fórmula; `$B$2` queda fija. `$B2` fija solo la columna.
- **Tabla de Excel**: un rango convertido en tabla (Ctrl+T) con nombre, encabezados y referencias estructuradas (`Tabla1[monto]`).
- **Separador de argumentos**: el carácter que separa los argumentos de una función. En Excel en español de muchos equipos es `;`; en otros es `,`.
- **Formato de celda**: cómo se *muestra* un valor (porcentaje, moneda, fecha) sin cambiar el valor que guarda.
- **Importar desde texto/CSV**: la función *Datos → Obtener datos → Desde texto/CSV*, que permite fijar la codificación y el delimitador antes de cargar.
- **Valor frente a formato**: 0,8 con formato de porcentaje se *ve* 80 %; escribir `80` y luego aplicar formato porcentaje mostraría 8 000 %.

## Ejemplo paso a paso

**1. Importar un CSV sin que Excel lo interprete mal.** No hagas doble clic sobre el CSV. Usa *Datos → Obtener datos → Desde archivo → Desde texto/CSV*, y en la ventana previa fija:

- origen del archivo: **UTF-8** (65001),
- delimitador: **coma** (o el que use el archivo),
- configuración regional del archivo si pregunta: la del archivo (punto decimal para los CSV del curso).

Después de cargar, **comprueba**: ¿los montos están alineados a la derecha (números) o a la izquierda (texto)? ¿La suma de la columna coincide con la cifra de control? Con una coma decimal en el sistema y un CSV con punto decimal, Excel lee `6.5` como texto o como una fecha, y la suma falla en silencio.

**2. La cifra de control antes de abrir Excel.**

```python
import pandas as pd

lineas = pd.read_csv("04_DATASETS/mini_base/venta_lineas.csv")
lineas["importe"] = lineas["cantidad"] * lineas["precio_unitario"]
print(len(lineas), lineas["cantidad"].sum(), lineas["importe"].sum())
```

```salida
39 364 2721.5
```

Cuando cargues `venta_lineas.csv` en Excel y agregues una columna `importe` (`=[@cantidad]*[@precio_unitario]`), debes ver 39 filas, suma de `cantidad` 364 y suma de `importe` 2 721,5. **Si no coinciden, el problema es la importación, no la fórmula.**

**3. Valor frente a formato: el cumplimiento.** Ventas reales 80 000 y presupuesto 100 000.

| Celda | Contenido | Resultado visible |
|---|---|---|
| `B2` | 80000 | ventas reales |
| `B3` | 100000 | presupuesto |
| `B4` | `=SI(B3=0;"";B2/B3)` (o con comas) | 0,8 → con formato porcentaje: **80 %** |
| `B5` | `=B2-B3` | −20 000 (desviación absoluta) |
| `B6` | `=SI(B3=0;"";(B2-B3)/B3)` | −0,2 → **−20 %** (desviación relativa) |

El `SI(B3=0;"";…)` evita dividir entre cero: si no hay presupuesto, la celda queda vacía, no en 0 % (lección 6.6). **Nunca escribas `80` y luego pongas formato porcentaje**: Excel multiplica por 100 al mostrar y verías 8 000 %. La regla: se escribe el **valor** (0,8) y el formato lo muestra como %.

```python
real, presupuesto = 80000, 100000
print(real / presupuesto, real - presupuesto, (real - presupuesto) / presupuesto)
```

```salida
0.8 -20000 -0.2
```

**4. Separadores de argumentos: el error «esta fórmula tiene un problema».** Los ejemplos de este material usan `;` como separador de argumentos. Si tu Excel usa la coma, escribe `=SI(B3=0,"",B2/B3)`. Si la fórmula es rechazada, **cambia solo el separador**. Tampoco cambies a la vez el separador decimal y el de argumentos: complican el diagnóstico. Los nombres de función se muestran **en español** en un Excel en español (`SI`, `SUMAR.SI.CONJUNTO`), pero el archivo `.xlsx` guarda los nombres en inglés internamente, así que un libro abre bien en un Excel de otro idioma.

**5. Convertir el rango en tabla y usar referencias estructuradas.** Selecciona los datos y presiona Ctrl+T. La ventaja: la tabla crece sola y las fórmulas usan nombres, no direcciones:

| Sin tabla | Con tabla |
|---|---|
| `=SUMA(C2:C40)` | `=SUMA(Tabla1[importe])` |
| se rompe si añades filas | se actualiza sola |

Dale a la tabla un nombre claro (`tbl_lineas`) en *Diseño de tabla*.

**6. Congelar, filtrar y no tocar el original.** Reglas de higiene: trabaja sobre una **copia** del CSV (nunca guardes encima del original), deja una hoja «Datos» sin cambios y otra «Calculo» con las fórmulas, y anota en una hoja «Notas» de dónde vienen los datos, la fecha de corte y las decisiones (qué se excluyó). Un libro sin notas no se puede auditar.

**7. Cuidado con las conversiones silenciosas de Excel.** Excel puede cambiar datos al abrir un archivo: códigos como `007` pasan a `7`; textos como `1-2` se convierten en fechas; números largos se pasan a notación científica. Para códigos, importa la columna como **texto** (en la ventana de importación o con *Transformar datos*). Después de cualquier importación revisa los códigos con ceros a la izquierda y las columnas de fecha.

Ejemplo comercial: el ERP entrega `drop_por_pedido.csv`. Al importarlo con el punto decimal correcto, la suma de la columna de importe y el conteo de pedidos coinciden con los de SQL. Si la suma sale mucho menor, probablemente algunos montos se importaron como texto.

## Errores comunes

- **Abrir un CSV con doble clic** y dejar que Excel decida.
- **Escribir `80` y luego aplicar formato porcentaje.**
- **Confundir el valor con el formato.**
- **No comprobar la cifra de control** después de importar.
- **Mezclar el separador decimal y el de argumentos.**
- **Pegar encima del archivo original.**
- **Códigos de cliente importados como número.**
- **Libros sin hoja de notas.**

## Para comprobar que entendiste

1. ¿Por qué no se abre un CSV con doble clic?
2. ¿Qué mostraría Excel si escribes `80` y aplicas formato de porcentaje?
3. ¿Qué haces si Excel rechaza una fórmula copiada con comas?
4. ¿Qué cifras comparas después de importar?

<details><summary>Respuestas</summary>

1. Porque Excel decide el delimitador, la codificación y los tipos sin preguntar, y puede leer montos como texto.
2. 8 000 %.
3. Cambio solo el separador de argumentos a `;` (o al que use tu configuración).
4. Número de filas y suma de las columnas numéricas contra las cifras de control.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Importa `ventas.csv` de la mini-base en Excel con el procedimiento de texto/CSV y verifica 16 filas y que `fecha` quedó como fecha.
2. Crea una tabla (`tbl_ventas`) y cuenta cuántas ventas hay con estado `entregado` con una fórmula; el valor debe ser 14.
3. Calcula en una hoja el cumplimiento de una meta con `SI` para evitar la división entre cero.
4. Anota en una hoja de notas las decisiones que tomaste.

Cómo saber que está bien: 16 filas y 14 entregadas; en la 3, 465 de ventas sobre una meta de 450 da 103,3 % y, si pruebas con meta 0, la celda queda vacía en lugar de dar error.

<details><summary>Cifra de control de la parte 2</summary>

```python
import pandas as pd

v = pd.read_csv("04_DATASETS/mini_base/ventas.csv")
print(len(v), int((v["estado"] == "entregado").sum()))
```

```salida
16 14
```

</details>

## Después, en los ejercicios

Los ejercicios EX01–EX03 de [`03_EJERCICIOS/Casos/`](../../03_EJERCICIOS/Casos/) usan Excel como segundo camino de validación. Siguiente: [15.2 Funciones para cuadrar](02_funciones_para_cuadrar.md).
