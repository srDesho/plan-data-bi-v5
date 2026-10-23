# Capítulo 12 — Estadística inferencial: decidir con incertidumbre

Aquí das el salto de **describir** los datos a **concluir** algo sobre una población más grande a partir de una muestra, midiendo la incertidumbre en lugar de ignorarla. El orden es deliberado: primero entiendes de dónde sale la variabilidad (con una simulación), luego estimas (intervalos), luego decides (hipótesis, p-valor), luego aplicas dos pruebas (t y chi-cuadrado) y por último aprendes a medir el tamaño del efecto y a comunicar con límites. **No se empieza con funciones de SciPy**: cada cálculo se hace antes a mano, con datos pequeños e inventados, y SciPy solo se usa para verificarlo.

**Tiempo total estimado de primera vez:** unas 8 h 5 min (8 lecciones). Recomendado: una lección por sesión; la 12.4 (p-valor por permutación) merece repetirse con calma.

**Antes de empezar:** el [capítulo 11](11_Estadistica_descriptiva.md) completo (sobre todo desviación estándar con `n − 1`, y muestreo). Se usa `scipy` 1.17 y `numpy`; las versiones están en `requirements.txt`.

## Lecciones

| # | Lección | Qué aprendes | Tipo | Tiempo |
|---|---|---|---|---|
| 12.1 | [Por qué hace falta la inferencia](12_Estadistica_inferencia/01_por_que_inferencia.md) | variabilidad entre muestras, error estándar, simulación | NÚCLEO · D36 | 55 min |
| 12.2 | [Estimación e intervalos de confianza](12_Estadistica_inferencia/02_estimacion_intervalo_confianza.md) | `x̄ ± t*·s/√n`, qué significa el 95 %, cobertura | NÚCLEO · D37 | 65 min |
| 12.3 | [Hipótesis nula y alternativa](12_Estadistica_inferencia/03_hipotesis.md) | `H0`, `H1`, `α`, errores tipo I y II, potencia | NÚCLEO · D37 | 60 min |
| 12.4 | [El p-valor, calculado de verdad](12_Estadistica_inferencia/04_pvalor.md) | permutación a mano, qué es y qué no es | NÚCLEO · D38 | 65 min |
| 12.5 | [Prueba t: Student y Welch](12_Estadistica_inferencia/05_prueba_t_welch.md) | estadístico, grados de libertad, supuestos | NÚCLEO · D39 | 70 min |
| 12.6 | [Chi-cuadrado](12_Estadistica_inferencia/06_chi_cuadrado.md) | tablas de contingencia, esperados, Yates | COMPLEMENTARIA | 60 min |
| 12.7 | [Tamaño del efecto](12_Estadistica_inferencia/07_tamano_del_efecto.md) | d de Cohen, puntos porcentuales, V de Cramér, significancia práctica | COMPLEMENTARIA | 55 min |
| 12.8 | [Interpretar, comunicar y no equivocarse](12_Estadistica_inferencia/08_interpretacion_limitaciones.md) | comparaciones múltiples, lenguaje correcto, plantilla de informe | NÚCLEO · D39 | 55 min |

## Ideas centrales

- Una estimación sin su incertidumbre es incompleta.
- El p-valor mide qué tan raros serían los datos **si `H0` fuera cierta**; no es la probabilidad de que `H0` sea cierta.
- «No rechazar `H0`» no es «`H0` es cierta»: con pocos datos, la prueba tiene poca potencia.
- Significativo no es lo mismo que importante: reporta siempre el tamaño del efecto y el intervalo.
- Cada comparación adicional aumenta el riesgo de falsas alarmas.
- Sin asignación aleatoria no hay conclusión causal; toda conclusión termina con una limitación.
- Las pruebas se calculan **a mano** antes de verificarlas con Python; si el resultado de la herramienta no coincide, revisa primero los supuestos y las opciones por defecto (corrección de Yates, `equal_var`).

## Ejercicios autónomos de este capítulo

ST05–ST07, el caso C03 y el notebook N05 en [`03_EJERCICIOS/Estadistica/`](../03_EJERCICIOS/Estadistica/). Cada entrega lleva: hipótesis y `α`, prueba usada y por qué, resultado, tamaño del efecto, interpretación de negocio y limitaciones. Las microprácticas de las lecciones no son evaluables.

Términos: [glosario](GLOSARIO.md). Fuentes: [FUENTES.md](FUENTES.md).

Siguiente capítulo: [Capítulo 13 — Modelado dimensional](13_Modelado.md).
