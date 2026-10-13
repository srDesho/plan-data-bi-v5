# Funciones, errores y archivos reproducibles

Una función encapsula una transformación. Recibe parámetros, hace un trabajo y devuelve un valor con `return`. Imprimir no equivale a devolver: una función que solo imprime no sirve para combinar su resultado con otra. Una función pequeña se prueba con entradas conocidas antes de usarla en miles de filas.

```python
def cumplimiento(venta, meta):
    if meta <= 0:
        return None
    return 100 * venta / meta

assert cumplimiento(80,100) == 80
assert cumplimiento(0,0) is None
```

Una función debe tener un contrato: tipos de entrada, condiciones válidas y significado de salida. Para precios, explica qué formatos admite y cuándo falla. No rellenes un precio ilegible con cero, porque eso cambia las ventas. Evita funciones que limpien, escriban archivos y envíen mensajes a la vez: separar extracción, transformación y carga permite aislar fallos.

`try/except` captura errores esperados. Captura `ValueError` al convertir un importe, agrega el motivo a un registro rechazado y continúa si la regla lo permite. Un `except: pass` oculta fallos y puede producir informes incompletos. Errores de estructura (columna obligatoria ausente, catálogo con claves duplicadas) deben detener el proceso.

```python
from pathlib import Path
import csv
archivo = Path('04_DATASETS/distribuidora/clientes.csv')
with archivo.open(encoding='utf-8-sig',newline='') as f:
    clientes = list(csv.DictReader(f))
assert len(clientes) == 120
```

Ejecuta desde la raíz del paquete. `Path` evita concatenar barras manualmente y ofrece `.exists()`, `.parent` y `.mkdir()`. En un script distribuible, resuelve la raíz desde `__file__`; en un notebook usa la celda de localización incluida. El directorio actual depende de dónde abriste la terminal y no siempre coincide con el archivo.

CSV es texto tabular: especifica separador, codificación y tipos. JSON guarda objetos/listas estructurados; `json.load` lee y `json.dump` escribe. Fechas en JSON deben serializarse a texto ISO. No evalúes texto con `eval()` para leer datos.

## Pruebas y rutina de trabajo

Prueba una entrada normal, un límite y una inválida. Para `recencia`, prueba última compra igual al corte (0), cinco días antes (5) y fecha posterior (error). Para cantidad, 3 y 3.0 pueden ser válidos; 3.7 debe rechazarse, no truncarse a 3.

Escribe una función, ejecuta sus tres pruebas, añade un caso empresarial y recién intégrala. El bloque `if __name__ == '__main__':` separa ejecución de importación. Un logger registra etapas y conteos; no debe contener datos privados. Un script reproducible recibe rutas/configuración, no depende de celdas ejecutadas hace una semana.

Práctica P09–P16 y P29–P30. Método obligatorio: intento 10 min → comprobar → depurar 10 min → pista → solución con explicación propia. Fuente: Python, funciones, errores, pathlib, csv y json.
