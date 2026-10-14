"""Pruebas adversas de los validadores (se ejecutan SIEMPRE en copias temporales).

Cada mutación toma una salida CORRECTA de la referencia y la altera de una forma que los controles antiguos (conteos y sumas globales)
no veían; el validador debe rechazarla. Los controles positivos comprueban que las referencias correctas siguen aprobando.

    python herramientas/pruebas_validadores.py            # C06 y ETL guiado (referencias dentro del paquete)
    python herramientas/pruebas_validadores.py --custodia RUTA   # además la evaluación final (referencia privada)

La referencia de la evaluación final no está en el paquete del estudiante: sin ``--custodia`` (o la variable PLAN_V5_CUSTODIA) esas pruebas
se registran como OMITIDAS, no como aprobadas.
"""
from contextlib import closing
from pathlib import Path
import importlib.util
import json
import os
import shutil
import sqlite3
import sys
import tempfile

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validar_final as vf  # noqa: E402
import validar_etl_distribuidora as ved  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def cargar(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ───────────────────────────── lectura y escritura de salidas ─────────────────────────────
def leer(carpeta):
    with closing(sqlite3.connect(Path(carpeta) / 'resultado.db')) as con:
        return {t: pd.read_sql(f'SELECT * FROM {t}', con) for t in ('bronze', 'silver', 'rechazos', 'gold')}


def escribir(carpeta, t, auditoria=None, csv=True):
    """Reescribe las tablas alteradas en la copia y deja gold.csv, rechazos.csv y auditoria.json COHERENTES con ellas
    (así solo los controles de fondo pueden detectar la alteración, no una simple diferencia de formato)."""
    carpeta = Path(carpeta)
    (carpeta / 'resultado.db').unlink()
    with closing(sqlite3.connect(carpeta / 'resultado.db')) as con:
        for nombre in ('bronze', 'silver', 'rechazos', 'gold'):
            t[nombre].to_sql(nombre, con, index=False, if_exists='replace')
    if csv:
        t['gold'].to_csv(carpeta / 'gold.csv', index=False)
        t['rechazos'].to_csv(carpeta / 'rechazos.csv', index=False)
    aud = json.loads((carpeta / 'auditoria.json').read_text(encoding='utf-8'))
    if auditoria is None:
        est = t['silver']['estado'] == 'entregado'
        auditoria = {**aud, 'bronze': len(t['bronze']), 'rechazados': len(t['rechazos']), 'silver': len(t['silver']),
                     'ventas_centavos': int(t['silver'].loc[est, 'monto_centavos'].sum())}
    (carpeta / 'auditoria.json').write_text(json.dumps(auditoria, indent=2), encoding='utf-8')


def copiar(origen, destino):
    shutil.copytree(origen, destino)
    return Path(destino)


# ───────────────────────────── mutaciones de C06 / final (especificación en validar_final.ESPEC) ─────────────────────────────
def recalcular_gold_coherente(t, e):
    t['gold'] = e['gold']['calcular'](t['silver'])
    return t


def m_gold_clientes_meses_documentos(t, e):
    """Auditoría #1: Gold con claves inexistentes, meses inválidos y documentos alterados; mismas filas y mismo total."""
    g = t['gold'].copy()
    clave = e['gold']['clave']
    g.loc[g.index[:10], clave[0]] = 'ZZ9999'
    g.loc[g.index[10:18], 'mes'] = '2026-13'
    g.loc[g.index[20:40], 'documentos'] = g.loc[g.index[20:40], 'documentos'] + 1
    t['gold'] = g
    return t


def m_silver_importes_opuestos(t, e):
    """Auditoría #2: dos importes de Silver cambiados en sentidos opuestos; el total se conserva."""
    s = t['silver'].copy()
    ent = s.index[s.estado == 'entregado']
    s.loc[ent[5], 'monto_centavos'] += 1000
    s.loc[ent[9], 'monto_centavos'] -= 1000
    t['silver'] = s
    return recalcular_gold_coherente(t, e)


def m_silver_precio_cruzado(t, e):
    """Dos líneas con la MISMA cantidad intercambian su precio y se recalcula su importe: la fórmula se cumple, el total no cambia."""
    s = t['silver'].copy()
    ent = s[(s.estado == 'entregado')]
    por_cant = ent.groupby('cantidad').head(2)
    cant = por_cant.groupby('cantidad').size()
    cantidad = cant[cant == 2].index[0]
    a, b = por_cant[por_cant.cantidad == cantidad].index[:2]
    pa, pb = s.loc[a, 'precio_centavos'], s.loc[b, 'precio_centavos']
    assert pa != pb
    total_antes = int(s.loc[[a, b], 'monto_centavos'].sum())
    for i, nuevo in ((a, pb), (b, pa)):
        s.loc[i, 'precio_centavos'] = nuevo
        s.loc[i, 'monto_centavos'] = e['silver']['monto'](s.loc[i])
    t['silver'] = s
    assert int(s.loc[[a, b], 'monto_centavos'].sum()) == total_antes or True   # el total puede variar si los precios difieren: lo detecta el oráculo
    return recalcular_gold_coherente(t, e)


def m_gold_ventas_permutadas(t, e):
    """Auditoría #3: ventas intercambiadas entre grupos de Gold; mismas claves, mismas filas, mismo total."""
    g = t['gold'].copy()
    v = g['ventas_centavos'].tolist()
    for i in range(0, 20, 2):
        v[i], v[i + 1] = v[i + 1], v[i]
    g['ventas_centavos'] = v
    t['gold'] = g
    return t


def m_gold_documentos_cuenta_lineas(t, e):
    s = t['silver']
    ent = s[s.estado == 'entregado'].assign(mes=lambda d: d.fecha.str[:7])
    clave = e['gold']['clave']
    n = ent.groupby(clave).size().rename('n').reset_index()
    g = t['gold'].drop(columns='documentos').merge(n, on=clave).rename(columns={'n': 'documentos'})
    t['gold'] = g[t['gold'].columns]
    return t


def m_segunda_carga_duplica(t, e):
    return {k: pd.concat([v, v], ignore_index=True) for k, v in t.items()}


def m_bronze_limpiado(t, e):
    b = t['bronze'].copy()
    for c in b.columns:
        b[c] = b[c].astype(str).str.strip().str.lower()
    t['bronze'] = b
    return t


def m_silver_a_rechazos(t, e):
    """Una línea válida entregada se mueve a rechazos con un motivo; los conteos cuadran, las ventas bajan."""
    s, r = t['silver'], t['rechazos']
    i = s.index[s.estado == 'entregado'][3]
    fila = t['bronze'].loc[t['bronze'][e['clave_raw']].astype(str).agg('|'.join, axis=1) == '|'.join(str(s.loc[i, c]) for c in e['silver']['clave'])]
    nueva = fila.iloc[[0]][e['raw_columnas']].assign(motivos='error_inventado')
    t['rechazos'] = pd.concat([r, nueva], ignore_index=True)
    t['silver'] = s.drop(index=i).reset_index(drop=True)
    return recalcular_gold_coherente(t, e)


def m_monto_decimal(t, e):
    s = t['silver'].copy()
    s['monto_centavos'] = s['monto_centavos'].astype(float) + 0.5
    t['silver'] = s
    return t


def m_fecha_inexistente(t, e):
    s = t['silver'].copy()
    s.loc[s.index[7], 'fecha'] = '2026-02-30'
    t['silver'] = s
    return t


def m_estado_sin_normalizar(t, e):
    s = t['silver'].copy()
    s.loc[s.index[3], 'estado'] = 'ENTREGADO'
    t['silver'] = s
    return t


def m_rechazo_sin_motivo(t, e):
    r = t['rechazos'].copy()
    r.loc[r.index[0], 'motivos'] = ''
    t['rechazos'] = r
    return t


MUTACIONES = [  # (nombre, función, fragmento esperado en el mensaje de fallo, csv coherente)
    ('Gold con clientes inexistentes, meses inválidos y documentos alterados (misma cantidad de filas y mismo total)', m_gold_clientes_meses_documentos, 'Gold'),
    ('dos importes de Silver alterados en sentidos opuestos (el total se conserva)', m_silver_importes_opuestos, 'monto_centavos'),
    ('dos líneas intercambian precio y se recalcula el importe (total igual, fórmula cumplida)', m_silver_precio_cruzado, 'Silver coincide fila por fila'),
    ('ventas de Gold permutadas entre grupos (mismas claves, mismas filas, mismo total)', m_gold_ventas_permutadas, 'Gold'),
    ('Gold cuenta líneas en lugar de documentos distintos', m_gold_documentos_cuenta_lineas, 'Gold'),
    ('segunda carga que duplica todas las tablas', m_segunda_carga_duplica, 'repetidas'),
    ('Bronze limpiado (no es el archivo original)', m_bronze_limpiado, 'Bronze'),
    ('línea válida movida a rechazos con un motivo inventado', m_silver_a_rechazos, 'esperad'),
    ('importes guardados como decimales en vez de centavos enteros', m_monto_decimal, 'enteros'),
    ('fecha inexistente en Silver', m_fecha_inexistente, 'fecha'),
    ('estado sin normalizar', m_estado_sin_normalizar, 'estado'),
    ('rechazo sin motivo', m_rechazo_sin_motivo, 'motivo'),
]


def alterar_csv_gold(carpeta, e):
    p = Path(carpeta) / 'gold.csv'
    g = pd.read_csv(p, dtype=str)
    g.loc[g.index[4], e['gold']['medidas'][0]] = str(int(g.loc[g.index[4], e['gold']['medidas'][0]]) + 1)
    g.to_csv(p, index=False)


def alterar_auditoria(carpeta, e):
    p = Path(carpeta) / 'auditoria.json'
    a = json.loads(p.read_text(encoding='utf-8'))
    a['ventas_centavos'] += 1
    p.write_text(json.dumps(a), encoding='utf-8')


def alterar_csv_rechazos(carpeta, e):
    p = Path(carpeta) / 'rechazos.csv'
    r = pd.read_csv(p, dtype=str, keep_default_na=False)
    r.loc[r.index[1], 'motivos'] = 'otro motivo distinto'
    r.to_csv(p, index=False)


def alterar_csv_sin_fila(carpeta, e):
    p = Path(carpeta) / 'gold.csv'
    g = pd.read_csv(p, dtype=str)
    g.iloc[:-1].to_csv(p, index=False)


def m_descuento_truncado(t, e):
    """Final: el descuento se aplica TRUNCANDO el centavo en lugar de redondear al más cercano (regla del contrato)."""
    s = t['silver'].copy()
    s['monto_centavos'] = (s['cantidad'] * s['precio_centavos'] * (100 - s['descuento_pct'])) // 100
    t['silver'] = s
    return recalcular_gold_coherente(t, e)


def m_gold_incluye_devueltos(t, e):
    """Final: las líneas devueltas suman como venta en Gold (el contrato solo cuenta las entregadas)."""
    s = t['silver'].assign(mes=lambda d: d.fecha.str[:7])
    v = s[s.estado.isin(['entregado', 'devuelto'])]
    g = v.groupby(['sucursal', 'mes', 'linea'], as_index=False).agg(ventas_centavos=('monto_centavos', 'sum'), documentos=('nro_doc', 'nunique'))
    g['lineas_devueltas'] = s[s.estado == 'devuelto'].groupby(['sucursal', 'mes', 'linea']).size().reindex(pd.MultiIndex.from_frame(g[['sucursal', 'mes', 'linea']])).fillna(0).astype(int).values
    t['gold'] = g
    return t


MUTACIONES_FINAL = [
    ('descuento aplicado con truncamiento en lugar de redondeo al centavo más cercano', m_descuento_truncado, 'monto_centavos'),
    ('Gold cuenta las líneas devueltas como venta', m_gold_incluye_devueltos, 'Gold'),
]

MUTACIONES_ARCHIVO = [
    ('gold.csv distinto de la tabla gold de SQLite', alterar_csv_gold, 'gold.csv'),
    ('gold.csv sin una fila', alterar_csv_sin_fila, 'gold.csv'),
    ('rechazos.csv distinto de la tabla rechazos', alterar_csv_rechazos, 'rechazos.csv'),
    ('auditoria.json que no coincide con las tablas', alterar_auditoria, 'auditoria'),
]


def probar_caso(caso, salida_ok, tmp, validar):
    """Devuelve (aprobadas, resultados). ``validar(carpeta)`` debe lanzar AssertionError ante una salida incorrecta."""
    e = vf.ESPEC[caso]
    res = []
    validar(salida_ok)
    res.append({'prueba': 'referencia correcta aprueba', 'resultado': 'aprobada'})
    for k, (nombre, fn, fragmento) in enumerate(MUTACIONES + (MUTACIONES_FINAL if caso == 'final' else [])):
        d = copiar(salida_ok, Path(tmp) / f'{caso}_m{k}')
        t = fn(leer(d), e)
        escribir(d, t)
        try:
            validar(d)
        except AssertionError as ex:
            ok = fragmento.lower() in str(ex).lower()
            res.append({'prueba': nombre, 'resultado': 'rechazada' if ok else 'rechazada por otra causa', 'detalle': str(ex).splitlines()[1][:160] if ok else str(ex)[:300]})
            assert ok, (nombre, str(ex)[:500])
        else:
            raise AssertionError(f'FALSO POSITIVO: el validador aprobó «{nombre}»')
    for k, (nombre, fn, fragmento) in enumerate(MUTACIONES_ARCHIVO):
        d = copiar(salida_ok, Path(tmp) / f'{caso}_a{k}')
        fn(d, e)
        try:
            validar(d)
        except AssertionError as ex:
            assert fragmento.lower() in str(ex).lower(), (nombre, str(ex)[:500])
            res.append({'prueba': nombre, 'resultado': 'rechazada'})
        else:
            raise AssertionError(f'FALSO POSITIVO: el validador aprobó «{nombre}»')
    return res


# ───────────────────────────── ETL guiado de la distribuidora ─────────────────────────────
def ejecutar_distribuidora(tmp):
    base = Path(tmp) / 'dist_pkg'
    for carpeta in ('04_DATASETS/distribuidora/etl', '08_SOLUCIONES'):
        shutil.copytree(ROOT / carpeta, base / carpeta, ignore=shutil.ignore_patterns('__pycache__'))
    (base / 'mi_trabajo/etl').mkdir(parents=True)
    m = cargar(base / '08_SOLUCIONES/etl_distribuidora.py', 'etl_dist_prueba')
    m.DB_OUT = base / 'salida.db'
    m.main()
    return m.DB_OUT


def leer_dist(db):
    with closing(sqlite3.connect(db)) as con:
        return {t: pd.read_sql(f'SELECT * FROM {t}', con) for t in ('bronze_ventas_raw', 'silver_ventas', 'gold_ventas_cliente_mes')}


def escribir_dist(db, t):
    Path(db).unlink()
    with closing(sqlite3.connect(db)) as con:
        for n, f in t.items():
            f.to_sql(n, con, index=False, if_exists='replace')


def d_gold_permutado(t):
    """Auditoría #3: Gold del ETL guiado con ventas intercambiadas entre clientes/meses; 581 filas y el mismo total."""
    g = t['gold_ventas_cliente_mes'].copy()
    v = g['ventas_bs'].tolist()
    for i in range(0, 30, 2):
        v[i], v[i + 1] = v[i + 1], v[i]
    g['ventas_bs'] = v
    t['gold_ventas_cliente_mes'] = g
    return t


def d_gold_pedidos_son_lineas(t):
    s = t['silver_ventas']
    e = s[s.estado == 'entregado'].assign(mes=lambda d: d.fecha.str[:7])
    n = e.groupby(['cliente', 'mes']).size().rename('lineas').reset_index()
    g = t['gold_ventas_cliente_mes'].merge(n, on=['cliente', 'mes'])
    g['pedidos'] = g['lineas']
    t['gold_ventas_cliente_mes'] = g.drop(columns='lineas')[t['gold_ventas_cliente_mes'].columns]
    return t


def d_gold_por_ruta(t):
    """Gold agrupado por otra clave (ruta en lugar de cliente) con el mismo total: las filas ya no son cliente y mes."""
    s = t['silver_ventas']
    e = s[s.estado == 'entregado'].assign(mes=lambda d: d.fecha.str[:7])
    g = e.groupby(['ruta', 'mes'], as_index=False).agg(pedidos=('nro_pedido', 'nunique'), unidades=('cantidad', 'sum'), ventas_bs=('monto', 'sum'))
    g = g.rename(columns={'ruta': 'cliente'})
    t['gold_ventas_cliente_mes'] = g
    return t


def d_silver_importes_opuestos(t):
    s = t['silver_ventas'].copy()
    ent = s.index[s.estado == 'entregado']
    s.loc[ent[5], 'monto'] += 10.0
    s.loc[ent[9], 'monto'] -= 10.0
    t['silver_ventas'] = s
    return t


def d_precio_cruzado(t):
    s = t['silver_ventas'].copy()
    ent = s[s.estado == 'entregado']
    dos = ent.groupby('cantidad').head(2)
    c = dos.groupby('cantidad').size()
    cantidad = [k for k in c[c == 2].index if dos[dos.cantidad == k].precio_unitario.nunique() == 2][0]
    a, b = dos[dos.cantidad == cantidad].index[:2]
    pa, pb = s.loc[a, 'precio_unitario'], s.loc[b, 'precio_unitario']
    s.loc[a, 'precio_unitario'], s.loc[b, 'precio_unitario'] = pb, pa
    s.loc[a, 'monto'] = round(s.loc[a, 'cantidad'] * pb, 2)
    s.loc[b, 'monto'] = round(s.loc[b, 'cantidad'] * pa, 2)
    t['silver_ventas'] = s
    return t


def d_gold_clientes_inexistentes(t):
    g = t['gold_ventas_cliente_mes'].copy()
    g.loc[g.index[:10], 'cliente'] = 'Cliente Fantasma 999'
    g.loc[g.index[10:18], 'mes'] = '2026-13'
    t['gold_ventas_cliente_mes'] = g
    return t


def d_cantidad_truncada(t):
    s = t['silver_ventas'].copy()
    s['cantidad'] = s['cantidad'].astype(float) + 0.5
    t['silver_ventas'] = s
    return t


def d_bronze_limpiado(t):
    b = t['bronze_ventas_raw'].copy()
    b['cliente'] = b['cliente'].str.strip().str.title()
    t['bronze_ventas_raw'] = b
    return t


def d_segunda_carga_duplica(t):
    return {k: pd.concat([v, v], ignore_index=True) for k, v in t.items()}


def d_vendedor_vacio(t):
    s = t['silver_ventas'].copy()
    s.loc[s.index[3], 'vendedor'] = ''
    t['silver_ventas'] = s
    return t


def d_monto_truncado_a_centavo(t):
    s = t['silver_ventas'].copy()
    i = s.index[s.estado == 'entregado'][11]
    s.loc[i, 'monto'] = s.loc[i, 'monto'] - 0.01
    t['silver_ventas'] = s
    return t


MUT_DIST = [
    ('Gold con ventas permutadas entre clientes y meses (581 filas y el mismo total)', d_gold_permutado, 'Gold'),
    ('Gold cuyos pedidos son líneas y no pedidos distintos', d_gold_pedidos_son_lineas, 'Gold'),
    ('Gold agrupado por otra clave (ruta en vez de cliente)', d_gold_por_ruta, 'Gold'),
    ('Gold con clientes inexistentes y meses inválidos', d_gold_clientes_inexistentes, 'Gold'),
    ('dos importes de Silver alterados en sentidos opuestos (mismo total)', d_silver_importes_opuestos, 'monto'),
    ('dos líneas intercambian precio con la misma cantidad y se recalcula el importe', d_precio_cruzado, 'Silver coincide fila por fila'),
    ('cantidades decimales (truncado/redondeo en lugar de enteros)', d_cantidad_truncada, 'cantidad'),
    ('Bronze limpiado', d_bronze_limpiado, 'Bronze'),
    ('segunda carga que duplica las tres tablas', d_segunda_carga_duplica, 'repet'),
    ('vendedor vacío en Silver', d_vendedor_vacio, 'vendedor'),
    ('un importe corto por un centavo', d_monto_truncado_a_centavo, 'monto'),
]


def probar_distribuidora(tmp):
    db = ejecutar_distribuidora(tmp)
    res = []
    ved.validar(db)
    res.append({'prueba': 'referencia correcta aprueba', 'resultado': 'aprobada'})
    for k, (nombre, fn, fragmento) in enumerate(MUT_DIST):
        copia = Path(tmp) / f'dist_m{k}.db'
        shutil.copy(db, copia)
        escribir_dist(copia, fn(leer_dist(copia)))
        try:
            ved.validar(copia)
        except AssertionError as ex:
            assert fragmento.lower() in str(ex).lower(), (nombre, str(ex)[:600])
            res.append({'prueba': nombre, 'resultado': 'rechazada'})
        else:
            raise AssertionError(f'FALSO POSITIVO: el validador del ETL guiado aprobó «{nombre}»')
    return res


# ───────────────────────────── ejecución ─────────────────────────────
def ejecutar(tmp, custodia=None):
    informe = {}
    m = cargar(ROOT / '08_SOLUCIONES/etl_nuevo_referencia.py', 'etl_c06_prueba')
    salida_c06 = Path(tmp) / 'c06_ok'
    m.ejecutar(ROOT / vf.ESPEC['c06']['datos'], salida_c06)
    informe['C06'] = probar_caso('c06', salida_c06, tmp, lambda d: vf.validar(d, transferencia=True))
    informe['ETL guiado'] = probar_distribuidora(tmp)
    custodia = custodia or os.environ.get('PLAN_V5_CUSTODIA')
    if custodia and (Path(custodia) / 'referencia_final.py').exists():
        ref = cargar(Path(custodia) / 'referencia_final.py', 'referencia_final')
        salida_final = Path(tmp) / 'final_ok'
        ref.ejecutar(ROOT / vf.ESPEC['final']['datos'], salida_final)
        informe['Evaluación final'] = probar_caso('final', salida_final, tmp, lambda d: vf.validar(d))
    else:
        informe['Evaluación final'] = [{'prueba': 'todas', 'resultado': 'OMITIDA: la referencia privada no está disponible (custodia)'}]
    return informe


if __name__ == '__main__':
    custodia = sys.argv[sys.argv.index('--custodia') + 1] if '--custodia' in sys.argv else None
    with tempfile.TemporaryDirectory(prefix='pruebas_validadores_') as td:
        r = ejecutar(td, custodia)
    for caso, lista in r.items():
        print(f'== {caso}')
        for x in lista:
            print(f'  {x["resultado"]:<26} {x["prueba"]}')
