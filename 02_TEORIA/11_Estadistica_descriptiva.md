# Estadística empresarial: describir la población correcta

Empieza por la unidad observada: ¿pedido, cliente, visita o vendedor? Luego especifica periodo, filtro y variable. El drop del dataset es una entrega expresada en Bs; no mide rentabilidad ni litros. Mezclar unidades produce estadísticas inútiles aunque la fórmula sea correcta.

La media suma valores y divide por cantidad. La mediana divide los valores ordenados en dos mitades; con cantidad par promedia los dos centrales. La moda es el valor más frecuente y puede haber varias o ninguna relevante. En `[120,80,450,60,230,90,1100,75,320,180,90,95,210,85,90]`: media 218,33, mediana 95 y moda 90. Un pedido de 1.100 eleva la media; no demuestra por sí mismo un error.

Rango = máximo−mínimo. Varianza expresa dispersión cuadrática; desviación estándar vuelve a las unidades originales. Para describir toda una población divide por n; para estimar varianza poblacional a partir de una muestra usa n−1. En Python `statistics.stdev` es muestral y `pstdev` poblacional. No mezcles resultados de Excel `DESVEST.M` y `DESVEST.P` sin explicar la elección.

En 3.442 pedidos entregados: media 426,7648, mediana 354 y desviación muestral 307,7396 Bs. La media responde "venta total por entrega"; la mediana describe una entrega central. Puedes reportar ambas. Ninguna es automáticamente la mejor para todas las decisiones.

## Percentiles e IQR

Un percentil indica el umbral bajo el cual se sitúa un porcentaje de observaciones según una convención de cálculo. Pandas utiliza aquí interpolación lineal; usa la misma convención al comparar herramientas. Q1=214,125 y Q3=555,75; IQR=341,625. Cercas de Tukey: Q1−1,5×IQR y Q3+1,5×IQR. Hay 141 observaciones fuera de esas cercas.

Un atípico es una señal para investigar. No se elimina automáticamente: una venta mayorista puede ser válida. Revisa cantidad, precio, cliente y tipo de canal. Documenta si tu informe incluye o excluye el valor y muestra el efecto de la decisión.

## Distribución y normalidad

El histograma depende de los intervalos; el diagrama de caja destaca posición y atípicos. La asimetría positiva 1,7697 indica cola hacia valores altos. Una distribución normal es simétrica y queda descrita por media y desviación; no asumas normalidad de ventas solo porque conoces ambas. El z-score `(x−media)/desviación` estandariza distancia; 64 pedidos tienen |z|>3 usando desviación poblacional, pero eso no es una probabilidad normal exacta para una distribución asimétrica.

## Muestreo y correlación

Una muestra de clientes convenientes puede excluir rutas difíciles. Define población, marco muestral y método (por ejemplo aleatorio estratificado por ruta). Si tomas varios pedidos del mismo cliente, no tienes igual cantidad de clientes independientes. Correlación describe asociación; campañas, estacionalidad o tamaño del cliente pueden explicar dos variables sin que una cause la otra.

Práctica ST01–ST04, notebook N04 y caso C03. Entrega gráfico con título que describa un hallazgo, unidad, periodo y recomendación. Fuente: SciPy stats; la interpretación y los ejemplos de negocio están desarrollados aquí para estudiar sin depender de búsquedas.
