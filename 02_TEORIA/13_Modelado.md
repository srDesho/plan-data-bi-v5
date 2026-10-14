# Capítulo 13 — Modelado dimensional: hechos, dimensiones y modelo estrella

Un modelo responde preguntas de negocio con una estructura explícita. Aquí aprendes a decidir **qué representa una fila** de cada tabla (granularidad), a separar los eventos medibles (hechos) de su contexto (dimensiones), a conectarlos en un modelo estrella sin multiplicar cifras y a construir la tabla de fechas que necesitan los reportes por período. Es la base del modelo de Power BI y de las tablas Gold del ETL. Todo se comprueba en Pandas con la mini-base inventada antes de pasar a cualquier herramienta de visualización.

**Tiempo total estimado de primera vez:** unas 2 h 40 min (3 lecciones).

**Antes de empezar:** capítulo 3 (claves y JOIN), capítulo 10 (merge y controles) y la lección 9.6 (fechas).

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 13.1 | [Hechos, dimensiones y granularidad](13_Modelado/01_hechos_dimensiones.md) | tabla de hechos, dimensión, medidas aditivas y no aditivas, claves | refuerzo | 55 min |
| 13.2 | [El modelo estrella](13_Modelado/02_modelo_estrella.md) | relaciones uno a muchos, dimensiones conformadas, caminos ambiguos, pruebas previas | núcleo · D30 | 60 min |
| 13.3 | [La tabla de fechas](13_Modelado/03_tabla_de_fechas.md) | calendario sin huecos, atributos, orden de meses, días sin ventas | profundización | 45 min |

## Ideas centrales

- La primera decisión del modelo es la **granularidad** de cada hecho.
- Presupuesto y visitas tienen otra granularidad que las ventas: van en **hechos separados** unidos por dimensiones conformadas; añadir un presupuesto a cada línea de venta lo multiplica.
- Las relaciones deben ser 1:* y normalmente con filtro en un sentido, de la dimensión al hecho. Una relación muchos a muchos puede ocultar un defecto de claves.
- El importe es aditivo; ticket, recencia y porcentajes **no se suman**: se recalculan en cada contexto.
- La tabla de fechas incluye **todos** los días del período, sin huecos ni duplicados.
- Este modelo usa la ruta actual del cliente; no modela cambios históricos de asignación. No presentes como histórico un atributo maestro actual.
- Antes de abrir Power BI prueba claves únicas, huérfanos, filas del hecho y total de ventas. Las relaciones dentro de Power BI se comprueban manualmente.

## Ejercicios autónomos de este capítulo

El exportador de modelo y el proyecto de Power BI en [`05_PROYECTOS/`](../05_PROYECTOS/). Las microprácticas de las lecciones no son evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 14 — Power BI, Power Query y DAX](14_PowerBI_DAX.md).
