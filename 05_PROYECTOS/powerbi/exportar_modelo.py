"""Exporta tablas de estrella verificables. No crea ni simula un archivo PBIX."""
from pathlib import Path
import argparse
import json
import sqlite3
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]

def exportar(destino):
    destino=Path(destino);destino.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(ROOT/'04_DATASETS/comercial.db') as con:
        frames={t:pd.read_sql(f'SELECT * FROM {t}',con) for t in ['clientes','productos','vendedores','pedidos','pedido_items','visitas','presupuesto']}
    c,p,v=frames['clientes'].copy(),frames['productos'].copy(),frames['vendedores'].copy()
    c['nombre_negocio']=c.nombre_negocio.str.strip();c['zona']=c.zona.fillna('Sin zona')
    fact=frames['pedido_items'].merge(frames['pedidos'],on='pedido_id',validate='many_to_one').merge(c[['cliente_id','ruta']],on='cliente_id',validate='many_to_one')
    fact['fecha_id']=fact.fecha.str.replace('-','',regex=False).astype(int)
    fact['mes']=fact.fecha.str[:7]
    fact['precio_centavos']=(fact.precio_unitario*100).round().astype('int64')
    fact['monto_centavos']=fact.cantidad*fact.precio_centavos
    fact=fact.drop(columns=['precio_unitario','fecha'])
    fechas=pd.DataFrame({'fecha':pd.date_range('2026-04-01','2026-09-30')})
    fechas['fecha_id']=fechas.fecha.dt.strftime('%Y%m%d').astype(int)
    fechas['anio']=fechas.fecha.dt.year;fechas['mes_numero']=fechas.fecha.dt.month
    fechas['mes']=fechas.fecha.dt.strftime('%Y-%m');fechas['dia']=fechas.fecha.dt.day
    fechas['fecha']=fechas.fecha.dt.strftime('%Y-%m-%d')
    meses=fechas[['mes','anio','mes_numero']].drop_duplicates().reset_index(drop=True)
    rutas=pd.DataFrame({'ruta':sorted(c.ruta.unique())})
    visitas=frames['visitas'].copy();visitas['fecha_id']=visitas.fecha.str.replace('-','',regex=False).astype(int)
    visitas['mes']=visitas.fecha.str[:7];visitas=visitas.drop(columns='fecha')
    # Se omite dim_cliente→fact_visitas para evitar un segundo camino por ruta.
    tablas={'fact_ventas':fact,'dim_cliente':c,'dim_producto':p,'dim_vendedor':v,'dim_fecha':fechas,'dim_mes':meses,'dim_ruta':rutas,'fact_presupuesto':frames['presupuesto'],'fact_visitas':visitas}
    for table,key in [('dim_cliente','cliente_id'),('dim_producto','producto_id'),('dim_vendedor','vendedor_id'),('dim_fecha','fecha_id'),('dim_mes','mes'),('dim_ruta','ruta')]:
        if tablas[table][key].isna().any() or tablas[table][key].duplicated().any():raise ValueError(f'Clave inválida {table}')
    for key,table in [('cliente_id','dim_cliente'),('producto_id','dim_producto'),('vendedor_id','dim_vendedor'),('fecha_id','dim_fecha'),('mes','dim_mes'),('ruta','dim_ruta')]:
        if not fact[key].isin(tablas[table][key]).all():raise ValueError(f'Huérfanos {key}')
    total=int(fact.loc[fact.estado=='entregado','monto_centavos'].sum())
    if len(fact)!=16178 or total!=146892450:raise ValueError('Hecho no cuadra')
    for name,frame in tablas.items():frame.to_csv(destino/f'{name}.csv',index=False)
    control={'filas':{k:len(x) for k,x in tablas.items()},'ventas_entregadas_centavos':total,'pedidos_entregados':fact.loc[fact.estado=='entregado','pedido_id'].nunique()}
    (destino/'control_modelo.json').write_text(json.dumps(control,indent=2),encoding='utf-8')
    return control

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--salida',default=str(Path(__file__).parent/'datos_modelo'))
    args=parser.parse_args();print(json.dumps(exportar(args.salida),ensure_ascii=False))
