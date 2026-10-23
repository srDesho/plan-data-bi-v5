# Capítulo 17 — Transferencia y autonomía: resolver datos que cambian

Aprender un ETL de memoria no demuestra que puedas construir otro. La práctica de **transferencia** cambia los nombres de columnas, las claves, el catálogo y los formatos. Este capítulo te da el método para enfrentarlo: los ocho pasos aplicados a un caso nuevo (con cambios adversos del archivo), la técnica de reducir el problema cuando un total no cuadra y las reglas de trabajo para demostrar autonomía sin depender de que otro escriba el código por ti.

**Tiempo total estimado de primera vez:** unas 2 h 55 min (3 lecciones).

**Antes de empezar:** capítulos 5, 8 y 10 (en especial 5.5, 8.7 y 10.5).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 17.1 | [Los ocho pasos frente a un caso nuevo](17_Transferencia_debug/01_ocho_pasos_caso_nuevo.md) | Bronze, perfilado, clasificación, funciones con pruebas, catálogo, cuadre con SQL independiente, cambios adversos | NÚCLEO · D36 | 70 min |
| 17.2 | [Cuando no cuadra](17_Transferencia_debug/02_cuando_no_cuadra.md) | primer desvío, comparación por documento, hipótesis, corregir la causa | NÚCLEO · D38 | 60 min |
| 17.3 | [Resolver sin ayuda externa](17_Transferencia_debug/03_resolver_sin_ia.md) | método intento-comprobar-depurar-pista, registro de consultas, evidencia de autonomía | COMPLEMENTARIA | 45 min |

## El proceso de ocho pasos (resumen)

1. Copia la entrada a Bronze y registra nombres, tamaños y conteos.
2. Perfila todas las columnas: tipos observados, nulos, categorías, duplicados y formatos.
3. Distingue estructura inválida, conflictos de clave y filas rechazables.
4. Escribe funciones pequeñas y pruébalas con tres ejemplos.
5. Aplica transformaciones y conserva rechazos con motivos.
6. Une el catálogo con validación de cardinalidad y busca huérfanos.
7. Calcula Gold y cuadra conteos e importes con un SQL independiente.
8. Ejecuta de nuevo, documenta y explica límites a gerencia.

## Ideas centrales

- Una columna nueva no obligatoria se conserva en Bronze y se ignora explícitamente en Silver; una columna obligatoria ausente produce un error legible; un SKU duplicado con descripciones contradictorias detiene el JOIN; si faltan campos para un KPI, se documenta «no calculable» y se solicita el dato (sin sustituto bajo el mismo nombre).
- La prueba de repetición verifica idempotencia lógica: iguales claves, filas y ventas (no igualdad de bytes). La carga incremental no forma parte de esta práctica.
- Cuando no cuadra: reducir. Si las filas coinciden pero el dinero no, busca cantidades truncadas, precios mal interpretados, estados incorrectos o un presupuesto multiplicado; compara importes **por documento** para localizar el primer desvío.
- Se pueden consultar documentación oficial y tus definiciones conceptuales; no copiar soluciones del paquete ni pedir a una IA que programe. Se registran las páginas consultadas y el motivo.
- El objetivo de noviembre es un ETL junior funcional y defendible, no una autonomía profesional avanzada garantizada. Si no superas un hito, el plan recorta extras y reserva una sesión para esa base; no crea deuda acumulada.

## Ejercicios autónomos de este capítulo

El caso **C06** y la evaluación final. No abras `08_SOLUCIONES/etl_nuevo_referencia.py` ni los controles de C06 hasta terminar el intento (la evaluación final no tiene referencia en el paquete: ver su enunciado) integral. Las microprácticas de las lecciones no son evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 18 — Preparación para entrevistas](18_Entrevistas.md).
