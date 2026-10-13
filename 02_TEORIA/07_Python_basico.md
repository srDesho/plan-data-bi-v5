# Python: construir el razonamiento antes de Pandas

Un programa transforma entradas en salidas mediante pasos explícitos. Escribe primero un ejemplo a mano: dos líneas de 3×10 y 2×20 suman 70 Bs. Después traduce los pasos. La computadora ejecuta lo escrito, no la intención. Predecir el resultado antes de ejecutar es parte de la práctica.

Una variable enlaza un nombre con un valor. `cantidad=3` no crea una fórmula que cambie sola como en Excel. `int` representa enteros, `float` aproximaciones decimales, `str` texto, `bool` verdadero/falso y `None` ausencia. `"3"*2` produce `"33"`; `3*2` produce 6. Convertir texto con `int()` exige un formato válido.

```python
cantidad = 3
precio = 10.0
total = cantidad * precio
print(f"Venta: {total:.2f} Bs")
```

Los textos tienen métodos: `strip()` elimina espacios en extremos, `upper()` cambia mayúsculas y `replace()` sustituye contenido. No son operaciones mágicas de limpieza: quitar comas de `11,50` da `1150`, no `11.50`. Conoce el formato antes de convertir.

Una lista es una secuencia mutable: `ventas=[100,200,300]`. Se indexa desde cero. Una tupla agrupa valores y no permite reasignar sus posiciones. Un diccionario relaciona claves y valores: `cliente={'id':1,'ruta':'R01'}`. Un set conserva elementos únicos y permite comprobar pertenencia. El orden de un set no debe utilizarse como orden del informe.

```python
lineas = [{'cantidad':3,'precio':10}, {'cantidad':2,'precio':20}]
total = 0
for linea in lineas:
    total += linea['cantidad'] * linea['precio']
assert total == 70
```

`for` recorre elementos; no necesita inventar índices si solo quieres sus valores. La sangría define qué instrucciones pertenecen al bloque. `if/elif/else` selecciona una rama. Usa `==` para comparar y `=` para asignar. `and`, `or` y `not` combinan condiciones; distingue `None` de cero, porque ambos pueden evaluarse como falsos en un if.

Para sumar solo entregados comprueba `linea['estado']=='entregado'` dentro del bucle. Haz tres casos: entregado, anulado y estado inválido. El tercero debe provocar revisión; no lo conviertas silenciosamente en entregado.

## Tu primera función corta

Una función agrupa pasos bajo un nombre. `def` la define; los parámetros reciben las entradas y `return` devuelve el resultado.

```python
def importe(cantidad, precio):
    return cantidad * precio

assert importe(3, 10) == 30
```

Puedes empezar P01 como un script de variables y después envolver el cálculo en esta firma. No copies el ejemplo para todas las tareas: explica qué entra, qué sale y prueba un precio distinto. El capítulo 08 desarrolla contratos, errores y archivos.

## Depuración de principiante

Lee la última línea del traceback: tipo de error y mensaje. Luego encuentra la línea de tu archivo. `NameError` suele indicar un nombre no definido; `TypeError`, tipos incompatibles; `KeyError`, clave ausente; `ValueError`, conversión inválida. Imprime una variable pequeña y su `type()`. No imprimas miles de filas esperando descubrir algo.

Cuando un bucle suma de más, escribe el acumulador después de cada iteración en un ejemplo de tres filas. Cuando una condición filtra de menos, prueba sus límites. No cambies cinco cosas al mismo tiempo.

Práctica P01–P08. Guarda un script propio y explica por qué escogiste lista, diccionario o set. La clase UAGRM 1 complementa estos apuntes; las soluciones no se abren durante el intento. Fuente: tutorial oficial Python, tipos, control de flujo y estructuras de datos.
