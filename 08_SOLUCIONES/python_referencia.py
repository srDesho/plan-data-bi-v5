"""Referencia de ejercicios. Abrir después del intento propio, no durante el examen."""
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import csv
import json
import statistics
import numpy as np
import pandas as pd

def importe(cantidad, precio):
    return cantidad * precio

def porcentaje(real, meta):
    return None if meta <= 0 else 100 * real / meta

def normalizar_nombre(texto):
    return ' '.join(texto.strip().split()).title()

def cliente_diccionario(codigo, ruta):
    return {'cliente_id': codigo, 'ruta': ruta}

def clientes_unicos(codigos):
    return sorted(set(codigos))

def contar_estados(estados):
    conteos = {}
    for estado in estados:
        conteos[estado] = conteos.get(estado, 0) + 1
    return conteos

def ventas_entregadas(lineas):
    total = 0
    for linea in lineas:
        if linea['estado'] == 'entregado':
            total += linea['cantidad'] * linea['precio']
    return total

def clasificar_ticket(monto):
    if monto < 200:
        return 'Pequeño'
    if monto <= 600:
        return 'Mediano'
    return 'Grande'

def precio_centavos(texto):
    limpio = str(texto).strip().removeprefix('Bs').strip().replace(',', '.')
    try:
        valor = Decimal(limpio)
    except InvalidOperation as e:
        raise ValueError('Precio inválido') from e
    if not valor.is_finite() or valor < 0 or valor * 100 != (valor * 100).to_integral_value():
        raise ValueError('Precio negativo, no finito o con más de dos decimales')
    return int(valor * 100)

def fecha_iso(texto):
    for formato in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%y'):
        try:
            return datetime.strptime(texto.strip(), formato).date().isoformat()
        except ValueError:
            continue
    raise ValueError('Fecha inválida')

def cantidad_entera(texto):
    try:
        valor = Decimal(str(texto).strip())
    except InvalidOperation as e:
        raise ValueError('Cantidad inválida') from e
    if not valor.is_finite() or valor <= 0 or valor != valor.to_integral_value():
        raise ValueError('Cantidad debe ser entera positiva')
    return int(valor)

def recencia(ultima, corte):
    dias = (date.fromisoformat(corte) - date.fromisoformat(ultima)).days
    if dias < 0:
        raise ValueError('Compra posterior al corte')
    return dias

def leer_clientes(ruta):
    with Path(ruta).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def resumir_montos(valores):
    if not valores:
        raise ValueError('Lista vacía')
    return {'media': statistics.mean(valores), 'mediana': statistics.median(valores)}

def recuperar_vendedor(ruta, mapa):
    if ruta not in mapa:
        raise ValueError('Ruta sin vendedor')
    return mapa[ruta]

def filtrar_fecha(filas, inicio, fin):
    return [f for f in filas if inicio <= f['fecha'] <= fin]

def cargar_pedidos(ruta):
    return pd.read_csv(ruta)

def contar_por_ruta(clientes):
    return clientes.groupby('ruta', as_index=False).agg(clientes=('cliente_id', 'size')).sort_values('ruta').reset_index(drop=True)

def monto_detalle(items):
    return items.assign(monto=items['cantidad'] * items['precio_unitario'])

def ticket_por_pedido(items):
    return monto_detalle(items).groupby('pedido_id', as_index=False).agg(monto=('monto', 'sum'))

def unir_clientes(pedidos, clientes):
    unido = pedidos.merge(clientes[['cliente_id', 'ruta']], on='cliente_id', how='left', validate='many_to_one', indicator=True)
    if not unido['_merge'].eq('both').all():
        raise ValueError('Cliente huérfano')
    return unido.drop(columns='_merge')

def quitar_exactos(df):
    return df.drop_duplicates().reset_index(drop=True)

def perfilar(df):
    return {'filas': len(df), 'nulos': df.isna().sum().to_dict(), 'duplicados_exactos': int(df.duplicated().sum())}

def mes_fechas(fechas):
    return pd.to_datetime(fechas, format='%Y-%m-%d').dt.strftime('%Y-%m')

def gold_cliente_mes(silver):
    validos = silver.loc[silver['estado'].eq('entregado')].copy()
    validos['mes'] = mes_fechas(validos['fecha'])
    validos['monto'] = validos['cantidad'] * validos['precio_unitario']
    return validos.groupby(['cliente_id', 'mes'], as_index=False).agg(ventas_bs=('monto', 'sum'), pedidos=('pedido_id', 'nunique'))

def abc_ventas(df):
    orden = df.sort_values(['ventas', 'cliente_id'], ascending=[False, True]).copy()
    total = orden['ventas'].sum()
    if total <= 0:
        raise ValueError('Total no positivo')
    antes = (orden['ventas'].cumsum() - orden['ventas']) / total
    orden['abc'] = np.select([antes < .8, antes < .95], ['A', 'B'], default='C')
    return orden

def detectar_atipicos(valores):
    serie = pd.Series(valores)
    q1, q3 = serie.quantile([.25, .75])
    iqr = q3 - q1
    return serie[(serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)].tolist()

def validar_claves(df, clave):
    if df[clave].isna().any() or df[clave].astype(str).str.strip().eq('').any() or df[clave].duplicated().any():
        raise ValueError('Clave vacía o duplicada')
    return True

def escribir_resumen(ruta, datos):
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding='utf-8')
    return destino

def auditoria_conteos(bronze, duplicados, rechazos, silver):
    if min(bronze, duplicados, rechazos, silver) < 0 or bronze != duplicados + rechazos + silver:
        raise ValueError('Conteos no cuadran')
    return True
