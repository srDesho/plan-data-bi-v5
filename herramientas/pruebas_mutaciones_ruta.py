"""Comprueba que verificar_etapa2.py detecta incoherencias de la ruta (se ejecuta SIEMPRE sobre una copia temporal; el paquete no se modifica).

    python herramientas/pruebas_mutaciones_ruta.py

Cada mutación cambia un archivo de la copia (un umbral, un minuto, un prerrequisito, una regla de hito…), ejecuta verificar_etapa2.py y exige que
falle en el grupo esperado. Después restaura el archivo. Tarda unos minutos.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CARPETAS = ['01_PLAN_DIARIO', '02_TEORIA', '03_EJERCICIOS', '04_DATASETS', '05_PROYECTOS', '06_ENTREVISTAS', '08_SOLUCIONES', '09_EVALUACION_FINAL', 'herramientas']

# (nombre, archivo, texto actual, texto nuevo, parte del mensaje de error esperada)
MUTACIONES = [
    ('umbral de S03 distinto del de COMPETENCIAS', '03_EJERCICIOS/EXAMENES/S03.md', 'Umbral: **75/100**', 'Umbral: **70/100**', 'exámenes S01–S06'),
    ('puntos de S02 que no suman 100', '03_EJERCICIOS/EXAMENES/S02.md', 'comparar | 65 |', None, 'exámenes S01–S06'),
    ('hito H03 sin condición necesaria', '03_EJERCICIOS/Comprension/H03.md', '| **Necesaria** |', '| Valoración |', 'exámenes S01–S06'),
    ('H06 vuelve a pedir ventas_centavos en el ETL guiado', '03_EJERCICIOS/Comprension/H06.md', 'la suma de `ventas_bs` de `gold_ventas_cliente_mes`', 'la suma de `ventas_centavos` del Gold', 'exámenes S01–S06'),
    ('calendario de la evaluación final distinto de nucleo.json', '09_EVALUACION_FINAL/ENUNCIADO.md', '| 24 martes | 120 | 90 |', '| 24 martes | 120 | 120 |', 'exámenes S01–S06'),
    ('rúbrica sin puerta crítica de dinero', '09_EVALUACION_FINAL/RUBRICA.md', 'Dinero incorrecto', 'Importe dudoso', 'exámenes S01–S06'),
    ('control de examen alterado', '08_SOLUCIONES/controles_examenes.json', '"esperado": "2485.5 6 414.25 27"', '"esperado": "2485.5 6 400.0 27"', 'exámenes S01–S06'),
    ('requisito de entrada demostrado el mismo día', '01_PLAN_DIARIO/nucleo.json', '"P04",\n      "P05",\n      "L:7.9"', '"P06",\n      "P05",\n      "L:7.9"', 'generador sincronizado'),
    ('REDUCIDO que omite la lección de su ejercicio', '01_PLAN_DIARIO/nucleo.json', '"reducido_lecciones": [\n    "10.3"\n   ]', '"reducido_lecciones": []', 'generador sincronizado'),
    ('guía diaria editada a mano', '01_PLAN_DIARIO/dias/D10_2026-10-21.md', '**Antes de empezar**', '**Antes de empezar (editado)**', 'generador sincronizado'),
    ('CARGA_ESTIMADA editada a mano', '01_PLAN_DIARIO/CARGA_ESTIMADA.md', '| D17 |', '| D17x |', 'generador sincronizado'),
    ('lección con el día cambiado', '01_PLAN_DIARIO/lecciones.json', None, None, 'lecciones'),
    ('fundamentos Pandas omitidos antes de transformar', '01_PLAN_DIARIO/nucleo.json', 'PD-BASE', None, 'prerrequisitos'),
    ('agrupación Pandas omitida antes de H03', '01_PLAN_DIARIO/nucleo.json', 'PD-AGR', None, 'prerrequisitos'),
]


def ejecutar_verificador(raiz):
    r = subprocess.run([sys.executable, str(raiz / 'herramientas/verificar_etapa2.py'), '--raiz', str(raiz)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, r.stdout + r.stderr


def main():
    with tempfile.TemporaryDirectory(prefix='mutaciones_ruta_') as td:
        copia = Path(td) / 'paquete'
        for c in CARPETAS:
            shutil.copytree(ROOT / c, copia / c, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy(ROOT / 'README.md', copia / 'README.md')
        (copia / 'mi_trabajo').mkdir()
        codigo, salida = ejecutar_verificador(copia)
        assert codigo == 0, 'la copia sin mutar debe pasar:\n' + salida[-1500:]
        print('base sin mutar: todos los grupos OK')
        detectadas = 0
        for nombre, archivo, viejo, nuevo, esperado in MUTACIONES:
            ruta = copia / archivo
            original = ruta.read_bytes()
            texto = original.decode('utf-8')
            crlf = '\r\n' in texto
            t = texto.replace('\r\n', '\n')
            if viejo in ('PD-BASE', 'PD-AGR'):
                datos = json.loads(t)
                borradas = 0
                for jornada in datos['dias'].values():
                    original_obligatorio = jornada['obligatorio']
                    jornada['obligatorio'] = [x for x in original_obligatorio if (x['id'] if isinstance(x, dict) else x) != viejo]
                    borradas += len(original_obligatorio) - len(jornada['obligatorio'])
                assert borradas == 1, f'{nombre}: se esperaba una práctica obligatoria'
                mutado = json.dumps(datos, ensure_ascii=False, indent=1)
            elif nombre.startswith('puntos de S02'):
                v, n = '| 65 |', '| 60 |'
            elif nombre.startswith('lección con el día'):
                v, n = '02_group_by_having.md",\n   "tipo": "NÚCLEO",\n   "dia": 5', '02_group_by_having.md",\n   "tipo": "NÚCLEO",\n   "dia": 6'
            else:
                v, n = viejo, nuevo
            if viejo not in ('PD-BASE', 'PD-AGR'):
                if t.count(v) < 1:
                    raise AssertionError(f'{nombre}: no se encuentra el texto a mutar en {archivo}')
                mutado = t.replace(v, n, 1)
            ruta.write_bytes(mutado.replace('\n', '\r\n' if crlf else '\n').encode('utf-8'))
            try:
                codigo, salida = ejecutar_verificador(copia)
            finally:
                ruta.write_bytes(original)
            ok = codigo != 0 and any(l.startswith('ERROR') and esperado in l for l in salida.splitlines())
            print(('DETECTADA  ' if ok else 'NO DETECTADA ') + nombre + f' → {esperado}')
            detectadas += ok
        print(f'{detectadas} de {len(MUTACIONES)} mutaciones detectadas')
        if detectadas != len(MUTACIONES):
            raise SystemExit(1)


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
