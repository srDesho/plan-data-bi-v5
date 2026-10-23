"""PE01 corregido. Ábrelo solo después de tu intento.

Causa 1: el catálogo repite P-02, así que el merge multiplica sus ventas (una fila de venta pasa a ser dos).
         `validate="many_to_one"` detiene el proceso en lugar de inflar el total.
Causa 2: el cliente 3 no tiene zona; `groupby` descarta los grupos vacíos por defecto, y esas ventas desaparecen del total por zona.
         `dropna=False` las conserva en un grupo propio.
Controles: cada total agrupado debe sumar el total de ventas.
"""
from pathlib import Path

import pandas as pd


def resumen(ventas, catalogo, clientes):
    """Devuelve (por_categoria, por_zona): dos diccionarios {grupo: total de monto}."""
    total = ventas["monto"].sum()
    con_categoria = ventas.merge(catalogo, on="producto", how="left", validate="many_to_one")
    por_categoria = con_categoria.groupby("categoria", dropna=False)["monto"].sum()
    con_zona = ventas.merge(clientes, on="cliente", how="left", validate="many_to_one")
    por_zona = con_zona.groupby("zona", dropna=False)["monto"].sum()
    assert por_categoria.sum() == total, f"Control: las categorías suman {por_categoria.sum()} y las ventas son {total}"
    assert por_zona.sum() == total, f"Control: las zonas suman {por_zona.sum()} y las ventas son {total}"
    return dict(por_categoria), dict(por_zona)


if __name__ == "__main__":
    carpeta = Path(__file__).resolve().parents[1] / "03_EJERCICIOS" / "Depuracion"
    ventas = pd.read_csv(carpeta / "PE01_ventas.csv")
    catalogo = pd.DataFrame({"producto": ["P-01", "P-02", "P-03"], "categoria": ["Abarrotes", "Bebidas", "Snacks"]})
    clientes = pd.DataFrame({"cliente": [1, 2, 3, 4], "zona": ["Norte", "Sur", None, "Norte"]})
    print(resumen(ventas, catalogo, clientes))
