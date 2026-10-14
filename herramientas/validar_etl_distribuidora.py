"""Corrige el ETL guiado de la distribuidora DESPUÉS del intento. Uso: python herramientas/validar_etl_distribuidora.py ruta/etl_salida.db

Comprueba filas y agrupaciones, no solo conteos y sumas globales:
  · Bronze idéntico al archivo de origen (texto exacto).
  · Silver fila por fila (pedido+producto) contra el resultado esperado, y cada importe = cantidad × precio.
  · Gold recalculado desde TU Silver (pedidos distintos, unidades y ventas por cliente y mes) y comparado con el esperado.

Regla monetaria de este proyecto: Silver y Gold guardan Bs como número decimal con dos decimales (REAL). Para comparar sin errores de coma flotante,
cada importe se convierte a centavos enteros con redondeo al centavo más cercano (mitad hacia arriba); la comparación de centavos es EXACTA
(tolerancia 0): ``monto`` debe ser exactamente ``cantidad × precio_unitario`` y ``ventas_bs`` la suma exacta de los ``monto`` de ese cliente y mes.

Contrato de columnas:
  bronze_ventas_raw      nro_pedido, fecha, cliente, ruta, vendedor, estado, producto, categoria, cantidad, precio_unitario  (texto, sin limpiar)
  silver_ventas          las mismas diez columnas ya limpias (fecha AAAA-MM-DD, cantidad entera) + monto
  gold_ventas_cliente_mes cliente, mes (AAAA-MM), pedidos, unidades, ventas_bs
"""
from contextlib import closing
from pathlib import Path
import re
import sqlite3
import sys
from datetime import date

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validacion_comun import Informe, Oraculo, a_centavos, canon, tiene_dos_decimales  # noqa: E402
from validar_final import iguales, llave, sha256_archivo, tiene_columnas  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ESPEC = {
    'huellas': '08_SOLUCIONES/huellas_etl_distribuidora.json',
    'datos': '04_DATASETS/distribuidora/etl',
    'raw': 'ventas_erp_raw.csv',
    'raw_columnas': ['nro_pedido', 'fecha', 'cliente', 'ruta', 'vendedor', 'estado', 'producto', 'categoria', 'cantidad', 'precio_unitario'],
    'silver': {'clave': ['nro_pedido', 'producto'],
               'columnas': ['fecha', 'cliente', 'ruta', 'vendedor', 'estado', 'categoria', 'cantidad', 'precio_centavos', 'monto_centavos']},
    'gold': {'clave': ['cliente', 'mes'], 'medidas': ['pedidos', 'unidades', 'ventas_centavos']},
}


def nombre_canonico(texto):
    return ' '.join(str(texto).split()).casefold()


def preparar_silver(df):
    """Silver del estudiante → tabla comparable: cliente canónico y dinero en centavos enteros (regla de a_centavos)."""
    s = df.copy()
    s['cliente'] = s['cliente'].map(nombre_canonico)
    s['precio_centavos'] = s['precio_unitario'].map(a_centavos)
    s['monto_centavos'] = s['monto'].map(a_centavos)
    return s


def preparar_gold(df):
    g = df.copy()
    g['cliente'] = g['cliente'].map(nombre_canonico)
    g['ventas_centavos'] = g['ventas_bs'].map(a_centavos)
    return g


def recalcular_gold(silver):
    """Gold que debería salir de la Silver preparada: solo entregados, pedidos distintos, unidades y ventas por cliente y mes."""
    e = silver[silver['estado'] == 'entregado']
    e = e.assign(mes=e['fecha'].astype(str).str[:7])
    return e.groupby(['cliente', 'mes'], as_index=False).agg(pedidos=('nro_pedido', 'nunique'), unidades=('cantidad', 'sum'), ventas_centavos=('monto_centavos', 'sum'))


def validar(path, huellas=None, datos=None):
    p = Path(path).resolve()
    e = ESPEC
    inf = Informe('ETL guiado · distribuidora')
    oraculo = Oraculo.desde_archivo(Path(huellas) if huellas else ROOT / e['huellas'])
    datos = Path(datos) if datos else ROOT / e['datos']
    for nombre, h in oraculo.datos.get('raw_sha256', {}).items():
        inf.comprobar(sha256_archivo(datos / nombre) == h, f'datos de entrada {nombre} sin modificar', 'el archivo de entrada no coincide con el original')
    if not inf.comprobar(p.exists(), 'existe la base de datos', str(p)):
        return inf.cerrar()
    raw = pd.read_csv(datos / e['raw'], sep=';', dtype=str, keep_default_na=False)
    with closing(sqlite3.connect(p.as_uri() + '?mode=ro', uri=True)) as con:
        inf.comprobar(con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'SQLite íntegra')
        presentes = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        nombres = ['bronze_ventas_raw', 'silver_ventas', 'gold_ventas_cliente_mes']
        faltan = [t for t in nombres if t not in presentes]
        if not inf.comprobar(not faltan, 'tablas bronze_ventas_raw, silver_ventas y gold_ventas_cliente_mes', f'faltan {faltan}'):
            return inf.cerrar()
        bronze, silver_raw, gold_raw = (pd.read_sql(f'SELECT * FROM {t}', con) for t in nombres)
        cantidad_no_entera = con.execute("SELECT COUNT(*) FROM silver_ventas WHERE typeof(cantidad) <> 'integer'").fetchone()[0] \
            if 'cantidad' in silver_raw.columns else -1

    # Bronze = origen sin tocar
    cols = e['raw_columnas']
    f = tiene_columnas(bronze, cols)
    if inf.comprobar(not f, 'Bronze conserva las diez columnas del origen', f'faltan {f}'):
        inf.comprobar(len(bronze) == len(raw), 'Bronze tiene todas las filas del origen', f'{len(bronze)} filas y el archivo tiene {len(raw)}')
        inf.comprobar(sorted(map(tuple, bronze[cols].astype(str).values.tolist())) == sorted(map(tuple, raw[cols].values.tolist())),
                      'Bronze es idéntico al origen (texto exacto, sin limpiar)', 'alguna fila de Bronze fue modificada respecto al archivo')

    # Silver
    necesarias = cols + ['monto']
    f = tiene_columnas(silver_raw, necesarias)
    if not inf.comprobar(not f, 'Silver tiene las columnas del contrato', f'faltan {f}'):
        return inf.cerrar()
    nulos = int(silver_raw[necesarias].isna().sum().sum())
    inf.comprobar(nulos == 0, 'Silver sin valores vacíos', f'{nulos} valores vacíos')
    if nulos or silver_raw[['precio_unitario', 'monto', 'cantidad']].isna().any().any():
        return inf.cerrar()
    clave = e['silver']['clave']
    inf.comprobar(not silver_raw.duplicated(clave).any(), 'Silver sin pedido+producto repetidos')
    inf.comprobar(cantidad_no_entera == 0, 'Silver.cantidad es entera (sin truncar ni decimales)', f'{cantidad_no_entera} cantidades no enteras')
    inf.comprobar((silver_raw['cantidad'] > 0).all(), 'Silver: cantidad positiva')
    inf.comprobar(silver_raw['estado'].isin({'entregado', 'anulado'}).all(), 'Silver.estado solo entregado o anulado')
    inf.comprobar(silver_raw['fecha'].astype(str).str.fullmatch(r'\d{4}-\d{2}-\d{2}').all(), 'Silver.fecha en formato AAAA-MM-DD')
    reales = []
    for v in silver_raw['fecha'].astype(str):
        try:
            date.fromisoformat(v)
            reales.append(True)
        except ValueError:
            reales.append(False)
    inf.comprobar(all(reales), 'Silver.fecha es una fecha real')
    inf.comprobar(silver_raw['ruta'].astype(str).str.fullmatch(r'R\d{2}').all(), 'Silver.ruta normalizada (R01…)')
    inf.comprobar(silver_raw['vendedor'].astype(str).str.strip().ne('').all(), 'Silver sin vendedores vacíos')
    decimales = silver_raw['precio_unitario'].map(tiene_dos_decimales) & silver_raw['monto'].map(tiene_dos_decimales)
    inf.comprobar(decimales.all(), 'precio y monto con a lo sumo dos decimales (sin fracciones de centavo)', f'{int((~decimales).sum())} filas')
    if decimales.all():
        silver = preparar_silver(silver_raw)
        esperado = silver['cantidad'] * silver['precio_centavos']
        malos = silver[esperado != silver['monto_centavos']]
        inf.comprobar(malos.empty, 'monto = cantidad × precio_unitario exacto en centavos en cada fila',
                      f'{len(malos)} filas, p. ej. {llave(malos, clave).head(3).tolist()}')
        for col in ('fecha', 'cliente'):
            inf.comprobar(silver.groupby('nro_pedido')[col].nunique().max() == 1, f'cada pedido tiene un solo valor de {col}')
        inf.diferencias('Silver coincide fila por fila con el resultado esperado', oraculo.comparar('silver', silver[clave + e['silver']['columnas']]))
        # Gold
        g = e['gold']
        f = tiene_columnas(gold_raw, ['cliente', 'mes', 'pedidos', 'unidades', 'ventas_bs'])
        if inf.comprobar(not f, 'Gold tiene las columnas del contrato', f'faltan {f}') and not gold_raw[['cliente', 'mes', 'pedidos', 'unidades', 'ventas_bs']].isna().any().any():
            gold = preparar_gold(gold_raw)
            inf.comprobar(not gold.duplicated(g['clave']).any(), 'Gold sin cliente+mes repetidos')
            inf.comprobar(gold['mes'].astype(str).str.fullmatch(r'\d{4}-(0[1-9]|1[0-2])').all(), 'Gold.mes es AAAA-MM válido')
            calculado = recalcular_gold(silver)
            inf.comprobar(set(llave(gold, g['clave'])) <= set(llave(calculado, g['clave'])), 'todo cliente y mes de Gold existe en Silver (entregados)',
                          f'inexistentes, p. ej. {sorted(set(llave(gold, g["clave"])) - set(llave(calculado, g["clave"])))[:3]}')
            dif = iguales(gold[g['clave'] + g['medidas']], calculado[g['clave'] + g['medidas']], g['clave'])
            inf.comprobar(not dif, 'Gold = agrupación de tu propia Silver (pedidos distintos, unidades y ventas por cliente y mes)', '; '.join(dif))
            inf.diferencias('Gold coincide fila por fila con el resultado esperado', oraculo.comparar('gold', gold[g['clave'] + g['medidas']]))
            inf.comprobar(int(gold['ventas_centavos'].sum()) == int(silver.loc[silver['estado'] == 'entregado', 'monto_centavos'].sum()),
                          'suma de ventas de Gold = ventas entregadas de Silver (en centavos, exacta)')
        # controles globales (publicados en el README del proyecto)
        esc = {'bronze': len(bronze), 'silver': len(silver), 'pedidos': int(silver['nro_pedido'].nunique()), 'clientes': int(silver['cliente'].nunique()),
               'gold_filas': len(gold_raw), 'ventas_centavos': int(silver.loc[silver['estado'] == 'entregado', 'monto_centavos'].sum())}
        for k, v in esc.items():
            inf.comprobar(oraculo.escalar_ok(k, v), f'control global {k}')
    return inf.cerrar()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print('OK', validar(sys.argv[1]))
