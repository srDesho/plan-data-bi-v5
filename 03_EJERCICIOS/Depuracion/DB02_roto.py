"""DB02 · Este script NO falla, pero el total de unidades está mal. Cópialo a mi_trabajo/depuracion/DB02.py."""


def unidades_validas(textos):
    """Convierte textos a enteros. Una cantidad como "3.7" no es un entero: debe lanzar ValueError."""
    return [int(float(t)) for t in textos]


if __name__ == "__main__":
    entradas = ["3", "4.0", "2.5", "10"]
    cantidades = unidades_validas(entradas)
    print("Cantidades:", cantidades, "· total:", sum(cantidades))
    print("Total que calculas a mano con 3 + 4 + 2.5 + 10 =", 3 + 4 + 2.5 + 10)
