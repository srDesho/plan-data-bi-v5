# SQL desde cero: una pregunta, una tabla y un resultado

Una base de datos guarda tablas. Una tabla tiene filas y columnas; una fila debe representar algo concreto. En `clientes`, una fila representa un cliente y `cliente_id` lo identifica. En `pedidos`, una fila es un pedido. En `pedido_items`, una fila es un producto dentro de un pedido. Antes de escribir SQL di en voz alta qué representa una fila de tu resultado.

SQL describe el conjunto que quieres obtener. No necesitas recorrer filas con un bucle. `SELECT` elige columnas; `FROM` indica la tabla; `WHERE` conserva las filas cuya condición es verdadera. El resultado es otra tabla, incluso si tiene una sola fila. Leer datos no exige modificarlos.

```sql
SELECT cliente_id, nombre_negocio, ruta
FROM clientes
WHERE ruta = 'R03'
ORDER BY cliente_id
LIMIT 5;
```

La consulta busca clientes de R03, ordena por código y muestra cinco. Los textos van entre comillas simples. Los nombres de columnas no son textos. `=` compara, no asigna. El punto y coma termina la sentencia. `ORDER BY` permite que el orden sea intencional; sin él no existe un orden garantizado. `LIMIT` recorta filas después del ordenamiento; no sirve para contar toda la población.

Combina condiciones con `AND` cuando ambas deban cumplirse y `OR` cuando baste una. Usa paréntesis: `ruta='R01' AND (tipo='Kiosco' OR tipo='Farmacia')`. `IN` simplifica alternativas de una misma columna. `BETWEEN` incluye ambos extremos. `LIKE '%sol%'` busca un patrón de texto, pero su comportamiento con acentos y mayúsculas depende del motor y la configuración.

`NULL` indica información desconocida o ausente. No es cero ni cadena vacía. `zona = NULL` no identifica faltantes; usa `zona IS NULL`. Al comparar un nulo, el resultado puede ser desconocido y `WHERE` lo descarta. `COALESCE(zona,'Sin zona')` ofrece una etiqueta para un informe; no significa que hayas corregido el dato en origen. No reemplaces importes faltantes por cero sin una regla de negocio.

`DISTINCT` elimina combinaciones repetidas de las columnas que seleccionas. `DISTINCT ruta,tipo` devuelve pares distintos; no una lista independiente de rutas y otra de tipos. `COUNT(*)` cuenta filas, mientras que `COUNT(zona)` excluye zonas nulas. `COUNT(DISTINCT cliente_id)` cuenta clientes únicos.

## Del requerimiento al código

Requerimiento: "Necesito negocios de R03 para revisar la ruta". Define población (clientes), filtro (R03), columnas necesarias (código, nombre, zona) y orden (código). Ejecuta primero cinco filas; luego quita LIMIT y cuenta. Si aparecen 14 clientes, explica que representan clientes asignados, no visitas realizadas ni compradores activos.

Errores frecuentes: usar nombres como claves, confundir clientes con pedidos, filtrar fechas escritas como DD/MM/YYYY en texto, y limitar antes de comprobar el total. Las fechas de esta base están en ISO YYYY-MM-DD: su orden textual coincide con el cronológico. Eso no se cumple para cualquier formato.

Práctica: S1–S10. Al terminar escribe una nueva consulta para una ruta distinta y explica cada cláusula sin mirar el ejemplo. Fuente concreta: SQLite, SELECT, secciones WHERE, ORDER BY y LIMIT; enlaces en `FUENTES.md`.
