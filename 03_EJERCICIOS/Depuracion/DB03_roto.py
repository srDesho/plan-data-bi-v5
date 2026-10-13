"""DB03 · Este script NO falla, pero el total de ventas sube. Cópialo a mi_trabajo/depuracion/DB03.py."""
import pandas as pd


def ventas_con_categoria(ventas, catalogo):
    """Devuelve las ventas con su categoría. No debe cambiar el número de filas ni el total."""
    return ventas.merge(catalogo, on="producto", how="left")


if __name__ == "__main__":
    ventas = pd.DataFrame({"ticket": [1, 2, 3], "producto": ["P-01", "P-02", "P-01"], "monto": [100, 50, 80]})
    catalogo = pd.DataFrame({"producto": ["P-01", "P-02", "P-01"], "categoria": ["Abarrotes", "Snacks", "Abarrotes"]})
    unido = ventas_con_categoria(ventas, catalogo)
    print("Filas:", len(ventas), "->", len(unido))
    print("Total:", ventas["monto"].sum(), "->", unido["monto"].sum())
