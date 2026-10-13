"""Corrige después del intento. No muestra código. Uso: validar_final.py salida [--transferencia]"""
from pathlib import Path
import json,sqlite3,sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def validar(salida,transferencia=False):
    salida=Path(salida).resolve()
    oracle=json.loads((ROOT/'08_SOLUCIONES'/('controles_transferencia.json' if transferencia else 'controles_final.json')).read_text(encoding='utf-8'))
    with sqlite3.connect((salida/'resultado.db').as_uri()+'?mode=ro',uri=True) as c:
        assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        for table,key in [('bronze','bronze'),('silver','silver'),('rechazos','rechazados'),('gold','gold_filas')]:
            actual=c.execute('SELECT COUNT(*) FROM '+table).fetchone()[0]
            assert actual==oracle[key],f'Conteo incorrecto: {table}={actual}'
        assert c.execute('SELECT COUNT(*)-COUNT(DISTINCT linea_id) FROM silver').fetchone()[0]==0
        assert c.execute("SELECT COUNT(*) FROM silver WHERE cantidad<=0 OR cantidad<>CAST(cantidad AS INTEGER) OR precio_centavos<0 OR estado NOT IN ('entregado','anulado')").fetchone()[0]==0
        assert c.execute("SELECT SUM(monto_centavos) FROM silver WHERE estado='entregado'").fetchone()[0]==oracle['ventas_centavos']
        assert c.execute('SELECT SUM(ventas_centavos) FROM gold').fetchone()[0]==oracle['ventas_centavos']
        assert c.execute('SELECT COUNT(DISTINCT documento),COUNT(DISTINCT cliente_id) FROM silver').fetchone()==(oracle['documentos'],oracle['clientes'])
        assert c.execute("SELECT COUNT(*) FROM rechazos WHERE motivos IS NULL OR TRIM(motivos)=''").fetchone()[0]==0
        esperada=pd.read_csv(ROOT/'08_SOLUCIONES'/('silver_transferencia_esperada.csv' if transferencia else 'silver_final_esperada.csv'))
        campos=list(esperada.columns)
        real=pd.read_sql('SELECT '+','.join(campos)+' FROM silver ORDER BY linea_id',c)
        esperada=esperada.sort_values('linea_id').reset_index(drop=True)
        pd.testing.assert_frame_equal(real,esperada,check_dtype=False)
        raw_fecha=real.groupby('documento').fecha.nunique()
        assert raw_fecha.max()==1,'Un documento no debe tener fechas contradictorias'
    auditoria=json.loads((salida/'auditoria.json').read_text(encoding='utf-8'))
    for key in ['bronze','duplicados_exactos','rechazados','silver','ventas_centavos']:
        assert auditoria[key]==oracle[key],f'Auditoria incorrecta: {key}'
    assert auditoria['bronze']==auditoria['duplicados_exactos']+auditoria['rechazados']+auditoria['silver']
    return 'Controles numéricos correctos; falta evaluar explicación, cambios adversos y autonomía.'

if __name__=='__main__':
    if len(sys.argv)<2:raise SystemExit(__doc__)
    print('OK',validar(sys.argv[1],'--transferencia' in sys.argv))
