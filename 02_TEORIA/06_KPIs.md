# KPIs empresariales: definición antes de fórmula

Una métrica es una medida; un KPI es una medida elegida para seguir un objetivo y orientar una decisión. Debe declarar población, periodo, unidad, granularidad, numerador, denominador y criterio de acción. Un número sin contexto no permite evaluar desempeño.

Estos ejemplos y bases son sintéticos. Ningún KPI demuestra por sí mismo una causa.

## KPI 01 · Ventas netas y venta entregada

**Definición y fórmula:** Ventas netas = venta bruta − descuentos − devoluciones; unidad Bs, periodo y fecha contable definidos.

**Ejemplo numérico:** 1.000 − 50 − 100 = 850 Bs. En la base de práctica faltan descuentos/devoluciones, por eso solo calculamos ventas entregadas.

```python
venta_neta = 1000 - 50 - 100
assert venta_neta == 850
```

**Práctica SQL:** J2; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** No etiquetes 1.468.924,50 como ventas netas contables. Es el importe de pedidos entregados del dataset.

**Errores comunes:** Confundir pedido tomado, facturación y entrega; incluir anulados; omitir descuentos disponibles.


## KPI 02 · Crecimiento

**Definición y fórmula:** (Venta actual − venta anterior)/venta anterior × 100. Misma moneda, periodo y población.

**Ejemplo numérico:** De 100.000 a 120.000 Bs: +20%.

```python
anterior, actual = 100000, 120000
crecimiento = 100 * (actual-anterior) / anterior
assert crecimiento == 20
```

**Práctica SQL:** N5; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Un incremento no identifica su causa. Comprueba días hábiles, promociones y cobertura con datos adicionales.

**Errores comunes:** Anterior cero no da un porcentaje finito; comparar mes parcial con mes completo.


## KPI 03 · Cumplimiento de presupuesto

**Definición y fórmula:** Ventas reales/presupuesto × 100. Grano mes/ruta, presupuestos aditivos solo a ese nivel.

**Ejemplo numérico:** 80.000/100.000 = 80%; faltan 20.000 Bs.

```python
venta, meta = 80000, 100000
cumplimiento = None if meta == 0 else 100*venta/meta
assert cumplimiento == 80
```

**Práctica SQL:** N1; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** 80% expresa brecha contra meta, no necesariamente baja ejecución de visitas. Cruza indicadores operativos.

**Errores comunes:** Multiplicar presupuesto al unir detalle; promediar porcentajes de rutas; meta ausente como cero.


## KPI 04 · Cobertura de ejecución

**Definición y fórmula:** Visitas realizadas/visitas planificadas × 100 en el mismo periodo y universo.

**Ejemplo numérico:** 384 realizadas/480 planificadas = 80%.

```python
planificadas, realizadas = 480, 384
cobertura = 100*realizadas/planificadas
assert cobertura == 80
```

**Práctica SQL:** N2; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Sirve para revisar ejecución de agenda. Los datos de visitas son simulados y separados de entregas.

**Errores comunes:** Usar clientes compradores como sustituto de visitas; contar actividades fuera de agenda sin aclaración.


## KPI 05 · Cobertura de clientes

**Definición y fórmula:** Clientes únicos visitados/clientes únicos planificados × 100, no cantidad de visitas.

**Ejemplo numérico:** 96 visitados/120 planificados = 80%.

```python
clientes_plan, clientes_visit = 120, 96
cobertura_clientes = 100*clientes_visit/clientes_plan
assert cobertura_clientes == 80
```

**Práctica SQL:** N4; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Revisar clientes nunca visitados; varias visitas a un mismo cliente no aumentan cobertura única.

**Errores comunes:** Sumar coberturas diarias o contar clientes repetidos como nuevos.


## KPI 06 · Efectividad comercial

**Definición y fórmula:** Visitas realizadas que consiguieron pedido/visitas realizadas × 100.

**Ejemplo numérico:** 288 visitas con pedido/384 realizadas = 75%.

```python
con_pedido, realizadas = 288, 384
efectividad = 100*con_pedido/realizadas
assert efectividad == 75
```

**Práctica SQL:** N3; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Separar conversión de ejecución. Un pedido tomado no garantiza entrega ni venta final.

**Errores comunes:** Dividir por toda la agenda sin llamarlo conversión de agenda; mezclar preventa y liquidación.


## KPI 07 · Productividad de vendedor y ruta

**Definición y fórmula:** Salida útil por recurso y periodo: ventas/vendedor/día, entregas/día o visitas realizadas/día. Declara la medida.

**Ejemplo numérico:** Un vendedor vende 10.000 Bs en cinco días: 2.000 Bs/día.

```python
ventas_bs, dias_trabajados = 10000, 5
productividad = ventas_bs / dias_trabajados
assert productividad == 2000
```

**Práctica SQL:** J4; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** J4 compara ventas totales por vendedor; sin horas y días trabajados no demuestra productividad horaria.

**Errores comunes:** Comparar rutas de tamaño distinto; confundir mayor venta con mayor productividad.


## KPI 08 · Drop size y ticket medio

**Definición y fórmula:** Drop size: tamaño de una entrega. Ticket medio: importe total/documentos de venta definidos. Aquí un pedido entregado es un drop.

**Ejemplo numérico:** 1.468.924,50/3.442 = 426,76 Bs por pedido entregado.

```python
ventas, drops = 1468924.50, 3442
ticket = ventas/drops
assert round(ticket,2) == 426.76
```

**Práctica SQL:** K1, N9; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Calcula primero monto por pedido. Reporta media y mediana si hay asimetría.

**Errores comunes:** Promediar valor de líneas o promedios de rutas; llamar Bs por entrega a unidades por entrega.


## KPI 09 · Frecuencia

**Definición y fórmula:** Pedidos entregados/clientes compradores únicos en un periodo. También puede medirse intervalo entre compras, pero es otro KPI.

**Ejemplo numérico:** Septiembre: 722 pedidos/101 activos = 7,15 pedidos por cliente activo.

```python
pedidos, activos = 722, 101
frecuencia = pedidos/activos
assert round(frecuencia,2) == 7.15
```

**Práctica SQL:** N12; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Indica intensidad entre compradores; no describe a quienes no compraron. Declara el denominador.

**Errores comunes:** Dividir por clientes maestros sin cambiar el nombre de la métrica; sumar frecuencias mensuales.


## KPI 10 · Recencia, activos e inactivos

**Definición y fórmula:** Recencia = días desde última compra entregada hasta corte fijo. Activo mensual = tuvo compra en mes; inactivo >60 días es otra regla.

**Ejemplo numérico:** Última compra 25/09 y corte 30/09: cinco días.

```python
from datetime import date
recencia = (date(2026,9,30)-date(2026,9,25)).days
assert recencia == 5
```

**Práctica SQL:** V1, V2, N7, N12; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Hay 101 activos en septiembre, 19 sin compra ese mes y 11 con recencia >60 días. Son definiciones distintas.

**Errores comunes:** Corte variable con fecha actual; excluir nunca compradores del reporte sin aclararlo.


## KPI 11 · ABC y Pareto

**Definición y fórmula:** ABC por ventas usa aporte acumulado ordenado. Por diversidad de SKU usa SKU distintos y umbrales acordados. Pareto describe concentración, no obliga a 80/20.

**Ejemplo numérico:** V4 obtiene A=41 con 80,5% de ventas; B=37 con 14,6%; C=42 con 4,9%.

```python
clases = {"A":41,"B":37,"C":42}
assert sum(clases.values()) == 120
```

**Práctica SQL:** V4, N10; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Prioriza análisis según la pregunta. Para reposición, variedad puede importar más que ventas.

**Errores comunes:** Cambiar convención del cliente que cruza umbral; intercambiar ABC por valor y ABC por SKU.


## KPI 12 · Rotación de inventario

**Definición y fórmula:** Salidas en unidades/stock promedio en unidades del mismo periodo. Stock promedio aproximado=(inicial+final)/2.

**Ejemplo numérico:** Salidas 300; inicial 100 y final 200: rotación 2 veces.

```python
inicial, final, salidas = 100, 200, 300
rotacion = salidas / ((inicial+final)/2)
assert rotacion == 2
```

**Práctica SQL:** N11; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** El inventario del ejercicio es un caso separado simulado. No atribuyas sus salidas a la venta histórica del otro dataset.

**Errores comunes:** Dividir ventas Bs por unidades; promediar solo extremos cuando hay grandes fluctuaciones sin advertirlo.


## KPI 13 · Variación absoluta y porcentual

**Definición y fórmula:** Brecha = actual−referencia; relativa = brecha/referencia ×100. Puede comparar venta, meta o coste.

**Ejemplo numérico:** 80.000 contra 100.000: −20.000 Bs y −20%.

```python
real, ref = 80000, 100000
brecha = real-ref
variacion = 100*brecha/ref
assert (brecha,variacion) == (-20000,-20)
```

**Práctica SQL:** N1, N5; contratos y corrector en `03_EJERCICIOS/SQL`.

**Interpretación empresarial:** Muestra Bs y porcentaje para evaluar magnitud; misma fecha y población.

**Errores comunes:** Signos invertidos; dividir por actual; bases de comparación diferentes.


## Cuando faltan datos

Escribe "no calculable con las fuentes actuales", identifica el campo requerido y propone cómo registrarlo. No sustituyas cobertura de visitas por clientes compradores, venta neta por venta bruta, ni productividad horaria por venta total. El gerente debe poder distinguir un resultado observado de una hipótesis.
