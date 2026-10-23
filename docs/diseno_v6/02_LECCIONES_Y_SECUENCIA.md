# 02 · Lecciones, secuencia y prerrequisitos

## Contabilidad de las 100 lecciones

| Clase | Cantidad | Detalle |
|---|---:|---|
| NÚCLEO (programadas en BASE) | 87 | las 47 originales + 40 promovidas; **14.5 solo en su sección inicial** (resto complementario) |
| COMPLEMENTARIAS | 10 | 1.7, 4.4, 8.2, 9.1, 11.6, 11.7, 11.9, 12.6, 12.7, 17.3 |
| Integradas en el tiempo de empleo (sin casilla propia) | 3 | 16.3 (D09), 18.2 (D24), 18.3 (D31) |
| **Total** | **100** | |
| Puente (capítulo 19, fuera de las 100) | 4 | 19.1 (D09), 19.2 (D23), 19.3 (D22), 19.4 (D24); en el diseño anterior 19.3 quedó sin programar por estar en un día de examen: corregido |

Corrección de cifras: en la propuesta 1B se habló de «88 NÚCLEO». Esa cifra mezclaba 84 lecciones con 3 secciones del puente y omitía 19.3. La cuenta exacta es la de esta tabla.

## Cuestiones de secuencia resueltas con el contenido real

### 1. 7.4 aparece antes que 7.3
- Qué se leyó: la sección inicial de 7.4 («Base inicial de funciones», 8 min) y el enunciado de P01.
- Resultado: la sección es autocontenida: ejecuta un `.py`, define variable, entero, decimal y texto, usa `+ - * /` y paréntesis, y presenta `def` y `return` con un ejemplo propio. P01 solo pide `cantidad × precio` dentro de una función.
- Decisión: se mantiene la sección inicial en D01 (con 7.1 y 7.2 antes). 7.3 y el resto de 7.4 se estudian en D02, antes de P02/P03. Se registra como excepción documentada (`excepciones_prerrequisito`), no como incumplimiento. La regla para el generador: una *sección inicial* puede preceder al prerrequisito declarado de su lección solo si es autocontenida y lo declara.

### 2. 8.7 depende de 8.6 y 8.6 estaba como complementaria
- Qué se leyó: 8.6 (pila de llamadas, causa raíz, reproducir) y 8.7 (assert, depuración, regresión), más 19.1.
- Resultado: 19.1 enseña a leer un traceback en 15 min, pero 8.6 añade pila de llamadas, causa raíz y reproducción mínima, que 8.7 usa en su método de depuración. No son equivalentes.
- Decisión: **8.6 pasa a NÚCLEO** (D12, 20 min de lectura + 15 de micropráctica) inmediatamente antes de 8.7 (D12). PT01 (D19) es su práctica autónoma de pruebas. El prerrequisito queda cumplido sin excepción.

### 3. ¿9.1 (NumPy) es indispensable antes de 9.2?
- Qué se leyó: prerrequisito de 9.2 (solo 8.3), uso de NumPy en 10.1, 11.4, 11.5, P23, ST02.
- Resultado: **no**. 9.2 no exige NumPy. 10.1 declara «NumPy no es un requisito» y define `np.where`/`np.select` en el propio ejemplo. 11.4 y 11.5 usan `np.std` y `np.percentile` solo para verificar (11.4 explica la diferencia de divisor). Los ejercicios que mencionan NumPy lo hacen sobre resultados de Pandas.
- Decisión: 9.1 permanece complementaria. Verificación pendiente en la Fase 3: que 10.1 siga siendo autocontenida en `import numpy as np` y que ningún enunciado BASE exija arreglos NumPy.

### 4. ¿14.5 (diseño de tablero) queda cubierta por lecciones y ejercicios BASE?
- Qué se leyó: 14.3, 14.4 y 14.5 completas en estructura, términos y micropráctica; enunciados PB03, PB05.
- Resultado: **no estaba cubierta**. 14.3 y 14.4 enseñan medidas, contexto y control; ninguna enseña estructura de página, títulos descriptivos con unidad y período, jerarquía visual, interacción entre visuales ni cómo comunicar el tablero. Esos contenidos están solo en 14.5.
- Decisión: se programa la **sección inicial de 14.5** (12 min de lectura + 5 de micropráctica: estructura sugerida, reglas de diseño, cómo comunicar) en D33, antes de PB07 (panel mínimo de una página, 45 min, nuevo). El resto de 14.5 (tablero defendible, lista de comprobación completa, diagnóstico) y PB05 (dos páginas) quedan como recursos complementarios. 14.4 pasa a NÚCLEO porque PB07 usa sus medidas de cobertura.

### 5. Prerrequisitos blandos que permanecen documentados
- 6.3 declara 4.4: en BASE solo se usan ticket medio y drop size (K1); «clientes activos» no tiene práctica obligatoria (4.4 complementaria). Los ejercicios N7, N13 y V2 pasan a complementarios por exigir 4.4.
- 14.5 (sección inicial) declara 6.6: la sección no usa hallazgos de 6.6, que llega en D38.

## Lecciones NÚCLEO por jornada (lectura + micropráctica obligatoria, en minutos)

| Día | Lecciones |
|---|---|
| D01 | 7.1 15 · 1.1 20 · 7.2 15 · 1.2 (sec.) 8 · 7.4 (sec.) 8 |
| D02 | 1.3 26 · 1.4 15 · 7.6 20 · 1.2 (resto) 15 · 1.6 (sec.) 7 · 7.3 20 · 7.4 (resto) 20 · 7.5 (sec.) 12 · 7.5 (resto) 22 · 7.10 (sec.) 7 |
| D03 | 1.6 (resto) 15 · 1.5 15 · 7.8 20+25 · 7.9 20+25 |
| D04 | 2.1 20+10 · 7.10 (resto) 20+20 · 7.11 20+35 · 7.12 28+25 · micro 7.1,7.2,7.3 35 |
| D05 | 2.2 20+10 · 2.3 25+30 · 7.13 25+30 · 16.1 20+20 |
| D08 | 7.7 30+25 · 8.1 20+25 |
| D09 | 3.1 20+15 · 3.2 25+25 · 8.5 25+25 · 19.1 15 · 11.1 25+15 |
| D10 | 8.3 25+20 · 8.4 30+20 · micro 7.4,7.5,7.6 40 |
| D11 | 3.3 20+10 · 3.4 25+30 · 2.4 20+20 · 11.2 20+15 · 11.3 25+20 |
| D12 | 6.1 41+15 · 8.6 20+15 · 8.7 20+25 |
| D15 | 9.2 25+25 · 9.3 20+25 |
| D16 | 10.1 25+25 · 9.5 22+20 · 6.3 25+25 |
| D17 | 10.2 20+30 · 10.3 25+30 · 9.4 20+20 · 2.5 20+20 |
| D18 | 4.1 20+20 · 4.2 15+15 · 4.3 25+25 · 11.4 30+25 |
| D19 | 6.5 25+25 · 10.5 25+30 |
| D22 | 5.1 30+15 · 19.3 25 |
| D23 | 5.5 25+10 · 5.2 25+20 · 19.2 15 · 9.6 25+25 |
| D24 | 5.3 25+20 · 19.4 15 · 10.4 20+20 · 5.4 25+15 |
| D25 | 6.2 25+25 · 11.5 30+25 · 6.4 20+25 |
| D26 | 13.1 25+20 · 10.6 25+25 |
| D29 | 13.2 30+25 |
| D30 | 14.1 34+15 · 15.1 25+15 |
| D31 | 15.3 30+10 · 15.2 25+25 · 14.2 25+20 |
| D32 | 13.3 20+15 · 11.8 25+30 |
| D33 | 14.3 35+25 · 14.4 30+25 · 14.5 (sec.) 12+5 |
| D36 | 17.1 30 · 12.1 25+30 |
| D37 | 12.2 30+25 · 12.3 30+20 |
| D38 | 17.2 25 · 6.6 25+20 · 12.4 30+35 |
| D39 | 12.8 30+15 · 12.5 30+20 |
| D40 | 16.2 25+10 · 18.1 25+20 |

## Matriz: cada concepto se enseña antes de usarse

Calculada desde `plan_v6.json`. «Enseñanza» es el primer día con lectura completa; «Primer uso» es el primer ejercicio BASE que lo exige. ⚠ = el uso es anterior a la lección completa (solo permitido si la lección figura en `excepciones_prerrequisito` o si el ejercicio solo exige la sección inicial).

| Concepto | Lecciones (día) | Primer uso BASE (día) | Estado |
|---|---|---|---|
| SELECT, ORDER/LIMIT, WHERE, NULL, DISTINCT/LIKE | 1.1 D01 · 1.2 D02 · 1.3 D02 · 1.4 D02 · 1.5 D03 · 1.6 D03 | S1 D01 · S2 D02 · S7 D02 · S4 D03 · S6 D03 | ✔ |
| Agregados, GROUP BY/HAVING, denominadores | 2.1 D04 · 2.2 D05 · 2.3 D05 | G3 D04 · G1 D04 · G5 D05 · G6 D05 | ✔ |
| Fechas SQL y CASE/COALESCE | 2.4 D11 · 2.5 D17 | SQ04 D15 · V4 D19 · SQ09 D26 | ✔ |
| Claves, INNER/LEFT JOIN, JOIN que duplica | 3.1 D09 · 3.2 D09 · 3.3 D11 · 3.4 D11 | J1 D09 · J2 D09 · J5 D11 · SQ07 D24 · SQ08 D25 | ✔ |
| Subconsulta, CTE, ventanas | 4.1 D18 · 4.2 D18 · 4.3 D18 | V3 D18 · V4 D19 · SQ10 D30 · SQ11 D30 · SQ12 D32 | ✔ |
| Variables, tipos, función | 7.1 D01 · 7.2 D01 · 7.3 D02 · 7.4 D02 | P01 D01 | ⚠ documentado (7.4 sec. en D01) |
| Texto, booleanos, if | 7.5 D02 · 7.6 D02 · 7.10 D04 | P02 D02 · P03 D02 | ⚠ documentado: P02 usa la sección inicial de 7.10 (D02, autocontenida); el resto llega en D04 |
| Listas y diccionarios | 7.8 D03 · 7.9 D03 | P04 D03 · P05 D03 | ✔ |
| Bucles, acumuladores, registros | 7.11 D04 · 7.12 D04 · 7.13 D05 | P06 D04 · P07 D05 | ✔ |
| Conversiones, contratos, excepciones | 7.7 D08 · 8.1 D08 · 8.5 D09 | P08 D08 · P09 D10 · P11 D12 | ✔ |
| Archivos CSV y módulos | 8.3 D10 · 8.4 D10 | P13 D10 · P10 D12 | ✔ |
| Traceback, pruebas y depuración | 19.1 D09 · 8.6 D12 · 8.7 D12 | DB01 D09 · PT01 D19 | ✔ |
| DataFrame y perfilado | 9.2 D15 · 9.3 D15 | P17 D15 · P23 D19 | ✔ |
| Nulos, duplicados, filtros | 9.5 D16 · 9.4 D17 | P22 D16 · PD01 D18 | ✔ |
| groupby y merge | 10.1 D16 · 10.2 D17 · 10.3 D17 | PD-BASE D16 · PD-AGR D17 · P21 D17 | ✔ |
| Fechas, carga y controles en Pandas | 9.6 D23 · 10.4 D24 · 10.5 D19 · 10.6 D26 | ME02 D23 · ME03 D24 · PE01 D37 | ✔ |
| Estadística descriptiva | 11.1 D09 · 11.2 D11 · 11.3 D11 · 11.4 D18 · 11.5 D25 | AN08 D19 · ST01 D25 · ST02 D26 | ✔ |
| Muestreo e inferencia | 11.8 D32 · 12.1 D36 · 12.2 D37 · 12.3 D37 · 12.4 D38 · 12.8 D39 · 12.5 D39 | AN17 D38 · ST05 D39 · ST07 D40 | ✔ |
| KPIs | 6.1 D12 · 6.3 D16 · 6.5 D19 · 6.2 D25 · 6.4 D25 · 6.6 D38 | K1 D16 · V4 D19 · KP01 D29 · AN18 D39 | ✔ |
| ETL | 5.1 D22 · 5.5 D23 · 5.2 D23 · 5.3 D24 · 5.4 D24 · 19.3 D22 | ME01 D22 · ME02 D23 · ME03 D24 · ETL-1 D25 | ✔ |
| Data Warehousing | 13.1 D26 · 13.2 D29 · 13.3 D32 | MD01 D30 · ETL-5 D30 · PB02 D32 | ✔ |
| Excel | 15.1 D30 · 15.3 D31 · 15.2 D31 | EX01 D31 · EX04 D31 | ✔ |
| Power Query, Power BI, DAX | 14.1 D30 · 14.2 D31 · 14.3 D33 · 14.4 D33 | PQ01 D32 · PB01 D32 · PB03 D33 · PB07 D33 | ✔ |
| Git y documentación | 16.1 D05 · 16.2 D40 · 18.1 D40 | GIT01 D10 · C06-4 D40 | ✔ |
