"""Esqueleto del estudiante; completar deliberadamente, no es un pipeline terminado."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def extraer(ruta):
    raise NotImplementedError('Lee raw y conserva texto')

def transformar(raw, vendedores):
    raise NotImplementedError('Implementa reglas desde el diccionario')

def validar(silver):
    raise NotImplementedError('Comprueba claves, tipos, conteos e importes')

def cargar(raw, silver, destino):
    raise NotImplementedError('Carga Bronze/Silver/Gold de forma reproducible')
