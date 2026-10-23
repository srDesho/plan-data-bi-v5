# REL1 · Una regla más sin romper el cuadre

Nivel 2/3 · Tiempo objetivo 35 min · Primera vez: 30–40 min.
REFUERZO sobre lo ya estudiado. Repasa las lecciones [5.3](../../02_TEORIA/05_calidad_ETL/03_rechazos_y_reconciliacion.md) y [5.4](../../02_TEORIA/05_calidad_ETL/04_cargas_registro_reproducibilidad.md). Parte de tu `mi_trabajo/mini_etl/mini_etl.py` con ME03 y ME04 ya aprobados.

## Situación

El supervisor del mini-ETL de ventas pide otra regla de calidad: **una línea cuyo monto (`unidades × precio`) supere Bs 5.000 se rechaza** con causa `monto`, porque suele ser un error de digitación. Ya tienes la regla de ME04 (más de 500 unidades se rechaza por `unidades`). Debes añadir la nueva **sin reescribir el flujo** y sin romper la ecuación de conteos.

## Qué debes hacer

1. Añade la regla de monto a tu `transformar`: si una línea es válida en `unidades` y en `precio`, calcula `unidades × precio` en centavos; si supera 500.000 centavos, se rechaza con una causa que contenga la palabra `monto`.
2. Prueba con tu propia copia de `04_DATASETS/mini_etl/ventas_mini_raw_v2.csv` a la que agregas dos filas al final:

```
T027;2026-10-13;Tienda Sol;P-01;480;entregado;Bs 10,50
T028;2026-10-13;Tienda Sol;P-01;480;entregado;Bs 10,00
```

   Antes de ejecutar, calcula a mano cuál de las dos se rechaza y cuáles serán los nuevos conteos de bronze, rechazados y silver.
3. Comprueba la ecuación `filas del raw = duplicados exactos + rechazadas + filas Silver` con las métricas que devuelve `ejecutar`, y que con el raw original el resultado de ME03 no cambia.
4. Anota en `mi_trabajo/errores.md` qué línea de tu código tocaste y por qué no hubo que cambiar nada más.

## Reglas

- Las filas que ya se rechazaban por otra causa no cambian de causa.
- La carga sigue siendo repetible: dos ejecuciones seguidas dan las mismas métricas.
- Trabaja en tu `mini_etl.py`; copia ahí cualquier función que reutilices.

## Cómo comprobarlo

`python herramientas/corregir_nuevos.py REL1 mi_trabajo/mini_etl/mini_etl.py`. El corrector ejecuta tu `ejecutar` sobre el raw v2 con las dos filas agregadas y comprueba conteos, causas y que ME03 siga cumpliéndose; dice qué métrica o qué ticket falló, no muestra la solución.

## Pistas (en este orden, solo cuando las necesites)

1. **Orientación.** Una regla nueva se agrega donde ya validas el resto de la fila; no crees un segundo flujo.
2. **Concepto.** Las causas se acumulan en la lista de motivos de la fila; la ecuación de conteos se cumple mientras cada fila termine en exactamente un lugar: duplicado, rechazo o Silver (lecciones 5.3 y 5.4).
3. **Si no cuadra.** Si T028 se rechaza, comparas con `>=` o con otra unidad (Bs en vez de centavos). Si no se rechaza T027, revisa que calculas el monto después de convertir unidades y precio a números.

Método: intenta 10 minutos antes de leer la primera pista y depura otros 10 antes de la tercera.

## Criterios de aceptación

- [ ] T027 se rechaza con causa `monto` y T028 pasa a Silver.
- [ ] La ecuación de conteos se cumple con el raw v2 ampliado y con el raw original.
- [ ] Las reglas de ME03 y ME04 siguen funcionando.
- [ ] Explicas en una frase qué línea tocaste y por qué la separación en funciones evitó otros cambios.
- [ ] Anotaste en `mi_trabajo/errores.md` un error o aprendizaje de este ejercicio.

Solución separada: `08_SOLUCIONES/mini_etl_rel1_referencia.py` (ábrela solo después de tu intento).
