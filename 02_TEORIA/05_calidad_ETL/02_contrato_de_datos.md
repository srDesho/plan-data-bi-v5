# 5.2 El contrato de datos: escribirlo antes de programar

> Tiempo estimado: 50 min (lectura 25 + práctica 25). Prerrequisitos: [5.1 ETL y medallón](01_etl_elt_medallon.md) y [9.3 Perfilado](../09_Pandas_basico/03_inspeccionar.md).

## Para qué sirve

La causa más frecuente de un ETL frágil es programar sin haber decidido qué es un dato válido. Si no puedes decir, para tres filas escritas a mano, cuáles pasan y cuáles se rechazan, todavía no estás listo para procesar 12 000. El **contrato de datos** es ese documento corto: cuando existe, el código se escribe casi solo, y las decisiones difíciles quedan por escrito en lugar de estar en la cabeza de quien programó.

## Términos nuevos

- **Contrato de datos**: la descripción, por escrito, de lo que debe cumplir un archivo o tabla: columnas, tipos, claves, formatos, valores permitidos y qué hacer con lo que no cumple.
- **Clave de negocio**: la columna o combinación que identifica un registro (por ejemplo, `linea_id`).
- **Formato admitido**: la forma de escritura aceptada para un campo (fechas `DD/MM/AAAA` o ISO).
- **Regla de rechazo**: una condición que, si se cumple, manda la fila a rechazos con un motivo.
- **Regla de detención**: una condición que, si se cumple, **detiene** todo el proceso (falta una columna obligatoria, clave duplicada con contenido distinto).
- **Regla de normalización**: una transformación permitida para unificar valores (quitar espacios, pasar a minúsculas, cambiar coma decimal).
- **Cuadre**: una igualdad que el resultado debe cumplir (filas, totales).
- **Expresión regular**: un patrón de texto que describe la forma que debe tener una cadena. Por ejemplo, `\d+` significa «uno o más dígitos»; con `re.fullmatch(patron, texto)` se comprueba que **todo** el texto cumpla el patrón.
- **Supuesto**: algo que se da por cierto sin comprobarlo; debe quedar escrito (por ejemplo, «cada ruta tiene un solo vendedor»).

## Ejemplo paso a paso

Imagina que recibes un archivo de ventas de kioscos con estas primeras filas (inventadas):

```text
id_venta;fecha;kiosco;producto;cantidad;precio;estado
V-001;03/09/2026;Luna;Agua 2L;10;Bs 6,00;entregado
V-002;2026-09-03;Faro;Jugo 1L;4;9;Entregado
V-003;03/09/2026;;Agua 2L;1.5;6;entregado
```

**1. Primero, observar (perfilar).** Ya ves cuatro cosas: el separador es `;`; hay dos formatos de fecha; el precio trae `Bs` y coma en una fila; la cantidad `1.5` no es entera; falta un kiosco; y el estado viene con mayúscula en una fila. **No programes todavía.**

**2. Escribir el contrato.** Una tabla corta, campo por campo:

| Campo | Tipo | Obligatorio | Formato / valores admitidos | Si no cumple |
|---|---|---|---|---|
| `id_venta` | texto | sí | único en el archivo | clave repetida con contenido distinto → **detener**; repetida igual → duplicado exacto |
| `fecha` | fecha | sí | `DD/MM/AAAA` o `AAAA-MM-DD` | rechazar: «fecha inválida» |
| `kiosco` | texto | sí | no vacío, existe en el catálogo | rechazar: «kiosco ausente / no existe» |
| `producto` | texto | sí | existe en el catálogo de productos | rechazar: «producto no existe» |
| `cantidad` | entero | sí | entero positivo | rechazar: «cantidad no entera / no positiva» (no truncar) |
| `precio` | decimal | sí | número positivo; se admite prefijo `Bs` y coma decimal | rechazar: «precio inválido» |
| `estado` | texto | sí | `entregado` o `anulado` (sin importar mayúsculas ni espacios) | rechazar: «estado no permitido» |

Más tres cosas que el contrato también debe decir:

- **Qué es una fila:** una línea de venta.
- **Clave única:** `id_venta` (más el producto si una venta puede traer varios).
- **Cuadres:** `Bronze = duplicados + rechazados + Silver`; `importe Silver entregado = importe Gold`.

**3. Detener o rechazar: la diferencia que importa.**

| Situación | Acción | Por qué |
|---|---|---|
| falta la columna `precio` en todo el archivo | **detener** | seguir sería procesar basura |
| el archivo cambió de separador | **detener** | todas las filas serían ilegibles |
| una fila con cantidad `1.5` | **rechazar** esa fila | el resto del archivo es válido |
| `id_venta` repetido con montos distintos | **detener** (o enviar a revisión) | no sabes cuál es el correcto |
| el estado `Entregado` | **normalizar** a `entregado` | la regla de normalización lo permite |
| el estado `pendiente` | **rechazar** | no está entre los permitidos |

**4. Probar el contrato con tres filas a mano.** Aplica el contrato a las tres filas del ejemplo, sin código:

| Fila | Resultado | Motivo |
|---|---|---|
| V-001 | válida | fecha DD/MM, precio `Bs 6,00` → 6.00, estado correcto |
| V-002 | válida | fecha ISO admitida, estado se normaliza |
| V-003 | **rechazada** | kiosco ausente **y** cantidad `1.5` no entera (dos motivos) |

Si puedes completar esta tabla sin dudas, el contrato está listo. Si dudas en una fila, la duda es una **pregunta para el dueño del dato** y debe resolverse antes de programar. La fila V-003 tiene **dos** motivos: el contrato debe prever que una fila acumule varias causas.

**5. El contrato como código.** Ya con el contrato claro, las reglas se traducen casi uno a uno:

```python
import re

ESTADOS_PERMITIDOS = {"entregado", "anulado"}


def normalizar_estado(texto):
    return texto.strip().lower()


def convertir_precio(texto):
    """Admite 'Bs 6,00', '6.5', ' 9 '. Devuelve float o None si no es válido."""
    limpio = texto.replace("Bs", "").strip().replace(",", ".")
    try:
        valor = float(limpio)
    except ValueError:
        return None
    return valor if valor > 0 else None


def convertir_cantidad(texto):
    """Solo enteros positivos. '1.5' no se trunca: se rechaza."""
    limpio = texto.strip()
    if not re.fullmatch(r"\d+", limpio):
        return None
    valor = int(limpio)
    return valor if valor > 0 else None


print(normalizar_estado("Entregado "), convertir_precio("Bs 6,00"), convertir_precio("abc"))
print(convertir_cantidad("10"), convertir_cantidad("1.5"), convertir_cantidad("-2"))
```

```salida
entregado 6.0 None
10 None None
```

`re.fullmatch(r"\d+", limpio)` comprueba que el texto esté formado **solo por dígitos** (una expresión regular); así `"1.5"` y `"-2"` quedan fuera. Cada función implementa **una** regla del contrato y devuelve `None` cuando el dato es inválido (en lugar de inventar un valor). Observa que `convertir_cantidad("1.5")` da `None`: truncarla a 1 cambiaría el monto silenciosamente.

**6. Documentar los supuestos.** Algunas decisiones son supuestos válidos solo en cierto contexto. Ejemplo: «si falta el vendedor de una venta, se recupera por la ruta del cliente». Esa regla solo es correcta **si cada ruta tiene un solo vendedor**. Si dos vendedores se turnan en una ruta, o la asignación cambia con el tiempo, la recuperación inventaría un dato. Por eso el supuesto se escribe en el contrato, con su condición, y se comprueba cada vez («¿sigue habiendo un vendedor por ruta?»). Normalizar nombres tampoco reemplaza a un identificador estable.

**7. El contrato también lleva su versión y su dueño.** Un contrato cambia (llega una columna nueva). Anota la fecha, quién lo definió y qué cambió. Así, cuando mañana el archivo falle, sabes si el problema es el archivo o el contrato.

Ejemplo comercial: la regla «una cantidad de 1.5 es inválida cuando el contrato exige unidades enteras; truncarla cambia el monto» parece menor, pero es lo que evita que el total no cuadre con el ERP.

## Errores comunes

- **Programar sin contrato.**
- **Reglas en la cabeza** de quien programó, no escritas.
- **Confundir detener con rechazar.**
- **Truncar o redondear en silencio** un valor para que «pase».
- **Convertir lo desconocido en conocido** (un estado nuevo en uno válido).
- **No prever varios motivos** por fila.
- **Supuestos sin condición ni comprobación** («cada ruta tiene un vendedor»).
- **No versionar el contrato.**

## Para comprobar que entendiste

1. ¿Qué campos mínimos describe un contrato de datos?
2. ¿Cuándo se detiene el proceso y cuándo solo se rechaza una fila?
3. ¿Por qué no se trunca una cantidad `1.5`?
4. ¿Qué debe acompañar a un supuesto como «una ruta, un vendedor»?

<details><summary>Respuestas</summary>

1. Qué es una fila, columnas con tipo y obligatoriedad, clave única, formatos admitidos, valores permitidos, qué hacer con lo inválido y los cuadres.
2. Se detiene ante errores de estructura (falta de columnas, claves en conflicto); se rechaza la fila ante errores de fila.
3. Porque cambia el monto sin que nadie lo sepa.
4. Su condición de validez y una comprobación periódica.

</details>

## Micropráctica

Recibes un archivo de pedidos con las columnas `pedido`, `cliente`, `fecha`, `monto`.

1. Escribe su contrato en una tabla (campo, tipo, obligatorio, formato, si no cumple).
2. Define dos reglas de detención y tres de rechazo.
3. Aplica tu contrato, a mano, a estas tres filas y escribe el resultado de cada una: `P1;Luna;15/09/2026;120,50`, `P2;;2026-09-16;80`, `P3;Faro;31/02/2026;45`.
4. Escribe una función `convertir_monto(texto)` que implemente tu regla de monto y pruébala con `assert`.

Cómo saber que está bien: P2 y P3 se rechazan (cliente ausente; fecha inexistente) y P1 es válida.

<details><summary>Ejemplo de resolución de la parte 4</summary>

```python
def convertir_monto(texto):
    limpio = texto.strip().replace(",", ".")
    try:
        valor = float(limpio)
    except ValueError:
        return None
    return valor if valor > 0 else None


assert convertir_monto("120,50") == 120.5
assert convertir_monto("80") == 80
assert convertir_monto("abc") is None
assert convertir_monto("-5") is None
print("ok")
```

```salida
ok
```

</details>

## Después, en los ejercicios

Cada ejercicio de [Puente](../../03_EJERCICIOS/Puente/) y del proyecto ETL trae su propio diccionario de datos: léelo como un contrato y complétalo con las reglas de rechazo antes de programar. Siguiente: [5.3 Rechazos, duplicados y reconciliación](03_rechazos_y_reconciliacion.md).
