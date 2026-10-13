# Casos laborales y prácticas de Excel/Power BI

Cada caso se entrega en `mi_trabajo/casos/ID.md` y su código/archivo asociado. Revisa la solución únicamente después del intento.
Todos los datos de negocio son sintéticos.

## C01 · Explicar incumplimiento sin inventar causas

Ventas reales 80000 Bs, presupuesto 100000 Bs;100 visitas planificadas,80 realizadas,60 con pedido. Calcula cumplimiento, cobertura y efectividad. Redacta cuatro frases para gerencia y pide un dato que ayude a investigar la causa.

Entrada: Datos incluidos en el enunciado. Tiempo: 30 min. Enunciado completo: `03_EJERCICIOS/Casos/C01.md`.

## C02 · Visitas repetidas y cobertura

Plan:12 actividades a 10 clientes distintos. Ejecución:9 actividades; clientes visitados [1,1,2,3,4,5,6,7,8]. Calcula cobertura de actividades y de clientes. ¿Por qué difieren?

Entrada: Datos incluidos en el enunciado. Tiempo: 25 min. Enunciado completo: `03_EJERCICIOS/Casos/C02.md`.

## C03 · Qué entrega es típica

Gerencia cree que todas las entregas deberían acercarse al ticket promedio. Compara media/mediana/P90 e IQR; muestra cinco pedidos altos y decide qué revisarías.

Entrada: 04_DATASETS/distribuidora/drop_por_pedido.csv. Tiempo: 35 min. Enunciado completo: `03_EJERCICIOS/Casos/C03.md`.

## C04 · SQL y reporte no coinciden

Un reporte muestra 1534625 Bs y otro 1468924,50 Bs. Encuentra la diferencia por estado y confirma con SQL/Pandas. Propón un control para que no vuelva a ocurrir.

Entrada: 04_DATASETS/comercial.db y CSV distribuidora. Tiempo: 40 min. Enunciado completo: `03_EJERCICIOS/Casos/C04.md`.

## C05 · Un pipeline funciona pero modifica datos

Un parser convierte cantidades 3.7 a 3 y deja como 0 un precio ilegible. Diseña tres pruebas adversas, decide cuándo rechazar/detener y verifica que un catálogo con SKU duplicado no multiplique ventas.

Entrada: Tabla pequeña que construirás a mano; referencia contratos P09/P11/P21. Tiempo: 45 min. Enunciado completo: `03_EJERCICIOS/Casos/C05.md`.

## C06 · ETL de transferencia completo

Recibe una exportación nueva. Construye contrato, perfilado, Bronze, Silver, rechazos, Gold cliente/mes y SQLite. Usa centavos enteros, valida catálogo y reejecución. Entrega README y resumen gerencial. Distribuye C06 en cuatro bloques: 25 + 70 + 80 + 65 = 240 minutos, ya incluidos en la semana 6.

Entrada: 04_DATASETS/transferencia/transacciones_raw.csv y catalogo.csv. Tiempo: 240 min. Enunciado completo: `03_EJERCICIOS/Casos/C06.md`.

## EX01 · Cuadre Excel por ruta

Importa drop_por_pedido.csv con tipos correctos. Tabla dinámica: ruta, suma drop_bs, conteo pedido_id. Compara contra E4 y comprueba total.

Entrada: 04_DATASETS/distribuidora/drop_por_pedido.csv. Tiempo: 40 min. Enunciado completo: `03_EJERCICIOS/Casos/EX01.md`.

## EX02 · Presupuesto y porcentajes ponderados

Usa presupuesto.csv y ventas por ruta/mes exportadas desde N1. Construye cumplimiento y brecha. Calcula global como suma reales/suma metas, no promedio de porcentajes.

Entrada: 04_DATASETS/presupuesto.csv; tu consulta N1. Tiempo: 40 min. Enunciado completo: `03_EJERCICIOS/Casos/EX02.md`.

## EX03 · Percentiles entre Excel y Python

Calcula PROMEDIO, MEDIANA, DESVEST.M, PERCENTIL.INC para drop. Explica población/muestra y qué cambia si redondeas Q1 antes de IQR.

Entrada: 04_DATASETS/distribuidora/drop_por_pedido.csv. Tiempo: 30 min. Enunciado completo: `03_EJERCICIOS/Casos/EX03.md`.

## PB01 · Importación y tipos

Importa los nueve CSV de datos_modelo, verifica tipos/claves y cuenta filas. No aceptes relaciones inferidas sin revisarlas.

Entrada: 05_PROYECTOS/powerbi/datos_modelo. Tiempo: 45 min. Enunciado completo: `03_EJERCICIOS/Casos/PB01.md`.

## PB02 · Relaciones y calendario

Crea relaciones del MODELO.md con filtros únicos y marca dim_fecha. Comprueba que un segmento de ruta filtre hechos correctamente.

Entrada: 05_PROYECTOS/powerbi/MODELO.md. Tiempo: 45 min. Enunciado completo: `03_EJERCICIOS/Casos/PB02.md`.

## PB03 · Medidas comerciales

Crea ventas, pedidos, ticket, clientes compradores y frecuencia. Compara total y septiembre con SQL.

Entrada: 05_PROYECTOS/powerbi/medidas.dax. Tiempo: 45 min. Enunciado completo: `03_EJERCICIOS/Casos/PB03.md`.

## PB04 · Contexto, presupuesto y tiempo

Crea presupuesto, cumplimiento, mes anterior, crecimiento y participación. Explica dim_mes frente a dim_fecha y restricción de presupuesto mensual.

Entrada: 05_PROYECTOS/powerbi/medidas.dax. Tiempo: 50 min. Enunciado completo: `03_EJERCICIOS/Casos/PB04.md`.

## PB05 · Dashboard y recomendación

Construye dos páginas:comercial mensual y ejecución operativa. Máximo seis visuales útiles por página. Incluye dos hallazgos y qué dato falta para probar su causa.

Entrada: Modelo y medidas propios. Tiempo: 50 min. Enunciado completo: `03_EJERCICIOS/Casos/PB05.md`.

## PB06 · Actualizar y reconciliar

Reexporta los CSV, refresca Desktop, compara rutaR01, categoríaLácteos, septiembre y total. Completa VALIDACION_MANUAL.md y guarda PBIX propio.

Entrada: 05_PROYECTOS/powerbi/VALIDACION_MANUAL.md. Tiempo: 45 min. Enunciado completo: `03_EJERCICIOS/Casos/PB06.md`.
