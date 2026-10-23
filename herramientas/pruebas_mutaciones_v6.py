"""Pruebas de mutación del plan v6 (solo lectura sobre los archivos del paquete).

Cada «mutante» es una versión deliberadamente defectuosa de una solución de referencia (o de una guía generada); los correctores y el verificador DEBEN rechazarlo.
Un mutante aceptado indebidamente es un fallo de la prueba. Las variantes que son soluciones válidas distintas se marcan «aceptar» y deben pasar.

Uso (desde la raíz, con el Python del .venv):
    python herramientas/pruebas_mutaciones_v6.py ejercicios   # correctores de los ejercicios nuevos
    python herramientas/pruebas_mutaciones_v6.py guias        # verificador de guías (modifica una guía y la restaura byte a byte)
    python herramientas/pruebas_mutaciones_v6.py todo
Código de salida 1 si algún mutante supera las pruebas previstas.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
REPO = str(Path(__file__).resolve().parents[1])
PY = sys.executable
NUEVOS = os.path.join(REPO, "herramientas", "corregir_nuevos.py")
VER = os.path.join(REPO, "herramientas", "verificar_diseno_v6.py")


def correr(id_, ruta):
    return subprocess.run([PY, "-B", NUEVOS, id_, ruta], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO)


def probar(id_, ref_rel, mutantes, entrega_ext=None):
    """Mutantes (descripción, texto viejo, texto nuevo) sobre una referencia; todos deben ser rechazados. Devuelve cuántos se aceptaron."""
    ref = open(os.path.join(REPO, ref_rel), encoding="utf-8").read()
    malos = 0
    for desc, viejo, nuevo in mutantes:
        assert ref.count(viejo) >= 1, f"{id_}: no hay «{viejo}» en la referencia ({desc})"
        marca = f"# {id_}"
        pos = ref.index(marca) if marca in ref else 0
        i = ref.index(viejo, pos)
        m = ref[:i] + nuevo + ref[i + len(viejo):]
        d = tempfile.mkdtemp()
        ruta = os.path.join(d, "m" + (entrega_ext or os.path.splitext(ref_rel)[1]))
        open(ruta, "w", encoding="utf-8").write(m)
        r = correr(id_, ruta)
        rechazado = r.returncode != 0
        print(("RECHAZADO " if rechazado else "¡ACEPTADO! "), id_, desc, "|", (r.stdout.strip() or r.stderr.strip())[:100].replace("\n", " "))
        malos += 0 if rechazado else 1
    return malos


SQL_MUTANTES = {
    "SQ01": [("OR sin paréntesis", "(tipo='Farmacia' OR tipo='Kiosco') AND", "tipo='Farmacia' OR tipo='Kiosco' AND")],
    "SQ02": [("pierde los NULL", "zona IS NULL OR ", "")],
    "SQ03": [("umbral distinto", ">=4500", ">=4000")],
    "SQ04": [("mes distinto", "='2026-09'", "='2026-08'"), ("sin filtrar estado", "p.estado='entregado' AND", "")],
    "SQ05": [("umbral distinto", ">4.5", ">4.0")],
    "SQ06": [("cuenta ítems, no pedidos", "COUNT(DISTINCT p.pedido_id)", "COUNT(*)")],
    "SQ07": [("condición en WHERE", "AND v.realizada=1 WHERE v.visita_id IS NULL", "WHERE v.visita_id IS NULL AND v.realizada=1")],
    # SQ09 c: SQLite devuelve NULL al dividir entre 0, así que NULLIF no cambia el resultado; el corrector exige su uso por texto.
    "SQ09": [("COALESCE sin etiqueta", "COALESCE(zona,'Sin zona')", "zona"), ("divisor sin NULLIF", "NULLIF(SUM(realizada),0)", "SUM(realizada)")],
    "SQ10": [("promedio fijo", ">(SELECT AVG(precio_unitario) FROM productos)", ">20"), ("promedio equivocado", "HAVING COUNT(*)>(SELECT AVG(n)", "HAVING COUNT(*)>(SELECT MAX(n)/2")],
    "SQ11": [("une solo por ruta", "AND pr.mes=v.mes", "")],
    "SQ12": [("tres por categoría", "pos<=2", "pos<=3"), ("sin partición", "PARTITION BY categoria ", "")],
    # SQ13 a: con los datos reales todos los nombres con espacio los tienen al inicio; el corrector añade filas de prueba en memoria (espacio final / espacio inicial).
    "SQ13": [("zonas con dato", "WHERE zona IS NULL GROUP", "WHERE zona IS NOT NULL GROUP"), ("LTRIM en lugar de TRIM", "<>TRIM(nombre_negocio)", "<>LTRIM(nombre_negocio)"), ("RTRIM en lugar de TRIM", "<>TRIM(nombre_negocio)", "<>RTRIM(nombre_negocio)")],
    "KP01": [("días del mes en lugar de días con ventas", "COUNT(DISTINCT p.fecha)", "COUNT(*)"), ("sin guarda de base 0", "WHEN base=0 THEN 'n/c'", "WHEN base=-1 THEN 'n/c'"), ("mes equivocado", "'2026-08'", "'2026-07'")],
    "SQ14": [("estado inexistente", "estado='anulado'", "estado='cancelado'")],
    "SQ15": [("acumulado sin orden", "OVER (ORDER BY mes)", "OVER ()")],
    "SQ16": [("umbral A distinto", "<80", "<70")],
    "SQ17": [("cuenta ítems, no pedidos", "COUNT(DISTINCT p.pedido_id)", "COUNT(*)")],
}


def sql():
    malos = 0
    for id_, lista in SQL_MUTANTES.items():
        ref = open(os.path.join(REPO, "08_SOLUCIONES", "sql", f"{id_}.sql"), encoding="utf-8").read()
        r = correr(id_, os.path.join(REPO, "08_SOLUCIONES", "sql", f"{id_}.sql"))
        assert r.returncode == 0, f"{id_}: la referencia debe aprobar: {r.stdout}"
        for desc, viejo, nuevo in lista:
            assert viejo in ref, (id_, desc)
            d = tempfile.mkdtemp()
            ruta = os.path.join(d, f"{id_}.sql")
            open(ruta, "w", encoding="utf-8").write(ref.replace(viejo, nuevo))
            r = correr(id_, ruta)
            print(("RECHAZADO " if r.returncode else "¡ACEPTADO! "), id_, desc, "|", (r.stdout.strip() or r.stderr.strip())[:90])
            malos += 0 if r.returncode else 1
    return malos


def py_b2():
    PYREF = "08_SOLUCIONES/python_referencia_v6.py"
    total = 0
    total += probar("RP05", PYREF, [
        ("sin ignorar líneas vacías", "if not fila:\n                continue", "pass"),
        ("negativo permitido", "if any(x < 0 for x in numeros):", "if False:"),
        ("vacío antes que columnas", "if len(fila) != len(cabecera):", "if len(fila) < 0:"),
        ("sin utf-8-sig", 'encoding="utf-8-sig"', 'encoding="utf-8"'),
        ("línea relativa", "linea = lector.line_num", "linea = len(validas) + len(rechazadas) + 1"),
        ("motivo distinto", '"campo vacío"', '"vacío"'),
        ("valores como texto", "validas.append(dict(zip(cabecera, numeros)))", "validas.append(dict(zip(cabecera, fila)))"),
    ])
    total += probar("RS01", PYREF, [
        ("sin redondeo", "round(100 * f / total, 1)", "100 * f / total"),
        ("sin desempate", "key=lambda t: (-t[1], t[0])", "key=lambda t: -t[1]"),
        ("orden ascendente", "key=lambda t: (-t[1], t[0])", "key=lambda t: (t[1], t[0])"),
        ("porcentaje sobre categorías", "round(100 * f / total, 1)", "round(100 * f / len(conteo), 1)"),
    ])
    return total


def py_b3():
    PYREF = "08_SOLUCIONES/python_referencia_v6.py"
    total = 0
    total += probar("PD01", PYREF, [
        ("sin filtrar estado", '(pedidos["estado"] == "entregado") & ', ""),
        ("sin filtrar ruta", 'pedidos["cliente_id"].isin(ids) & ', ""),
        ("mes por prefijo equivocado", ".startswith(mes)", ".startswith(mes[:4])"),
        ("sin desempate por pedido_id", 'sort_values(["fecha", "pedido_id"])', 'sort_values(["fecha"], kind="stable")'),
        ("índice sin reiniciar", ".reset_index(drop=True)", ""),
        ("columnas de más", 'columnas = ["pedido_id", "cliente_id", "fecha"]', 'columnas = ["pedido_id", "cliente_id", "fecha", "estado"]'),
        ("modifica la entrada", "mascara = (", "pedidos.sort_values('fecha', inplace=True, ascending=False); mascara = ("),
    ])
    total += probar("RD01", PYREF, [
        ("mayor o igual", 'inventario["salidas_unidades"] > inventario["stock_final"]', 'inventario["salidas_unidades"] >= inventario["stock_final"]'),
        ("diferencia invertida", 'd["salidas_unidades"] - d["stock_final"]', 'd["stock_final"] - d["salidas_unidades"]'),
        ("orden ascendente", "ascending=[False, True]", "ascending=[True, True]"),
        ("sin desempate", 'sort_values(["diferencia", "producto_id"], ascending=[False, True])', 'sort_values("diferencia", ascending=False, kind="stable")'),
        ("columnas distintas", '"salidas_unidades", "stock_final"]].copy()', '"stock_final", "salidas_unidades"]].copy()'),
    ])
    total += probar("RS02", PYREF, [
        ("desviación poblacional", "(n - 1)) ** 0.5", "n) ** 0.5"),
        ("mediana sin promedio", "(ordenados[mitad - 1] + ordenados[mitad]) / 2", "ordenados[mitad]"),
        ("cv en porcentaje", "round(cv, 3)", "round(cv * 100, 3)"),
        ("sin caso n<2", "if n < 2:", "if n < 0:"),
        ("media cero sin proteger", "None if media == 0 else desviacion / media", "desviacion / media"),
    ])

    REF = open(os.path.join(REPO, "08_SOLUCIONES", "pruebas_PT01_referencia.py"), encoding="utf-8").read()
    casos = {
        "sin límites": REF.replace("assert clasificar_ticket(200) == \"Mediano\"\n", "").replace("assert clasificar_ticket(600) == \"Mediano\"\n", ""),
        "sin dato ausente": REF.split("# dato ausente")[0],
        "solo un límite": REF.replace("assert clasificar_ticket(600) == \"Mediano\"\n", "").replace("assert clasificar_ticket(600.01) == \"Grande\"\n", ""),
        "esperado equivocado": REF.replace('assert clasificar_ticket(50) == "Pequeño"', 'assert clasificar_ticket(50) == "Mediano"'),
        "menos de 4 assert": "from mis_funciones import clasificar_ticket\nassert clasificar_ticket(50) == 'Pequeño'\nassert clasificar_ticket(200) == 'Mediano'\n",
    }
    for desc, texto in casos.items():
        d = tempfile.mkdtemp(); ruta = os.path.join(d, "pruebas_PT01.py"); open(ruta, "w", encoding="utf-8").write(texto)
        r = subprocess.run([PY, "-B", os.path.join(REPO, "herramientas", "corregir_nuevos.py"), "PT01", ruta], capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(("RECHAZADO " if r.returncode else "¡ACEPTADO! "), "PT01", desc, "|", (r.stdout.strip() or r.stderr.strip())[:110])
        total += 0 if r.returncode else 1
    return total


def py_b4():
    PYREF = "08_SOLUCIONES/python_referencia_v6.py"
    total = 0
    total += probar("RD02", PYREF, [
        ("modifica la entrada", "for fila in df.to_dict(\"records\"):", "df.loc[df.index[0], \"id\"] = -1\n    for fila in df.to_dict(\"records\"):"),
        ("acepta nan", "if not math.isfinite(monto) or monto < 0:", "if monto < 0:"),
        ("acepta negativos", "if not math.isfinite(monto) or monto < 0:", "if not math.isfinite(monto):"),
        ("no quita punto de miles", 'texto = texto.replace(".", "").replace(",", ".")', 'texto = texto.replace(",", ".")'),
        ("fecha DD/MM sin validar", "iso = datetime.strptime(fecha, formato).strftime(\"%Y-%m-%d\")", "iso = fecha"),
        ("acepta día de un dígito", r'r"\d{2}/\d{2}/\d{4}"', r'r"\d{1,2}/\d{1,2}/\d{4}"'),
        ("motivo único", '";".join(motivos)', "motivos[0]"),
        ("pierde texto original", '"fecha": fila["fecha"], "monto": fila["monto"], "motivo"', '"fecha": iso, "monto": monto, "motivo"'),
        ("rechaza monto cero", "monto < 0:", "monto <= 0:"),
    ])
    total += probar("RS03", PYREF, [
        ("percentil sin interpolar", "return ordenados[base] + resto * (ordenados[base + 1] - ordenados[base])", "return ordenados[base]"),
        ("cerca con 3 en lugar de 1,5", "q1 - 1.5 * iqr, q3 + 1.5 * iqr\n    return", "q1 - 3 * iqr, q3 + 3 * iqr\n    return"),
        ("atípicos con >=", "x < inferior or x > superior", "x <= inferior or x >= superior"),
        ("sin ValueError", "if n < 4:\n        raise ValueError(\"se necesitan al menos 4 datos\")", "if n < 1:\n        raise ValueError(\"x\")"),
        ("sin ordenar", "ordenados = sorted(valores)", "ordenados = list(valores)"),
    ])
    REF = os.path.join(REPO, "08_SOLUCIONES", "mini_etl_rel1_referencia.py")
    src = open(REF, encoding="utf-8").read()
    casos = {
        "sin regla (ME04)": open(os.path.join(REPO, "08_SOLUCIONES", "mini_etl_referencia.py"), encoding="utf-8").read(),
        "límite demasiado alto": src.replace("MAX_MONTO_CENTAVOS = 500000", "MAX_MONTO_CENTAVOS = 600000"),
        "límite demasiado bajo": src.replace("MAX_MONTO_CENTAVOS = 500000", "MAX_MONTO_CENTAVOS = 400000"),
        "causa mal rotulada": src.replace("motivos.append('monto')", "motivos.append('valor')"),
        "rompe unidades": src.replace("MAX_UNIDADES = 500 ", "MAX_UNIDADES = 5000 "),
    }
    for desc, texto in casos.items():
        d = tempfile.mkdtemp(); ruta = os.path.join(d, "mini_etl.py"); open(ruta, "w", encoding="utf-8").write(texto)
        r = subprocess.run([PY, "-B", os.path.join(REPO, "herramientas", "corregir_nuevos.py"), "REL1", ruta], capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(("RECHAZADO " if r.returncode else "¡ACEPTADO! "), "REL1", desc, "|", (r.stdout.strip() or r.stderr.strip())[:120])
        total += 0 if r.returncode else 1
    return total


def py_b6():
    PYREF = "08_SOLUCIONES/python_referencia_v6.py"
    total = 0
    total += probar("RS04", PYREF, [
        ("normal en vez de t", "stats.t.interval(confianza, n - 1, loc=media, scale=error)", "stats.norm.interval(confianza, loc=media, scale=error)"),
        ("error estándar poblacional", "error = stats.sem(valores)", "error = stats.sem(valores, ddof=0)"),
        ("grados de libertad n", "stats.t.interval(confianza, n - 1,", "stats.t.interval(confianza, n,"),
        ("sin ValueError", "if n < 2:\n        raise ValueError(\"se necesitan al menos 2 datos\")", "if n < 0:\n        raise ValueError(\"x\")"),
        ("comparación invertida", 'if meta < ic["inferior"]:\n        return "por encima de la meta"', 'if meta < ic["inferior"]:\n        return "por debajo de la meta"'),
        ("ignora la confianza", "stats.t.interval(confianza, n - 1,", "stats.t.interval(0.95, n - 1,"),
    ])
    total += probar("RS05", PYREF, [
        ("unilateral", "if abs(dif) >= abs(observada) - 1e-9:", "if dif <= observada + 1e-9:"),
        ("sin semilla", "azar = random.Random(semilla)", "azar = random.Random()"),
        ("sin mezclar", "azar.shuffle(junto)", "pass"),
        ("diferencia invertida", "observada = sum(a) / len(a) - sum(b) / len(b)", "observada = sum(b) / len(b) - sum(a) / len(a)"),
        ("p constante", '"p_valor": (extremos + 1) / (repeticiones + 1)}', '"p_valor": 0.5}'),
        ("sin ValueError", "if not a or not b:\n        raise ValueError(\"los dos grupos necesitan datos\")", "if False:\n        raise ValueError(\"x\")"),
    ])
    total += probar("RS06", PYREF, [
        ("gl combinados", "gl = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))", "gl = na + nb - 2"),
        ("porcentaje sobre la media equivocada", 'round(100 * dif / mb, 1)', 'round(100 * dif / ma, 1)'),
        ("t de Student", "equal_var=False", "equal_var=True"),
        ("ic con z", "critico = stats.t.ppf(0.975, gl)", "critico = 1.96"),
        ("varianza poblacional", "va = sum((x - ma) ** 2 for x in a) / (na - 1)", "va = sum((x - ma) ** 2 for x in a) / na"),
    ])
    return total


def pe01():
    src = open(os.path.join(REPO, "08_SOLUCIONES", "depuracion_PE01_referencia.py"), encoding="utf-8").read()
    roto = open(os.path.join(REPO, "03_EJERCICIOS", "Depuracion", "PE01_roto.py"), encoding="utf-8").read()
    V = ', validate="many_to_one"'
    A1 = 'assert por_categoria.sum() == total, f"Control: las categorías suman {por_categoria.sum()} y las ventas son {total}"'
    A2 = 'assert por_zona.sum() == total, f"Control: las zonas suman {por_zona.sum()} y las ventas son {total}"'
    for a in (V, A1, A2):
        assert a in src, a
    casos = [
        ("referencia", src, "aceptar"),
        ("sin validate (el control de categoría sigue deteniendo): válido", src.replace(V, "", 1), "aceptar"),
        ("sin validate ni control de categoría", src.replace(V, "", 1).replace(A1, "pass"), "rechazar"),
        ("sin validate en categoría y sin ningún assert", src.replace(V, "", 1).replace(A1, "pass").replace(A2, "pass"), "rechazar"),
        ("arreglos presentes pero sin controles", src.replace(A1, "pass").replace(A2, "pass"), "rechazar"),
        ("un solo control", src.replace(A2, "pass"), "rechazar"),
        ("sin dropna=False", src.replace('"zona", dropna=False', '"zona"'), "rechazar"),
        ("sin dropna=False ni control de zona", src.replace('"zona", dropna=False', '"zona"').replace(A2, "pass"), "rechazar"),
        ("merge interno en el catálogo (pierde ventas) con controles", src.replace('catalogo, on="producto", how="left", validate="many_to_one"', 'catalogo, on="producto", how="inner", validate="many_to_one"'), "aceptar"),
        ("merge interno en el catálogo sin validate ni controles", src.replace('catalogo, on="producto", how="left", validate="many_to_one"', 'catalogo, on="producto", how="inner"').replace(A1, "pass").replace(A2, "pass"), "rechazar"),
        ("validate demasiado estricto", src.replace(V, ', validate="one_to_one"', 1), "rechazar"),
        ("elimina duplicados del catálogo sin avisar", src.replace('catalogo, on="producto", how="left", validate="many_to_one"', 'catalogo.drop_duplicates(), on="producto", how="left"'), "rechazar"),
        ("script roto original", roto, "rechazar"),
        ("original roto con dos assert vacíos", roto.replace('    return dict(por_categoria), dict(por_zona)', '    assert True\n    assert True\n    return dict(por_categoria), dict(por_zona)'), "rechazar"),
        ("sin validate y control de categoría tautológico", src.replace(V, "", 1).replace(A1, "assert True"), "rechazar"),
        ("sin dropna=False y control de zona tautológico", src.replace('"zona", dropna=False', '"zona"').replace(A2, "assert True"), "rechazar"),
    ]
    malos = 0
    for desc, texto, esperado in casos:
        d = tempfile.mkdtemp(); ruta = os.path.join(d, "PE01.py"); open(ruta, "w", encoding="utf-8").write(texto)
        r = correr("PE01", ruta)
        res = "aceptar" if r.returncode == 0 else "rechazar"
        marca = "OK " if res == esperado else "FALLA"
        malos += res != esperado
        print(marca, f"[{res}]", desc, "|", (r.stdout.strip() or r.stderr.strip())[:100])
    return malos


def guias():
    dias = os.path.join(REPO, "01_PLAN_DIARIO", "dias")


    def ejecutar(*a):
        return subprocess.run([PY, "-B", VER, *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO)


    def guia(n):
        return [os.path.join(dias, f) for f in os.listdir(dias) if f.startswith(f"D{n:02d}_")][0]


    def mutar(n, desc, f):
        ruta = guia(n)
        original = open(ruta, "rb").read()
        try:
            t = original.decode("utf-8")
            t2 = f(t)
            assert t2 != t, f"la mutación «{desc}» no cambió nada"
            open(ruta, "wb").write(t2.encode("utf-8"))
            r = ejecutar("guias", "--dias", str(n))
            ok = r.returncode != 0
            print(("RECHAZADA " if ok else "¡ACEPTADA!  "), f"D{n:02d}", desc, "|", [l.strip() for l in r.stdout.splitlines() if "ERROR" in l][:1])
            return 0 if ok else 1
        finally:
            open(ruta, "wb").write(original)


    def primera_linea(t, patron):
        return next(l for l in t.splitlines() if re.search(patron, l))


    malos = 0
    # línea de la sección A (una lección) y primer ejercicio de C
    malos += mutar(10, "una lección desaparece de A", lambda t: t.replace(primera_linea(t, r"k:lec:8\.4\|completa"), "", 1))
    malos += mutar(10, "un enlace de ejercicio dentro de A", lambda t: t.replace("Teoría de la jornada:", "- [SQ01](../../03_EJERCICIOS/SQL/SQ01.md)\n\nTeoría de la jornada:", 1))
    malos += mutar(10, "ID accionable duplicado en C", lambda t: t.replace(primera_linea(t, r"k:ej:SQ01"), primera_linea(t, r"k:ej:SQ01") + "\n" + primera_linea(t, r"k:ej:SQ01"), 1))
    malos += mutar(10, "minutos de la tabla B alterados", lambda t: re.sub(r"(\|Teoría NÚCLEO\|)(\d+)(\|)", lambda m: m.group(1) + str(int(m.group(2)) + 5) + m.group(3), t, count=1))
    malos += mutar(10, "aparece EXTENDIDA", lambda t: t.replace("## E. Comprobar y entregar", "## E. Comprobar y entregar\n\nRuta EXTENDIDA opcional.", 1))
    malos += mutar(10, "enlace roto", lambda t: t.replace("03_EJERCICIOS/SQL/SQ01.md", "03_EJERCICIOS/SQL/SQ99.md", 1))
    malos += mutar(10, "ancla inexistente", lambda t: t.replace("04_modulos_imports.md)", "04_modulos_imports.md#no-existe)", 1))
    malos += mutar(10, "secciones D y E intercambiadas", lambda t: t.replace("## D. REFUERZO — voluntario", "## E. Comprobar y entregar", 1).replace("## E. Comprobar y entregar\n\nCorrectores", "## D. REFUERZO — voluntario\n\nCorrectores", 1))
    malos += mutar(10, "un ejercicio BASE sustituido", lambda t: t.replace("[P09 · precio_centavos](../../03_EJERCICIOS/Python/P09.md)", "[P10 · fecha_iso](../../03_EJERCICIOS/Python/P10.md)", 1).replace("k:ej:P09", "k:ej:P10", 1))
    malos += mutar(10, "REFUERZO que repite un BASE", lambda t: t.replace("<!--k:ej:E5-->", "<!--k:ej:P13-->", 1))
    malos += mutar(10, "sesiones retomables eliminadas", lambda t: t.replace("**Sesiones retomables**", "**Notas**", 1))
    malos += mutar(10, "lección movida después de C", lambda t: t.replace(primera_linea(t, r"k:lec:8\.3\|completa") + "\n", "", 1).replace("### SQL de recuperación", primera_linea(t, r"k:lec:8\.3\|completa") + "\n\n### SQL de recuperación", 1))
    malos += mutar(10, "total de la tabla B alterado", lambda t: t.replace("|**Total BASE**|**327**|", "|**Total BASE**|**330**|", 1))
    malos += mutar(6, "examen: se agrega teoría", lambda t: t.replace("No hay lecciones nuevas en un día de examen.", "- [ ] [1.1 · Tablas](../../02_TEORIA/01_SQL_basico/01_tablas_filas_columnas.md) <!--k:lec:1.1|completa-->\n\nNo hay lecciones nuevas en un día de examen.", 1))
    malos += mutar(7, "domingo con tiempo obligatorio", lambda t: t.replace("**0 minutos obligatorios**", "**30 minutos obligatorios**", 1))

    # casilla [x] borrada: se prueba sobre una copia de las guías con `progreso --carpeta`
    tmp = tempfile.mkdtemp()
    copia = os.path.join(tmp, "dias")
    shutil.copytree(dias, copia)
    f = [os.path.join(copia, x) for x in os.listdir(copia) if x.startswith("D04_")][0]
    t = open(f, encoding="utf-8").read()
    linea = next(l for l in t.splitlines() if l.startswith("- [x]"))
    open(f, "w", encoding="utf-8", newline="").write(t.replace(linea, linea.replace("- [x]", "- [ ]", 1), 1))
    r = ejecutar("progreso", "--carpeta", copia)
    print(("RECHAZADA " if r.returncode else "¡ACEPTADA!  "), "casilla [x] borrada |", [l.strip() for l in r.stdout.splitlines() if "ERROR" in l or "FALL" in l][:1])
    malos += 0 if r.returncode else 1
    return malos


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if modo not in ("ejercicios", "guias", "todo"):
        raise SystemExit(__doc__)
    malos = 0
    if modo in ("ejercicios", "todo"):
        for f in (sql, py_b2, py_b3, py_b4, py_b6, pe01):
            malos += f()
    if modo in ("guias", "todo"):
        malos += guias()
    print(f"\nMutantes aceptados indebidamente: {malos}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
