"""Piezas comunes de los validadores de ETL (validar_final.py y validar_etl_distribuidora.py).

Un validador debe comprobar filas y agrupaciones, no solo cantidades de registros y sumas globales. Este módulo aporta:

* ``a_centavos``: regla explícita para pasar importes en Bs (REAL con dos decimales) a centavos enteros.
* ``canon`` / ``huella``: forma canónica de una fila y su huella SHA-256 con sal. Permiten comparar tablas completas
  contra un oráculo que NO publica los valores esperados (``Oraculo.desde_huellas``) o contra tablas esperadas
  completas (``Oraculo.desde_tablas``) con exactamente el mismo código.
* ``Informe``: acumula todos los fallos (no se detiene en el primero) para que se vea qué grupo falla.

No es custodia privada: quien ejecuta el validador puede ver QUÉ filas no coinciden (por su clave), no los valores
esperados. Quien tenga el archivo de huellas podría intentar adivinar valores por fuerza bruta; para una prueba ciega
real hace falta que otra persona guarde la referencia (ver 09_EVALUACION_FINAL/ENUNCIADO.md).
"""
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json

import pandas as pd


# ───────────────────────────── dinero ─────────────────────────────
def a_centavos(valor):
    """Importe en Bs (int, float, str o Decimal) → centavos enteros, redondeando al centavo más cercano (mitad hacia arriba).

    Es la regla de conversión de los proyectos que guardan Bs como REAL con dos decimales (ETL guiado): se pasa por el texto
    más corto del número (``repr``) y no por la representación binaria, para que 4.35 sea 435 y no 434.
    """
    if valor is None or (isinstance(valor, float) and valor != valor):
        raise ValueError('importe vacío')
    d = Decimal(repr(valor) if isinstance(valor, float) else str(valor).strip())
    return int((d * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def tiene_dos_decimales(valor):
    """True si el importe en Bs no tiene fracciones de centavo (las toleradas son errores de coma flotante < 1e-7)."""
    d = Decimal(repr(valor) if isinstance(valor, float) else str(valor).strip()) * 100
    return abs(d - d.to_integral_value()) < Decimal('1e-7')


# ───────────────────────────── huellas ─────────────────────────────
def canon(valor):
    """Texto canónico de una celda: enteros sin '.0', None/NaN vacíos, textos sin espacios alrededor."""
    if valor is None or (isinstance(valor, float) and valor != valor):
        return ''
    if isinstance(valor, bool):
        return str(int(valor))
    if isinstance(valor, float) and valor == int(valor):
        return str(int(valor))
    return str(valor).strip()


def clave_texto(fila, columnas):
    return '|'.join(canon(fila[c]) for c in columnas)


def huella(sal, clave, fila_canonica):
    return hashlib.sha256(f'{sal}\x1f{clave}\x1f{fila_canonica}'.encode('utf-8')).hexdigest()[:16]


def huella_escalar(sal, nombre, valor):
    return hashlib.sha256(f'{sal}\x1f{nombre}\x1f{canon(valor)}'.encode('utf-8')).hexdigest()[:16]


def huellas_tabla(frame, clave, columnas, sal):
    """{clave_texto: huella de la fila} de un DataFrame. Falla si la clave se repite."""
    salida = {}
    for fila in frame.to_dict('records'):
        k = clave_texto(fila, clave)
        if k in salida:
            raise ValueError(f'clave repetida: {k}')
        salida[k] = huella(sal, k, '|'.join(canon(fila[c]) for c in columnas))
    return salida


class Oraculo:
    """Resultado esperado: escalares y, por tabla, {clave: huella}. Se construye desde tablas completas o desde un archivo de huellas."""

    def __init__(self, datos):
        self.datos = datos
        self.sal = datos['sal']

    @classmethod
    def desde_tablas(cls, sal, escalares, tablas, especificacion_tablas, extra=None):
        """tablas: {nombre: DataFrame esperado}; especificacion_tablas: {nombre: {'clave': [...], 'columnas': [...]}}."""
        datos = {'version': 1, 'sal': sal, 'escalares': {k: huella_escalar(sal, k, v) for k, v in escalares.items()}, 'tablas': {}}
        for nombre, frame in tablas.items():
            esp = especificacion_tablas[nombre]
            datos['tablas'][nombre] = {'clave': esp['clave'], 'columnas': esp['columnas'],
                                       'filas': huellas_tabla(frame, esp['clave'], esp['columnas'], sal)}
        datos.update(extra or {})
        return cls(datos)

    @classmethod
    def desde_archivo(cls, ruta):
        return cls(json.loads(open(ruta, encoding='utf-8').read()))

    def guardar(self, ruta):
        with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write('\n')

    def escalar_ok(self, nombre, valor):
        return self.datos['escalares'][nombre] == huella_escalar(self.sal, nombre, valor)

    def comparar(self, nombre, frame):
        """Compara un DataFrame real con la tabla esperada. Devuelve {'faltan': [...], 'sobran': [...], 'distintas': [...]} (claves)."""
        esp = self.datos['tablas'][nombre]
        real = {}
        for fila in frame.to_dict('records'):
            k = clave_texto(fila, esp['clave'])
            if k in real:
                real[k] = None            # clave repetida: se reporta como distinta
                continue
            real[k] = huella(self.sal, k, '|'.join(canon(fila[c]) for c in esp['columnas']))
        esperada = esp['filas']
        return {'faltan': sorted(set(esperada) - set(real)),
                'sobran': sorted(set(real) - set(esperada)),
                'distintas': sorted(k for k in set(real) & set(esperada) if real[k] != esperada[k])}


# ───────────────────────────── informe ─────────────────────────────
class Informe:
    """Acumula comprobaciones: cada una es OK o un fallo con mensaje. ``cerrar`` lanza AssertionError si hubo fallos."""

    def __init__(self, titulo=''):
        self.titulo = titulo
        self.ok = []
        self.fallos = []

    def comprobar(self, condicion, nombre, detalle=''):
        if condicion:
            self.ok.append(nombre)
        else:
            self.fallos.append(f'{nombre}' + (f': {detalle}' if detalle else ''))
        return bool(condicion)

    def diferencias(self, nombre, resultado, maximo=5):
        """Registra el resultado de Oraculo.comparar como un fallo con las primeras claves de cada tipo (sin valores esperados)."""
        malo = {k: v for k, v in resultado.items() if v}
        if not malo:
            self.ok.append(nombre)
            return True
        partes = [f'{k} {len(v)} (p. ej. {", ".join(v[:maximo])})' for k, v in malo.items()]
        self.fallos.append(f'{nombre}: ' + '; '.join(partes))
        return False

    def cerrar(self):
        if self.fallos:
            raise AssertionError(f'{len(self.fallos)} comprobación(es) fallida(s) de {len(self.ok) + len(self.fallos)}:\n  - ' + '\n  - '.join(self.fallos))
        return f'{len(self.ok)} comprobaciones correctas'


def leer_tabla(con, nombre, columnas=None):
    return pd.read_sql('SELECT ' + (', '.join(columnas) if columnas else '*') + f' FROM {nombre}', con)
