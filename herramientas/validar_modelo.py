"""Validador estructural de los diseños de modelo estrella (MD01 y RM01).

Uso:
    python herramientas/validar_modelo.py MD01 mi_trabajo/modelo/MD01.md
    python herramientas/validar_modelo.py RM01 mi_trabajo/modelo/RM01.md

Comprueba la estructura de tu documento, no la calidad de tu razonamiento (eso lo revisas con la rúbrica del enunciado):
  - una sección «Grano» que diga qué representa una fila de la tabla de hechos;
  - una sección «Hecho» con una tabla cuyas filas indican el rol de cada columna: claves foráneas y medidas;
  - una sección «Dimensiones» con al menos dos tablas `dim_*` y su clave;
  - una sección «Dimensiones conformadas» que nombre las dimensiones compartidas con ventas;
  - una sección «Controles de calidad» con al menos cinco controles;
  - ninguna relación directa hecho–hecho (las tablas de hechos se relacionan solo a través de dimensiones compartidas).
"""
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):  # una consola Windows cp1252 no debe romper el mensaje
    sys.stdout.reconfigure(errors="replace")

EXIGE = {
    "MD01": {"hecho": "fact_", "dimensiones": ["dim_producto"], "conformadas": ["dim_producto"]},
    "RM01": {"hecho": "fact_visitas", "dimensiones": ["dim_cliente", "dim_fecha"], "conformadas": ["dim_cliente", "dim_fecha"]},
}
SEPARADORES_RELACION = ("→", "->", "↔", "<->", "⟷", " join ", "foreign key")


def secciones(texto):
    """Devuelve {título en minúsculas: contenido} para los encabezados `##` y `###`."""
    partes, actual = {}, None
    for linea in texto.splitlines():
        m = re.match(r"^#{2,3}\s+(.*?)\s*$", linea)
        if m:
            actual = m.group(1).lower()
            partes[actual] = ""
        elif actual is not None:
            partes[actual] += linea + "\n"
    return partes


def buscar(partes, *claves):
    for titulo, cuerpo in partes.items():
        if all(c in titulo for c in claves):
            return titulo, cuerpo
    return None, None


def validar(id_, texto):
    if id_ not in EXIGE:
        raise SystemExit(f"{id_}: ejercicio desconocido (usa MD01 o RM01).")
    regla = EXIGE[id_]
    partes = secciones(texto)
    hallazgos = []

    def ok(condicion, mensaje):
        hallazgos.append((bool(condicion), mensaje))

    t, grano = buscar(partes, "grano")
    ok(grano and re.search(r"una fila", grano, re.I), "Sección «Grano» que empiece diciendo qué representa una fila («Una fila de fact_… representa …»).")

    t, hecho = buscar(partes, "hecho")
    filas = [l for l in (hecho or "").splitlines() if l.strip().startswith("|") and not re.match(r"^\|\s*:?-", l.strip())]
    celdas = [[c.strip() for c in l.strip().strip("|").split("|")] for l in filas[1:]]
    claves = [c for c in celdas if any(re.search(r"clave|fk|for[aá]nea", x, re.I) for x in c[1:])]
    medidas = [c for c in celdas if any(re.search(r"medida", x, re.I) for x in c[1:])]
    ok(len(claves) >= 2, f"La tabla de «Hecho» debe tener al menos 2 claves foráneas (hay {len(claves)}); indica el rol en una columna: «clave foránea» o «medida».")
    ok(len(medidas) >= 1, "La tabla de «Hecho» debe tener al menos una medida.")
    nombres_hecho = set(re.findall(r"fact_\w+", texto))
    ok(any(n.startswith(regla["hecho"]) for n in nombres_hecho) if regla["hecho"].endswith("_") else regla["hecho"] in nombres_hecho,
       f"Nombra la tabla de hechos ({'fact_…' if regla['hecho'].endswith('_') else regla['hecho']}).")

    t, dims = buscar(partes, "dimensiones")
    dims_texto = "\n".join(c for titulo, c in partes.items() if "dimension" in titulo or titulo.startswith("dim_"))
    nombres_dim = set(re.findall(r"dim_\w+", dims_texto))
    ok(len(nombres_dim) >= 2, f"La sección «Dimensiones» debe nombrar al menos 2 tablas dim_* (hay {len(nombres_dim)}).")
    for d in regla["dimensiones"]:
        ok(d in nombres_dim or d in texto, f"Incluye la dimensión {d}.")
    ok(re.search(r"clave", dims_texto, re.I), "Indica la clave de cada dimensión.")

    t, conf = buscar(partes, "conformad")
    ok(conf and all(d in conf for d in regla["conformadas"]), f"La sección «Dimensiones conformadas» debe nombrar {', '.join(regla['conformadas'])} como compartidas con ventas.")

    t, ctrl = buscar(partes, "control")
    items = re.findall(r"^\s*(?:\d+[.)]|[-*])\s+\S", ctrl or "", re.M)
    ok(len(items) >= 5, f"La sección «Controles de calidad» debe tener al menos 5 controles (hay {len(items)}).")

    problemas = []
    for linea in texto.splitlines():
        hechos = set(re.findall(r"fact_\w+", linea))
        if len(hechos) >= 2 and any(s in linea.lower() for s in SEPARADORES_RELACION):
            problemas.append(linea.strip()[:90])
    ok(not problemas, "No relaciones una tabla de hechos con otra directamente; conéctalas solo por dimensiones conformadas" + (f" (revisa: «{problemas[0]}»)" if problemas else "") + ".")
    return hallazgos


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    id_, archivo = sys.argv[1].upper(), Path(sys.argv[2])
    if not archivo.exists():
        print(f"REVISAR {id_}: no existe {archivo}. Crea el documento con las secciones indicadas en el enunciado.")
        raise SystemExit(1)
    hallazgos = validar(id_, archivo.read_text(encoding="utf-8-sig"))
    for bien, mensaje in hallazgos:
        print(("OK       " if bien else "REVISAR  ") + mensaje)
    fallos = sum(1 for b, _ in hallazgos if not b)
    print(f"\n{id_}: {len(hallazgos) - fallos}/{len(hallazgos)} comprobaciones estructurales correctas." + (" Corrige lo marcado como REVISAR." if fallos else " Ahora revisa el diseño con la rúbrica del enunciado."))
    raise SystemExit(1 if fallos else 0)


if __name__ == "__main__":
    main()
