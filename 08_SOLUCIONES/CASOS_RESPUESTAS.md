# Corrección de casos

| Caso | Resultado y criterio |
|---|---|
|C01|Cumplimiento 80%, cobertura 80%, efectividad 75%, brecha−20000 Bs. No atribuir causa sin datos adicionales.|
|C02|Actividades 9/12=75%; clientes 8/10=80%. Los denominadores responden preguntas diferentes.|
|C03|Media 426,76; mediana 354; P90=819;141 atípicos. Grandes entregas pueden ser válidas; investigar cliente/producto.|
|C04|Diferencia 65700,50 Bs corresponde a ítems de pedidos anulados. Cuadrar G3 contra J2 con el mismo periodo.|
|C05|3.7 se rechaza, precio ilegible no es 0; catálogo duplicado detiene carga. Esperar error en tests P09/P11/P21.|
|C06|Usa controles_transferencia.json y validar_final.py --transferencia; exige lógica propia, cuadres y segunda ejecución.|
|EX01|Suma 1468924,50;3442 pedidos; R01=211141,50 y R02=396680,50. Tabla por ruta contra E4.|
|EX02|Comparar tabla N1 completa; cumplimiento global=sumaVentas/sumaPresupuesto. No promedio de tasas.|
|EX03|Media 426,7648; mediana 354; desv 307,7396; Q1=214,125; Q3=555,75; P90=819.|
|PB01|fact 16178; dimCliente 120; dimProducto 40; dimVendedor 6; dimFecha 183; dimMes 6; dimRuta 6; presupuesto 36; visitas 480.|
|PB02|Relaciones MODELO.md sin ambigüedad; tipos compatibles y fecha marcada. Verificar manualmente.|
|PB03|Total 1468924,50;3442; ticket 426,76; septiembre 300922 y 722.|
|PB04|Primer mes sin anteriorBLANK; presupuesto mensual/ruta y control N1; documentar filtros parciales.|
|PB05|Valorar claridad de decisiones, filtros, unidades, comparaciones y límites; no premiar decoración.|
|PB06|R01=211141,50; Lácteos 406249; septiembre 300922; total 1468924,50; actualización comprobada en Desktop.|
