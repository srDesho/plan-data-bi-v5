# 10.5 Controles de calidad y reconciliación en Pandas

> Tiempo estimado: 65 min (lectura 25 + práctica 40). Prerrequisitos: [9.5 Nulos y duplicados](../09_Pandas_basico/05_nulos_duplicados.md), [8.5 Excepciones](../08_Python_funciones_archivos/05_excepciones.md) y [10.3 merge](03_merge_cardinalidad.md).

## Para qué sirve

Un programa que «corre sin errores» no es un programa que «da el resultado correcto». Los controles de calidad son preguntas que el propio programa se hace sobre los datos y sobre su propio trabajo, y que lo detienen o lo avisan cuando algo no cuadra. Esta lección reúne, en forma de funciones pequeñas, los controles que usarás en tus ETL: validar la estructura, validar cada fila y **reconciliar** (hacer cuadrar) lo que entró con lo que salió.

## Términos nuevos

- **Control de calidad**: una comprobación automática sobre los datos o sobre un resultado.
- **Validación de estructura**: comprueba lo que afecta a **todo** el archivo (columnas requeridas presentes, clave única, tipos). Si falla, se **detiene** el proceso.
- **Validación de fila**: comprueba cada registro (cantidad positiva, estado permitido). Si falla, la fila se **rechaza con motivo** y el proceso sigue.
- **Reconciliación** (o *cuadre*): comprobar que las cantidades de entrada, salida y rechazados cuadran: `entrada = válidas + rechazadas + duplicados`, y que los totales de valor coinciden entre capas.
- **Capa**: una etapa del pipeline. **Bronze**: el dato crudo tal como llegó; **Silver**: limpio, con tipos y claves, más la tabla de rechazos; **Gold**: resumen listo para el reporte.
- **Contrato de datos**: el documento que dice qué columnas, tipos y valores permitidos tiene el archivo.
- **`assert` frente a excepción explícita**: `assert` sirve para pruebas y comprobaciones internas; para controles de producción se usa `raise`, porque `assert` puede desactivarse al ejecutar Python con optimización.

## Ejemplo paso a paso

Datos crudos inventados (una exportación de líneas de venta con problemas):

```python
import io
import pandas as pd

TEXTO = """linea_id,venta_id,estado,cantidad,precio
1,10,entregado,3,12.5
2,10,entregado,2,8
3,11,anulado,1,50
3,11,anulado,1,50
4,12,entregado,-2,10
5,12,entregado,x,10
6,13,pendiente,4,9
7,13,entregado,5,
8,14,entregado,2,20
"""
crudo = pd.read_csv(io.StringIO(TEXTO), dtype=str)
print(len(crudo))
print(crudo.head(3))
```

```salida
9
  linea_id venta_id     estado cantidad precio
0        1       10  entregado        3   12.5
1        2       10  entregado        2      8
2        3       11    anulado        1     50
```

Leemos todo como **texto** (`dtype=str`) para no perder nada al leer: la capa Bronze conserva la entrada original. Hay 9 filas. Contrato (inventado): columnas `linea_id, venta_id, estado, cantidad, precio`; `linea_id` único; estado ∈ {`entregado`, `anulado`}; cantidad entera positiva; precio numérico mayor que 0.

**1. Validación de estructura (detiene el proceso).**

```python
import pandas as pd

COLUMNAS = ["linea_id", "venta_id", "estado", "cantidad", "precio"]


def validar_estructura(df):
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise ValueError(f"faltan columnas obligatorias: {faltan}")


ok = pd.DataFrame(columns=COLUMNAS)
validar_estructura(ok)
print("estructura correcta")

mal = pd.DataFrame(columns=["linea_id", "venta_id"])
validar_estructura(mal)
```

```error
ValueError: faltan columnas obligatorias: ['estado', 'cantidad', 'precio']
```

Si falta una columna obligatoria, el proceso **se detiene** con un mensaje claro: seguir procesando sería construir resultados sobre una base rota. (Se usa `raise`, no `assert`.)

**2. Validación de fila (rechazo con motivo).** Una función que devuelve el motivo del rechazo o `None` si la fila es válida:

```python
import pandas as pd

ESTADOS = {"entregado", "anulado"}


def motivo_rechazo(fila):
    if fila["estado"].strip().lower() not in ESTADOS:
        return "estado no permitido"
    try:
        cantidad = int(fila["cantidad"])
    except ValueError:
        return "cantidad no numérica"
    if cantidad <= 0:
        return "cantidad no positiva"
    if pd.isna(fila["precio"]):
        return "precio ausente"
    try:
        precio = float(fila["precio"])
    except ValueError:
        return "precio no numérico"
    if precio <= 0:
        return "precio no positivo"
    return None


print(motivo_rechazo({"estado": "entregado", "cantidad": "3", "precio": "12.5"}))
print(motivo_rechazo({"estado": "pendiente", "cantidad": "4", "precio": "9"}))
print(motivo_rechazo({"estado": "entregado", "cantidad": "x", "precio": "10"}))
print(motivo_rechazo({"estado": "entregado", "cantidad": "-2", "precio": "10"}))
print(motivo_rechazo({"estado": "entregado", "cantidad": "5", "precio": None}))
```

```salida
None
estado no permitido
cantidad no numérica
cantidad no positiva
precio ausente
```

Cada regla es una pregunta con respuesta clara y un motivo legible. Un estado desconocido (`pendiente`) **no se convierte en un estado válido**: se rechaza. Esta función es **pura** (lección 8.1) y se prueba con casos conocidos.

**3. Aplicar los controles: Bronze → Silver + rechazos.**

```python
import io
import pandas as pd

TEXTO = """linea_id,venta_id,estado,cantidad,precio
1,10,entregado,3,12.5
2,10,entregado,2,8
3,11,anulado,1,50
3,11,anulado,1,50
4,12,entregado,-2,10
5,12,entregado,x,10
6,13,pendiente,4,9
7,13,entregado,5,
8,14,entregado,2,20
"""
ESTADOS = {"entregado", "anulado"}


def motivo_rechazo(fila):
    if fila["estado"].strip().lower() not in ESTADOS:
        return "estado no permitido"
    try:
        cantidad = int(fila["cantidad"])
    except ValueError:
        return "cantidad no numérica"
    if cantidad <= 0:
        return "cantidad no positiva"
    if pd.isna(fila["precio"]):
        return "precio ausente"
    try:
        precio = float(fila["precio"])
    except ValueError:
        return "precio no numérico"
    if precio <= 0:
        return "precio no positivo"
    return None


bronze = pd.read_csv(io.StringIO(TEXTO), dtype=str)

duplicados = bronze.duplicated().sum()
sin_duplicados = bronze.drop_duplicates().copy()
sin_duplicados["motivo"] = sin_duplicados.apply(motivo_rechazo, axis=1)

rechazadas = sin_duplicados[sin_duplicados["motivo"].notna()]
silver = sin_duplicados[sin_duplicados["motivo"].isna()].drop(columns="motivo").copy()

print("bronze:", len(bronze), "duplicados:", duplicados)
print("silver:", len(silver), "rechazadas:", len(rechazadas))
print(rechazadas[["linea_id", "motivo"]].to_string(index=False))
print("cuadre de filas:", len(bronze) == duplicados + len(silver) + len(rechazadas))
```

```salida
bronze: 9 duplicados: 1
silver: 4 rechazadas: 4
linea_id               motivo
       4 cantidad no positiva
       5 cantidad no numérica
       6  estado no permitido
       7       precio ausente
cuadre de filas: True
```

El flujo: leer todo como texto (Bronze) → quitar duplicados exactos (y contarlos) → evaluar cada fila → separar Silver (válidas) de rechazadas con su motivo. Nada desapareció sin explicación.

**4. La reconciliación (el cuadre).** La última línea del programa anterior ya la hizo: `cuadre de filas: True` significa que 9 filas de Bronze = 1 duplicado + 4 rechazadas + 4 válidas. En un ETL real, si el cuadre **no** se cumple, el proceso debe detenerse con un error explícito:

```py
if len(bronze) != duplicados + len(silver) + len(rechazadas):
    raise RuntimeError("el cuadre de filas no coincide: se perdió o duplicó algo")
```

Hay tres cuadres típicos:

| Cuadre | Igualdad |
|---|---|
| Filas | Bronze = duplicados eliminados + rechazadas + Silver |
| Valor | importe de Silver (entregadas) = importe de Gold |
| Unión | filas antes y después de un `merge` m:1 son iguales |

**5. Convertir Silver a tipos finales y reconciliar valores.**

```python
import pandas as pd

silver = pd.DataFrame({
    "linea_id": ["1", "2", "3", "8"],
    "venta_id": ["10", "10", "11", "14"],
    "estado": ["entregado", "entregado", "anulado", "entregado"],
    "cantidad": ["3", "2", "1", "2"],
    "precio": ["12.5", "8", "50", "20"],
})
silver["cantidad"] = silver["cantidad"].astype(int)
silver["precio"] = silver["precio"].astype(float)
silver["importe"] = silver["cantidad"] * silver["precio"]

entregado = silver[silver["estado"] == "entregado"]
gold = entregado.groupby("venta_id", as_index=False)["importe"].sum()

print(entregado["importe"].sum(), gold["importe"].sum())
print(entregado["importe"].sum() == gold["importe"].sum())
```

```salida
93.5 93.5
True
```

El importe de Silver entregado (93,5) coincide con el total de Gold (93,5): el cuadre de valor se cumple. Si hubieras agregado mal (por ejemplo, tras una unión que duplica), esta igualdad fallaría y te avisaría.

**6. Controles de clave única.**

```python
import pandas as pd

df = pd.DataFrame({"linea_id": ["1", "2", "3", "3"]})
print(df["linea_id"].is_unique)
repetidas = df[df["linea_id"].duplicated(keep=False)]
print(repetidas["linea_id"].tolist())
```

```salida
False
['3', '3']
```

Una clave que debe ser única y no lo es es un **error de estructura**: detiene la carga o se envía a revisión; no se resuelve con `drop_duplicates` sin investigar.

**7. El informe de la corrida.** Al terminar, el programa debe poder decir:

```text
Bronze leídas: 9
Duplicados exactos eliminados: 1
Rechazadas: 4 (cantidad no positiva: 1, cantidad no numérica: 1, estado no permitido: 1, precio ausente: 1)
Silver: 4
Cuadre filas: OK (9 = 1 + 4 + 4)
Cuadre valor Silver-Gold: OK
```

Ese resumen (que se guarda en un log) es lo que permite explicar, en una entrevista o a un gerente, qué hizo el programa con cada fila.

Ejemplo comercial: «Faltaron 120 ventas en el reporte» se resuelve en minutos si el log dice que 120 filas se rechazaron por «cliente no existe en el catálogo»: el control convierte un misterio en un dato.

## Errores comunes

- **Controlar con `assert` en producción.**
- **Resolver duplicados de clave con `drop_duplicates` sin investigar.**
- **Convertir un valor desconocido en uno válido para que el programa «corra».**
- **No contar los rechazados** (el cuadre nunca cierra).
- **Validar solo la estructura o solo las filas.**
- **No guardar el motivo del rechazo.**
- **No comparar totales entre capas.**

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre una validación de estructura y una de fila, y qué hace el programa en cada caso?
2. ¿Qué igualdad deben cumplir las filas entre Bronze y las capas siguientes?
3. ¿Por qué usar `raise` y no `assert` para validar datos?
4. ¿Qué haces con una fila cuyo estado es `pendiente` si el contrato solo permite `entregado` y `anulado`?

<details><summary>Respuestas</summary>

1. La de estructura afecta a todo el archivo y detiene el proceso; la de fila rechaza el registro con motivo y el proceso continúa.
2. Bronze = duplicados eliminados + rechazadas + Silver.
3. Porque `assert` puede desactivarse al ejecutar Python con optimización.
4. La rechazo con motivo «estado no permitido»; no la convierto en otro estado.

</details>

## Micropráctica

Con un CSV en memoria de 8 líneas de pedidos que tú inventes (con una columna faltante opcional, un duplicado, un valor negativo, un texto en un número y un estado desconocido):

1. Escribe el contrato (columnas, claves, valores permitidos).
2. Implementa `validar_estructura` y `motivo_rechazo` para tu contrato.
3. Separa Bronze, Silver y rechazadas, y comprueba el cuadre de filas.
4. Calcula el importe Silver y el de un Gold agrupado, y comprueba que coinciden.

Cómo saber que está bien: tu cuadre de filas cierra y puedes explicar cada fila rechazada.

<details><summary>Ejemplo de resolución de la parte 3</summary>

```python
import io
import pandas as pd

texto = """id,estado,cantidad
1,entregado,2
2,entregado,-1
3,anulado,x
3,anulado,x
4,pendiente,5
5,entregado,3
"""
bronze = pd.read_csv(io.StringIO(texto), dtype=str)
sin_dup = bronze.drop_duplicates()


def motivo(f):
    if f["estado"] not in {"entregado", "anulado"}:
        return "estado"
    try:
        if int(f["cantidad"]) <= 0:
            return "cantidad <= 0"
    except ValueError:
        return "cantidad no numérica"
    return None


m = sin_dup.apply(motivo, axis=1)
print(len(bronze), len(bronze) - len(sin_dup), int(m.notna().sum()), int(m.isna().sum()))
print(len(bronze) == (len(bronze) - len(sin_dup)) + int(m.notna().sum()) + int(m.isna().sum()))
```

```salida
6 1 3 2
True
```

</details>

## Después, en los ejercicios

Estos controles son los que exige el mini-ETL (P21–P28 y la serie de [Puente](../../03_EJERCICIOS/Puente/)) y el ETL final. El capítulo 5 explica cómo diseñarlos como parte de un pipeline reproducible. Siguiente: [10.6 Errores silenciosos y cómo detectarlos](06_errores_silenciosos.md).
