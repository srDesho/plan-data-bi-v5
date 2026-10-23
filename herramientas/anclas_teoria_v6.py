#!/usr/bin/env python
"""Añade (de forma idempotente) las anclas que usan las guías: `micropractica` en toda lección con micropráctica y `seccion-inicial` en 14.5.

    .venv\\Scripts\\python.exe herramientas/anclas_teoria_v6.py            # escribe
    .venv\\Scripts\\python.exe herramientas/anclas_teoria_v6.py --comprobar # solo informa
"""
import re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
NOTA_145 = ('<a id="seccion-inicial"></a>\n> **Sección inicial (plan v6, D33):** lee primero los pasos 1, 2 y 6 de «Ejemplo paso a paso» '
            '(estructura de la página, reglas de diseño y cómo comunicar el tablero): son 12 de los 25 min de lectura y lo único que necesita PB07. '
            'El resto de la lección es complementario.\n')


def main():
    solo = "--comprobar" in sys.argv
    cambios = []
    for f in sorted((RAIZ / "02_TEORIA").rglob("*.md")):
        raw = f.read_bytes().decode("utf-8-sig")
        crlf = "\r\n" in raw
        t = raw.replace("\r\n", "\n")
        nuevo = t
        if re.search(r"^## Micropr[aá]ctica\s*$", nuevo, re.M) and '<a id="micropractica"></a>' not in nuevo:
            nuevo = re.sub(r"^(## Micropr[aá]ctica\s*)$", '<a id="micropractica"></a>\n\n\\1', nuevo, count=1, flags=re.M)
        if f.name == "05_diseno_y_comprobacion.md" and 'id="seccion-inicial"' not in nuevo:
            nuevo = nuevo.replace("## Para qué sirve", NOTA_145 + "\n## Para qué sirve", 1)
        if nuevo != t:
            cambios.append(f.relative_to(RAIZ).as_posix())
            if not solo:
                f.write_bytes((nuevo.replace("\n", "\r\n") if crlf else nuevo).encode("utf-8"))
    print(("Por modificar" if solo else "Modificados") + f": {len(cambios)}")
    for c in cambios:
        print("  ", c)


if __name__ == "__main__":
    main()
