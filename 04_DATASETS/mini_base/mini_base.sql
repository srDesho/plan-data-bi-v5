-- Mini-base didáctica de las lecciones. Datos inventados. Generado por herramientas/crear_mini_base.py

CREATE TABLE tiendas (tienda_id INTEGER PRIMARY KEY, nombre TEXT, tipo TEXT, zona TEXT, ruta TEXT, fecha_alta TEXT);
CREATE TABLE articulos (articulo_id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, precio REAL);
CREATE TABLE vendedores_ej (vendedor_id INTEGER PRIMARY KEY, nombre TEXT, ruta TEXT);
CREATE TABLE ventas (venta_id INTEGER PRIMARY KEY, tienda_id INTEGER, vendedor_id INTEGER, fecha TEXT, estado TEXT);
CREATE TABLE venta_lineas (linea_id INTEGER PRIMARY KEY, venta_id INTEGER, articulo_id INTEGER, cantidad INTEGER, precio_unitario REAL);
CREATE TABLE metas (mes TEXT, ruta TEXT, meta_bs REAL);
CREATE TABLE visitas_ej (visita_id INTEGER PRIMARY KEY, fecha TEXT, tienda_id INTEGER, planificada INTEGER, realizada INTEGER, pedido_tomado INTEGER);

INSERT INTO tiendas VALUES
  (1, 'Tienda La Palma', 'Tienda de barrio', 'Norte', 'R01', '2025-02-10'),
  (2, 'Kiosco El Faro', 'Kiosco', 'Centro', 'R01', '2025-03-01'),
  (3, 'Farmacia Salud', 'Farmacia', 'Centro', 'R02', '2025-03-15'),
  (4, 'Minimarket Sol Naciente', 'Minimarket', 'Norte', 'R02', '2025-05-20'),
  (5, '  Kiosco La Esquina ', 'Kiosco', NULL, 'R03', '2025-06-02'),
  (6, 'Restaurante Sabor', 'Restaurante', 'Equipetrol', 'R03', '2025-06-18'),
  (7, 'Tienda Don Pepe', 'Tienda de barrio', 'Plan 3000', 'R01', '2025-07-07'),
  (8, 'Farmacia Vida', 'Farmacia', NULL, 'R02', '2025-08-11'),
  (9, 'Minimarket Central', 'Minimarket', 'Centro', 'R03', '2025-09-09'),
  (10, 'Kiosco Luna', 'Kiosco', 'Norte', 'R01', '2025-10-30'),
  (11, 'Tienda Nueva Esperanza', 'Tienda de barrio', 'Plan 3000', 'R03', '2026-01-15'),
  (12, 'Restaurante El Buen Gusto', 'Restaurante', 'Centro', 'R02', '2026-02-20');

INSERT INTO articulos VALUES
  (1, 'Agua 2L', 'Bebidas', 6.0),
  (2, 'Jugo 1L', 'Bebidas', 9.0),
  (3, 'Gaseosa 2L', 'Bebidas', 11.5),
  (4, 'Papas 100g', 'Snacks', 7.5),
  (5, 'Galletas', 'Snacks', 4.5),
  (6, 'Maní 80g', 'Snacks', 5.0),
  (7, 'Detergente 1kg', 'Limpieza', 14.0),
  (8, 'Jabón', 'Limpieza', 3.5),
  (9, 'Leche 1L', 'Lácteos', 8.0),
  (10, 'Yogurt 1L', 'Lácteos', 12.0);

INSERT INTO vendedores_ej VALUES
  (1, 'Ana', 'R01'),
  (2, 'Luis', 'R02'),
  (3, 'Marta', 'R03'),
  (4, 'Pedro', 'R01');

INSERT INTO ventas VALUES
  (1, 1, 1, '2026-08-03', 'entregado'),
  (2, 2, 1, '2026-08-05', 'entregado'),
  (3, 3, 2, '2026-08-07', 'entregado'),
  (4, 4, 2, '2026-08-12', 'anulado'),
  (5, 1, 1, '2026-08-19', 'entregado'),
  (6, 5, 3, '2026-08-21', 'entregado'),
  (7, 6, 3, '2026-08-28', 'entregado'),
  (8, 2, 1, '2026-09-02', 'entregado'),
  (9, 3, 2, '2026-09-04', 'entregado'),
  (10, 7, 1, '2026-09-08', 'entregado'),
  (11, 4, 2, '2026-09-10', 'entregado'),
  (12, 9, 3, '2026-09-15', 'entregado'),
  (13, 9, 3, '2026-09-18', 'anulado'),
  (14, 1, 1, '2026-09-22', 'entregado'),
  (15, 10, 1, '2026-09-25', 'entregado'),
  (16, 3, 2, '2026-09-29', 'entregado');

INSERT INTO venta_lineas VALUES
  (1, 1, 1, 10, 6.0),
  (2, 1, 4, 6, 7.5),
  (3, 1, 9, 4, 8.0),
  (4, 2, 3, 8, 11.5),
  (5, 2, 5, 12, 4.5),
  (6, 3, 7, 3, 14.0),
  (7, 3, 8, 10, 3.5),
  (8, 3, 2, 6, 9.0),
  (9, 4, 3, 20, 11.5),
  (10, 4, 1, 15, 6.0),
  (11, 5, 1, 12, 6.0),
  (12, 5, 6, 10, 5.0),
  (13, 5, 10, 5, 12.0),
  (14, 6, 2, 8, 9.0),
  (15, 6, 4, 5, 7.5),
  (16, 7, 9, 12, 8.0),
  (17, 7, 10, 6, 12.0),
  (18, 7, 1, 20, 6.0),
  (19, 8, 3, 10, 11.5),
  (20, 8, 4, 8, 7.5),
  (21, 8, 5, 6, 4.5),
  (22, 9, 7, 2, 14.0),
  (23, 9, 8, 12, 3.5),
  (24, 10, 1, 15, 6.0),
  (25, 10, 2, 10, 9.0),
  (26, 10, 6, 8, 5.0),
  (27, 11, 5, 20, 4.5),
  (28, 11, 4, 10, 7.5),
  (29, 12, 9, 8, 8.0),
  (30, 12, 10, 8, 12.0),
  (31, 13, 3, 6, 11.5),
  (32, 14, 1, 18, 6.0),
  (33, 14, 3, 6, 11.5),
  (34, 14, 9, 6, 8.0),
  (35, 15, 2, 12, 9.0),
  (36, 15, 5, 10, 4.5),
  (37, 16, 7, 4, 14.0),
  (38, 16, 10, 5, 12.0),
  (39, 16, 8, 8, 3.5);

INSERT INTO metas VALUES
  ('2026-08', 'R01', 450.0),
  ('2026-08', 'R02', 280.0),
  ('2026-08', 'R03', 320.0),
  ('2026-09', 'R01', 600.0),
  ('2026-09', 'R02', 450.0),
  ('2026-09', 'R03', 300.0);

INSERT INTO visitas_ej VALUES
  (1, '2026-09-01', 1, 1, 1, 0),
  (2, '2026-09-01', 2, 1, 1, 1),
  (3, '2026-09-01', 3, 1, 1, 1),
  (4, '2026-09-01', 5, 1, 0, 0),
  (5, '2026-09-02', 4, 1, 1, 1),
  (6, '2026-09-02', 6, 1, 1, 0),
  (7, '2026-09-02', 7, 1, 0, 0),
  (8, '2026-09-03', 1, 1, 1, 1),
  (9, '2026-09-03', 3, 1, 1, 0),
  (10, '2026-09-03', 9, 1, 1, 1),
  (11, '2026-09-04', 2, 1, 1, 0),
  (12, '2026-09-04', 8, 1, 0, 0),
  (13, '2026-09-04', 10, 1, 1, 1),
  (14, '2026-09-05', 1, 1, 1, 1);
