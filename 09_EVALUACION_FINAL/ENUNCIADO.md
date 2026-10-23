# Evaluación final de transferencia · 23–30 de noviembre de 2026

Abre los datos el 23 de noviembre, **solo si cumpliste la Puerta 7** (S06 y H08). Una distribuidora ferretera ficticia envía una exportación de despachos con un contrato que **no es el de C06**: otra clave, otras fechas y precios, un descuento con una regla de redondeo, un tercer estado y otro grano de Gold. El objetivo es leer un contrato nuevo, **adaptar** tu método y defender tus decisiones.

## Este bloque no está incluido en las 157 h 32 min de las 42 jornadas

Las 42 jornadas suman 157 h 32 min de trabajo BASE (seis semanas). La evaluación final es una **séptima semana de evaluación, posterior y explícita**: 570 minutos netos (9,5 h) estimados de primera vez, no medidos. Antes reservaba 750 minutos (12,5 h); se redujo en 180 minutos porque reutilizas tus funciones y estructura de C06 en vez de construirlas dos veces desde cero (detalle en [`CARGA_ESTIMADA.md`](../01_PLAN_DIARIO/CARGA_ESTIMADA.md)). No se suman horas voluntarias ni se añade otra semana. Si no puedes dedicar este bloque en esas fechas, se reprograma sin acumular horas y no se declara autonomía.

## Regla de autonomía

- **Sin código generado por IA y sin referencias resueltas.** Puedes consultar la documentación oficial (pandas, sqlite3, la biblioteca estándar) y definiciones conceptuales: registra URL, pregunta y decisión en `consultas_documentacion.md`.
- **Permitido y esperado:** reutilizar funciones que escribiste tú (de P09–P11, ME01–ME03, ETL y C06) **si puedes explicarlas línea por línea**. No es lo mismo que memorizar toda la sintaxis: nadie te pide recordarla de memoria, te piden entender lo que escribes.
- **No permitido:** pegar código que no escribiste, de una IA, de un tutorial resuelto o de otra persona. Si recibes ayuda, regístrala: esa parte no acredita autonomía hasta un segundo intento independiente con otra variante.
- Ningún corrector certifica la autoría. La respaldan tres cosas que haces delante de otra persona (ver «Defensa»): explicar, anticipar un resultado, reparar un fallo y cambiar una regla en vivo.

### Qué custodia hay y qué no

- El paquete del estudiante **no** incluye la referencia de esta evaluación, ni la tabla Silver esperada, ni los totales esperados. `herramientas/validar_final.py` compara tu salida con **huellas** (`verificacion/huellas_final.json`): te dice qué claves coinciden y cuáles no, sin mostrar los valores esperados.
- Eso **no es una prueba ciega**. Las huellas se pueden contrastar con valores que adivines, y quien tenga acceso a todo el paquete podría construirse su propia solución. La referencia, el generador de los datos y la verdad de la corrección están en una carpeta aparte, fuera del paquete (`Plan_Data_BI_v5_CUSTODIA_FINAL`), que debe guardar otra persona (tutor, docente o compañero de confianza) y no abrirse hasta el final. Si no hay otra persona, la prueba mide cumplimiento del contrato y honestidad declarada, no ceguera: regístralo en el informe y no la presentes como ciega.

## Requerimiento de gerencia

Gerencia quiere saber, por sucursal, mes y línea de producto: cuánto se vendió, en cuántos documentos y cuántas líneas se devolvieron; y quiere entender los rechazos y los duplicados. Calcula el **ticket medio por documento** (ventas ÷ documentos) por sucursal y mes e indica qué KPIs **no** puedes calcular con estas fuentes (márgenes, impuestos, descuentos como motivo de venta) y qué datos pedirías.

## Trabajo propio (todo esto se evalúa)

1. **Contrato**: lee [`datos/DICCIONARIO.md`](datos/DICCIONARIO.md) y escribe en `reglas.md` tu propia versión: granularidad, clave compuesta, formatos, reglas de rechazo, regla de redondeo, qué significa cada estado y los cuadres. Perfila `despachos_raw.csv` y `articulos.csv`.
2. **Bronze** sin modificar y conteos del origen.
3. **Conflictos de clave** `(nro_doc, item)` detectados **antes** de quitar duplicados exactos; los conflictos detienen el proceso.
4. **Conversiones** propias y probadas con casos que escribes antes: tres formatos de fecha, cantidad entera positiva, precio con `Bs` y separador de miles, descuento (vacío = 0) y monto en centavos con la regla de redondeo.
5. **Catálogo** único, artículo huérfano rechazado, sucursal y estado normalizados, rechazo con todos sus motivos.
6. **Silver** enriquecida con la línea de producto; se conservan anuladas y devueltas y se excluyen de las ventas.
7. **Gold** por `(sucursal, mes, linea)`: `ventas_centavos`, `documentos` distintos y `lineas_devueltas`.
8. **SQLite** con `bronze`, `silver`, `rechazos` y `gold`, publicada solo después de validar, con segunda ejecución sin duplicar y la salida anterior preservada si falla el contrato estructural.
9. **Auditoría** JSON y salidas CSV coherentes con las tablas.
10. **Validación SQL independiente** (`validacion.sql`), entradas adversas en copias (columna ausente, catálogo con clave repetida, misma clave con contenido distinto, cantidad fraccionaria), registro (`logging`) y README de reproducción desde una terminal limpia.
11. **Informe** corto con una tabla o un gráfico, cinco hallazgos o límites y un dato adicional que pedirías.

### Tres cosas que debes escribir tú durante el intento (no se pueden «reutilizar»)

- **Una transformación breve nueva**: la conversión del precio con miles (`Bs 1.250,50`) o la fecha compacta `AAAAMMDD`; no existen en tus proyectos anteriores.
- **Una adaptación a una regla nueva**: el descuento con redondeo al centavo y el estado `devuelto` en Gold.
- **Un error que reparas**: durante la defensa se te pide localizar y corregir un fallo descrito por su síntoma en tu propio ETL (por ejemplo, un Gold que no cuadra por unos pocos documentos).

## Calendario: 9,5 horas netas, posterior a las 42 jornadas

| Fecha | Antes | Ahora | Entrega comprobable |
|---|---:|---:|---|
| 23 lunes | 90 | 90 | Contrato propio y perfil de los datos nuevos; clase UAGRM aparte |
| 24 martes | 120 | 90 | Funciones adaptadas, pruebas de formatos y Bronze |
| 25 miércoles | 120 | 90 | Silver con clave compuesta, catálogo, rechazos y cuadre de conteos |
| 26 jueves | 120 | 90 | Gold, SQLite y validación previa a publicar |
| 27 viernes | 90 | 60 | SQL independiente, segunda ejecución y cuatro entradas adversas |
| 28 sábado | 120 | 60 | README, informe con tabla o gráfico y ensayo de la defensa |
| 29 domingo | 0 | 0 | Descanso |
| 30 lunes | 90 | 90 | Defensa con observador, corrector y rúbrica; clase UAGRM aparte |
| **Total** | **750** | **570** | |

El SQL de esta evaluación es la validación independiente del viernes; si quieres, repasa una consulta conocida durante diez minutos dentro de un bloque (opcional, no suma tiempo). Modo REDUCIDO: 60 minutos con una entrega menor (la que corresponda al día); MÍNIMO: 20 minutos que mantienen la continuidad y no acreditan contenidos. Son alternativas, no sesiones añadidas. Si no terminas en el plazo, entrega el avance y registra los faltantes sin declarar aprobación. Power BI es una aplicación posterior y opcional; no bloquea la evaluación de autonomía ETL.

## Entrega y corrección

`mi_trabajo/final/`: `etl.py`, `requirements.txt`, `README.md`, `reglas.md`, `consultas_documentacion.md`, `validacion.sql`, `hallazgos.md`, `informe.md` y `salida/` con `resultado.db`, `rechazos.csv`, `gold.csv` y `auditoria.json`. Copia tu registro desde [`PLANTILLA_REGISTRO.md`](PLANTILLA_REGISTRO.md).

1. Ejecuta **una vez**, al cerrar tu entrega: `python herramientas/validar_final.py mi_trabajo/final/salida`. El corrector acumula todos los fallos y revisa fila por fila (Bronze, Silver, rechazos, Gold, CSV y auditoría). No lo uses para depurar.
2. Aplica la [rúbrica](RUBRICA.md) y haz la defensa (abajo).
3. La prueba numérica **no** acredita autonomía por sí sola ni el comportamiento de Power BI Desktop o de Excel.

## Defensa con observador (30 de noviembre, 60 de los 90 minutos)

Delante de otra persona (tutor, docente, compañero) o, si no la hay, grabada y revisada después por alguien que no escribió tu código. En este orden:

1. **Explicar (15 min).** Cinco decisiones o líneas que elige la persona observadora entre tu código, incluida la regla de redondeo y un rechazo concreto; tú explicas sin leerlas.
2. **Anticipar (10 min).** Antes de ejecutar, escribes qué esperas de un cambio que te dicta la persona observadora (por ejemplo, un descuento máximo del 40 %): cuántos rechazos nuevos, qué cambia en Silver y si cambian las ventas.
3. **Reparar (15 min).** La persona observadora introduce en una copia de tu ETL un defecto descrito solo por su síntoma; localizas la causa por reducción del problema y la corriges.
4. **Modificar en vivo (10 min).** Haces el cambio de la regla anunciada en el paso 2 y verificas que la ecuación de conteos sigue cerrando.

## Criterio de autonomía

Se declara autonomía en esta etapa solo si se cumplen **todas**: S06 ≥ 80 sin puertas críticas · H08 cumplido · este corrector sin fallos · rúbrica ≥ 80/100 sin puertas críticas · la defensa superada en los cuatro pasos · ninguna ayuda sin declarar. Si algo falla: se registra qué base concreta y se hace una variante nueva, no se repite la semana por defecto. Preparar bien esta evaluación acredita que el material está listo; solo resolverla y defenderla acredita que tú ya eres autónomo.
