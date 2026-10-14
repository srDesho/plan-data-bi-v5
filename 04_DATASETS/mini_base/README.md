# Mini-base de las lecciones

Datos **inventados** para los ejemplos de `02_TEORIA/`. Son pocos y están pensados para poder calcular a mano. **No** son los datos de `comercial.db` ni de los ejercicios: así un ejemplo de la teoría nunca coincide con la respuesta de un ejercicio.

| Tabla | Filas | Qué representa una fila |
|---|---|---|
| `tiendas` | 12 | un punto de venta (cliente de la distribuidora) |
| `articulos` | 10 | un producto del catálogo |
| `vendedores_ej` | 4 | un vendedor y su ruta (en los CSV se llama `vendedores.csv`) |
| `ventas` | 16 | una venta (cabecera): quién, cuándo, estado |
| `venta_lineas` | 39 | un artículo dentro de una venta (detalle) |
| `metas` | 6 | la meta en Bs de una ruta en un mes |
| `visitas_ej` | 14 | una visita planificada a una tienda (en los CSV se llama `visitas.csv`) |

Archivos: `mini_base.sql` (crea y llena las tablas), `mini_base.db` (SQLite ya construida) y un CSV por tabla.

Se regeneran siempre idénticos con `python herramientas/crear_mini_base.py`. Para consultarla:

```
python herramientas/ejecutar_sql.py --db 04_DATASETS/mini_base/mini_base.db --consulta "SELECT * FROM tiendas LIMIT 3;"
```

Las lecciones no modifican este archivo: `herramientas/verificar_teoria.py` ejecuta cada ejemplo sobre una copia.

Detalles intencionales para practicar limpieza: la tienda 5 tiene espacios sobrantes en el nombre y zona vacía (NULL), la tienda 8 también tiene zona NULL, y las ventas 4 y 13 están `anulado`.
