"""Referencia del mini-ETL (ME01–ME04). Abrir solo después de tu intento.

Cuatro funciones que se repiten en el ETL grande: extraer, transformar, validar y cargar.
Uso desde la raíz:  python 08_SOLUCIONES/mini_etl_referencia.py --entrada 04_DATASETS/mini_etl --salida /ruta/salida
"""
from contextlib import closing
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import argparse
import json
import logging
import os
import sqlite3

import pandas as pd

log = logging.getLogger('mini_etl')

COLUMNAS = ['ticket_id', 'fecha', 'tienda', 'producto', 'unidades', 'estado', 'precio']
ESTADOS = {'entregado', 'anulado'}
MAX_UNIDADES = 500          # ME04: regla añadida; no afecta al raw original


def extraer(ruta):
    """Lee el CSV como texto, sin convertir nada: Bronze debe ser idéntico al origen."""
    return pd.read_csv(ruta, sep=';', dtype=str, keep_default_na=False)


def quitar_exactos(df):
    return df.drop_duplicates().reset_index(drop=True)


def perfilar(df):
    return {'filas': len(df),
            'nulos': {c: int((df[c].str.strip() == '').sum()) for c in df.columns},
            'duplicados_exactos': int(df.duplicated().sum())}


def _fecha(texto):
    for formato in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.strptime(texto.strip(), formato).date().isoformat()
        except ValueError:
            pass
    raise ValueError('fecha')


def _unidades(texto):
    try:
        x = Decimal(texto.strip())
    except InvalidOperation:
        raise ValueError('unidades')
    if not x.is_finite() or x != x.to_integral_value() or x <= 0:
        raise ValueError('unidades')
    if x > MAX_UNIDADES:
        raise ValueError('unidades')
    return int(x)


def _precio_centavos(texto):
    limpio = texto.strip().removeprefix('Bs').strip().replace(',', '.')
    try:
        x = Decimal(limpio)
    except InvalidOperation:
        raise ValueError('precio')
    if not x.is_finite() or x < 0 or x != x.quantize(Decimal('0.01')):
        raise ValueError('precio')
    return int(x * 100)


def transformar(raw, catalogo):
    """Devuelve (silver, rechazos). No modifica `raw`. Sin imputar valores."""
    if not set(COLUMNAS) <= set(raw.columns):
        raise ValueError('columna obligatoria ausente: ' + ', '.join(sorted(set(COLUMNAS) - set(raw.columns))))
    if catalogo['producto'].duplicated().any():
        raise ValueError('catálogo con producto duplicado')
    unico = raw.drop_duplicates()
    conflictos = unico[unico['ticket_id'].duplicated(keep=False)]
    if len(conflictos):
        raise ValueError('ticket_id con contenido distinto: ' + ', '.join(sorted(conflictos['ticket_id'].unique())))
    categorias = dict(zip(catalogo['producto'], catalogo['categoria']))
    buenos, malos = [], []
    for fila in unico.to_dict('records'):
        motivos = []
        item = {'ticket_id': fila['ticket_id']}
        for campo, funcion in (('fecha', _fecha), ('unidades', _unidades), ('precio', _precio_centavos)):
            try:
                item[campo] = funcion(fila[campo])
            except ValueError:
                motivos.append(campo)
        estado = fila['estado'].strip().lower()
        if estado not in ESTADOS:
            motivos.append('estado')
        producto = fila['producto'].strip().upper()
        if producto not in categorias:
            motivos.append('producto')
        if motivos:
            malos.append({**{c: fila[c] for c in COLUMNAS}, 'motivos': ';'.join(motivos)})
            continue
        buenos.append({'ticket_id': fila['ticket_id'], 'fecha': item['fecha'],
                       'tienda': ' '.join(fila['tienda'].split()).title(), 'producto': producto,
                       'categoria': categorias[producto], 'unidades': item['unidades'], 'estado': estado,
                       'precio_centavos': item['precio'], 'monto_centavos': item['unidades'] * item['precio']})
    silver = pd.DataFrame(buenos, columns=['ticket_id', 'fecha', 'tienda', 'producto', 'categoria', 'unidades',
                                           'estado', 'precio_centavos', 'monto_centavos'])
    rechazos = pd.DataFrame(malos, columns=COLUMNAS + ['motivos'])
    return silver.sort_values('ticket_id').reset_index(drop=True), rechazos.sort_values('ticket_id').reset_index(drop=True)


def gold_tienda_mes(silver):
    ent = silver[silver['estado'] == 'entregado'].assign(mes=lambda d: d['fecha'].str[:7])
    return (ent.groupby(['tienda', 'mes'], as_index=False)
               .agg(ventas_centavos=('monto_centavos', 'sum'), tickets=('ticket_id', 'nunique'))
               .sort_values(['tienda', 'mes']).reset_index(drop=True))


def validar(n_bronze, n_duplicados, n_rechazados, n_silver):
    for n in (n_bronze, n_duplicados, n_rechazados, n_silver):
        if n < 0:
            raise ValueError('conteo negativo')
    if n_bronze != n_duplicados + n_rechazados + n_silver:
        raise ValueError(f'No cuadra: {n_bronze} != {n_duplicados} + {n_rechazados} + {n_silver}')
    return True


def ejecutar(entrada, salida):
    entrada, salida = Path(entrada), Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    raw = extraer(entrada / 'ventas_mini_raw.csv')
    catalogo = pd.read_csv(entrada / 'productos_mini.csv', dtype=str, keep_default_na=False)
    silver, rechazos = transformar(raw, catalogo)
    gold = gold_tienda_mes(silver)
    n_dup = len(raw) - len(raw.drop_duplicates())
    validar(len(raw), n_dup, len(rechazos), len(silver))
    ventas = int(silver.loc[silver['estado'] == 'entregado', 'monto_centavos'].sum())
    if int(gold['ventas_centavos'].sum()) != ventas:
        raise ValueError('Gold no cuadra con Silver')
    tmp, destino = salida / 'mini.tmp.db', salida / 'mini.db'
    if tmp.exists():
        tmp.unlink()
    try:
        with closing(sqlite3.connect(tmp)) as con:
            for nombre, tabla in (('bronze', raw), ('silver', silver), ('rechazos', rechazos), ('gold', gold)):
                tabla.to_sql(nombre, con, index=False, if_exists='replace')
            suma_sql = con.execute("SELECT COALESCE(SUM(monto_centavos),0) FROM silver WHERE estado='entregado'").fetchone()[0]
            if suma_sql != ventas:
                raise ValueError('SQL no cuadra')
        os.replace(tmp, destino)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise
    metricas = {'bronze': len(raw), 'duplicados_exactos': n_dup, 'rechazados': len(rechazos),
                'silver': len(silver), 'ventas_centavos': ventas}
    (salida / 'auditoria.json').write_text(json.dumps(metricas, indent=2), encoding='utf-8')
    log.info('Carga completa: %s', metricas)
    return metricas


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--entrada', required=True)
    ap.add_argument('--salida', required=True)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    print(ejecutar(args.entrada, args.salida))
