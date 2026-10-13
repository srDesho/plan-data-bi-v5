"""Esqueleto del mini-ETL (ME01–ME04). Cópialo a mi_trabajo/mini_etl/mini_etl.py y complétalo por etapas.
No es un programa terminado: cada función lanza NotImplementedError hasta que la escribas tú.
Datos: 04_DATASETS/mini_etl/ (diccionario en DICCIONARIO.md).
"""
from contextlib import closing
from pathlib import Path
import sqlite3

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]      # ajusta si copias el archivo a otra carpeta
DATOS = ROOT / '04_DATASETS' / 'mini_etl'


# ---------- ME01 · Extraer y perfilar ----------
def extraer(ruta):
    """Lee ventas_mini_raw.csv como TEXTO (sin convertir nada) y devuelve un DataFrame."""
    raise NotImplementedError('ME01: extraer')


def quitar_exactos(df):
    """Elimina solo filas idénticas y devuelve un DataFrame nuevo con el índice reiniciado (como P22)."""
    raise NotImplementedError('ME01: quitar_exactos')


def perfilar(df):
    """Devuelve un diccionario con 'filas', 'nulos' (vacíos por columna) y 'duplicados_exactos' (como P23)."""
    raise NotImplementedError('ME01: perfilar')


# ---------- ME02 · Transformar ----------
def transformar(raw, catalogo):
    """Devuelve (silver, rechazos). No modifica `raw`. Reglas: 04_DATASETS/mini_etl/DICCIONARIO.md."""
    raise NotImplementedError('ME02: transformar')


# ---------- ME03 · Validar y cargar ----------
def validar(n_bronze, n_duplicados, n_rechazados, n_silver):
    """True si bronze = duplicados + rechazados + silver; ValueError si no (como P30)."""
    raise NotImplementedError('ME03: validar')


def ejecutar(entrada, salida):
    """Corre todo el proceso y publica salida/mini.db (tablas bronze, silver, rechazos, gold).
    Devuelve {'bronze','duplicados_exactos','rechazados','silver','ventas_centavos'}."""
    raise NotImplementedError('ME03: ejecutar')


if __name__ == '__main__':
    print(ejecutar(DATOS, ROOT / 'mi_trabajo' / 'mini_etl' / 'salida'))
