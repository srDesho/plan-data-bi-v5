# Comprobación individual de los 81 ejercicios SQL

Generada por `python herramientas/auditar_enunciados.py --tabla RUTA`. Cada fila resume qué se verificó automáticamente: columnas del enunciado frente al contrato, filas del contrato, resultado de la referencia frente al control mediante el corrector, tres pistas y criterios propios. «Cambio en la referencia» documenta cada modificación hecha en esta revisión y por qué.

| ID | Nivel | Primera vez | Columnas | Filas | Referencia = control (corrector) | 3 pistas | Criterios propios | Cambio en la referencia |
|---|:-:|---:|---:|---:|:-:|:-:|---:|---|
| S1 | 1 | 20–35 min | 6 | 10 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| S2 | 1 | 10–20 min | 1 | 5 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| S3 | 1 | 15–25 min | 6 | 14 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| S4 | 1 | 15–25 min | 2 | 3 | sí | sí | 3 | — |
| S5 | 1 | 15–25 min | 6 | 15 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| S6 | 1 | 15–30 min | 6 | 12 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| S7 | 1 | 15–30 min | 6 | 6 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| S8 | 1 | 15–30 min | 5 | 399 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| S9 | 1 | 20–35 min | 3 | 8 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| S10 | 1 | 10–20 min | 1 | 1 | sí | sí | 2 | — |
| G1 | 1 | 15–25 min | 2 | 2 | sí | sí | 1 | orden explícito en la referencia (el contenido del control no cambia) |
| G2 | 1 | 10–20 min | 1 | 1 | sí | sí | 1 | — |
| G3 | 1 | 15–25 min | 1 | 1 | sí | sí | 2 | — |
| G4 | 1 | 20–35 min | 4 | 5 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| G5 | 1 | 15–25 min | 2 | 6 | sí | sí | 1 | orden explícito en la referencia (el contenido del control no cambia) |
| G6 | 1 | 20–35 min | 2 | 3 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| G7 | 1 | 20–35 min | 3 | 32 | sí | sí | 3 | — |
| G8 | 1 | 25–40 min | 2 | 6 | sí | sí | 2 | — |
| J1 | 2 | 25–40 min | 3 | 3600 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| J2 | 2 | 25–45 min | 1 | 1 | sí | sí | 2 | — |
| J3 | 2 | 30–50 min | 2 | 5 | sí | sí | 1 | — |
| J4 | 2 | 25–45 min | 2 | 6 | sí | sí | 1 | — |
| J5 | 2 | 35–60 min | 2 | 19 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| J6 | 2 | 25–45 min | 2 | 5 | sí | sí | 2 | — |
| K1 | 3 | 35–60 min | 4 | 3442 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| K2a | 3 | 35–60 min | 1 | 1 | sí | sí | 1 | — |
| K2b | 3 | 40–65 min | 3 | 6 | sí | sí | 1 | — |
| K3 | 3 | 40–70 min | 2 | 1325 | sí | sí | 2 | — |
| K4 | 3 | 40–70 min | 2 | 3 | sí | sí | 2 | — |
| K5 | 3 | 40–65 min | 4 | 10 | sí | sí | 2 | — |
| K6 | 3 | 45–75 min | 3 | 5 | sí | sí | 2 | — |
| V1 | 3 | 30–50 min | 3 | 120 | sí | sí | 1 | — |
| V2 | 3 | 45–75 min | 4 | 11 | sí | sí | 3 | — |
| V3 | 3 | 50–80 min | 4 | 15 | sí | sí | 3 | — |
| V4 | 3 | 55–90 min | 3 | 3 | sí | sí | 3 | — |
| V5 | 3 | 55–90 min | 4 | 18 | sí | sí | 2 | — |
| X1 | 3 | 30–50 min | 2 | 6 | sí | sí | 1 | — |
| X2 | 3 | 40–65 min | 2 | 6 | sí | sí | 1 | — |
| X3 | 3 | 30–50 min | 2 | 10 | sí | sí | 1 | — |
| X4 | 3 | 40–65 min | 3 | 5 | sí | sí | 1 | — |
| X5 | 3 | 40–65 min | 4 | 6 | sí | sí | 2 | — |
| X6 | 3 | 30–50 min | 4 | 1 | sí | sí | 1 | — |
| X7 | 3 | 40–65 min | 3 | 6 | sí | sí | 1 | orden explícito en la referencia (el contenido del control no cambia) |
| X8 | 3 | 40–65 min | 3 | 6 | sí | sí | 1 | orden explícito en la referencia (el contenido del control no cambia) |
| E1 | 2 | 25–40 min | 2 | 4 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| E2 | 2 | 20–35 min | 2 | 3 | sí | sí | 1 | — |
| E3 | 2 | 25–40 min | 2 | 6 | sí | sí | 1 | — |
| E4 | 2 | 30–50 min | 2 | 6 | sí | sí | 1 | — |
| E5 | 2 | 35–60 min | 2 | 17 | sí | sí | 3 | orden explícito en la referencia (el contenido del control no cambia) |
| E6 | 2 | 35–55 min | 3 | 25 | sí | sí | 2 | — |
| E7 | 2 | 30–50 min | 2 | 3 | sí | sí | 1 | orden explícito en la referencia (el contenido del control no cambia) |
| E8 | 2 | 35–60 min | 2 | 51 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| CL1 | 2 | 20–35 min | 1 | 1 | sí | sí | 1 | — |
| CL2 | 2 | 20–35 min | 2 | 120 | sí | sí | 1 | — |
| CL3 | 2 | 25–40 min | 2 | 8 | sí | sí | 2 | orden explícito en la referencia (el contenido del control no cambia) |
| CL4 | 2 | 30–50 min | 1 | 1 | sí | sí | 3 | — |
| N1 | 3 | 60–100 min | 5 | 36 | sí | sí | 3 | — |
| N2 | 3 | 35–60 min | 3 | 1 | sí | sí | 1 | — |
| N3 | 3 | 35–60 min | 3 | 1 | sí | sí | 1 | — |
| N4 | 3 | 40–70 min | 2 | 1 | sí | sí | 2 | — |
| N5 | 3 | 60–100 min | 3 | 6 | sí | sí | 1 | alias `ventas_bs` en la segunda columna (solo el nombre del contrato) |
| N6 | 3 | 45–80 min | 2 | 6 | sí | sí | 1 | — |
| N7 | 3 | 50–80 min | 3 | 120 | sí | sí | 1 | — |
| N8 | 3 | 40–70 min | 2 | 2 | sí | sí | 1 | — |
| N9 | 3 | 35–60 min | 1 | 1 | sí | sí | 1 | — |
| N10 | 3 | 45–75 min | 2 | 120 | sí | sí | 1 | — |
| N11 | 3 | 35–60 min | 2 | 40 | sí | sí | 1 | — |
| N12 | 3 | 40–65 min | 3 | 1 | sí | sí | 1 | — |
| N13 | 3 | 30–50 min | 4 | plan | sí | sí | 2 | — |
| N14 | 3 | 40–65 min | 4 | 120 | sí | sí | 2 | — |
| N15 | 3 | 45–75 min | 3 | 40 | sí | sí | 2 | — |
| N16 | 3 | 35–60 min | 3 | 6 | sí | sí | 1 | — |
| ES1A | 1 | 10–20 min | 2 | 25 | sí | sí | 1 | — |
| ES1B | 1 | 15–30 min | 3 | 2 | sí | sí | 1 | filtro cambiado a «precio medio > 9 Bs» (el anterior no filtraba nada): control de 5 a 2 filas |
| ES1C | 1 | 10–20 min | 1 | 1 | sí | sí | 1 | — |
| ES2A | 2 | 20–35 min | 1 | 1 | sí | sí | 1 | — |
| ES2B | 2 | 25–40 min | 2 | 30 | sí | sí | 1 | — |
| ES2C | 2 | 20–35 min | 3 | 6 | sí | sí | 1 | — |
| ES3A | 3 | 30–50 min | 2 | 6 | sí | sí | 1 | — |
| ES3B | 3 | 25–45 min | 2 | 11 | sí | sí | 1 | — |
| ES3C | 3 | 30–50 min | 3 | 6 | sí | sí | 1 | competencia cambiada de RANK a participación con ventana (practicada en V3): control nuevo |
