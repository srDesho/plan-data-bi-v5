# Pandas: limpiar, unir y validar

Limpieza no significa eliminar todo lo extraño. Significa convertir representaciones conocidas en una forma acordada y registrar lo que no se puede interpretar. Bronze conserva la entrada original; Silver conserva registros válidos con tipos y claves; rechazos permiten explicar diferencias.

## Fechas y dinero

No adivines el formato de `01/02/2026`. En estos ejercicios significa 1 de febrero porque el contrato dice DD/MM/YYYY. Un parser debe admitir únicamente los formatos del diccionario. Puedes usar `pd.to_datetime(...,format='%d/%m/%Y',errors='coerce')` y separar NaT; para mezclar ISO y DD/MM/YYYY aplica una máscara de formato antes de convertir cada grupo.

Dinero puede contener `Bs`, coma decimal y espacios. Primero normaliza las representaciones admitidas, luego convierte. Para el proyecto final usa `Decimal` y almacena centavos enteros: evita errores acumulados de flotantes. Dos decimales y moneda Bs son una regla explícita. No elimines separadores de miles que el contrato nunca definió.

## JOIN de Pandas

```python
import pandas as pd
pedidos=pd.read_csv('04_DATASETS/distribuidora/pedidos.csv')
clientes=pd.read_csv('04_DATASETS/distribuidora/clientes.csv')
unido=pedidos.merge(clientes,on='cliente_id',how='left',validate='many_to_one',indicator=True)
assert len(unido)==len(pedidos)
assert unido['_merge'].eq('both').all()
```

`validate` comprueba cardinalidad; falla si el catálogo duplica claves. `indicator` muestra left_only/both/right_only. Usa primero un LEFT JOIN para identificar huérfanos. INNER JOIN los descartaría. Una columna sufijada `_x/_y` indica nombres repetidos; selecciona columnas del catálogo y renombra intencionalmente.

## Duplicados y claves

`duplicated()` sobre todas las columnas detecta duplicados exactos. `duplicated(subset=['linea_id'])` detecta claves repetidas, que pueden contener importes distintos. No conserves la primera arbitrariamente: detecta conflictos y detén o envía a revisión. La clave `[nro_pedido,producto]` del ETL original es válida solo porque ese dataset tiene una línea por producto/pedido. En una exportación nueva puede repetirse el producto legítimamente. El caso final trae `linea_id`.

## Validaciones que cambian decisiones

Verifica columnas requeridas, claves únicas, cantidades enteras positivas, catálogo completo, estados permitidos y nulos en campos obligatorios. Separa validación de estructura (detiene carga) y de fila (rechazo con motivo). Después verifica el cuadre: Bronze = duplicados eliminados + rechazados + Silver; venta Silver entregada = Gold; filas antes/después de merge iguales cuando es muchos a uno.

`assert` ayuda en ejercicios; para contratos de producción usa excepciones explícitas porque Python puede desactivar asserts con optimización. Reejecutar el pipeline no debe duplicar datos: reemplaza el conjunto completo en esta práctica y documenta esa estrategia. Carga incremental queda para después.

Práctica P21–P28, notebooks N02/N03 y proyecto ETL. Fuente: Pandas merge, missing data y to_datetime; Python Decimal.
