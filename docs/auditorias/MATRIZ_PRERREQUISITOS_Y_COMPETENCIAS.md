# Matriz de prerrequisitos y competencias · V5

Estado: muestra D04, D05 y D08–D13. Las fuentes implementadas no acreditan aprendizaje del estudiante. Las prácticas pendientes siguen sin marcar. Fuera de muestra se conserva la obligación canónica, pero la arquitectura, teoría complementaria y guías corregidas son PROPUESTAS NO IMPLEMENTADAS; no se certifica el curso completo.

D01–D03 permanecen byte por byte. D04 mantiene cinco casillas completas vigentes: 2.1, 7.10, G3, P06 y G2; sus minutos nuevos son cero y las nuevas micros no se atribuyen al progreso anterior. S3/S5 ya completados en D03 no crean deuda nueva.

S01–S06 conservan enunciados, criterios, tiempos y puntajes. D06/D13/D20/D27/D34/D41 no reciben contenido obligatorio nuevo. Los checkpoints adicionales requieren aprobación individual y se proponen fuera de esas jornadas. Los seis domingos permanecen descanso.

La fuente de muestra es [nucleo.json](../../01_PLAN_DIARIO/nucleo.json): ruta_integral contiene el orden y los requisitos por ID; sesiones_integrales agrupa sin repetir. L:x.y es enseñanza con ejemplo; MP-Dxx-x_y apunta a la micropráctica ya existente del capítulo. Un ejemplo resuelto, una repetición del mismo ID y un notebook guiado no son tres prácticas autónomas.

## Competencia → preparación → práctica → evaluación

IM = implementado en fuente/guía de muestra, pendiente de realización. H = histórico conservado. P/NA = propuesto, no implementado ni acreditado. V = voluntario.

| Área y competencias completas | Conocimientos previos | Enseñanza NÚCLEO y ejemplo | Micropráctica | Obligatorio / jornada | Evaluación posterior y recuperación | Estado |
|---|---|---|---|---|---|---|
| SQL: tablas, filas, campos, tipos, claves; SELECT/FROM/alias/expresiones; WHERE/comparaciones/AND/OR/NOT/IN/BETWEEN/paréntesis; NULL; DISTINCT/LIKE; ORDER BY/LIMIT | No presumir dominio por preparaciones breves | 1.1 → 1.2 → 1.3 → 1.5 D04; 1.4/1.6 históricas D02/D03 se conservan | MP-D04-1_1/1_2/1_3/1_5; recuperación específica NULL/DISTINCT según evidencia, no micro falsa D03 | G3 histórico; G1/G5/G6/G7 D05; S3/S5 históricos sin nueva deuda | S01 original D06; recuperación del filtro/orden antes de avanzar | IM + H; suficiencia de NULL/DISTINCT no se infiere por lectura |
| SQL: COUNT/SUM/AVG/MIN/MAX; GROUP BY/HAVING; granularidad/denominador; ROUND; texto/fechas/corte | Selección, condición y orden | 2.1 histórico con micro pendiente D04 → 2.2/2.3 D05 → 2.4 D09 | MP-D04-2_1; MP-D05-2_2/2_3; MP-D09-2_4 | G1 estados, G5 ruta, G6 umbral, G7 tipo/zona D05; G8 D09 tras strftime | S01 original; S02 original para cuadres; tres variantes y diagnóstico existentes | IM |
| SQL: claves/cardinalidad/INNER/LEFT/duplicación; CASE/COALESCE; subconsulta/CTE/ventanas; fechas/recencia/frecuencia/KPI | Agregación, grano y NULL | 3.2 D09 → 3.3/3.4 D11; 2.5 P D17; 4.1 → 4.2 → 4.3/4.4 P D18; 6.3 P D19 | MP-D09-3_2 y MP-D11-3_3/3_4; futuras micros completas 2.5/4.x/6.3 | J1 → J2 → J3 D09; J4 D10; J5 D11. K3/V3/V4/V2 futuros conservados | S02 original D13; S03 original D20. K2a/b se ofrecen después de subconsulta/CTE; V2 usa corte/recencia, no exige ventana | IM para JOIN; resto P/NA |
| Python: variables/tipos/operadores/conversión; texto; listas/diccionarios/tuplas/conjuntos; condiciones/bucles/acumuladores | Registros históricos; no atribuir nuevas micros D03 | 7.2 → 7.3 → 7.4 D04; 7.10 histórico + 7.11 D04; 7.12/7.13 D05; 7.5/7.7 D08 | Micros existentes de cada lección; 7.12 tiene cinco decisiones distintas; 7.7 cuatro apartados, incluido no finito | P06 histórico; P07 D05; P08 D08; P09/P11 posteriores | S01 y S02 originales; casos vacío/repetidos/tipo inválido y retorno | IM + H |
| Python: funciones/parámetros/return/contratos; errores/excepciones/trazas; archivos/CSV/JSON/rutas/módulos; pruebas/depuración/validación/modularidad | Variables, texto, colecciones y bucles | 8.1 D08 → 8.5 y 19.1 §1 D09 → 8.3/8.4 D10. 7.7 y 8.5 incluyen finitud/Decimal/InvalidOperation→ValueError | MP-D08-8_1; MP-D09-8_5 cuatro apartados; MP-D10-8_3/8_4. DB01 práctica equivalente de 19.1, sin duplicar conteo | DB01 D09 antes de P09 D10 y P11 D12; P13 D10; P10 D12 | S02/H02 originales; proyecto ME/ETL y adversos de S04/S06 futuros; 8.7 ampliación no acreditada por ID | IM; proyectos fuera muestra P/NA |
| Pandas: Series/DataFrame/lectura/inspección; columnas/filtros/tipos/faltantes/duplicados; transformaciones/calculadas; groupby; merge/cardinalidad/validación/exportación/ETL | CSV, tipos, funciones y claves | 9.2 D12; 9.3 P D15; 9.4/9.5/9.6/10.1 P D16 → 10.2/10.3 P D17 → 10.4 P D18 | MP-D12-9_2; PD-BASE/PD-AGR y futuras micros sin contar dos veces práctica integrada | P17/P19/P20/P21/P22/P23 futuros; N01/N02 completos D17 guiados; N03 perfil/fechas D19 guiado | S03/H03 originales; catálogo duplicado/huérfano/origen intacto. Notebook no sustituye autónomo | IM para 9.2; resto P/NA |
| Descriptiva: unidad/población/muestra/variable; frecuencias/proporciones/porcentajes; media/mediana/moda/rango/varianza/desviación/n frente n−1 | Tabla/fila; división y lista | 11.1/11.2/11.3 D05 manual → 11.4 D08; ejemplo antes de statistics | MP-D05-11_1/11_2/11_3; MP-D08-11_4. Sorteo manual registrado; la reproducción Pandas queda diferida | ST01 D11 después de estadística y módulos; AN08/AN13 posteriores ya existentes | Criterios originales de ST01; CK-DA separado solo propuesto. No hay nuevo examen estadístico S01–S06 | IM, ejecución pendiente |
| Descriptiva: percentiles/cuartiles/atípicos/histograma/distribuciones; muestreo/sesgo; correlación/causalidad | Centro/dispersión y frecuencias | 11.5 P D15 → 11.6 P D18 → 11.7 P D19 → 11.8 P D22 | Micros manuales existentes antes de automatizar | ST02 P D16; ST03 P D19; ST04 P D22, todos tras preparación | CK-DA separado propuesto; no inferir normalidad solo por asimetría cero | P/NA |
| Inferencia: variabilidad/error estándar/estimación/IC; H0/H1/alpha/errores I-II/p; Welch/efecto/independencia/sesgos/limitaciones | Muestreo, centro y dispersión; proporciones | 12.1 P D23 → 12.2 D24 → 12.3 D25 → 12.4 D26 → 12.5 D29 → secciones de 12.7/12.8 D30 | Micros existentes, simulación de tamaños, cuenta manual del IC, lectura del p y comparación económica | ST05 OBLIGATORIO propuesto D33; ST07 general P D39 condicionado a preparación | CK-STI separado P D39, después de ST05; no alterar S05 ni añadir inferencia nueva D34 | P/NA |
| Inferencia: contingencia/chi-cuadrado/esperados/V Cramér | Frecuencias y p | 12.6 y sección V de 12.7 después de sus bases | Opcionales | ST06 voluntario | Sin requisito oculto de ST05/ST07 | V por instrucción posterior |
| Excel: tablas/referencias/tipos/limpieza/condicionales/SUMAR.SI.CONJUNTO/CONTAR.SI.CONJUNTO/búsqueda/claves/no encontrado/dinámica/conciliación/SQL | Fila, tipos, condiciones, grano y claves | 15.1 P D24; 15.2/15.3 P D29; 15.2 ya contiene BUSCARX e INDICE+COINCIDIR | Micros existentes reales; caso integrado EX04 solo propuesto para búsquedas/errores | ME04 P D24; EX01–03 P D31; EX04 requiere aprobación | S05 Parte B original y CK-BI separado propuesto. Excel real; simulación no acredita | P/NA |
| Power Query: importación/tipos/cultura/limpieza/transformación/anexión/combinación/cardinalidad/actualización/reconciliación | CSV, tipos y JOIN | 14.1/14.2 P D32; completar anexión y recorrido de interfaz | Micro actual papel/Pandas insuficiente para ejecución; PQ01 real integrado solo propuesto | PB01 carga y PQ01 propuesto; PB06 actualización posterior | Lista manual/CK-BI separado; archivo/consulta y conteos antes-después pendientes | P/NA |
| BI/DAX: carga/modelado/relación/cardinalidad/filtros/medidas/contexto/CALCULATE/ventas/pedidos/clientes/ticket/frecuencia/calendario/tiempo/presupuesto/cumplimiento/dashboard/validación/refresh/interpretación | Datos limpios, grano y claves; KPI | 13.2/13.3 P D30; 14.1 D32 → 14.3/14.4 D33 → 14.5/6.6 D37 | Micros y PB01–06 completos; no recortar contratos por minutos | PB01/PB02 D32; PB03 D33; PB04 D36 → PB05 D37 → PB06 D38 propuestos | S05 Parte B/H07 originales; CK-BI separado D40 propuesto; todo Desktop manual pendiente | P/NA |
| KPIs comerciales: definición/numerador/denominador/ventas/cobertura/efectividad/ticket/frecuencia/activos/crecimiento/presupuesto/ABC/gerencia | 2.3, estado, fecha/corte y grano | 6.1 D12; 6.2 P D25; 6.3/6.5 P D19; 6.4 P D31; 6.6 P D37 | MP-D12-6_1; futuras micros: ventanas, sin compras, total ponderado y ranking | AN07 D12; AN03 histórico; K1/V2/V4/N1/N5/AN14/AN18 futuros | S01/S05 originales y checkpoint BI separado; no cubrir frecuencia solo con ticket | IM parcial; resto P/NA |
| ETL/DW: ETL frente ELT/extracción/transformación/carga/calidad/Bronze-Silver-Gold/rechazos/trazabilidad/reconciliar/persistencia/idempotencia/pruebas; OLTP/OLAP/DW/mart/estrella/hechos/dimensiones/grano/claves naturales/sustitutas/historia/consumo BI | Archivos, tipos, claves, funciones y pruebas | 5.1 P D22 → 5.2/5.3 D23/24 → 5.4/5.5; 13.2 P D30 sí cubre hechos/dimensiones/grano; completar 13.1 para OLTP/OLAP/DW/mart/natural vs sustituta | Micros existentes + ME/ETL; DW01 propuesto para cambio de ruta/vigencia | ME01–04/ETL-1–6/C06-0–4 preservados; DW01 no creado | S04–S06 y final privada intactos; cuadres fila por fila, adversos y repetición | P/NA |

## Distribución global D01–D42

La fecha académica original se conserva. Fuera de muestra, la tabla es propuesta y no una guía ya corregida. Restaurar una clasificación en JSON no significa que su preparación futura esté implementada.

| Día | Fecha | Enseñanza → micro → aplicación / evaluación | Estado |
|---|---|---|---|
| D01 | 2026-10-12 | Entorno/filas/variables y logros originales | H; inmutable |
| D02 | 2026-10-13 | NULL/tipos/funciones y logros originales | H; inmutable |
| D03 | 2026-10-14 | DISTINCT/listas/diccionarios; S3/S5 completos sin deuda | H; inmutable |
| D04 | 2026-10-15 | Fundamentos SQL/Python → micros existentes; cinco [x] vigentes | IM pendiente estudiante |
| D05 | 2026-10-16 | 2.2→G1/G5/G6/G7;2.3→AN03;7.12/7.13→P07;11.1–11.3 manuales | IM pendiente estudiante |
| D06 | 2026-10-17 | S01/H01 originales;2.3 ya anticipada D05; guía física no tocada | Original; ajuste editorial global pendiente |
| D07 | 2026-10-18 | Descanso | Conservado |
| D08 | 2026-10-19 | 7.5/7.7/8.1→micros→P08;11.4→micro | IM pendiente estudiante |
| D09 | 2026-10-20 | 2.4→G8;3.2→J1/J2/J3;8.5/19.1→DB01;AN04 | IM pendiente estudiante |
| D10 | 2026-10-21 | 8.3/8.4→micros→P09/P13/J4;AN05 | IM pendiente estudiante |
| D11 | 2026-10-22 | 3.3/3.4→micros→J5;ST01 preparado;AN06 | IM pendiente estudiante |
| D12 | 2026-10-23 | 6.1/9.2→micros→P10/P11;AN07;N01/ST02 conservados pendientes futuros | IM pendiente estudiante |
| D13 | 2026-10-24 | S02/H02 originales;11.3 trasladada D05; deduplicación editorial | Sin nueva obligación |
| D14 | 2026-10-25 | Descanso | Conservado |
| D15 | 2026-10-26 | 9.3→micro→P17;11.5 manual→micro antesST02 | P/NA |
| D16 | 2026-10-27 | 9.4/9.5/9.6/10.1→PD-BASE/P19/P22;ST02 traspercentiles | P/NA |
| D17 | 2026-10-28 | 10.2/10.3→PD-AGR/P20/P21;2.5→micro;N01/N02 completos guiados | P/NA |
| D18 | 2026-10-29 | 4.1→4.2→4.3/4.4→micros/K3/V3;11.6histograma/z;K2a/b despuésCTE | P/NA |
| D19 | 2026-10-30 | 6.3/6.5→micros/V2/V4;11.7correlación;P23/N03perfil;ST03 | P/NA |
| D20 | 2026-10-31 | S03/H03 originales | Sin nueva obligación |
| D21 | 2026-11-01 | Descanso | Conservado |
| D22 | 2026-11-02 | 5.1→micro/ME01;11.8muestreo→micro/ST04;CK-DA solo propuesto | P/NA |
| D23 | 2026-11-03 | 5.2/19.2→ME02;12.1variabilidad/error estándar→micro | P/NA |
| D24 | 2026-11-04 | 5.3/19.4→ME03;15.1Excel→ME04;12.2IC→micro | P/NA |
| D25 | 2026-11-05 | ETL-1/6.2→micro/H05;12.3hipótesis/errores→micro;11.4 yaD08 | P/NA |
| D26 | 2026-11-06 | ETL-2;12.4p→micro antesWelch | P/NA |
| D27 | 2026-11-07 | S04 original;11.5 se propone anticipadaD15 | Sin nueva obligación; traslado editorial pendiente |
| D28 | 2026-11-08 | Descanso | Conservado |
| D29 | 2026-11-09 | ETL-4;15.2/15.3→micros;12.5Welch→micro | P/NA |
| D30 | 2026-11-10 | ETL-5/6/H06;13.2/13.3→micros;efecto/interpretación12.7/12.8 sinchi obligatorio | P/NA |
| D31 | 2026-11-11 | 6.4→micro;E4/EX01–03 Excelreal;EX04 solo propuesto | P/NA |
| D32 | 2026-11-12 | 14.1/14.2→micros;PQ01 real solo propuesto;PB01/PB02 completos | P/NA |
| D33 | 2026-11-13 | 14.3/14.4→micros/PB03/H07;ST05 obligatorio preparado | P/NA |
| D34 | 2026-11-14 | S05 original con partes/puntos intactos | Sin nueva obligación |
| D35 | 2026-11-15 | Descanso | Conservado |
| D36 | 2026-11-16 | 17.1/C06-0;PB04 despuéscalendario/contexto/presupuesto | P/NA |
| D37 | 2026-11-17 | C06-1;6.6/14.5→micro/PB05;DW01 solo propuesto | P/NA |
| D38 | 2026-11-18 | 17.2/C06-2;PB06 refresh/reconciliación real | P/NA |
| D39 | 2026-11-19 | C06-3/AN18;ST07 condicionado;CK-STI separado propuesto | P/NA |
| D40 | 2026-11-20 | 16.2/C06-4/H08;CK-BI separado propuesto | P/NA |
| D41 | 2026-11-21 | S06 original;final privada separada | Sin nueva obligación |
| D42 | 2026-11-22 | Descanso/cierre | Conservado |

## Traslados, equivalencias y límites

ST01 D04→D11: preparación manual 11.1–11.3 D05 y 11.4 D08; no existe intento completado atribuible a D04. G1/G5/G7 D05, G8 D09 tras strftime; J1/J3 D09 y J4 D10 conservan contratos. S3/S5 permanecen acreditados históricamente D03 sin tarea nueva.

Nueve obligaciones futuras conservadas inequívocamente en listas OBLIGATORIO de fuente: ST02/P19 D16; P20/N01/N02 D17; K3 D18; V2/N03 D19; ME04 D24. Se retiran de categorías voluntarias. Sus guías destino NO se regeneran; su preparación es propuesta no implementada. N01 se conserva íntegro después de groupby, N03 después de perfil/fechas. Los notebooks son obligaciones guiadas y no cuentan como autonomía.

Primera enseñanza: 2.3 D06→D05;11.3 D13→D05;11.4 D25→D08. D06/D25 físicos no se regeneran. El desajuste transitorio está declarado. D13 solo retira la lectura trasladada y deduplica, conservando examen y hito.

13.2 ya incorpora hechos/dimensiones/grano antes de PB01/PB02; 14.1 ya incluye cuatro minutos reales para marcar calendario. No se duplican lecciones para corregir ausencias inexistentes. Error estándar, errores I/II y funciones condicionales Excel existen en teoría: falta obligatoriedad/práctica, no definición. Anexión Power Query solo está definida/equiparada: falta ejecutar. OLTP/OLAP/DW/mart y distinción natural/sustituta requieren complemento introductorio antes de DW01.

ST06/chi-cuadrado/V de Cramér permanecen voluntarios y no bloquean ST05/ST07. Los apartados de efecto de medias no exigirán previamente la ampliación chi-cuadrado.

Empleo/LinkedIn/entrevista/UAGRM/cierre conservan texto/minutos originales. UAGRM y final privada se contabilizan aparte. No se modifica trabajo personal, datos, correctores ni respuestas privadas.

Aceptación: requisitos anteriores en la ruta; cero IDs accionables repetidos; cinco [x] D04 únicas y vigentes; cero obligación perdida/degradada; modalidad corta deja OBLIGATORIO PENDIENTE; ninguna propuesta ni ejecución manual pendiente se presenta como aprobada.
