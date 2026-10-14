# Capítulo 14 — Power BI, Power Query y DAX: cargar, modelar, medir y comprobar

Este capítulo te lleva de cero a un tablero comercial **comprobable**: cargar tablas limpias en Power BI cuidando la configuración regional, transformar con Power Query, entender el contexto de filtro de DAX, escribir las siete medidas de un tablero comercial y diseñar páginas con títulos que digan qué se ve. Todo con una regla: **cada cifra se cruza con SQL y con Excel**.

> **Qué está verificado y qué no.** Las cifras de control de todo el capítulo se calcularon con Python sobre la mini-base inventada y se comprueban automáticamente. Los pasos de interfaz de Power BI Desktop, el código M y el código DAX **no se ejecutaron en Power BI Desktop** al escribir este material (no se afirma que hayan sido probados allí): son guía de referencia que tú pruebas en tu equipo con la lista de comprobación manual de la lección 14.5. Este paquete no contiene un `.pbix` fabricado.

**Tiempo total estimado de primera vez:** unas 4 h 45 min de lectura y práctica (5 lecciones), sin contar el tiempo de construir tu propio tablero en Desktop.

**Antes de empezar:** capítulos 10 (Pandas), 13 (modelado) y 6 (KPIs). Se necesita Windows y Power BI Desktop (gratuito) para la parte práctica en interfaz.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 14.1 | [Power BI desde cero](14_PowerBI_DAX/01_power_bi_desde_cero.md) | flujo de cuatro etapas, configuración regional, cifras de control | núcleo · D32 | 50 min |
| 14.2 | [Power Query y M](14_PowerBI_DAX/02_power_query.md) | pasos aplicados, equivalencias con Pandas, combinar, actualización | profundización | 55 min |
| 14.3 | [DAX: medidas y contexto de filtro](14_PowerBI_DAX/03_dax_contexto.md) | medida frente a columna, contexto, `CALCULATE`, `DIVIDE`, `BLANK` | núcleo · D33 | 70 min |
| 14.4 | [Medidas útiles y su control](14_PowerBI_DAX/04_medidas_utiles.md) | ventas, pedidos, ticket, meta, cumplimiento, % del total, mes anterior | profundización | 65 min |
| 14.5 | [Diseño y comprobación manual](14_PowerBI_DAX/05_diseno_y_comprobacion.md) | páginas, títulos, lista de comprobación | profundización | 45 min |

## Ideas centrales

- Power Query transforma datos al actualizar; DAX calcula medidas y columnas dentro del modelo. Una columna calculada tiene un valor por fila y ocupa almacenamiento; una **medida** se evalúa según los filtros del visual. Ticket medio, cumplimiento y crecimiento deben ser medidas.
- No aceptes automáticamente las relaciones inferidas: revísalas contra el documento del modelo.
- `DIVIDE` controla el denominador cero y devuelve `BLANK`. **No conviertas `BLANK` en 0** si significa que no existe presupuesto o período comparable.
- Si aplicas un filtro de producto, el presupuesto por ruta **no** se vuelve presupuesto por producto: no muestres cumplimiento por SKU sin un presupuesto asignado a ese nivel.
- Explica en el título si un porcentaje se compara contra todo el período o contra la selección (`ALLSELECTED` frente a `REMOVEFILTERS`).
- Dinero en centavos enteros para evitar interpretaciones de decimales según la configuración regional; sigue siendo bolivianos al mostrarlo.
- Si el total cuadra y una ruta no, revisa relaciones y el campo del segmentador. Si todo se multiplica, revisa la unicidad de las dimensiones.

## Ejercicios autónomos de este capítulo

El proyecto de Power BI en [`05_PROYECTOS/powerbi/`](../05_PROYECTOS/powerbi/) (`MODELO.md`, `cargar_csv.m`, `medidas.dax`, `VALIDACION_MANUAL.md`, los CSV de `datos_modelo` y el exportador `exportar_modelo.py`). El diseño y los CSV se comprueban automáticamente; las relaciones, las medidas y la actualización dentro de Power BI se comprueban **manualmente**.

Fuentes: Microsoft Learn (esquema estrella, tablas de fechas, DAX `CALCULATE` y `DIVIDE`). Términos: [glosario](GLOSARIO.md). [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 15 — Excel como segundo camino de validación](15_Excel_cuadres.md).
