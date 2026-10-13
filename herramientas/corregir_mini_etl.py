"""Corrector del mini-ETL. Muestra QUÉ falló y con qué dato, pero no el código de la referencia.

Uso:  python herramientas/corregir_mini_etl.py ME01 mi_trabajo/mini_etl/mini_etl.py
      ME01 extraer + quitar_exactos + perfilar · ME02 transformar · ME03 ejecutar (carga y cuadre)
      ME04 ejecutar con la regla nueva (unidades > 500) sobre el raw v2
"""
from contextlib import closing
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import sqlite3
import sys
import tempfile

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATOS = ROOT / '04_DATASETS' / 'mini_etl'
CONTROL = json.loads((ROOT / '08_SOLUCIONES' / 'controles_mini_etl.json').read_text(encoding='utf-8'))
sys.dont_write_bytecode = True


class Revisar(Exception):
    """Hallazgo para el estudiante (no es un fallo del corrector)."""


def exigir(condicion, mensaje):
    if not condicion:
        raise Revisar(mensaje)


def cargar(path):
    spec = importlib.util.spec_from_file_location('mini_etl_estudiante', Path(path).resolve())
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def funcion(modulo, nombre):
    exigir(hasattr(modulo, nombre), f'Falta la función `{nombre}` en tu archivo.')
    return getattr(modulo, nombre)


def comparar_filas(obtenido, esperado, columnas, etiqueta):
    """Compara DataFrame/lista con las filas esperadas y señala la primera diferencia concreta."""
    obt = {str(r[0]): r for r in obtenido[columnas].itertuples(index=False, name=None)}
    esp = {str(r[0]): r for r in esperado}
    faltan = sorted(set(esp) - set(obt))
    sobran = sorted(set(obt) - set(esp))
    exigir(not faltan, f'{etiqueta}: faltan filas con clave {faltan}.')
    exigir(not sobran, f'{etiqueta}: sobran filas con clave {sobran} (¿debían rechazarse o eliminarse?).')
    for clave in sorted(esp):
        for i, nombre in enumerate(columnas):
            a, e = obt[clave][i], esp[clave][i]
            exigir(str(a) == str(e) if isinstance(e, str) else a == e,
                   f'{etiqueta}: clave {clave}, columna `{nombre}`: obtuviste {a!r} y se esperaba {e!r}.')


def leer_tabla(db, nombre):
    with closing(sqlite3.connect(db)) as con:
        return pd.read_sql(f'SELECT * FROM {nombre}', con)


def entrada_v(variante, td):
    """Carpeta temporal con el raw de la variante pedida (el raw v2 se copia como ventas_mini_raw.csv)."""
    d = Path(td) / f'entrada_{variante}'
    d.mkdir()
    shutil.copy(DATOS / 'productos_mini.csv', d / 'productos_mini.csv')
    shutil.copy(DATOS / ('ventas_mini_raw_v2.csv' if variante == 2 else 'ventas_mini_raw.csv'), d / 'ventas_mini_raw.csv')
    return d


def me01(m):
    n = 0
    extraer, quitar, perfilar = funcion(m, 'extraer'), funcion(m, 'quitar_exactos'), funcion(m, 'perfilar')
    raw = extraer(DATOS / 'ventas_mini_raw.csv')
    exigir(isinstance(raw, pd.DataFrame), '`extraer` debe devolver un DataFrame.')
    exigir(list(raw.columns) == CONTROL['v1']['columnas_raw'], f'Columnas obtenidas {list(raw.columns)}; se esperaban {CONTROL["v1"]["columnas_raw"]}.')
    exigir(len(raw) == CONTROL['v1']['filas_raw'], f'`extraer` devolvió {len(raw)} filas; el archivo tiene {CONTROL["v1"]["filas_raw"]}.')
    exigir(all(isinstance(v, str) for v in raw.to_numpy().ravel()),
           'Bronze debe conservar TODO como texto (dtype=str). Hay valores convertidos a número o NaN.')
    exigir(raw.loc[0, 'tienda'] == ' Tienda Sol ', 'Bronze no debe limpiar nada: la primera tienda debe seguir siendo " Tienda Sol " con espacios.')
    exigir(raw.loc[2, 'unidades'] == '4.0', 'Bronze no debe convertir: la fila 3 debe conservar el texto "4.0".')
    n += 5
    copia = raw.copy()
    sin = quitar(raw)
    exigir(len(sin) == len(copia) - 2, f'`quitar_exactos` dejó {len(sin)} filas; se esperaban {len(copia) - 2} (2 duplicados exactos).')
    exigir(list(sin.index) == list(range(len(sin))), '`quitar_exactos` debe devolver el índice reiniciado (0, 1, 2…).')
    exigir(raw.equals(copia), '`quitar_exactos` modificó el DataFrame de entrada; debe devolver uno nuevo.')
    n += 3
    perfil = perfilar(raw)
    exigir(isinstance(perfil, dict), '`perfilar` debe devolver un diccionario.')
    exigir(perfil.get('filas') == 24, f'perfil["filas"] = {perfil.get("filas")!r}; se esperaba 24.')
    exigir(perfil.get('duplicados_exactos') == 2, f'perfil["duplicados_exactos"] = {perfil.get("duplicados_exactos")!r}; se esperaba 2.')
    return n + 3


def me02(m):
    transformar = funcion(m, 'transformar')
    raw = pd.read_csv(DATOS / 'ventas_mini_raw.csv', sep=';', dtype=str, keep_default_na=False)
    cat = pd.read_csv(DATOS / 'productos_mini.csv', dtype=str, keep_default_na=False)
    antes = raw.copy()
    resultado = transformar(raw, cat)
    exigir(isinstance(resultado, tuple) and len(resultado) == 2, '`transformar` debe devolver (silver, rechazos).')
    silver, rechazos = resultado
    exigir(raw.equals(antes), '`transformar` modificó el raw de entrada. Bronze debe quedar intacto: trabaja sobre una copia.')
    cols = CONTROL['v1']['silver_columnas']
    exigir(list(silver.columns) == cols, f'Columnas de Silver {list(silver.columns)}; se esperaban {cols}.')
    comparar_filas(silver, CONTROL['v1']['silver'], cols, 'Silver')
    exigir({'ticket_id', 'motivos'} <= set(rechazos.columns), 'Rechazos necesita al menos las columnas `ticket_id` y `motivos`.')
    obtenidos = {str(r.ticket_id): str(r.motivos) for r in rechazos.itertuples()}
    esperados = CONTROL['v1']['rechazos']
    exigir(set(obtenidos) == set(esperados),
           f'Rechazos: obtuviste {sorted(obtenidos)} y se esperaban {sorted(esperados)}.')
    for clave, palabra in esperados.items():
        exigir(palabra in obtenidos[clave].lower(),
               f'Rechazo {clave}: la causa debe mencionar "{palabra}"; escribiste {obtenidos[clave]!r}.')
    return len(CONTROL['v1']['silver']) + len(esperados) + 3


def verificar_db(db, esperado, variante):
    n = 0
    for tabla in ('bronze', 'silver', 'rechazos', 'gold'):
        with closing(sqlite3.connect(db)) as con:
            existe = con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (tabla,)).fetchone()[0]
        exigir(existe, f'Falta la tabla `{tabla}` en {Path(db).name}.')
        n += 1
    met = esperado['metricas']
    exigir(len(leer_tabla(db, 'bronze')) == met['bronze'], f'bronze tiene {len(leer_tabla(db, "bronze"))} filas; se esperaban {met["bronze"]}.')
    exigir(len(leer_tabla(db, 'silver')) == met['silver'], f'silver tiene {len(leer_tabla(db, "silver"))} filas; se esperaban {met["silver"]}.')
    exigir(len(leer_tabla(db, 'rechazos')) == met['rechazados'], f'rechazos tiene {len(leer_tabla(db, "rechazos"))} filas; se esperaban {met["rechazados"]}.')
    with closing(sqlite3.connect(db)) as con:
        ventas = con.execute("SELECT COALESCE(SUM(monto_centavos),0) FROM silver WHERE estado='entregado'").fetchone()[0]
        gold_total = con.execute('SELECT COALESCE(SUM(ventas_centavos),0) FROM gold').fetchone()[0]
    exigir(ventas == met['ventas_centavos'], f'Ventas entregadas en Silver = {ventas} centavos; se esperaban {met["ventas_centavos"]}.')
    exigir(gold_total == met['ventas_centavos'], f'La suma de Gold = {gold_total}; no cuadra con Silver ({met["ventas_centavos"]}).')
    n += 5
    if variante == 1:
        cols = CONTROL['v1']['silver_columnas']
        comparar_filas(leer_tabla(db, 'silver'), CONTROL['v1']['silver'], cols, 'Tabla silver')
        gcols = CONTROL['v1']['gold_columnas']
        comparar_filas(leer_tabla(db, 'gold').assign(clave=lambda d: d['tienda'] + '|' + d['mes'])[['clave'] + gcols[2:]],
                       [[f'{r[0]}|{r[1]}'] + r[2:] for r in CONTROL['v1']['gold']], ['clave'] + gcols[2:], 'Tabla gold')
        n += 2
    return n


def me03(m):
    ejecutar = funcion(m, 'ejecutar')
    n = 0
    with tempfile.TemporaryDirectory(prefix='mini_etl_', ignore_cleanup_errors=True) as td:
        salida = Path(td) / 'salida'
        met1 = ejecutar(DATOS, salida)
        exigir(isinstance(met1, dict), '`ejecutar` debe devolver un diccionario con bronze, duplicados_exactos, rechazados, silver y ventas_centavos.')
        for k, v in CONTROL['v1']['metricas'].items():
            exigir(met1.get(k) == v, f'metricas["{k}"] = {met1.get(k)!r}; se esperaba {v!r}.')
        n += 5
        db = salida / 'mini.db'
        exigir(db.exists(), 'No existe salida/mini.db.')
        n += verificar_db(db, CONTROL['v1'], 1)
        exigir(met1['bronze'] == met1['duplicados_exactos'] + met1['rechazados'] + met1['silver'], 'La ecuación bronze = duplicados + rechazados + silver no se cumple.')
        met2 = ejecutar(DATOS, salida)
        exigir(met2 == met1, f'La segunda ejecución cambió las métricas: {met2} frente a {met1}. Una carga repetible no duplica.')
        verificar_db(db, CONTROL['v1'], 1)
        n += 2
        try:
            os.replace(db, Path(td) / 'renombrada.db')
        except PermissionError:
            raise Revisar('Dejaste abierta la conexión SQLite: en Windows el archivo no se puede renombrar ni borrar (WinError 32). '
                          'Usa `with contextlib.closing(sqlite3.connect(...)) as con:` y mira 02_TEORIA/19_Puente_Python_a_ETL.md §4.')
        shutil.copyfile(Path(td) / 'renombrada.db', db)
        n += 1
        previo = hashlib.sha256(db.read_bytes()).hexdigest()
        malo = Path(td) / 'conflicto'
        malo.mkdir()
        shutil.copy(DATOS / 'productos_mini.csv', malo / 'productos_mini.csv')
        lineas = (DATOS / 'ventas_mini_raw.csv').read_text(encoding='utf-8').splitlines()
        lineas.append('T001;2026-09-01; Tienda Sol ;P-01;3; ENTREGADO ;Bs 99,99')       # misma clave, contenido distinto
        (malo / 'ventas_mini_raw.csv').write_text('\n'.join(lineas) + '\n', encoding='utf-8')
        try:
            ejecutar(malo, salida)
        except ValueError:
            pass
        except Exception as e:
            raise Revisar(f'Con un ticket repetido y contenido distinto debes lanzar ValueError; lanzaste {type(e).__name__}.')
        else:
            raise Revisar('Un ticket_id repetido con contenido distinto (T001) debe detener la carga con ValueError; tu proceso continuó.')
        exigir(hashlib.sha256(db.read_bytes()).hexdigest() == previo, 'Tras el error, la salida anterior cambió. Publica solo después de validar (archivo temporal + os.replace).')
        n += 2
        sin_columna = Path(td) / 'sin_columna'
        sin_columna.mkdir()
        shutil.copy(DATOS / 'productos_mini.csv', sin_columna / 'productos_mini.csv')
        (sin_columna / 'ventas_mini_raw.csv').write_text((DATOS / 'ventas_mini_raw.csv').read_text(encoding='utf-8').replace('precio', 'valor', 1), encoding='utf-8')
        try:
            ejecutar(sin_columna, Path(td) / 'otra')
        except ValueError:
            n += 1
        except Exception as e:
            raise Revisar(f'Con una columna obligatoria ausente debes lanzar ValueError con un mensaje legible; lanzaste {type(e).__name__}.')
        else:
            raise Revisar('Falta la columna `precio` y tu proceso no se detuvo. Valida la estructura antes de transformar.')
    return n


def me04(m):
    ejecutar = funcion(m, 'ejecutar')
    with tempfile.TemporaryDirectory(prefix='mini_etl_v2_', ignore_cleanup_errors=True) as td:
        entrada = entrada_v(2, td)
        met = ejecutar(entrada, Path(td) / 'salida')
        for k, v in CONTROL['v2']['metricas'].items():
            exigir(met.get(k) == v, f'metricas["{k}"] = {met.get(k)!r}; se esperaba {v!r} (regla nueva: unidades > 500 se rechazan por "unidades").')
        db = Path(td) / 'salida' / 'mini.db'
        rech = {str(r.ticket_id): str(r.motivos).lower() for r in leer_tabla(db, 'rechazos').itertuples()}
        for clave in ('T024', 'T026'):
            exigir(clave in rech, f'{clave} (900 y 600 unidades) debía rechazarse.')
            exigir('unidades' in rech[clave], f'{clave}: la causa debe mencionar "unidades"; escribiste {rech[clave]!r}.')
        verificar_db(db, CONTROL['v2'], 2)
        met1 = ejecutar(DATOS, Path(td) / 'salida1')
        exigir(met1 == CONTROL['v1']['metricas'], 'La regla nueva no debe cambiar el resultado con el raw original (ME03 dejó de cumplirse).')
    return 12


FUNCIONES = {'ME01': me01, 'ME02': me02, 'ME03': me03, 'ME04': me04}

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1].upper() not in FUNCIONES:
        raise SystemExit(__doc__)
    try:
        comprobaciones = FUNCIONES[sys.argv[1].upper()](cargar(sys.argv[2]))
        print(f'OK {sys.argv[1].upper()}: {comprobaciones} comprobaciones. Explica cada regla con un ejemplo y escribe un aprendizaje en errores.md.')
    except Revisar as e:
        print(f'REVISAR {sys.argv[1].upper()}: {e}')
        raise SystemExit(1)
    except Exception as e:
        print(f'REVISAR {sys.argv[1].upper()}: tu código falló con {type(e).__name__}: {e}')
        if isinstance(e, PermissionError):
            print('Pista: una conexión SQLite sigue abierta al reemplazar o borrar el archivo. `with sqlite3.connect()` NO la cierra: '
                  'usa `contextlib.closing` (02_TEORIA/19_Puente_Python_a_ETL.md §4).')
        else:
            print('Lee la ÚLTIMA línea del traceback y busca la línea de TU archivo (02_TEORIA/19_Puente_Python_a_ETL.md §1).')
        raise SystemExit(1)
