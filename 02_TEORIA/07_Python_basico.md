# Capítulo 7 — Python: construir el razonamiento antes de Pandas

Este capítulo parte de cero: qué es un programa, qué es una variable y cómo se ejecuta una línea. Avanza pieza por pieza (texto, números, listas, diccionarios, condiciones, bucles) y solo al final junta todo en la tarea típica de un ETL: **recorrer registros, acumular y separar lo inválido**. Cada lección tiene ejemplos que se ejecutan con Python 3.12 y cuya salida está comprobada.

**Tiempo total estimado de primera vez:** unas 12 h 32 min si lees y practicas todas las lecciones (13). No se hace de una vez: la carga se reparte con los ejercicios P01–P08. La columna «Tipo» indica la clase de cada lección (**NÚCLEO**, con la jornada en que se lee en la ruta BASE, **COMPLEMENTARIA** o **EMPLEO**); el detalle está en [`RUTAS.md`](../01_PLAN_DIARIO/RUTAS.md).

**Antes de empezar:** nada de Python. Necesitas el entorno del curso (`.venv` con Python 3.12) y VS Code.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 7.1 | [Qué es un programa](07_Python_basico/01_que_es_un_programa.md) | instrucciones, `print`, ejecutar un archivo, leer un error | NÚCLEO · D01 | 45 min |
| 7.2 | [Variables y asignación](07_Python_basico/02_variables_asignacion.md) | nombres, `=`, reasignar, tabla de seguimiento | NÚCLEO · D01 | 45 min |
| 7.3 | [Tipos de datos y aritmética](07_Python_basico/03_tipos_aritmetica.md) | int, float, str, bool, None; `//`, `%`; decimales y redondeo | NÚCLEO · D02 | 50 min |
| 7.4 | [Tu primera función corta](07_Python_basico/04_primera_funcion.md) | `def`, parámetros, argumentos, `return`, `assert` | NÚCLEO · D01–D02 | 63 min |
| 7.5 | [Texto](07_Python_basico/05_texto.md) | índices, rebanadas, métodos, f-strings, montos como texto | NÚCLEO · D02 | 72 min |
| 7.6 | [Booleanos, comparaciones y None](07_Python_basico/06_booleanos_comparaciones_none.md) | `==` frente a `=`, `and/or/not`, `None` | NÚCLEO · D02 | 50 min |
| 7.7 | [Conversiones y primeros errores de valor](07_Python_basico/07_conversiones.md) | `int()`, `float()`, `ValueError`, validar | NÚCLEO · D08 | 70 min |
| 7.8 | [Listas y tuplas](07_Python_basico/08_listas_tuplas.md) | índices, rebanadas, mutabilidad, alias | NÚCLEO · D03 | 55 min |
| 7.9 | [Diccionarios y conjuntos](07_Python_basico/09_diccionarios_sets.md) | claves, `get`, `KeyError`, sets | NÚCLEO · D03 | 55 min |
| 7.10 | [Condicionales](07_Python_basico/10_condicionales.md) | `if/elif/else`, casos límite, el caso desconocido | NÚCLEO · D02–D04 | 57 min |
| 7.11 | [Repetir: for y while](07_Python_basico/11_for_while.md) | iteración, `range`, `enumerate`, `break` | NÚCLEO · D04 | 55 min |
| 7.12 | [Acumuladores y patrones de recorrido](07_Python_basico/12_acumuladores.md) | sumar, contar, máximo, filtrar, caso vacío, lista por comprensión | NÚCLEO · D04 | 70 min |
| 7.13 | [Recorrer registros](07_Python_basico/13_registros_listas_de_diccionarios.md) | lista de diccionarios, agrupar, válidos y rechazados | NÚCLEO · D05 | 65 min |

## Cómo estudiar este capítulo

1. **Predice antes de ejecutar**: escribe en papel qué mostrará el código; después ejecútalo.
2. **Escribe tú el código**, no lo copies. Cambia un valor y vuelve a predecir.
3. Para cada bucle, haz la **tabla de seguimiento** de tres iteraciones.
4. Haz la micropráctica sin mirar la comprobación; después compara.
5. Cuando algo falle, lee la **última línea** del error primero.

## Ejercicios autónomos de este capítulo

P01–P08 en [`03_EJERCICIOS/Python/`](../03_EJERCICIOS/Python/). Las microprácticas de las lecciones son **práctica guiada**: no tienen corrector ni cuentan en el progreso. Los ejercicios P01–P30 son los evaluables, con corrector. La clase UAGRM 1 ([`UAGRM/`](UAGRM/LEEME.md)) complementa estos apuntes; las soluciones no se abren durante el intento. Guarda un script propio y explica por qué escogiste lista, diccionario o set en cada caso.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 8 — Funciones, errores y archivos](08_Python_funciones_archivos.md).
