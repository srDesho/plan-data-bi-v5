"""Construye los archivos de huellas (oráculos) de los validadores a partir de una salida de REFERENCIA ya comprobada.

    python herramientas/construir_huellas.py c06            # 08_SOLUCIONES/huellas_c06.json (ejecuta la referencia de C06 en una carpeta temporal)
    python herramientas/construir_huellas.py distribuidora  # 08_SOLUCIONES/huellas_etl_distribuidora.json
    python herramientas/construir_huellas.py final --referencia SALIDA_REF [--datos DIR] [--destino ARCHIVO]
        # SALIDA_REF: carpeta con resultado.db generada por la referencia privada de la evaluación final (custodia)

Una huella es sha256(sal, clave, fila). El archivo permite decir qué filas coinciden y cuáles no, sin publicar los valores esperados.
Esto NO es custodia: ver el aviso en validacion_comun.py y en 09_EVALUACION_FINAL/ENUNCIADO.md.
"""
from contextlib import closing
from pathlib import Path
import argparse
import importlib.util
import json
import shutil
import sqlite3
import sys
import tempfile

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validacion_comun import Oraculo, a_centavos  # noqa: E402
import validar_final as vf  # noqa: E402
import validar_etl_distribuidora as ved  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def cargar(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def tablas_db(db):
    with closing(sqlite3.connect(db)) as con:
        return {t: pd.read_sql(f'SELECT * FROM {t}', con) for t in [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]}


def oraculo_validar_final(caso, salida, datos, sal):
    e = vf.ESPEC[caso]
    t = tablas_db(Path(salida) / 'resultado.db')
    aud = json.loads((Path(salida) / 'auditoria.json').read_text(encoding='utf-8'))
    s, g = e['silver'], e['gold']
    esp = {'silver': {'clave': s['clave'], 'columnas': s['columnas']}, 'gold': {'clave': g['clave'], 'columnas': g['clave'] + g['medidas']},
           'rechazos': {'clave': e['rechazos_clave'], 'columnas': []}}
    o = Oraculo.desde_tablas(sal, {k: aud[k] for k in e['auditoria']},
                             {'silver': t['silver'][s['columnas']], 'gold': t['gold'][g['clave'] + g['medidas']], 'rechazos': t['rechazos'][e['rechazos_clave']]},
                             esp, extra={'raw_sha256': {n: vf.sha256_archivo(Path(datos) / n) for n in (e['raw'], e['catalogo'])}})
    return o, t, aud


def construir_c06(destino=None):
    e = vf.ESPEC['c06']
    with tempfile.TemporaryDirectory(prefix='huellas_c06_') as td:
        m = cargar(ROOT / '08_SOLUCIONES/etl_nuevo_referencia.py', 'etl_c06_ref')
        m.ejecutar(ROOT / e['datos'], Path(td))
        o, t, aud = oraculo_validar_final('c06', td, ROOT / e['datos'], 'plan-v5-c06')
    # control independiente: la Silver esperada publicada en la versión anterior (con su cálculo propio) y Gold recalculado de ella
    previa = ROOT / '08_SOLUCIONES/silver_transferencia_esperada.csv'
    if previa.exists():
        ant = pd.read_csv(previa, dtype=str, keep_default_na=False)
        ant['monto_centavos'] = ant['cantidad'].astype(int) * ant['precio_centavos'].astype(int)
        cols = e['silver']['columnas']
        dif = o.comparar('silver', ant[cols])
        assert not any(dif.values()), ('La referencia difiere de la Silver esperada independiente', {k: v[:3] for k, v in dif.items()})
        for c in ('cantidad', 'precio_centavos', 'monto_centavos'):
            ant[c] = ant[c].astype(int)
        dif = o.comparar('gold', e['gold']['calcular'](ant))
        assert not any(dif.values()), ('Gold recalculado desde la Silver independiente no coincide', {k: v[:3] for k, v in dif.items()})
    o.guardar(destino or ROOT / e['huellas'])
    return {k: len(v['filas']) for k, v in o.datos['tablas'].items()}, aud


def construir_final(referencia, datos, destino):
    o, t, aud = oraculo_validar_final('final', referencia, datos, 'plan-v5-final-2026')
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    o.guardar(destino)
    return {k: len(v['filas']) for k, v in o.datos['tablas'].items()}, aud


def construir_distribuidora(destino=None):
    spec = ved.ESPEC
    with tempfile.TemporaryDirectory(prefix='huellas_dist_') as td:
        base = Path(td) / 'pkg'
        for carpeta in ('04_DATASETS/distribuidora/etl', '08_SOLUCIONES'):
            shutil.copytree(ROOT / carpeta, base / carpeta, ignore=shutil.ignore_patterns('__pycache__'))
        (base / 'mi_trabajo/etl').mkdir(parents=True)
        m = cargar(base / '08_SOLUCIONES/etl_distribuidora.py', 'etl_dist_ref')
        m.DB_OUT = base / 'salida.db'
        m.main()
        t = tablas_db(m.DB_OUT)
    silver = ved.preparar_silver(t['silver_ventas'])
    gold = ved.preparar_gold(t['gold_ventas_cliente_mes'])
    esc = {'bronze': len(t['bronze_ventas_raw']), 'silver': len(silver), 'pedidos': int(silver.nro_pedido.nunique()), 'clientes': int(silver.cliente.nunique()),
           'gold_filas': len(gold), 'ventas_centavos': int(silver.loc[silver.estado == 'entregado', 'monto_centavos'].sum())}
    # control independiente: recalcular Gold desde la Silver de referencia (agrupación propia del validador)
    dif = ved.recalcular_gold(silver)[spec['gold']['clave'] + spec['gold']['medidas']]
    ref = gold[spec['gold']['clave'] + spec['gold']['medidas']]
    assert vf.iguales(dif, ref, spec['gold']['clave']) == [], 'El Gold de referencia no coincide con su propia Silver'
    o = Oraculo.desde_tablas('plan-v5-distribuidora', esc, {'silver': silver[spec['silver']['clave'] + spec['silver']['columnas']],
                                                         'gold': gold[spec['gold']['clave'] + spec['gold']['medidas']]},
                             {'silver': {'clave': spec['silver']['clave'], 'columnas': spec['silver']['columnas']},
                              'gold': {'clave': spec['gold']['clave'], 'columnas': spec['gold']['medidas']}},
                             extra={'raw_sha256': {n: vf.sha256_archivo(ROOT / '04_DATASETS/distribuidora/etl' / n) for n in ('ventas_erp_raw.csv', 'vendedores_por_ruta.csv')}})
    o.guardar(destino or ROOT / spec['huellas'])
    return {k: len(v['filas']) for k, v in o.datos['tablas'].items()}, esc


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('caso', choices=['c06', 'distribuidora', 'final'])
    ap.add_argument('--referencia')
    ap.add_argument('--datos', default=str(ROOT / '09_EVALUACION_FINAL/datos'))
    ap.add_argument('--destino')
    a = ap.parse_args()
    if a.caso == 'c06':
        print(construir_c06(a.destino))
    elif a.caso == 'distribuidora':
        print(construir_distribuidora(a.destino))
    else:
        if not a.referencia:
            raise SystemExit('final necesita --referencia SALIDA_REF')
        print(construir_final(a.referencia, a.datos, a.destino or ROOT / vf.ESPEC['final']['huellas']))
