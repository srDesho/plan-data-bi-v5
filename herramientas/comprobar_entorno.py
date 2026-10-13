"""Comprueba dependencias y acceso a los datasets, sin abrir soluciones."""
from pathlib import Path
import importlib,sys,sqlite3
ROOT=Path(__file__).resolve().parents[1]
if sys.version_info<(3,11):raise SystemExit('Se requiere Python 3.11 o posterior; se probó 3.12')
for name in ['pandas','numpy','scipy','matplotlib','nbformat']:
    module=importlib.import_module(name);print(name,getattr(module,'__version__','disponible'))
with sqlite3.connect((ROOT/'04_DATASETS/comercial.db').as_uri()+'?mode=ro',uri=True) as con:
    assert con.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]==120
print('OK entorno y datos. Empieza por el Día 1, sin abrir las soluciones.')
