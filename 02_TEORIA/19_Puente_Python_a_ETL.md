# Puente: de funciones sueltas a un programa que puedes defender

Hasta ahora escribiste funciones pequeñas que un corrector probaba. Un ETL es lo mismo en grande: varias funciones pequeñas, en orden, con un cuadre al final. Este capítulo muestra lo que cambia, con ejemplos que puedes ejecutar. Úsalo junto a ME01–ME04 y DB01–DB03. Las secciones 1 y 2 sirven desde la semana 2; la 3 y la 4, desde que empieces el mini-ETL.

## 1. Leer un error en lugar de temerle

Un error no es un fracaso: es la computadora diciéndote dónde dejó de entender. Lee en este orden: primero la **última línea** (tipo de error y mensaje), después la **línea de tu archivo** que aparece justo encima.

```text
Traceback (most recent call last):
  File "s1.py", line 8, in <module>
    print(total_por_tienda(ventas))
  File "s1.py", line 4, in total_por_tienda
    totales[fila["tienda"]] = totales.get(fila["tienda"], 0) + fila["monto"]
KeyError: 'monto'
```

La última línea dice que se pidió la clave `'monto'` y no existe. La línea 4 dice dónde. La pregunta que sigue es qué fila no tiene `monto`. Imprime esa fila (`print(fila)`) antes de la línea que falla; en este caso es `{'tienda': 'Luna'}`. Con la causa clara, decides: la fila está incompleta (¿rechazarla?) o el nombre de la clave es otro. Regla de oro: **cambia una cosa por vez y vuelve a ejecutar**. Otros tipos que verás: `TypeError` (tipos incompatibles), `ValueError` (valor con formato inválido), `NameError` (nombre sin definir), `PermissionError` (archivo bloqueado, ver §4).

Los errores que no avisan son más peligrosos: el programa termina, pero el total no cuadra. Ahí la herramienta es el **cuadre**: calcula a mano tres filas y compara. DB02 y DB03 practican esto.

## 2. Rechazar con ValueError y dejar rastro

Convertir un dato inválido en cero o truncarlo cambia las ventas sin avisar. La alternativa es rechazarlo con una causa legible. `try/except` captura el error esperado; `raise ValueError(...)` lo convierte en un mensaje tuyo.

```python
def descuento_valido(texto):
    try:
        valor = float(texto.replace(",", "."))
    except ValueError:
        raise ValueError(f"descuento no numérico: {texto!r}")
    if not 0 <= valor <= 100:
        raise ValueError(f"descuento fuera de 0–100: {valor}")
    return valor

assert descuento_valido("12,5") == 12.5
for malo in ["abc", "150"]:
    try:
        descuento_valido(malo)
    except ValueError as error:
        print("rechazado ->", error)
```

Salida:

```text
rechazado -> descuento no numérico: 'abc'
rechazado -> descuento fuera de 0–100: 150.0
```

Fíjate en tres decisiones: la función valida y devuelve un valor (no imprime); el mensaje dice qué pasó y con qué dato; quien la llama decide si rechaza la fila o detiene todo. En P09, P10 y P11 aplicas esta forma a precios, fechas y cantidades.

## 3. De funciones a un programa: extraer, transformar, validar, cargar

Un ETL pequeño cabe en cuatro funciones. El ejemplo usa cuatro filas en memoria para ver la idea sin archivos. Observa el **orden** (extraer → transformar → validar), la **copia** que protege el original (Bronze) y la **ecuación de cuadre** al final.

```python
FILAS = [
    {"ticket": "T1", "tienda": " sol ", "unidades": "3", "precio": "Bs 10,50", "estado": "entregado"},
    {"ticket": "T2", "tienda": "LUNA", "unidades": "2.5", "precio": "8.00", "estado": "entregado"},
    {"ticket": "T3", "tienda": "sol", "unidades": "4.0", "precio": "5,25", "estado": "anulado"},
    {"ticket": "T1", "tienda": " sol ", "unidades": "3", "precio": "Bs 10,50", "estado": "entregado"},
]

def extraer():
    return [dict(f) for f in FILAS]                      # Bronze: copia sin tocar

def transformar(raw):
    vistos, silver, rechazos = set(), [], []
    for fila in raw:
        clave = tuple(sorted(fila.items()))
        if clave in vistos:
            continue                                      # duplicado exacto
        vistos.add(clave)
        try:
            x = float(fila["unidades"])
            if x != int(x) or x <= 0:
                raise ValueError("unidades")
            precio = round(float(fila["precio"].replace("Bs", "").replace(",", ".")) * 100)
        except ValueError as error:
            rechazos.append({**fila, "motivo": str(error)})
            continue
        silver.append({"ticket": fila["ticket"], "tienda": fila["tienda"].strip().title(),
                       "unidades": int(x), "precio_centavos": precio, "estado": fila["estado"]})
    return silver, rechazos

def validar(n_raw, n_duplicados, n_rechazos, n_silver):
    if n_raw != n_duplicados + n_rechazos + n_silver:
        raise ValueError("no cuadra")
    return True

raw = extraer()
silver, rechazos = transformar(raw)
duplicados = len(raw) - len({tuple(sorted(f.items())) for f in raw})
print("raw:", len(raw), "· duplicados:", duplicados, "· rechazos:", len(rechazos), "· silver:", len(silver))
print("cuadra:", validar(len(raw), duplicados, len(rechazos), len(silver)))
```

Salida:

```text
raw: 4 · duplicados: 1 · rechazos: 1 · silver: 2
cuadra: True
```

Cuatro filas: una duplicada exacta, una rechazada por tener 2.5 unidades y dos válidas. 4 = 1 + 1 + 2. Ese cuadre es el que protege tu trabajo con 16.000 filas: si no cuadra, perdiste o inventaste filas.

Este ejemplo es una versión simplificada (sin Pandas, sin fecha ni catálogo, con `float` en vez de `Decimal`). En ME02 trabajarás con las reglas completas y en ME03 con la carga a SQLite. Para el ETL de la distribuidora y el caso final, la estructura es la misma; solo cambian las reglas.

## 4. Cargar a SQLite en Windows: cierra la conexión

Publicar un resultado seguro significa escribirlo primero en un archivo temporal y reemplazar el destino solo si todo cuadra. Hay una trampa específica: `with sqlite3.connect(...) as con:` **confirma** la transacción pero **no cierra** la conexión. En Windows, un archivo abierto no se puede reemplazar ni borrar y obtienes `PermissionError: [WinError 32]`. En Linux el mismo código funciona, por eso el error parece misterioso. La solución es `contextlib.closing`:

```python
from contextlib import closing
from pathlib import Path
import os
import sqlite3
import tempfile

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as carpeta:
    temporal = Path(carpeta) / "salida.tmp.db"
    destino = Path(carpeta) / "salida.db"
    with closing(sqlite3.connect(temporal)) as con:          # closing() cierra la conexión al salir
        with con:                                            # y `with con` confirma la transacción
            con.execute("CREATE TABLE ventas (ticket TEXT, monto INTEGER)")
            con.execute("INSERT INTO ventas VALUES ('T1', 3150)")
    os.replace(temporal, destino)                            # ahora sí se puede reemplazar en Windows
    with closing(sqlite3.connect(destino)) as con:
        print("filas publicadas:", con.execute("SELECT COUNT(*) FROM ventas").fetchone()[0])
```

Salida: `filas publicadas: 1`. Regla práctica: **toda conexión SQLite va dentro de `closing(...)`**, incluso para leer. `herramientas/prueba_sqlite_cierre.py` comprueba que las herramientas del paquete cumplen esta regla; ejecútalo en tu máquina si dudas.

## 5. Mapa de práctica

| Ejercicio | Qué entrena | Cuándo |
|---|---|---|
| DB01 | Leer un traceback | Antes del mini-ETL |
| ME01 | Extraer como texto, quitar exactos, perfilar | Mini-ETL, parte 1 |
| ME02 | Reglas de transformación y rechazos con causa | Mini-ETL, parte 2 |
| ME03 | Cuadre, carga repetible, conexión cerrada, errores de estructura | Mini-ETL, parte 3 |
| DB02, DB03 | Errores silenciosos: truncar y duplicar con un JOIN | Refuerzo antes del ETL grande |
| ME04 | Modificar un ETL existente con una regla nueva | Antes del caso de transferencia |

Después viene el ETL de la distribuidora (guiado) y el caso de transferencia (C06, sin plantilla). La puerta para avanzar a cada uno está en `01_PLAN_DIARIO/COMPETENCIAS.md`. Fuente: tutorial oficial de Python (errores y excepciones), documentación de `contextlib` y de `sqlite3`.
