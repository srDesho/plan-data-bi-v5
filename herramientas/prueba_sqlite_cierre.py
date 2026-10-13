"""Prueba reproducible: ninguna herramienta del paquete deja abierta una conexión SQLite.

Contexto (auditoría J-5): `with sqlite3.connect(...) as con:` confirma la transacción pero NO cierra la
conexión. En Windows un archivo abierto no se puede reemplazar ni borrar (WinError 32); en Linux sí.

Uso desde la raíz:  python herramientas/prueba_sqlite_cierre.py
Termina con código 0 si todo pasa. No modifica archivos del paquete: trabaja en un directorio temporal.
"""
from contextlib import closing
from pathlib import Path
import importlib.util
import os
import shutil
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'herramientas'))
sys.dont_write_bytecode = True


def cargar(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def patron_malo(tmp, dest):
    """El patrón que falla en Windows: reemplazar el archivo mientras `con` sigue viva."""
    with sqlite3.connect(tmp) as con:
        con.execute('CREATE TABLE t(x)')
        con.execute('INSERT INTO t VALUES (1)')
        os.replace(tmp, dest)


def patron_bueno(tmp, dest):
    with closing(sqlite3.connect(tmp)) as con:
        with con:
            con.execute('CREATE TABLE t(x)')
            con.execute('INSERT INTO t VALUES (1)')
    os.replace(tmp, dest)


def prueba_demostracion(td):
    resultados = []
    d = Path(td) / 'demo'
    d.mkdir()
    if os.name == 'nt':
        try:
            patron_malo(d / 'a.tmp.db', d / 'a.db')
        except PermissionError:
            resultados.append('patrón `with sqlite3.connect()`: PermissionError reproducido (esperado en Windows)')
        else:
            raise AssertionError('En Windows el patrón malo debía fallar; el comportamiento del sistema cambió')
    else:
        resultados.append('patrón malo: no aplicable fuera de Windows (el archivo abierto sí se puede reemplazar)')
    patron_bueno(d / 'b.tmp.db', d / 'b.db')
    assert (d / 'b.db').exists()
    resultados.append('patrón `closing(...)` + os.replace: correcto')
    return resultados


def prueba_corregir_sql(td):
    """consulta() debe soltar el archivo: si queda abierto, no se puede borrar la copia en Windows."""
    mod = cargar(ROOT / 'herramientas' / 'corregir_sql.py', 'corregir_sql_prueba')
    copia = Path(td) / 'comercial_copia.db'
    shutil.copyfile(ROOT / '04_DATASETS' / 'comercial.db', copia)
    cols, filas = mod.consulta('SELECT COUNT(*) AS n FROM clientes;', copia)
    assert cols == ['n'] and filas == [(120,)], (cols, filas)
    copia.unlink()
    return 'corregir_sql.consulta libera el archivo (copia borrada sin error)'


def prueba_etl_referencia(td):
    """ETL de transferencia + validador: tras ejecutar, el destino se puede renombrar y borrar."""
    etl = cargar(ROOT / '08_SOLUCIONES' / 'etl_nuevo_referencia.py', 'etl_nuevo_prueba')
    val = cargar(ROOT / 'herramientas' / 'validar_final.py', 'validar_final_prueba')
    salida = Path(td) / 'transferencia'
    etl.ejecutar(ROOT / '04_DATASETS' / 'transferencia', salida)
    etl.ejecutar(ROOT / '04_DATASETS' / 'transferencia', salida)       # segunda ejecución sobre el mismo destino
    val.validar(salida, True)
    os.replace(salida / 'resultado.db', salida / 'renombrada.db')        # falla en Windows si algo quedó abierto
    (salida / 'renombrada.db').unlink()
    return 'etl_nuevo_referencia + validar_final: sin archivos abiertos (renombrar y borrar sin error)'


def prueba_etl_distribuidora(td):
    etl = cargar(ROOT / '08_SOLUCIONES' / 'etl_distribuidora.py', 'etl_dist_prueba')
    val = cargar(ROOT / 'herramientas' / 'validar_etl_distribuidora.py', 'validar_dist_prueba')
    etl.DB_OUT = Path(td) / 'etl_dist.db'
    import logging
    logging.disable(logging.CRITICAL)
    try:
        etl.main()
        etl.main()
        val.validar(etl.DB_OUT)
    finally:
        logging.disable(logging.NOTSET)
    os.replace(etl.DB_OUT, Path(td) / 'etl_dist_renombrada.db')
    (Path(td) / 'etl_dist_renombrada.db').unlink()
    return 'etl_distribuidora + validar_etl_distribuidora: sin archivos abiertos'


def prueba_estatica():
    """Todo `sqlite3.connect(...)` de código ejecutable del paquete debe ser el argumento de closing(...)."""
    import ast
    excluir = {'.venv', '.git', '__pycache__', 'originales'}
    malos, revisados = [], 0
    for p in ROOT.rglob('*.py'):
        if excluir & set(p.relative_to(ROOT).parts) or p.name == Path(__file__).name:
            continue
        arbol = ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
        padre = {hijo: nodo for nodo in ast.walk(arbol) for hijo in ast.iter_child_nodes(nodo)}
        for nodo in ast.walk(arbol):
            if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute) and nodo.func.attr == 'connect'
                    and isinstance(nodo.func.value, ast.Name) and nodo.func.value.id == 'sqlite3'):
                revisados += 1
                envoltura = padre.get(nodo)
                nombre = getattr(getattr(envoltura, 'func', None), 'id', None) or getattr(getattr(envoltura, 'func', None), 'attr', None)
                if nombre != 'closing':
                    malos.append(f'{p.relative_to(ROOT)}:{nodo.lineno}')
    assert not malos, 'sqlite3.connect sin closing en: ' + ', '.join(malos)
    return f'{revisados} usos de sqlite3.connect revisados (análisis del código); todos dentro de closing()'


def main():
    pruebas = []
    with tempfile.TemporaryDirectory(prefix='plan_v5_cierre_', ignore_cleanup_errors=True) as td:
        for etiqueta, fn, usa_td in [
            ('demostración', prueba_demostracion, True),
            ('corregir_sql', prueba_corregir_sql, True),
            ('ETL transferencia', prueba_etl_referencia, True),
            ('ETL distribuidora', prueba_etl_distribuidora, True),
            ('revisión estática', prueba_estatica, False),
        ]:
            try:
                detalle = fn(td) if usa_td else fn()
                for linea in (detalle if isinstance(detalle, list) else [detalle]):
                    print('OK   ', etiqueta, '·', linea)
                pruebas.append(True)
            except Exception as e:
                print('ERROR', etiqueta, '·', type(e).__name__, str(e)[:300])
                pruebas.append(False)
    print(f'Resumen: {sum(pruebas)}/{len(pruebas)} grupos correctos · sistema: {os.name} ({sys.platform})')
    raise SystemExit(0 if all(pruebas) else 1)


if __name__ == '__main__':
    main()
