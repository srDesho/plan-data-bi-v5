# Informe de validación · Plan Data & BI v5

Este informe distingue material ejecutado, inspección estructural y acciones manuales pendientes.
El paquete contiene el programa y sus referencias; no acredita que el estudiante ya adquirió las habilidades.
**Cierre de pruebas: 13 grupos aprobados, 0 fallos.** El control adicional de cantidad fraccionaria del ETL adaptado también pasó.

Evidencia reproducible: `python herramientas/verificar_paquete.py`; resultados detallados en
`resultados_pruebas.json`, `evidencia_sql.json`, `evidencia_python.json` y los archivos complementarios.

## Contenido construido

42 guías diarias, plan maestro con casillas, 18 capítulos de teoría, glosario y fuentes;
81 actividades SQL, 30 funciones Python, 7 ejercicios de estadística, 7 notebooks guiados,
15 casos (incluidos Excel/Power BI), 6 exámenes y 6 simulacros con 24 preguntas técnicas.
CV/perfil, seguimiento de postulaciones y 12 borradores de LinkedIn completan la formación laboral.
La evaluación final incluye un dataset nuevo, contrato, calendario, rúbrica y controles separados.

## Pruebas y resultados

| Componente | Prueba realizada | Resultado |
|---|---|---|
|SQL original v3|56 bloques ejecutados contra la base original|Sin errores de ejecución|
|SQL v5|81 actividades de referencia ejecutadas y corregidas por resultado completo|Controles coincidentes; consulta incorrecta rechazada|
|Datos originales|Comparación fila por fila de cinco CSV con SQLite; integridad SQLite y CRC de ZIP|120 clientes, 40 productos, 6 vendedores, 3600 pedidos y 16178 ítems|
|Cuadre independiente|Pandas sobre CSV frente a SQLite y drop_por_pedido completo|1468924,50 Bs; 3442 entregados; 158 anulados|
|Python|30 contratos, 68 casos normales/límites/errores; función incorrecta como control negativo|Casos aprobados y resultado incorrecto rechazado|
|ETL v3/adaptado|Ejecución original y dos ejecuciones de la adaptación v5|Bronze16378, Silver16178, Gold581; venta1468924,50 Bs|
|ETL nuevo|Transferencia y final, cada uno dos veces; comparación contra oracle generado antes de ensuciar|Mismos resultados lógicos, Silver correcta fila por fila y Gold cuadrada|
|Transferencia|Conteos explicados|4048 Bronze, 40 duplicados, 8 rechazos, 4000 Silver y 724 Gold|
|Final|Conteos explicados, sin publicar aquí su importe para conservar la evaluación|12170 Bronze, 150 duplicados, 20 rechazos, 12000 Silver y 1128 Gold|
|Pruebas adversas|Columna ausente, catálogo duplicado, clave conflictiva y cantidad fraccionaria|Errores/rechazo explícitos; salida anterior preservada ante fallo estructural|
|KPIs auxiliares|Agenda sintética y denominadores independientes|480 planificadas, 384 realizadas, 288 con pedido; cobertura80%, efectividad75%|
|Estadística|Percentiles, IQR, z, Welch, IC y chi-cuadrado contra controles|141 atípicos IQR, 64 con absoluto z>3; pilotos y convenciones reproducibles|
|Modelo BI|Exportación de nueve tablas, claves únicas, huérfanos y cuadres|Fact16178; dims120/40/6/183/6/6; presupuesto36, visitas480|
|Notebooks nuevos|Validación nbformat y ejecución en orden de sus celdas Python|7 notebooks:21 celdas con ejemplos y7 de práctica con comentarios; todas ejecutables y con esquema válido|
|Calendario|42 fechas consecutivas, modalidades, suma de bloques y referencias|900 minutos semanales; lunes compatible con clase; seis domingos0|
|Markdown/rutas|Fences cerradas, enlaces internos, IDs, archivos no vacíos y separación|Ver conteos exactos y resultado final en resultados_pruebas.json|

Los controles SQL almacenados se obtuvieron ejecutando las referencias; los cuadres comerciales principales
se contrastaron además con CSV/Pandas. No se afirma una demostración independiente de cada interpretación
empresarial solo por haber ejecutado una consulta. Los enunciados y criterios explicitan población y granularidad.
La prueba de idempotencia compara filas/importes; no exige igualdad byte a byte de archivos SQLite.

Las pruebas adicionales comprobaron el inicializador sin sobrescribir registros y ejecutaron todos los ejemplos Python completos de los apuntes.

## Complemento UAGRM

- Clase 1: JSON/esquema validado y 58 celdas de código ejecutadas en orden sin error.
- Clase 2: esquema válido; ejecución detenida en la celda18 al conectar con UCI (`ConnectionError`).
  Dos celdas de instalación pip se omitieron porque las dependencias ya estaban instaladas.
  No se declara ejecutado el resto de ese notebook ni descargados sus datasets externos.

- ml_eda_functions.py: importación correcta tras instalar dependencias y una prueba de cramers_v con
  asociación nula. Las otras 16 funciones avanzadas no se probaron integralmente y están fuera del núcleo.

- PDF UAGRM: texto extraído de32 páginas,32 renderizados abiertos correctamente y revisión visual del conjunto.
  Se preserva el original; no se presenta el PDF como sustituto del programa generado.

El lanzamiento de un kernel Jupyter TCP falló por restricciones de red/socket del entorno. Los siete notebooks
nuevos y Clase1 se ejecutaron en el mismo proceso, con variables conservadas entre celdas; se verificó su código,
no el comportamiento del frontend Jupyter/Colab. Este método y el error están registrados expresamente.

## Pendientes reales y límites

1. **Power BI Desktop:** aplicar y probar M/DAX, relaciones, fecha, segmentadores, medidas, filtros y actualización
   en Windows. CSV/modelo Python comprobados; no existe un PBIX simulado ni DAX declarado como ejecutado.

2. **Excel:** importación, fórmulas localizadas y tablas dinámicas de EX01–EX03. Hay fuentes y cifras de control;
   la interfaz Excel no se ejecutó aquí.

3. **Notebooks externos:** conexión UCI y ejecución restante de Clase2; frontend/kernel Jupyter nativo.
4. **Material avanzado suplementario:** las16 funciones restantes de ml_eda_functions.py; no son requisitos del núcleo.
5. **SQL Server:** las diferencias T-SQL son material conceptual; no se ejecutó una instancia SQL Server.
6. **Notion/GitHub/LinkedIn/empleo:** importación, publicación, CV adaptado y envíos los realiza el estudiante.
   No se enviaron mensajes ni postulaciones, no se verificaron vacantes ni se garantiza contratación.

7. **Autonomía:** requiere completar el examen del23–30 y defensa honesta/observada. Las referencias ejecutadas
   prueban el material, no la capacidad del estudiante. La progresión/calendario se revisaron por alcance y dependencias;
   el tiempo real de una persona concreta debe registrarse y ajustarse, no se considera probado empíricamente.

8. **Fuentes web:** se consultaron las referencias principales indicadas en FUENTES.md; algunos enlaces adicionales
   no se comprobaron individualmente. La integridad exigida de enlaces internos sí se prueba automáticamente.

## Correcciones y reproducción

Consulta `DECISIONES_Y_CORRECCIONES.md`. Se reutilizaron datos, soluciones y estructuras v3; la base original
no se reemplazó. CL4 recibió una consulta de prueba real; cantidades fraccionarias no se truncan; ABC por SKU
se distingue de ventas; ventas entregadas no se llaman ventas netas contables. Se corrigió interpretación de
p-valor y se separó un piloto independiente de pedidos repetidos por cliente.

Las soluciones permanecen en08_SOLUCIONES, los ejercicios en03_EJERCICIOS y los originales archivados en10_VALIDACION.
Los esqueletos con NotImplementedError y las celdas de práctica son actividades sin resolver deliberadamente;
no se presentan como programas completos. Versiones de prueba: `versiones.json`.

El ZIP final se verifica con CRC y un manifiesto SHA256 de sus archivos. La evidencia de cierre está en `CIERRE_PAQUETE.json`. Para comenzar: README y Día1; no abrir el caso final antes del23 de noviembre.
