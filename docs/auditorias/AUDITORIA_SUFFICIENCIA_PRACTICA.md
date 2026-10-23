# Auditoría de suficiencia práctica · Plan Data & BI V5

Alcance: muestra D04, D05 y D08–D13. Se conserva el curso y el progreso; no se declara acreditada una competencia por editar su guía. La distribución global es propuesta, no implementación terminada. No se han creado ejercicios autónomos nuevos.

## Qué se cuenta

- Un ID original se cuenta una vez como recurso, aunque sirva a varias competencias. Las filas por competencia no son sumables para obtener un total de ejercicios.
- Un ejemplo resuelto y su comprobación posterior no cuentan como práctica autónoma. Los notebooks N01–N03 conservan su obligación guiada íntegra y se contabilizan aparte.
- Se han hecho obligatorias **30 microprácticas existentes**, localizadas por su lección, jornada y ancla. No son 30 ejercicios autónomos nuevos ni se cuentan sus apartados como otros tantos IDs independientes.
- La fuente contiene 18 IDs pendientes de ejercicios originales en la ruta de la muestra: G1/G5/G6/G7/P07/P08/G8/J1/J2/J3/DB01/P09/P13/J4/J5/ST01/P10/P11. DB01 tiene código inicial y funciona también como práctica equivalente de 19.1; cuenta una vez.
- Se conservan los ejercicios G3/P06 ya completados y G2 completado de refuerzo, sin volver a exigirlos ni sumarlos a la carga pendiente. Las dos lecturas completas D04 siguen marcadas; las micros son pendientes.
- Los seis AN02–AN07 se cuentan como aplicaciones de criterio originales diferenciadas de ejercicios de programación. H02/S02 mantienen sus contratos originales D13; no son nuevas evaluaciones.
- S3/S5 ya completados D03 permanecen históricos obligatorios, sin nueva deuda. Los ocho ejercicios históricos restaurados dentro de muestra y las nueve obligaciones futuras constan en el inventario.
- Las lecciones que contienen ejemplos resueltos no equivalen a otras tantas tareas autónomas. Tampoco se acredita Desktop por una simulación Python.

IM = incorporado a fuente y guía de muestra; el estudiante aún debe realizarlo. H = evidencia histórica conservada. P/NA = propuesta fuera de muestra, no implementada ni acreditada.

## Suficiencia por competencia implementada

Los números de apartados son inventario del trabajo existente, no una cuota ni equivalencia automática de dificultad. La comprobación debe exigir intento previo, resultado propio, explicación y casos límite cuando correspondan.

| Competencia | Ejercicios originales relacionados | Microprácticas NÚCLEO | Autónomos nuevos | Variantes / decisiones diferentes | Evaluación posterior | Justificación y estado |
|---|---|---|---:|---|---|---|
| Tabla/fila/columna/tipo/clave | S1 H; G3 H; J1 posterior | 1.1 D04: 3 apartados | 0 | Identificar unidad, tipo y clave en tablas distintas | S01 original; explicación del grano en S02 | Cobertura inicial explícita; no presumir dominio histórico. IM |
| SELECT/FROM/alias/expresión | S1 H; G3 H; G1/G5 | 1.2 D04: 3 | 0 | Selección simple, alias, columna calculada | S01 original | Varias decisiones antes de agregar; resultado y explicación aún pendientes. IM |
| WHERE/comparación/AND/OR/IN/BETWEEN | S3/S5 H; S4/S6 H | 1.3 D04: 4 | 0 | Tipo; categoría y precio; lista IN; rango con condición | S01 filtro/variante/diagnóstico | Cuatro problemas existentes distintos; NOT y paréntesis se enseñan, pero no se declara práctica autónoma repetida de cada operador. IM con límite explícito |
| NULL, DISTINCT y LIKE | S7/S2/S6 H; G7/J5 | Micros históricas no se inventan como realizadas | 0 | Grupo sin zona; cliente sin pareja; diferencia NULL/0 | S01 y S02 originales | Varias aplicaciones existen, pero la suficiencia individual histórica requiere evidencia; no aprobar por lectura. H/IM parcial |
| ORDER BY/LIMIT/desempate | S3/S5 H; G5/G6/G8 | 1.5 D04: 3 | 0 | Orden numérico, empate y recorte | S01 original y variantes | Tres tareas cortas existentes más contexto autónomo; no duplicar ID histórico. IM |
| COUNT/SUM/AVG/MIN/MAX | G3/G2 H; G1/G5/G7 | 2.1 D04: 4 | 0 | Contar filas frente a valores; total/promedio/extremos; filtro | S01 original | Cuatro apartados más ejercicios empresariales; cada función debe explicarse, no solo resultado total. IM |
| GROUP BY/HAVING | G1/G5/G6/G7: 4 IDs | 2.2 D05: 3 | 0 | Estado; ruta; umbral; combinación tipo-zona; NULL propio | S01 variante y diagnóstico | Grupos de 1/2 claves y HAVING con suma/conteo aportan variación; no asumir maestría por contar cuatro IDs. IM |
| Granularidad/denominador/ponderación/cero | P02 H; AN03; G6 | 2.3 D05: 3 | 0 | Cumplimiento diario, efectividad total, importe por unidad | S01/H01 originales | Tres cocientes con denominadores distintos, aplicación y examen después de preparación. IM |
| ROUND/texto/mes/recencia | G8; J2/J3/J4 | 2.4 D09: 4 | 0 | Redondeo al presentar; TRIM; mes-estado; fecha de corte | S02 cuadres original | G8 después de strftime; dinero después de ROUND; no confundir funciones de presentación y cálculo. IM |
| Claves/cardinalidad/INNER JOIN | J1/J2/J3/J4: 4 IDs | 3.2 D09: 3 | 0 | Pedido-cliente; cabecera-detalle; categoría; vendedor de pedido | S02 original | Variaciones de grano y cadenas de unión, control por conteos y sumas. 3.2 cubre equivalente de 3.1. IM |
| LEFT JOIN/ausencia/ON frente WHERE | J5: 1 ID, varias decisiones | 3.3 D11: 3 | 0 | Conservar cero compras, filtro periodo/estado, contar pareja | S02/H02 originales y variantes | Una actividad integrada más tres microcasos y diagnóstico independiente; no recortar J5 a listado mínimo para acreditar. IM |
| Duplicaciones por JOIN | J1/J2/J3/J4/J5 | 3.4 D11: 3 | 0 | Predecir filas; inflación de total; grano y clave repetida | S02 diagnóstico original | Casos distintos de error y cuadres; el mismo JOIN no cuenta dos veces por aparecer en dos listas. IM |
| Variables/asignación | P01/P02 H; P07 | 7.2 D04: 3 | 0 | Estado del valor, actualización, dependencia entre variables | S01 Python original | Recuperación con predicción y ejecución; no atribuirla a D01 por una preparación breve. IM |
| Tipos/aritmética/operadores | P01/P02 H; P07/P09/P11 | 7.3 D04: 4 | 0 | Texto frente número, división, resto y conversión | S01/S02 originales | Variación existente; no equivale a cuatro prácticas de cada operador. IM |
| Funciones/parámetros/return/contratos | P08/P09/P10/P11/P13: 5 IDs | 7.4 D04:3 y 8.1 D08:3 | 0 | IVA, cajas, print/None; vacío/límite/inválido y pureza | S01/S02 originales | Seis microdecisiones y varios contratos autónomos posteriores; retorno probado antes de archivos/ETL. IM |
| Condiciones/lógica/límites | P06 H; P07/P08/P09/P11 | 7.10 D04: 3 | 0 | Clasificación, frontera y rama alternativa | S01/S02 originales | Práctica esencial pendiente aunque lectura/P06 estén completos. IM |
| for/while/recorrido | P06 H; P07/P13 | 7.11 D04: 4 | 0 | Recorrer, repetir, límite y detener | S01 original | Cuatro problemas cortos más función de registros; preservar práctica de bucle, no solo lectura. IM |
| Acumuladores y registros | P07: 1 integrado; P06 H | 7.12 D05:5 y 7.13 D05:4 | 0 | Suma, conteo, mínimo positivo, selección y suma filtrada | S01 variante/diagnóstico/H01 | Nueve apartados con operaciones distintas; se cuentan como dos micros y un ejercicio, no diez ejercicios. IM |
| Listas/diccionarios/tuplas/conjuntos | P04/P05 H; P07 | 7.13 D05:4; micros D03 no se inventan | 0 | Iterar registros, claves faltantes y contar categorías | S01 original | Cobertura aplicable a registros; ampliar tuplas/conjuntos solo cuando un contrato lo necesite. H/IM |
| Texto/limpieza/métodos | P03 H; P09/P10/P13 | 7.5 D08: 4 | 0 | Inmutabilidad, strip, reemplazo, separar/unir | S02 original | Reusa micro completa antes de dinero/CSV; cuatro decisiones, no copia de P03 como tarea nueva. IM |
| Conversiones/vacío/no finito | P08/P09/P11 | 7.7 D08: 4 | 0 | Decimal local, vacío, ValueError y NaN/infinito | S02/adversos originales | Preparación finita antes de P09/P11; resultado correcto y excepción acordada. IM |
| Excepción/Decimal/traceback/depuración | DB01/P09/P11 | 8.5 D09:4; DB01 equivalente de 19.1 | 0 | ValueError; InvalidOperation→ValueError; dato no finito; línea propia | S02 diagnóstico original | La equivalencia guiada de 19.1 no crea otro ID autónomo; recuperación con otro error si falla. IM |
| CSV/JSON/rutas/escritura/lectura | P13/P10 | 8.3 D10: 4 | 0 | Leer precio; contar zona vacía; escribir/leer CSV; archivo ausente | S02 original; ME/ETL futuros | Práctica real con archivos bajo mi_trabajo, datos originales intactos; JSON tiene enseñanza aunque no se declara proyecto autónomo extra. IM |
| Módulos/importaciones/reutilización | P10/P13 | 8.4 D10: 5 | 0 | Biblioteca estándar, módulo propio, importación y ejecución | S02 original | Dos caminos, módulo propio y regla 20AA antes del ETL; no equiparar importar con dominar empaquetado avanzado. IM |
| Pruebas/validación/código modular | P08/P09/P10/P11/P13 y DB01 | 7.4/assert + 8.1/contrato + 8.5/casos | 0 | Casos normales/límite/inválidos; resultado y excepción | S01/S02 originales; S04/S06 futuros | Varias pruebas con propósito; 8.7 no se cuenta como obligación si sigue voluntaria. IM parcial |
| Población/muestra/unidad/variables | ST01; AN01 H | 11.1 D05: 3 | 0 | Clasificar, contar unidad y muestra manual registrada | ST01 criterios originales; CK-DA propuesto | Prepara alcance sin exigir Pandas; aleatorización reproducible por semilla aún no acreditada. IM parcial |
| Frecuencias/proporciones/porcentajes/acumulada | G1/G5/G7; AN03/AN07 | 11.2 D05: 3 | 0 | Categoría, estado y tramo ordenado con denominador | S01 KPI original; CK-DA propuesto | GROUP BY solo no sustituye relativa/acumulada: aquí se calculan explícitamente. IM |
| Media/mediana/moda/extremo | ST01; AN08 posterior | 11.3 D05: 3 | 0 | Centro manual, quitar extremo como experimento, decisión de logística | ST01 criterio original; CK-DA propuesto | Micro y ejercicio autónomo distintos, más aplicación AN08 futura. No se declara evaluación estadística independiente ya creada. IM |
| Rango/varianza/desviación/n frente n−1 | ST01; AN13 posterior | 11.4 D08: 3 | 0 | Tabla de cuadrados, verificación statistics y CV empresarial | ST01 criterio original; CK-DA propuesto | Dos datasets y método manual/automático; decidir divisor, no memorizar std(). IM |
| Ficha KPI/numerador/denominador/ventas | AN02–AN07; G3/J2 | 6.1 D12: 3 | 0 | Definir unidades entregadas, SQL frente csv estándar antes de Pandas, interpretación | S01 original y S05 original posterior | Aplicación empresarial con filtros; no acredita por sí sola frecuencia ni activos. IM parcial |
| Series/DataFrame/lectura inicial | P17 posterior; N01 futuro guiado | 9.2 D12: 4 | 0 | Construir, leer, asignar/comprobar columna y validar forma | S03 original posterior | Inicio preparado; 9.3/10.x todavía requieren implementación global. IM parcial |

## Registro exacto de microprácticas de muestra

| ID | Lección existente | Jornada | Minutos pendientes | Apartados existentes |
|---|---|---|---:|---:|
| MP-D04-1_1 | 1.1 | D04 | 25 | 3 |
| MP-D04-1_2 | 1.2 | D04 | 30 | 3 |
| MP-D04-1_3 | 1.3 | D04 | 30 | 4 |
| MP-D04-1_5 | 1.5 | D04 | 25 | 3 |
| MP-D04-2_1 | 2.1 | D04 | 30 | 4 |
| MP-D04-7_2 | 7.2 | D04 | 30 | 3 |
| MP-D04-7_3 | 7.3 | D04 | 30 | 4 |
| MP-D04-7_4 | 7.4 | D04 | 35 | 3 |
| MP-D04-7_10 | 7.10 | D04 | 30 | 3 |
| MP-D04-7_11 | 7.11 | D04 | 35 | 4 |
| MP-D05-2_2 | 2.2 | D05 | 35 | 3 |
| MP-D05-2_3 | 2.3 | D05 | 30 | 3 |
| MP-D05-7_12 | 7.12 | D05 | 42 | 5 |
| MP-D05-7_13 | 7.13 | D05 | 40 | 4 |
| MP-D05-11_1 | 11.1 | D05 | 25 | 3 |
| MP-D05-11_2 | 11.2 | D05 | 25 | 3 |
| MP-D05-11_3 | 11.3 | D05 | 30 | 3 |
| MP-D08-7_5 | 7.5 | D08 | 38 | 4 |
| MP-D08-7_7 | 7.7 | D08 | 40 | 4 |
| MP-D08-8_1 | 8.1 | D08 | 35 | 3 |
| MP-D08-11_4 | 11.4 | D08 | 35 | 3 |
| MP-D09-2_4 | 2.4 | D09 | 30 | 4 |
| MP-D09-3_2 | 3.2 | D09 | 35 | 3 |
| MP-D09-8_5 | 8.5 | D09 | 45 | 4 |
| MP-D10-8_3 | 8.3 | D10 | 40 | 4 |
| MP-D10-8_4 | 8.4 | D10 | 40 | 5 |
| MP-D11-3_3 | 3.3 | D11 | 35 | 3 |
| MP-D11-3_4 | 3.4 | D11 | 30 | 3 |
| MP-D12-6_1 | 6.1 | D12 | 35 | 3 |
| MP-D12-9_2 | 9.2 | D12 | 35 | 4 |

Total: 30 microprácticas existentes obligatorias, 1000 minutos de práctica estimada en fuente. El total no incluye teoría, ejercicios, empleo ni cierre; el consolidado de muestra se documenta en DISTRIBUCION_PEDAGOGICA_FINAL.md. No es tiempo medido ni aprendizaje aprobado.

Ampliaciones de preparación dentro de los recursos existentes: 8.4 conserva sus cuatro apartados y añade un quinto para la regla contractual 20AA frente a %y, con predicción y fecha imposible antes de P10. La micropráctica 6.1 usa SQL y csv.DictReader ya enseñado para calcular el KPI antes de Pandas; requiere 35 minutos. La lección 9.2 explica asignar y comprobar una columna calculada antes de su micropráctica, sin depender ocultamente de 10.1. Son ampliaciones de enseñanza/micropráctica existente: **cero ejercicios autónomos nuevos**.

## Competencias futuras: práctica disponible y brechas todavía abiertas

| Competencia | Ejercicios originales disponibles | Microprácticas obligatorias propuestas | Autónomos nuevos creados | Variantes y evaluación | Evidencia de suficiencia / límite |
|---|---|---|---:|---|---|
| Pandas filtros/tipos/faltantes/duplicados | P17/P19/P22/P23 | 9.3/9.4/9.5/9.6/10.1 y PD-BASE sin doble conteo | 0 | Dataset limpio/sucio/conflicto; S03 original | Recursos suficientes para diseñar recorrido; fuera muestra aún no implementado ni acreditado |
| Pandas calculadas/groupby/merge/cardinalidad/exportación/ETL | P20/P21/P24/P25 y ME/ETL | 10.1/10.2/10.3/10.4 + PD-AGR | 0 | Catálogo repetido/huérfano; S03/H03; C06 | Una integración sirve si contiene decisiones y controles independientes; N01/N02/N03 guiados aparte |
| Percentiles/IQR/atípicos/histograma/distribución | ST02/ST03/AN13/EX03 | 11.5/11.6 | 0 | Diferentes unidades, cuantiles y dos criterios; CK-DA propuesto | Variación disponible; falta programarla y corregir criterio que confunde asimetría cero con normalidad |
| Muestreo/sesgo/correlación/causalidad | ST04 | 11.7/11.8 | 0 | Muestra proporcional, semilla, unidad y factor; CK-DA propuesto | Ejercicio integrado de cinco decisiones más micros; no son cinco IDs; no afirmar suficiente por existir archivo |
| Variabilidad/error estándar/IC | ST05 parte IC; ST07 interpretación | 11.8 y 12.1/12.2 | 0 | Simular tamaños, cuenta manual y contexto empresarial; CK-STI propuesto | Recursos reales existen; falta obligatoriedad/ejecución/evaluación independiente |
| Hipótesis/alpha/errores I-II/p/Welch/efecto/independencia/límites | ST05 y ST07 | 12.3/12.4/12.5; secciones adecuadas 12.7/12.8 | 0 | ST05 cuatro entregables; ST07 tres afirmaciones y diseño; CK-STI propuesto | ST05 será obligatorio en propuesta; ST07 condicionado; no evaluar inferencia como contenido nuevo dentro de S05 |
| Contingencia/chi-cuadrado/esperados/V Cramér | ST06 | 12.6 y sección V 12.7 voluntarias | 0 | Tabla, supuestos y efecto | Ampliación voluntaria por instrucción posterior; no requisito oculto |
| Excel tablas/referencias/tipos/limpieza | ME04/EX01 | 15.1 | 0 | Importación real y cuadre | No basta lectura; fuente restaura ME04 pendiente; guías futuras no regeneradas |
| Excel SI/SUMAR.SI.CONJUNTO/CONTAR.SI.CONJUNTO/búsqueda/claves/no encontrado | EX01–03 cubren parte; búsquedas requieren más aplicación propia | 15.2 | 0 | Caso integrado EX04 solo propuesto | Brecha real de autonomía de fórmulas y casos no encontrado/duplicado; pendiente aprobación |
| Excel dinámica/conciliación/SQL | EX01/EX02/EX03 | 15.3 | 0 | Rutas, presupuesto ponderado y percentiles; S05 Parte B original | Tres aplicaciones distintas existen; ejecución Excel y evidencia manual pendientes |
| Power Query tipos/cultura/limpieza/transformación | PB01 importación parcialmente; PB06 actualización | 14.2 necesita convertir papel/Pandas en práctica real | 0 | PQ01 propuesto | Falta tarea autónoma real suficiente de Power Query: no se certifica por equivalencia Python |
| Power Query anexión/combinación/cardinalidad/actualización/reconciliación | Ningún ejercicio específico integrado de todo el recorrido | 14.2 por completar | 0 | Dos archivos, catálogo repetido, conteos y refresh en PQ01 propuesto | Anexión solo definida; brecha permanece hasta aprobar/ejecutar PQ01 |
| DAX modelo/relación/filtros/medidas/CALCULATE | PB01/PB02/PB03; H07 | 13.2/14.1/14.3 | 0 | Contextos total/ruta/mes; S05 Parte B original | Casos existentes suficientes para base si se cumplen completos; alcance mínimo legado no cubre todo |
| DAX ventas/pedidos/clientes/ticket/frecuencia | PB03 completo | 14.3/14.4 | 0 | Cinco medidas y denominadores; CK-BI propuesto | Requerir clientes/frecuencia y contraste SQL; no confundir tres medidas mínimas con cinco |
| Calendario/tiempo/presupuesto/cumplimiento | PB04 | 13.3/14.4 | 0 | Mes inicial BLANK, filtro de calendario/mes, producto parcial | Integrado y con casos límite; enseñanza anterior y ejecución Desktop pendientes |
| Dashboard/gerencia/actualizar/validar | PB05/PB06 | 14.5/6.6 | 0 | Dos páginas, dos hallazgos, cuatro cuadres y refresh | Dos casos amplios pueden bastar si completos; CK-BI propuesto comprueba transferencia |
| KPI ticket/frecuencia/activos/crecimiento/presupuesto/ABC | K1/V2/V4/N1/N5/N7/N9/N12 y AN | 6.2/6.3/6.4/6.5/6.6 | 0 | Corte/ventana/sin compras/ponderación/ranking | Ticket sí tiene equivalencias; frecuencia/activos requieren enseñanza y práctica propias. Fuera muestra no acreditado |
| ETL/ELT/capas/calidad/rechazos/trazabilidad/reconciliar | ME01–04, ETL-1–6, C06-0–4 | 5.1–5.5/19.3/19.4 según equivalencia | 0 | Datos diferentes, adversos, segunda ejecución, defensa | Proyectos integrados contienen múltiples decisiones; conservar contratos/correctores; S04–S06/final privada intactos |
| DW/OLTP/OLAP/mart/estrella/hechos/dimensiones/grano/natural-sustituta/historia | PB02 aplica parte del modelo; no cubre toda la arquitectura DW | 13.2 real + complemento introductorio 13.1 | 0 | DW01 solo propuesto | No duplicar 13.1 entera: 13.2 cubre equivalente de hechos/dimensiones/grano. Falta distinguir arquitecturas y claves/historia |

## Seis propuestas individuales para aprobación

No se crean archivos de ejercicios, no se añaden casillas ni se contabilizan estos minutos como carga obligatoria implementada. La tabla presenta trabajo concreto y su volumen para decidir antes de crear enunciados. Las ampliaciones de ejemplos y micros existentes no son un lote encubierto de nuevos ejercicios autónomos.

| ID propuesto | Brecha concreta | Trabajo distinto y datos reutilizados | Prerrequisitos / destino propuesto | Corrección después del intento | Minutos primera vez | Estado |
|---|---|---|---|---|---:|---|
| EX04 | Aplicación autónoma de fórmulas condicionales y búsquedas con claves | Libro mini-base: suma/conteo de dos criterios, búsqueda de ruta, ID sin pareja y catálogo duplicado; diferencia frente SQL | 15.1/15.2 y claves; después de EX01, D31 o sesión posterior preparada | Fórmulas visibles, casos normales/límite/error, cuadre independiente; BUSCARX e INDICE+COINCIDIR alternativos | 90–130 | PENDIENTE DE APROBACIÓN; no creado |
| PQ01 | Ejecución real de Power Query, especialmente anexión | Dos CSV existentes separados por periodo: importar/cultura/tipos/limpieza, anexar, combinar catálogo m:1, detectar duplicado, actualizar y reconciliar | JOIN/cardinalidad, 14.1/14.2; D32 en sesiones retomables | Pasos aplicados y archivo real, conteos antes/después, valor local y refresh; Python solo control independiente | 100–150 | PENDIENTE DE APROBACIÓN; no creado |
| DW01 | OLTP/OLAP/DW/Data Mart, claves naturales/sustitutas e historia | Diseñar modelo comercial existente y cambio de ruta de un cliente: comparar consulta operativa/analítica, definir grano y vigencias | Complemento introductorio 13.1 y 13.2; D37 | Rúbrica de grano/claves/relaciones y límites históricos, sin requerir SCD avanzado | 60–90 | PENDIENTE DE APROBACIÓN; no creado |
| CK-DA | Evaluación independiente de descriptiva después de práctica | Tabla pequeña existente con otra unidad: población/muestra, centro/dispersión/percentil y recomendación; cálculo manual y comprobación posterior | 11.1–11.8 necesarias y ST01–ST04; D22 después de su preparación | Rúbrica separada, cifras reservadas al final, interpretación y límites; no altera S01–S06 | 30–45 | PENDIENTE DE APROBACIÓN; no creado |
| CK-STI | Evaluación introductoria de inferencia y lectura crítica | Datos piloto existentes: error estándar/IC, hipótesis, lectura del p, diferencia económica e independencia; no exigir chi-cuadrado | Microprácticas 12.x y ST05; ST07 preparado; D39 en bloque separado | Rúbrica propia de método/interpretación/limitaciones; resultado por API no basta | 35–50 | PENDIENTE DE APROBACIÓN; no creado |
| CK-BI | Transferencia de modelo/contexto/tiempo/refresh y conciliación real | Modelo comercial existente con otro filtro: relaciones, medida, mes inicial/BLANK, presupuesto en su grano y refresh sin duplicar | EX/PB01–PB06 completos; D40 separado de S06 | Evidencia real Excel/Desktop, filtro visible, SQL y límites; sin herramientas queda pendiente | 45–60 | PENDIENTE DE APROBACIÓN; no creado |

**Volumen total propuesto: 6 actividades nuevas, 360–525 minutos (6 h–8 h 45 min). Actividades autónomas nuevas creadas: 0.** No es un techo de curso ni se suma a la muestra autorizada. Si se aprueba solo una parte, se documentarán alcance, horas y brechas que permanezcan abiertas.

## Criterios de aceptación y límites de esta auditoría

La suficiencia depende del contenido, no de la cifra 3–5 o 2–4. Para una habilidad simple, los apartados existentes cubren decisiones distintas; para JOIN, funciones, ETL o BI se evalúan además errores, contratos, interpretación y control independiente. Una actividad extensa integrada puede aportar más que varios IDs triviales.

No se declara dominio hasta que el estudiante produzca resultados y los explique sin copiar. Un ejemplo comprobado no cuenta como intento autónomo; una obligación pospuesta conserva su condición; un notebook resuelto no reemplaza P17/P20/P21.

La muestra resuelve obligatoriedad y orden de las prácticas listadas. Permanecen brechas explícitas de evaluación independiente, Power Query real, Excel de fórmulas/búsquedas y DW introductorio, además de implementación global. Las propuestas no justifican certificar hoy esas competencias.

Esta auditoría no afirma que se hayan ejecutado Excel/Power BI Desktop ni aprobado los nuevos checkpoints. Los resultados técnicos, hashes y tiempos finales de la muestra se consignan tras generar y verificar por el flujo principal; aquí no se inventan pruebas ejecutadas.
