"""Uso: python herramientas/corregir_depuracion.py DB01 mi_trabajo/depuracion/DB01.py
Comprueba tu versión corregida y dice qué comportamiento falta. No muestra la solución."""
from pathlib import Path
import importlib.util
import sys

import pandas as pd

sys.dont_write_bytecode = True


class Revisar(Exception):
    pass


def exigir(cond, msg):
    if not cond:
        raise Revisar(msg)


def cargar(path):
    spec = importlib.util.spec_from_file_location('depuracion_estudiante', Path(path).resolve())
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def db01(m):
    f = getattr(m, 'ventas_por_tienda', None)
    exigir(f, 'Falta la función `ventas_por_tienda`.')
    datos = [{'tienda': 'Sol', 'monto': 30}, {'tienda': 'Luna', 'monto': 20}, {'tienda': 'Sol', 'monto': 5}]
    r = f(datos)
    exigir(r == {'Sol': 35, 'Luna': 20}, f'Con {datos} obtuviste {r}; se esperaba {{"Sol": 35, "Luna": 20}}.')
    exigir(f([]) == {}, 'Con una lista vacía debe devolver {}.')
    return 2


def db02(m):
    f = getattr(m, 'unidades_validas', None)
    exigir(f, 'Falta la función `unidades_validas`.')
    r = f(['3', '4.0', '10'])
    exigir(r == [3, 4, 10] and all(type(x) is int for x in r), f'Con ["3","4.0","10"] obtuviste {r}; se esperaba [3, 4, 10] (enteros).')
    for malo in ('2.5', '3.7', 'abc'):
        try:
            f([malo])
        except ValueError:
            continue
        except Exception as e:
            raise Revisar(f'Con {malo!r} debes lanzar ValueError; lanzaste {type(e).__name__}.')
        raise Revisar(f'Con {malo!r} no lanzaste ValueError. Truncar o ignorar cambia las ventas sin avisar.')
    return 4


def db03(m):
    f = getattr(m, 'ventas_con_categoria', None)
    exigir(f, 'Falta la función `ventas_con_categoria`.')
    ventas = pd.DataFrame({'ticket': [1, 2, 3], 'producto': ['P-01', 'P-02', 'P-01'], 'monto': [100, 50, 80]})
    limpio = pd.DataFrame({'producto': ['P-01', 'P-02'], 'categoria': ['Abarrotes', 'Snacks']})
    r = f(ventas, limpio)
    exigir(len(r) == 3 and r['monto'].sum() == 230 and 'categoria' in r.columns,
           f'Con un catálogo correcto debe devolver 3 filas, total 230 y columna `categoria`; obtuviste {len(r)} filas, total {r["monto"].sum()}.')
    repetido = pd.concat([limpio, limpio.iloc[:1]], ignore_index=True)
    try:
        f(ventas, repetido)
    except ValueError:
        return 2
    except Exception as e:
        raise Revisar(f'Con el catálogo repetido debes lanzar ValueError (o una subclase); lanzaste {type(e).__name__}.')
    raise Revisar('Con un producto repetido en el catálogo tu función devolvió datos en silencio (el total sube). Debe detenerse con un error.')


if __name__ == '__main__':
    tabla = {'DB01': db01, 'DB02': db02, 'DB03': db03}
    if len(sys.argv) != 3 or sys.argv[1].upper() not in tabla:
        raise SystemExit(__doc__)
    try:
        n = tabla[sys.argv[1].upper()](cargar(sys.argv[2]))
        print(f'OK {sys.argv[1].upper()}: {n} comprobaciones. Anota en errores.md: síntoma, causa y cómo lo detectaste.')
    except Revisar as e:
        print(f'REVISAR {sys.argv[1].upper()}: {e}')
        raise SystemExit(1)
    except Exception as e:
        print(f'REVISAR {sys.argv[1].upper()}: tu código falló con {type(e).__name__}: {e}')
        raise SystemExit(1)
