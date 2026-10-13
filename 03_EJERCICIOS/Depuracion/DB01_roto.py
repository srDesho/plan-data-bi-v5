"""DB01 · Este script falla. Cópialo a mi_trabajo/depuracion/DB01.py, ejecútalo y lee el traceback."""


def ventas_por_tienda(filas):
    """filas: lista de diccionarios con 'tienda' y 'monto'. Devuelve {tienda: total}."""
    totales = {}
    for fila in filas:
        tienda = fila["tiendas"]
        totales[tienda] = totales.get(tienda, 0) + fila["monto"]
    return totales


if __name__ == "__main__":
    datos = [{"tienda": "Sol", "monto": 30}, {"tienda": "Luna", "monto": 20}, {"tienda": "Sol", "monto": 5}]
    print(ventas_por_tienda(datos))
