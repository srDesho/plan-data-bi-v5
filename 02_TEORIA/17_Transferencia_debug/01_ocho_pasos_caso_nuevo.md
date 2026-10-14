# 17.1 Los ocho pasos frente a un caso nuevo

> Tiempo estimado: 70 min (lectura 30 + práctica 40). Prerrequisitos: capítulo 5 completo y [10.5 Controles de calidad](../10_Pandas_transformaciones/05_controles_calidad.md).

## Para qué sirve

Aprender un ETL de memoria no demuestra que puedas construir otro. Un caso de **transferencia** cambia los nombres de las columnas, las claves, el catálogo y los formatos, y comprueba si entiendes el método y no solo una receta. Aquí practicas el método de ocho pasos sobre un dominio distinto al de los ejemplos anteriores (una bodega y su catálogo de productos), y ves cómo reaccionar ante cambios adversos del archivo.

## Términos nuevos

- **Transferencia**: aplicar lo aprendido en un problema parecido pero con datos, nombres y reglas distintos.
- **Cambio adverso**: una variación del archivo que pone a prueba el proceso (columna nueva, columna ausente, catálogo contradictorio).
- **Columna opcional / obligatoria**: una columna que el proceso puede ignorar frente a una sin la cual no puede continuar.
- **Diccionario de datos**: documento que define cada columna, su significado, tipo y valores válidos.
- **Error legible**: un mensaje que dice qué falló y dónde (en lugar de un traceback críptico).
- **Idempotencia lógica**: que dos ejecuciones generen las mismas claves, filas y totales (no exige que los bytes internos del archivo sean idénticos).
- **Carga incremental**: agregar solo lo nuevo. Aquí **no** se practica; las cargas del curso son completas.

## Ejemplo paso a paso

**El caso (inventado):** la bodega de una cadena envía un archivo de **movimientos** de entrada y salida de productos y un **catálogo** de productos. Columnas del movimiento: `mov_id`, `fecha`, `sku`, `tipo` (`entrada`/`salida`), `unidades`, `costo_unit`. Columnas del catálogo: `sku`, `producto`, `categoria`.

**Antes de escribir código: el diccionario.** Con 3 filas a mano, decide:

- Una fila = un movimiento de un producto. Clave: `mov_id`.
- `tipo` ∈ {`entrada`, `salida`}; `unidades` entero positivo; `costo_unit` decimal positivo con `Bs`/coma admitidos; `fecha` `DD/MM/AAAA` o ISO.
- `sku` debe existir en el catálogo (huérfano → rechazo).
- Cuadres: Bronze = duplicados + rechazados + Silver; entradas − salidas por SKU = saldo.

**Los datos de entrada del ejemplo:**

```python
import io
import pandas as pd

MOVS = """mov_id,fecha,sku,tipo,unidades,costo_unit
M1,02/09/2026,A100,entrada,50,Bs 4,50
M2,03/09/2026,A100,salida,20,4.5
M2,03/09/2026,A100,salida,20,4.5
M3,03/09/2026,B200,entrada,10,12
M4,04/09/2026,B200,salida,12.5,12
M5,04/09/2026,Z999,salida,3,7
M6,05/09/2026,B200,Devolucion,2,12
"""
CATALOGO = """sku,producto,categoria
A100,Cuaderno,Papelería
B200,Mochila,Escolar
"""
print(len(MOVS.strip().splitlines()) - 1, "filas de movimientos")
```

```salida
7 filas de movimientos
```

Atención: el primer movimiento trae `Bs 4,50` con una **coma decimal dentro de un archivo separado por comas**: la fila tiene un campo de más. Un archivo así no se puede leer con `read_csv` sin cuidado. Este es el tipo de hallazgo del paso 2.

**Paso 1 · Bronze: copiar sin tocar y registrar.**

```python
import io
import pandas as pd

MOVS = """mov_id,fecha,sku,tipo,unidades,costo_unit
M1,02/09/2026,A100,entrada,50,"Bs 4,50"
M2,03/09/2026,A100,salida,20,4.5
M2,03/09/2026,A100,salida,20,4.5
M3,03/09/2026,B200,entrada,10,12
M4,04/09/2026,B200,salida,12.5,12
M5,04/09/2026,Z999,salida,3,7
M6,05/09/2026,B200,Devolucion,2,12
"""
bronze = pd.read_csv(io.StringIO(MOVS), dtype=str)
print(bronze.shape, list(bronze.columns))
print(bronze.loc[0, "costo_unit"])
```

```salida
(7, 6) ['mov_id', 'fecha', 'sku', 'tipo', 'unidades', 'costo_unit']
Bs 4,50
```

En el archivo real, el valor `Bs 4,50` debe venir **entre comillas** (`"Bs 4,50"`); así el CSV lo lee como un solo campo. Si el origen no lo cita, es un defecto del origen que se **informa**, no se parchea adivinando. Leer todo como texto (`dtype=str`) conserva lo que llegó. Registra: 7 filas, 6 columnas.

**Paso 2 · Perfilar.**

```python
import io
import pandas as pd

MOVS = """mov_id,fecha,sku,tipo,unidades,costo_unit
M1,02/09/2026,A100,entrada,50,"Bs 4,50"
M2,03/09/2026,A100,salida,20,4.5
M2,03/09/2026,A100,salida,20,4.5
M3,03/09/2026,B200,entrada,10,12
M4,04/09/2026,B200,salida,12.5,12
M5,04/09/2026,Z999,salida,3,7
M6,05/09/2026,B200,Devolucion,2,12
"""
bronze = pd.read_csv(io.StringIO(MOVS), dtype=str)
print(bronze["tipo"].value_counts().to_dict())
print(int(bronze.duplicated().sum()), "duplicado exacto")
print(bronze[~bronze["unidades"].str.fullmatch(r"\d+")]["mov_id"].tolist(), "unidades no enteras")
print(sorted(set(bronze["sku"]) - {"A100", "B200"}), "SKU fuera del catálogo")
```

```salida
{'salida': 4, 'entrada': 2, 'Devolucion': 1}
1 duplicado exacto
['M4'] unidades no enteras
['Z999'] SKU fuera del catálogo
```

Hallazgos: el tipo `Devolucion` **no está permitido**; hay 1 duplicado exacto (M2); M4 tiene `12.5` unidades (no entera); el SKU `Z999` no existe en el catálogo.

**Paso 3 · Clasificar los problemas.**

| Problema | Clase | Acción |
|---|---|---|
| M2 duplicado exacto | duplicado | eliminar uno y contar |
| M4 unidades 12.5 | fila rechazable | rechazar (no truncar) |
| M5 SKU inexistente | huérfana | rechazar |
| M6 tipo `Devolucion` | valor no permitido | rechazar |
| `Bs 4,50` con comillas | formato admitido | normalizar |

No hay errores de estructura ni conflictos de clave: el proceso continúa.

**Paso 4 y 5 · Funciones pequeñas con pruebas y transformación con rechazos.**

```python
import io
from decimal import Decimal, InvalidOperation

import pandas as pd

MOVS = """mov_id,fecha,sku,tipo,unidades,costo_unit
M1,02/09/2026,A100,entrada,50,"Bs 4,50"
M2,03/09/2026,A100,salida,20,4.5
M2,03/09/2026,A100,salida,20,4.5
M3,03/09/2026,B200,entrada,10,12
M4,04/09/2026,B200,salida,12.5,12
M5,04/09/2026,Z999,salida,3,7
M6,05/09/2026,B200,Devolucion,2,12
"""
CATALOGO = ["A100", "B200"]
TIPOS = {"entrada", "salida"}


def costo_centavos(texto):
    limpio = texto.replace("Bs", "").strip().replace(",", ".")
    try:
        valor = Decimal(limpio)
    except InvalidOperation:
        return None
    return int(valor * 100) if valor > 0 else None


def unidades_validas(texto):
    return int(texto) if texto.strip().isdigit() and int(texto) > 0 else None


assert costo_centavos("Bs 4,50") == 450
assert costo_centavos("12") == 1200
assert unidades_validas("12.5") is None
assert unidades_validas("20") == 20

bronze = pd.read_csv(io.StringIO(MOVS), dtype=str)
duplicados = int(bronze.duplicated().sum())
unica = bronze.drop_duplicates()

silver, rechazos = [], []
for _, f in unica.iterrows():
    motivos = []
    unidades = unidades_validas(f["unidades"])
    costo = costo_centavos(f["costo_unit"])
    if unidades is None:
        motivos.append("unidades no enteras positivas")
    if costo is None:
        motivos.append("costo inválido")
    if f["tipo"].strip().lower() not in TIPOS:
        motivos.append("tipo no permitido")
    if f["sku"] not in CATALOGO:
        motivos.append("sku no existe en el catálogo")
    if motivos:
        rechazos.append((f["mov_id"], "; ".join(motivos)))
    else:
        silver.append({"mov_id": f["mov_id"], "sku": f["sku"], "tipo": f["tipo"], "unidades": unidades, "valor_centavos": unidades * costo})

print(len(bronze), duplicados, len(rechazos), len(silver))
print(len(bronze) == duplicados + len(rechazos) + len(silver))
print(rechazos)
```

```salida
7 1 3 3
True
[('M4', 'unidades no enteras positivas'), ('M5', 'sku no existe en el catálogo'), ('M6', 'tipo no permitido')]
```

Cada regla del contrato es una condición con motivo; las dos funciones de conversión se probaron con `assert` antes de usarlas. **Cuadre de filas:** 7 = 1 + 3 + 3 (3 rechazos, 3 válidas).

**Paso 6 · Unir el catálogo con control de cardinalidad.**

```python
import io
import pandas as pd

CATALOGO = """sku,producto,categoria
A100,Cuaderno,Papelería
B200,Mochila,Escolar
"""
cat = pd.read_csv(io.StringIO(CATALOGO))
silver = pd.DataFrame({"mov_id": ["M1", "M2", "M3"], "sku": ["A100", "A100", "B200"], "unidades": [50, 20, 10]})

unido = silver.merge(cat, on="sku", how="left", validate="m:1", indicator=True)
print(len(silver), len(unido), unido["_merge"].value_counts().to_dict())
```

```salida
3 3 {'both': 3, 'left_only': 0, 'right_only': 0}
```

`validate="m:1"` confirma que el catálogo no repite SKU; el número de filas no cambia y no hay huérfanas.

**Paso 7 · Gold y cuadre con SQL independiente.** Se calcula el saldo por SKU en Pandas y se verifica con una consulta SQL sobre una base en memoria:

```python
import sqlite3
from contextlib import closing

import pandas as pd

silver = pd.DataFrame({
    "mov_id": ["M1", "M2", "M3"],
    "sku": ["A100", "A100", "B200"],
    "tipo": ["entrada", "salida", "entrada"],
    "unidades": [50, 20, 10],
})
silver["firmadas"] = silver["unidades"].where(silver["tipo"] == "entrada", -silver["unidades"])
gold = silver.groupby("sku", as_index=False)["firmadas"].sum().rename(columns={"firmadas": "saldo"})
print(gold.values.tolist())

with closing(sqlite3.connect(":memory:")) as con:
    silver[["mov_id", "sku", "tipo", "unidades"]].to_sql("silver", con, index=False)
    sql = con.execute(
        "SELECT sku, SUM(CASE WHEN tipo='entrada' THEN unidades ELSE -unidades END) FROM silver GROUP BY sku ORDER BY sku"
    ).fetchall()
print(sql)
print(gold.values.tolist() == [list(x) for x in sql])
```

```salida
[['A100', 30], ['B200', 10]]
[('A100', 30), ('B200', 10)]
True
```

El saldo por SKU (A100: 30, B200: 10) sale de **dos caminos distintos** (Pandas y SQL) y coinciden. Esa es la regla del paso 7: la verificación del Gold no se hace con el mismo código que lo calculó.

**Paso 8 · Reejecutar, documentar y explicar límites.** Una segunda ejecución con los mismos datos debe producir las mismas claves, filas y saldos (idempotencia lógica). Documentas: qué se rechazó y por qué, los cuadres, y los límites («el cálculo de saldo no incluye el stock inicial porque el archivo no lo trae»).

**Cambios adversos: cómo debe reaccionar el proceso.**

| Cambio | Reacción correcta |
|---|---|
| llega una columna nueva no obligatoria (`lote`) | se conserva en Bronze y se **ignora explícitamente** en Silver (documentado) |
| falta una columna obligatoria (`sku`) | **error legible** que detiene el proceso |
| el catálogo repite un SKU con productos distintos | `validate="m:1"` **detiene** la unión |
| faltan datos para un indicador (no hay `costo_unit`) | indicador «**no calculable**»; se solicita el dato; no se construye un sustituto con el mismo nombre |

```python
import pandas as pd

OBLIGATORIAS = ["mov_id", "fecha", "sku", "tipo", "unidades", "costo_unit"]


def verificar_columnas(df):
    faltan = [c for c in OBLIGATORIAS if c not in df.columns]
    if faltan:
        raise ValueError(f"columnas obligatorias ausentes: {faltan}")
    return [c for c in df.columns if c not in OBLIGATORIAS]


print(verificar_columnas(pd.DataFrame(columns=OBLIGATORIAS + ["lote"])))
try:
    verificar_columnas(pd.DataFrame(columns=["mov_id", "fecha"]))
except ValueError as e:
    print(e)
```

```salida
['lote']
columnas obligatorias ausentes: ['sku', 'tipo', 'unidades', 'costo_unit']
```

Una columna extra (`lote`) se detecta y se informa como ignorada; la falta de columnas obligatorias detiene el proceso con un mensaje claro.

Ejemplo comercial: el mes siguiente la bodega añade la columna `lote` y la reorganiza. Un proceso que ya separa la lectura (`extraer`) de las reglas no se rompe: avisa de la columna nueva y sigue.

## Errores comunes

- **Programar sin el diccionario de datos.**
- **Parchear en silencio un defecto del origen** (la coma decimal sin comillas).
- **Truncar `12.5` unidades a 12.**
- **Verificar el Gold con el mismo código que lo calculó.**
- **Construir un sustituto de un indicador cuando falta un dato.**
- **No probar los cambios adversos.**
- **Confundir idempotencia lógica con igualdad de bytes.**

## Para comprobar que entendiste

1. ¿Cuáles son los dos cuadres que cierran el proceso?
2. ¿Por qué se verifica el Gold con una consulta SQL independiente?
3. ¿Qué haces si falta una columna obligatoria? ¿Y si llega una opcional nueva?
4. ¿Qué haces si faltan los datos para calcular un indicador?

<details><summary>Respuestas</summary>

1. Filas (Bronze = duplicados + rechazadas + Silver) y valor (entre capas / por camino independiente).
2. Porque un error de lógica en el código original se repetiría en una verificación hecha con el mismo código.
3. Un error legible que detiene el proceso; la opcional se conserva en Bronze y se ignora explícitamente.
4. Lo documento como «no calculable» y solicito el dato.

</details>

## Micropráctica

Inventa un caso propio de transferencia (por ejemplo, pedidos de una panadería con `pedido`, `cliente`, `producto`, `precio`, `entregado`):

1. Escribe el diccionario de datos y el contrato.
2. Crea un archivo de 8 filas con 4 problemas distintos.
3. Aplica los ocho pasos y comprueba los dos cuadres.
4. Prueba un cambio adverso (una columna obligatoria ausente).

Cómo saber que está bien: tus dos cuadres cierran y tu proceso falla con un mensaje claro ante la columna ausente.

<details><summary>Pista</summary>

Empieza por el diccionario con tres filas escritas a mano. Cada regla del contrato es una condición con motivo; cada función de conversión se prueba con `assert` antes de usarla en el recorrido.

</details>

## Después, en los ejercicios

El caso de transferencia **C06** y la evaluación final siguen estos pasos. No abras `08_SOLUCIONES/controles_final.json` ni la referencia hasta terminar el intento integral ([`03_EJERCICIOS/Casos/`](../../03_EJERCICIOS/Casos/)). Siguiente: [17.2 Cuando no cuadra](02_cuando_no_cuadra.md).
