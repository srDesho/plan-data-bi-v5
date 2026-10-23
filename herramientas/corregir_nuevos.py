"""Corrector de los ejercicios nuevos del plan v6.

Uso:
    python herramientas/corregir_nuevos.py SQ01 mi_trabajo/sql/SQ01.sql
    python herramientas/corregir_nuevos.py RP01 mi_trabajo/python/mis_funciones.py

SQL: compara columnas y filas con los controles de `08_SOLUCIONES/controles_sql_v6.json` (no muestra la consulta de referencia).
Python/Pandas: ejecuta los casos de `contratos_v6.py`. Los ejercicios de estadística, Excel, Power Query, Power BI y modelado se comprueban con la rúbrica y los
controles de su enunciado. No modifica los correctores existentes.
"""
from pathlib import Path
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, "reconfigure"):  # una consola Windows cp1252 no debe romper el mensaje del corrector
    sys.stdout.reconfigure(errors="replace")


def sql(id_, archivo):
    from corregir_sql import consulta, normalizar
    esperado = json.loads((ROOT / "08_SOLUCIONES" / "controles_sql_v6.json").read_text(encoding="utf-8"))
    if id_ not in esperado:
        raise KeyError(f"{id_}: sin controles SQL en controles_sql_v6.json")
    total = 0
    texto = Path(archivo).read_text(encoding="utf-8-sig")
    partes = [p for p in esperado[id_]["apartados"]]
    # una consulta por apartado, separadas por punto y coma, en el orden del enunciado
    bloques = [b.strip() for b in texto.split(";") if b.strip() and not all(l.strip().startswith("--") or not l.strip() for l in b.strip().splitlines())]
    necesarias = max((k + 1 for k, ap in enumerate(partes) if not ap.get("rubrica")), default=0)
    if len(bloques) < necesarias:
        raise AssertionError(f"Se esperaban {necesarias} consultas (una por apartado, terminadas en ;) y hay {len(bloques)}")
    for k, ap in enumerate(partes):
        if ap.get("rubrica"):
            continue
        cols, rows = consulta(bloques[k] + ";")
        assert len(cols) == len(ap["columnas"]), f"Apartado {ap['id']}: cantidad u orden de columnas distinto del contrato"
        assert normalizar(rows) == normalizar([tuple(f) for f in ap["filas"]]), f"Apartado {ap['id']}: resultado diferente ({len(rows)} filas; se esperaban {len(ap['filas'])})"
        for palabra in ap.get("requiere_texto", []):
            assert palabra.upper() in bloques[k].upper(), f"Apartado {ap['id']}: el enunciado pide usar {palabra} y tu consulta no lo usa"
        aum = ap.get("aumentado")
        if aum:  # misma consulta sobre una copia en memoria con filas de prueba añadidas (comercial.db no se modifica)
            cols2, rows2 = consulta_aumentada(bloques[k] + ";", aum["preparacion"])
            assert normalizar(rows2) == normalizar([tuple(f) for f in aum["filas"]]), (
                f"Apartado {ap['id']}: tu consulta da el resultado correcto con los datos del curso, pero falla con datos de prueba adicionales "
                f"({len(rows2)} filas; se esperaban {len(aum['filas'])}). Piensa qué casos de los datos reales no cubre tu condición.")
        total += 1
    return total


def consulta_aumentada(texto, preparacion):
    """Ejecuta `texto` sobre una copia en memoria de comercial.db a la que se aplica `preparacion` (INSERT de prueba). No toca el archivo."""
    import sqlite3
    from contextlib import closing
    with closing(sqlite3.connect((ROOT / "04_DATASETS" / "comercial.db").as_uri() + "?mode=ro", uri=True)) as origen, closing(sqlite3.connect(":memory:")) as copia:
        origen.backup(copia)
        copia.executescript(preparacion)
        cur = copia.execute(texto.strip().rstrip(";"))
        return [d[0] for d in cur.description], cur.fetchall()


def python(id_, archivo):
    from contratos_v6 import comprobar, comprobar_pruebas
    if id_ == "PT01":  # el estudiante entrega pruebas, no una función: se ejecutan contra la versión correcta y contra versiones defectuosas
        return comprobar_pruebas(id_, archivo)
    spec = importlib.util.spec_from_file_location("funciones_estudiante", Path(archivo).resolve())
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return comprobar(id_, modulo)


def rel1(archivo):
    """REL1: tu mini-ETL de ME04 con una regla más (monto > Bs 5.000 se rechaza por «monto»), sin romper la ecuación de conteos."""
    import tempfile
    import corregir_mini_etl as me
    modulo = me.cargar(archivo)
    ejecutar = me.funcion(modulo, "ejecutar")
    n = 0
    with tempfile.TemporaryDirectory(prefix="rel1_", ignore_cleanup_errors=True) as td:
        entrada = me.entrada_v(2, td)
        raw = entrada / "ventas_mini_raw.csv"
        texto = raw.read_text(encoding="utf-8")
        texto += ("" if texto.endswith("\n") else "\n") + "T027;2026-10-13;Tienda Sol;P-01;480;entregado;Bs 10,50\nT028;2026-10-13;Tienda Sol;P-01;480;entregado;Bs 10,00\n"
        raw.write_text(texto, encoding="utf-8")
        met = ejecutar(entrada, Path(td) / "salida")
        base = me.CONTROL["v2"]["metricas"]
        esperado = {"bronze": base["bronze"] + 2, "duplicados_exactos": base["duplicados_exactos"], "rechazados": base["rechazados"] + 1,
                    "silver": base["silver"] + 1, "ventas_centavos": base["ventas_centavos"] + 480 * 1000}
        for k, v in esperado.items():
            me.exigir(met.get(k) == v, f'metricas["{k}"] = {met.get(k)!r}; se esperaba {v!r} (T027 = Bs 5.040 se rechaza por «monto»; T028 = Bs 4.800 pasa).')
            n += 1
        me.exigir(met["bronze"] == met["duplicados_exactos"] + met["rechazados"] + met["silver"], "La ecuación bronze = duplicados + rechazados + silver no se cumple con la regla nueva.")
        rech = {str(r.ticket_id): str(r.motivos).lower() for r in me.leer_tabla(Path(td) / "salida" / "mini.db", "rechazos").itertuples()}
        me.exigir("T027" in rech and "monto" in rech["T027"], f'T027 debía rechazarse con una causa que mencione "monto"; obtuviste {rech.get("T027")!r}.')
        me.exigir("T028" not in rech, "T028 (Bs 4.800) no supera el límite y no debe rechazarse.")
        me.exigir("unidades" in rech.get("T024", ""), "T024 (900 unidades) debe seguir rechazándose por «unidades» (regla de ME04).")
        met1 = ejecutar(me.DATOS, Path(td) / "salida1")
        me.exigir(met1 == me.CONTROL["v1"]["metricas"], "La regla nueva cambió el resultado con el raw original: ME03 dejó de cumplirse.")
        n += 4
    return n


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    id_, archivo = sys.argv[1], sys.argv[2]
    try:
        if id_.startswith(("SQ", "KP")):
            n = sql(id_, archivo)
            print(f"OK {id_}: {n} apartados correctos. Explica el filtro, la granularidad y qué no puedes concluir.")
        elif id_ == "REL1":
            n = rel1(archivo)
            print(f"OK {id_}: {n} comprobaciones. Explica qué línea tocaste y por qué no cambió el raw original.")
        else:
            n = python(id_, archivo)
            print(f"OK {id_}: {n} casos aprobados. Explica tu razonamiento y prueba una entrada nueva.")
    except Exception as e:
        print(f"REVISAR {id_}: {type(e).__name__}: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
