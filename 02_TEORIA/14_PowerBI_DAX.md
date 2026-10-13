# Power BI: cargar, modelar, medir y comprobar

Power Query transforma datos al actualizar. DAX calcula medidas y columnas dentro del modelo. Una columna calculada tiene un valor por fila y ocupa almacenamiento; una medida se evalúa según los filtros del visual. Ticket medio, cumplimiento y crecimiento deben ser medidas para recalcularse por periodo/ruta.

## Construcción guiada en Desktop

1. Ejecuta el exportador Python y abre la carpeta `05_PROYECTOS/powerbi/datos_modelo`.
2. Obtener datos → Texto/CSV → importa cada tabla. En Power Query especifica UTF-8, coma, claves de texto cuando corresponda y fechas Date. Dinero se exporta en centavos enteros; evita interpretar decimales según configuración regional.
3. Comprueba claves únicas y crea las relaciones del documento `MODELO.md`; no aceptes automáticamente relaciones inferidas sin revisar.
4. Marca dim_fecha como tabla de fechas y oculta IDs que no deban aparecer en visuales.
5. Crea medidas una por una desde `medidas.dax`, seleccionando el nombre y expresión de cada bloque. El archivo es texto de referencia, no una importación automática de todo el modelo.

```dax
Ventas Bs =
DIVIDE(
    CALCULATE(SUM(fact_ventas[monto_centavos]),fact_ventas[estado]="entregado"),
    100
)
```

`CALCULATE` modifica contexto de filtros; SUM suma una columna en el contexto resultante. `DIVIDE` controla un denominador cero y devuelve BLANK por defecto. No conviertas BLANK en 0 si significa que no existe presupuesto o periodo comparable. La venta sigue expresada en Bs aunque el almacenamiento sea en centavos.

## Contexto y denominadores

Un segmentador de ruta filtra hechos a través de dim_ruta. El presupuesto debe usar ese mismo filtro. Si usas ruta de dim_cliente, las ventas podrían filtrarse sin filtrar presupuesto en este diseño. Para el comparativo mensual utiliza dim_mes; para tendencias diarias, dim_fecha. Si aplicas un filtro de producto, el presupuesto por ruta no se vuelve presupuesto por producto: no muestres cumplimiento por SKU sin un presupuesto asignado a ese nivel.

`ALLSELECTED` permite una participación relativa al conjunto seleccionado; `REMOVEFILTERS` cambia deliberadamente el denominador. Explica en el título si se compara contra todo el periodo o la selección. La medida de mes anterior usa DATEADD sobre dim_fecha; el primer mes sin histórico devuelve BLANK, y los cortes parciales deben explicarse.

## Dashboard laboral

Página comercial: tarjetas de ventas entregadas, pedidos y ticket; línea por fecha; barras por ruta; tabla con presupuesto/cumplimiento por mes y ruta. Página operativa: cobertura y efectividad de visitas y clientes inactivos. Usa títulos con unidad/periodo, colores consistentes y dos o tres hallazgos. No llenes el tablero de gráficos sin decisiones asociadas.

Control total: 1.468.924,50 Bs y 3.442 pedidos; septiembre: 300.922 Bs y 722 pedidos. Compara una ruta y una categoría contra SQL. Si el total cuadra y una ruta no, revisa relaciones y campos del segmentador. Si todo se multiplica, revisa unicidad de dimensiones.

Este paquete entrega CSV, guía, M y DAX; no contiene un `.pbix` fabricado ni medidas declaradas como ejecutadas. La lista manual exige probar importación, filtros, relaciones, medidas y actualización en Windows. Fuentes: Microsoft Learn, esquema estrella, tablas fecha, DAX CALCULATE y DIVIDE.
