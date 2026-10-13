# Proyecto SQL comercial

Problema: gerencia necesita conocer venta entregada, concentración, clientes inactivos
y ejecución de visitas, sin confundir agenda, preventa y entrega.
Base `04_DATASETS/comercial.db`. Los datos son sintéticos.

## Construye por etapas

1. Semana 1: describe cinco tablas, granularidad, tipos y nulos; guarda S/G propios.
2. Semana 2: une clientes/pedidos/ítems, cuadra ventas por ruta y categoría.
3. Semana 3: calcula ticket, recencia, ventanas y ABC con convención explícita.
4. Semana 4: añade visitas/presupuesto y tres recomendaciones con límites.

Entregables: `mi_trabajo/sql/*.sql`, README propio, diccionario breve y `hallazgos.md`.
Consultas mínimas: G1, J2, J4, J5, K2 b, V2, V4, N1, N2 y N3.
Corrector: `python herramientas/corregir_sql.py J2 mi_trabajo/sql/J2.sql`.

## Criterios de aceptación

- [ ] Ventas 1468924,50 Bs, 3442 entregados; agrupaciones suman el total.
- [ ] ABC, recencia y denominadores se explican sin leer el código.
- [ ] Clientes sin compras no desaparecen por un LEFT JOIN mal filtrado.
- [ ] Presupuesto no se multiplica al unir detalle.
- [ ] README permite repetir las consultas y contiene limitaciones.

Usa `05_PROYECTOS/README_PLANTILLA.md` como estructura; no publiques la solución de referencia
como si fuera tu trabajo. Las plantillas originales v 3 se preservan en el ZIP de originales;
su estructura SQL/ETL/BI se reutiliza y adapta a las rutas únicas de v 5.
