"""Repite pruebas del material en archivos temporales; no evalúa tus conocimientos."""
from pathlib import Path
import ast,contextlib,csv,datetime,hashlib,importlib,importlib.util,io,json,math,os,re,sqlite3,sys,tempfile,zipfile
import pandas as pd
import nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from contratos_python import comprobar as comprobar_python
from corregir_sql import comprobar as comprobar_sql,consulta
from validar_etl_distribuidora import validar as validar_original
from validar_final import validar as validar_nuevo

ROOT=Path(__file__).resolve().parents[1]
sys.dont_write_bytecode=True

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def numeric(actual,expected):
    if isinstance(expected,dict):
        for key,value in expected.items():numeric(actual[key],value)
    elif isinstance(expected,list):
        assert len(actual)==len(expected)
        for x,y in zip(actual,expected):numeric(x,y)
    elif isinstance(expected,(int,float)):
        assert math.isclose(actual,expected,rel_tol=1e-8,abs_tol=1e-8),(actual,expected)
    else:assert actual==expected,(actual,expected)

def main():
    tests=[];cwd=Path.cwd()
    os.chdir(ROOT)
    def add(name,fn):
        try:
            detail=fn();tests.append({'prueba':name,'estado':'OK','evidencia':detail})
            print('OK',name,flush=True)
        except Exception as e:
            tests.append({'prueba':name,'estado':'ERROR','tipo':type(e).__name__,'detalle':str(e)})
            print('ERROR',name,type(e).__name__,str(e),flush=True)
    with tempfile.TemporaryDirectory(prefix='plan_v5_') as td:
        tmp=Path(td)
        def sql():
            ids=json.loads((ROOT/'08_SOLUCIONES/controles_sql.json').read_text(encoding='utf-8'))
            records=[]
            for id in ids:
                path=ROOT/'08_SOLUCIONES/sql'/f'{id}.sql'
                n=comprobar_sql(id,path);records.append({'id':id,'filas':n})
            wrong=tmp/'sql_incorrecto.sql';wrong.write_text('SELECT 0;')
            try:comprobar_sql('J2',wrong)
            except AssertionError:pass
            else:raise AssertionError('Corrector aceptó monto incorrecto')
            (ROOT/'10_VALIDACION/evidencia_sql.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
            return {'actividades':len(records),'control_negativo':'monto incorrecto rechazado'}
        add('SQL completo y corrector negativo',sql)
        def py():
            m=module(ROOT/'08_SOLUCIONES/python_referencia.py','py_ref');records=[]
            for i in range(1,31):
                id=f'P{i:02}';records.append({'id':id,'casos':comprobar_python(id,m)})
            old=m.porcentaje;m.porcentaje=lambda real,meta:0
            try:comprobar_python('P02',m)
            except AssertionError:pass
            else:raise AssertionError('Corrector aceptó función incorrecta')
            m.porcentaje=old
            return {'ejercicios':len(records),'casos':sum(x['casos'] for x in records),'control_negativo':'función incorrecta rechazada'}
        add('Python contratos y casos límite',py)
        def data():
            with sqlite3.connect(ROOT/'04_DATASETS/comercial.db') as c:
                assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
                counts={}
                for table in ['clientes','vendedores','productos','pedidos','pedido_items']:
                    csvdata=pd.read_csv(ROOT/'04_DATASETS/distribuidora'/f'{table}.csv')
                    dbdata=pd.read_sql(f'SELECT * FROM {table}',c)
                    key=csvdata.columns[0]
                    csvdata=csvdata.astype(object).where(pd.notna(csvdata),None)
                    dbdata=dbdata.astype(object).where(pd.notna(dbdata),None)
                    pd.testing.assert_frame_equal(csvdata.sort_values(key).reset_index(drop=True),dbdata.sort_values(key).reset_index(drop=True),check_dtype=False)
                    counts[table]=len(csvdata)
                items=pd.read_csv(ROOT/'04_DATASETS/distribuidora/pedido_items.csv')
                orders=pd.read_csv(ROOT/'04_DATASETS/distribuidora/pedidos.csv')
                x=items.merge(orders,on='pedido_id',validate='many_to_one')
                total=float((x.loc[x.estado=='entregado','cantidad']*x.loc[x.estado=='entregado','precio_unitario']).sum())
                assert total==1468924.5
                drop=pd.read_csv(ROOT/'04_DATASETS/distribuidora/drop_por_pedido.csv')
                assert len(drop)==3442 and drop.drop_bs.sum()==total
                byorder=x[x.estado=='entregado'].assign(monto=lambda z:z.cantidad*z.precio_unitario).groupby('pedido_id').monto.sum()
                pd.testing.assert_series_equal(byorder.sort_index(),drop.set_index('pedido_id').drop_bs.sort_index(),check_names=False,check_dtype=False)
                visitas=pd.read_sql('SELECT * FROM visitas',c)
                assert len(visitas)==480 and visitas.realizada.sum()==384 and visitas.pedido_tomado.sum()==288
                assert visitas.cliente_id.nunique()==120 and visitas[visitas.realizada==1].cliente_id.nunique()==96
                assert c.execute('SELECT COUNT(*) FROM presupuesto').fetchone()[0]==36
                assert c.execute('SELECT COUNT(*) FROM inventario').fetchone()[0]==40
            for zpath in (ROOT/'10_VALIDACION/originales').glob('*.zip'):
                with zipfile.ZipFile(zpath) as z:assert z.testzip() is None
            return {'tablas_CSV_vs_SQLite':counts,'ventas_independientes_csv':total,'drop_completo_por_pedido':'igual a SQL','visitas':[480,384,288]}
        add('Datos íntegros y cuadres independientes CSV/SQL',data)
        def original():
            m=module(ROOT/'08_SOLUCIONES/etl_distribuidora.py','etl_original')
            m.DB_OUT=tmp/'etl_original.db';m.main();validar_original(m.DB_OUT)
            m.main();counts=validar_original(m.DB_OUT)
            return {'repeticion':'mismos conteos e importe','capas':counts,'ventas_bs':1468924.50}
        add('ETL distribuidora dos ejecuciones',original)
        def nuevo():
            m=module(ROOT/'08_SOLUCIONES/etl_nuevo_referencia.py','etl_nuevo')
            results={}
            for transfer,folder in [(True,'04_DATASETS/transferencia'),(False,'09_EVALUACION_FINAL/datos')]:
                output=tmp/('transferencia' if transfer else 'final')
                first=m.ejecutar(ROOT/folder,output);second=m.ejecutar(ROOT/folder,output)
                assert first==second;validar_nuevo(output,transfer)
                results['transferencia' if transfer else 'final']=first
            return results
        add('ETL transferencia/final y oracle fila por fila',nuevo)
        def adverse():
            m=module(ROOT/'08_SOLUCIONES/etl_nuevo_referencia.py','etl_adverso')
            raw=pd.read_csv(ROOT/'04_DATASETS/transferencia/transacciones_raw.csv',sep=';',dtype=str,keep_default_na=False)
            cat=pd.read_csv(ROOT/'04_DATASETS/transferencia/catalogo.csv',dtype=str,keep_default_na=False)
            cases=[]
            for name,r,c in [('columna_ausente',raw.drop(columns='sku'),cat),('catalogo_duplicado',raw,pd.concat([cat,cat.iloc[:1]])),('clave_en_conflicto',pd.concat([raw,raw.iloc[:1].assign(precio_unitario='999.99')]),cat)]:
                try:m.transformar(r,c)
                except ValueError:cases.append(name)
                else:raise AssertionError('No rechazó '+name)
            valid=raw[raw.linea_id.str.startswith('L')].iloc[:1].copy();valid['cantidad']='3.7';valid['linea_id']='NUEVO'
            silver,reject,gold,metrics=m.transformar(valid,cat)
            assert len(silver)==0 and len(reject)==1 and 'cantidad' in reject.iloc[0].motivos
            cases.append('cantidad_fraccionaria_rechazada')
            # La salida previa no cambia si el siguiente contrato falla.
            input_copy=tmp/'adverso_entrada';input_copy.mkdir()
            raw.to_csv(input_copy/'transacciones_raw.csv',sep=';',index=False);cat.to_csv(input_copy/'catalogo.csv',index=False)
            output=tmp/'adverso_salida';m.ejecutar(input_copy,output)
            digest=hashlib.sha256((output/'resultado.db').read_bytes()).hexdigest()
            pd.concat([cat,cat.iloc[:1]]).to_csv(input_copy/'catalogo.csv',index=False)
            try:m.ejecutar(input_copy,output)
            except ValueError:pass
            else:raise AssertionError('No detuvo catálogo duplicado')
            assert hashlib.sha256((output/'resultado.db').read_bytes()).hexdigest()==digest
            cases.append('salida_previa_preservada')
            return cases
        add('Pruebas adversas y publicación segura',adverse)
        def statistics():
            m=module(ROOT/'08_SOLUCIONES/estadistica_referencia.py','stats_ref')
            controls=json.loads((ROOT/'08_SOLUCIONES/controles_estadistica.json').read_text(encoding='utf-8'))
            calculated=m.calcular();numeric(calculated,controls)
            return {'controles':list(controls),'atipicos':calculated['ST03']['atipicos'],'Welch_p':calculated['ST05']['p'],'chi2_p':calculated['ST06']['p']}
        add('Estadística con supuestos y controles',statistics)
        def model():
            m=module(ROOT/'05_PROYECTOS/powerbi/exportar_modelo.py','modelo_ref')
            control=m.exportar(tmp/'modelo')
            for p in (tmp/'modelo').glob('*.csv'):
                df=pd.read_csv(p);included=pd.read_csv(ROOT/'05_PROYECTOS/powerbi/datos_modelo'/p.name)
                pd.testing.assert_frame_equal(df,included)
            return {'filas':control['filas'],'ventas_centavos':control['ventas_entregadas_centavos'],'Desktop_M_DAX':'pendiente manual'}
        add('Modelo estrella y CSV de BI',model)
        def notebooks():
            records=[]
            for p in sorted((ROOT/'03_EJERCICIOS/Notebooks').glob('*.ipynb')):
                n=nbformat.read(p,as_version=4);nbformat.validate(n);scope={'__name__':'__main__'}
                count=0
                with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                    for i,cell in enumerate(n.cells,1):
                        if cell.cell_type=='code' and cell.source.strip():
                            exec(compile(cell.source,f'{p.name}:{i}','exec'),scope);count+=1
                plt.close('all');records.append({'archivo':p.name,'celdas_ejecutadas':count,'esquema':'OK'})
            return {'metodo':'ejecución Python de celdas en orden, sin kernel TCP','notebooks':records,'ejercicios_del_estudiante':'celdas vacías intencionales, no se declaran resueltos'}
        add('Notebooks del núcleo estructurados y ejecutados',notebooks)
        def calendar():
            ds=json.loads((ROOT/'01_PLAN_DIARIO/calendario.json').read_text(encoding='utf-8'))
            assert len(ds)==42
            begin=datetime.date(2026,10,12);weeks={};links=[]
            for i,d in enumerate(ds):
                assert d['fecha']==(begin+datetime.timedelta(days=i)).isoformat()
                assert sum(x[1] for x in d['bloques'])==d['completo']
                assert 0<=d['minimo']<=d['reducido']<=d['completo']
                if i%7==6:assert d['completo']==0 and not d['sql']
                else:assert d['sql'] and d['bloques'][0][1]>=15
                weeks[d['semana']]=weeks.get(d['semana'],0)+d['completo']
                for id in d['sql']:assert (ROOT/f'03_EJERCICIOS/SQL/{id}.md').exists()
                for id in d['python']:assert (ROOT/f'03_EJERCICIOS/Python/{id}.md').exists()
                for id in d['estadistica']:assert (ROOT/f'03_EJERCICIOS/Estadistica/{id}.md').exists()
                for t in d['teoria']:assert (ROOT/f'02_TEORIA/{t}.md').exists()
            assert set(weeks.values())=={900}
            return {'dias':42,'minutos_semanales':weeks,'domingo':'0 minutos','SQL_activo':'15–25 minutos en todas las jornadas'}
        add('Calendario fechas, horas y progresión',calendar)
        def init_space():
            m=module(ROOT/'herramientas/crear_espacio.py','crear_espacio_prueba')
            m.ROOT=tmp/'inicio';m.ROOT.mkdir();(m.ROOT/'01_PLAN_DIARIO').mkdir()
            (m.ROOT/'01_PLAN_DIARIO/calendario.json').write_bytes((ROOT/'01_PLAN_DIARIO/calendario.json').read_bytes())
            with contextlib.redirect_stdout(io.StringIO()):m.crear()
            notes=m.ROOT/'mi_trabajo/errores.md';assert notes.read_text(encoding='utf-8').count('\n')>=4
            notes.write_text('Aprendizaje propio que debe preservarse',encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):m.crear()
            assert notes.read_text(encoding='utf-8')=='Aprendizaje propio que debe preservarse'
            with (m.ROOT/'mi_trabajo/progreso.csv').open(encoding='utf-8-sig') as f:rows=list(csv.reader(f))
            assert len(rows)==43 and rows[1][0]=='2026-10-12' and rows[-1][0]=='2026-11-22'
            return {'registro':42,'segunda_ejecucion':'no sobrescribe el aprendizaje del estudiante'}
        add('Inicializador y registro de avance',init_space)
        def theory_examples():
            count=0
            for p in (ROOT/'02_TEORIA').glob('*.md'):
                for code in re.findall(r'```python\n([\s\S]*?)```',p.read_text(encoding='utf-8')):
                    with contextlib.redirect_stdout(io.StringIO()):exec(compile(code,str(p),'exec'),{'__name__':'__main__'})
                    count+=1
            return {'ejemplos_python_completos_ejecutados':count,'SQL':'las consultas docentes se desarrollan y corrigen además en el banco','DAX':'pendiente Desktop'}
        add('Ejemplos Python de los apuntes',theory_examples)
        def links():
            found=0;markdowns=list(ROOT.rglob('*.md'));broken=[]
            for p in markdowns:
                source=p.read_text(encoding='utf-8')
                assert len(re.findall(r'^```',source,re.M))%2==0,f'Fence sin cerrar: {p}'
                for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',source):
                    if re.match(r'https?://|mailto:',target):continue
                    target=target.split('#')[0]
                    if not target:continue
                    found+=1
                    if not (p.parent/target).exists():broken.append((str(p.relative_to(ROOT)),target))
            assert not broken,broken
            for p in ROOT.rglob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
            files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
            assert all(p.stat().st_size>0 for p in files),'Archivo vacío'
            sqlids=json.loads((ROOT/'08_SOLUCIONES/controles_sql.json').read_text(encoding='utf-8'))
            for id in sqlids:assert (ROOT/f'03_EJERCICIOS/SQL/{id}.md').exists() and (ROOT/f'08_SOLUCIONES/sql/{id}.sql').exists()
            assert len(list((ROOT/'03_EJERCICIOS/EXAMENES').glob('S*.md')))==6
            assert len(list((ROOT/'01_PLAN_DIARIO/dias').glob('D*.md')))==42
            return {'enlaces_internos_comprobados':found,'markdown':len(markdowns),'archivos_no_vacios':len(files),'soluciones':'separadas en 08_SOLUCIONES','esqueletos':'intencionalmente sin resolver'}
        add('Rutas, Markdown, contratos y separación de soluciones',links)
    os.chdir(cwd)
    report={'ejecutado_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pruebas':tests,'fallos':sum(x['estado']!='OK' for x in tests),'pendientes':['Power BI Desktop: M,DAX,relaciones,filtros y actualización','Excel: importación,fórmulas ytablas dinámicas','Notion importación yGitHub publicación','Kernel Jupyter externo bloqueado en entorno: se ejecutaron celdas en proceso','Notebook UAGRM estadística detenido al conectar UCI;funciones avanzadas completas no probadas','Autonomía real del estudiante: evaluación futura ydefensa']}
    (ROOT/'10_VALIDACION/resultados_pruebas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pruebas':len(tests),'fallos':report['fallos']},ensure_ascii=False))
    if report['fallos']:raise SystemExit(1)

if __name__=='__main__':main()
