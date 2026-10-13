"""Uso: python herramientas/corregir_python.py P09 mi_trabajo/python/mis_funciones.py"""
from pathlib import Path
import importlib.util
import sys
from contratos_python import comprobar

def cargar(path):
    spec=importlib.util.spec_from_file_location('funciones_estudiante',Path(path).resolve())
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    try:
        n=comprobar(sys.argv[1],cargar(sys.argv[2]))
        print(f'OK {sys.argv[1]}: {n} casos aprobados. Explica tu razonamiento y prueba una entrada nueva.')
    except Exception as e:
        print(f'REVISAR {sys.argv[1]}: {type(e).__name__}: {e}')
        raise SystemExit(1)

if __name__=='__main__':main()
