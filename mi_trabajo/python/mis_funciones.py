def importe(precio, cantidad):
    return precio * cantidad

print(importe(150, 2))

def porcentaje(real, meta):
    if (meta <= 0):
        return None
    result = 100 * real / meta
    if (result <= 0):
        return  None
    else:
        return result

def normalizar_nombre(texto):
     partes = texto.split()
     result = " ".join(partes).title()
     return result