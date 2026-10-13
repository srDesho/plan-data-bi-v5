"""Auditoría automática de enunciados: detecta plantillas reutilizadas, pistas genéricas, datos escondidos en el corrector,
respuestas publicadas en el enunciado, prerrequisitos ausentes y exámenes que evalúan algo no preparado.

Uso desde la raíz:  python herramientas/auditar_enunciados.py      (código de salida 0 si todo cumple)
También lo ejecuta `verificar_paquete.py` y comprueba, con un control negativo, que detecta una plantilla masiva.
"""
from collections import Counter
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True

FRASES_PROHIBIDAS = [
    "Caso laboral: el gerente requiere este resultado",
    "Decide qué condición filtra filas (WHERE) y cuál filtra grupos (HAVING)",
    "Identifica la tabla y la granularidad antes de escribir SELECT",
    "Si unes detalle y cabecera, cuenta pedidos distintos",
    "Pista 1: describe qué representa una fila y qué filtro pide gerencia",
    "separa agenda, pedido y venta entregada; comprueba claves y periodo antes de fórmulas",
    "Pista 1: identifica la unidad independiente y si se describe población",
    "Pista 1 (tras 10 min): identifica el tipo de entrada y el tipo exacto de salida",
]
SECCIONES_SQL = ["## Situación", "## Qué debes entregar", "## Comprobación", "## Pistas", "## Criterios de aceptación"]
COMUN = "Anotaste en `mi_trabajo/errores.md`"


def leer(p):
    return Path(p).read_text(encoding='utf-8')


def seccion(texto, titulo):
    m = re.search(rf'^## {re.escape(titulo)}[^\n]*\n(.*?)(?=^## |\Z)', texto, re.S | re.M)
    return m.group(1).strip() if m else ''


def pistas(texto):
    sec = seccion(texto, 'Pistas')
    return [re.sub(r'^\d+\.\s+\*\*[^*]+\*\*\s*', '', l).strip() for l in sec.splitlines() if re.match(r'^\d+\.', l)]


def criterios(texto):
    return [l[6:].strip() for l in seccion(texto, 'Criterios de aceptación').splitlines() if l.startswith('- [ ]')]


def numeros_largos(valor):
    """Formas en que podría aparecer un valor numérico grande en un texto (1468924.5 → 1.468.924,50 / 1468924,5 …)."""
    v = float(valor)
    formas = set()
    for dec in (0, 1, 2):
        base = f'{v:.{dec}f}'
        entero, _, frac = base.partition('.')
        miles = f'{int(entero):,}'.replace(',', '.')
        formas |= {entero + ('.' + frac if frac else ''), entero + (',' + frac if frac else ''), miles + (',' + frac if frac else '')}
    return {f for f in formas if len(re.sub(r'\D', '', f)) >= 5}


def auditar_sql(carpeta=None, controles=None):
    carpeta = Path(carpeta or ROOT / '03_EJERCICIOS/SQL')
    controles = controles if controles is not None else json.loads(leer(ROOT / '08_SOLUCIONES/controles_sql.json'))
    problemas, datos = [], {}
    for p in sorted(carpeta.glob('*.md')):
        if p.stem in ('INDICE', 'CONTRATOS'):
            continue
        t = leer(p)
        datos[p.stem] = t
        for s in SECCIONES_SQL:
            if s not in t:
                problemas.append(f'{p.stem}: falta la sección {s}')
        if 'Una fila del resultado representa:' not in t:
            problemas.append(f'{p.stem}: no dice qué representa una fila')
        if not re.search(r'Primera vez: \d+–\d+ min', t):
            problemas.append(f'{p.stem}: sin tiempo realista de primera vez')
        h = pistas(t)
        if len(h) != 3:
            problemas.append(f'{p.stem}: tiene {len(h)} pistas (deben ser 3)')
        for k, x in enumerate(h, 1):
            if re.search(r'SELECT\s+[^…\n`]{3,}\s+FROM', x):
                problemas.append(f'{p.stem}: la pista {k} parece incluir una consulta completa')
        if p.stem in controles and p.stem != 'N13':
            for col in controles[p.stem]['columnas']:
                if f'`{col}`' not in t:
                    problemas.append(f'{p.stem}: la columna `{col}` del contrato no aparece en el enunciado')
            n = len(controles[p.stem]['filas'])
            citas = re.findall(r'(\d[\d.]*) filas?\b', seccion(t, 'Criterios de aceptación')) + re.findall(r'[Dd]ebes obtener (\d[\d.]*) filas', t)
            for c in citas:
                v = int(c.replace('.', ''))
                if v != n:
                    problemas.append(f'{p.stem}: menciona {v} filas pero el contrato dice {n}')
    # reutilización masiva
    for etiqueta, extractor in (('situación', lambda t: seccion(t, 'Situación')), ('pista 1', lambda t: (pistas(t) + ['', '', ''])[0]),
                                ('pista 2', lambda t: (pistas(t) + ['', '', ''])[1]), ('pista 3', lambda t: (pistas(t) + ['', '', ''])[2])):
        cuenta = Counter(extractor(t) for t in datos.values())
        for texto, k in cuenta.items():
            if texto and k > 1:
                repetidos = [i for i, t in datos.items() if extractor(t) == texto]
                problemas.append(f'{etiqueta} repetida en {k} ejercicios ({", ".join(repetidos[:4])}…): «{texto[:60]}»')
    cuenta_crit = Counter(c for t in datos.values() for c in criterios(t) if COMUN not in c)
    for i, t in datos.items():
        propios = [c for c in criterios(t) if COMUN not in c and cuenta_crit[c] == 1]
        if len(propios) < 1:
            problemas.append(f'{i}: ningún criterio propio (todos se repiten en otros ejercicios)')
        for c in criterios(t):
            if COMUN not in c and cuenta_crit[c] > 8:
                problemas.append(f'{i}: el criterio «{c[:50]}» se repite en {cuenta_crit[c]} ejercicios')
    return problemas, len(datos)


def auditar_python():
    problemas = []
    carpeta = ROOT / '03_EJERCICIOS/Python'
    plantilla = leer(carpeta / 'plantilla.py')
    contratos = leer(ROOT / 'herramientas/contratos_python.py')
    exige_error = set(re.findall(r'error\(modulo\.(\w+)', contratos))
    textos = {}
    for p in sorted(carpeta.glob('P[0-9][0-9].md')):
        t = leer(p)
        textos[p.stem] = t
        m = re.search(r'`def (\w+)\(([^)]*)\):`', t)
        if not m:
            problemas.append(f'{p.stem}: no muestra la firma `def …`')
            continue
        if f'def {m.group(1)}(' not in plantilla:
            problemas.append(f'{p.stem}: la función {m.group(1)} no está en plantilla.py')
        if m.group(1) in exige_error and 'ValueError' not in t:
            problemas.append(f'{p.stem}: el corrector exige ValueError en {m.group(1)} y el enunciado no lo dice')
        for s in ('## Situación', '## Qué recibe y qué devuelve', '## Reglas', '## Ejemplos', '## Pistas', '## Criterios de aceptación'):
            if s not in t:
                problemas.append(f'{p.stem}: falta {s}')
        if not re.search(r'Primera vez: \d+–\d+ min', t):
            problemas.append(f'{p.stem}: sin tiempo de primera vez')
        if len(pistas(t)) != 3:
            problemas.append(f'{p.stem}: no tiene 3 pistas')
    for n in (1, 2, 3):
        cuenta = Counter((pistas(t) + ['', '', ''])[n - 1] for t in textos.values())
        for x, k in cuenta.items():
            if x and k > 1:
                problemas.append(f'pista {n} repetida en {k} ejercicios Python: «{x[:60]}»')
    return problemas, len(textos)


def auditar_otros():
    problemas, total = [], 0
    for sub, patron in (('Estadistica', 'ST0*.md'), ('Casos', '*.md'), ('Puente', 'ME0*.md'), ('Depuracion', 'DB0*.md')):
        carpeta = ROOT / '03_EJERCICIOS' / sub
        textos = {}
        for p in sorted(carpeta.glob(patron)):
            t = leer(p)
            textos[p.stem] = t
            total += 1
            for fr in FRASES_PROHIBIDAS:
                if fr in t:
                    problemas.append(f'{sub}/{p.stem}: contiene texto genérico reutilizado «{fr[:50]}»')
            if len(pistas(t)) < 3 and not re.search(r'^\*\*Pistas', t, re.M):
                problemas.append(f'{sub}/{p.stem}: menos de 3 pistas')
            if not re.search(r'Primera vez:', t):
                problemas.append(f'{sub}/{p.stem}: sin tiempo realista de primera vez')
        for n in (1, 2):
            cuenta = Counter((pistas(t) + ['', '', ''])[n - 1] for t in textos.values())
            for x, k in cuenta.items():
                if x and k > 1:
                    problemas.append(f'{sub}: pista {n} repetida en {k} ejercicios: «{x[:50]}»')
    # estadística: ninguna cifra de los controles en los enunciados
    ctrl = json.loads(leer(ROOT / '08_SOLUCIONES/controles_estadistica.json'))
    planos = []

    def aplanar(x):
        if isinstance(x, dict):
            for v in x.values():
                aplanar(v)
        elif isinstance(x, list):
            for v in x:
                aplanar(v)
        elif isinstance(x, float):
            planos.append(x)
    aplanar(ctrl)
    for p in sorted((ROOT / '03_EJERCICIOS/Estadistica').glob('ST0*.md')):
        t = leer(p)
        for v in planos:
            for f in (f'{v:.2f}'.replace('.', ','), f'{v:.2f}', f'{v:.4f}'.rstrip('0')):
                if len(f) >= 5 and f in t:
                    problemas.append(f'{p.stem}: publica la cifra de control {f}')
    return problemas, total


def auditar_fuga_sql_python_etc():
    """Resultados de una sola fila numérica grande: no deben aparecer en enunciados de SQL, Python, estadística, puente ni depuración."""
    problemas = []
    ctrl = json.loads(leer(ROOT / '08_SOLUCIONES/controles_sql.json'))
    formas = {}
    for i, c in ctrl.items():
        if len(c['filas']) == 1 and len(c['filas'][0]) == 1 and isinstance(c['filas'][0][0], (int, float)) and abs(c['filas'][0][0]) >= 10000:
            formas[i] = numeros_largos(c['filas'][0][0])
    for sub in ('SQL', 'Python', 'Estadistica', 'Puente', 'Depuracion'):
        for p in (ROOT / '03_EJERCICIOS' / sub).glob('*.md'):
            t = leer(p)
            for i, fs in formas.items():
                for f in fs:
                    if re.search(rf'(?<![\d.,]){re.escape(f)}(?![\d])', t):
                        problemas.append(f'{sub}/{p.stem}: publica el resultado de {i} ({f})')
    return problemas, len(formas)


def auditar_dependencias():
    """Cada OBLIGATORIO exige solo teoría que ya se asignó (hasta ese día) y los exámenes solo evalúan lo preparado."""
    problemas = []
    nuc = json.loads(leer(ROOT / '01_PLAN_DIARIO/nucleo.json'))['dias']
    cal = {d['dia']: d for d in json.loads(leer(ROOT / '01_PLAN_DIARIO/calendario.json'))}
    acumulada, aprendido = set(), {}
    for dia in sorted(cal):
        d = cal[dia]
        acumulada |= set(d.get('teoria', []))
        s = nuc.get(str(dia))
        if not s:
            for k in ('sql', 'python', 'estadistica', 'otros'):
                for i in d.get(k, []):
                    aprendido.setdefault(i, dia)
            continue
        for x in s['obligatorio'] + s['repaso']:
            i = x['id'] if isinstance(x, dict) else x
            aprendido.setdefault(i, dia)
            if i.startswith(('EXAMEN', 'ETL-', 'C06-')):
                continue
            for sub in ('SQL', 'Python', 'Estadistica', 'Puente', 'Depuracion', 'Casos'):
                p = ROOT / '03_EJERCICIOS' / sub / f'{i}.md'
                if p.exists():
                    t = leer(p)
                    for req in re.findall(r'02_TEORIA/(\w+)\.md', t.split('## Situación')[0] if '## Situación' in t else t[:600]):
                        if req not in acumulada and req not in ('FUENTES', 'GLOSARIO'):
                            problemas.append(f'D{dia:02}: {i} (OBLIGATORIO) pide leer {req}, que aún no se asignó en el plan')
    # los OBLIGATORIOS no dependen de un ejercicio que solo es REFUERZO/OPCIONAL (texto «tu Pxx», «tus Pxx»)
    opcionales = {}
    for dia, s in nuc.items():
        for cat in ('refuerzo', 'opcional'):
            for x in s[cat]:
                opcionales.setdefault(x['id'] if isinstance(x, dict) else x, int(dia))
    for dia, s in nuc.items():
        for x in s['obligatorio']:
            i = x['id'] if isinstance(x, dict) else x
            textos = []
            if i.startswith('ETL-') or i.startswith('C06-'):
                textos.append(json.loads(leer(ROOT / '01_PLAN_DIARIO/nucleo.json'))['items_personalizados'][i]['nota'])
            else:
                for sub in ('Puente', 'Depuracion', 'Python', 'SQL', 'Casos'):
                    p = ROOT / '03_EJERCICIOS' / sub / f'{i}.md'
                    if p.exists():
                        textos.append(leer(p).split('## Pistas')[0])
            for t in textos:
                for m in re.finditer(r'\b(?:tu|tus)\s+((?:[PKJGSVNXE]|ST|ME|DB)\d+[ab]?)(?:\s*(?:,|y|e)\s*((?:[PKJGSVNXE]|ST|ME|DB)\d+[ab]?))?', t):
                    for ref in filter(None, m.groups()):
                        if ref in opcionales and ref not in aprendido:
                            problemas.append(f'D{int(dia):02}: {i} (OBLIGATORIO) depende de «{ref}», que solo es REFUERZO/OPCIONAL')
    for k in range(5):
        if f'C06-{k}' in aprendido:
            aprendido.setdefault('C06', aprendido[f'C06-{k}'])
    # exámenes: todo ID mencionado debe estar preparado (OBL o repaso) en un día anterior o igual
    dia_examen = {f'S0{k}': d for d, k in ((6, 1), (13, 2), (20, 3), (27, 4), (34, 5), (41, 6))}
    for ex, dia in dia_examen.items():
        t = leer(ROOT / f'03_EJERCICIOS/EXAMENES/{ex}.md')
        tareas = seccion(t, 'Tareas')
        for ref in set(re.findall(r'\b(?:[PGJKVXENC]\d+[ab]?|ME0\d|DB0\d|C0\d)\b', tareas)):
            if ref.startswith('ES'):
                continue
            if ref not in aprendido or aprendido[ref] > dia:
                problemas.append(f'{ex}: evalúa {ref}, que no está preparado como OBLIGATORIO/REPASO antes del examen (D{dia:02})')
    return problemas, len(aprendido)


def auditar_indices():
    problemas = []
    for sub, patron in (('SQL', '*.md'), ('Python', 'P[0-9][0-9].md'), ('Puente', 'ME0*.md'), ('Depuracion', 'DB0*.md')):
        carpeta = ROOT / '03_EJERCICIOS' / sub
        indice = leer(carpeta / 'INDICE.md')
        for p in carpeta.glob(patron):
            if p.stem in ('INDICE', 'CONTRATOS'):
                continue
            if f']({p.name})' not in indice:
                problemas.append(f'{sub}/INDICE.md no lista {p.name}')
    ctrl = json.loads(leer(ROOT / '08_SOLUCIONES/controles_sql.json'))
    contratos = leer(ROOT / '03_EJERCICIOS/SQL/CONTRATOS.md')
    for i, c in ctrl.items():
        fila = re.search(rf'^\| {i} \| (.*?) \| (\d+) \|$', contratos, re.M)
        if not fila:
            problemas.append(f'CONTRATOS.md no lista {i}')
        elif fila.group(1) != ', '.join(c['columnas']) or int(fila.group(2)) != len(c['filas']):
            problemas.append(f'CONTRATOS.md no coincide con el control de {i}')
    # enunciados ↔ diccionario ↔ base de datos: columnas y filas de cada tabla citada
    import sqlite3
    from contextlib import closing
    with closing(sqlite3.connect((ROOT / '04_DATASETS/comercial.db').as_uri() + '?mode=ro', uri=True)) as con:
        esquema = {t: [r[1] for r in con.execute(f'PRAGMA table_info({t})')] for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        filas_db = {t: con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in esquema}
    for p in (ROOT / '03_EJERCICIOS/SQL').glob('*.md'):
        if p.stem in ('INDICE', 'CONTRATOS'):
            continue
        for tabla, resto in re.findall(r'^- `(\w+)`: (.+)$', leer(p), re.M):
            nombres = [x.strip() for x in re.sub(r'\([^)]*\)', '', resto).split(',') if x.strip()]
            if tabla not in esquema:
                problemas.append(f'{p.stem}: cita la tabla {tabla}, que no existe en comercial.db')
            elif set(nombres) != set(esquema[tabla]):
                problemas.append(f'{p.stem}: las columnas citadas de {tabla} no coinciden con la base ({sorted(set(nombres) ^ set(esquema[tabla]))})')
    dic = leer(ROOT / '04_DATASETS/DICCIONARIO.md')
    for tabla, n in esquema.items():
        m = re.search(rf'^\| {tabla} \|.*\|\s*(\d+)\s*\|$', dic, re.M)
        if not m:
            problemas.append(f'DICCIONARIO.md no describe la tabla {tabla}')
        elif int(m.group(1)) != filas_db[tabla]:
            problemas.append(f'DICCIONARIO.md dice {m.group(1)} filas para {tabla} y la base tiene {filas_db[tabla]}')
    return problemas, len(ctrl)


def ejecutar():
    resultado = {}
    for nombre, fn in (('SQL', auditar_sql), ('Python', auditar_python), ('Otros (estadística, casos, puente, depuración)', auditar_otros),
                       ('Fugas de resultados', auditar_fuga_sql_python_etc), ('Dependencias y exámenes', auditar_dependencias), ('Índices y contratos', auditar_indices)):
        resultado[nombre] = fn()
    return resultado


CAMBIOS_REFERENCIA = {
    **{i: 'orden explícito en la referencia (el contenido del control no cambia)' for i in (
        'S1', 'S2', 'S3', 'S5', 'S6', 'S7', 'S8', 'S9', 'G1', 'G4', 'G5', 'G6', 'E1', 'E5', 'E7', 'E8', 'CL3', 'J1', 'J5', 'K1', 'X7', 'X8')},
    'N5': 'alias `ventas_bs` en la segunda columna (solo el nombre del contrato)',
    'ES1B': 'filtro cambiado a «precio medio > 9 Bs» (el anterior no filtraba nada): control de 5 a 2 filas',
    'ES3C': 'competencia cambiada de RANK a participación con ventana (practicada en V3): control nuevo',
}


def tabla_sql():
    """Tabla Markdown con la comprobación individual de los 81 ejercicios SQL (enunciado, contrato, referencia y corrector)."""
    sys.path.insert(0, str(ROOT / 'herramientas'))
    from corregir_sql import comprobar
    ctrl = json.loads(leer(ROOT / '08_SOLUCIONES/controles_sql.json'))
    filas = ['| ID | Nivel | Primera vez | Columnas | Filas | Referencia = control (corrector) | 3 pistas | Criterios propios | Cambio en la referencia |', '|---|:-:|---:|---:|---:|:-:|:-:|---:|---|']
    textos = {i: leer(ROOT / f'03_EJERCICIOS/SQL/{i}.md') for i in ctrl}
    cuenta = Counter(c for t in textos.values() for c in criterios(t) if COMUN not in c)
    for i in ctrl:
        t = textos[i]
        nivel = re.search(r'Nivel (\d)/3', t).group(1)
        pv = re.search(r'Primera vez: (\d+–\d+) min', t).group(1)
        try:
            n = comprobar(i, ROOT / f'08_SOLUCIONES/sql/{i}.sql')
            ok = 'sí'
        except Exception as e:
            ok = f'NO ({type(e).__name__})'
        propios = sum(1 for c in criterios(t) if COMUN not in c and cuenta[c] == 1)
        filas.append(f'| {i} | {nivel} | {pv} min | {len(ctrl[i]["columnas"])} | {len(ctrl[i]["filas"]) if i != "N13" else "plan"} | {ok} | {"sí" if len(pistas(t)) == 3 else "NO"} | {propios} | {CAMBIOS_REFERENCIA.get(i, "—")} |')
    return '\n'.join(filas) + '\n'


if __name__ == '__main__':
    if '--tabla' in sys.argv:
        destino = Path(sys.argv[sys.argv.index('--tabla') + 1])
        encabezado = ('# Comprobación individual de los 81 ejercicios SQL\n\n'
                      'Generada por `python herramientas/auditar_enunciados.py --tabla RUTA`. Cada fila resume qué se verificó automáticamente: columnas del enunciado frente al contrato, '
                      'filas del contrato, resultado de la referencia frente al control mediante el corrector, tres pistas y criterios propios. «Cambio en la referencia» documenta cada '
                      'modificación hecha en esta revisión y por qué.\n\n')
        destino.write_text(encabezado + tabla_sql(), encoding='utf-8')
        print('Tabla escrita en', destino)
        raise SystemExit(0)
    res = ejecutar()
    total = 0
    for nombre, (problemas, n) in res.items():
        print(f'{"OK   " if not problemas else "FALLA"} {nombre}: {n} elementos revisados, {len(problemas)} problemas')
        for p in problemas[:25]:
            print('      -', p)
        total += len(problemas)
    raise SystemExit(1 if total else 0)
