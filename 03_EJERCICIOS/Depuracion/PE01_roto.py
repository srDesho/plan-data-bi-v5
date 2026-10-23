"""PE01 (roto). Resume las ventas por categoría y por zona.

Termina sin error, pero dos totales no cuadran con el total de ventas. No lo arregles a ojo:
cuenta filas y suma montos antes y después de cada paso.
"""
from pathlib import Path

import pandas as pd


def resumen(ventas, catalogo, clientes):
    """Devuelve (por_categoria, por_zona): dos diccionarios {grupo: total de monto}."""
    con_categoria = ventas.merge(catalogo, on="producto", how="left")
    por_categoria = con_categoria.groupby("categoria")["monto"].sum()
    con_zona = ventas.merge(clientes, on="cliente", how="left")
    por_zona = con_zona.groupby("zona")["monto"].sum()
    return dict(por_categoria), dict(por_zona)


if __name__ == "__main__":
    carpeta = Path(__file__).resolve().parents[2] / "03_EJERCICIOS" / "Depuracion"
    ventas = pd.read_csv(carpeta / "PE01_ventas.csv")
    catalogo = pd.DataFrame({"producto": ["P-01", "P-02", "P-02", "P-03"],
                             "categoria": ["Abarrotes", "Bebidas", "Bebidas", "Snacks"]})
    clientes = pd.DataFrame({"cliente": [1, 2, 3, 4], "zona": ["Norte", "Sur", None, "Norte"]})
    por_categoria, por_zona = resumen(ventas, catalogo, clientes)
    print("Ventas totales:", ventas["monto"].sum())
    print("Por categoría:", por_categoria, "suma =", sum(por_categoria.values()))
    print("Por zona:", por_zona, "suma =", sum(por_zona.values()))
