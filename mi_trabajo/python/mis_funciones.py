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

def cliente_diccionario(codigo, ruta):
    return {"cliente_id" : codigo, "ruta" : ruta}

def clientes_unicos(codigos):
    return sorted(set(codigos))

def contar_estados(lista_tipo):
    cantitades = {}
    for tipo in lista_tipo:
        if (tipo in cantitades):
            cantitades[tipo] += 1
        else:
            cantitades[tipo] = 1
    return cantitades
