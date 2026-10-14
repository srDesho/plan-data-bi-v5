# Proyecto ETL de la distribuidora

Antes de este proyecto haces el mini-ETL (ME01–ME04, `03_EJERCICIOS/Puente/`) con 24 filas: es la misma estructura en pequeño.
Construye tu propio script por fases en `mi_trabajo/etl/etl.py`. Las fechas de la tabla son objetivos; avanzas con la Puerta 4 (mini-ETL) cumplida.
Entrada: `04_DATASETS/distribuidora/etl/ventas_erp_raw.csv` y `vendedores_por_ruta.csv`.
Lee primero `02_TEORIA/05_calidad_ETL.md` y `10_Pandas_transformaciones.md`.

| Etapa | Jornada (objetivo) | Trabajo autónomo | Control |
|---|---|---|---|
| 1 · Extraer | D25 | CSV como texto; perfil por columna; conserva raw |16378 filas|
| 2 · Texto | D25 | espacios, estados, rutas, clientes |120 clientes normalizados|
| 3 · Tipos | D26 | tres formatos fecha, cantidad entera, precio |sin conversiones silenciosas|
| 4 · Claves | D26 | revisa duplicados y catálogo vendedor/ruta |200 duplicados, 301 vendedores recuperados|
| 5 · Silver | D29 | valida tipos, estados y pedido/producto |16178 líneas, 3600 pedidos|
| 6 · Gold | D30 | entregados por cliente/mes, pedidos distintos |581 filas; 1468924,50 Bs|
| 7 · Cargar | D30 | SQLite: bronze_ventas_raw, silver_ventas, gold_ventas_cliente_mes |cuadre SQL, segunda ejecución sin duplicar|

No empieces por copiar `etl_distribuidora.py`. El esqueleto es intencionalmente incompleto,
recuperado y simplificado a partir del repositorio plantilla original.
Completa una función por vez y prueba tres filas antes de ejecutar todo.

Después de la entrega consulta `08_SOLUCIONES/etl_distribuidora.py` y revisa cada diferencia.
Corrección: `python herramientas/validar_etl_distribuidora.py mi_trabajo/etl/etl_salida.db`.
Puedes cambiar ubicación de salida; debe incluir las tres tablas con los nombres del contrato.

## Contrato de salida y qué revisa el corrector

| Tabla | Columnas |
|---|---|
| `bronze_ventas_raw` | `nro_pedido`, `fecha`, `cliente`, `ruta`, `vendedor`, `estado`, `producto`, `categoria`, `cantidad`, `precio_unitario`: el archivo tal cual, como texto, con sus 16.378 filas |
| `silver_ventas` | las mismas columnas ya limpias más `monto` (`fecha` AAAA-MM-DD, `cantidad` entera, `precio_unitario` y `monto` en Bs con dos decimales) |
| `gold_ventas_cliente_mes` | `cliente`, `mes` (AAAA-MM), `pedidos` (pedidos distintos), `unidades`, `ventas_bs` |

**Dinero en este proyecto:** Bs con dos decimales (REAL), no centavos enteros. Para comparar sin errores de coma flotante, el corrector pasa cada importe a centavos redondeando al centavo más cercano (mitad hacia arriba) y exige igualdad exacta: `monto` = `cantidad` × `precio_unitario` y `ventas_bs` = suma de los `monto` entregados de ese cliente y mes (tolerancia de 0 centavos). Los proyectos C06 y la evaluación final sí usan centavos enteros.
El corrector revisa filas y agrupaciones, no solo totales: Bronze idéntico al archivo, Silver fila por fila (pedido + producto), Gold recalculado desde tu propia Silver y comparado con el esperado. Una Gold con las ventas intercambiadas entre clientes, o con líneas contadas como pedidos, falla aunque el total sea 1.468.924,50 Bs.

Aceptación: contrato escrito, registro auditable de la ejecución (logging), datos de origen preservados, claves válidas, cuadres
y README de reproducción. La adaptación v 5 evita truncar cantidades fraccionarias.

Aquí **logging** significa dejar un rastro por ejecución de las etapas realizadas, sus conteos y las reglas aplicadas. Los registros de auditoría y conteos ya exigidos bastan si están documentados y permiten reconstruir qué ocurrió en cada ejecución. Usar el módulo Python `logging` es opcional; [5.4 Cargas, registro y reproducibilidad](../../02_TEORIA/05_calidad_ETL/04_cargas_registro_reproducibilidad.md) lo amplía como REFUERZO. Esta aclaración no añade otra entrega ni sustituye las validaciones, los cuadres o la segunda ejecución.
