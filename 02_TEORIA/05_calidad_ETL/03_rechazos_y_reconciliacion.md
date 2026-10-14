# 5.3 Rechazos, duplicados y reconciliación

> Tiempo estimado: 55 min (lectura 25 + práctica 30). Prerrequisitos: [5.2 Contrato de datos](02_contrato_de_datos.md), [9.5 Nulos y duplicados](../09_Pandas_basico/05_nulos_duplicados.md) y [10.5 Controles de calidad](../10_Pandas_transformaciones/05_controles_calidad.md).

## Para qué sirve

La 10.5 te mostró cómo implementar controles en Pandas. Aquí está el diseño: ¿qué información debe guardar un archivo de rechazos? ¿cuándo un duplicado es inofensivo y cuándo es un conflicto? ¿cómo se reconcilia dinero y no solo filas? Un ETL que no puede responder estas preguntas no se puede auditar ni defender.

## Términos nuevos

- **Archivo de rechazos**: la tabla donde cada fila rechazada conserva su identificación original, los valores originales y el motivo.
- **Múltiples causas**: una misma fila puede incumplir varias reglas a la vez; se guardan todas (en una lista o separadas por `;`).
- **Duplicado exacto**: dos filas idénticas en todos los campos. Se elimina dejando una y contando las eliminadas.
- **Conflicto de clave**: la misma clave con contenido distinto. No se resuelve automáticamente.
- **Imputación por regla**: completar un faltante usando una regla válida y documentada (por ejemplo, vendedor recuperado por una ruta con un solo vendedor). Se cuenta y se informa.
- **Reconciliación de filas**: `Bronze = duplicados + rechazadas + Silver`.
- **Reconciliación de valor**: el importe (en centavos) de Silver entregado coincide con el de Gold.
- **Centavos enteros**: representar el dinero como enteros (Bs 12,50 = 1250) para que las sumas sean exactas.

## Ejemplo paso a paso

**1. Estructura de un archivo de rechazos.** Mínimo útil: identificar la fila, mostrar el valor problemático y explicar:

| Columna | Para qué |
|---|---|
| `fila_origen` | número de línea en el archivo original (para ubicarla) |
| `id_venta` | su clave, si existe |
| `campo` | qué campo falló (`cantidad`, `fecha`...) |
| `valor_original` | exactamente lo que llegó |
| `motivo` | texto claro de la regla incumplida |

Una fila con dos problemas genera dos líneas de rechazo (o una con los motivos separados por `;`): lo importante es que el revisor sepa qué corregir. El archivo **no** contiene datos privados innecesarios.

**2. Duplicado exacto o conflicto: distinguirlos antes de eliminar.**

```python
import io
import pandas as pd

TEXTO = """id_venta,producto,cantidad,precio
V1,Agua,2,6.0
V1,Agua,2,6.0
V2,Jugo,1,9.0
V3,Agua,1,6.0
V3,Agua,5,6.0
"""
df = pd.read_csv(io.StringIO(TEXTO), dtype=str)

exactos = int(df.duplicated().sum())
sin_exactos = df.drop_duplicates()
conflictos = sin_exactos[sin_exactos.duplicated(subset=["id_venta"], keep=False)]

print("duplicados exactos:", exactos)
print("filas tras quitar exactos:", len(sin_exactos))
print("conflictos de clave:", conflictos["id_venta"].unique().tolist())
```

```salida
duplicados exactos: 1
filas tras quitar exactos: 4
conflictos de clave: ['V3']
```

V1 aparece dos veces idéntica: **duplicado exacto**, se elimina una y se cuenta. V3 aparece con cantidades distintas (1 y 5): **conflicto de clave**, y no se sabe cuál es la correcta. La regla de este curso: ante un conflicto, **se detiene el proceso (o se manda a revisión)**; no se conserva «la primera». El orden importa: primero se quitan los exactos y **después** se buscan los conflictos, porque si no, un duplicado exacto parecería un conflicto.

**3. Imputación por regla (con su condición).**

```python
import pandas as pd

ventas = pd.DataFrame({"venta": [1, 2, 3], "ruta": ["R01", "R02", "R01"], "vendedor": ["Ana", None, None]})
catalogo = pd.DataFrame({"ruta": ["R01", "R02"], "vendedor": ["Ana", "Luis"]})

assert catalogo["ruta"].is_unique, "la regla solo vale si hay un vendedor por ruta"

completo = ventas.merge(catalogo, on="ruta", how="left", suffixes=("", "_ruta"), validate="m:1")
completo["vendedor_final"] = completo["vendedor"].fillna(completo["vendedor_ruta"])
recuperados = completo["vendedor"].isna().sum()
print(completo[["venta", "ruta", "vendedor_final"]])
print("recuperados:", recuperados)
```

```salida
   venta ruta vendedor_final
0      1  R01            Ana
1      2  R02           Luis
2      3  R01            Ana
recuperados: 2
```

Los vendedores faltantes se recuperan por la ruta **solo** porque el catálogo tiene un vendedor por ruta (la primera línea del programa lo comprueba y detiene si deja de ser cierto). Se **cuenta** cuántos se recuperaron (2) y ese número va al informe. La regla es un supuesto: documentado, verificado y contado.

**4. Reconciliar dinero en centavos.** Los decimales acumulan restos; los enteros no:

```python
from decimal import Decimal

montos_texto = ["12.50", "7.25", "0.10", "0.20"]
en_centavos = [int(Decimal(m) * 100) for m in montos_texto]
print(en_centavos)
print(sum(en_centavos))
print(sum(en_centavos) / 100)

en_float = [float(m) for m in montos_texto]
print(sum(en_float))
```

```salida
[1250, 725, 10, 20]
2005
20.05
20.05
```

Se convierte cada texto con `Decimal` (exacto) y se multiplica por 100 para obtener un entero de centavos; la suma `2005` centavos es exacta. Con `float`, la suma `20.05` puede arrastrar restos diminutos en otros casos. Para el reporte, se divide entre 100 solo al final.

**5. El cuadre de valor.**

```python
silver_entregado = [1250, 725, 1000]
gold = {"R01": 1975, "R02": 1000}

print(sum(silver_entregado), sum(gold.values()))
print(sum(silver_entregado) == sum(gold.values()))
```

```salida
2975 2975
True
```

El importe de Silver entregado (2975 centavos) debe coincidir con la suma de Gold. **El número de filas correcto, por sí solo, no detecta importes multiplicados** (un merge que duplica una línea mantiene los conteos plausibles pero infla el valor). Por eso hay dos cuadres: filas y valor.

**6. El informe final de una corrida (lo que guardas).**

```text
Bronze: 5 filas
Duplicados exactos eliminados: 1
Conflictos de clave: 1  → DETENIDO (V3)
```

Si hubiera conflictos, el informe termina ahí y el proceso no publica. Si no los hay:

```text
Bronze: 5 | duplicados: 1 | rechazadas: 1 | Silver: 3  (5 = 1 + 1 + 3 ✔)
Vendedores recuperados por ruta: 2
Importe Silver entregado = Gold: 2975 centavos ✔
```

Cada línea responde una pregunta que le harán al ETL.

**7. Cuando una fila tiene más de un problema.**

```python
def motivos(fila):
    lista = []
    if not fila["kiosco"].strip():
        lista.append("kiosco ausente")
    if not fila["cantidad"].strip().isdigit():
        lista.append("cantidad no entera")
    return lista


print(motivos({"kiosco": "", "cantidad": "1.5"}))
print(motivos({"kiosco": "Luna", "cantidad": "10"}))
```

```salida
['kiosco ausente', 'cantidad no entera']
[]
```

La función devuelve **todos** los motivos (una lista), no solo el primero. Una fila sin problemas devuelve una lista vacía. Quien corrige el origen necesita saber todo lo que está mal, no solo lo primero.

Ejemplo comercial: el área comercial pregunta por qué el reporte tiene 120 ventas menos que el ERP. El archivo de rechazos responde: 118 por «cliente no existe en el catálogo» y 2 por «fecha inexistente». Con los motivos se corrige el catálogo y se recupera la diferencia.

## Errores comunes

- **Eliminar duplicados antes de distinguir exactos de conflictos.**
- **Conservar «la primera» fila ante un conflicto.**
- **Rechazos sin valor original ni motivo.**
- **Guardar solo el primer motivo.**
- **Imputar sin verificar el supuesto ni contar cuántos.**
- **Reconciliar solo filas y no valor.**
- **Sumar dinero en `float`** sin una regla de redondeo.
- **Datos privados innecesarios en los rechazos.**

## Para comprobar que entendiste

1. ¿Cuál es la diferencia entre un duplicado exacto y un conflicto de clave?
2. ¿Por qué se eliminan los exactos antes de buscar conflictos?
3. ¿Qué dos cuadres se hacen y por qué no basta uno?
4. ¿Qué debe cumplirse para recuperar el vendedor por la ruta?

<details><summary>Respuestas</summary>

1. El exacto es idéntico en todos los campos; el conflicto repite la clave con contenido distinto.
2. Porque si no, los exactos parecerían conflictos.
3. Filas (Bronze = duplicados + rechazadas + Silver) y valor (Silver = Gold); las filas pueden cuadrar aunque los importes estén multiplicados.
4. Que cada ruta tenga un solo vendedor, y que se cuente y documente la imputación.

</details>

## Micropráctica

1. Con un CSV en memoria de 8 filas que incluya un exacto, un conflicto y un faltante recuperable, aplica el orden correcto y documenta los conteos.
2. Define las columnas de tu archivo de rechazos y escribe 3 filas de ejemplo.
3. Convierte cuatro montos con coma decimal a centavos enteros y demuestra que la suma es exacta.
4. Redacta el informe final de la corrida con la ecuación de cuadre.

Cómo saber que está bien: tus conteos de la parte 1 cierran con la ecuación.

<details><summary>Ejemplo de resolución de la parte 3</summary>

```python
from decimal import Decimal

textos = ["10,25", "3,40", "0,35", "6,00"]
centavos = [int(Decimal(t.replace(",", ".")) * 100) for t in textos]
print(centavos, sum(centavos), sum(centavos) / 100)
```

```salida
[1025, 340, 35, 600] 2000 20.0
```

</details>

## Después, en los ejercicios

El mini-ETL (ME01–ME04 en [Puente](../../03_EJERCICIOS/Puente/)) y el proyecto ETL piden rechazos con motivo, ecuación de auditoría y cuadre de valor. Lee en cada enunciado qué debe detenerse y qué rechazarse. Siguiente: [5.4 Cargas repetibles, registro y reproducibilidad](04_cargas_registro_reproducibilidad.md).
