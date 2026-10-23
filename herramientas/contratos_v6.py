"""Contratos de los ejercicios nuevos del plan v6 (Python y Pandas). No sustituye a contratos_python.py: lo complementa.

Cada ejercicio define casos con resultado esperado y casos que deben fallar. El corrector (corregir_nuevos.py) los ejecuta sobre el módulo del estudiante.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def igualdad(actual, esperado):
    if isinstance(esperado, pd.DataFrame):
        pd.testing.assert_frame_equal(actual.reset_index(drop=True), esperado.reset_index(drop=True), check_dtype=False)
    elif isinstance(esperado, float):
        assert actual is not None and abs(actual - esperado) < 1e-8, (actual, esperado)
    else:
        assert actual == esperado, (actual, esperado)


def comprobar(id_, modulo):
    n = 0

    def check(fn, args, esperado):
        nonlocal n
        igualdad(getattr(modulo, fn)(*args), esperado)
        n += 1

    if id_ == "RP01":
        check("con_descuento", (100, 10), 90.0); check("con_descuento", (19.99, 15), 16.99); check("con_descuento", (50, 0), 50.0)
        check("con_descuento", (50, 100), 0.0); check("con_descuento", (50, 150), None); check("con_descuento", (50, -1), None)
    elif id_ == "RP02":
        check("clasificar_stock", (0, 10), "agotado"); check("clasificar_stock", (5, 10), "reponer"); check("clasificar_stock", (10, 10), "ok")
        check("clasificar_stock", (25, 10), "ok"); check("clasificar_stock", (None, 10), "sin dato"); check("clasificar_stock", (3, None), "sin dato")
        check("clasificar_stock", (None, None), "sin dato")
    elif id_ == "RP03":
        check("unidades_por_categoria", ([("Snacks", 3), ("Bebidas", 5), ("Snacks", 2)],), {"Snacks": 5, "Bebidas": 5})
        check("unidades_por_categoria", ([],), {}); check("unidades_por_categoria", ([("Lácteos", 7)],), {"Lácteos": 7})
        entrada = [("A", 1), ("A", 2)]
        modulo.unidades_por_categoria(entrada)
        assert entrada == [("A", 1), ("A", 2)], "No debes modificar la lista recibida"; n += 1
    elif id_ == "RP04":
        a = [{"tienda": "A", "ventas": 10}, {"tienda": "B", "ventas": 25}, {"tienda": "A", "ventas": 20}]
        check("mejor_tienda", (a,), ("A", 30)); check("mejor_tienda", ([],), None)
        check("mejor_tienda", ([{"tienda": "B", "ventas": 5}, {"tienda": "A", "ventas": 5}],), ("A", 5))
        check("mejor_tienda", ([{"tienda": "Z", "ventas": 1}],), ("Z", 1))
        copia = [dict(x) for x in a]
        modulo.mejor_tienda(a)
        assert a == copia, "No debes modificar los registros recibidos"; n += 1
    elif id_ == "RP05":
        import tempfile

        def archivo(texto, codificacion="utf-8"):
            d = tempfile.mkdtemp()
            ruta = Path(d) / "inventario.csv"
            ruta.write_bytes(texto.encode(codificacion))
            return str(ruta)

        cab = "producto_id,stock_inicial,stock_final,salidas_unidades\n"
        v, r = modulo.leer_inventario(archivo(cab + "1,82,103,154\n2,84,106,158\n"))
        assert v == [{"producto_id": 1, "stock_inicial": 82, "stock_final": 103, "salidas_unidades": 154},
                     {"producto_id": 2, "stock_inicial": 84, "stock_final": 106, "salidas_unidades": 158}] and r == [], (v, r); n += 1
        v, r = modulo.leer_inventario(archivo(cab + "1,82,103,154\n41,abc,100,5\n42,,100,5\n43,50,-3,5\n44,10,20\n2,84,106,158\n"))
        assert [x["producto_id"] for x in v] == [1, 2], f"filas válidas: {v}"; n += 1
        assert list(r) == [(3, "no numérico"), (4, "campo vacío"), (5, "negativo"), (6, "columnas incorrectas")], f"rechazadas: {r}"; n += 1
        v, r = modulo.leer_inventario(archivo(cab + "7,,x,3\n8,-1,,2\nx,-1,2,3\n"))
        assert list(r) == [(2, "campo vacío"), (3, "campo vacío"), (4, "no numérico")], f"orden de motivos: {r}"; n += 1
        v, r = modulo.leer_inventario(archivo("﻿" + cab + "\n1,5,6,7\n\n"))
        assert len(v) == 1 and r == [] and list(v[0]) == ["producto_id", "stock_inicial", "stock_final", "salidas_unidades"], f"BOM o líneas vacías: {v} {r}"; n += 1
        v, r = modulo.leer_inventario(ROOT / "04_DATASETS" / "inventario.csv")
        assert len(v) == 40 and r == [], "El archivo original tiene 40 filas válidas"; n += 1
    elif id_ == "RS01":
        from collections import Counter
        casos = [["a", "b", "a", "c", "a", "b"], ["x"] * 3, ["Kiosco", "Farmacia", "Kiosco", "Farmacia", "Tienda"]]
        for valores in casos:
            c = Counter(valores)
            esperado = [(k, f, round(100 * f / len(valores), 1)) for k, f in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))]
            actual = modulo.tabla_frecuencias(list(valores))
            assert [tuple(x) for x in actual] == esperado, f"{valores}: {actual} != {esperado}"; n += 1
        assert modulo.tabla_frecuencias([]) == [], "Lista vacía → []"; n += 1
        import sqlite3
        from contextlib import closing
        with closing(sqlite3.connect((ROOT / "04_DATASETS" / "comercial.db").as_uri() + "?mode=ro", uri=True)) as con:
            tipos = [f[0] for f in con.execute("SELECT tipo FROM clientes")]
        tabla = modulo.tabla_frecuencias(tipos)
        assert sum(f for _, f, _ in tabla) == len(tipos) and abs(sum(p for _, _, p in tabla) - 100) <= 0.2, "Las frecuencias deben sumar el total y los porcentajes ≈ 100"; n += 1
    elif id_ == "PD01":
        ped = pd.DataFrame({"pedido_id": [5, 1, 4, 2, 3, 6, 7], "cliente_id": [10, 10, 11, 12, 10, 12, 10],
                            "vendedor_id": [1, 1, 2, 2, 1, 2, 1],
                            "fecha": ["2026-09-03", "2026-09-03", "2026-09-01", "2026-09-30", "2026-10-01", "2026-09-15", "2026-09-10"],
                            "estado": ["entregado", "entregado", "entregado", "anulado", "entregado", "entregado", "entregado"]})
        cli = pd.DataFrame({"cliente_id": [10, 11, 12], "ruta": ["R01", "R02", "R01"]})
        copia_p, copia_c = ped.copy(), cli.copy()
        esperado = pd.DataFrame({"pedido_id": [1, 5, 7, 6], "cliente_id": [10, 10, 10, 12], "fecha": ["2026-09-03", "2026-09-03", "2026-09-10", "2026-09-15"]})
        check("filtrar_entregas", (ped, cli, "R01", "2026-09"), esperado)
        assert list(modulo.filtrar_entregas(ped, cli, "R01", "2026-09").index) == [0, 1, 2, 3], "El índice debe reiniciarse (0, 1, 2…)"; n += 1
        pd.testing.assert_frame_equal(ped, copia_p); pd.testing.assert_frame_equal(cli, copia_c); n += 1
        vacio = modulo.filtrar_entregas(ped, cli, "R09", "2026-09")
        assert list(vacio.columns) == ["pedido_id", "cliente_id", "fecha"] and len(vacio) == 0, "Sin coincidencias: DataFrame vacío con las tres columnas"; n += 1
        check("filtrar_entregas", (ped, cli, "R02", "2026-09"), pd.DataFrame({"pedido_id": [4], "cliente_id": [11], "fecha": ["2026-09-01"]}))
        real_p = pd.read_csv(ROOT / "04_DATASETS" / "distribuidora" / "pedidos.csv")
        real_c = pd.read_csv(ROOT / "04_DATASETS" / "distribuidora" / "clientes.csv")
        rutas = dict(zip(real_c.cliente_id, real_c.ruta))
        esp = sorted((f, p, c) for p, c, f, e in zip(real_p.pedido_id, real_p.cliente_id, real_p.fecha, real_p.estado) if e == "entregado" and rutas.get(c) == "R02" and f.startswith("2026-09"))
        got = modulo.filtrar_entregas(real_p, real_c, "R02", "2026-09")
        assert [(f, p, c) for p, c, f in zip(got.pedido_id, got.cliente_id, got.fecha)] == esp, "Con los datos reales (R02, 2026-09) las filas o su orden no coinciden"; n += 1
    elif id_ == "RD01":
        inv = pd.DataFrame({"producto_id": [1, 2, 3, 4, 5], "stock_inicial": [10, 10, 10, 10, 10], "stock_final": [5, 20, 7, 9, 0], "salidas_unidades": [9, 8, 7, 14, 3]})
        copia = inv.copy()
        esperado = pd.DataFrame({"producto_id": [4, 1, 5], "salidas_unidades": [14, 9, 3], "stock_final": [9, 5, 0], "diferencia": [5, 4, 3]})
        check("productos_a_reponer", (inv,), esperado)
        assert list(modulo.productos_a_reponer(inv).index) == [0, 1, 2], "El índice debe reiniciarse (0, 1, 2…)"; n += 1
        pd.testing.assert_frame_equal(inv, copia); n += 1
        empate = pd.DataFrame({"producto_id": [9, 3], "stock_inicial": [1, 1], "stock_final": [1, 1], "salidas_unidades": [6, 6]})
        check("productos_a_reponer", (empate,), pd.DataFrame({"producto_id": [3, 9], "salidas_unidades": [6, 6], "stock_final": [1, 1], "diferencia": [5, 5]}))
        ninguno = modulo.productos_a_reponer(inv.assign(salidas_unidades=0))
        assert len(ninguno) == 0 and list(ninguno.columns) == ["producto_id", "salidas_unidades", "stock_final", "diferencia"], "Sin filas: DataFrame vacío con las cuatro columnas"; n += 1
        real = pd.read_csv(ROOT / "04_DATASETS" / "inventario.csv")
        esp = sorted(((s - f), p) for p, f, s in zip(real.producto_id, real.stock_final, real.salidas_unidades) if s > f)
        esp = sorted(esp, key=lambda t: (-t[0], t[1]))
        got = modulo.productos_a_reponer(real)
        assert [(d, p) for d, p in zip(got["diferencia"], got["producto_id"])] == esp, "Con inventario.csv el orden o las filas no coinciden"; n += 1
    elif id_ == "RS02":
        import statistics as st
        casos = [[10, 20, 30, 40], [5, 5, 5], [1, 2, 100], [7.5, 8.5, 9.0, 10.0, 30.0]]
        for v in casos:
            m = st.mean(v); sd = st.stdev(v)
            esperado = {"n": len(v), "media": round(m, 2), "mediana": round(st.median(v), 2), "desviacion": round(sd, 2), "cv": round(sd / m, 3)}
            actual = modulo.resumen_centro_dispersion(list(v))
            assert {k: actual[k] for k in esperado} == esperado, f"{v}: {actual} != {esperado}"; n += 1
        un = modulo.resumen_centro_dispersion([42])
        assert un["n"] == 1 and un["media"] == 42 and un["mediana"] == 42 and un["desviacion"] is None and un["cv"] is None, f"Con un solo dato la desviación y el cv son None: {un}"; n += 1
        cero = modulo.resumen_centro_dispersion([-1, 1])
        assert cero["cv"] is None, "Si la media es 0 el cv es None"; n += 1
        import csv
        with open(ROOT / "04_DATASETS" / "distribuidora" / "drop_por_pedido.csv", encoding="utf-8-sig", newline="") as f:
            r05 = [float(x["drop_bs"]) for x in csv.DictReader(f) if x["ruta"] == "R05"]
        m, sd = st.mean(r05), st.stdev(r05)
        real = modulo.resumen_centro_dispersion(r05)
        assert (real["n"], real["media"], real["mediana"], real["desviacion"], real["cv"]) == (len(r05), round(m, 2), round(st.median(r05), 2), round(sd, 2), round(sd / m, 3)), f"Con la ruta R05: {real}"; n += 1
    elif id_ == "RD02":
        df = pd.DataFrame({"id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                           "fecha": ["2026-09-01", "05/09/2026", "31/02/2026", "2026-13-01", "ayer", "", "2026-09-20", "19/9/2026", "2026-09-02", "2026-09-03", "2026-09-04"],
                           "monto": ["1.234,50", "Bs 80,5", "50,00", "20,00", "10,00", "7,00", "abc", "10,00", "-5,00", "nan", "80.25"]})
        copia = df.copy()
        validas, rechazadas = modulo.limpiar_ventas(df)
        pd.testing.assert_frame_equal(df, copia); n += 1  # no modifica la entrada
        assert list(validas.columns) == ["id", "fecha", "monto"], f"Columnas de válidas: {list(validas.columns)}"; n += 1
        assert list(rechazadas.columns) == ["id", "fecha", "monto", "motivo"], f"Columnas de rechazadas: {list(rechazadas.columns)}"; n += 1
        esp_v = pd.DataFrame({"id": [1, 2, 11], "fecha": ["2026-09-01", "2026-09-05", "2026-09-04"], "monto": [1234.5, 80.5, 80.25]})
        pd.testing.assert_frame_equal(validas.reset_index(drop=True), esp_v, check_dtype=False); n += 1
        esp_r = {3: "fecha", 4: "fecha", 5: "fecha", 6: "fecha", 7: "monto", 8: "fecha", 9: "monto", 10: "monto"}
        assert {int(i): m for i, m in zip(rechazadas["id"], rechazadas["motivo"])} == esp_r, f"Motivos de rechazo: {dict(zip(rechazadas['id'], rechazadas['motivo']))}"; n += 1
        assert len(validas) + len(rechazadas) == len(df), "Cuadre: válidas + rechazadas debe ser igual a las filas de entrada"; n += 1
        assert list(rechazadas.loc[rechazadas["id"] == 3, "fecha"]) == ["31/02/2026"] and list(rechazadas.loc[rechazadas["id"] == 7, "monto"]) == ["abc"], "Las rechazadas conservan el texto original"; n += 1
        doble = modulo.limpiar_ventas(pd.DataFrame({"id": [1], "fecha": ["ayer"], "monto": ["abc"]}))[1]
        assert list(doble["motivo"]) == ["fecha;monto"], f"Con fecha y monto inválidos el motivo es 'fecha;monto': {list(doble['motivo'])}"; n += 1
        cero = modulo.limpiar_ventas(pd.DataFrame({"id": [1], "fecha": ["2026-09-01"], "monto": ["0,00"]}))[0]
        assert list(cero["monto"]) == [0.0], "Un monto 0 es válido"; n += 1
    elif id_ == "RS03":
        import numpy as np
        for v in ([1, 2, 3, 4, 5, 100], [10, 12, 13, 15, 15, 16, 18, 21], [3.5, 3.5, 3.5, 3.5, 9.0], [4, 8, 15, 16, 23, 42, -30]):
            q1, q3 = np.percentile(v, [25, 75])
            iqr = q3 - q1
            inf, sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            esperado = {"q1": round(float(q1), 2), "q3": round(float(q3), 2), "iqr": round(float(iqr), 2), "cerca_inferior": round(float(inf), 2),
                        "cerca_superior": round(float(sup), 2), "atipicos": sum(1 for x in v if x < inf or x > sup)}
            actual = modulo.cercas_tukey(list(v))
            assert {k: actual[k] for k in esperado} == esperado, f"{v}: {actual} != {esperado}"; n += 1
        try:
            modulo.cercas_tukey([1, 2, 3])
        except ValueError:
            n += 1
        else:
            raise AssertionError("Con menos de 4 datos debe lanzar ValueError")
        import csv
        with open(ROOT / "04_DATASETS" / "distribuidora" / "drop_por_pedido.csv", encoding="utf-8-sig", newline="") as f:
            r03 = [float(x["drop_bs"]) for x in csv.DictReader(f) if x["ruta"] == "R03"]
        q1, q3 = np.percentile(r03, [25, 75]); iqr = q3 - q1
        real = modulo.cercas_tukey(r03)
        esperado = (round(float(q1), 2), round(float(q3), 2), round(float(iqr), 2), sum(1 for x in r03 if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr))
        assert (real["q1"], real["q3"], real["iqr"], real["atipicos"]) == esperado, f"Con la ruta R03: {real}"; n += 1
    elif id_ == "PE01":
        ventas = pd.DataFrame({"ticket": [1, 2, 3, 4, 5, 6], "producto": ["P-01", "P-02", "P-02", "P-03", "P-01", "P-03"],
                               "cliente": [1, 2, 3, 3, 4, 1], "monto": [100, 50, 70, 30, 20, 10]})
        catalogo = pd.DataFrame({"producto": ["P-01", "P-02", "P-03"], "categoria": ["Abarrotes", "Bebidas", "Snacks"]})
        clientes = pd.DataFrame({"cliente": [1, 2, 3, 4], "zona": ["Norte", "Sur", None, "Norte"]})
        total = int(ventas["monto"].sum())
        import ast
        import inspect
        import textwrap
        controles = sum(isinstance(x, (ast.Assert, ast.Raise)) for x in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(modulo.resumen)))))
        assert controles >= 2, f"Dentro de `resumen` faltan los dos controles de cuadre (assert o raise): encontré {controles}"; n += 1
        copias = [ventas.copy(), catalogo.copy(), clientes.copy()]
        por_cat, por_zona = modulo.resumen(ventas, catalogo, clientes)
        por_cat, por_zona = dict(por_cat), dict(por_zona)
        for a, b in zip((ventas, catalogo, clientes), copias):
            pd.testing.assert_frame_equal(a, b)
        n += 1  # no modifica las entradas
        assert por_cat == {"Abarrotes": 120, "Bebidas": 120, "Snacks": 40}, f"Totales por categoría: {por_cat}"; n += 1
        assert sum(por_zona.values()) == total, f"Los totales por zona suman {sum(por_zona.values())} y las ventas son {total}: se perdieron ventas con la zona vacía"; n += 1
        assert len(por_zona) == 3 and por_zona.get("Norte") == 130 and por_zona.get("Sur") == 50, f"Totales por zona: {por_zona}"; n += 1
        repetido = pd.concat([catalogo, pd.DataFrame({"producto": ["P-02"], "categoria": ["Bebidas"]})], ignore_index=True)
        try:
            resultado = modulo.resumen(ventas, repetido, clientes)
        except (ValueError, AssertionError):
            n += 1
        else:
            raise AssertionError("Con un producto repetido en el catálogo la función debe detenerse (ValueError o AssertionError): el total por categoría se infla en silencio" + f" (devolvió {dict(resultado[0])})")
        desconocido = pd.concat([ventas, pd.DataFrame({"ticket": [7], "producto": ["P-99"], "cliente": [2], "monto": [5]})], ignore_index=True)
        try:
            c2, z2 = modulo.resumen(desconocido, catalogo, clientes)
        except (ValueError, AssertionError):
            n += 1
        else:
            assert sum(dict(c2).values()) == total + 5, "Un producto fuera del catálogo no puede hacer desaparecer ventas: detén el proceso o consérvalas en un grupo propio"; n += 1
    elif id_ == "RS04":
        from scipy import stats
        casos = [[10, 12, 9, 11, 13, 10, 12], [100, 200, 150, 120, 180], [5.5, 6.5, 7.5, 6.0, 8.0, 7.0]]
        for v in casos:
            m = sum(v) / len(v)
            se = stats.sem(v)
            lo, hi = stats.t.interval(0.95, len(v) - 1, loc=m, scale=se)
            esperado = {"n": len(v), "media": round(m, 2), "error_estandar": round(float(se), 3), "inferior": round(float(lo), 2), "superior": round(float(hi), 2)}
            actual = modulo.ic_media(list(v))
            assert {k: actual[k] for k in esperado} == esperado, f"{v}: {actual} != {esperado}"; n += 1
        lo99 = modulo.ic_media(casos[1], 0.99)
        m, se = sum(casos[1]) / 5, stats.sem(casos[1])
        assert lo99["inferior"] == round(float(stats.t.interval(0.99, 4, loc=m, scale=se)[0]), 2), "Con confianza 0,99 el intervalo es más ancho"; n += 1
        try:
            modulo.ic_media([5])
        except ValueError:
            n += 1
        else:
            raise AssertionError("Con un solo dato debe lanzar ValueError")
        import csv
        with open(ROOT / "04_DATASETS" / "distribuidora" / "drop_por_pedido.csv", encoding="utf-8-sig", newline="") as f:
            r05 = [float(x["drop_bs"]) for x in csv.DictReader(f) if x["ruta"] == "R05"]
        m, se = sum(r05) / len(r05), stats.sem(r05)
        lo, hi = stats.t.interval(0.95, len(r05) - 1, loc=m, scale=se)
        real = modulo.ic_media(r05)
        assert (real["n"], real["media"], real["inferior"], real["superior"]) == (len(r05), round(m, 2), round(float(lo), 2), round(float(hi), 2)), f"Con la ruta R05: {real}"; n += 1
        for meta, texto in ((float(lo) - 30, "por encima de la meta"), (float(hi) + 30, "por debajo de la meta"), (round(m), "no distinguible de la meta")):
            assert modulo.compara_con_meta(r05, meta) == texto, f"Meta {meta:.0f}: se esperaba «{texto}» y se obtuvo «{modulo.compara_con_meta(r05, meta)}»"; n += 1
    elif id_ == "RS05":
        import itertools
        import statistics as st
        a, b = [1, 2, 3], [4, 5, 6]
        r = modulo.prueba_permutacion(a, b, repeticiones=20000, semilla=7)
        assert r["diferencia"] == -3.0, f"diferencia = media(a) - media(b): {r['diferencia']}"; n += 1
        exacto = sum(1 for c in itertools.combinations(range(6), 3)
                     if abs(st.mean([(a + b)[i] for i in c]) - st.mean([(a + b)[i] for i in range(6) if i not in c])) >= 3 - 1e-9) / 20
        assert abs(r["p_valor"] - exacto) < 0.03, f"p-valor = {r['p_valor']:.4f}; el p exacto bilateral es {exacto}"; n += 1
        assert modulo.prueba_permutacion(a, b, 2000, 3)["p_valor"] == modulo.prueba_permutacion(a, b, 2000, 3)["p_valor"], "Con la misma semilla el resultado debe repetirse"; n += 1
        igual = modulo.prueba_permutacion([1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8], repeticiones=2000, semilla=1)
        assert igual["diferencia"] == 0 and igual["p_valor"] >= 0.9, f"Dos grupos idénticos: p ≈ 1 ({igual})"; n += 1
        lejos = modulo.prueba_permutacion([100 + i for i in range(30)], [i for i in range(30)], repeticiones=3000, semilla=2)
        assert lejos["p_valor"] < 0.01, f"Grupos muy separados: p ≈ 0 ({lejos})"; n += 1
        try:
            modulo.prueba_permutacion([], [1, 2])
        except ValueError:
            n += 1
        else:
            raise AssertionError("Un grupo vacío debe lanzar ValueError")
        import csv
        with open(ROOT / "04_DATASETS" / "distribuidora" / "drop_por_pedido.csv", encoding="utf-8-sig", newline="") as f:
            filas = list(csv.DictReader(f))
        r01 = [float(x["drop_bs"]) for x in filas if x["ruta"] == "R01"]
        r04 = [float(x["drop_bs"]) for x in filas if x["ruta"] == "R04"]
        real = modulo.prueba_permutacion(r01, r04, repeticiones=3000, semilla=11)
        assert real["diferencia"] == round(st.mean(r01) - st.mean(r04), 2) and real["p_valor"] < 0.03, f"R01 frente a R04: {real}"; n += 1
    elif id_ == "RS06":
        import statistics as st
        from scipy import stats
        casos = [([10, 12, 9, 11, 13, 10, 12], [14, 15, 13, 16, 12, 17]), ([100, 200, 150, 120, 180, 90], [110, 210, 170, 140, 160, 95, 130]), ([5.0, 5.5, 6.0, 5.2], [8.0, 7.5, 9.0, 8.5, 7.9])]
        for a, b in casos:
            na, nb = len(a), len(b)
            va, vb = st.variance(a), st.variance(b)
            dif = st.mean(a) - st.mean(b)
            ee = (va / na + vb / nb) ** 0.5
            gl = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
            t = stats.ttest_ind(a, b, equal_var=False)
            crit = stats.t.ppf(0.975, gl)
            mb = st.mean(b)
            esperado = {"diferencia": round(dif, 2), "t": round(float(t.statistic), 3), "gl": round(gl, 1), "p_valor": round(float(t.pvalue), 4),
                        "ic_inferior": round(dif - crit * ee, 2), "ic_superior": round(dif + crit * ee, 2), "dif_relativa_pct": round(100 * dif / mb, 1)}
            actual = modulo.welch_y_efecto(list(a), list(b))
            assert {k: actual[k] for k in esperado} == esperado, f"{a} y {b}: {actual} != {esperado}"; n += 1
        try:
            modulo.welch_y_efecto([1], [2, 3])
        except ValueError:
            n += 1
        else:
            raise AssertionError("Con un grupo de un solo dato debe lanzar ValueError")
        import csv
        with open(ROOT / "04_DATASETS" / "distribuidora" / "drop_por_pedido.csv", encoding="utf-8-sig", newline="") as f:
            filas = list(csv.DictReader(f))
        r04 = [float(x["drop_bs"]) for x in filas if x["ruta"] == "R04"]
        r05 = [float(x["drop_bs"]) for x in filas if x["ruta"] == "R05"]
        t = stats.ttest_ind(r04, r05, equal_var=False)
        real = modulo.welch_y_efecto(r04, r05)
        assert (real["t"], real["p_valor"]) == (round(float(t.statistic), 3), round(float(t.pvalue), 4)), f"R04 frente a R05: {real}"; n += 1
        assert real["p_valor"] < 0.001 and real["dif_relativa_pct"] < 0, "Con estos datos la diferencia es distinguible del azar y R04 queda por debajo de R05"; n += 1
    else:
        raise KeyError(f"{id_}: sin contrato definido en contratos_v6.py")
    return n


def comprobar_pruebas(id_, archivo):
    """Ejercicios en los que el estudiante entrega pruebas: deben PASAR con la versión correcta y FALLAR con cada versión defectuosa."""
    import ast
    import sys
    import types

    if id_ != "PT01":
        raise KeyError(f"{id_}: sin contrato de pruebas definido")
    texto = Path(archivo).read_text(encoding="utf-8-sig")
    codigo = compile(texto, str(archivo), "exec")
    asserts = sum(isinstance(x, ast.Assert) for x in ast.walk(ast.parse(texto)))
    assert asserts >= 4, f"Se esperaban al menos 4 assert y hay {asserts}"

    def correcta(monto):
        if monto < 200:
            return "Pequeño"
        if monto <= 600:
            return "Mediano"
        return "Grande"

    def v1(monto):  # límite inferior mal tratado
        if monto <= 200:
            return "Pequeño"
        if monto <= 600:
            return "Mediano"
        return "Grande"

    def v2(monto):  # límite superior mal tratado
        if monto < 200:
            return "Pequeño"
        if monto < 600:
            return "Mediano"
        return "Grande"

    def v3(monto):  # acepta un dato ausente en silencio
        if monto is None:
            return "Pequeño"
        return correcta(monto)

    def ejecutar(funcion):
        previo = sys.modules.get("mis_funciones")
        modulo = types.ModuleType("mis_funciones")
        modulo.clasificar_ticket = funcion
        sys.modules["mis_funciones"] = modulo
        try:
            exec(codigo, {"__name__": "pruebas_estudiante"})
        finally:
            if previo is None:
                sys.modules.pop("mis_funciones", None)
            else:
                sys.modules["mis_funciones"] = previo

    try:
        ejecutar(correcta)
    except AssertionError as e:
        raise AssertionError(f"Tus pruebas fallan con la versión correcta de clasificar_ticket: revisa el valor esperado de tu assert ({e})")
    descripciones = {v1: "un error en un límite inferior", v2: "un error en un límite superior", v3: "no rechaza un dato ausente"}
    for version, que in descripciones.items():
        try:
            ejecutar(version)
        except AssertionError:
            continue
        raise AssertionError(f"Tus pruebas no detectaron una versión con {que}. Agrega una prueba que la haga fallar")
    return asserts
