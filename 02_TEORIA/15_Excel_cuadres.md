# Capítulo 15 — Excel como segundo camino de validación

Excel sirve para **reconciliar** un resultado y comunicarlo, siempre que controles tipos y granularidad. Este capítulo parte de cero: importar un CSV sin que Excel lo interprete mal, entender la diferencia entre valor y formato, usar las fórmulas de condición, suma y búsqueda que permiten cuadrar contra SQL o Python, construir tablas dinámicas y diagnosticar una discrepancia entre herramientas con un orden fijo.

> **Qué está verificado y qué no.** Las cifras de control de todo el capítulo se calcularon con Python sobre la mini-base inventada y se comprueban automáticamente. Las acciones de interfaz de Excel (menús, tablas dinámicas, formato) y las fórmulas **no se ejecutaron automáticamente**: son comprobación manual en tu equipo. Los ejemplos escritos usan `;` como separador de argumentos y los nombres de función en español; si tu Excel usa otra configuración, cambia solo el separador.

**Tiempo total estimado de primera vez:** unas 2 h 50 min de lectura y práctica (3 lecciones).

**Antes de empezar:** capítulos 2 y 3 (SQL), capítulo 6 (fichas de KPI) y la lección 14.1 (configuración regional).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 15.1 | [Excel desde cero](15_Excel_cuadres/01_excel_desde_cero.md) | importar CSV, valor frente a formato, tablas, separadores | refuerzo | 45 min |
| 15.2 | [Funciones para cuadrar](15_Excel_cuadres/02_funciones_para_cuadrar.md) | `SI`, `SUMAR.SI.CONJUNTO`, `BUSCARX`/`INDICE+COINCIDIR`, `SI.ERROR` | refuerzo | 60 min |
| 15.3 | [Tablas dinámicas, estadística y cuadre](15_Excel_cuadres/03_tablas_dinamicas_cuadre.md) | tabla dinámica, `PERCENTIL.INC/EXC`, `DESVEST.M/P`, diagnóstico de discrepancias | núcleo · D29 | 65 min |

## Ideas centrales

- No abras un CSV con doble clic si tu configuración usa coma decimal: podrías convertir montos a texto. Importa con *Desde texto/CSV*, fija UTF-8 y el delimitador, y compara la suma con una cifra de control.
- Escribe el **valor** (0,8) y deja que el **formato** lo muestre como porcentaje. No escribas 80 y luego apliques formato porcentaje.
- Una búsqueda sobre un catálogo con códigos duplicados devuelve solo la primera coincidencia: revisa la unicidad. Un código que no existe recibe una etiqueta de revisión, no una ruta inventada.
- El promedio de una tabla dinámica sobre líneas es el promedio **por línea**, no el ticket; el promedio de promedios de rutas es incorrecto.
- Si SQL y Excel no coinciden, antes de culpar a Excel fija el mismo período, estado, tabla y unidad. Registra el cuadre con una captura sin datos privados.
- Estadística: `PROMEDIO`, `MEDIANA`, `DESVEST.M`/`DESVEST.P` y `PERCENTIL.INC`/`PERCENTIL.EXC`; marca los atípicos con límites de IQR y **conserva la fila**.
- Los archivos XLSX guardan los nombres de función en inglés; el nombre localizado solo se muestra en tu Excel.

## Ejercicios autónomos de este capítulo

EX01 (tabla dinámica de rutas y comparación con SQL), EX02 (presupuesto por mes y ruta, comparado con el indicador de cumplimiento) y EX03 (percentiles, comparados con el ejercicio de estadística) en [`03_EJERCICIOS/Casos/`](../03_EJERCICIOS/Casos/). Sus criterios están en [`03_EJERCICIOS/CASOS.md`](../03_EJERCICIOS/CASOS.md). Las acciones de interfaz de Excel quedan como comprobación manual.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 16 — Git y comunicación](16_Git_comunicacion.md).
