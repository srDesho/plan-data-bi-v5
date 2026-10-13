"""Pruebas del estudiante: casos conocidos, límites y fallos de contrato."""
from pathlib import Path
import json
import tempfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def igualdad(actual, esperado):
    if isinstance(esperado, pd.DataFrame):
        pd.testing.assert_frame_equal(actual.reset_index(drop=True), esperado.reset_index(drop=True), check_dtype=False)
    elif isinstance(esperado, pd.Series):
        pd.testing.assert_series_equal(actual, esperado, check_names=False, check_dtype=False)
    elif isinstance(esperado, float):
        assert abs(actual-esperado) < 1e-8, (actual, esperado)
    else:
        assert actual == esperado, (actual, esperado)

def error(funcion, *args):
    try:
        funcion(*args)
    except ValueError:
        return
    raise AssertionError('Se esperaba ValueError para entrada inválida')

def comprobar(id, modulo):
    tests = 0
    def check(fn, args, expected):
        nonlocal tests
        igualdad(getattr(modulo, fn)(*args), expected)
        tests += 1
    if id == 'P01':
        check('importe',(3,10),30);check('importe',(0,4.5),0)
    elif id == 'P02':
        check('porcentaje',(80,100),80);check('porcentaje',(0,0),None);check('porcentaje',(20,-1),None)
    elif id == 'P03':
        check('normalizar_nombre',('  TIENDA   el SOL  ',),'Tienda El Sol');check('normalizar_nombre',('josé',),'José')
    elif id == 'P04': check('cliente_diccionario',('001','R01'),{'cliente_id':'001','ruta':'R01'})
    elif id == 'P05': check('clientes_unicos',([3,1,3,2],),[1,2,3]);check('clientes_unicos',([31,7,18,7,25],),[7,18,25,31]);check('clientes_unicos',([],),[])
    elif id == 'P06': check('contar_estados',(['entregado','anulado','entregado'],),{'entregado':2,'anulado':1});check('contar_estados',([],),{})
    elif id == 'P07': check('ventas_entregadas',([{'estado':'entregado','cantidad':3,'precio':10},{'estado':'anulado','cantidad':99,'precio':10}],),30)
    elif id == 'P08':
        for x,y in [(199.99,'Pequeño'),(200,'Mediano'),(600,'Mediano'),(600.01,'Grande')]:check('clasificar_ticket',(x,),y)
    elif id == 'P09':
        for x,y in [(' Bs 11,50 ',1150),('0',0),('2.05',205)]:check('precio_centavos',(x,),y)
        for x in ['abc','-1','2.001','NaN']:error(modulo.precio_centavos,x);tests+=1
    elif id == 'P10':
        for x in ['2026-09-01','01/09/2026','01-09-26']:check('fecha_iso',(x,),'2026-09-01')
        error(modulo.fecha_iso,'31/02/2026');tests+=1
    elif id == 'P11':
        check('cantidad_entera',('3.0',),3)
        for x in ['1.5','0','-1','NaN','inf','abc']:error(modulo.cantidad_entera,x);tests+=1
    elif id == 'P12':
        check('recencia',('2026-09-25','2026-09-30'),5);check('recencia',('2026-09-30','2026-09-30'),0)
        error(modulo.recencia,'2026-10-01','2026-09-30');tests+=1
    elif id == 'P13':
        rows=modulo.leer_clientes(ROOT/'04_DATASETS/distribuidora/clientes.csv')
        assert len(rows)==120 and rows[0]['cliente_id']=='1';tests+=1
    elif id == 'P14':
        check('resumir_montos',([10,20,90],),{'media':40,'mediana':20});error(modulo.resumir_montos,[]);tests+=1
    elif id == 'P15':
        check('recuperar_vendedor',('R01',{'R01':'Ana'}),'Ana');error(modulo.recuperar_vendedor,'R02',{'R01':'Ana'});tests+=1
    elif id == 'P16': check('filtrar_fecha',([{'fecha':'2026-09-01'},{'fecha':'2026-09-30'},{'fecha':'2026-10-01'}],'2026-09-01','2026-09-30'),[{'fecha':'2026-09-01'},{'fecha':'2026-09-30'}])
    elif id == 'P17':
        x=modulo.cargar_pedidos(ROOT/'04_DATASETS/distribuidora/pedidos.csv');assert len(x)==3600 and x['estado'].eq('entregado').sum()==3442;tests+=1
    elif id == 'P18': check('contar_por_ruta',(pd.DataFrame({'cliente_id':[1,2,3],'ruta':['R02','R01','R01']}),),pd.DataFrame({'ruta':['R01','R02'],'clientes':[2,1]}))
    elif id in ('P19','P20'):
        x=pd.DataFrame({'pedido_id':[1,1,2],'cantidad':[3,2,1],'precio_unitario':[10,20,5]})
        if id=='P19':check('monto_detalle',(x,),x.assign(monto=[30,40,5]));assert 'monto' not in x;tests+=1
        else:check('ticket_por_pedido',(x,),pd.DataFrame({'pedido_id':[1,2],'monto':[70,5]}))
    elif id == 'P21':
        p=pd.DataFrame({'pedido_id':[1,2],'cliente_id':[3,3]});c=pd.DataFrame({'cliente_id':[3],'ruta':['R01']})
        check('unir_clientes',(p,c),p.assign(ruta=['R01','R01']))
        error(modulo.unir_clientes,p,pd.concat([c,c]));error(modulo.unir_clientes,p,c.assign(cliente_id=9));tests+=2
    elif id == 'P22':check('quitar_exactos',(pd.DataFrame({'id':[1,1,1],'monto':[10,10,20]}),),pd.DataFrame({'id':[1,1],'monto':[10,20]}))
    elif id == 'P23':check('perfilar',(pd.DataFrame({'a':[1,1,None]}),),{'filas':3,'nulos':{'a':1},'duplicados_exactos':1})
    elif id == 'P24':check('mes_fechas',(pd.Series(['2026-09-01','2026-10-31']),),pd.Series(['2026-09','2026-10']))
    elif id == 'P25':
        x=pd.DataFrame({'cliente_id':[1,1,1],'pedido_id':[1,1,2],'fecha':['2026-09-01']*3,'estado':['entregado','entregado','anulado'],'cantidad':[2,3,100],'precio_unitario':[10,5,99]})
        check('gold_cliente_mes',(x,),pd.DataFrame({'cliente_id':[1],'mes':['2026-09'],'ventas_bs':[35],'pedidos':[1]}))
    elif id == 'P26':
        x=pd.DataFrame({'cliente_id':[1,2,3,4],'ventas':[75,10,10,5]})
        check('abc_ventas',(x,),x.assign(abc=['A','A','B','C']));error(modulo.abc_ventas,x.assign(ventas=0));tests+=1
    elif id == 'P27':check('detectar_atipicos',([10,11,12,13,14,100],),[100]);check('detectar_atipicos',([10,10,10],),[])
    elif id == 'P28':
        check('validar_claves',(pd.DataFrame({'id':[1,2]}),'id'),True)
        for vals in [[1,1],[1,None],['a',' ']]:error(modulo.validar_claves,pd.DataFrame({'id':vals}),'id');tests+=1
    elif id == 'P29':
        with tempfile.TemporaryDirectory() as tmp:
            p=modulo.escribir_resumen(Path(tmp)/'sub/resumen.json',{'ventas':20,'nombre':'José'})
            assert isinstance(p,Path) and json.loads(p.read_text(encoding='utf-8'))=={'ventas':20,'nombre':'José'};tests+=1
    elif id == 'P30':
        check('auditoria_conteos',(12170,150,20,12000),True)
        error(modulo.auditoria_conteos,5,1,1,4);error(modulo.auditoria_conteos,5,-1,1,5);tests+=2
    else: raise ValueError('ID de ejercicio desconocido')
    return tests
