"""Ejecuta SQL de lectura desde archivo o texto, sin interfaz adicional."""
from pathlib import Path
import argparse,json
from corregir_sql import consulta
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--archivo');g.add_argument('--consulta')
    p.add_argument('--db');p.add_argument('--limite',type=int,default=30)
    args=p.parse_args();sql=Path(args.archivo).read_text(encoding='utf-8-sig') if args.archivo else args.consulta
    cols,rows=consulta(sql,args.db)
    print(json.dumps({'columnas':cols,'filas_mostradas':rows[:args.limite],'filas_totales':len(rows)},ensure_ascii=False,indent=2))
