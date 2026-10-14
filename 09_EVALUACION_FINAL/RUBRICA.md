# Rúbrica de la evaluación final: 100 puntos

Cada componente indica la competencia que mide, la preparación obligatoria previa, la evidencia observable y los puntos. Lo que no ejecutaste vale 0 y se registra como pendiente; no se estima.

| Componente | Pts | Competencia (`COMPETENCIAS.md`) y preparación | Evidencia para puntaje completo | Parcial |
|---|---:|---|---|---|
| Perfil y contrato | 10 | N1.4 · C06-0 y C06-1 (D36–D37) · lección 17.1 | `reglas.md` con granularidad y clave compuesta, formatos, regla de redondeo, significado de cada estado, cuadres y KPIs no calculables | 2 por: clave y grano · formatos · redondeo · estados · KPIs no calculables |
| Transformación | 30 | N1.4 · P09–P11, ME02, C06-2 | tipos, claves, catálogo, duplicados y rechazos trazables; la transformación nueva y la regla nueva escritas por ti | corrector: Silver fila por fila 15 · rechazos trazables 5 · conflicto antes de duplicados 5 · transformación nueva y regla nueva explicadas 5 |
| Carga | 15 | N1.4 · ME03, ETL-6, C06-4 | Bronze/Silver/Gold íntegros, SQLite publicada tras validar y segunda carga sin duplicar | Bronze idéntico 4 · Gold fila por fila 6 · segunda carga 3 · CSV y auditoría coherentes 2 |
| Validación | 20 | N1.4 / N1.7 · ETL-6, C06-4 | `validacion.sql` independiente (ventas, documentos distintos y devueltas), cuatro entradas adversas en copias con la salida anterior preservada | SQL independiente 8 · adversas 8 (2 cada una) · salida anterior preservada 4 |
| Analítica | 10 | N1.5 / N1.8 · AN14–AN18 | KPIs posibles con unidad y periodo, ticket por documento, tabla o gráfico, cinco hallazgos o límites y un dato adicional | KPI y unidad 3 · tabla o gráfico 2 · hallazgos y límites 3 · dato que pedirías 2 |
| Reproducción | 5 | N1.4 · lección 16.2 | README y comando desde una terminal limpia, `requirements.txt` y `logging` útil | README y comando 3 · logging 2 |
| Defensa propia | 10 | N1.9 · H08 | los cuatro pasos de la defensa del [enunciado](ENUNCIADO.md) | explicar 3 · anticipar 2 · reparar 3 · modificar 2 |

Objetivo: **80/100**. Entre 75 y 79 o por debajo: no se repite la semana; se identifica la base concreta en la tabla de abajo y se hace una variante nueva de esa base antes de volver a defender.

## Puertas críticas

Un promedio alto no compensa ninguna de estas. Cualquiera impide declarar autonomía aunque el total llegue a 80:

1. Dinero incorrecto (importes, redondeo o unidades).
2. Filas perdidas sin explicar, o ecuación de conteos que no cierra.
3. Claves duplicadas, conflicto de clave resuelto en silencio o catálogo ambiguo aceptado.
4. Una segunda carga que duplica, o una salida anterior destruida por un fallo estructural.
5. Incapacidad de explicar el código o de reparar el fallo de la defensa.
6. Ayuda externa, código generado por IA o copia no declarados.

## Evidencias esenciales

Perfilado, granularidad y claves · funciones comprensibles · tipos y dinero correctos · uniones controladas · duplicados y rechazos · carga SQLite repetible · conciliación SQL independiente · reproducción desde terminal · interpretación de KPIs · defensa de decisiones. La transferencia se comprueba con tres piezas que no existen en los proyectos anteriores: una transformación breve nueva, una adaptación a una regla nueva y la reparación de un error.

## Entradas adversas (en copias; registra comandos y resultados)

Columna obligatoria ausente · catálogo con clave repetida · la misma `(nro_doc, item)` con importe distinto · cantidad fraccionaria. Las tres primeras detienen el proceso y preservan la salida anterior; la última rechaza con causa.

## Si no alcanzas el objetivo: base concreta y variante

| Falló | Base a recuperar | Variante nueva que lo demuestra |
|---|---|---|
| Contrato o transformación | la función con el mensaje del corrector; lección 17.2 | cambia una sola regla del diccionario (por ejemplo, descuento máximo de 40 %) y predice los rechazos antes de ejecutar |
| Carga | ME03 y ETL-6 | repite la segunda carga con un duplicado exacto añadido y explica qué cambia en los conteos |
| Validación | C06-4 | escribe otra comprobación SQL (por sucursal y mes) y una entrada adversa nueva |
| Defensa | H08 y 17.3 | repara otro defecto que te describe un observador |

## Límites de esta evaluación

Los cuadres automáticos apoyan la evaluación; la regla sin IA requiere honestidad y una persona observadora. La prueba no certifica el uso de Power BI Desktop, Excel ni SQL Server: lo que no se ejecutó queda registrado como pendiente.
