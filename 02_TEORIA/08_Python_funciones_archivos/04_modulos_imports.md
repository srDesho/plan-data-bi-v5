# 8.4 Módulos e importaciones

> Tiempo estimado: 55 min (lectura 22 + práctica 33). Prerrequisitos: [8.1 Funciones con contrato](01_funciones_con_contrato.md) y [8.3 Archivos](03_archivos_csv_json.md).

## Para qué sirve

No escribes todo desde cero: Python trae decenas de herramientas listas (matemáticas, fechas, archivos, SQLite), y los proyectos reales dividen su propio código en varios archivos. Un **módulo** es un archivo de Python que otro programa puede **importar**. Es la forma de reutilizar funciones sin copiarlas y la base para organizar un ETL en piezas (leer, transformar, validar, cargar).

## Términos nuevos

- **Módulo**: un archivo `.py` con definiciones (funciones, constantes) que se puede importar desde otro.
- **Importar** (`import`): hacer disponible el contenido de un módulo en tu programa.
- **Biblioteca estándar**: los módulos que vienen con Python sin instalar nada: `math`, `datetime`, `csv`, `json`, `pathlib`, `sqlite3`, `statistics`...
- **Paquete externo**: una biblioteca que no viene con Python y se instala aparte (`pandas`, `numpy`, `scipy`). En este curso se instalan en el entorno `.venv` desde `requirements.txt`.
- **`from modulo import nombre`**: importar solo una pieza para usarla sin el prefijo del módulo.
- **Alias de importación**: un nombre corto al importar: `import pandas as pd`.
- **`__name__`**: una variable especial. Vale `"__main__"` cuando el archivo se ejecuta directamente y el nombre del módulo cuando se importa.

## Ejemplo paso a paso

**1. Importar y usar un módulo estándar.**

```python
import math

print(math.sqrt(144))
print(math.ceil(2.1))
print(math.floor(2.9))
print(math.pi)
```

```salida
12.0
3
2
3.141592653589793
```

`import math` trae el módulo; sus funciones se usan con el prefijo `math.`. `ceil` redondea hacia arriba (cajas necesarias para guardar 25 unidades si caben 12 por caja: `math.ceil(25 / 12)`) y `floor` hacia abajo.

**2. `from ... import`.**

```python
from statistics import mean, median

ventas = [120, 80, 200, 150]
print(mean(ventas))
print(median(ventas))
```

```salida
137.5
135.0
```

Así importas solo `mean` y `median` y las usas sin prefijo. Úsalo para pocas funciones; con muchas, `import modulo` deja claro de dónde viene cada una.

**3. Fechas con `datetime`.** En un ETL las fechas llegan como texto `"2026-09-18"`; el módulo `datetime` las convierte en objetos con los que sí se puede calcular:

```python
from datetime import date, timedelta

hoy_corte = date.fromisoformat("2026-09-30")
ultima_compra = date.fromisoformat("2026-09-02")

print((hoy_corte - ultima_compra).days)
print(ultima_compra + timedelta(days=7))
print(ultima_compra.year, ultima_compra.month, ultima_compra.day)
print(ultima_compra < hoy_corte)
```

```salida
28
2026-09-09
2026 9 2
True
```

`date.fromisoformat` lee texto `AAAA-MM-DD`. Restar dos fechas da una duración (`timedelta`), y `.days` son los días de diferencia: 28. Sumar `timedelta(days=7)` mueve la fecha. Es el equivalente de `julianday` en SQL. Si el texto no tiene un formato válido, falla con `ValueError`:

```python
from datetime import date

print(date.fromisoformat("18/09/2026"))
```

```error
ValueError: Invalid isoformat string: '18/09/2026'
```

Para otros formatos se usa `datetime.strptime(texto, "%d/%m/%Y")`, que dice cómo está escrita la fecha.

```python
from datetime import datetime

d = datetime.strptime("18/09/2026", "%d/%m/%Y").date()
print(d)
print(d.strftime("%Y-%m"))
```

```salida
2026-09-18
2026-09
```

`strptime` (*parse*) convierte texto en fecha según el formato; `strftime` (*format*) convierte una fecha en texto. Los códigos son los mismos que viste en SQL (`%Y`, `%m`, `%d`).

**3b. Fechas ISO como texto: se comparan bien.** Una fecha escrita `AAAA-MM-DD` ordena igual como texto que como calendario, así que puedes comparar o filtrar sin convertir (siempre que **todas** estén en ese formato):

```python
inicio, fin = "2026-09-01", "2026-09-30"
for fecha in ["2026-08-31", "2026-09-15", "2026-10-01"]:
    print(fecha, inicio <= fecha <= fin)
```

```salida
2026-08-31 False
2026-09-15 True
2026-10-01 False
```

Con `DD/MM/AAAA` esto **no** funciona (`"15/09/2026"` se ordena por el día). Con formatos mezclados, convierte primero con `strptime`.

**4. Crear y usar tu propio módulo.** Un archivo `utilidades.py` con funciones, y otro programa que lo importa. Aquí lo simulamos en una carpeta temporal:

```python
from pathlib import Path

Path("utilidades.py").write_text(
    "def limpiar(texto):\n"
    "    return texto.strip().upper()\n"
    "\n"
    "IVA = 13\n",
    encoding="utf-8",
)

import utilidades

print(utilidades.limpiar("  r01 "))
print(utilidades.IVA)
```

```salida
R01
13
```

Todo archivo `.py` en la misma carpeta del programa se puede importar con `import nombre_sin_extension`. Python busca en la carpeta actual y en las carpetas de la lista `sys.path`. Si ves `ModuleNotFoundError: No module named 'utilidades'`, el archivo no está donde Python lo busca o escribiste mal el nombre.

```python
import modulo_que_no_existe
```

```error
ModuleNotFoundError: No module named 'modulo_que_no_existe'
```

**5. `if __name__ == "__main__":`.** Cuando importas un módulo, Python **ejecuta todo su código**. Si el módulo imprime o procesa datos al nivel principal, esas acciones ocurren al importar, lo cual casi nunca es lo que quieres. La solución es esta guarda:

```py
# utilidades.py
def limpiar(texto):
    return texto.strip().upper()


def main():
    print(limpiar("  prueba "))


if __name__ == "__main__":
    main()
```

- Si ejecutas `python utilidades.py`, `__name__` vale `"__main__"` y se ejecuta `main()`.
- Si otro archivo hace `import utilidades`, `__name__` vale `"utilidades"` y `main()` **no** se ejecuta; solo quedan disponibles las funciones.

Así el mismo archivo sirve como programa y como biblioteca. Los ETL del curso siguen este esquema.

**6. Paquetes externos y versiones.** `pandas` y `numpy` no vienen con Python; están en el entorno `.venv` del curso. Se importan igual (`import pandas as pd`). Para saber qué versiones tienes, `pip list` (con el Python del `.venv`) o el archivo `requirements.txt`. Anota las versiones en tu documentación: un resultado puede cambiar entre versiones.

```text
.venv\Scripts\python.exe -m pip list
```

Ejemplo comercial: un proyecto con `leer.py` (extracción), `limpiar.py` (transformación), `validar.py` y `main.py` que los importa y los ejecuta en orden. Si falla la limpieza, abres solo `limpiar.py`.

## Errores comunes

- **`ModuleNotFoundError`** por nombre mal escrito o archivo en otra carpeta.
- **Nombrar tu archivo igual que un módulo estándar** (`csv.py`, `math.py`): Python importa el tuyo y todo falla de formas raras.
- **Ejecutar el programa desde otra carpeta** y no encontrar tus módulos.
- **Poner código que se ejecuta al importar** (sin la guarda `__main__`).
- **`from modulo import *`**: mezcla nombres y es difícil de seguir.
- **Instalar paquetes en el Python global** en lugar del `.venv`.
- **No anotar las versiones** de los paquetes usados.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre `import math` y `from math import sqrt`?
2. ¿Qué devuelve `date.fromisoformat("2026-09-30") - date.fromisoformat("2026-09-20")`?
3. ¿Para qué sirve `if __name__ == "__main__":`?
4. ¿Por qué no debes llamar `csv.py` a tu archivo?

<details><summary>Respuestas</summary>

1. El primero trae el módulo (se usa `math.sqrt`); el segundo trae solo `sqrt` (se usa `sqrt`).
2. Una duración de 10 días (`timedelta`); `.days` da 10.
3. Para que el código de `main()` solo se ejecute al correr el archivo directamente, no al importarlo.
4. Porque Python importaría tu archivo en lugar del módulo estándar `csv`.

</details>

## Micropráctica

1. Calcula cuántos días hay entre `2026-08-03` y `2026-09-30` con `datetime`.
2. Convierte el texto `"05/09/2026"` (día/mes/año) en una fecha ISO `2026-09-05`.
3. Crea un módulo `mis_utilidades.py` con una función `limpiar_codigo` y úsalo desde otro archivo (hazlo en `mi_trabajo`).
4. Calcula con `math.ceil` cuántas cajas de 24 unidades se necesitan para 130 unidades.

Cómo saber que está bien: 1 → 58; 2 → `2026-09-05`; 4 → 6.

<details><summary>Comprobación de las partes 1, 2 y 4</summary>

```python
import math
from datetime import date, datetime

print((date.fromisoformat("2026-09-30") - date.fromisoformat("2026-08-03")).days)
print(datetime.strptime("05/09/2026", "%d/%m/%Y").date().isoformat())
print(math.ceil(130 / 24))
```

```salida
58
2026-09-05
6
```

</details>

## Después, en los ejercicios

Las fechas de P10 y P12 en [Python](../../03_EJERCICIOS/Python/) se resuelven con `datetime`; revisa qué formato de fecha pide cada enunciado. El esqueleto de varios módulos es el del mini-ETL y el ETL final. Siguiente: [8.5 Excepciones: try, except y raise](05_excepciones.md).
