"""Referencia de DB01–DB03. Abrir solo después de tu intento."""
import pandas as pd


def ventas_por_tienda(filas):
    totales = {}
    for fila in filas:
        tienda = fila["tienda"]                                   # DB01: la clave era "tiendas"
        totales[tienda] = totales.get(tienda, 0) + fila["monto"]
    return totales


def unidades_validas(textos):
    resultado = []
    for t in textos:
        x = float(t)                                              # DB02: int(float(t)) truncaba 2.5 a 2 en silencio
        if x != int(x):
            raise ValueError(f"cantidad no entera: {t!r}")
        resultado.append(int(x))
    return resultado


def ventas_con_categoria(ventas, catalogo):
    # DB03: validate falla si el catálogo repite un producto; sin él, el merge duplica filas y suma de más.
    return ventas.merge(catalogo, on="producto", how="left", validate="many_to_one")
