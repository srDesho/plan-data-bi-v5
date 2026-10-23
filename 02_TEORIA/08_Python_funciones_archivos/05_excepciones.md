# 8.5 Excepciones: try, except y raise

> Tiempo estimado: 70 min (lectura 25 + práctica 45). Prerrequisitos: [7.7 Conversiones](../07_Python_basico/07_conversiones.md) y [8.1 Funciones con contrato](01_funciones_con_contrato.md).

## Para qué sirve

Un archivo de 10 000 filas tendrá filas malas. Si el programa se detiene en la primera, no avanzas; si las ignora en silencio, tus totales quedan equivocados sin que lo sepas. Las excepciones te permiten **atrapar** los errores esperados, **registrar** cuáles fueron y **decidir** si seguir o detener el proceso. Es el mecanismo de los «registros rechazados» de un ETL.

## Términos nuevos

- **Excepción** (ya vista en 7.7): un error en tiempo de ejecución que detiene el programa si nadie lo atiende.
- **`try`**: el bloque donde pones el código que podría fallar.
- **`except`**: el bloque que se ejecuta si ocurre la excepción indicada. Se escribe `except TipoDeError:`.
- **`else`** (de `try`): el bloque que se ejecuta solo si **no** hubo excepción.
- **`finally`**: el bloque que se ejecuta **siempre**, haya o no error (por ejemplo, para cerrar una conexión).
- **`raise`**: la instrucción para **lanzar** una excepción tú mismo: `raise ValueError("mensaje")`.
- **Error esperado**: un fallo previsible por la naturaleza de los datos (un monto con texto). Se atrapa y se registra.
- **Error de estructura**: un fallo que invalida todo el proceso (falta una columna obligatoria, clave duplicada en un catálogo). Debe **detener** la carga.
- **Registro rechazado**: una fila que no pasó la validación, guardada aparte con el motivo.

## Ejemplo paso a paso

**1. Sin protección el programa se detiene.**

```python
montos = ["120", "abc", "80"]
total = 0
for texto in montos:
    total = total + float(texto)
print(total)
```

```error
ValueError: could not convert string to float: 'abc'
```

El programa murió en el segundo valor y el tercero ni se miró.

**2. `try/except` para un error esperado.**

```python
montos = ["120", "abc", "80"]
total = 0
rechazados = []

for texto in montos:
    try:
        valor = float(texto)
    except ValueError:
        rechazados.append(texto)
    else:
        total = total + valor

print(total)
print(rechazados)
```

```salida
200.0
['abc']
```

Cómo se ejecuta cada iteración:

1. Python intenta `float(texto)` dentro del `try`.
2. Si funciona, salta al `else` y suma el valor.
3. Si falla con `ValueError`, ejecuta el `except` y guarda el texto en la lista de rechazados.

Resultado: se suman 120 y 80 (200.0) y queda registrado que `'abc'` no sirvió. **El control**: 2 aceptados + 1 rechazado = 3 de entrada.

**3. Captura el error específico, nunca todos.**

```python
def a_float(texto):
    try:
        return float(texto)
    except ValueError:
        return None


print(a_float("8.5"), a_float("x"))
```

```salida
8.5 None
```

`except ValueError` atrapa **solo** ese tipo. Otras excepciones (por ejemplo `TypeError` si `texto` fuera `None`) siguen su camino y te avisan. Compara con el anti-patrón:

```py
try:
    valor = float(texto)
except:        # NO hagas esto
    pass
```

Un `except:` sin tipo atrapa **todo** (incluso errores de programación como un `NameError`) y `pass` no hace nada: el error desaparece sin dejar rastro. Los informes salen incompletos y nadie sabe por qué. **No uses `except: pass`.**

**4. Leer el mensaje: `as e`.**

```python
try:
    valor = int("12.5")
except ValueError as e:
    print("No se pudo convertir:", e)
```

```salida
No se pudo convertir: invalid literal for int() with base 10: '12.5'
```

`as e` guarda la excepción en la variable `e`; imprimirla muestra el mensaje original de Python, útil para el registro de rechazados.

**5. Lanzar tu propio error con `raise`.** Para reglas de negocio que Python no conoce:

```python
def validar_cantidad(texto):
    cantidad = int(texto)
    if cantidad <= 0:
        raise ValueError(f"la cantidad debe ser positiva, llegó {cantidad}")
    return cantidad


try:
    print(validar_cantidad("5"))
    print(validar_cantidad("-3"))
except ValueError as e:
    print("Rechazada:", e)
```

```salida
5
Rechazada: la cantidad debe ser positiva, llegó -3
```

`raise ValueError("mensaje")` detiene la función en ese punto y propaga el error con tu mensaje. Quien llama decide si lo atrapa (como arriba) o deja que el programa se detenga.

**6. Dos tipos de problemas, dos respuestas.**

```python
def procesar(filas, columnas_obligatorias):
    if "monto" not in columnas_obligatorias:
        raise KeyError("falta la columna obligatoria 'monto'")
    validas, rechazadas = [], []
    for fila in filas:
        try:
            validas.append(float(fila["monto"]))
        except (ValueError, KeyError) as e:
            rechazadas.append((fila, str(e)))
    return validas, rechazadas


validas, rechazadas = procesar([{"monto": "10"}, {"monto": "x"}, {}], ["monto"])
print(validas)
print(len(rechazadas))
```

```salida
[10.0]
2
```

Un fallo en una **fila** (monto ilegible, campo ausente) se atrapa y se registra: el proceso sigue. Un fallo de **estructura** (falta una columna obligatoria en todo el archivo) se lanza con `raise` y debe **detener** la carga: seguir sería procesar basura. `except (ValueError, KeyError)` atrapa cualquiera de los dos tipos.

**7. `finally`: lo que ocurre siempre.**

```python
def leer_con_aviso(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return f.readline()
    except FileNotFoundError:
        return None
    finally:
        print("intento de lectura terminado")


print(leer_con_aviso("no_existe.txt"))
```

```salida
intento de lectura terminado
None
```

El `finally` se ejecutó aunque el archivo no existía. Lo usarás para cerrar conexiones (como la de SQLite) pase lo que pase.

**8. `assert` frente a `raise`.** `assert` es para **tus** suposiciones al programar (pruebas, controles internos); `raise` es para **datos** que no cumplen una regla. Un dato inválido nunca debe controlarse con `assert`, porque los `assert` pueden desactivarse al ejecutar Python con optimización.

Ejemplo comercial: un ETL lee 10 000 filas. 9 940 pasan, 60 se rechazan con motivo («monto no numérico», «fecha futura»). El log final dice `leídas=10000 válidas=9940 rechazadas=60` y la suma cuadra. Si faltara la columna `fecha`, el proceso se detiene inmediatamente con un mensaje claro.

<a id="contrato-decimal"></a>

## Traducir errores internos al contrato de la función

Una función puede prometer `ValueError` para cualquier texto inválido aunque internamente utilice `Decimal`. Su constructor lanza **`InvalidOperation`** ante texto no convertible. Capturar únicamente `ValueError` no lo intercepta. La traducción mantiene estable el contrato para quien llama; `raise ... from error` conserva además la causa original en el traceback.

El ejemplo usa temperaturas, un dominio distinto del ejercicio de precios. Predice las salidas antes de ejecutarlo:

```python
from decimal import Decimal, InvalidOperation

def temperatura_finita(texto):
    try:
        valor = Decimal(texto.strip())
    except InvalidOperation as error:
        raise ValueError("temperatura no convertible") from error
    if not valor.is_finite():
        raise ValueError("temperatura no finita")
    return valor

for entrada in ["18.5", "ayer", "NaN", "Infinity"]:
    try:
        print(temperatura_finita(entrada))
    except ValueError as error:
        print(type(error).__name__, str(error))
```

```salida
18.5
ValueError temperatura no convertible
ValueError temperatura no finita
ValueError temperatura no finita
```

Orden: convertir capturando el error específico → comprobar finitud → aplicar la regla de negocio → devolver. Si el contrato exige un entero, comprueba que no haya fracción antes de convertir. No captures excepciones ajenas al contrato para ocultar errores de programación.

## Errores comunes

- **`except:` sin tipo, o `except Exception: pass`.**
- **Poner demasiado código dentro del `try`**: no sabes cuál línea falló. Solo la línea que puede fallar.
- **Atrapar un error y no registrar nada.**
- **Atrapar errores de estructura y seguir**.
- **Usar `assert` para validar datos.**
- **Olvidar el tipo concreto** (`ValueError` frente a `TypeError`).
- **No comprobar que aceptados + rechazados = entrada.**

## Para comprobar que entendiste

1. ¿Cuándo se ejecuta el bloque `else` de un `try`?
2. ¿Por qué `except: pass` es peligroso?
3. ¿Cuándo lanzas una excepción con `raise`?
4. ¿Qué diferencia hay entre un error de fila y uno de estructura?

<details><summary>Respuestas</summary>

1. Solo si el `try` terminó sin excepción.
2. Atrapa todos los errores y los oculta, produciendo resultados incompletos sin aviso.
3. Cuando un dato o una situación viola una regla y quien llama debe enterarse.
4. El de fila se registra y el proceso sigue; el de estructura detiene el proceso.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Dada la lista `["15", "", "7", "dos", "30"]`, suma los valores válidos, guarda los inválidos junto a su motivo y comprueba que aceptados + rechazados = 5.
2. Escribe `def porcentaje_seguro(parte, total)` que lance `ValueError` si `total` es 0 o negativo, y pruébala atrapando el error.
3. Explica con tus palabras por qué un `try` debe envolver solo la línea que puede fallar.
4. Amplía tu registro de errores del apartado 1 con una comprobación separada de conversión `Decimal`: predice y registra tipo y causa para `"7.25"`, `"vacío"`, `"nan"` y `"-Infinity"`. Haz que la interfaz traduzca el error de conversión a `ValueError` y rechace los valores no finitos. Comprueba que el dato válido conserva sus decimales; justifica por qué no has sustituido los inválidos por cero. Cierra este apartado antes de intentar P09/P11. Conserva los tres apartados originales.

<details><summary>Control del apartado 4, después del intento</summary>

Solo la primera entrada es válida. La segunda debe llegar al llamador como `ValueError` con una causa `InvalidOperation`; las dos últimas deben rechazarse por no finitas. No se exige la función de precios del ejercicio ni se proporciona su solución.

</details>

Cómo saber que está bien: en la 1 el total es 52.0 con 3 aceptados y 2 rechazados.

<details><summary>Comprobación de la parte 1</summary>

```python
entradas = ["15", "", "7", "dos", "30"]
total = 0
rechazados = []

for texto in entradas:
    try:
        total = total + float(texto)
    except ValueError as e:
        rechazados.append((texto, str(e)))

print(total, len(entradas) - len(rechazados), len(rechazados))
```

```salida
52.0 3 2
```

</details>

## Después, en los ejercicios

Los ejercicios P09, P11 y P13–P16 de [Python](../../03_EJERCICIOS/Python/) y el mini-ETL piden separar válidos de rechazados con su motivo. Lee en el enunciado qué debe hacerse con cada caso inválido (devolver `None`, lanzar un error o rechazarlo). Siguiente: [8.6 Leer un traceback](06_leer_tracebacks.md).
