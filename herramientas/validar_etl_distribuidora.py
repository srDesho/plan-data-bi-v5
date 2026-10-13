"""Uso: python herramientas/validar_etl_distribuidora.py ruta/etl_salida.db"""
import sqlite3,sys
from pathlib import Path

def validar(path):
    p=Path(path).resolve()
    with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as con:
        assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        counts={t:con.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['bronze_ventas_raw','silver_ventas','gold_ventas_cliente_mes']}
        assert list(counts.values())==[16378,16178,581],counts
        assert con.execute('SELECT COUNT(DISTINCT nro_pedido),COUNT(DISTINCT cliente) FROM silver_ventas').fetchone()==(3600,120)
        assert con.execute("SELECT ROUND(SUM(monto),2) FROM silver_ventas WHERE estado='entregado'").fetchone()[0]==1468924.50
        assert con.execute('SELECT ROUND(SUM(ventas_bs),2) FROM gold_ventas_cliente_mes').fetchone()[0]==1468924.50
    return counts

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    print('OK',validar(sys.argv[1]))
