"""Crea la mini-base didáctica de las lecciones (04_DATASETS/mini_base): SQL, base SQLite y CSV.

Los datos son inventados y distintos de `comercial.db`: las lecciones los usan para que los ejemplos no coincidan con los ejercicios.
Uso desde la raíz:  python herramientas/crear_mini_base.py   (regenera los archivos; son siempre los mismos)
"""
from contextlib import closing
from pathlib import Path
import csv
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / '04_DATASETS' / 'mini_base'

TIENDAS = [
    (1, 'Tienda La Palma', 'Tienda de barrio', 'Norte', 'R01', '2025-02-10'),
    (2, 'Kiosco El Faro', 'Kiosco', 'Centro', 'R01', '2025-03-01'),
    (3, 'Farmacia Salud', 'Farmacia', 'Centro', 'R02', '2025-03-15'),
    (4, 'Minimarket Sol Naciente', 'Minimarket', 'Norte', 'R02', '2025-05-20'),
    (5, '  Kiosco La Esquina ', 'Kiosco', None, 'R03', '2025-06-02'),
    (6, 'Restaurante Sabor', 'Restaurante', 'Equipetrol', 'R03', '2025-06-18'),
    (7, 'Tienda Don Pepe', 'Tienda de barrio', 'Plan 3000', 'R01', '2025-07-07'),
    (8, 'Farmacia Vida', 'Farmacia', None, 'R02', '2025-08-11'),
    (9, 'Minimarket Central', 'Minimarket', 'Centro', 'R03', '2025-09-09'),
    (10, 'Kiosco Luna', 'Kiosco', 'Norte', 'R01', '2025-10-30'),
    (11, 'Tienda Nueva Esperanza', 'Tienda de barrio', 'Plan 3000', 'R03', '2026-01-15'),
    (12, 'Restaurante El Buen Gusto', 'Restaurante', 'Centro', 'R02', '2026-02-20'),
]
ARTICULOS = [
    (1, 'Agua 2L', 'Bebidas', 6.00), (2, 'Jugo 1L', 'Bebidas', 9.00), (3, 'Gaseosa 2L', 'Bebidas', 11.50),
    (4, 'Papas 100g', 'Snacks', 7.50), (5, 'Galletas', 'Snacks', 4.50), (6, 'Maní 80g', 'Snacks', 5.00),
    (7, 'Detergente 1kg', 'Limpieza', 14.00), (8, 'Jabón', 'Limpieza', 3.50),
    (9, 'Leche 1L', 'Lácteos', 8.00), (10, 'Yogurt 1L', 'Lácteos', 12.00),
]
VENDEDORES = [(1, 'Ana', 'R01'), (2, 'Luis', 'R02'), (3, 'Marta', 'R03'), (4, 'Pedro', 'R01')]
# venta_id, tienda_id, vendedor_id, fecha, estado
VENTAS = [
    (1, 1, 1, '2026-08-03', 'entregado'), (2, 2, 1, '2026-08-05', 'entregado'), (3, 3, 2, '2026-08-07', 'entregado'),
    (4, 4, 2, '2026-08-12', 'anulado'), (5, 1, 1, '2026-08-19', 'entregado'), (6, 5, 3, '2026-08-21', 'entregado'),
    (7, 6, 3, '2026-08-28', 'entregado'), (8, 2, 1, '2026-09-02', 'entregado'), (9, 3, 2, '2026-09-04', 'entregado'),
    (10, 7, 1, '2026-09-08', 'entregado'), (11, 4, 2, '2026-09-10', 'entregado'), (12, 9, 3, '2026-09-15', 'entregado'),
    (13, 9, 3, '2026-09-18', 'anulado'), (14, 1, 1, '2026-09-22', 'entregado'), (15, 10, 1, '2026-09-25', 'entregado'),
    (16, 3, 2, '2026-09-29', 'entregado'),
]
# venta_id: [(articulo_id, cantidad, precio_unitario)]
LINEAS = {
    1: [(1, 10, 6.00), (4, 6, 7.50), (9, 4, 8.00)],
    2: [(3, 8, 11.50), (5, 12, 4.50)],
    3: [(7, 3, 14.00), (8, 10, 3.50), (2, 6, 9.00)],
    4: [(3, 20, 11.50), (1, 15, 6.00)],
    5: [(1, 12, 6.00), (6, 10, 5.00), (10, 5, 12.00)],
    6: [(2, 8, 9.00), (4, 5, 7.50)],
    7: [(9, 12, 8.00), (10, 6, 12.00), (1, 20, 6.00)],
    8: [(3, 10, 11.50), (4, 8, 7.50), (5, 6, 4.50)],
    9: [(7, 2, 14.00), (8, 12, 3.50)],
    10: [(1, 15, 6.00), (2, 10, 9.00), (6, 8, 5.00)],
    11: [(5, 20, 4.50), (4, 10, 7.50)],
    12: [(9, 8, 8.00), (10, 8, 12.00)],
    13: [(3, 6, 11.50)],
    14: [(1, 18, 6.00), (3, 6, 11.50), (9, 6, 8.00)],
    15: [(2, 12, 9.00), (5, 10, 4.50)],
    16: [(7, 4, 14.00), (10, 5, 12.00), (8, 8, 3.50)],
}
METAS = [('2026-08', 'R01', 450.0), ('2026-08', 'R02', 280.0), ('2026-08', 'R03', 320.0),
         ('2026-09', 'R01', 600.0), ('2026-09', 'R02', 450.0), ('2026-09', 'R03', 300.0)]
# visita_id, fecha, tienda_id, planificada, realizada, pedido_tomado
VISITAS = [
    (1, '2026-09-01', 1, 1, 1, 0), (2, '2026-09-01', 2, 1, 1, 1), (3, '2026-09-01', 3, 1, 1, 1), (4, '2026-09-01', 5, 1, 0, 0),
    (5, '2026-09-02', 4, 1, 1, 1), (6, '2026-09-02', 6, 1, 1, 0), (7, '2026-09-02', 7, 1, 0, 0), (8, '2026-09-03', 1, 1, 1, 1),
    (9, '2026-09-03', 3, 1, 1, 0), (10, '2026-09-03', 9, 1, 1, 1), (11, '2026-09-04', 2, 1, 1, 0), (12, '2026-09-04', 8, 1, 0, 0),
    (13, '2026-09-04', 10, 1, 1, 1), (14, '2026-09-05', 1, 1, 1, 1),
]

ESQUEMA = """
CREATE TABLE tiendas (tienda_id INTEGER PRIMARY KEY, nombre TEXT, tipo TEXT, zona TEXT, ruta TEXT, fecha_alta TEXT);
CREATE TABLE articulos (articulo_id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, precio REAL);
CREATE TABLE vendedores_ej (vendedor_id INTEGER PRIMARY KEY, nombre TEXT, ruta TEXT);
CREATE TABLE ventas (venta_id INTEGER PRIMARY KEY, tienda_id INTEGER, vendedor_id INTEGER, fecha TEXT, estado TEXT);
CREATE TABLE venta_lineas (linea_id INTEGER PRIMARY KEY, venta_id INTEGER, articulo_id INTEGER, cantidad INTEGER, precio_unitario REAL);
CREATE TABLE metas (mes TEXT, ruta TEXT, meta_bs REAL);
CREATE TABLE visitas_ej (visita_id INTEGER PRIMARY KEY, fecha TEXT, tienda_id INTEGER, planificada INTEGER, realizada INTEGER, pedido_tomado INTEGER);
"""


def filas_lineas():
    n = 0
    for venta, ls in LINEAS.items():
        for art, cant, precio in ls:
            n += 1
            yield (n, venta, art, cant, precio)


TABLAS = {'tiendas': TIENDAS, 'articulos': ARTICULOS, 'vendedores_ej': VENDEDORES, 'ventas': VENTAS,
          'venta_lineas': list(filas_lineas()), 'metas': METAS, 'visitas_ej': VISITAS}
ENCABEZADOS = {'tiendas': 'tienda_id,nombre,tipo,zona,ruta,fecha_alta', 'articulos': 'articulo_id,nombre,categoria,precio',
               'vendedores_ej': 'vendedor_id,nombre,ruta', 'ventas': 'venta_id,tienda_id,vendedor_id,fecha,estado',
               'venta_lineas': 'linea_id,venta_id,articulo_id,cantidad,precio_unitario', 'metas': 'mes,ruta,meta_bs',
               'visitas_ej': 'visita_id,fecha,tienda_id,planificada,realizada,pedido_tomado'}


def literal(v):
    if v is None:
        return 'NULL'
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    return repr(v)


def sql_texto():
    partes = ['-- Mini-base didáctica de las lecciones. Datos inventados. Generado por herramientas/crear_mini_base.py\n', ESQUEMA.strip() + '\n']
    for tabla, filas in TABLAS.items():
        partes.append(f'INSERT INTO {tabla} VALUES')
        partes.append(',\n'.join('  (' + ', '.join(literal(v) for v in f) + ')' for f in filas) + ';\n')
    return '\n'.join(partes)


def crear():
    DESTINO.mkdir(parents=True, exist_ok=True)
    (DESTINO / 'mini_base.sql').write_text(sql_texto(), encoding='utf-8')
    db = DESTINO / 'mini_base.db'
    if db.exists():
        db.unlink()
    with closing(sqlite3.connect(db)) as con:
        con.executescript(sql_texto())
        con.commit()
    for tabla, filas in TABLAS.items():
        nombre = {'vendedores_ej': 'vendedores', 'visitas_ej': 'visitas'}.get(tabla, tabla)
        with (DESTINO / f'{nombre}.csv').open('w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(ENCABEZADOS[tabla].split(','))
            for fila in filas:
                w.writerow(['' if v is None else v for v in fila])


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    crear()
    print('mini_base creada en', DESTINO)
