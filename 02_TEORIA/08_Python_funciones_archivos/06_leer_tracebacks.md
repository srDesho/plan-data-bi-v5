# 8.6 Leer un traceback

> Tiempo estimado: 45 min (lectura 20 + práctica 25). Prerrequisitos: [7.1 Qué es un programa](../07_Python_basico/01_que_es_un_programa.md), [8.1 Funciones](01_funciones_con_contrato.md) y [8.5 Excepciones](05_excepciones.md).

## Para qué sirve

Cuando un programa falla, Python no dice «algo salió mal»: entrega un informe preciso de dónde y por qué. Quien sabe leerlo resuelve en minutos lo que otros tardan una hora adivinando. Esta lección te da el procedimiento para leer un traceback completo, incluso cuando el error ocurre varias funciones adentro.

## Términos nuevos

- **Traceback** (ya visto en 7.1): el informe que imprime Python al ocurrir una excepción no atendida.
- **Pila de llamadas** (*call stack*): la lista de funciones que estaban ejecutándose, una dentro de otra, cuando ocurrió el error.
- **Marco** (*frame*): cada línea «File ..., line N, in funcion» del traceback; representa una función de la pila.
- **Línea de error**: la última línea del traceback, con el tipo de excepción y su mensaje.
- **Causa raíz**: el lugar donde nació el problema (normalmente un dato malo o una condición no prevista), que puede estar lejos de la línea donde el programa explotó.
- **Reproducir**: lograr que el error ocurra de forma repetible con el menor ejemplo posible.

## Ejemplo paso a paso

**1. Un traceback completo.** Un programa de tres funciones anidadas que falla. (Para ver el informe dentro de esta lección lo capturamos con el módulo `traceback`; en la terminal lo verás sin ese paso.)

```python
import traceback


def leer_monto(fila):
    return fila["monto"]


def importe_de_fila(fila):
    return leer_monto(fila) * fila["cantidad"]


def total(filas):
    suma = 0
    for fila in filas:
        suma = suma + importe_de_fila(fila)
    return suma


try:
    print(total([{"monto": 5, "cantidad": 2}, {"cantidad": 3}]))
except Exception:
    print(traceback.format_exc())
```

```salida
Traceback (most recent call last):
  File "<leccion>", line 20, in <module>
  File "<leccion>", line 15, in total
  File "<leccion>", line 9, in importe_de_fila
  File "<leccion>", line 5, in leer_monto
KeyError: 'monto'
```

En tu terminal, cada marco `File ...` aparece con la ruta real de tu archivo y, debajo, el texto de la línea que se estaba ejecutando; aquí solo ves el nombre `<leccion>` y los números de línea.

**Cómo leerlo, de abajo hacia arriba:**

1. **Última línea**: `KeyError: 'monto'`. Se pidió la clave `'monto'` y no existe en el diccionario.
2. **La línea anterior** (`return fila["monto"]`, dentro de `leer_monto`) es **dónde explotó**: en esa función se pidió la clave.
3. **Los marcos de arriba** muestran quién llamó a quién: `total` llamó a `importe_de_fila`, que llamó a `leer_monto`. Es el camino que recorrió el programa.
4. **El marco más arriba** (`in <module>`) es la llamada original, la que escribiste al final.

Lo difícil: el error *explotó* en `leer_monto`, pero la **causa raíz** está en los datos: la segunda fila no tiene `monto`. Arreglar `leer_monto` no sirve; hay que decidir qué hacer con una fila incompleta (rechazarla, o corregir el origen). La pregunta correcta no es «¿cómo evito el error?» sino «¿qué fila lo provocó y por qué le falta el campo?». Para averiguarlo, imprime la fila justo antes de la línea que falla.

**2. El procedimiento de cinco pasos.**

1. **Lee la última línea**: tipo de error y mensaje.
2. **Busca la última línea que sea de TU archivo** (no de módulos de Python) en el traceback. Ahí empieza tu investigación.
3. **Formula una pregunta concreta**: «¿qué valor tiene esa variable en ese momento?».
4. **Compruébalo**: imprime la variable o usa un `assert`; no cambies código todavía.
5. **Cambia una sola cosa** y vuelve a ejecutar.

**3. Los errores más frecuentes y qué preguntan.**

| Tipo de error | Significa | Primera pregunta |
|---|---|---|
| `NameError` | un nombre que Python no conoce | ¿lo escribí distinto o lo usé antes de crearlo? |
| `TypeError` | operación entre tipos incompatibles | ¿qué tipo tiene cada valor? (`type(x)`) |
| `ValueError` | tipo correcto, valor inválido | ¿qué texto exacto llegó? |
| `KeyError` | clave inexistente en un diccionario | ¿qué claves tiene realmente? (`fila.keys()`) |
| `IndexError` | posición fuera de la lista | ¿cuántos elementos hay? (`len(lista)`) |
| `ZeroDivisionError` | división entre cero | ¿cuándo el denominador es 0? |
| `FileNotFoundError` | la ruta no existe | ¿qué ruta resolvió Python? ¿desde qué carpeta ejecuto? |
| `AttributeError` | el objeto no tiene ese método | ¿es del tipo que creía? (por ejemplo `None`) |
| `IndentationError` / `SyntaxError` | escritura inválida | ¿falta un `:`, un paréntesis o una sangría? |

**4. Un `AttributeError` con `None`.** Muy frecuente cuando una función devuelve `None`:

```python
def buscar_zona(codigo):
    zonas = {"R01": "Norte", "R02": "Centro"}
    zonas.get(codigo)


zona = buscar_zona("R01")
print(zona.upper())
```

```error
AttributeError: 'NoneType' object has no attribute 'upper'
```

El error está en `zona.upper()`, pero la causa raíz está en `buscar_zona`: **olvidó el `return`**, así que devolvió `None`. El mensaje lo dice: `'NoneType' object` quiere decir que `zona` era `None`. Al leer `NoneType`, busca qué función olvidó devolver o devolvió «sin dato».

**5. Reducir hasta lo mínimo.** Si el error aparece en un archivo de 10 000 filas, no lo analices con las 10 000: encuentra la fila que lo provoca y trabaja con ella.

```python
filas = [{"monto": "10"}, {"monto": "x"}, {"monto": "30"}]

for numero, fila in enumerate(filas, start=1):
    try:
        float(fila["monto"])
    except ValueError:
        print("la fila", numero, "tiene un monto inválido:", fila)
```

```salida
la fila 2 tiene un monto inválido: {'monto': 'x'}
```

En lugar de dejar que el programa muera, este recorrido **localiza** la fila 2. Con esa fila aislada ya puedes preguntarte por qué tiene `x`. Esta técnica (reducir el problema al caso más pequeño que lo reproduce) es la más poderosa para depurar.

Ejemplo comercial: «Mi ETL falló en la fila 8 421» es información valiosa si la imprimes. Un log que dice `fila 8421: monto 'N/A' no numérico` ahorra horas.

## Errores comunes

- **Leer el traceback desde arriba** en lugar de empezar por la última línea.
- **Cambiar código antes de entender el error.**
- **Culpar a la línea donde explotó** cuando la causa está en el dato o en una función anterior.
- **Pegar el error en una IA y copiar la solución** sin entender qué pasó (el objetivo del curso es poder explicarlo).
- **Cambiar varias cosas a la vez.**
- **No reducir el problema** y trabajar con todo el archivo.
- **Ignorar el mensaje** (`'NoneType' object has no attribute...` ya te dice que hay un `None`).

## Para comprobar que entendiste

1. ¿Qué línea del traceback lees primero?
2. En el ejemplo 1, ¿por qué arreglar `leer_monto` no resuelve el problema?
3. ¿Qué significa `'NoneType' object has no attribute 'upper'`?
4. ¿Qué haces antes de cambiar código?

<details><summary>Respuestas</summary>

1. La última: el tipo de error y el mensaje.
2. Porque la causa raíz es una fila de datos incompleta, no la función.
3. Que la variable valía `None` cuando se le pidió `.upper()`.
4. Formulo una pregunta concreta y compruebo el valor de la variable (imprimiendo o con un `assert`).

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe un programa de dos funciones que falle con `ZeroDivisionError`. Léelo con el procedimiento de cinco pasos y anota: la última línea, la línea de tu archivo y la causa raíz.
2. Provoca un `IndexError` con una lista de 3 elementos y anota qué índices son válidos.
3. Dada una lista de diccionarios donde una fila no tiene la clave `ruta`, escribe el recorrido que **localiza** la fila sin detener el programa.

Cómo saber que está bien: en la 1 puedes decir cuál valor era cero y dónde se originó; en la 2, los índices válidos son 0, 1 y 2.

<details><summary>Comprobación de la parte 3</summary>

```python
filas = [{"ruta": "R01"}, {"nombre": "sin ruta"}, {"ruta": "R03"}]

for numero, fila in enumerate(filas, start=1):
    if "ruta" not in fila:
        print("fila", numero, "sin ruta:", fila)
```

```salida
fila 2 sin ruta: {'nombre': 'sin ruta'}
```

</details>

## Después, en los ejercicios

Los tres ejercicios de depuración DB01–DB03 ([`03_EJERCICIOS/Depuracion/`](../../03_EJERCICIOS/Depuracion/)) y las pistas de todos los P usan esta lectura. El [capítulo 19](../19_Puente_Python_a_ETL.md) (§1) la aplica a un caso completo. Siguiente: [8.7 Pruebas con assert y depuración paso a paso](07_pruebas_y_depuracion.md).
