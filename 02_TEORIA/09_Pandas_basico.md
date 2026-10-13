# Pandas: tablas después de entender listas y funciones

Una Series es una columna con índice; un DataFrame es una tabla de columnas. Pandas aplica operaciones a columnas completas. No necesitas recorrer cada fila para sumar ventas o normalizar textos. Primero entiende la operación en una lista de tres filas; luego usa la versión vectorizada.

```python
import pandas as pd
pedidos = pd.read_csv('04_DATASETS/distribuidora/pedidos.csv')
entregados = pedidos.loc[pedidos['estado'].eq('entregado')].copy()
resumen = entregados.groupby('vendedor_id').size()
assert len(entregados) == 3442
```

`head()` muestra una muestra, `shape` da filas/columnas, `dtypes` tipos y `isna().sum()` faltantes. No concluyas que todo está limpio porque cinco filas se ven bien. Describe cada columna y prueba valores permitidos con `value_counts(dropna=False)`. Un código cliente debe tratarse como texto si sus ceros iniciales importan.

`loc` selecciona por etiquetas y máscaras; `iloc` por posición. Para combinar condiciones usa paréntesis y `&`/`|`, no `and`/`or`: `(df['cantidad']>0) & df['estado'].eq('entregado')`. Selecciona columnas con una lista. `.copy()` hace explícito que trabajarás con una tabla independiente antes de modificarla.

`groupby` define la granularidad del resumen igual que GROUP BY. `.agg(ventas=('monto','sum'),pedidos=('pedido_id','nunique'))` conserva numeradores y denominadores. `size()` cuenta filas; `count()` excluye nulos por columna. `nunique()` cuenta distintos y normalmente excluye nulos. Define si ese comportamiento responde tu pregunta.

Una columna calculada `monto = cantidad*precio_unitario` requiere tipos numéricos. Si el precio es texto, perfila y convierte. `pd.to_numeric(errors='coerce')` coloca NaN para inválidos, pero todavía debes contar y separar esas filas. `.fillna(0)` no sustituye una política de calidad.

## NumPy suficiente para este curso

Un array permite cálculo numérico vectorizado: `np.array([10,20,30]).mean()` produce 20. Distingue desviación poblacional (`ddof=0`) de muestral (`ddof=1`). El índice de Pandas puede alinear Series al operar: si sus etiquetas difieren aparecen nulos inesperados. Multiplica columnas de la misma tabla o alinea claves explícitamente.

## Puente con SQL

Reproduce G1 y G5 usando CSV. Compara fila por fila, no solo el tamaño. Ordena ambos resultados por su clave para el cuadre. En Python revisa `reset_index()` para convertir claves agrupadas en columnas. Un dataframe de tres rutas no demuestra que sus cifras sean correctas.

Práctica P17–P20 y notebook N01. El ejemplo está resuelto; la sección autónoma contiene únicamente el enunciado. Fuente: Pandas introductory tutorials, selección y agregación; NumPy absolute beginners.
