# Proyecto de dashboard comercial

Ejecuta desde la raíz: `python 05_PROYECTOS/powerbi/exportar_modelo.py`.
Los CSV listos para importar ya están incluidos en `datos_modelo`.
Todos son sintéticos; no requieren ODBC ni conexión a un servidor.

| Dimensión y clave única | Tabla destino y clave | Cardinalidad |
|---|---|---|
| dim_cliente.cliente_id | fact_ventas.cliente_id |1:*|
| dim_producto.producto_id | fact_ventas.producto_id |1:*|
| dim_vendedor.vendedor_id | fact_ventas.vendedor_id |1:*|
| dim_fecha.fecha_id | fact_ventas.fecha_id y fact_visitas.fecha_id |1:*|
| dim_mes.mes | fact_ventas.mes, fact_presupuesto.mes y fact_visitas.mes |1:*|
| dim_ruta.ruta | fact_ventas.ruta, fact_presupuesto.ruta y fact_visitas.ruta |1:*|

Filtro único dimensión→hecho. No añadas dim_ruta→dim_cliente ni relaciones entre hechos:
pueden crear caminos alternativos o multiplicaciones. No conectes dim_mes→dim_fecha en
este diseño: cada tabla filtra directamente sus hechos.

Grano fact_ventas = línea de pedido; monto_centavos es entero. fact_presupuesto = mes/ruta.
La página de cumplimiento usa segmentadores dim_mes y dim_ruta, para filtrar ambas fuentes.
La página diaria de ventas usa dim_fecha; el presupuesto mensual no se prorratea automáticamente.
Si seleccionas días parciales o producto, no presentes cumplimiento como si hubiera presupuesto
de ese mismo nivel. Mantén las páginas separadas y explica el periodo.

## Construcción por sesiones

PB01 importar y tipos → PB02 relaciones/fecha → PB03 medidas básicas → PB04 contexto y tiempo
→ PB05 visuales/interpretación → PB06 actualizar y reconciliar.
Para cada sesión sigue `03_EJERCICIOS/CASOS.md` y guarda .pbix propio en `mi_trabajo/powerbi`.

No se incluye un PBIX: requiere Power BI Desktop en Windows. `medidas.dax` y `cargar_csv.m`
son referencias de texto que se deben aplicar y comprobar manualmente.
