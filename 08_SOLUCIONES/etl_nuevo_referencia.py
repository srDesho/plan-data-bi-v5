"""ETL de referencia del caso de transferencia C06. Consultar solo después de entregar el intento. (La evaluación final tiene otro contrato y su referencia no está en el paquete.)"""
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation
import argparse
import json
import logging
import os
import sqlite3
from contextlib import closing
import pandas as pd

log=logging.getLogger('etl_nuevo')
REQUERIDAS=['linea_id','documento','fecha','cliente_id','ruta','sku','cantidad','precio_unitario','estado']

def precio(texto):
    try:x=Decimal(texto.strip().removeprefix('Bs').strip().replace(',','.'))
    except InvalidOperation as e:raise ValueError('precio_invalidable') from e
    if not x.is_finite() or x<0 or x*100!=(x*100).to_integral_value():raise ValueError('precio_invalido')
    return int(x*100)

def cantidad(texto):
    try:x=Decimal(texto.strip())
    except InvalidOperation as e:raise ValueError('cantidad_invalidable') from e
    if not x.is_finite() or x<=0 or x!=x.to_integral_value():raise ValueError('cantidad_no_entera_positiva')
    return int(x)

def fecha(texto):
    for formato in ('%Y-%m-%d','%d/%m/%Y'):
        try:return datetime.strptime(texto.strip(),formato).date().isoformat()
        except ValueError:continue
    raise ValueError('fecha_invalida')

def transformar(raw,catalogo):
    faltan=set(REQUERIDAS)-set(raw.columns)
    if faltan:raise ValueError(f'Columnas ausentes: {sorted(faltan)}')
    catalogo=catalogo.copy()
    catalogo['sku']=catalogo['sku'].str.strip()
    if catalogo['sku'].isna().any() or catalogo['sku'].eq('').any() or catalogo['sku'].duplicated().any():
        raise ValueError('Catálogo con claves vacías o duplicadas')
    # Comparación sobre columnas contractuales: extras se preservan en Bronze.
    unique=raw[REQUERIDAS].drop_duplicates()
    if unique['linea_id'].str.strip().duplicated().any():raise ValueError('Conflicto: misma linea_id con contenido diferente')
    ndup=len(raw)-len(unique)
    skus=set(catalogo['sku'])
    buenos=[];malos=[]
    for row in unique.to_dict('records'):
        x={k:v.strip() for k,v in row.items()};causas=[]
        for key in ('linea_id','documento','cliente_id','ruta'):
            if not x[key]:causas.append(key+'_vacio')
        x['ruta']=x['ruta'].upper();x['estado']=x['estado'].lower()
        if x['estado'] not in {'entregado','anulado'}:causas.append('estado_invalido')
        if x['sku'] not in skus:causas.append('sku_huerfano')
        for key,fn in [('fecha',fecha),('cantidad',cantidad),('precio_unitario',precio)]:
            try:x[key]=fn(x[key])
            except ValueError as e:causas.append(str(e))
        if causas:malos.append({**row,'motivos':';'.join(causas)});continue
        x['precio_centavos']=x.pop('precio_unitario');x['monto_centavos']=x['cantidad']*x['precio_centavos'];buenos.append(x)
    cols=['linea_id','documento','fecha','cliente_id','ruta','sku','cantidad','estado','precio_centavos','monto_centavos']
    silver=pd.DataFrame(buenos,columns=cols).merge(catalogo,on='sku',how='left',validate='many_to_one')
    reject=pd.DataFrame(malos,columns=REQUERIDAS+['motivos'])
    delivered=silver[silver.estado=='entregado'].copy();delivered['mes']=delivered.fecha.str[:7]
    gold=delivered.groupby(['cliente_id','mes'],as_index=False).agg(ventas_centavos=('monto_centavos','sum'),documentos=('documento','nunique'))
    metrics={'bronze':len(raw),'duplicados_exactos':ndup,'rechazados':len(reject),'silver':len(silver),'documentos':silver.documento.nunique(),'clientes':silver.cliente_id.nunique(),'ventas_centavos':int(delivered.monto_centavos.sum()),'ventas_bs':int(delivered.monto_centavos.sum())/100,'gold_filas':len(gold)}
    if len(raw)!=ndup+len(reject)+len(silver):raise ValueError('Conteos no cuadran')
    if int(gold.ventas_centavos.sum())!=metrics['ventas_centavos']:raise ValueError('Gold no cuadra')
    return silver,reject,gold,metrics

def ejecutar(entrada,salida):
    entrada=Path(entrada);salida=Path(salida);salida.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(entrada/'transacciones_raw.csv',sep=';',dtype=str,keep_default_na=False)
    catalogo=pd.read_csv(entrada/'catalogo.csv',dtype=str,keep_default_na=False)
    silver,reject,gold,metrics=transformar(raw,catalogo)
    tmp=salida/'resultado.tmp.db';dest=salida/'resultado.db'
    if tmp.exists():tmp.unlink()
    try:
        # closing() cierra la conexión antes de os.replace; en Windows un archivo abierto no se puede reemplazar.
        with closing(sqlite3.connect(tmp)) as con:
            for name,frame in [('bronze',raw),('silver',silver),('rechazos',reject),('gold',gold)]:frame.to_sql(name,con,index=False,if_exists='replace')
            total=con.execute("SELECT COALESCE(SUM(monto_centavos),0) FROM silver WHERE estado='entregado'").fetchone()[0]
            if total!=metrics['ventas_centavos']:raise ValueError('SQL no cuadra')
            if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite inválida')
        os.replace(tmp,dest)
    except Exception:
        if tmp.exists():tmp.unlink()
        raise
    reject.to_csv(salida/'rechazos.csv',index=False)
    gold.to_csv(salida/'gold.csv',index=False)
    (salida/'auditoria.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    log.info('Carga completa: %s',metrics)
    return metrics

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada',required=True);parser.add_argument('--salida',required=True)
    args=parser.parse_args();logging.basicConfig(level=logging.INFO,format='%(levelname)s %(message)s')
    ejecutar(args.entrada,args.salida)
