# 5.1 ETL, ELT y capas Bronze, Silver y Gold

> Tiempo estimado: 50 min (lectura 30 + práctica 20). Prerrequisitos: capítulos 9 y 10 (Pandas) y [10.5 Controles de calidad](../10_Pandas_transformaciones/05_controles_calidad.md).

## Para qué sirve

Un reporte confiable no se arma de golpe: se construye en etapas, y cada etapa tiene un propósito y una garantía distinta. «ETL» y «medallón» son los nombres con que la industria describe esas etapas. Entenderlos te da el **mapa** de cualquier proyecto de datos: dónde se guarda lo que llegó, dónde se limpia, dónde se calculan las cifras del negocio y dónde se explican las diferencias.

## Términos nuevos

- **ETL** (*Extract, Transform, Load*): extraer los datos de su origen, transformarlos (limpiar, convertir, unir) y cargarlos en el destino.
- **ELT**: la variante que **carga primero** los datos crudos en el destino y los transforma dentro de él (por ejemplo, con SQL). Es un orden de trabajo, no una garantía de calidad.
- **Origen (fuente)**: de dónde vienen los datos (un CSV del ERP, una API).
- **Destino**: donde se publican los resultados (una base SQLite, un archivo para Power BI).
- **Arquitectura medallón**: la forma de organizar los datos en tres capas de calidad creciente: Bronze, Silver y Gold.
- **Bronze**: la capa del dato **tal como llegó**, sin cambios, con registro de la fuente. No se sobrescribe el archivo original.
- **Silver**: la capa de datos **limpios y validados**: claves, tipos, fechas y estados normalizados. Contiene los registros válidos.
- **Gold**: la capa de **resúmenes listos para el negocio**: cifras por cliente y mes, por ruta, por categoría.
- **Rechazos**: la salida de las filas que no pasaron la validación, con su motivo. Son una salida auditada, no una papelera oculta.
- **Pipeline**: el conjunto de pasos encadenados que lleva los datos del origen al destino.
- **Trazabilidad**: poder explicar de dónde sale cada cifra y qué pasó con cada fila.

## Ejemplo paso a paso

**1. ETL frente a ELT.**

| | ETL | ELT |
|---|---|---|
| Orden | extraer → transformar fuera → cargar | extraer → cargar crudo → transformar dentro |
| Dónde se transforma | en tu programa (Python) | en el destino (SQL) |
| Ejemplo del curso | CSV → Python → SQLite | CSV cargado a SQLite y luego consultas SQL |
| Ventaja | control total de reglas en código | el destino hace el trabajo pesado |

Ninguno es «mejor»: ambos son órdenes. En este curso practicarás el ETL con Python porque el trabajo lo exige y porque te obliga a entender cada regla.

**2. Las tres capas en una imagen.**

```text
Origen (CSV del ERP)
   │ copiar tal cual
   ▼
BRONZE  filas y valores como llegaron
   │ limpiar, convertir, validar
   ├──────────────► RECHAZOS  (filas inválidas + motivo)
   ▼
SILVER  filas válidas, con tipos y claves
   │ agregar
   ▼
GOLD    resúmenes (ventas por cliente y mes, por ruta...)
   │
   ▼
Reporte / Power BI / Excel
```

**3. Qué garantiza cada capa.**

| Capa | Contiene | Garantía | Quién la usa |
|---|---|---|---|
| Bronze | datos crudos + fuente + fecha de carga | «esto es lo que llegó» (no se pierde nada) | el ETL; auditoría |
| Silver | registros válidos con tipos y claves | «esto es limpio y coherente» | analistas, validaciones |
| Rechazos | filas inválidas + motivo | «esto no pasó, y por qué» | revisión con el área dueña del dato |
| Gold | cifras agregadas | «esto es lo que se reporta» | gerencia, Power BI |

Silver conserva también las ventas **anuladas** si son hechos operativos del negocio; el filtro «solo entregadas» se aplica al calcular cada cifra de Gold, no al limpiar.

**4. La ecuación de auditoría.** Cada fila de Bronze debe terminar en un solo lugar:

`filas Bronze = duplicados exactos + rechazadas + filas Silver`

Si no se cumple, el proceso se detiene: se perdió o se duplicó algo.

**5. Un esquema con datos inventados.** Una pequeña simulación de las tres capas con 6 filas:

```python
import io
import pandas as pd

ORIGEN = """venta_id,cliente,estado,monto
1,Luna,entregado,100
2,Faro,entregado,50
2,Faro,entregado,50
3,Salud,anulado,80
4,Sol,entregado,abc
5,Palma,entregado,70
"""

bronze = pd.read_csv(io.StringIO(ORIGEN), dtype=str)
sin_duplicados = bronze.drop_duplicates()
monto = pd.to_numeric(sin_duplicados["monto"], errors="coerce")

rechazos = sin_duplicados[monto.isna()].assign(motivo="monto no numérico")
silver = sin_duplicados[monto.notna()].assign(monto=monto[monto.notna()])
gold = silver[silver["estado"] == "entregado"].groupby("cliente", as_index=False)["monto"].sum()

print(len(bronze), len(bronze) - len(sin_duplicados), len(rechazos), len(silver))
print(len(bronze) == (len(bronze) - len(sin_duplicados)) + len(rechazos) + len(silver))
print(gold)
```

```salida
6 1 1 4
True
  cliente  monto
0    Faro   50.0
1    Luna  100.0
2   Palma   70.0
```

Entran 6 filas (Bronze); 1 era duplicado exacto; 1 se rechazó (el monto `abc`); quedan 4 en Silver, y la ecuación `6 = 1 + 1 + 4` se cumple. Gold suma solo las **entregadas** (Luna 100, Faro 50, Palma 70): la venta anulada de Salud está en Silver pero no cuenta en Gold. Cada cifra se puede rastrear hasta sus filas.

**6. Lo que NO es el medallón.** Bronze, Silver y Gold describen estados de calidad y uso; **no obligan** a usar la nube ni productos específicos. En este curso son simplemente tablas o archivos con ese propósito.

**7. Lo que hace defendible un ETL.** En una entrevista te preguntarán «¿cómo sabes que tus cifras son correctas?». Respuestas sólidas: tengo un contrato de datos, conservé el crudo, cada fila rechazada tiene motivo, la ecuación de auditoría cuadra, los totales de Silver y Gold coinciden y puedo repetir el proceso y obtener lo mismo.

Ejemplo comercial: la distribuidora recibe cada día el archivo de ventas del ERP. Bronze lo guarda sin tocar; Silver lo limpia; Gold alimenta el tablero de la gerencia; los rechazos van al encargado de datos para corregir el origen. El tablero no cambia sin que alguien entienda por qué.

## Errores comunes

- **Mezclar las capas**: limpiar el archivo original y perder el crudo.
- **Filtrar en Silver lo que debería filtrarse al calcular Gold** (por ejemplo, descartar las anuladas al limpiar).
- **Rechazos sin motivo** o descartados sin registro.
- **No verificar la ecuación de auditoría.**
- **Creer que ELT o la nube garantizan calidad.**
- **Gold con cifras que no cuadran con Silver.**
- **No poder explicar de dónde sale una cifra.**

## Para comprobar que entendiste

1. ¿Qué contiene Bronze y por qué no se modifica?
2. ¿Qué diferencia hay entre ETL y ELT?
3. ¿Por qué Silver conserva las ventas anuladas?
4. ¿Qué dice la ecuación de auditoría?

<details><summary>Respuestas</summary>

1. Los datos como llegaron; no se modifica para poder auditar y repetir el proceso.
2. En ETL se transforma antes de cargar (en tu programa); en ELT se carga primero y se transforma dentro del destino.
3. Porque son hechos operativos; el filtro de «entregadas» se aplica al calcular cada indicador.
4. Filas de Bronze = duplicados exactos + rechazadas + filas de Silver.

</details>

## Micropráctica

1. Dibuja (en papel) el flujo de datos de un proceso que leería `ventas.csv`, produciría un reporte por ruta y guardaría los rechazos. Marca dónde viven Bronze, Silver, rechazos y Gold.
2. Con 8 filas inventadas, implementa las tres capas como en el ejemplo 5 y comprueba la ecuación.
3. Explica en tres frases cómo contestarías «¿cómo sé que las cifras del tablero son correctas?».

Cómo saber que está bien: tu ecuación cierra y tu Gold coincide con la suma de las entregadas de Silver.

<details><summary>Ejemplo de resolución de la parte 2</summary>

```python
import io
import pandas as pd

texto = """id,ruta,estado,monto
1,R01,entregado,10
2,R01,entregado,x
3,R02,anulado,30
3,R02,anulado,30
4,R02,entregado,40
5,R03,entregado,
6,R03,entregado,60
7,R01,entregado,70
"""
bronze = pd.read_csv(io.StringIO(texto), dtype=str)
unica = bronze.drop_duplicates()
monto = pd.to_numeric(unica["monto"], errors="coerce")
rechazos = unica[monto.isna()]
silver = unica[monto.notna()].assign(monto=monto[monto.notna()])
gold = silver[silver["estado"] == "entregado"].groupby("ruta", as_index=False)["monto"].sum()
print(len(bronze), len(bronze) - len(unica), len(rechazos), len(silver))
print(gold.values.tolist())
```

```salida
8 1 2 5
[['R01', 80.0], ['R02', 40.0], ['R03', 60.0]]
```

</details>

## Después, en los ejercicios

El mini-ETL (ME01–ME04) y el proyecto ETL siguen exactamente este mapa: [`03_EJERCICIOS/Puente/`](../../03_EJERCICIOS/Puente/) y [`05_PROYECTOS/`](../../05_PROYECTOS/). El ETL original validado está separado de las actividades para evitar copiarlo antes del intento. Siguiente: [5.2 El contrato de datos](02_contrato_de_datos.md).
