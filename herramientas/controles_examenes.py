"""Cifras de control de las variantes, diagnósticos y predicciones de los exámenes S01–S06 (y de sus variantes de recuperación).

    python herramientas/controles_examenes.py --generar     # escribe 08_SOLUCIONES/controles_examenes.json y .md
    python herramientas/controles_examenes.py --comprobar   # vuelve a ejecutar cada control y compara con el JSON (lo usa verificar_etapa2.py)

Cada control es una consulta SQL sobre 04_DATASETS/comercial.db o un fragmento de Python que se ejecuta aislado (python -I) desde la raíz del paquete.
Las cifras no están en los enunciados de los exámenes: se abren en 08_SOLUCIONES/controles_examenes.md solo DESPUÉS de cerrar el intento.
"""
from pathlib import Path
import argparse
import json
import sqlite3
import subprocess
import sys
from contextlib import closing

RAIZ = Path(__file__).resolve().parents[1]
DB = '04_DATASETS/comercial.db'
CARGAR_REF_C06 = '''
import importlib.util, pandas as pd
spec = importlib.util.spec_from_file_location('ref', '08_SOLUCIONES/etl_nuevo_referencia.py'); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
raw = pd.read_csv('04_DATASETS/transferencia/transacciones_raw.csv', sep=';', dtype=str, keep_default_na=False)
cat = pd.read_csv('04_DATASETS/transferencia/catalogo.csv', dtype=str, keep_default_na=False)
'''
CARGAR_REF_MINI = '''
import importlib.util, pandas as pd
spec = importlib.util.spec_from_file_location('mini', '08_SOLUCIONES/mini_etl_referencia.py'); mini = importlib.util.module_from_spec(spec); spec.loader.exec_module(mini)
raw = mini.extraer('04_DATASETS/mini_etl/ventas_mini_raw.csv')
cat = pd.read_csv('04_DATASETS/mini_etl/productos_mini.csv', dtype=str, keep_default_na=False)
'''
CARGAR_REF_DIST = '''
import importlib.util, shutil, tempfile, pathlib, logging
logging.disable(logging.CRITICAL)
tmp = pathlib.Path(tempfile.mkdtemp())
for carpeta in ('04_DATASETS/distribuidora/etl', '08_SOLUCIONES'):
    shutil.copytree(carpeta, tmp / carpeta, ignore=shutil.ignore_patterns('__pycache__'))
(tmp / 'mi_trabajo/etl').mkdir(parents=True)
spec = importlib.util.spec_from_file_location('dist', tmp / '08_SOLUCIONES/etl_distribuidora.py'); dist = importlib.util.module_from_spec(spec); spec.loader.exec_module(dist)
raw, vend = dist.extraer()
silver = dist.transformar(raw, vend)
'''

# (id, examen, titulo, tipo, contenido)  — tipo: 'sql' (consulta sobre comercial.db) o 'python' (fragmento que imprime el resultado)
CONTROLES = [
    # ───────────────────────── S01 ─────────────────────────
    ('S01-VS', 'S01', 'Variante SQL: rutas con al menos dos kioscos', 'sql',
     "SELECT ruta, COUNT(*) AS kioscos FROM clientes WHERE tipo = 'Kiosco' GROUP BY ruta HAVING COUNT(*) >= 2 ORDER BY kioscos DESC, ruta"),
    ('S01-VP', 'S01', 'Variante Python: contar_por_tipo (solo tipos con dos o más clientes)', 'python', '''
def contar_por_tipo(clientes):
    conteos = {}
    for c in clientes:
        conteos[c["tipo"]] = conteos.get(c["tipo"], 0) + 1
    return {tipo: n for tipo, n in conteos.items() if n >= 2}

entradas = [[{"tipo": "Kiosco"}, {"tipo": "Farmacia"}, {"tipo": "Kiosco"}, {"tipo": "Minimarket"}, {"tipo": "Kiosco"}, {"tipo": "Farmacia"}], [], [{"tipo": "Kiosco"}]]
for e in entradas:
    print(contar_por_tipo(e))
'''),
    ('S01-KPI', 'S01', 'KPI: cumplimiento de cuatro zonas (la última con meta cero)', 'python', '''
def porcentaje(real, meta):
    return None if meta <= 0 else 100 * real / meta

for zona, meta, real in [("Norte", 80, 72), ("Centro", 100, 100), ("Sur", 60, 66), ("Este", 0, 5)]:
    print(zona, porcentaje(real, meta))
'''),
    ('S01-D1', 'S01', 'Diagnóstico SQL: COUNT en WHERE', 'python', '''
import sqlite3
c = sqlite3.connect("file:04_DATASETS/comercial.db?mode=ro", uri=True)
try:
    c.execute("SELECT ruta, COUNT(*) FROM clientes WHERE COUNT(*) > 20 GROUP BY ruta")
except sqlite3.OperationalError as e:
    print("error:", e)
print(c.execute("SELECT ruta, COUNT(*) FROM clientes GROUP BY ruta HAVING COUNT(*) > 20 ORDER BY 2 DESC, 1").fetchall())
'''),
    ('S01-D2', 'S01', 'Diagnóstico Python: acumulador que se reinicia dentro del bucle', 'python', '''
lineas = [{"estado": "entregado", "cantidad": 2, "precio": 10}, {"estado": "anulado", "cantidad": 9, "precio": 9}, {"estado": "entregado", "cantidad": 1, "precio": 30}, {"estado": "entregado", "cantidad": 3, "precio": 5}]
def mala(lineas):
    for linea in lineas:
        total = 0
        if linea["estado"] == "entregado":
            total = total + linea["cantidad"] * linea["precio"]
    return total
def buena(lineas):
    total = 0
    for linea in lineas:
        if linea["estado"] == "entregado":
            total = total + linea["cantidad"] * linea["precio"]
    return total
print(mala(lineas), buena(lineas))
'''),
    ('S01-PR1', 'S01', 'Predicción SQL: tipos de cliente de la ruta R03', 'sql',
     "SELECT tipo, COUNT(*) FROM clientes WHERE ruta = 'R03' GROUP BY tipo ORDER BY COUNT(*) DESC, tipo"),
    ('S01-R1', 'S01', 'Recuperación SQL: rutas con al menos tres minimarkets', 'sql',
     "SELECT ruta, COUNT(*) AS minimarkets FROM clientes WHERE tipo = 'Minimarket' GROUP BY ruta HAVING COUNT(*) >= 3 ORDER BY minimarkets DESC, ruta"),
    ('S01-R2', 'S01', 'Recuperación Python: suma de cantidades por estado', 'python', '''
def unidades_por_estado(lineas):
    total = {}
    for linea in lineas:
        total[linea["estado"]] = total.get(linea["estado"], 0) + linea["cantidad"]
    return total
print(unidades_por_estado([{"estado": "entregado", "cantidad": 4}, {"estado": "anulado", "cantidad": 2}, {"estado": "entregado", "cantidad": 1}]))
print(unidades_por_estado([]))
'''),
    ('S01-R3', 'S01', 'Recuperación KPI: cumplimiento de cuatro zonas inventadas', 'python', '''
def porcentaje(real, meta):
    return None if meta <= 0 else 100 * real / meta
for meta, real in [(50, 25), (0, 3), (40, 40), (200, 150)]:
    print(meta, real, porcentaje(real, meta))
'''),
    # ───────────────────────── S02 ─────────────────────────
    ('S02-VS', 'S02', 'Variante SQL: clientes de R04 sin pedido entregado en julio', 'sql',
     "SELECT c.cliente_id, c.nombre_negocio FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'entregado' "
     "AND p.fecha BETWEEN '2026-07-01' AND '2026-07-31' WHERE c.ruta = 'R04' AND p.pedido_id IS NULL ORDER BY c.cliente_id"),
    ('S02-VP', 'S02', 'Variante Python: descuento_pct (entero de 0 a 100)', 'python', '''
from decimal import Decimal, InvalidOperation
def descuento_pct(texto):
    try:
        x = Decimal(texto.strip())
    except InvalidOperation as e:
        raise ValueError("no es un número") from e
    if not x.is_finite() or x != x.to_integral_value() or x < 0 or x > 100:
        raise ValueError("fuera de rango o con decimales")
    return int(x)
for t in ["15", " 15 ", "15.0", "0", "100", "-1", "101", "2.5", "abc", "", "nan"]:
    try:
        print(repr(t), descuento_pct(t))
    except ValueError:
        print(repr(t), "ValueError")
'''),
    ('S02-D1', 'S02', 'Diagnóstico SQL: LEFT JOIN con el filtro de la tabla derecha en el WHERE', 'python', '''
import sqlite3
c = sqlite3.connect("file:04_DATASETS/comercial.db?mode=ro", uri=True)
mala = c.execute("SELECT COUNT(*) FROM (SELECT c.cliente_id, COUNT(p.pedido_id) FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id WHERE c.ruta = 'R03' AND p.estado = 'anulado' GROUP BY c.cliente_id)").fetchone()[0]
buena = c.execute("SELECT COUNT(*) FROM (SELECT c.cliente_id, COUNT(p.pedido_id) FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'anulado' WHERE c.ruta = 'R03' GROUP BY c.cliente_id)").fetchone()[0]
print(mala, buena)
'''),
    ('S02-D2', 'S02', 'Diagnóstico Python: int(float(texto)) trunca en silencio', 'python', '''
def cantidad(texto):
    return int(float(texto))
for t in ["3", "3.0", "3.7", "0.2", "abc"]:
    try:
        print(repr(t), cantidad(t))
    except ValueError:
        print(repr(t), "ValueError")
'''),
    ('S02-C', 'S02', 'Cuadre: valor de todas las líneas, ventas entregadas y la diferencia (líneas de pedidos anulados)', 'sql',
     "SELECT ROUND((SELECT SUM(cantidad * precio_unitario) FROM pedido_items), 2) AS todas, "
     "ROUND((SELECT SUM(i.cantidad * i.precio_unitario) FROM pedido_items i JOIN pedidos p ON p.pedido_id = i.pedido_id WHERE p.estado = 'entregado'), 2) AS entregadas, "
     "ROUND((SELECT SUM(i.cantidad * i.precio_unitario) FROM pedido_items i JOIN pedidos p ON p.pedido_id = i.pedido_id WHERE p.estado = 'anulado'), 2) AS anuladas"),
    ('S02-R1', 'S02', 'Recuperación SQL: clientes de R02 sin pedido anulado', 'sql',
     "SELECT c.cliente_id FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.cliente_id AND p.estado = 'anulado' WHERE c.ruta = 'R02' AND p.pedido_id IS NULL ORDER BY c.cliente_id"),
    ('S02-R2', 'S02', 'Recuperación Python: precio con dos decimales a centavos sin float', 'python', '''
from decimal import Decimal, InvalidOperation
def a_centavos(texto):
    try:
        x = Decimal(texto.strip().replace(",", "."))
    except InvalidOperation as e:
        raise ValueError("no es un número") from e
    if not x.is_finite() or x < 0 or x * 100 != (x * 100).to_integral_value():
        raise ValueError("precio inválido")
    return int(x * 100)
for t in ["2,05", "10", " 0.10 ", "2.005", "-1", "x"]:
    try:
        print(repr(t), a_centavos(t))
    except ValueError:
        print(repr(t), "ValueError")
'''),
    # ───────────────────────── S03 ─────────────────────────
    ('S03-VS', 'S03', 'Variante SQL: ventas entregadas de agosto por categoría y su porcentaje', 'sql',
     "WITH v AS (SELECT pr.categoria, SUM(i.cantidad * i.precio_unitario) AS ventas FROM pedido_items i JOIN pedidos p ON p.pedido_id = i.pedido_id "
     "JOIN productos pr ON pr.producto_id = i.producto_id WHERE p.estado = 'entregado' AND p.fecha BETWEEN '2026-08-01' AND '2026-08-31' GROUP BY pr.categoria) "
     "SELECT categoria, ROUND(ventas, 2), ROUND(100.0 * ventas / SUM(ventas) OVER (), 2) FROM v ORDER BY ventas DESC, categoria"),
    ('S03-VP', 'S03', 'Variante Pandas: contar_huerfanos (pedidos sin cliente) deteniendo un catálogo repetido', 'python', '''
import pandas as pd
def contar_huerfanos(pedidos, clientes):
    unido = pedidos.merge(clientes[["cliente_id"]], on="cliente_id", how="left", validate="many_to_one", indicator=True)
    return int((unido["_merge"] == "left_only").sum())
pedidos = pd.DataFrame({"pedido_id": [1, 2, 3, 4], "cliente_id": [10, 11, 99, 10]})
print(contar_huerfanos(pedidos, pd.DataFrame({"cliente_id": [10, 11, 12]})))
try:
    contar_huerfanos(pedidos, pd.DataFrame({"cliente_id": [10, 10, 11]}))
except Exception as e:
    print(type(e).__name__)
'''),
    ('S03-D1', 'S03', 'Diagnóstico Pandas: el merge con catálogo repetido multiplica filas', 'python', '''
import pandas as pd
pedidos = pd.DataFrame({"pedido_id": [1, 2, 3], "cliente_id": [10, 11, 10], "monto": [100, 50, 70]})
clientes = pd.DataFrame({"cliente_id": [10, 10, 11], "ruta": ["R01", "R01", "R02"]})
unido = pedidos.merge(clientes, on="cliente_id", how="left")
print(len(pedidos), len(unido), int(pedidos["monto"].sum()), int(unido["monto"].sum()))
'''),
    ('S03-D2', 'S03', 'Diagnóstico SQL: el acumulado con empates', 'sql',
     "WITH t(c, v) AS (VALUES ('A', 10), ('B', 10), ('C', 5)) SELECT c, v, SUM(v) OVER (ORDER BY v DESC) AS acum_sin_desempate, "
     "SUM(v) OVER (ORDER BY v DESC, c ROWS UNBOUNDED PRECEDING) AS acum_con_desempate FROM t ORDER BY v DESC, c"),
    ('S03-R1', 'S03', 'Recuperación SQL: porcentaje de cada ruta en las ventas entregadas de septiembre', 'sql',
     "WITH v AS (SELECT c.ruta, SUM(i.cantidad * i.precio_unitario) AS ventas FROM pedido_items i JOIN pedidos p ON p.pedido_id = i.pedido_id "
     "JOIN clientes c ON c.cliente_id = p.cliente_id WHERE p.estado = 'entregado' AND p.fecha BETWEEN '2026-09-01' AND '2026-09-30' GROUP BY c.ruta) "
     "SELECT ruta, ROUND(ventas, 2), ROUND(100.0 * ventas / SUM(ventas) OVER (), 2) FROM v ORDER BY ventas DESC, ruta"),
    ('S03-R2', 'S03', 'Recuperación Pandas: quitar exactos y perfilar una tabla nueva', 'python', '''
import pandas as pd
df = pd.DataFrame({"id": [1, 1, 2, 3, 3], "monto": [10, 10, 20, None, 30]})
exactos = df.drop_duplicates().reset_index(drop=True)
print(len(df), len(exactos), exactos["monto"].isna().sum(), int(df.duplicated().sum()))
'''),
    # ───────────────────────── S04 ─────────────────────────
    ('S04-V', 'S04', 'Regla nueva en el mini-ETL: precio menor que Bs 2,00 → rechazo «precio_bajo»', 'python', CARGAR_REF_MINI + '''
silver, rechazos = mini.transformar(mini.quitar_exactos(raw), cat)
bajos = silver[silver["precio_centavos"] < 200]
print(len(raw), len(mini.quitar_exactos(raw)), len(rechazos), len(silver), "→", len(rechazos) + len(bajos), len(silver) - len(bajos), sorted(bajos["ticket_id"]))
'''),
    ('S04-D', 'S04', 'Diagnóstico: la ecuación de conteos no cierra', 'python', '''
bronze, duplicados, rechazados, silver = 24, 2, 6, 17
print(bronze - (duplicados + rechazados + silver))
'''),
    ('S04-R1', 'S04', 'Recuperación: cuántas líneas del mini-ETL tienen cantidad fraccionaria o no numérica', 'python', CARGAR_REF_MINI + '''
silver, rechazos = mini.transformar(mini.quitar_exactos(raw), cat)
print(int(rechazos["motivos"].str.contains("unidades").sum()), sorted(rechazos.loc[rechazos["motivos"].str.contains("unidades"), "ticket_id"]))
'''),
    ('S04-R2', 'S04', 'Recuperación: regla «unidades mayores que 8» en el mini-ETL', 'python', CARGAR_REF_MINI + '''
silver, rechazos = mini.transformar(mini.quitar_exactos(raw), cat)
altos = silver[silver["unidades"] > 8]
print(len(rechazos) + len(altos), len(silver) - len(altos), sorted(altos["ticket_id"]))
'''),
    ('S04-R3', 'S04', 'Recuperación: otra ecuación que no cierra', 'python', '''
bronze, duplicados, rechazados, silver = 30, 3, 4, 24
print(bronze - (duplicados + rechazados + silver))
'''),
    # ───────────────────────── S05 ─────────────────────────
    ('S05-V', 'S05', 'Variante del ETL guiado: ticket de un cliente y un mes', 'python', CARGAR_REF_DIST + '''
e = silver[(silver["estado"] == "entregado") & (silver["cliente"] == "Farmacia Don Lucho 064") & (silver["fecha"].dt.strftime("%Y-%m") == "2026-04")]
print(round(e["monto"].sum(), 2), e["nro_pedido"].nunique(), round(e["monto"].sum() / e["nro_pedido"].nunique(), 2), len(e))
'''),
    ('S05-D', 'S05', 'Diagnóstico: contar líneas en lugar de pedidos distintos', 'python', '''
import pandas as pd
silver = pd.DataFrame({"cliente": ["A", "A", "A", "B"], "nro_pedido": ["1", "1", "2", "3"], "monto": [10, 20, 30, 40]})
g = silver.groupby("cliente").agg(pedidos_mal=("nro_pedido", "count"), pedidos_bien=("nro_pedido", "nunique"), ventas=("monto", "sum"))
print(g.to_dict("index"))
'''),
    ('S05-R1', 'S05', 'Recuperación: pedidos distintos y ventas de un cliente en un mes del ETL guiado', 'python', CARGAR_REF_DIST + '''
e = silver[(silver["estado"] == "entregado") & (silver["cliente"] == "Farmacia Don Lucho 064") & (silver["fecha"].dt.strftime("%Y-%m") == "2026-05")]
print(round(e["monto"].sum(), 2), e["nro_pedido"].nunique(), int(e["cantidad"].sum()))
'''),
    ('S05-R2', 'S05', 'Recuperación: pedidos contados como líneas con otras filas', 'python', '''
import pandas as pd
silver = pd.DataFrame({"cliente": ["X", "X", "X", "Y"], "nro_pedido": ["7", "7", "8", "9"], "monto": [5, 5, 9, 1]})
g = silver.groupby("cliente").agg(pedidos_mal=("nro_pedido", "count"), pedidos_bien=("nro_pedido", "nunique"), ventas=("monto", "sum"))
print(g.to_dict("index"))
'''),
    # ───────────────────────── S06 ─────────────────────────
    ('S06-V', 'S06', 'Regla nueva en C06: precio mayor que Bs 45,00 → rechazo «precio_alto»', 'python', CARGAR_REF_C06 + '''
silver, rechazos, gold, metricas = ref.transformar(raw, cat)
altos = silver[silver["precio_centavos"] > 4500]
nuevo_monto = int(silver.loc[(silver["estado"] == "entregado") & (silver["precio_centavos"] <= 4500), "monto_centavos"].sum())
print(metricas["rechazados"], len(rechazos) + len(altos), metricas["silver"], len(silver) - len(altos), metricas["ventas_centavos"], nuevo_monto)
'''),
    ('S06-D', 'S06', 'Diagnóstico: quitar duplicados por la clave oculta un conflicto', 'python', '''
import pandas as pd
df = pd.DataFrame({"linea_id": ["L1", "L1", "L2"], "precio_centavos": [1000, 1250, 500], "cantidad": [2, 2, 1]})
mal = df.drop_duplicates(subset=["linea_id"])
bien = df.drop_duplicates()
print(len(mal), int((mal["precio_centavos"] * mal["cantidad"]).sum()), len(bien), int(df.duplicated(subset=["linea_id"], keep=False).sum()))
'''),
    ('S06-R2', 'S06', 'Recuperación: regla «precio menor que Bs 5,00» en C06', 'python', CARGAR_REF_C06 + '''
silver, rechazos, gold, metricas = ref.transformar(raw, cat)
bajos = silver[silver["precio_centavos"] < 500]
print(metricas["rechazados"], len(rechazos) + len(bajos), metricas["silver"], len(silver) - len(bajos))
'''),
    ('S06-R1', 'S06', 'Recuperación: conteo de documentos distintos de ventas entregadas en C06', 'python', CARGAR_REF_C06 + '''
silver, rechazos, gold, metricas = ref.transformar(raw, cat)
e = silver[silver["estado"] == "entregado"]
print(e["documento"].nunique(), int(gold["documentos"].sum()), len(gold))
'''),
]


def ejecutar(raiz, tipo, contenido, id_):
    if tipo == 'sql':
        with closing(sqlite3.connect(f'file:{raiz / DB}?mode=ro', uri=True)) as c:
            return [list(f) for f in c.execute(contenido).fetchall()]
    r = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-c', contenido], capture_output=True, text=True, encoding='utf-8', cwd=raiz,
                       env={'PYTHONIOENCODING': 'utf-8', 'SYSTEMROOT': r'C:\Windows'} if sys.platform == 'win32' else {'PYTHONIOENCODING': 'utf-8'})
    assert r.returncode == 0, f'{id_}: {r.stderr[-500:]}'
    return r.stdout.rstrip('\n')


def calcular(raiz=RAIZ):
    salida = {}
    for id_, examen, titulo, tipo, contenido in CONTROLES:
        salida[id_] = {'examen': examen, 'titulo': titulo, 'tipo': tipo, 'codigo': contenido.strip('\n'), 'esperado': ejecutar(Path(raiz), tipo, contenido, id_)}
    return salida


def markdown(datos):
    L = ['# Controles de los exámenes S01–S06', '',
         'Ábrelo **solo después** de cerrar tu intento. Contiene la solución de las variantes, de los diagnósticos, de las predicciones y de las variantes de '
         'recuperación. Cada cifra se vuelve a calcular con `python herramientas/verificar_etapa2.py`.', '']
    por_examen = {}
    for id_, d in datos.items():
        por_examen.setdefault(d['examen'], []).append((id_, d))
    for ex, lista in sorted(por_examen.items()):
        L += [f'## {ex}', '']
        for id_, d in lista:
            L += [f'### {id_} · {d["titulo"]}', '', '```sql' if d['tipo'] == 'sql' else '```python', d['codigo'], '```', '', '**Resultado esperado**', '', '```']
            if d['tipo'] == 'sql':
                L += [json.dumps(f, ensure_ascii=False) for f in d['esperado']]
            else:
                L.append(d['esperado'])
            L += ['```', '']
    return '\n'.join(L)


def generar(raiz=RAIZ):
    datos = calcular(raiz)
    carpeta = Path(raiz) / '08_SOLUCIONES'
    (carpeta / 'controles_examenes.json').write_text(json.dumps({'version': '5.3-fase2-etapa3', 'controles': datos}, ensure_ascii=False, indent=1), encoding='utf-8')
    (carpeta / 'controles_examenes.md').write_text(markdown(datos), encoding='utf-8')
    return len(datos)


def comprobar(raiz=RAIZ):
    guardado = json.loads((Path(raiz) / '08_SOLUCIONES/controles_examenes.json').read_text(encoding='utf-8'))['controles']
    assert set(guardado) == {c[0] for c in CONTROLES}, 'el JSON no corresponde a las definiciones'
    for id_, examen, titulo, tipo, contenido in CONTROLES:
        nuevo = ejecutar(Path(raiz), tipo, contenido, id_)
        assert nuevo == guardado[id_]['esperado'], f'{id_}: salió {nuevo!r} y el control dice {guardado[id_]["esperado"]!r}'
    return len(CONTROLES)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--generar', action='store_true')
    ap.add_argument('--comprobar', action='store_true')
    a = ap.parse_args()
    if a.generar:
        print('controles escritos:', generar())
    elif a.comprobar:
        print('controles comprobados:', comprobar())
    else:
        raise SystemExit(__doc__)
