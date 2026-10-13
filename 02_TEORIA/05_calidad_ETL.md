# ETL y Medallion: un proceso que puedas defender

ETL significa extraer, transformar y cargar. ELT carga primero y transforma dentro del destino. Son órdenes de trabajo; ninguno garantiza calidad por sí mismo. Para esta práctica extraemos CSV, transformamos con Python y cargamos SQLite. Bronze, Silver y Gold describen estados de calidad y uso; no obligan a usar cloud ni productos específicos.

Bronze conserva filas y valores como llegaron y registra la fuente. No sobrescribas el archivo original. Silver contiene claves, tipos, fechas y estados normalizados; conserva también anulados porque son hechos operativos. Gold reúne cifras útiles, por ejemplo cliente/mes con ventas entregadas y pedidos distintos. Los rechazos son una salida auditada, no una papelera oculta.

## Un diseño de cuatro funciones

`extraer(ruta)` lee con separador y codificación conocidos. `transformar(raw,catalogo)` normaliza y separa filas. `validar(silver)` verifica reglas. `cargar(...)` publica una versión coherente. Mantén la lógica en funciones importables y un `main` pequeño que configure rutas y logging. Escribe mensajes con etapa, conteos y motivos; nunca claves secretas ni datos privados.

Antes de programar redacta el contrato: columnas requeridas, qué es una fila, clave única, formatos admitidos, estados permitidos, cuándo rechazar y qué cuadres deben cumplirse. Si no puedes definirlo para tres filas a mano, todavía no estás listo para escribir un pipeline de 12.000 filas.

## Caso distribuidora existente

Entrada: 16.378 líneas, tres formatos de fecha, precios con Bs/coma y vendedores vacíos. Debe producir 16.178 líneas Silver después de quitar 200 duplicados, recuperar 301 vendedores por una ruta inequívoca y mantener 3.600 pedidos. Gold cliente/mes tiene 581 filas y suma 1.468.924,50 Bs.

La recuperación por ruta solo es válida porque el catálogo tiene un vendedor por ruta en este escenario. Si varios vendedores se turnan o cambia la asignación, necesitas vigencia temporal u otra clave; no uses esa imputación por costumbre. Normalizar nombres no sustituye un ID estable.

## Caso nuevo y rechazos

El caso final usa línea_id estable y un catálogo de SKU. Una cantidad 1.5 es inválida cuando el contrato exige unidades enteras. Truncarla cambia el monto. Una fecha imposible o un SKU huérfano debe aparecer con su causa en `rechazos.csv`. La ecuación de auditoría es:

`filas Bronze = duplicados exactos + rechazados + filas Silver`.

Antes de eliminar exactos, detecta misma clave con contenido distinto: un conflicto debe detener esta práctica. Cada fila rechazada puede tener más de una causa; conserva una lista o un texto separado por `;`. Preserva suficiente identificación para revisión.

## Carga y reproducibilidad

Una segunda ejecución debe producir iguales filas y totales, no duplicarlos. En la versión del curso se publica una base nueva en un archivo temporal y se reemplaza el destino solo después de pasar validaciones. Esa es una carga completa, no incremental. Si falla el catálogo o el parser, la salida anterior se mantiene.

Cuadra dinero en centavos enteros para el caso final: suma detallada entregada = resumen Gold. Comprueba fechas y claves, también tablas con filas vacías. El número de filas correcto por sí solo no detecta importes multiplicados.

Práctica: proyecto ETL en etapas, P21–P30 y casos C04/C06. Fuente: Databricks Medallion, Python logging y sqlite 3. El ETL original validado está separado de las actividades para evitar copiarlo antes del intento.
