# Cifras de control de los ejercicios de evidencia manual (plan v6)

Ábrelo solo **después** de entregar tu intento. Excel, Power Query y Power BI no se ejecutan en este paquete: estas cifras son lo que debe darte tu archivo; lo que no ejecutes queda registrado como PENDIENTE.

## EX04 · Ventas por ruta y mes, presupuesto y diferencia

- Total de ventas entregadas abril–septiembre de 2026: **Bs 1.468.924,50**; total del presupuesto del periodo: **Bs 2.115.000**; cumplimiento total ponderado: **69,5 %**.
- La tabla resumen tiene 36 filas (6 rutas × 6 meses) y la columna de diferencia contra tu SQL vale 0 en todas.

Ventas entregadas (Bs) por ruta y mes:

| ruta | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 |
|---|---|---|---|---|---|---|
| R01 | 43.915,50 | 38.962,00 | 36.287,50 | 29.079,50 | 27.580,50 | 35.316,50 |
| R02 | 66.366,00 | 64.360,00 | 57.351,00 | 72.467,00 | 55.429,00 | 80.707,50 |
| R03 | 15.757,00 | 27.807,00 | 17.630,50 | 18.593,00 | 22.342,50 | 36.196,00 |
| R04 | 40.869,50 | 27.993,00 | 40.578,50 | 35.965,00 | 27.482,00 | 48.260,00 |
| R05 | 53.036,00 | 62.719,00 | 59.588,50 | 52.167,00 | 45.730,00 | 68.298,00 |
| R06 | 26.436,00 | 25.100,50 | 33.235,00 | 22.710,50 | 20.464,00 | 32.144,00 |

## RE01 · Cumplimiento de septiembre por ruta (ponderado)

| ruta | ventas sep (Bs) | presupuesto sep (Bs) | cumplimiento % |
|---|---|---|---|
| R01 | 35.316,50 | 52.500 | 67,3 |
| R02 | 80.707,50 | 55.000 | 146,7 |
| R03 | 36.196,00 | 57.500 | 62,9 |
| R04 | 48.260,00 | 60.000 | 80,4 |
| R05 | 68.298,00 | 62.500 | 109,3 |
| R06 | 32.144,00 | 65.000 | 49,5 |

Total septiembre: ventas Bs 300.922,00, presupuesto Bs 352.500, cumplimiento ponderado **85,4 %** (no es el promedio de los seis porcentajes).

## PQ01 · Visitas realizadas con semana

- Filas de `visitas.csv`: 480; con `realizada = 1`: **384**; sin duplicados de `visita_id` (480 claves distintas antes y 384 después del filtro).
- Semana = lunes de la semana de la visita (`Date.StartOfWeek(fecha, Day.Monday)`):

| semana (lunes) | visitas realizadas |
|---|---|
| 2026-08-31 | 96 |
| 2026-09-07 | 96 |
| 2026-09-14 | 96 |
| 2026-09-21 | 96 |

## RQ01 · Inventario con nulos

- `inventario.csv` tiene 40 filas. Si vacías `stock_final` en los productos 7 y 23 de tu copia: **38 filas completas** en la consulta principal, **2 filas** en la consulta de revisión y 40 en total. No se imputa ningún valor.

## PB07 · Cifras para validar el panel mínimo

| medida | todo el periodo (abr–sep) | septiembre |
|---|---|---|
| Ventas Bs | 1.468.924,50 | 300.922,00 |
| Pedidos Entregados | 3.442 | 722 |
| Ticket Bs | 426,76 | 416,79 |
| Cumplimiento % | 69,5 | 85,4 |

Con el segmentador de ruta en `R02` las cifras cambian; valida con SQL cada combinación que muestres en pantalla.

## RB01 · Ventas de Bebidas con CALCULATE

- Ventas de la categoría Bebidas en todo el periodo: **Bs 276.186,50**; en septiembre de 2026: **Bs 56.324,00**.
- Participación de Bebidas en septiembre: **18,7 %** de las ventas del mes (Bs 300.922,00).
