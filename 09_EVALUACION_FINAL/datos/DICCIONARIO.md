# Datos sintéticos y contrato: evaluación final (despachos de una ferretería mayorista)

Empresa ficticia (no proviene de Cruzimex). Es un caso **nuevo**: la clave, los formatos, las unidades y una regla de negocio no son los de C06 ni los de la distribuidora. Lee todo el contrato antes de programar; es parte de lo que se evalúa.

## Archivos

| Archivo | Separador | Contenido |
|---|---|---|
| `despachos_raw.csv` | `\|` (barra vertical) | una fila por línea de un documento de despacho; UTF-8 |
| `articulos.csv` | `,` | catálogo: `cod_art`, `descripcion`, `linea` (familia de producto); UTF-8 |

## Columnas de `despachos_raw.csv`

| Columna | Qué contiene | Regla del contrato |
|---|---|---|
| `nro_doc` | número de documento (`D-000123`) | no vacío; un documento tiene varias líneas |
| `item` | número de línea dentro del documento | entero positivo. **La clave de una línea es `(nro_doc, item)`**, no una sola columna |
| `fecha_despacho` | fecha | tres formatos: `AAAA-MM-DD`, `DD/MM/AAAA` o `AAAAMMDD` (sin separadores). Fecha imposible: rechazar |
| `sucursal` | código de sucursal | `SCZ`, `LPZ` o `CBB`, sin importar mayúsculas ni espacios. Otro código: rechazar |
| `cod_cliente` | código de cliente | no vacío (después de quitar espacios) |
| `cod_art` | código de artículo | debe existir en `articulos.csv` (sin importar mayúsculas ni espacios). Si no existe: rechazar |
| `cantidad` | unidades | entero positivo; `7.0` es válido, `3.5`, `0`, `-2`, `2,5` y texto no |
| `precio_unitario` | precio en Bs | prefijo `Bs` opcional; **coma decimal con dos decimales**; el punto separa miles (`Bs 1.250,50`). No negativo. Otro formato: rechazar |
| `descuento_pct` | descuento de la línea | entero de 0 a 100. **Vacío significa 0** (sin descuento). Otro valor: rechazar |
| `estado` | estado de la línea | `entregado`, `anulado` o `devuelto`, sin importar mayúsculas ni espacios. Otro valor: rechazar |

## Dinero: reglas de este caso

- El dinero se guarda en **centavos enteros** (`precio_centavos`, `monto_centavos`). No uses `float` para el resultado.
- `monto_centavos = (cantidad × precio_centavos × (100 − descuento_pct) + 50) // 100` (división entera): el importe de la línea con el descuento aplicado, **redondeado al centavo más cercano, la mitad hacia arriba**. Solo enteros: no hay errores de coma flotante.
- El monto se calcula para todas las líneas válidas (también anuladas y devueltas).

## Qué significa cada estado

- `entregado`: es venta.
- `anulado`: se conserva en Silver y **no** suma a las ventas.
- `devuelto`: se conserva en Silver, **no** suma a las ventas y se cuenta aparte en Gold como línea devuelta.

## Calidad de datos

- Hay duplicados exactos (filas idénticas) y filas inválidas. **Busca primero conflictos de clave** (la misma clave `(nro_doc, item)` con contenido distinto): detienen el proceso. Elimina solo duplicados exactos. Registra cada rechazo con su causa. No inventes valores.
- Un documento tiene una sola fecha y una sola sucursal.
- El catálogo tiene 72 artículos únicos; el join es muchos a uno por `cod_art`. Un catálogo con clave vacía o repetida detiene el proceso.
- No se solicitan impuestos, comisiones ni costos: esos campos no están disponibles, así que no puedes calcular márgenes.

## Salidas exigidas

Carpeta `mi_trabajo/final/salida/` con `resultado.db` (tablas `bronze`, `silver`, `rechazos`, `gold`), `rechazos.csv`, `gold.csv` y `auditoria.json`.

- **bronze**: el archivo tal cual (texto exacto, todas las filas, incluidos los duplicados).
- **silver**: una fila por línea válida, sin repetir la clave, con las columnas `nro_doc`, `item`, `fecha` (`AAAA-MM-DD`), `sucursal` (mayúsculas), `cod_cliente`, `cod_art` (mayúsculas), `cantidad`, `precio_centavos`, `descuento_pct`, `estado` (minúsculas), `monto_centavos` y `linea` (del catálogo); puedes añadir `descripcion`.
- **rechazos**: la fila original completa y una columna `motivos` (causas separadas por `;`). Ninguna sin motivo.
- **gold**: una fila por `(sucursal, mes, linea)` con al menos una línea entregada, con `mes` en `AAAA-MM`, `ventas_centavos` (solo líneas entregadas), `documentos` (documentos **distintos** con al menos una línea entregada en ese grupo) y `lineas_devueltas` (líneas con estado `devuelto` del mismo grupo; 0 si no hay).
- **auditoria.json**: `bronze`, `duplicados_exactos`, `rechazados`, `silver` y `ventas_centavos`.
