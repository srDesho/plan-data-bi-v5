# 05 · Especificación de ejercicios nuevos (ninguno está creado)

BASE nuevos: 26 (590 min) · REFUERZO nuevos: 18 (520 min). Cada ejercicio tiene finalidad distinta de los existentes, prerrequisitos (lecciones ya enseñadas antes de su día), datos, entregable y método verificable. Los correctores y contratos existentes **no se modifican**: en la Fase 3 se añadirán registros nuevos, con aprobación. Las consultas de referencia de SQ01–SQ17 se verificaron en solo lectura contra `comercial.db` y se guardan **fuera del repositorio** (`Respaldos_Plan_Data_BI_v5/FASE1B_DISENO/referencias_privadas/`) hasta que se aprueben; aquí solo constan los contratos de forma (filas × columnas).

## Ejercicios BASE nuevos de recuperación SQL (SQ01–SQ17)

Etapas: Inicial (SQ01–SQ02) · Intermedia (SQ03, SQ05) · Relacional (SQ04, SQ06–SQ08) · Analítica (SQ09–SQ12) · BI/Data Engineering (SQ13–SQ17). Cada una es breve, autocontenida, usa `comercial.db` y solo teoría anterior a su día.

### SQ01 · D10 · 25 min · nivel 1/3 · etapa Inicial
- Prerrequisitos: lecciones 1.1, 1.2, 1.3, 1.5. Micropráctica que integra: 1.1 (2,3) · 1.2 (2,3) · 1.3 (3,4) · 1.5 (2).
- Distinto de: S1, S4, S9: otras tablas, otros filtros; añade columna calculada, IN/OR con paréntesis y descripción de esquema.
- Tareas:
  - a) Los 5 productos de Snacks más baratos: nombre, precio y precio_con_iva (precio×1,13 con 2 decimales); desempate por producto_id.
  - b) Clientes de la ruta R02 que sean Farmacia o Kiosco (cliente_id, nombre_negocio, tipo).
  - c) Los 5 productos de inventario donde las salidas superan al stock final, con la diferencia, de mayor a menor.
  - d) Describe `visitas` con PRAGMA table_info y explica en 2 frases qué es una fila y qué significan planificada, realizada y pedido_tomado.
- Contrato de resultado: a 5×3 · b 6×3 · c 5×4 · d por rúbrica.
- Realismo del tiempo: 3 consultas de ~4 min + 1 descripción de ~8 min + lectura ~5 min = 25 min en primera vez.
- Entregable: mi_trabajo/sql/SQ01.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ02 · D12 · 25 min · nivel 1/3 · etapa Inicial
- Prerrequisitos: lecciones 1.4, 1.6, 2.4. Micropráctica que integra: 1.4 (2,3) · 1.6 (2,4).
- Distinto de: S6, S7: trampa de NULL con negación y pares DISTINCT, no vistos en los S.
- Tareas:
  - a) Clientes de la ruta R03 con zona conocida.
  - b) Clientes cuya zona no es 'Centro' sin perder los de zona vacía; explica en una frase por qué `zona <> 'Centro'` solo no basta.
  - c) Clientes cuyo nombre contiene 'Rosa'.
  - d) Parejas distintas (tipo, ruta) y cuántas hay.
- Contrato de resultado: a 14×3 · b 103×3 · c 10×2 · d 24×2 + cifra 24.
- Realismo del tiempo: 4 consultas cortas de ~4 min + 2 frases ~4 min + lectura ~5 min = 25 min.
- Entregable: mi_trabajo/sql/SQ02.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ03 · D12 · 15 min · nivel 1/3 · etapa Intermedia
- Prerrequisitos: lecciones 2.1, 2.2. Micropráctica que integra: 2.2 (3).
- Distinto de: G5, G6: otra tabla (visitas) y comparación entre dos agregados dentro de HAVING.
- Tareas:
  - a) Pedidos por estado.
  - b) Unidades por producto con 4.500 o más (mayor a menor).
  - c) Fechas de visitas donde lo realizado es menor que lo planificado.
- Contrato de resultado: a 2×2 · b 3–6×2 (umbral calibrado en Fase 3) · c 4×3.
- Realismo del tiempo: 3 consultas de GROUP BY de ~4 min + lectura ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ03.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ04 · D15 · 15 min · nivel 2/3 · etapa Relacional
- Prerrequisitos: lecciones 3.2, 2.4, 2.1. Micropráctica que integra: (sustituye el repaso de J2, D15).
- Distinto de: J1, J2: ventas por ruta y mes (J2 es el total global); añade filtro por mes y control de cuadre.
- Tareas:
  - a) Ventas entregadas de septiembre de 2026 por ruta del cliente (JOIN de pedidos, ítems y clientes).
  - b) Total de septiembre sin agrupar y comprobación a mano de que la suma de (a) coincide.
- Contrato de resultado: a 6×2 · b 1×1 (300.922,00).
- Realismo del tiempo: 2 consultas con 3 tablas ~6 min c/u + control ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ04.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ05 · D17 · 15 min · nivel 2/3 · etapa Intermedia
- Prerrequisitos: lecciones 2.2, 2.3, 2.5. Micropráctica que integra: 2.3 (denominadores).
- Distinto de: G1, G5: denominador por grupo, no global; CASE dentro de agregado.
- Tareas:
  - a) Pedidos por vendedor y estado.
  - b) Porcentaje de pedidos anulados por vendedor con 1 decimal (CASE dentro de SUM).
  - c) Vendedores con más de 4,5 % de anulados (HAVING con la misma expresión).
- Contrato de resultado: a 12×3 · b 6×2 · c 2×2.
- Realismo del tiempo: 3 consultas de ~4 min + lectura ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ05.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ06 · D23 · 15 min · nivel 2/3 · etapa Relacional
- Prerrequisitos: lecciones 3.2, 2.2. Micropráctica que integra: 3.2 (2).
- Distinto de: J3/J4: cadena de 4 tablas y conteo de pedidos distintos, no filas de ítems.
- Tareas:
  - a) Las 5 combinaciones categoría × ruta con más unidades entregadas (4 tablas).
  - b) Pedidos entregados por tipo de cliente (COUNT DISTINCT).
- Contrato de resultado: a 5×3 · b 5×2.
- Realismo del tiempo: 1 consulta de 4 tablas ~8 min + 1 de ~5 min + lectura ~2 min = 15 min.
- Entregable: mi_trabajo/sql/SQ06.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ07 · D24 · 15 min · nivel 2/3 · etapa Relacional
- Prerrequisitos: lecciones 3.3. Micropráctica que integra: 3.3 (2).
- Distinto de: J5, E8: ausencia en una tabla de hechos distinta (visitas) con condición en el ON.
- Tareas:
  - a) Clientes sin ninguna visita realizada.
  - b) Por ruta, cuántos clientes no tuvieron ninguna visita con pedido tomado.
- Contrato de resultado: a 24×2 · b 6×2.
- Realismo del tiempo: 2 anti-joins de ~6 min + explicación ~2 min + lectura ~1 min = 15 min.
- Entregable: mi_trabajo/sql/SQ07.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ08 · D25 · 15 min · nivel 2/3 · etapa Relacional
- Prerrequisitos: lecciones 3.4, 3.2. Micropráctica que integra: 3.4 (todos).
- Distinto de: DB03 (Pandas) y 3.4: aquí en SQL con cifras que el estudiante verifica.
- Tareas:
  - a) Total entregado por la vía directa (ítems y pedidos).
  - b) El mismo total uniendo además con visitas por cliente_id: ¿por qué cambia? (2 frases) y corrígelo agregando antes de unir.
  - c) Cuántas filas produce la unión pedidos–visitas.
- Contrato de resultado: a 1×1 (1.468.924,50) · b muestra el inflado · c 1×1 (14.400).
- Realismo del tiempo: 3 consultas cortas ~3 min + explicación y corrección ~5 min + lectura ~1 min = 15 min.
- Entregable: mi_trabajo/sql/SQ08.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ09 · D26 · 15 min · nivel 3/3 · etapa Analítica
- Prerrequisitos: lecciones 2.5. Micropráctica que integra: 2.5 (1,3).
- Distinto de: CL3, N14, V4: CASE/COALESCE sobre clientes y visitas, sin ABC.
- Tareas:
  - a) Clientes por clase antigua/reciente (fecha_alta antes de 2026-01-01).
  - b) Clientes por zona mostrando 'Sin zona' para los vacíos (COALESCE).
  - c) Efectividad por ruta = pedido_tomado / realizada con NULLIF y 1 decimal.
- Contrato de resultado: a 2×2 · b 8×2 · c 6×2.
- Realismo del tiempo: 3 consultas de ~4 min + lectura ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ09.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ10 · D30 · 15 min · nivel 3/3 · etapa Analítica
- Prerrequisitos: lecciones 4.1. Micropráctica que integra: 4.1 (1,3).
- Distinto de: K3: subconsulta escalar en WHERE y en HAVING, otras columnas.
- Tareas:
  - a) Productos con precio mayor al promedio general.
  - b) Los 10 clientes con más pedidos entregados que el promedio de pedidos por cliente.
- Contrato de resultado: a 15×3 · b 10×2.
- Realismo del tiempo: a ~5 min; b (subconsulta anidada) ~8 min; lectura ~2 min = 15 min.
- Entregable: mi_trabajo/sql/SQ10.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ11 · D30 · 15 min · nivel 3/3 · etapa Analítica
- Prerrequisitos: lecciones 4.2, 3.2. Micropráctica que integra: 4.2 (2).
- Distinto de: N1 (todos los meses, 80 min) y V3: un solo mes y una CTE; sin ventanas.
- Tareas:
  - a) Cumplimiento de septiembre por ruta contra presupuesto con una CTE de ventas.
  - b) Los 5 clientes con más ventas entregadas con una CTE.
- Contrato de resultado: a 6×5 · b 5×2.
- Realismo del tiempo: a ~9 min; b ~4 min; lectura ~2 min = 15 min.
- Entregable: mi_trabajo/sql/SQ11.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ12 · D32 · 15 min · nivel 3/3 · etapa Analítica
- Prerrequisitos: lecciones 4.2, 4.3. Micropráctica que integra: 4.3 (2).
- Distinto de: V5 (mejores 3 clientes por ruta) y V3: partición por categoría de producto.
- Tareas:
  - Los 2 productos con más unidades entregadas en cada categoría (ROW_NUMBER con PARTITION BY; desempate por nombre).
- Contrato de resultado: 10×4.
- Realismo del tiempo: 1 consulta con CTE + ventana ~12 min + lectura ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ12.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ13 · D33 · 15 min · nivel 2/3 · etapa BI/Data Engineering
- Prerrequisitos: lecciones 3.3, 3.4, 2.4. Micropráctica que integra: —.
- Distinto de: N8, N14: controles de calidad sobre comercial.db en formato de lista de verificación.
- Tareas:
  - a) Clientes con espacios sobrantes en el nombre (conteo).
  - b) Clientes sin zona por ruta.
  - c) Ítems sin pedido (debe dar 0).
  - d) Pedidos sin cliente (debe dar 0). Explica qué significa un 0 en un control.
- Contrato de resultado: a 1×1 (8) · b 2×2 · c 1×1 (0) · d 1×1 (0).
- Realismo del tiempo: 4 consultas de ~3 min + explicación ~2 min + lectura ~1 min = 15 min.
- Entregable: mi_trabajo/sql/SQ13.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ14 · D37 · 15 min · nivel 2/3 · etapa BI/Data Engineering
- Prerrequisitos: lecciones 2.3, 4.2, 3.2. Micropráctica que integra: —.
- Distinto de: SQ08/V3: conciliación de una carga, útil para C06.
- Tareas:
  - a) Pedidos totales, entregados y anulados en una fila y comprobación de que cuadran.
  - b) Suma de las ventas mensuales frente al total directo: deben coincidir.
- Contrato de resultado: a 1×3 (3600/3442/158) · b 1×2 (1.468.924,50 ambos).
- Realismo del tiempo: 2 consultas ~5 min + comprobación escrita ~4 min + lectura ~2 min = 15 min (a 15 con margen).
- Entregable: mi_trabajo/sql/SQ14.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ15 · D38 · 15 min · nivel 3/3 · etapa BI/Data Engineering
- Prerrequisitos: lecciones 4.2, 4.3. Micropráctica que integra: 4.3 (1,3).
- Distinto de: N6 (ventas acumuladas, 62 min): aquí solo acumulado y porcentaje en una consulta.
- Tareas:
  - Ventas entregadas por mes con acumulado y porcentaje acumulado (SUM OVER).
- Contrato de resultado: 6×4.
- Realismo del tiempo: 1 consulta con CTE + 2 ventanas ~12 min + lectura ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ15.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ16 · D39 · 20 min · nivel 3/3 · etapa BI/Data Engineering
- Prerrequisitos: lecciones 4.3, 6.5. Micropráctica que integra: 6.5 (2,3).
- Distinto de: V4 (ABC de clientes): otra entidad y otra métrica; la consulta debe construirse sin copiar V4.
- Tareas:
  - Clasificación ABC de productos por unidades entregadas (acumulado antes < 80 → A; < 95 → B; resto C) y cuántos productos son A.
- Contrato de resultado: 40×5 + cifra.
- Realismo del tiempo: Consulta con CTE + ventana + CASE ~15 min + lectura ~3 min + conteo ~2 min = 20 min.
- Entregable: mi_trabajo/sql/SQ16.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

### SQ17 · D40 · 15 min · nivel 2/3 · etapa BI/Data Engineering
- Prerrequisitos: lecciones 3.2, 2.4. Micropráctica que integra: —.
- Distinto de: E4/X1: granularidad mes × categoría y control incorporado.
- Tareas:
  - a) Tabla plana mes × categoría con pedidos, unidades y ventas (lista para un tablero).
  - b) Control: la suma de ventas de (a) coincide con el total directo.
- Contrato de resultado: a 30×5 · b 1×1 (1.468.924,50).
- Realismo del tiempo: a ~9 min; b ~3 min; lectura ~3 min = 15 min.
- Entregable: mi_trabajo/sql/SQ17.sql con una consulta por apartado y, donde se pide, 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): compara el conjunto de filas con el contrato; apartados abiertos con rúbrica de 3 criterios.

## Otros ejercicios BASE nuevos

### PT01 · D19 · 25 min · nivel 1/3 · Python
- Competencia: Pruebas con assert (8.7). Prerrequisitos: 8.1, 8.6, 8.7. Datos: tu función clasificar_ticket (P08).
- Distinto de: P08: allí escribes la función; aquí compruebas que tus pruebas detectan errores.
- Tareas:
  - Escribe en `mi_trabajo/python/pruebas_PT01.py` al menos cuatro `assert` de tu P08: caso normal, límite, vacío/ausente e inválido.
  - El corrector ejecuta tus pruebas contra la función correcta y contra tres versiones con un error cada una.
- Entregable: pruebas_PT01.py.
- Corrección: Script corrector (Fase 3) que importa tus pruebas: deben PASAR con la versión correcta y FALLAR con cada versión defectuosa (mutantes).
- Realismo del tiempo: ~20 min para 4 asserts + ~5 min para provocar un error propio.

### KP01 · D29 · 30 min · nivel 2/3 · KPIs
- Competencia: Productividad y variación (6.4). Prerrequisitos: 6.4, 4.2, 4.3, 2.5. Datos: 04_DATASETS/comercial.db.
- Distinto de: J4 (ventas por vendedor) y N5 (crecimiento mensual de 80 min): aquí productividad por día y variación con n/c en una sola práctica corta.
- Tareas:
  - a) Productividad por vendedor = ventas entregadas por día con ventas, redondeo a 2 decimales.
  - b) Variación absoluta y relativa de las ventas entregadas por ruta de agosto a septiembre; mostrar 'n/c' cuando la base sea 0.
- Entregable: mi_trabajo/sql/KP01.sql + 2 frases de interpretación.
- Corrección: Corrector SQL nuevo (Fase 3): contrato de filas y columnas; interpretación con rúbrica.
- Realismo del tiempo: a ~12 min; b ~14 min; interpretación ~4 min.

### PD01 · D18 · 25 min · nivel 2/3 · Pandas
- Competencia: Filtrar, seleccionar y ordenar (9.4). Prerrequisitos: 9.2, 9.3, 9.4. Datos: 04_DATASETS/distribuidora/pedidos.csv y clientes.csv.
- Distinto de: P17 (cargar) y P22/P23: aquí solo selección y filtro combinados.
- Tareas:
  - Define `filtrar_entregas(pedidos, ruta, mes)` que devuelva los pedidos entregados de una ruta y mes con columnas pedido_id, cliente_id y fecha, ordenados por fecha y pedido_id.
  - Compara el número de filas con la consulta SQL equivalente.
- Entregable: función en mi_trabajo/python/mis_funciones.py.
- Corrección: Corrector Python nuevo (Fase 3) con casos y control negativo.
- Realismo del tiempo: función de 3 pasos ~15 min + comparación ~7 min + lectura ~3 min.

### PE01 · D37 · 35 min · nivel 2/3 · Pandas
- Competencia: Errores silenciosos en Pandas (10.6). Prerrequisitos: 9.5, 10.3, 10.5, 10.6. Datos: script roto + CSV de 12 filas (se crean en Fase 3).
- Distinto de: DB03 (solo merge) y DB02 (conversión): PE01 combina merge y groupby en un caso.
- Tareas:
  - Un script termina sin error pero un total sube por un catálogo con clave repetida y otro total baja por un vacío en la columna de agrupación.
  - Encuentra ambas causas, corrígelas (`validate`, `dropna=False` o tratamiento explícito) y añade dos controles de cuadre.
- Entregable: mi_trabajo/depuracion/PE01.py + explicación en errores.md.
- Corrección: Corrector nuevo (Fase 3): ejecuta la función corregida con datos adversos y comprueba totales.
- Realismo del tiempo: diagnóstico ~15 min + corrección ~10 min + controles ~8 min.

### MD01 · D30 · 35 min · nivel 2/3 · Modelado
- Competencia: Diseñar un modelo estrella (13.1–13.2). Prerrequisitos: 13.1, 13.2. Datos: 04_DATASETS/inventario.csv + ventas por producto de comercial.db.
- Distinto de: PB02 (aplica un modelo dado) y 13.2 micro (mini-base): MD01 pide diseñar uno propio.
- Tareas:
  - Define la granularidad, medidas, dimensiones y claves para un hecho 'movimiento de inventario por producto' y su relación con ventas.
  - Indica qué dimensiones se comparten (conformadas) y lista 5 controles de calidad.
- Entregable: mi_trabajo/modelo/MD01.md con tabla de hecho/dimensiones/claves.
- Corrección: Validador estructural nuevo (Fase 3) + rúbrica: grano declarado, claves en la hecho, sin relación hecho–hecho.
- Realismo del tiempo: diseño en papel ~20 min + controles ~10 min + lectura ~5 min.

### GIT01 · D10 · 30 min · nivel 1/3 · Git y portafolio
- Competencia: Git/GitHub práctico (16.1). Prerrequisitos: 16.1. Datos: carpeta de práctica fuera de este repositorio.
- Distinto de: 16.1 micro (carpeta efímera): GIT01 es el repositorio real de portafolio.
- Tareas:
  - Crea un repositorio de portafolio con README (6 secciones), .gitignore (.venv/, *.db y archivos privados) y al menos 2 commits.
  - Revisa `git diff` antes del segundo commit y lista 5 cosas que nunca subirás.
- Entregable: carpeta del repositorio + captura de `git log --oneline`.
- Corrección: Lista de verificación nueva (Fase 3): ≥2 commits, .gitignore correcto, README con secciones y sin credenciales ni datos privados.
- Realismo del tiempo: repositorio ~15 min + README ~10 min + lista ~5 min.

### EX04 · D31 · 35 min · nivel 2/3 · Excel
- Competencia: Fórmulas de cuadre: SUMAR.SI.CONJUNTO y BUSCARX (15.2). Prerrequisitos: 15.1, 15.2, 15.3. Datos: 04_DATASETS/distribuidora/drop_por_pedido.csv + presupuesto.csv.
- Distinto de: EX01 (tabla dinámica): aquí fórmulas, no tabla dinámica.
- Tareas:
  - Con SUMAR.SI.CONJUNTO calcula las ventas por ruta y mes; con BUSCARX trae el presupuesto de cada fila.
  - Crea una columna de diferencia contra tu consulta de SQL y confirma que es 0.
- Entregable: mi_trabajo/excel/EX04.xlsx + lista de cifras de control.
- Corrección: Evidencia manual (Excel no se ejecuta en este paquete): diferencias 0 y capturas; se registra como PE si no se hizo.
- Realismo del tiempo: fórmulas ~20 min + cuadre ~10 min + lectura ~5 min.

### PQ01 · D32 · 50 min · nivel 2/3 · Power Query
- Competencia: Transformaciones reproducibles (14.2). Prerrequisitos: 14.1, 14.2, 15.1. Datos: 04_DATASETS/visitas.csv.
- Distinto de: PB01 (importar y tipos de 9 tablas): PQ01 pide transformaciones y reproducibilidad en una tabla.
- Tareas:
  - Importa visitas.csv, fija tipos, filtra realizada = 1, agrega una columna de semana y quita duplicados por visita_id.
  - Documenta cada paso aplicado y compara filas esperadas (384) con las obtenidas.
- Entregable: pasos de Power Query documentados en mi_trabajo/powerbi/PQ01.md + filas obtenidas.
- Corrección: Evidencia manual: filas = 384 y lista de pasos; se registra como PE si no se ejecutó en Desktop.
- Realismo del tiempo: importar ~10 min + transformar ~25 min + documentar ~10 min + comparar ~5 min.

### PB07 · D33 · 45 min · nivel 2/3 · Power BI
- Competencia: Panel mínimo defendible (14.4 + sección de 14.5). Prerrequisitos: 14.3, 14.4, 14.5. Datos: 05_PROYECTOS/powerbi/datos_modelo + medidas de PB03.
- Distinto de: PB03 (medidas) y PB05 (dos páginas, complementario): PB07 es una sola página validada.
- Tareas:
  - Una página con 4 tarjetas, 2 visuales y un segmentador de ruta; títulos que digan qué, unidad y período.
  - Valida 4 cifras contra SQL, escribe 2 hallazgos con cifra y un dato que faltaría para probar su causa.
- Entregable: mi_trabajo/powerbi/PB07.pbix (si procede) + lista de comprobación manual.
- Corrección: Evidencia manual: 4 cifras coinciden con SQL; marca solo lo que ejecutaste.
- Realismo del tiempo: página ~20 min + validación ~15 min + hallazgos ~10 min.

## Ejercicios REFUERZO nuevos

| ID | Día | Min | Área | Competencia y prerrequisitos | Datos | Tarea | Control | Distinto de |
|---|---:|---:|---|---|---|---|---|---|
| RP01 | D02 | 15 | Python | Funciones y aritmética (7.3, 7.4) (lecc. 7.3, 7.4) | valores en el enunciado | `con_descuento(precio, porcentaje)` con redondeo a 2 decimales; porcentaje fuera de 0–100 devuelve None. | casos del corrector Python | P01: otra regla y caso inválido |
| RP02 | D03 | 20 | Python | Booleanos, None e if (7.6, 7.10) (lecc. 7.6, 7.10) | valores en el enunciado | `clasificar_stock(stock, minimo)` con tres etiquetas y manejo de None. | casos del corrector Python | P02: tres ramas y None de entrada |
| RP03 | D04 | 20 | Python | Bucles y diccionario acumulador (7.9, 7.11, 7.12) (lecc. 7.9, 7.11, 7.12) | lista de tuplas en el enunciado | `unidades_por_categoria(lineas)` que sume unidades por categoría desde tuplas (categoria, unidades). | casos del corrector Python | P06: suma por clave sobre tuplas, no conteo |
| RP04 | D05 | 25 | Python | Registros: lista de diccionarios (7.13) (lecc. 7.13) | lista de diccionarios en el enunciado | `mejor_tienda(registros)` devuelve la tienda con mayor total y el total; lista vacía devuelve None. | casos del corrector Python | P07: máximo con nombre y caso vacío |
| RP05 | D10 | 25 | Python | Archivos CSV y excepciones (8.3, 8.5) (lecc. 8.3, 8.5) | 04_DATASETS/inventario.csv con filas dañadas añadidas en una copia | `leer_inventario(ruta)` devuelve (validas, rechazadas con motivo) y cuadra. | corrector Python con archivo temporal | P13: rechaza filas, no solo lee |
| RS01 | D12 | 25 | Estadística | Frecuencias y porcentajes (11.1, 11.2) (lecc. 11.1, 11.2) | 04_DATASETS/comercial.db (clientes.tipo) | Tabla de frecuencias de `tipo` a mano, verificación con Python y comprobación de que suma 100. | control numérico | ST01: variable categórica, no medidas de centro |
| RD01 | D17 | 25 | Pandas | Filtrar, seleccionar y ordenar (9.4) (lecc. 9.4) | 04_DATASETS/inventario.csv | Productos con salidas mayores que el stock final, columnas elegidas y orden por diferencia; comparar con SQL. | corrector Python | PD01: otra tabla y otra condición |
| RS02 | D18 | 30 | Estadística | Centro y dispersión (11.3, 11.4) (lecc. 11.3, 11.4) | 04_DATASETS/distribuidora/drop_por_pedido.csv (una ruta) | Media, mediana, desviación y coeficiente de variación de una ruta; elige la medida típica y justifícalo. | controles estadísticos + rúbrica | ST01: otra ruta y decisión de medida |
| RD02 | D23 | 35 | Pandas | Fechas y dinero con formatos mixtos (9.6) (lecc. 9.6) | CSV de 15 filas con fechas ISO/DD-MM y montos con coma | Limpia fechas y montos, separa inválidos y cuadra conteos. | corrector Python | ME02: sin contrato completo, solo limpieza |
| RS03 | D25 | 30 | Estadística | Percentiles y atípicos (11.5) (lecc. 11.5) | drop_por_pedido.csv (otra ruta) | Q1, Q3, IQR, cercas de Tukey y atípicos de una ruta; compara con Pandas. | controles estadísticos | ST02: otra ruta y verificación cruzada |
| REL1 | D26 | 35 | ETL | Añadir una regla sin romper el cuadre (5.3, 5.4) (lecc. 5.3, 5.4) | 04_DATASETS/mini_etl/ventas_mini_raw_v2.csv | Agrega una regla de rechazo a tu mini-ETL y comprueba la ecuación de conteos. | corrector del mini-ETL (existente) | ME04: otra regla y archivo |
| RM01 | D30 | 30 | Modelado | Estrella para visitas (13.1, 13.2) (lecc. 13.1, 13.2) | 04_DATASETS/visitas.csv | Diseña `fact_visitas` conformada con dim_cliente y dim_fecha; lista de controles. | validador estructural | MD01: otro hecho |
| RE01 | D31 | 35 | Excel | Cuadre con SUMAR.SI.CONJUNTO (15.2) (lecc. 15.2) | 04_DATASETS/presupuesto.csv | Cumplimiento por ruta y mes con fórmulas y cuadre contra tu SQL. | evidencia manual | EX04: otro conjunto |
| RQ01 | D32 | 40 | Power Query | Tipos y nulos reproducibles (14.2) (lecc. 14.2) | 04_DATASETS/inventario.csv | Importar, tipar, tratar nulos y documentar pasos. | evidencia manual | PQ01: otra tabla |
| RB01 | D33 | 35 | DAX | CALCULATE con filtro (14.3) (lecc. 14.3) | 05_PROYECTOS/powerbi/datos_modelo | Medida de ventas de una categoría y mes con CALCULATE, validada contra SQL. | evidencia manual | PB03: filtro explícito |
| RS04 | D37 | 30 | Estadística | Intervalo de confianza (12.2) (lecc. 12.2) | drop_por_pedido.csv (ruta R05) | IC 95 % del drop medio y comparación con una meta dada. | controles estadísticos | ST05: IC de una sola ruta |
| RS05 | D39 | 30 | Estadística | Hipótesis y p-valor (12.3, 12.4) (lecc. 12.3, 12.4) | drop_por_pedido.csv (dos rutas) | Prueba de permutación con p-valor y conclusión de negocio. | controles estadísticos + rúbrica | ST05: p-valor por permutación |
| RS06 | D40 | 35 | Estadística | Welch y tamaño del efecto (12.5) (lecc. 12.5) | drop_por_pedido.csv (dos rutas) | Welch, IC de la diferencia y tamaño del efecto con conclusión de negocio. | controles estadísticos + rúbrica | ST05: otros datos y tamaño del efecto |

## Contratos SQL verificados (forma del resultado)

| Consulta | Filas | Columnas | Huella |
|---|---:|---|---|
| SQ01a | 5 | nombre, precio_unitario, precio_con_iva | 9a7fd17a45 |
| SQ01b | 6 | cliente_id, nombre_negocio, tipo | 7a19ed0798 |
| SQ01c | 5 | producto_id, salidas_unidades, stock_final, diferencia | 159fe9e6fb |
| SQ02a | 14 | cliente_id, nombre_negocio, zona | b965645669 |
| SQ02b | 103 | cliente_id, nombre_negocio, zona | 7f9f4d8496 |
| SQ02c | 10 | cliente_id, nombre_negocio | 25a1bc3880 |
| SQ02d | 24 | tipo, ruta | 946e473a05 |
| SQ03a | 2 | estado, pedidos | a4c968b18f |
| SQ03b | 27 | producto_id, unidades | bd8b55a755 |
| SQ03c | 4 | fecha, plan, real | de75d4c5d5 |
| SQ04a | 6 | ruta, ventas_bs | f91686aaee |
| SQ04b | 1 | total_bs | c9d1569eac |
| SQ05a | 12 | vendedor_id, estado, pedidos | 8ada44e596 |
| SQ05b | 6 | vendedor_id, pct_anulados | f123d49d68 |
| SQ05c | 2 | vendedor_id, pedidos | a7c39079f0 |
| SQ06a | 5 | categoria, ruta, unidades | 33f3f00bdd |
| SQ06b | 5 | tipo, pedidos | 32d9740688 |
| SQ07a | 24 | cliente_id, nombre_negocio | c1c55f27c0 |
| SQ07c | 6 | ruta, clientes_sin_pedido_tomado | 55d5a10887 |
| SQ08a | 1 | total_bs | dc7cb21da9 |
| SQ08b | 1 | total_bs | c44f5394a7 |
| SQ08c | 1 | filas_unidas | 005161611f |
| SQ09a | 2 | clase, clientes | c5cdde8a89 |
| SQ09b | 8 | zona, clientes | 5c4b7a32ad |
| SQ09c | 6 | ruta, efectividad | e34402335a |
| SQ10a | 15 | producto_id, nombre, precio_unitario | 263df765e3 |
| SQ10b | 10 | cliente_id, pedidos | 60b77e7a87 |
| SQ11a | 6 | ruta, mes, ventas, presupuesto_bs, cumplimiento | 6adb6033c6 |
| SQ11b | 5 | cliente_id, ventas | d3402d39ed |
| SQ12a | 10 | categoria, nombre, unidades, pos | dc5f32d3d0 |
| SQ13a | 1 | nombres_con_espacios | c5d72503b6 |
| SQ13b | 2 | ruta, sin_zona | 9ed482abc7 |
| SQ13c | 1 | items_sin_pedido | db407f11d7 |
| SQ13d | 1 | pedidos_sin_cliente | db407f11d7 |
| SQ14a | 1 | pedidos, entregados, anulados | 482f62450f |
| SQ14b | 1 | suma_meses, total_directo | fb7e6a5544 |
| SQ15a | 6 | mes, ventas, acumulado, pct_acumulado | 27179437f1 |
| SQ16a | 40 | producto_id, nombre, unidades, acum_antes, clase | 258bf37349 |
| SQ17a | 30 | mes, categoria, pedidos, unidades, ventas_bs | 55fab86e36 |
| SQ17b | 1 | control | dc7cb21da9 |
