# 7.1 Qué es un programa y cómo se ejecuta

> Tiempo estimado: 45 min (lectura 15 + práctica 30). No necesitas saber programar. Necesitas tener el entorno del curso (`.venv` con Python 3.12) funcionando.

## Para qué sirve

Todo lo que harás en el resto del curso (limpiar un archivo, calcular indicadores, construir un ETL) es escribir **programas**: listas de instrucciones que la computadora ejecuta exactamente como las escribes. Antes de aprender cualquier concepto de Python necesitas entender tres ideas: la computadora hace *lo que escribiste*, no lo que querías; las instrucciones se ejecutan *en orden*, de arriba hacia abajo; y cuando algo falla, Python te dice dónde y por qué, si sabes leerlo.

## Términos nuevos

- **Programa**: una lista ordenada de instrucciones escritas para que una computadora las ejecute en orden.
- **Instrucción**: una orden individual del programa. Normalmente ocupa una línea.
- **Python**: un lenguaje de programación, es decir, un conjunto de reglas para escribir instrucciones que la computadora entiende. En este curso usas la versión 3.12.
- **Intérprete**: el programa que lee tu archivo Python línea por línea y ejecuta cada instrucción. Cuando escribes `python` en la terminal, ejecutas el intérprete.
- **Script**: un archivo de texto con extensión `.py` que contiene un programa de Python.
- **Terminal**: la ventana donde escribes órdenes de texto, por ejemplo la terminal de VS Code.
- **Función**: un bloque de instrucciones con nombre que realiza una tarea. La usas escribiendo su nombre seguido de paréntesis. `print(...)` es una función que ya viene con Python.
- **Argumento**: el dato que le entregas a una función dentro de los paréntesis. En `print("Hola")`, el argumento es `"Hola"`.
- **Comentario**: texto que empieza con `#`. Python lo ignora; sirve para que los humanos entiendan el código.
- **Sintaxis**: las reglas de escritura del lenguaje (paréntesis, comillas, dos puntos). Un error de sintaxis significa que escribiste algo que Python no puede leer.
- **Traceback**: el informe de error que imprime Python cuando una instrucción falla. Dice qué línea falló y de qué tipo fue el error. Lo estudiarás con detalle en la lección 8.6; por ahora aprende a leer su **última línea**.

## Ejemplo paso a paso

**1. La primera instrucción.** `print` muestra algo en pantalla:

```python
print("Hola, distribuidora")
```

```salida
Hola, distribuidora
```

Línea por línea: `print` es la función; los paréntesis encierran su argumento; `"Hola, distribuidora"` es un **texto** (siempre entre comillas, simples o dobles). El resultado aparece debajo: sin las comillas, porque las comillas son parte de cómo se escribe el texto, no de lo que se muestra.

**2. Varias instrucciones: el orden importa.** Python ejecuta de arriba hacia abajo, una por una:

```python
print("Paso 1: abrir el archivo")
print("Paso 2: limpiar los datos")
print("Paso 3: guardar el resultado")
```

```salida
Paso 1: abrir el archivo
Paso 2: limpiar los datos
Paso 3: guardar el resultado
```

Si cambias el orden de las líneas, cambia el orden de la salida. No existe «el programa entiende lo que quise decir»: ejecuta lo escrito.

**3. Texto frente a cálculo.** Con y sin comillas es muy distinto:

```python
print("3 + 4")
print(3 + 4)
```

```salida
3 + 4
7
```

Con comillas, `"3 + 4"` es solo texto y se muestra tal cual. Sin comillas, `3 + 4` es una operación: Python la **calcula** y muestra el resultado, 7. Esta diferencia (texto o cálculo) aparecerá todo el curso.

**4. Comentarios.** Todo lo que sigue a un `#` se ignora:

```python
# Esta línea es solo una nota para mí
print(10 * 5)   # esto se calcula y se muestra
```

```salida
50
```

**5. Predice antes de ejecutar.** Este hábito vale más que cualquier truco: antes de correr un programa, escribe en papel qué crees que mostrará. Si coincide, entendiste; si no, aprendiste algo. Intenta con este:

```python
print("A")
print(2 * 3)
print("2 * 3")
print("B")
```

```salida
A
6
2 * 3
B
```

Resultado correcto: `A`, luego `6` (se calculó), luego `2 * 3` (era texto) y finalmente `B`.

**6. Cómo se ejecuta un archivo.** Hasta aquí los ejemplos son fragmentos. Un programa real vive en un archivo `.py`. Pasos:

1. Abre la carpeta del curso en VS Code.
2. Crea un archivo, por ejemplo `mi_trabajo/python/practica_1.py`, y escribe una instrucción `print(...)`.
3. Guarda el archivo (Ctrl+S).
4. En la terminal, desde la carpeta raíz del curso, ejecuta el archivo con el Python del entorno virtual:

```text
.venv\Scripts\python.exe mi_trabajo\python\practica_1.py
```

Lo que escribe `print` aparece en la terminal. Si cambias el archivo, tienes que guardarlo y volver a ejecutarlo.

**7. Tu primer error (y cómo leerlo).** Un error de sintaxis, a propósito: olvidamos cerrar las comillas.

```python
print("Hola)
```

```error
SyntaxError: unterminated string literal (detected at line 1)
```

La última línea es la importante: dice el *tipo* de error (`SyntaxError`, error de escritura) y el *motivo* (texto sin cerrar). Otro error típico es usar un nombre que no existe:

```python
print(total_ventas)
```

```error
NameError: name 'total_ventas' is not defined
```

`NameError` significa «no sé qué es `total_ventas`». Python no adivina: no hay ninguna instrucción anterior que le haya dado ese nombre. En la próxima lección aprenderás a crear nombres con valores.

**Regla de lectura de errores:** lee primero la **última línea** del mensaje; luego busca el número de línea de tu archivo que aparece más arriba. No cambies código al azar.

Ejemplo comercial: un script que imprime «Archivo leído» y «Archivo validado» antes de procesar parece trivial, pero es la base del *registro de progreso* que usarás en un ETL: ver en pantalla cuál paso se ejecutó permite saber dónde falló.

## Errores comunes

- **Olvidar cerrar comillas o paréntesis**: `SyntaxError`.
- **Escribir `Print` o `PRINT`**: Python distingue mayúsculas de minúsculas; `print` va en minúsculas.
- **Pensar que el programa corrige lo que quisiste decir**: ejecuta lo escrito.
- **Editar el archivo y no guardarlo** antes de ejecutar: ejecutas la versión vieja.
- **Ejecutar desde una carpeta distinta** de la raíz del curso: las rutas relativas a archivos fallan.
- **Copiar y pegar un ejemplo sin entender cada línea.**
- **Asustarse del mensaje de error**: la última línea casi siempre ya dice qué pasó.

## Para comprobar que entendiste

1. ¿Qué diferencia hay entre `print("5 + 2")` y `print(5 + 2)`?
2. ¿En qué orden ejecuta Python las instrucciones?
3. ¿Qué dice la última línea de un traceback?
4. ¿Para qué sirve un comentario?

<details><summary>Respuestas</summary>

1. El primero muestra el texto `5 + 2`; el segundo calcula y muestra `7`.
2. De arriba hacia abajo, una por una.
3. El tipo de error y el motivo (por ejemplo `NameError: name 'x' is not defined`).
4. Para explicar el código a quien lo lea; Python lo ignora.

</details>

<a id="micropractica"></a>

## Micropráctica

1. Escribe un script que imprima tu nombre, luego la suma 15 + 27 calculada por Python y luego el texto «Fin». Ejecútalo desde la terminal.
2. Antes de ejecutar, predice la salida de este programa y luego compruébalo:
   `print("x")`, `print(4 * 4)`, `print("4 * 4")`.
3. Provoca a propósito un `NameError` (escribe `print(mi_dato)`) y anota la última línea del error. Después provoca un `SyntaxError` olvidando un paréntesis.

Cómo saber que está bien: en la 1 ves tres líneas, la segunda es `42`; en la 2, `x`, `16`, `4 * 4`; en la 3 puedes decir con tus palabras qué significa cada tipo de error.

<details><summary>Comprobación de la primera parte</summary>

```python
print("Tu nombre aquí")
print(15 + 27)
print("Fin")
```

```salida
Tu nombre aquí
42
Fin
```

</details>

## Después, en los ejercicios

Esta lección es el punto de partida de P01–P08 en [`03_EJERCICIOS/Python/`](../../03_EJERCICIOS/Python/). Sigue con [7.2 Variables y asignación](02_variables_asignacion.md).
