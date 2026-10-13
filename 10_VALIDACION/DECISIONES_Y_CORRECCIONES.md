# Decisiones de integración

1. Reutilización: datos v 3, 56 bloques de solución SQL y estructura SQL/ETL/BI de las plantillas.
   Los ZIP y scripts originales se conservan; v 5 integra rutas coherentes y controles adicionales.

2. CL4 original solo creaba la vista temporal aunque anunciaba consulta de prueba; v 5 añade SELECT COUNT(*)
   y corrige su contrato a 120 clientes. No se cambió la base original.

3. ETL original funcionó con sus datos: 16378→16178→581; 301 vendedores recuperados y 1468924,50 Bs.
   Su adaptación v 5 rechaza cantidades fraccionarias en vez de truncarlas y resuelve rutas desde el paquete.

4. El pipeline nuevo usa clave de línea, centavos enteros, catálogo validado, rechazos y publicación SQLite
   tras validación. Se comparó contra registros válidos generados ANTES de ensuciar el dataset.

5. Se separó ABC por ventas de variedad de SKU. No se inventaron umbrales empresariales de variedad.
6. No se llamó venta neta contable al importe entregado: faltan descuentos y devoluciones.
7. Se añadieron visitas/presupuesto/inventario ficticios porque las ventas solas no permiten esos KPIs.
   Inventario y pilotos son casos separados, no reconstrucciones de stock/experimentos de Cruzimex.

8. La inferencia usa un piloto con tiendas independientes; el t de pedidos repetidos por cliente no se
   presenta como causalidad. La interpretación previa de p-valor se corrige en los nuevos apuntes.

9. Python precede a Pandas; SQL y KPI empiezan en semana 1. Empleo desde 15 oct y 2 publicaciones/semana.
10. Carga total:900 min/semana incluye empleo; clase aparte, domingos 0. Banco ampliado se recorta sin deuda.
11. Power BI entrega modelo CSV/M/DAX e instrucciones, sin PBIX simulado; comprobación manual marcada.
12. Olist, ML, Docker, cloud y Airflow permanecen fuera del núcleo. Plantillas originales archivadas no son tareas obligatorias.
13. Contexto: documentos v 3/v 4/contexto accesibles y prompt maestro. No se afirma lectura directa del otro chat completo.

## Revisión 5.1 (corrección pedagógica de enunciados)

14. Los 81 enunciados SQL se reescribieron uno a uno (situación, tablas, columnas con significado, qué representa una fila, reglas de filtro/orden/redondeo, tres pistas específicas, criterios propios y tiempo de primera vez). `CONTRATOS.md` queda como tabla de comprobación y no sustituye al enunciado.
15. Se declararon los datos que antes solo vivían en el corrector: redondeos, etiquetas exactas («Pequeño»), la convención del ABC, texto de nombres «tal como está guardado», contrato de salida de C06 y tablas/columnas del mini-ETL.
16. Se añadieron al capítulo 02 las funciones que los ejercicios exigían sin enseñarlas (`ROUND`, `strftime`, `CASE`, `TRIM`, `UPPER`, `UNION ALL`, vistas temporales) y se cambiaron dos ejemplos de teoría que reproducían J1 y J5. Se eliminaron respuestas publicadas en enunciados y teoría.
17. Los exámenes S02–S06 y sus tareas se alinearon con lo obligatorio previo; ES1B y ES3C cambiaron como se explica en `INFORME_VALIDACION.md`.
18. Los tiempos de cada ejercicio se declaran en su enunciado («Primera vez»); `CARGA_ESTIMADA.md` los usa como única fuente.
