"""Uso: python herramientas/corregir_sql.py J2 mi_trabajo/sql/J2.sql"""
from pathlib import Path
import collections
import json
import sqlite3
import sys
ROOT=Path(__file__).resolve().parents[1]

def consulta(texto,db=None):
    db=Path(db or ROOT/'04_DATASETS/comercial.db').resolve()
    with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as con:
        buf='';filas=[];columnas=[]
        for ch in texto:
            buf+=ch
            if ch==';' and sqlite3.complete_statement(buf):
                cur=con.execute(buf)
                if cur.description:columnas=[x[0] for x in cur.description];filas=cur.fetchall()
                buf=''
        if buf.strip():
            cur=con.execute(buf)
            if cur.description:columnas=[x[0] for x in cur.description];filas=cur.fetchall()
    return columnas,filas

def normalizar(filas):
    return collections.Counter(tuple(round(x,6) if isinstance(x,float) else x for x in fila) for fila in filas)

def comprobar(id,archivo):
    expected=json.loads((ROOT/'08_SOLUCIONES/controles_sql.json').read_text(encoding='utf-8'))[id]
    cols,rows=consulta(Path(archivo).read_text(encoding='utf-8-sig'))
    if id=='N13':
        assert rows and len(cols)==4, 'Se esperaba EXPLAIN QUERY PLAN; el texto del plan varía por versión'
    else:
        assert len(cols)==len(expected['columnas']), 'Cantidad u orden de columnas distinto del contrato'
        assert normalizar(rows)==normalizar(expected['filas']), f'Resultado diferente: {len(rows)} filas, esperado {len(expected["filas"])}'
    return len(rows)

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    try:print(f'OK {sys.argv[1]}: {comprobar(sys.argv[1],sys.argv[2])} filas correctas. Explica filtros y denominador.')
    except Exception as e:
        print(f'REVISAR: {type(e).__name__}: {e}');raise SystemExit(1)
