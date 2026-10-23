"""Referencia de PT01: pruebas de clasificar_ticket (P08). Ábrela solo después de tu intento."""
from mis_funciones import clasificar_ticket

# caso normal en cada etiqueta
assert clasificar_ticket(50) == "Pequeño"
assert clasificar_ticket(400) == "Mediano"
assert clasificar_ticket(900) == "Grande"
# límites: 200 y 600 son Mediano; justo por debajo y por encima cambian de etiqueta
assert clasificar_ticket(200) == "Mediano"
assert clasificar_ticket(199.99) == "Pequeño"
assert clasificar_ticket(600) == "Mediano"
assert clasificar_ticket(600.01) == "Grande"
# dato ausente: no se clasifica en silencio
try:
    clasificar_ticket(None)
    assert False, "clasificar_ticket(None) debía fallar"
except TypeError:
    pass
