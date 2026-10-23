# 5.4 Cargas repetibles, registro (logging) y reproducibilidad

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [5.3 Rechazos y reconciliación](03_rechazos_y_reconciliacion.md), [8.4 Módulos](../08_Python_funciones_archivos/04_modulos_imports.md) y [10.4 Exportación](../10_Pandas_transformaciones/04_resumen_y_exportacion.md).

## Para qué sirve

Un ETL se ejecuta muchas veces: cada día, cada mes, cuando alguien corrige el origen. Si cada ejecución duplica filas, deja la base a medias cuando falla o no deja rastro de lo que hizo, no se puede confiar en él. Esta lección trata tres garantías de ingeniería de datos: que repetir el proceso no cambie el resultado (**idempotencia**), que un fallo no deje basura (**carga atómica**) y que el proceso cuente lo que hizo (**registro** o *logging*).

## Términos nuevos

- **Idempotencia**: propiedad de una operación que, ejecutada una o varias veces, produce el mismo resultado. Una carga idempotente no duplica datos al repetirse.
- **Carga completa**: reemplazar todo el destino con el resultado nuevo (la que usa este curso). La **carga incremental** agrega solo lo nuevo y es más compleja; queda para más adelante.
- **Carga atómica**: la que se publica entera o no se publica. Se logra construyendo el resultado en un archivo temporal y reemplazando el destino solo si todo salió bien.
- **Archivo temporal**: un archivo auxiliar donde se construye el resultado antes de publicarlo.
- **Registro (log)**: mensajes que el programa escribe sobre lo que hace: etapa, conteos, advertencias, errores. En Python se usa el módulo `logging`.
- **Nivel de registro**: la importancia de un mensaje: `INFO` (informativo), `WARNING` (advertencia), `ERROR` (fallo).
- **Reproducibilidad**: que otra persona (o tú dentro de un mes) pueda ejecutar el proceso con las mismas entradas y versiones y obtener el mismo resultado.
- **Configuración**: los valores que cambian entre ejecuciones (rutas, fecha de corte) y que se reciben como parámetros, no se escriben dentro del código.
- **`os.replace`**: la instrucción que reemplaza un archivo por otro de forma atómica.

## Ejemplo paso a paso

**1. Reejecutar sin duplicar.** Ya viste en 10.4 que `append` duplica y `replace` no. En un ETL el principio es el mismo: la salida depende solo de la entrada.

```python
import sqlite3
from contextlib import closing

import pandas as pd

gold = pd.DataFrame({"ruta": ["R01", "R02"], "importe_centavos": [126500, 51000]})


def cargar(df, ruta_db):
    with closing(sqlite3.connect(ruta_db)) as con:
        df.to_sql("gold_ruta", con, if_exists="replace", index=False)


for _ in range(3):
    cargar(gold, "destino.db")

with closing(sqlite3.connect("destino.db")) as con:
    print(con.execute("SELECT COUNT(*), SUM(importe_centavos) FROM gold_ruta").fetchone())
```

```salida
(2, 177500)
```

Después de tres ejecuciones el destino sigue teniendo 2 filas y el mismo total: es **idempotente**.

**2. Publicar solo si todo salió bien (carga atómica).** Se construye una base nueva en un archivo temporal, se valida y **recién entonces** se reemplaza el destino:

```python
import os
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd


def publicar(df, destino):
    temporal = destino.with_suffix(".tmp")
    if temporal.exists():
        temporal.unlink()

    with closing(sqlite3.connect(temporal)) as con:
        df.to_sql("gold_ruta", con, index=False)
        filas = con.execute("SELECT COUNT(*) FROM gold_ruta").fetchone()[0]

    if filas != len(df):
        temporal.unlink()
        raise RuntimeError("la base temporal no coincide con los datos: no se publica")

    os.replace(temporal, destino)


destino = Path("final.db")
publicar(pd.DataFrame({"ruta": ["R01"], "importe_centavos": [100]}), destino)
publicar(pd.DataFrame({"ruta": ["R01", "R02"], "importe_centavos": [100, 200]}), destino)

with closing(sqlite3.connect(destino)) as con:
    print(con.execute("SELECT COUNT(*) FROM gold_ruta").fetchone()[0])
```

```salida
2
```

El flujo: crear temporal → escribir → **validar** (aquí, que las filas coincidan) → `os.replace`. Si algo falla antes del `replace`, el destino anterior queda intacto: el reporte sigue mostrando la versión buena. **En Windows hay una trampa**: antes de `os.replace` la conexión a la base temporal tiene que estar cerrada; por eso se usa `closing(...)`. Con `with sqlite3.connect(...)` solo se confirma la transacción, pero la conexión sigue abierta y `os.replace` falla con `PermissionError` (el [capítulo 19](../19_Puente_Python_a_ETL.md), §4, lo muestra con detalle).

**3. Registro con `logging`.** Cada etapa deja un mensaje con sus conteos:

```python
import logging
import sys

logger = logging.getLogger("etl_demo")
logger.setLevel(logging.INFO)
logger.handlers.clear()
manejador = logging.StreamHandler(sys.stdout)
manejador.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
logger.addHandler(manejador)

logger.info("extracción: %d filas leídas", 120)
logger.info("transformación: %d duplicados, %d rechazadas, %d válidas", 4, 6, 110)
logger.warning("vendedores recuperados por ruta: %d", 3)
logger.error("cuadre de filas NO coincide: faltan %d filas", 2)
```

```salida
INFO | extracción: 120 filas leídas
INFO | transformación: 4 duplicados, 6 rechazadas, 110 válidas
WARNING | vendedores recuperados por ruta: 3
ERROR | cuadre de filas NO coincide: faltan 2 filas
```

`getLogger` crea el registrador; el formato indica cómo se imprime cada mensaje; `info`, `warning` y `error` son los niveles. Los `%d` se llenan con los valores que siguen. **Qué registrar:** etapa, conteos, advertencias, y las decisiones. **Qué NO registrar:** claves secretas, contraseñas ni datos personales. En un programa real el log se guarda también en un archivo (con `FileHandler`).

**4. Configuración por parámetros.** Las rutas y la fecha de corte no se escriben dentro de las funciones:

```python
from pathlib import Path


def ejecutar_etl(carpeta_entrada, carpeta_salida, fecha_corte):
    entrada = Path(carpeta_entrada)
    salida = Path(carpeta_salida)
    salida.mkdir(parents=True, exist_ok=True)
    return {"entrada": entrada.name, "salida": salida.name, "corte": fecha_corte}


print(ejecutar_etl("datos/crudos", "datos/resultado", "2026-09-30"))
```

```salida
{'entrada': 'crudos', 'salida': 'resultado', 'corte': '2026-09-30'}
```

Con parámetros, el mismo código procesa otro mes o otra carpeta sin tocarlo; y quien lo ejecute sabe exactamente qué le entrega. Un script reproducible **no depende de celdas ejecutadas hace una semana** ni de variables que quedaron en la memoria de una sesión.

**5. Reproducibilidad: lo que debes anotar.**

| Qué | Dónde |
|---|---|
| versión de Python y de los paquetes | `requirements.txt` y el informe |
| entradas (nombres, tamaño o hash) | el log o un manifiesto |
| fecha de corte y parámetros | argumentos del programa |
| semilla de azar, si hay muestreo | constante visible |
| versión del contrato | encabezado del contrato |

Con esto, «en mi computadora funciona» se convierte en «con estas versiones y estas entradas da esto».

**6. Reintentar un fallo transitorio (opcional, aprendizaje del `while`).**

```python
intentos = 0
exito = False
while intentos < 3 and not exito:
    intentos = intentos + 1
    exito = intentos == 3
    print("intento", intentos, "ok" if exito else "falló")
```

```salida
intento 1 falló
intento 2 falló
intento 3 ok
```

Un ETL no debe «reintentar hasta que funcione» sin límite ni sin entender por qué falló: un reintento ayuda ante un archivo bloqueado un instante; no ante un dato inválido.

Ejemplo comercial: el ETL corre cada madrugada. Una noche el catálogo llega incompleto y la validación falla. Gracias a la carga atómica, el tablero de la mañana sigue mostrando los datos de ayer (buenos) y el log dice «catálogo: 48 de 120 productos, no se publica». Nadie vio un reporte roto.

## Errores comunes

- **`append` en una carga que se repite** (duplicación).
- **Escribir directamente sobre el destino** y dejarlo a medias si falla.
- **No cerrar la conexión SQLite** antes de reemplazar el archivo (Windows).
- **Cambiar la salida entre ejecuciones** (orden, nombres de columnas).
- **Registrar datos privados** o claves.
- **Logs que dicen «terminó» sin conteos.**
- **Rutas y fechas escritas dentro del código.**
- **Reintentos infinitos** ante errores de datos.

## Para comprobar que entendiste

1. ¿Qué significa que una carga sea idempotente?
2. ¿Qué ventaja tiene construir en un archivo temporal y usar `os.replace`?
3. ¿Qué debe contener un buen mensaje de registro y qué no?
4. ¿Por qué se pasa la fecha de corte como parámetro?

<details><summary>Respuestas</summary>

1. Que ejecutarla varias veces deja el mismo resultado que ejecutarla una.
2. Que el destino solo cambia si todo salió bien; si falla, la versión anterior queda intacta.
3. Etapa, conteos y decisiones; no claves ni datos personales.
4. Para que el mismo código sea reproducible y sirva para otro período sin modificarse.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe `publicar(df, destino)` con archivo temporal, validación de filas y `os.replace`, y pruébalo dos veces.
2. Provoca una validación que falle y comprueba que el destino anterior queda intacto.
3. Agrega tres mensajes de registro a un proceso tuyo (extracción, transformación, carga) con conteos.
4. Haz una lista de los parámetros que tu ETL debe recibir en lugar de tenerlos escritos dentro.

Cómo saber que está bien: el destino tiene siempre el mismo contenido tras reejecutar, y tras un fallo conserva la versión anterior.

<details><summary>Comprobación de la parte 2</summary>

```python
import os
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd


def publicar(df, destino, filas_esperadas):
    temporal = destino.with_suffix(".tmp")
    with closing(sqlite3.connect(temporal)) as con:
        df.to_sql("t", con, if_exists="replace", index=False)
    if len(df) != filas_esperadas:
        temporal.unlink()
        raise RuntimeError("no se publica")
    os.replace(temporal, destino)


destino = Path("seguro.db")
publicar(pd.DataFrame({"a": [1, 2]}), destino, 2)
try:
    publicar(pd.DataFrame({"a": [9]}), destino, 5)
except RuntimeError as e:
    print("falló:", e)

with closing(sqlite3.connect(destino)) as con:
    print(con.execute("SELECT COUNT(*) FROM t").fetchone()[0])
```

```salida
falló: no se publica
2
```

</details>

## Después, en los ejercicios

El ETL de transferencia y la evaluación final exigen una carga que se pueda repetir y un log con conteos ([`05_PROYECTOS/`](../../05_PROYECTOS/)). La prueba `python herramientas/prueba_sqlite_cierre.py` del paquete verifica que los scripts cierren sus conexiones. Siguiente: [5.5 Estructura de un ETL en funciones y módulos](05_estructura_etl_funciones.md).
