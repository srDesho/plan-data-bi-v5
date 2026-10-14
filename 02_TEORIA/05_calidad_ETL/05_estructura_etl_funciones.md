# 5.5 Estructura de un ETL: cuatro funciones y un `main` pequeño

> Tiempo estimado: 65 min (lectura 25 + práctica 40). Prerrequisitos: lecciones 5.1 a 5.4, [8.1 Funciones con contrato](../08_Python_funciones_archivos/01_funciones_con_contrato.md) y [8.4 Módulos](../08_Python_funciones_archivos/04_modulos_imports.md).

## Para qué sirve

Un ETL de 300 líneas en un solo bloque es imposible de probar y de depurar. Un ETL organizado en **cuatro funciones** (extraer, transformar, validar, cargar) y un `main` mínimo se puede probar pieza por pieza, y cuando algo falla sabes en cuál etapa mirar. Es la estructura que usarás en el proyecto final y la que se explica en una entrevista.

## Términos nuevos

- **Extraer** (`extraer`): leer el origen con separador y codificación conocidos y devolver los datos **sin cambiarlos** (Bronze).
- **Transformar** (`transformar`): normalizar, convertir, separar válidas de rechazadas y calcular las capas (Silver y los rechazos).
- **Validar** (`validar`): comprobar las reglas y los cuadres sobre lo transformado; si algo no cuadra, lanza un error.
- **Cargar** (`cargar`): publicar el resultado de forma completa y atómica (Gold, Silver, rechazos).
- **`main`**: la función de arranque, corta: recibe la configuración, llama a las cuatro funciones en orden y registra.
- **Función pura**: la que depende solo de sus entradas y no tiene efectos secundarios (lección 8.1). `transformar` y `validar` pueden serlo; `extraer` y `cargar` tocan archivos.
- **Separación de responsabilidades**: cada función hace una sola cosa, así un fallo se localiza.

## Ejemplo paso a paso

Construimos un ETL pequeño y completo con datos inventados. Entrada: un CSV de ventas de kioscos. Salida: una base SQLite con Gold y los rechazos, y un informe de conteos.

**1. Preparar el archivo de entrada** (solo para el ejemplo):

```python
from pathlib import Path

CRUDO = """id_venta;fecha;kiosco;cantidad;precio;estado
V1;03/09/2026;Luna;10;Bs 6,00;entregado
V2;2026-09-03;Faro;4;9;Entregado
V2;2026-09-03;Faro;4;9;Entregado
V3;04/09/2026;;1,5;6;entregado
V4;05/09/2026;Luna;3;10;anulado
V5;31/02/2026;Faro;2;5;entregado
V6;06/09/2026;Salud;2;8;entregado
"""
Path("ventas_kioscos.csv").write_text(CRUDO, encoding="utf-8")
print(len(CRUDO.splitlines()) - 1, "filas de datos")
```

```salida
7 filas de datos
```

**2. Las cuatro funciones y el `main`.** Todo junto, leído de arriba abajo:

```python
import csv
import logging
import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

ESTADOS = {"entregado", "anulado"}
logger = logging.getLogger("etl_kioscos")
logger.setLevel(logging.INFO)
logger.handlers.clear()
_h = logging.StreamHandler(sys.stdout)
_h.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
logger.addHandler(_h)


# ---------------------------------------------------------------- extraer
def extraer(ruta):
    """Lee el CSV tal como llegó (todo texto). No transforma nada."""
    with Path(ruta).open(encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f, delimiter=";"))
    columnas = ["id_venta", "fecha", "kiosco", "cantidad", "precio", "estado"]
    faltan = [c for c in columnas if c not in filas[0]] if filas else columnas
    if faltan:
        raise ValueError(f"faltan columnas obligatorias: {faltan}")
    return filas


# ---------------------------------------------------------------- transformar
def convertir_fecha(texto):
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto.strip(), formato).date().isoformat()
        except ValueError:
            pass
    return None


def convertir_precio_centavos(texto):
    limpio = texto.replace("Bs", "").strip().replace(",", ".")
    try:
        valor = Decimal(limpio)
    except InvalidOperation:
        return None
    return int(valor * 100) if valor > 0 else None


def convertir_cantidad(texto):
    limpio = texto.strip()
    if limpio.isdigit() and int(limpio) > 0:
        return int(limpio)
    return None


def transformar(filas):
    """Devuelve (silver, rechazos, duplicados_exactos). No modifica la entrada."""
    vistos = set()
    unicas, duplicados = [], 0
    for fila in filas:
        huella = tuple(sorted(fila.items()))
        if huella in vistos:
            duplicados += 1
            continue
        vistos.add(huella)
        unicas.append(fila)

    silver, rechazos = [], []
    for fila in unicas:
        motivos = []
        fecha = convertir_fecha(fila["fecha"])
        cantidad = convertir_cantidad(fila["cantidad"])
        precio = convertir_precio_centavos(fila["precio"])
        estado = fila["estado"].strip().lower()
        if fecha is None:
            motivos.append("fecha inválida")
        if not fila["kiosco"].strip():
            motivos.append("kiosco ausente")
        if cantidad is None:
            motivos.append("cantidad no entera positiva")
        if precio is None:
            motivos.append("precio inválido")
        if estado not in ESTADOS:
            motivos.append("estado no permitido")
        if motivos:
            rechazos.append({"id_venta": fila["id_venta"], "motivo": "; ".join(motivos)})
        else:
            silver.append({"id_venta": fila["id_venta"], "fecha": fecha, "kiosco": fila["kiosco"].strip(),
                           "importe_centavos": cantidad * precio, "estado": estado})
    return silver, rechazos, duplicados


def construir_gold(silver):
    gold = {}
    for fila in silver:
        if fila["estado"] == "entregado":
            gold[fila["kiosco"]] = gold.get(fila["kiosco"], 0) + fila["importe_centavos"]
    return [{"kiosco": k, "importe_centavos": v} for k, v in sorted(gold.items())]


# ---------------------------------------------------------------- validar
def validar(n_bronze, duplicados, silver, rechazos, gold):
    if n_bronze != duplicados + len(rechazos) + len(silver):
        raise RuntimeError("cuadre de filas: Bronze != duplicados + rechazos + Silver")
    total_silver = sum(f["importe_centavos"] for f in silver if f["estado"] == "entregado")
    total_gold = sum(f["importe_centavos"] for f in gold)
    if total_silver != total_gold:
        raise RuntimeError("cuadre de valor: Silver entregado != Gold")


# ---------------------------------------------------------------- cargar
def cargar(silver, rechazos, gold, destino):
    temporal = destino.with_suffix(".tmp")
    if temporal.exists():
        temporal.unlink()
    with closing(sqlite3.connect(temporal)) as con:
        con.execute("CREATE TABLE silver (id_venta TEXT, fecha TEXT, kiosco TEXT, importe_centavos INTEGER, estado TEXT)")
        con.execute("CREATE TABLE rechazos (id_venta TEXT, motivo TEXT)")
        con.execute("CREATE TABLE gold_kiosco (kiosco TEXT, importe_centavos INTEGER)")
        con.executemany("INSERT INTO silver VALUES (:id_venta, :fecha, :kiosco, :importe_centavos, :estado)", silver)
        con.executemany("INSERT INTO rechazos VALUES (:id_venta, :motivo)", rechazos)
        con.executemany("INSERT INTO gold_kiosco VALUES (:kiosco, :importe_centavos)", gold)
        con.commit()
    os.replace(temporal, destino)


# ---------------------------------------------------------------- main
def main(entrada, destino):
    filas = extraer(entrada)
    logger.info("extracción: %d filas", len(filas))
    silver, rechazos, duplicados = transformar(filas)
    gold = construir_gold(silver)
    logger.info("transformación: %d duplicados, %d rechazadas, %d válidas", duplicados, len(rechazos), len(silver))
    validar(len(filas), duplicados, silver, rechazos, gold)
    logger.info("validación: cuadres de filas y de valor correctos")
    cargar(silver, rechazos, gold, Path(destino))
    logger.info("carga: publicado en %s", Path(destino).name)
    return rechazos, gold


# Archivo de ejemplo (solo para esta lección; es el mismo del paso 1)
Path("ventas_kioscos.csv").write_text(
    "id_venta;fecha;kiosco;cantidad;precio;estado\n"
    "V1;03/09/2026;Luna;10;Bs 6,00;entregado\n"
    "V2;2026-09-03;Faro;4;9;Entregado\n"
    "V2;2026-09-03;Faro;4;9;Entregado\n"
    "V3;04/09/2026;;1,5;6;entregado\n"
    "V4;05/09/2026;Luna;3;10;anulado\n"
    "V5;31/02/2026;Faro;2;5;entregado\n"
    "V6;06/09/2026;Salud;2;8;entregado\n",
    encoding="utf-8",
)
rechazos, gold = main("ventas_kioscos.csv", "kioscos.db")
print(rechazos)
print(gold)

# Verificación sobre la base ya publicada (paso 5)
with closing(sqlite3.connect("kioscos.db")) as con:
    print(con.execute("SELECT COUNT(*) FROM silver").fetchone()[0])
    print(con.execute("SELECT id_venta, motivo FROM rechazos ORDER BY id_venta").fetchall())
    print(con.execute("SELECT SUM(importe_centavos) FROM silver WHERE estado = 'entregado'").fetchone()[0])
```

```salida
INFO | extracción: 7 filas
INFO | transformación: 1 duplicados, 2 rechazadas, 4 válidas
INFO | validación: cuadres de filas y de valor correctos
INFO | carga: publicado en kioscos.db
[{'id_venta': 'V3', 'motivo': 'kiosco ausente; cantidad no entera positiva'}, {'id_venta': 'V5', 'motivo': 'fecha inválida'}]
[{'kiosco': 'Faro', 'importe_centavos': 3600}, {'kiosco': 'Luna', 'importe_centavos': 6000}, {'kiosco': 'Salud', 'importe_centavos': 1600}]
4
[('V3', 'kiosco ausente; cantidad no entera positiva'), ('V5', 'fecha inválida')]
11200
```

Cómo se lee el resultado:

- **Extracción:** 7 filas.
- **Transformación:** 1 duplicado exacto (V2), 2 rechazadas (V3 con **dos** motivos; V5 con fecha inexistente) y 4 válidas.
- **Validación:** ambos cuadres cierran (`7 = 1 + 2 + 4`; el importe de Silver entregado coincide con Gold).
- **Carga:** publicada con archivo temporal y `os.replace`.
- **Gold** (en centavos): Faro 3 600 (4 × 9,00), Luna 6 000 (10 × 6,00) y Salud 1 600 (2 × 8,00). La venta anulada V4 está en Silver pero no suma en Gold.

**3. Por qué esta estructura.** Cada función se puede probar sola:

```python
from decimal import Decimal, InvalidOperation


def convertir_precio_centavos(texto):
    limpio = texto.replace("Bs", "").strip().replace(",", ".")
    try:
        valor = Decimal(limpio)
    except InvalidOperation:
        return None
    return int(valor * 100) if valor > 0 else None


assert convertir_precio_centavos("Bs 6,00") == 600
assert convertir_precio_centavos("9") == 900
assert convertir_precio_centavos("abc") is None
assert convertir_precio_centavos("0") is None
print("pruebas de la conversión correctas")
```

```salida
pruebas de la conversión correctas
```

Si el total final no cuadra, ejecutas `extraer`, luego `transformar` con 3 filas, luego `validar`, y encuentras la etapa culpable en minutos. Y si mañana cambia el origen (otro separador), solo se toca `extraer`.

**4. Dónde están los puntos de control.**

| Etapa | Control |
|---|---|
| `extraer` | columnas obligatorias presentes (error de estructura → detener) |
| `transformar` | cada regla del contrato; motivos múltiples; duplicados exactos contados |
| `validar` | cuadre de filas y cuadre de valor; si fallan, **error** (no `assert`) |
| `cargar` | archivo temporal + reemplazo atómico + conexión cerrada |

**5. Verificar la base publicada.** Las últimas líneas del programa anterior consultan la base ya publicada, por SQL, y es el mismo control hecho por otro camino: hay 4 filas en `silver`; la tabla `rechazos` tiene V3 y V5 con sus motivos; y el importe de Silver entregado suma 11 200 centavos (Bs 112,00), igual que 3 600 + 6 000 + 1 600 en Gold. Revisar lo publicado, y no solo lo que tenías en memoria, es la prueba de que la carga hizo lo que crees.

Ejemplo comercial: el jefe de datos pregunta «¿por qué V3 no está en el reporte?». Abres `rechazos` y respondes: «kiosco ausente; cantidad 1,5 no entera». La estructura en funciones hace que esa respuesta sea inmediata.

## Errores comunes

- **Un solo bloque de 300 líneas** que lee, limpia y escribe.
- **Una función que hace dos etapas a la vez** (limpia y carga).
- **`main` con lógica** en lugar de solo orquestar.
- **Validar con `assert`** en lugar de errores explícitos.
- **Modificar la entrada** dentro de `transformar`.
- **No probar las funciones de conversión** por separado.
- **Rutas y parámetros escritos dentro de las funciones.**
- **Copiar un ETL ajeno sin entender sus reglas.**

## Para comprobar que entendiste

1. ¿Cuáles son las cuatro funciones y qué hace cada una?
2. ¿Qué debe contener el `main`?
3. ¿Por qué `validar` lanza un error y no un `assert`?
4. ¿Dónde se corrige un cambio de separador en el origen?

<details><summary>Respuestas</summary>

1. `extraer` lee sin cambiar, `transformar` normaliza y separa válidas/rechazos, `validar` comprueba reglas y cuadres, `cargar` publica de forma completa y atómica.
2. Solo orquestación: recibir parámetros, llamar a las funciones en orden y registrar.
3. Porque los `assert` pueden desactivarse al ejecutar Python con optimización.
4. En `extraer`.

</details>

## Micropráctica

Con un CSV de pedidos que inventes (columnas `pedido`, `cliente`, `fecha`, `monto`, `estado`):

1. Escribe su contrato y las cuatro funciones (puedes partir de la estructura de esta lección, pero **con tus propias reglas y tus propios datos**).
2. Incluye una fila con dos motivos de rechazo y un duplicado exacto.
3. Haz que `validar` falle a propósito (altera un número) y comprueba que el destino anterior no cambia.
4. Escribe la explicación de tu ETL en cinco líneas, como si se la contaras a un entrevistador.

Cómo saber que está bien: tus dos cuadres cierran y puedes ejecutar el programa dos veces con el mismo resultado.

<details><summary>Pista de estructura</summary>

El esqueleto mínimo es: `extraer(ruta) -> filas`, `transformar(filas) -> (silver, rechazos, duplicados)`, `validar(...) -> None o error`, `cargar(...) -> None` y `main(entrada, destino)`. Cada función se prueba sola con 3 filas escritas a mano antes de integrarlas.

</details>

## Después, en los ejercicios

Esta estructura es la del mini-ETL (ME01–ME04) y del ETL de la evaluación final. La referencia validada de los ejercicios está separada de las actividades: no la abras antes de terminar tu intento ([`03_EJERCICIOS/Puente/`](../../03_EJERCICIOS/Puente/)). Siguiente capítulo: [Capítulo 6 — KPIs](../06_KPIs.md).
