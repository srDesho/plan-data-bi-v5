"""Corrige DESPUÉS del intento. No muestra código ni valores esperados. Comprueba filas, claves, agrupaciones, importes y salidas.

Uso:
    python herramientas/validar_final.py SALIDA                  # evaluación final (09_EVALUACION_FINAL)
    python herramientas/validar_final.py SALIDA --transferencia  # caso C06 (04_DATASETS/transferencia)

SALIDA es la carpeta con resultado.db, rechazos.csv, gold.csv y auditoria.json.
El corrector acumula todos los fallos (no se detiene en el primero). Una prueba numérica no acredita autonomía: falta la defensa.
"""
from contextlib import closing
from pathlib import Path
import hashlib
import json
import re
import sqlite3
import sys
from datetime import date

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validacion_comun import Informe, Oraculo, canon  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


# ───────────────────────────── especificaciones de contrato ─────────────────────────────
def monto_c06(f):
    return f['cantidad'] * f['precio_centavos']


def monto_final(f):
    """cantidad × precio × (100 − descuento) / 100, al centavo más cercano (mitad hacia arriba), solo con enteros."""
    return (f['cantidad'] * f['precio_centavos'] * (100 - f['descuento_pct']) + 50) // 100


def gold_c06(silver):
    e = silver[silver.estado == 'entregado']
    e = e.assign(mes=e.fecha.str[:7])
    return e.groupby(['cliente_id', 'mes'], as_index=False).agg(ventas_centavos=('monto_centavos', 'sum'), documentos=('documento', 'nunique'))


def gold_final(silver):
    s = silver.assign(mes=silver.fecha.str[:7])
    e = s[s.estado == 'entregado']
    g = e.groupby(['sucursal', 'mes', 'linea'], as_index=False).agg(ventas_centavos=('monto_centavos', 'sum'), documentos=('nro_doc', 'nunique'))
    d = s[s.estado == 'devuelto'].groupby(['sucursal', 'mes', 'linea']).size().rename('lineas_devueltas').reset_index()
    g = g.merge(d, on=['sucursal', 'mes', 'linea'], how='left')
    g['lineas_devueltas'] = g['lineas_devueltas'].fillna(0).astype(int)
    return g


ESPEC = {
    'c06': {
        'titulo': 'C06 · transferencia',
        'datos': '04_DATASETS/transferencia', 'raw': 'transacciones_raw.csv', 'sep': ';', 'catalogo': 'catalogo.csv',
        'huellas': '08_SOLUCIONES/huellas_c06.json',
        'raw_columnas': ['linea_id', 'documento', 'fecha', 'cliente_id', 'ruta', 'sku', 'cantidad', 'estado', 'precio_unitario'],
        'clave_raw': ['linea_id'],
        'silver': {'clave': ['linea_id'],
                   'columnas': ['linea_id', 'documento', 'fecha', 'cliente_id', 'ruta', 'sku', 'cantidad', 'estado', 'precio_centavos', 'monto_centavos'],
                   'enteros': ['cantidad', 'precio_centavos', 'monto_centavos'],
                   'patrones': {'fecha': r'\d{4}-\d{2}-\d{2}', 'ruta': r'[A-Z0-9]+', 'cliente_id': r'\S+'},
                   'dominios': {'estado': {'entregado', 'anulado'}},
                   'unico_por_documento': ['fecha'], 'documento': 'documento', 'monto': monto_c06, 'sin_negativos': ['precio_centavos', 'monto_centavos']},
        'gold': {'clave': ['cliente_id', 'mes'], 'medidas': ['ventas_centavos', 'documentos'], 'calcular': gold_c06},
        'rechazos_clave': ['linea_id'],
        'auditoria': ['bronze', 'duplicados_exactos', 'rechazados', 'silver', 'ventas_centavos'],
    },
    'final': {
        'titulo': 'Evaluación final · despachos',
        'datos': '09_EVALUACION_FINAL/datos', 'raw': 'despachos_raw.csv', 'sep': '|', 'catalogo': 'articulos.csv',
        'huellas': '09_EVALUACION_FINAL/verificacion/huellas_final.json',
        'raw_columnas': ['nro_doc', 'item', 'fecha_despacho', 'sucursal', 'cod_cliente', 'cod_art', 'cantidad', 'precio_unitario', 'descuento_pct', 'estado'],
        'clave_raw': ['nro_doc', 'item'],
        'silver': {'clave': ['nro_doc', 'item'],
                   'columnas': ['nro_doc', 'item', 'fecha', 'sucursal', 'cod_cliente', 'cod_art', 'cantidad', 'precio_centavos', 'descuento_pct', 'estado',
                                'monto_centavos', 'linea'],
                   'enteros': ['item', 'cantidad', 'precio_centavos', 'descuento_pct', 'monto_centavos'],
                   'patrones': {'fecha': r'\d{4}-\d{2}-\d{2}', 'sucursal': r'[A-Z]{3}', 'cod_art': r'[A-Z]{2}-\d{3}', 'cod_cliente': r'\S+'},
                   'dominios': {'estado': {'entregado', 'anulado', 'devuelto'}, 'sucursal': {'SCZ', 'LPZ', 'CBB'}},
                   'unico_por_documento': ['fecha', 'sucursal'], 'documento': 'nro_doc', 'monto': monto_final,
                   'sin_negativos': ['precio_centavos', 'monto_centavos'], 'rangos': {'descuento_pct': (0, 100)}},
        'gold': {'clave': ['sucursal', 'mes', 'linea'], 'medidas': ['ventas_centavos', 'documentos', 'lineas_devueltas'], 'calcular': gold_final},
        'rechazos_clave': ['nro_doc', 'item'],
        'auditoria': ['bronze', 'duplicados_exactos', 'rechazados', 'silver', 'ventas_centavos'],
    },
}


# ───────────────────────────── utilidades ─────────────────────────────
def sha256_archivo(ruta):
    """SHA-256 del contenido con fin de línea normalizado (un checkout con CRLF no debe parecer una modificación)."""
    return hashlib.sha256(Path(ruta).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def tabla(con, nombre):
    return pd.read_sql(f'SELECT * FROM {nombre}', con)


def tiene_columnas(frame, columnas):
    return [c for c in columnas if c not in frame.columns]


def llave(frame, columnas):
    return pd.Series(['|'.join(canon(v) for v in fila) for fila in frame[columnas].itertuples(index=False)], index=frame.index, dtype=object)


def _mapa(frame, clave, cols):
    claves = llave(frame, clave).tolist()
    valores = [tuple(canon(v) for v in fila) for fila in frame[cols].itertuples(index=False)]
    return dict(zip(claves, valores))


def iguales(a, b, clave):
    """Compara dos DataFrames por clave y por las columnas comunes (valores canónicos). Devuelve diferencias legibles (máx. 15)."""
    cols = [c for c in a.columns if c in b.columns]
    ma, mb = _mapa(a, clave, cols), _mapa(b, clave, cols)
    dif = [f'falta {k}' for k in sorted(set(mb) - set(ma))[:5]] + [f'sobra {k}' for k in sorted(set(ma) - set(mb))[:5]]
    dif += [f'distinta {k}' for k in sorted(set(ma) & set(mb)) if ma[k] != mb[k]][:5]
    return dif


# ───────────────────────────── validación ─────────────────────────────
def validar(salida, transferencia=False, caso=None, huellas=None, entrada=None):
    caso = caso or ('c06' if transferencia else 'final')
    e = ESPEC[caso]
    salida = Path(salida).resolve()
    inf = Informe(e['titulo'])
    datos = Path(entrada) if entrada else ROOT / e['datos']
    ruta_h = Path(huellas) if huellas else ROOT / e['huellas']
    if not ruta_h.exists():
        raise FileNotFoundError(f'Falta el archivo de huellas del oráculo: {ruta_h}')
    oraculo = Oraculo.desde_archivo(ruta_h)

    # 0 · datos de entrada intactos
    for nombre, h in oraculo.datos.get('raw_sha256', {}).items():
        inf.comprobar(sha256_archivo(datos / nombre) == h, f'datos de entrada {nombre} sin modificar',
                      'el archivo de entrada no coincide con el original; vuelve a copiarlo del paquete')
    # 1 · archivos de salida
    for nombre in ('resultado.db', 'rechazos.csv', 'gold.csv', 'auditoria.json'):
        if not inf.comprobar((salida / nombre).exists(), f'existe {nombre}', f'falta {nombre} en {salida}'):
            return inf.cerrar()
    raw = pd.read_csv(datos / e['raw'], sep=e['sep'], dtype=str, keep_default_na=False)
    n_unicas = len(raw.drop_duplicates())
    with closing(sqlite3.connect((salida / 'resultado.db').as_uri() + '?mode=ro', uri=True)) as con:
        inf.comprobar(con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'SQLite íntegra')
        presentes = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        faltan = [t for t in ('bronze', 'silver', 'rechazos', 'gold') if t not in presentes]
        if not inf.comprobar(not faltan, 'tablas bronze, silver, rechazos y gold', f'faltan {faltan}'):
            return inf.cerrar()
        bronze, silver, rechazos, gold = (tabla(con, t) for t in ('bronze', 'silver', 'rechazos', 'gold'))
        tipos_silver = {r[1]: r[2].upper() for r in con.execute('PRAGMA table_info(silver)')}
        no_entero = {}
        for c in e['silver']['enteros']:
            if c in silver.columns:
                n = con.execute(f"SELECT COUNT(*) FROM silver WHERE typeof({c}) <> 'integer'").fetchone()[0]
                if n:
                    no_entero[c] = n

    # 2 · Bronze = archivo original, sin tocar
    cols_raw = e['raw_columnas']
    f = tiene_columnas(bronze, cols_raw)
    bronze_ok = inf.comprobar(not f, 'Bronze conserva las columnas del origen', f'faltan {f}')
    if bronze_ok:
        inf.comprobar(len(bronze) == len(raw), 'Bronze tiene todas las filas del origen', f'{len(bronze)} filas en Bronze y {len(raw)} en el archivo')
        a = sorted(map(tuple, bronze[cols_raw].astype(str).values.tolist()))
        b = sorted(map(tuple, raw[cols_raw].values.tolist()))
        inf.comprobar(a == b, 'Bronze es idéntico al origen (texto exacto, sin limpiar)', 'alguna fila de Bronze fue modificada respecto al archivo')

    # 3 · Silver: contrato y reglas fila por fila
    s = e['silver']
    f = tiene_columnas(silver, s['columnas'])
    if not inf.comprobar(not f, 'Silver tiene las columnas del contrato', f'faltan {f}'):
        return inf.cerrar()
    inf.comprobar(not silver.duplicated(s['clave']).any(), f'Silver sin claves repetidas {s["clave"]}')
    inf.comprobar(not no_entero, 'Silver: cantidades y dinero son enteros (centavos)', f'columnas con valores no enteros: {no_entero}')
    sin_nulos = silver[s['columnas']].isna().sum()
    inf.comprobar(sin_nulos.sum() == 0, 'Silver sin valores vacíos en el contrato', f'{ {k: int(v) for k, v in sin_nulos.items() if v} }')
    for col, patron in s['patrones'].items():
        malas = ~silver[col].astype(str).str.fullmatch(patron)
        inf.comprobar(not malas.any(), f'Silver.{col} con el formato del contrato', f'{int(malas.sum())} filas, p. ej. {llave(silver[malas], s["clave"]).head(3).tolist()}')
    for col, dom in s['dominios'].items():
        malas = ~silver[col].isin(dom)
        inf.comprobar(not malas.any(), f'Silver.{col} dentro del dominio {sorted(dom)}', f'{int(malas.sum())} filas fuera del dominio')
    fechas_validas = []
    for v in silver['fecha'].astype(str):
        try:
            date.fromisoformat(v)
            fechas_validas.append(True)
        except ValueError:
            fechas_validas.append(False)
    inf.comprobar(all(fechas_validas), 'Silver.fecha es una fecha real', f'{fechas_validas.count(False)} fechas inexistentes')
    if not no_entero:
        inf.comprobar((silver['cantidad'] > 0).all(), 'Silver: cantidad entera positiva')
        for col in s['sin_negativos']:
            inf.comprobar((silver[col] >= 0).all(), f'Silver.{col} no negativo')
        for col, (lo, hi) in s.get('rangos', {}).items():
            inf.comprobar(silver[col].between(lo, hi).all(), f'Silver.{col} entre {lo} y {hi}')
        esperado = silver.apply(s['monto'], axis=1)
        malos = silver[esperado != silver['monto_centavos']]
        inf.comprobar(malos.empty, 'Silver.monto_centavos = regla del contrato en cada fila',
                      f'{len(malos)} filas con importe distinto, p. ej. {llave(malos, s["clave"]).head(3).tolist()}')
    for col in s['unico_por_documento']:
        inf.comprobar(silver.groupby(s['documento'])[col].nunique().max() == 1, f'cada documento tiene un solo valor de {col}')
    inf.diferencias('Silver coincide fila por fila con el resultado esperado', oraculo.comparar('silver', silver[s['columnas']]))

    # 4 · rechazos trazables y ecuación de conteos
    rc = e['rechazos_clave']
    f = tiene_columnas(rechazos, rc + ['motivos'])
    if inf.comprobar(not f, 'rechazos tiene la clave y la columna motivos', f'faltan {f}'):
        inf.comprobar(not (rechazos['motivos'].isna() | rechazos['motivos'].astype(str).str.strip().eq('')).any(), 'todo rechazo tiene motivo')
        k_rech, k_sil = set(llave(rechazos, rc)), set(llave(silver, rc))
        inf.comprobar(not (k_rech & k_sil), 'ninguna línea está a la vez en Silver y en rechazos')
        inf.comprobar(not rechazos.duplicated(rc).any(), 'rechazos sin claves repetidas')
        if bronze_ok:
            k_bronze = set(llave(bronze, e['clave_raw']))
            inf.comprobar(k_rech <= k_bronze, 'cada rechazo viene de una fila de Bronze')
            f = tiene_columnas(rechazos, cols_raw)
            if inf.comprobar(not f, 'rechazos conserva la fila original (todas las columnas del origen)', f'faltan {f}'):
                originales = set(map(tuple, raw[cols_raw].values.tolist()))
                traza = [tuple(r) in originales for r in rechazos[cols_raw].astype(str).values.tolist()]
                inf.comprobar(all(traza), 'cada rechazo coincide con su fila original', f'{traza.count(False)} rechazos distintos de su fila de origen')
        inf.diferencias('las líneas rechazadas son las esperadas', oraculo.comparar('rechazos', rechazos[rc]))
    n_dup = len(raw) - n_unicas
    inf.comprobar(len(bronze) == n_dup + len(rechazos) + len(silver), 'Bronze = duplicados exactos + rechazos + Silver',
                  f'{len(bronze)} ≠ {n_dup} + {len(rechazos)} + {len(silver)}')

    # 5 · Gold: claves, agrupaciones y cifras recalculadas desde la propia Silver y contra el esperado
    g = e['gold']
    f = tiene_columnas(gold, g['clave'] + g['medidas'])
    if inf.comprobar(not f, 'Gold tiene las columnas del contrato', f'faltan {f}'):
        inf.comprobar(not gold.duplicated(g['clave']).any(), f'Gold sin claves repetidas {g["clave"]}')
        inf.comprobar(gold['mes'].astype(str).str.fullmatch(r'\d{4}-(0[1-9]|1[0-2])').all(), 'Gold.mes es AAAA-MM válido')
        claves_silver = set(llave(g['calcular'](silver), g['clave']))
        inf.comprobar(set(llave(gold, g['clave'])) <= claves_silver, 'toda clave de Gold existe en Silver (clientes, meses y grupos reales)',
                      f'claves inexistentes, p. ej. {sorted(set(llave(gold, g["clave"])) - claves_silver)[:3]}')
        dif = iguales(gold[g['clave'] + g['medidas']], g['calcular'](silver)[g['clave'] + g['medidas']], g['clave'])
        inf.comprobar(not dif, 'Gold = agrupación de tu propia Silver (ventas, documentos distintos y demás medidas por grupo)', '; '.join(dif))
        inf.diferencias('Gold coincide fila por fila con el resultado esperado', oraculo.comparar('gold', gold[g['clave'] + g['medidas']]))
        inf.comprobar(int(gold['ventas_centavos'].sum()) == int(silver.loc[silver.estado == 'entregado', 'monto_centavos'].sum()),
                      'suma de ventas de Gold = ventas entregadas de Silver')

    # 6 · salidas CSV iguales a las tablas de SQLite
    gcsv = pd.read_csv(salida / 'gold.csv', dtype=str, keep_default_na=False)
    f = tiene_columnas(gcsv, g['clave'] + g['medidas'])
    if inf.comprobar(not f, 'gold.csv tiene las columnas del contrato', f'faltan {f}'):
        inf.comprobar(not iguales(gcsv[g['clave'] + g['medidas']], gold[g['clave'] + g['medidas']], g['clave']), 'gold.csv coincide con la tabla gold de SQLite')
    rcsv = pd.read_csv(salida / 'rechazos.csv', dtype=str, keep_default_na=False)
    f = tiene_columnas(rcsv, rc + ['motivos'])
    if inf.comprobar(not f, 'rechazos.csv tiene la clave y motivos', f'faltan {f}'):
        inf.comprobar(not iguales(rcsv[rc + ['motivos']], rechazos[rc + ['motivos']], rc), 'rechazos.csv coincide con la tabla rechazos de SQLite')

    # 7 · auditoría
    try:
        aud = json.loads((salida / 'auditoria.json').read_text(encoding='utf-8'))
    except ValueError:
        aud = {}
    inf.comprobar(all(k in aud for k in e['auditoria']), 'auditoria.json tiene todas las claves', f'faltan {[k for k in e["auditoria"] if k not in aud]}')
    if all(k in aud for k in e['auditoria']):
        reales = {'bronze': len(bronze), 'duplicados_exactos': n_dup, 'rechazados': len(rechazos), 'silver': len(silver),
                  'ventas_centavos': int(silver.loc[silver.estado == 'entregado', 'monto_centavos'].sum())}
        inf.comprobar(all(aud[k] == reales[k] for k in e['auditoria']), 'auditoria.json coincide con las tablas de SQLite',
                      f'distintas: {[k for k in e["auditoria"] if aud[k] != reales[k]]}')
        for k in e['auditoria']:
            inf.comprobar(oraculo.escalar_ok(k, aud[k]), f'auditoría.{k} es el valor esperado')
    return inf.cerrar()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    argumentos = sys.argv[1:]
    print('OK', validar(argumentos[0], transferencia='--transferencia' in argumentos))
