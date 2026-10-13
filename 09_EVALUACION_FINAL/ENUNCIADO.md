# Evaluación final de autonomía · 23–30 de noviembre de 2026

Abre los datos el 23 de noviembre. La exportación sintética contiene 12.170 filas, un catálogo y una
clave de línea estable. El objetivo es construir un ETL junior reproducible y defender tus decisiones.

## Regla de autonomía

Sin código generado por IA ni referencias resueltas del paquete. Puedes consultar documentación oficial
y definiciones conceptuales; registra URL, pregunta y decisión en consultas_documentacion.md.
Si recibes ayuda, regístrala: esa parte no acredita autonomía hasta un segundo intento independiente.
El corrector verifica resultados; la defensa y un registro honesto son necesarios para evaluar autoría.

## Requerimiento de gerencia

Una distribuidora ficticia recibe transacciones_raw.csv y catalogo.csv. Necesita explicar registros válidos,
duplicados y rechazos, ventas entregadas por cliente/mes, ticket por documento y aporte por categoría.
La carga debe repetirse sin duplicar. No hay descuentos, devoluciones, presupuesto ni agenda: indica qué
KPIs no puedes calcular con estas fuentes y qué datos solicitarías.

## Trabajo propio

1. Perfil completo, diccionario, granularidad, clave y reglas de conversión/rechazo.
2. Bronze sin modificar y metadatos/conteos del origen.
3. Detección de conflictos de una misma linea_id antes de quitar duplicados exactos.
4. Fechas ISO o DD/MM/YYYY, cantidad entera positiva, precio en centavos y estado normalizado.
5. Catálogo único, SKU huérfano rechazado y registro original con sus motivos.
6. Silver enriquecida con descripción/categoría; conservar anulados y excluirlos de ventas Gold.
7. Gold: una fila por cliente_id/mes con ventas_centavos y documentos distintos.
8. SQLite con tablas bronze, silver, rechazos y gold; publicación después de validar.
9. Auditoría JSON: bronze, duplicados_exactos, rechazados, silver y ventas_centavos.
10. Rechazos CSV, Gold CSV, SQL independiente, logging y README de reproducción.

Silver incluye linea_id, documento, fecha, cliente_id, ruta, sku, cantidad, estado, precio_centavos y
monto_centavos. Gold incluye cliente_id, mes, ventas_centavos y documentos. Rechazos incluye linea_id
y motivos. Consulta el diccionario junto a los datos para formatos y unidades.

## Calendario: 12,5 horas netas

| Fecha | Minutos | Entrega comprobable |
|---|---:|---|
|23 lunes|90|Contrato y perfilado; clase UAGRM aparte|
|24 martes|120|Funciones, pruebas de formatos y Bronze|
|25 miércoles|120|Silver, catálogo, rechazos y cuadre de conteos|
|26 jueves|120|Gold, SQLite y validación previa a publicar|
|27 viernes|90|SQL independiente y segunda ejecución|
|28 sábado|120|Entradas adversas, README e informe con tabla/gráfico|
|29 domingo|0|Descanso|
|30 lunes|90|Defensa, corrector y rúbrica; clase UAGRM aparte|

En cada día activo reserva quince minutos de SQL dentro del bloque. REDUCIDO: 60 minutos;
MÍNIMO: 20 (SQL 15 + registro 5). Domingo: cero. Son alternativas, no sesiones añadidas.
Si no termina en el plazo, entrega el avance y registra faltantes sin declarar aprobación.
Power BI es una aplicación posterior opcional; no bloquea la evaluación de autonomía ETL.

## Entrega y corrección

`mi_trabajo/final/`: etl.py, requirements.txt, README.md, reglas.md, consultas_documentacion.md,
salida/resultado.db, rechazos.csv, gold.csv, auditoria.json, validacion.sql y hallazgos.md.
Demuestra ejecución desde una terminal limpia, explica cinco decisiones/líneas seleccionadas y un rechazo.
Incluye cinco hallazgos o límites y un dato adicional que necesitarías para otro KPI.

Después de cerrar la entrega: `python herramientas/validar_final.py mi_trabajo/final/salida`.
Aplica [la rúbrica](RUBRICA.md). Soluciones y controles permanecen en 08_SOLUCIONES.
La prueba numérica no acredita automáticamente autonomía ni comportamiento de Power BI Desktop.
