# Evidencia requerida en Power BI Desktop

Estado de estas casillas: pendientes; no se ejecutaron en este entorno.

- [ ] Importar todos los CSV con tipos correctos y sin filas descartadas.
- [ ] Crear relaciones 1:* de MODELO.md, sin rutas ambiguas.
- [ ] Marcar dim_fecha[fecha] como tabla de fechas; 183 días únicos.
- [ ] Aplicar DAX y comprobar total 1468924,50 Bs; pedidos 3442; ticket 426,76.
- [ ] Filtrar septiembre con dim_fecha: 300922 Bs y 722 pedidos.
- [ ] Filtrar R01 y periodo completo: 211141,50 Bs.
- [ ] Filtrar categoría Lácteos: 406249 Bs.
- [ ] Comparar cumplimiento por dim_mes/ruta contra N1; no usar producto o día parcial.
- [ ] Cobertura 80%, efectividad 75%; diferencia entre visitas y pedidos entregados explicada.
- [ ] Comprobar meses anteriores y primer periodo BLANK; revisar selección parcial.
- [ ] Actualizar CSV y refrescar sin duplicar; revisar captura con filtros visibles.
- [ ] Guardar .pbix propio y documentar dos hallazgos y límites.

Entrega: capturas, medidas aplicadas, control_modelo.json y README. Nunca declares verificados
los filtros de Desktop solo porque los CSV y totales Python pasaron.
