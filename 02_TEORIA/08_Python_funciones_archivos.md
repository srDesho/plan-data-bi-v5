# Capítulo 8 — Funciones, errores y archivos reproducibles

Aquí conviertes lo que aprendiste en el capítulo 7 en programas confiables: funciones con contrato, lectura y escritura de archivos reales, módulos reutilizables, manejo de errores esperados, lectura de tracebacks y un método de depuración. Es el puente directo hacia el mini-ETL y el ETL final. Los ejemplos se ejecutan con Python 3.12 y su salida está comprobada.

**Tiempo total estimado de primera vez:** unas 6 h 10 min (7 lecciones). Se reparte con los ejercicios P09–P16 y P29–P30.

**Antes de empezar:** el [capítulo 7](07_Python_basico.md) completo, sobre todo funciones (7.4), conversiones (7.7), diccionarios (7.9) y registros (7.13).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 8.1 | [Funciones con contrato](08_Python_funciones_archivos/01_funciones_con_contrato.md) | docstring, valores por defecto, `None` como señal, devolver varios valores, funciones puras | núcleo · D08 | 55 min |
| 8.2 | [Ámbito y efectos secundarios](08_Python_funciones_archivos/02_ambito_efectos.md) | variables locales, alias de listas, por qué no usar `global` | refuerzo | 40 min |
| 8.3 | [Archivos: rutas, CSV y JSON](08_Python_funciones_archivos/03_archivos_csv_json.md) | `Path`, `with`, `csv`, `json`, codificación, BOM | núcleo · D10 | 65 min |
| 8.4 | [Módulos e importaciones](08_Python_funciones_archivos/04_modulos_imports.md) | `import`, `datetime`, tu propio módulo, `__main__`, versiones | núcleo · D10 | 55 min |
| 8.5 | [Excepciones](08_Python_funciones_archivos/05_excepciones.md) | `try/except/else/finally`, `raise`, errores de fila y de estructura | núcleo · D09 | 55 min |
| 8.6 | [Leer un traceback](08_Python_funciones_archivos/06_leer_tracebacks.md) | pila de llamadas, causa raíz, reducir el problema | refuerzo | 45 min |
| 8.7 | [Pruebas con assert y depuración](08_Python_funciones_archivos/07_pruebas_y_depuracion.md) | casos normal/límite/inválido, método de depuración, rutina de trabajo | refuerzo | 55 min |

## Ideas centrales

- Una función tiene un **contrato** y se prueba con un caso normal, uno límite y uno inválido.
- `print` muestra; `return` entrega. Los correctores miran lo que devuelves.
- No rellenes un dato ilegible con cero: cambia las ventas. Recházalo con su motivo.
- Un error de **fila** se atrapa y se registra; un error de **estructura** detiene el proceso.
- Un script reproducible recibe rutas y configuración; no depende de celdas ejecutadas hace una semana.
- Separa extracción, transformación y carga: así aíslas fallos.

## Ejercicios autónomos de este capítulo

P09–P16 y P29–P30 en [`03_EJERCICIOS/Python/`](../03_EJERCICIOS/Python/). Método obligatorio: intento 10 min → comprobar → depurar 10 min → pista → solución con explicación propia. Las microprácticas son práctica guiada y no tienen corrector; los P09–P16 sí. Para leer errores: [DB01–DB03](../03_EJERCICIOS/Depuracion/) y el [capítulo 19](19_Puente_Python_a_ETL.md).

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 9 — Pandas básico](09_Pandas_basico.md).
