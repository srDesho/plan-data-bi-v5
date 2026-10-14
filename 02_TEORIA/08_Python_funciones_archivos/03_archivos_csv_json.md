# 8.3 Archivos: rutas, CSV y JSON

> Tiempo estimado: 65 min (lectura 25 + práctica 40). Prerrequisitos: [7.5 Texto](../07_Python_basico/05_texto.md), [7.9 Diccionarios](../07_Python_basico/09_diccionarios_sets.md), [7.11 for](../07_Python_basico/11_for_while.md) y [8.1 Funciones](01_funciones_con_contrato.md).

## Para qué sirve

Los datos viven en archivos: el CSV que exporta el ERP, el JSON de una configuración, el resultado que entregas. Un ETL empieza leyendo un archivo y termina escribiendo otro. Leerlos bien (con la ruta correcta, la codificación correcta y sabiendo que todo llega como texto) evita la mitad de los errores de la primera hora.

## Términos nuevos

- **Archivo de texto**: un archivo cuyo contenido son caracteres legibles (CSV, JSON, `.py`).
- **Ruta**: la dirección de un archivo. Una ruta **absoluta** parte de la raíz del disco (`C:\...`); una **relativa** parte de la carpeta desde donde se ejecuta el programa.
- **Directorio de trabajo**: la carpeta desde la cual Python resuelve las rutas relativas. Depende de dónde abriste la terminal, no de dónde está el script.
- **`Path`** (módulo `pathlib`): un objeto para trabajar con rutas sin concatenar barras a mano. Tiene `.exists()`, `.read_text()`, `.parent`, `.name`.
- **Codificación** (*encoding*): la tabla que convierte bytes en caracteres. Para texto en español usa **UTF-8**. Algunos archivos de Excel traen una marca de inicio (BOM) y se leen con `utf-8-sig`.
- **CSV**: texto tabular donde cada línea es una fila y los campos se separan con un **delimitador** (coma, punto y coma). La primera línea suele ser el **encabezado** con los nombres de columna.
- **`with`**: la forma segura de abrir un archivo; lo **cierra** automáticamente al terminar el bloque, incluso si hay un error.
- **JSON**: formato de texto para guardar estructuras (diccionarios, listas, números, textos) de forma portable.

## Ejemplo paso a paso

Los ejemplos usan los CSV de la mini-base (`04_DATASETS/mini_base/`). Se ejecutan desde la raíz del paquete, que es el directorio de trabajo asumido.

**1. Comprobar que el archivo existe.**

```python
from pathlib import Path

ruta = Path("04_DATASETS/mini_base/tiendas.csv")
print(ruta.exists())
print(ruta.name)
print(ruta.parent)
```

```salida
True
tiendas.csv
04_DATASETS\mini_base
```

`from pathlib import Path` importa la herramienta (la lección 8.4 explica las importaciones). `Path("...")` crea un objeto ruta: `.exists()` dice si el archivo está, `.name` es el nombre y `.parent` la carpeta. Si `.exists()` es `False`, casi siempre el directorio de trabajo no es el que creías. (En Windows las rutas se muestran con barras invertidas, como en el resultado de arriba; en Linux o Mac verías barras normales.)

**2. Leer líneas de texto.**

```python
from pathlib import Path

ruta = Path("04_DATASETS/mini_base/tiendas.csv")
with ruta.open(encoding="utf-8") as f:
    linea_1 = f.readline().rstrip("\n")
    linea_2 = f.readline().rstrip("\n")
    linea_3 = f.readline().rstrip("\n")

print(linea_1)
print(linea_2)
print(linea_3)
```

```salida
tienda_id,nombre,tipo,zona,ruta,fecha_alta
1,Tienda La Palma,Tienda de barrio,Norte,R01,2025-02-10
2,Kiosco El Faro,Kiosco,Centro,R01,2025-03-01
```

`with ... as f:` abre el archivo y lo cierra al salir del bloque. `readline()` lee una línea. Aquí ves el encabezado y las dos primeras filas, todo como **texto plano**.

**3. Leer un CSV como lista de diccionarios.** `csv.DictReader` usa la primera línea como nombres de campo y entrega cada fila como diccionario:

```python
import csv
from pathlib import Path

ruta = Path("04_DATASETS/mini_base/tiendas.csv")
with ruta.open(encoding="utf-8", newline="") as f:
    filas = list(csv.DictReader(f))

print(len(filas))
print(filas[0])
print(filas[4]["zona"] == "")
```

```salida
12
{'tienda_id': '1', 'nombre': 'Tienda La Palma', 'tipo': 'Tienda de barrio', 'zona': 'Norte', 'ruta': 'R01', 'fecha_alta': '2025-02-10'}
True
```

Es exactamente la **lista de diccionarios** de la lección 7.13. Observa dos hechos importantes: **todos los valores son texto** (`'1'`, no `1`) y los campos vacíos llegan como texto vacío `''`, no como `None`. Por eso `filas[4]["zona"] == ""` es verdadero (la tienda 5 no tiene zona). `newline=""` es la forma recomendada de abrir CSV para que el módulo maneje bien los saltos de línea.

**4. Convertir tipos después de leer.**

```python
import csv
from pathlib import Path

ruta = Path("04_DATASETS/mini_base/venta_lineas.csv")
with ruta.open(encoding="utf-8", newline="") as f:
    lineas = list(csv.DictReader(f))

total_unidades = 0
for linea in lineas:
    total_unidades = total_unidades + int(linea["cantidad"])

print(len(lineas), total_unidades)
print(type(lineas[0]["cantidad"]))
```

```salida
39 364
<class 'str'>
```

Si no convirtieras con `int(...)`, `linea["cantidad"]` sería texto y la suma fallaría con `TypeError`. Las conversiones y validaciones de la lección 7.7 se aplican **después de leer**.

**5. Escribir un CSV.**

```python
import csv
from pathlib import Path

resumen = [
    {"ruta": "R01", "tiendas": 4},
    {"ruta": "R02", "tiendas": 4},
]

salida = Path("resumen_rutas.csv")
with salida.open("w", encoding="utf-8", newline="") as f:
    escritor = csv.DictWriter(f, fieldnames=["ruta", "tiendas"])
    escritor.writeheader()
    escritor.writerows(resumen)

print(salida.read_text(encoding="utf-8"))
```

```salida
ruta,tiendas
R01,4
R02,4
```

`"w"` abre para **escribir** (¡y borra el contenido anterior si el archivo existía!). `DictWriter` recibe los nombres de columna; `writeheader()` escribe el encabezado y `writerows()` las filas. En el ejemplo el archivo se crea en una carpeta temporal; en tu trabajo, verifica siempre la ruta de salida antes de escribir. **Nunca sobrescribas el archivo de origen.**

**6. JSON: guardar y leer una estructura.**

```python
import json
from pathlib import Path

config = {"fecha_corte": "2026-09-30", "rutas": ["R01", "R02"], "umbral": 0.9}

archivo = Path("config.json")
archivo.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

leido = json.loads(archivo.read_text(encoding="utf-8"))
print(leido["fecha_corte"], leido["rutas"], leido["umbral"])
print(leido == config)
```

```salida
2026-09-30 ['R01', 'R02'] 0.9
True
```

Antes de escribir en una carpeta que puede no existir, se crea con `Path(...).parent.mkdir(parents=True, exist_ok=True)` (crea las carpetas intermedias y no falla si ya existen). `json.dumps` convierte la estructura en texto JSON; `json.loads` hace el camino inverso. Las fechas **no** existen como tipo en JSON: se guardan como texto ISO (`"2026-09-30"`) y se convierten al leer. Nunca uses `eval()` para leer datos: ejecuta código arbitrario.

**7. Errores típicos de archivos.**

```python
from pathlib import Path

texto = Path("04_DATASETS/no_existe.csv").read_text(encoding="utf-8")
```

```error
FileNotFoundError: [Errno 2] No such file or directory: '04_DATASETS\\no_existe.csv'
```

`FileNotFoundError` significa que la ruta es incorrecta: comprueba el nombre, la carpeta y el directorio de trabajo. Si el archivo está abierto en Excel en Windows, escribir sobre él puede producir `PermissionError`: ciérralo y repite.

**8. La codificación y el BOM.** Un CSV exportado de Excel puede empezar con una marca invisible. Lo simulamos:

```python
import csv
from pathlib import Path

archivo = Path("exportado.csv")
archivo.write_bytes("\ufeffventa_id,estado\n1,entregado\n".encode("utf-8"))

with archivo.open(encoding="utf-8", newline="") as f:
    mal = list(csv.DictReader(f))
print(list(mal[0].keys()))

with archivo.open(encoding="utf-8-sig", newline="") as f:
    bien = list(csv.DictReader(f))
print(list(bien[0].keys()))
```

```salida
['\ufeffventa_id', 'estado']
['venta_id', 'estado']
```

Con `utf-8` la primera clave es `'\ufeffventa_id'` (¡con el carácter invisible!) y tu `fila["venta_id"]` fallaría con `KeyError` aunque el encabezado «se vea» bien. Con `utf-8-sig` la marca desaparece. Cuando una clave «correcta» da `KeyError`, sospecha del BOM.

**9. Rutas en scripts.** En un script guardado (no en estos fragmentos) la raíz del proyecto se deduce de la ubicación del archivo, para no depender del directorio de trabajo:

```py
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]      # carpeta superior a la de este script
datos = RAIZ / "04_DATASETS" / "mini_base" / "ventas.csv"
```

`__file__` es la ruta del script en ejecución, y el operador `/` une partes de una ruta. Este fragmento no se ejecuta en la comprobación automática porque `__file__` solo existe en archivos guardados.

Ejemplo comercial: el ERP exporta `ventas.csv` con coma decimal y fechas `DD/MM/AAAA`. Antes de convertir nada, abres 5 líneas con `readline()` para ver el delimitador, el encabezado y los formatos reales. Documentar lo que viste es el primer paso del ETL.

## Errores comunes

- **Rutas relativas desde una carpeta equivocada** (`FileNotFoundError`).
- **Olvidar que `csv` entrega todo como texto.**
- **Tratar el campo vacío como `None`**: llega como `''`.
- **Abrir con `"w"` el archivo de origen** y borrarlo.
- **Olvidar `newline=""`** al leer/escribir CSV.
- **No cerrar el archivo** (por eso se usa `with`).
- **Ignorar la codificación**: caracteres raros (`Ã³`) o claves con BOM.
- **Dejar el archivo de salida abierto en Excel** y recibir `PermissionError`.

## Para comprobar que entendiste

1. ¿Qué ventaja tiene `with open(...)`?
2. ¿Qué tipo tienen los valores que devuelve `csv.DictReader`?
3. ¿Para qué sirve `encoding="utf-8-sig"`?
4. ¿Qué hace abrir un archivo con `"w"`?

<details><summary>Respuestas</summary>

1. Cierra el archivo automáticamente, incluso si hay un error.
2. Texto (`str`): hay que convertir los números.
3. Para leer archivos que empiezan con la marca BOM sin que esta se pegue al primer nombre de columna.
4. Lo abre para escribir y borra su contenido anterior.

</details>

## Micropráctica

1. Lee `04_DATASETS/mini_base/articulos.csv` y muestra cuántas filas tiene y el nombre del artículo más caro (convierte el precio a `float`).
2. Cuenta cuántas tiendas tienen la zona vacía en `tiendas.csv`.
3. Escribe un CSV `categorias.csv` con dos columnas (`categoria`, `articulos`) que cuente cuántos artículos hay por categoría. Léelo de vuelta y compara.
4. Provoca un `FileNotFoundError` y explica con tus palabras la última línea.

Cómo saber que está bien: 1 → 10 filas y «Detergente 1kg»; 2 → 2 tiendas; 3 → 4 categorías con 3, 2, 2 y 3 artículos.

<details><summary>Comprobación de las partes 1 y 2</summary>

```python
import csv
from pathlib import Path

with Path("04_DATASETS/mini_base/articulos.csv").open(encoding="utf-8", newline="") as f:
    articulos = list(csv.DictReader(f))

caro = None
for a in articulos:
    if caro is None or float(a["precio"]) > float(caro["precio"]):
        caro = a
print(len(articulos), caro["nombre"])

with Path("04_DATASETS/mini_base/tiendas.csv").open(encoding="utf-8", newline="") as f:
    tiendas = list(csv.DictReader(f))

sin_zona = 0
for t in tiendas:
    if t["zona"] == "":
        sin_zona = sin_zona + 1
print(sin_zona)
```

```salida
10 Detergente 1kg
2
```

</details>

## Después, en los ejercicios

La lectura de CSV es el centro de P13, P15 y P17 en [Python](../../03_EJERCICIOS/Python/) y del paso de extracción del mini-ETL. Los CSV de `04_DATASETS/` están en UTF-8 sin marca BOM (comprobado byte a byte); `utf-8-sig` también los lee bien y te protege si un archivo nuevo viene de Excel. Lee cada `LEEME` o diccionario antes de abrir un conjunto de datos. Siguiente: [8.4 Módulos e importaciones](04_modulos_imports.md).
