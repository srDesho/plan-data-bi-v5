# Preparación técnica desde las primeras semanas

Una entrevista evalúa razonamiento, comunicación y límites además de sintaxis. Antes de escribir consulta di población, granularidad y denominador. Si falta presupuesto, no puedes calcular cumplimiento. Si hay anulados, aclara su tratamiento. Una buena pregunta al entrevistador suele ser mejor que asumir una regla silenciosa.

## Respuesta técnica en cuatro pasos

1. Reformula el pedido: "Una fila por ruta/mes con ventas entregadas".
2. Define tablas, claves y filtros.
3. Resuelve un ejemplo de dos pedidos a mano y escribe el código.
4. Verifica con total independiente y explica limitaciones.

Pregunta: "¿Por qué mi conteo de pedidos subió después del JOIN?" Respuesta: el detalle tiene varias líneas por pedido. Comprueba la granularidad; usa DISTINCTCOUNT para documentos o agrega el detalle antes. DISTINCT sobre toda la tabla sin entender el JOIN puede ocultar el error.

Pregunta: "¿Qué diferencia hay entre medida y columna DAX?" Explica contexto de filtro frente a valor por fila y da ticket medio como medida. Pregunta: "¿Eliminarías un atípico?" Primero revisa si es error o negocio válido, luego cuantifica el efecto de la decisión.

## Pasantía y apoyo de IA

Presentación inicial: "Soy Técnico Superior en Sistemas Informáticos. Terminé una pasantía de seis meses en BI en Cruzimex, trabajando con ERP, Excel y reportes; utilicé IA como apoyo para automatizaciones. Estoy construyendo bases de SQL y Python y puedo mostrar los ejercicios que ya resolví y explicar sus controles. Busco una posición junior de datos o reportes".

Actualiza esa presentación cuando completes los proyectos. No digas "entiendo cada línea" si todavía no puedes explicarla. Si una pregunta excede tu experiencia, identifica lo que sí sabes y cómo comprobarías lo restante. No uses los resultados generados por el paquete como prueba de que tú ya adquiriste la habilidad.

## Conductuales con hechos reales

STAR: situación, tarea, acción propia y resultado. Prepara una historia de error y depuración, una de plazo y otra de colaboración con supervisor. Separa lo que realizaste de lo que generó una herramienta. Un resultado válido también puede ser detectar un dato faltante y comunicarlo a tiempo.

Práctica: banco de preguntas, seis simulacros y casos empresariales de `06_ENTREVISTAS`. Cada simulacro usa una rúbrica: exactitud, validación, explicación y honestidad. Guarda una respuesta de voz de dos minutos o texto breve y revísala con la guía después del intento.
