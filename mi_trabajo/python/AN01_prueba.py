import mis_funciones as mf

codigos = ["C12", "C07", "C12", "C30", "C07", "C12", "C18", "C07", "C30", "C12"]
print(mf.clientes_unicos(codigos))

conteo = {}

for cliente in codigos:
    conteo[cliente] = conteo.get(cliente, 0) + 1

print(conteo)