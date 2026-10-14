"""Aplica 01_PLAN_DIARIO/nucleo.json y lecciones.json a las guías diarias, al calendario y a los documentos de carga (idempotente).

Cada jornada queda con: lecciones NÚCLEO del día (lectura), ejercicios OBLIGATORIO / REPASO / REFUERZO / OPCIONAL, actividad de criterio
analítico o hito de comprensión, bloque EXTENDIDA voluntario, prerrequisito y, si corresponde, su puerta de competencia. Los domingos son
descanso por defecto con recuperación voluntaria de 45–120 minutos. D01 no se toca; D02 solo recibe un bloque informativo de lecciones.
Los minutos de cada jornada (900 por semana) no cambian: el bloque de aprendizaje (SQL + teoría + práctica) se reparte entre lecciones, SQL,
práctica y criterio.

Uso desde la raíz:
    python herramientas/aplicar_nucleo.py              # escribe guías, PLAN_V5.md (títulos), calendario.json/csv, CARGA_ESTIMADA.md y RUTAS.md
    python herramientas/aplicar_nucleo.py --comprobar  # solo valida referencias y muestra la estimación
    python herramientas/aplicar_nucleo.py --raiz RUTA  # trabaja sobre una copia del paquete
"""
from pathlib import Path
import argparse
import csv
import json
import re
import sys

PROTEGIDOS = {1, 2}                       # D01 y D02 no se reescriben (D02 recibe solo un bloque informativo de lecciones)
MULT = {('SQL', 1): 1.5, ('SQL', 2): 1.75, ('SQL', 3): 2.25, ('PY', 1): 2.0, ('PY', 2): 2.5, ('PY', 3): 3.25,
        ('ST', 1): 2.0, ('ST', 2): 2.0, ('ST', 3): 2.5}
CASO_MIN = {'C01': 30, 'C02': 25, 'C03': 35, 'C04': 40, 'C05': 45}
ACCION = 'Resolver los OBLIGATORIOS; REFUERZO solo si la puerta no se cumplió; OPCIONAL no desplaza lo obligatorio.'
POOL = ('SQL', 'Teoría', 'Teoría/retro', 'Práctica', 'Lecciones', 'Criterio')   # bloques que se reparten el tiempo de aprendizaje
EXTRA_MIN = [30, 75, 75, 60, 75, 75]      # EXTENDIDA voluntaria: lunes … sábado
DOMINGO_MIN = (45, 120)
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
TIPOS_TXT = {'NÚCLEO': 'NÚCLEO', 'REFUERZO': 'REFUERZO', 'PROFUNDIZACIÓN': 'PROFUNDIZACIÓN'}
PUENTE_ARCHIVO = '19_Puente_Python_a_ETL.md'


class Contexto:
    def __init__(self, raiz):
        self.raiz = Path(raiz)
        plan = self.raiz / '01_PLAN_DIARIO'
        self.nucleo = json.loads((plan / 'nucleo.json').read_text(encoding='utf-8'))
        self.calendario = json.loads((plan / 'calendario.json').read_text(encoding='utf-8'))
        self.lecciones = json.loads((plan / 'lecciones.json').read_text(encoding='utf-8'))
        self.ejercicios = self.raiz / '03_EJERCICIOS'
        self.capitulos = {}
        for f in sorted((self.raiz / '02_TEORIA').glob('[0-9][0-9]_*.md')):
            self.capitulos[str(int(f.name[:2]))] = f.stem
        self._cache = {}


def norm(item):
    return item if isinstance(item, dict) else {'id': item}


def tipo(i):
    if i.startswith('EXAMEN:'):
        return 'EXAMEN'
    if i in ('C06-0', 'C06-1', 'C06-2', 'C06-3', 'C06-4', 'PD-BASE', 'PD-AGR') or i.startswith('ETL-'):
        return 'CUSTOM'
    if re.fullmatch(r'P\d\d', i):
        return 'PY'
    if re.fullmatch(r'ST\d\d', i):
        return 'ST'
    if re.fullmatch(r'ME\d\d', i):
        return 'ME'
    if re.fullmatch(r'DB\d\d', i):
        return 'DB'
    if re.fullmatch(r'N0\d', i):
        return 'NB'
    if re.fullmatch(r'PB\d\d', i):
        return 'PB'
    if re.fullmatch(r'EX\d\d', i):
        return 'EX'
    if re.fullmatch(r'C0\d', i):
        return 'CASO'
    return 'SQL'


def ruta_ejercicio(i):
    t = tipo(i)
    carpeta = {'SQL': 'SQL', 'PY': 'Python', 'ST': 'Estadistica', 'ME': 'Puente', 'DB': 'Depuracion',
               'PB': 'Casos', 'EX': 'Casos', 'CASO': 'Casos'}
    if t == 'NB':
        return f'Notebooks/{i}.ipynb'
    return f'{carpeta[t]}/{i}.md'


def datos_archivo(ctx, i):
    """(nivel, minutos objetivo, minutos de primera vez) leídos del propio enunciado; primera vez = punto medio del rango."""
    p = ctx.ejercicios / ruta_ejercicio(i)
    if not p.exists() or p.suffix != '.md':
        return 2, 20, None
    texto = p.read_text(encoding='utf-8')
    nivel = re.search(r'Nivel (\d)/3', texto)
    objetivo = re.search(r'Tiempo objetivo (\d+) ?min', texto)
    primera = re.search(r'Primera vez:\s*[≈~]?\s*(\d+)(?:\s*[–-]\s*(\d+))?\s*min', texto)
    pv = None
    if primera:
        a, b = int(primera.group(1)), int(primera.group(2) or primera.group(1))
        pv = round((a + b) / 2)
    return (int(nivel.group(1)) if nivel else 2), (int(objetivo.group(1)) if objetivo else 30), pv


def estimar(ctx, item, repaso=False):
    it = norm(item)
    i = it['id']
    if 'est' in it:
        return it['est']
    t = tipo(i)
    if t == 'EXAMEN':
        return 0
    if t == 'CUSTOM':
        return ctx.nucleo['items_personalizados'][i]['est']
    if repaso:
        return 10
    nivel, minutos, primera_vez = datos_archivo(ctx, i)
    if primera_vez is not None:                # fuente única: el tiempo realista declarado en el enunciado
        return primera_vez
    clave = {'SQL': 'SQL', 'PY': 'PY', 'ST': 'ST'}.get(t)      # respaldo si un enunciado no declara «Primera vez»
    if clave:
        return round(minutos * MULT[(clave, nivel)])
    if t in ('PB', 'EX'):
        return round(minutos * 2.0)
    return round(minutos * 1.75)


def enlace(ctx, item):
    it = norm(item)
    i = it['id']
    t = tipo(i)
    if t == 'EXAMEN':
        s = i.split(':')[1]
        n = int(s[1:])
        return (f'[Examen {s}](../../03_EJERCICIOS/EXAMENES/{s}.md) y [simulacro semanal](../../06_ENTREVISTAS/SIMULACRO_{n:02}.md). '
                'Examen 60 + corrección 25 + simulacro 30 = 115 minutos.')
    if t == 'CUSTOM':
        c = ctx.nucleo['items_personalizados'][i]
        links = ' · '.join(f'[{a}]({b})' for a, b in c['enlaces'])
        return f'**{c["titulo"]}** ({links}). {c["nota"]}'
    etiqueta = {'SQL': f'SQL {i}', 'PY': f'Python {i}', 'ST': f'Estadística {i}', 'ME': f'Mini-ETL {i}', 'DB': f'Depuración {i}',
                'NB': f'Notebook {i}', 'PB': f'Power BI {i}', 'EX': f'Excel {i}', 'CASO': f'Caso {i}'}[t]
    texto = f'[{etiqueta}](../../03_EJERCICIOS/{ruta_ejercicio(i)})'
    if it.get('nota'):
        texto += f' · {it["nota"]}'
    return texto


def nombre_corto(ctx, item):
    i = norm(item)['id']
    if tipo(i) == 'EXAMEN':
        return 'examen ' + i.split(':')[1]
    if tipo(i) == 'CUSTOM':
        return f"{i} ({ctx.nucleo['items_personalizados'][i]['titulo'].split(' · ')[-1]})"
    return i


def comando_correccion(ids):
    for item in ids:
        i = norm(item)['id']
        t = tipo(i)
        if t == 'SQL':
            return f'`python herramientas/corregir_sql.py {i} mi_trabajo/sql/{i}.sql`'
        if t == 'PY':
            return f'`python herramientas/corregir_python.py {i} mi_trabajo/python/mis_funciones.py`'
        if t == 'ME':
            return f'`python herramientas/corregir_mini_etl.py {i} mi_trabajo/mini_etl/mini_etl.py`'
        if t == 'DB':
            return f'`python herramientas/corregir_depuracion.py {i} mi_trabajo/depuracion/{i}.py`'
        if i == 'ETL-6':
            return '`python herramientas/validar_etl_distribuidora.py mi_trabajo/etl/etl_salida.db`'
    return None


# ───────────────────────────── lecciones ─────────────────────────────
def info_leccion(ctx, i):
    """Datos de una lección (o de una sección del capítulo 19): título, enlace desde las guías, lectura, práctica, tipo y día."""
    if i in ctx._cache:
        return ctx._cache[i]
    if i in ctx.lecciones['puente']:
        p = ctx.lecciones['puente'][i]
        r = {'id': i, 'titulo': f'Capítulo 19 {p["seccion"]} · {p["titulo"]}', 'archivo': PUENTE_ARCHIVO, 'lectura': p['min'], 'practica': 0,
             'tipo': p.get('tipo', 'NÚCLEO'), 'dia': p.get('dia'), 'dia_ext': None, 'cuando': '', 'puente': True}
    else:
        c = ctx.lecciones['lecciones'][i]
        texto = (ctx.raiz / '02_TEORIA' / c['archivo']).read_text(encoding='utf-8')
        titulo = re.match(r'# \d+\.\d+ (.+)', texto).group(1).strip()
        m = re.search(r'lectura (\d+) \+ práctica (\d+)', texto)
        r = {'id': i, 'titulo': titulo, 'archivo': c['archivo'], 'lectura': int(m.group(1)), 'practica': int(m.group(2)), 'tipo': c['tipo'],
             'dia': c.get('dia'), 'dia_ext': c.get('dia_ext'), 'cuando': c.get('cuando', ''), 'puente': False}
        r['practica_base'] = c.get('practica_base', 0)
        if not 0 <= r['practica_base'] <= r['practica']:
            raise ValueError(f'{i}: práctica BASE fuera del tiempo de práctica de la lección')
    ctx._cache[i] = r
    return r


def enlace_leccion(ctx, i):
    d = info_leccion(ctx, i)
    nombre = d['titulo'] if d['puente'] else f'{i} {d["titulo"]}'
    return f'[{nombre}](../../02_TEORIA/{d["archivo"]})'


def lectura_dia(ctx, s):
    return sum(info_leccion(ctx, i)['lectura'] for i in s.get('lecciones') or [])


def lectura_ids(ctx, ids):
    return sum(info_leccion(ctx, i)['lectura'] for i in ids or [])


def citas_lecciones(ctx, i, completo=False):
    """Lecciones que cita un ejercicio: en sus primeras líneas («Lee la lección 7.9», «Lee las lecciones 7.8 y 7.9») o, con ``completo``, en todo el enunciado."""
    if tipo(i) in ('EXAMEN', 'CUSTOM'):
        return []
    p = ctx.ejercicios / ruta_ejercicio(i)
    if not p.exists() or p.suffix != '.md':
        return []
    lineas = p.read_text(encoding='utf-8').split('Solución separada')[0].splitlines()
    texto = '\n'.join(lineas if completo else lineas[:6])
    ids = []
    for m in re.finditer(r'[Ll]ecci[oó]n(?:es)? ([\d.]+(?:(?:, | y | e )[\d.]+)*)', texto):
        ids += re.findall(r'\d+\.\d+', m.group(1))
    return [x for x in dict.fromkeys(ids) if x in ctx.lecciones['lecciones']]


def dia_entrada(ctx, p):
    """Día en que algo queda demostrado: «L:7.9» = lección NÚCLEO leída ese día; un ID = ejercicio OBLIGATORIO/REPASO resuelto ese día."""
    if p.startswith('L:'):
        i = p[2:]
        if i in ctx.lecciones['puente']:
            return ctx.lecciones['puente'][i]['dia']
        c = ctx.lecciones['lecciones'].get(i)
        return c['dia'] if c and c['tipo'] == 'NÚCLEO' else None
    return dia_ejercicio(ctx, p)


def fuente_entrada(ctx, p):
    if p.startswith('L:'):
        return f'lección {p[2:]} (D{dia_entrada(ctx, p):02})'
    return f'{nombre_corto(ctx, p)} (D{dia_entrada(ctx, p):02})'


def antes_de_empezar(ctx, s):
    """«Antes de empezar»: lo que ya se debe poder hacer (demostrado en jornadas anteriores) frente a lo que se aprende hoy."""
    entra = s.get('entra') or []
    lineas = []
    if entra:
        lineas += ['**Antes de empezar** (lo que ya debes poder hacer; cada punto viene de una jornada anterior):', '']
        for e in entra:
            if e.get('por'):
                lineas.append(f'- {e["texto"]} · viene de {", ".join(fuente_entrada(ctx, p) for p in e["por"])}.')
            else:
                lineas.append(f'- {e["texto"]} · requisito externo: si falta, la parte que lo necesita queda PENDIENTE y se registra.')
        lineas += ['', 'Si algún punto no se cumple, haz primero el REFUERZO de esa jornada anterior en lugar del OBLIGATORIO de hoy. '
                   'Lo que aparece en el bloque «Lecciones» y en los ejercicios de hoy se aprende hoy: no se exige al entrar.', '']
    nuevo = [f'{info_leccion(ctx, i)["titulo"]}' for i in s.get('lecciones') or []]
    if nuevo:
        lineas += [f'**Se aprende hoy** (no se exige al entrar): {"; ".join(nuevo)}.', '']
    return lineas


def capitulos_dia(ctx, s):
    caps = []
    for i in s.get('lecciones') or []:
        n = '19' if i.startswith('19.') else i.split('.')[0]
        c = ctx.capitulos[str(int(n))]
        if c not in caps:
            caps.append(c)
    return caps


def titulo_actividad(ctx, i):
    carpeta = 'Analitico' if i.startswith('AN') else 'Comprension'
    p = ctx.ejercicios / carpeta / f'{i}.md'
    if not p.exists():
        return i
    return p.read_text(encoding='utf-8').splitlines()[0].lstrip('# ').strip()


# ───────────────────────────── bloques de tiempo ─────────────────────────────
def redondear5(x):
    return int(round(x / 5.0) * 5)


def reparto(ctx, d, s):
    """Reparte el tiempo de aprendizaje de la jornada (SQL + teoría + práctica) entre lecciones, SQL, práctica y criterio."""
    bl = [(a.strip(), b) for a, b in d['bloques']]
    pool = d['completo'] - sum(b for a, b in bl if a not in POOL)     # los bloques fijos no cambian: el bloque de aprendizaje es el resto
    L = lectura_dia(ctx, s)
    C = (s.get('criterio') or {}).get('min', 0)
    E = pool - L - C
    obl = [norm(x) for x in s['obligatorio'] if not norm(x)['id'].startswith('EXAMEN:')]
    sql_est = sum(estimar(ctx, x) for x in obl if tipo(x['id']) == 'SQL') + sum(estimar(ctx, x, repaso=True) for x in s['repaso'] if tipo(norm(x)['id']) == 'SQL')
    otros_est = sum(estimar(ctx, x) for x in obl if tipo(x['id']) != 'SQL') + sum(estimar(ctx, x, repaso=True) for x in s['repaso'] if tipo(norm(x)['id']) != 'SQL')
    if E <= 0:
        sql = pr = 0
    elif sql_est and otros_est:
        sql = max(10, redondear5(E * sql_est / (sql_est + otros_est)))
        sql = min(sql, E - 10)
        pr = E - sql
    elif otros_est:
        sql, pr = 0, E
    else:
        sql, pr = E, 0
    return {'pool': pool, 'L': L, 'C': C, 'E': E, 'SQL': sql, 'Práctica': pr, 'sql_est': sql_est, 'otros_est': otros_est}


def nuevos_bloques(ctx, d, s):
    r = reparto(ctx, d, s)
    resto = [(a.strip(), b) for a, b in d['bloques'] if a.strip() not in POOL]
    nuevo = []
    if r['L']:
        nuevo.append(['Lecciones', r['L']])
    if r['SQL']:
        nuevo.append(['SQL', r['SQL']])
    if r['Práctica']:
        nuevo.append(['Práctica', r['Práctica']])
    if r['C']:
        nuevo.append(['Criterio', r['C']])
    nuevo += [list(x) for x in resto]
    return nuevo


ACCIONES = {
    'Lecciones': 'Lee las lecciones NÚCLEO de arriba y responde «Para comprobar que entendiste» sin mirar. La micropráctica es REFUERZO.',
    'SQL': 'Escribir y ejecutar consultas propias (OBLIGATORIO y REPASO de SQL).',
    'Práctica': ACCION,
    'Criterio': 'Actividad de criterio analítico o hito de comprensión (sección «Criterio analítico y comprensión»).',
}


def tabla_bloques(bloques, filas_resto, practica_base=False):
    lineas = ['|Bloque|Minutos|Acción|', '|---|---:|---|']
    for a, m in bloques:
        if a in ACCIONES:
            accion = ACCIONES[a]
            if a == 'Lecciones' and practica_base:
                accion = accion.replace('La micropráctica es REFUERZO.', 'El checkpoint BASE se cuenta en Práctica; solo el resto de la micropráctica es REFUERZO.')
            lineas.append(f'|{a}|{m}|{accion}|')
        elif a == 'Examen y corrección':
            lineas.append(f'|{a}|{m}|{ACCION}|')
        else:
            lineas.append(f'|{a}|{m}|{filas_resto.get(a, "")}|')
    return '\n'.join(lineas)


# ───────────────────────────── secciones de la guía ─────────────────────────────
def seccion_estudiar(ctx, dia, s):
    ids = s.get('lecciones') or []
    L = lectura_dia(ctx, s)
    if not ids:
        return ('## Qué estudiar\n\nHoy no hay lectura nueva: el estudio es la práctica. Si algo te bloquea, vuelve a la lección enlazada en el enunciado '
                'del ejercicio (todas siguen disponibles como consulta).\n')
    lineas = [f'## Qué estudiar · lecciones NÚCLEO ({L} min de lectura)', '']
    for i in ids:
        d = info_leccion(ctx, i)
        extra = f' · micropráctica {d["practica"]} min (REFUERZO)' if d['practica'] else ''
        if d.get('practica_base'):
            extra = (f' · checkpoint BASE {d["practica_base"]} min (contado en OBLIGATORIO)'
                     f' · resto de micropráctica {d["practica"] - d["practica_base"]} min (REFUERZO)')
        lineas.append(f'- [ ] {enlace_leccion(ctx, i)} · NÚCLEO · lectura {d["lectura"]} min{extra}.')
    lineas.append('- [ ] Predice el resultado de un ejemplo antes de ejecutarlo y declara qué representa una fila.')
    caps = capitulos_dia(ctx, s)
    consulta = ', '.join(f'[{c}](../../02_TEORIA/{c}.md)' for c in caps)
    lineas += ['', f'Consulta: {consulta}. Las lecciones que no están arriba siguen disponibles; las clasifica '
               '[`RUTAS.md`](../RUTAS.md) como REFUERZO o PROFUNDIZACIÓN.']
    return '\n'.join(lineas) + '\n'


def bloque_practica(ctx, dia, d, original_dataset):
    obl = [norm(x) for x in d['obligatorio']]
    est = sum(estimar(ctx, x) for x in obl) + sum(estimar(ctx, x, repaso=True) for x in d['repaso'])
    lineas = ['## Práctica y archivos', '']
    lineas.append(f'Entrada principal: **{d.get("dataset") or original_dataset}**; la ruta exacta aparece en cada enunciado.')
    lineas.append('SQL utiliza `04_DATASETS/comercial.db`. Los CSV/raw y el modelo tienen diccionarios junto a sus datos.')
    lineas.append('Cada ejercicio está clasificado: **OBLIGATORIO** (núcleo del día y condición de la puerta), **REPASO** (SQL que ya hiciste, '
                  'de memoria), **REFUERZO** (si la puerta falló o sobra tiempo) u **OPCIONAL** (no desplaza lo obligatorio).')
    lineas.append('Un notebook es un ejemplo guiado, no una jornada adicional. El sábado prioriza examen y corrección.')
    lineas.append('')
    lineas += antes_de_empezar(ctx, d)
    if obl:
        aviso = ' (sin contar el examen, que ocupa su propio bloque)' if any(x['id'].startswith('EXAMEN:') for x in obl) else ''
        lineas += [f'### OBLIGATORIO · estimación con margen ≈ {est} min{aviso} (supuestos en `01_PLAN_DIARIO/COMPETENCIAS.md`)', '']
        lineas += [f'- [ ] {enlace(ctx, x)}' + ('' if str(enlace(ctx, x)).endswith('.') else '.') for x in obl]
        lineas.append('')
    if d['repaso']:
        lineas += ['### REPASO · 10 minutos, de memoria y sin mirar la solución', '']
        lineas += [f'- [ ] {enlace(ctx, x)}.' for x in d['repaso']]
        lineas.append('')
    if d['refuerzo']:
        lineas += ['### REFUERZO · si la puerta no se cumplió o sobra tiempo', '']
        lineas += [f'- [ ] {enlace(ctx, x)}.' for x in d['refuerzo']]
        lineas.append('')
    if d['opcional']:
        lineas += ['### OPCIONAL · enriquecimiento; nunca desplaza lo obligatorio', '']
        lineas += [f'- [ ] {enlace(ctx, x)}.' for x in d['opcional']]
        lineas.append('')
    if d.get('puerta'):
        lineas += ['## Puerta de competencia', '', f'**{d["puerta"]["texto"]}**', '',
                   'Las fechas son objetivos, no plazos. Si la puerta no se cumple, no avanzas al bloque siguiente: haces REFUERZO y la secuencia se corre sin acumular horas '
                   '(ver `01_PLAN_DIARIO/COMPETENCIAS.md`).', '']
    lineas += seccion_criterio(ctx, dia, d)
    lineas += seccion_extendida(ctx, dia, d)
    return '\n'.join(lineas) + '\n'


def seccion_criterio(ctx, dia, s):
    c = s.get('criterio')
    lineas = ['## Criterio analítico y comprensión', '']
    if not c:
        lineas += ['Hoy no hay actividad escrita: la jornada ya contiene su propia demostración (clase del lunes, examen o proyecto). '
                   'Aun así, al cerrar, di en una frase **qué decisión de negocio cambia el resultado de hoy** y qué dato no tienes para afirmarla.', '']
        return lineas
    i = c['id']
    carpeta = 'Analitico' if i.startswith('AN') else 'Comprension'
    ruta = f'../../03_EJERCICIOS/{carpeta}/{i}.md'
    lineas.append(f'- [ ] [{titulo_actividad(ctx, i)}]({ruta}) · {c["min"]} min.')
    if i.startswith('H'):
        lineas += ['', 'Es un **hito de comprensión**: debes poder **explicar** el concepto con tus palabras, **predecir** una salida antes de ejecutar, '
                   '**resolver una variante nueva** sin copiar y **justificar** tus decisiones. Un OK del corrector no basta: sin este hito la puerta '
                   'no se da por cumplida.', '']
    else:
        lineas += ['', 'Escribe tu respuesta en `mi_trabajo/analitico/` con el mismo nombre del archivo. No hay corrector: compara tu razonamiento con la rúbrica '
                   'del enunciado y, solo después de escribirlo, con `08_SOLUCIONES/controles_analitico.md`.', '']
    return lineas


def seccion_extendida(ctx, dia, s):
    cap = EXTRA_MIN[(dia - 1) % 7]
    lineas = [f'## EXTENDIDA (voluntaria, hasta {cap} min)', '',
              f'Solo si la jornada BASE quedó terminada y tienes energía: elige de esta lista hasta {cap} min. '
              'Nunca reemplaza el descanso ni el cierre; lo que no hagas no se acumula.', '']
    items = []
    for i, c in ctx.lecciones['lecciones'].items():
        if c.get('dia_ext') == dia:
            d = info_leccion(ctx, i)
            practica = d['practica'] - d.get('practica_base', 0)
            items.append((f'{enlace_leccion(ctx, i)} · {d["tipo"]} · lectura {d["lectura"]} + micropráctica {practica} = {d["lectura"] + practica} min'
                          f' — {d["cuando"]}', d['lectura'] + practica))
    for x in s['refuerzo'][:3]:
        items.append((f'{enlace(ctx, x)} · REFUERZO · ≈ {estimar(ctx, x)} min', estimar(ctx, x)))
    if not items:
        lineas.append('Sin propuesta nueva: repite sin mirar uno de los ejercicios OBLIGATORIOS de la semana.')
    for texto, _m in items:
        lineas.append(f'- [ ] {texto}')
    lineas += ['', 'Rutas y horas por semana: [`RUTAS.md`](../RUTAS.md).', '']
    return lineas


def conocidos_antes(ctx, dia):
    """Últimos ejercicios de SQL y de Python resueltos (OBLIGATORIO/REPASO con tiempo propio) antes de la jornada: material del modo MÍNIMO."""
    sql, py = [], []
    for d in ctx.calendario:
        if d['dia'] >= dia:
            break
        if d['dia'] in PROTEGIDOS:
            sql += [i for i in d.get('sql', []) if i not in sql]
            py += [i for i in d.get('python', []) if i not in py]
            continue
        s = ctx.nucleo['dias'].get(str(d['dia']))
        if not s:
            continue
        for x in s['obligatorio'] + s['repaso']:
            it = norm(x)
            if it.get('est') == 0 or it['id'].startswith('EXAMEN:'):
                continue
            if tipo(it['id']) == 'SQL' and it['id'] not in sql:
                sql.append(it['id'])
            elif tipo(it['id']) == 'PY' and it['id'] not in py:
                py.append(it['id'])
    return sql[-2:], py[-2:]


def seccion_reducido(ctx, dia, cal, s):
    examen = [norm(x)['id'] for x in s['obligatorio'] if norm(x)['id'].startswith('EXAMEN:')]
    nombres = ', '.join(nombre_corto(ctx, x) for x in s['reducido'])
    pendientes = [nombre_corto(ctx, x) for x in s['obligatorio'] if norm(x)['id'] not in {norm(y)['id'] for y in s['reducido']}
                  and not norm(x).get('est') == 0]
    L = ['## REDUCIDO', '']
    if examen:
        L += [f'{cal["reducido"]} minutos: haz solo la evaluación del examen ({examen[0].split(":")[1]}), de 60 minutos, sin consultar nada. '
              'La corrección (25 min) y el simulacro (30 min) se hacen en el siguiente bloque disponible, sin sumar horas.',
              f'Haz solo: {nombres}.', '',
              'Qué no acredita: una evaluación sin corrección no cierra la puerta; la puerta se evalúa cuando se corrige y se completa el hito de comprensión.',
              'Empleo: si no cabe una postulación completa, registra el siguiente paso y retómalo en el siguiente bloque laboral.',
              'No agregues las horas omitidas al día siguiente.', '']
        return '\n'.join(L)
    lecs = s.get('reducido_lecciones') or []
    Lm = lectura_ids(ctx, lecs)
    Em = s['reducido_min']
    total = Lm + Em + 5
    L.append(f'Plan: {cal["reducido"]} minutos. Uso previsto de primera vez: lectura mínima {Lm} + entrega reducida {Em} + cierre 5 = {total} min; '
             f'el resto, si lo hay, es empleo o holgura (las estimaciones tienen un margen de ±35 %).')
    if lecs:
        L.append(f'- **Lectura mínima ({Lm} min):** ' + '; '.join(enlace_leccion(ctx, i) for i in lecs) +
                 '. Sin micropráctica; las demás lecciones del día quedan como consulta.')
    else:
        L.append('- **Lectura:** hoy no hay lectura en este modo (la preparación de la entrega reducida viene de jornadas anteriores).')
    L.append(f'- **Haz solo: {nombres}.** Entrega reducida ({Em} min): {s["reducido_entrega"]}')
    L.append('- **Pasa a REFUERZO (no se suma a otro día):** ' + (', '.join(pendientes) if pendientes else 'nada del OBLIGATORIO') +
             ('; la actividad de criterio del día se hace en el siguiente bloque disponible.' if s.get('criterio') else '.'))
    if s.get('puerta'):
        L.append(f'- **Qué no acredita:** este modo no cumple la {s["puerta"]["id"]}; mantiene la continuidad y la jornada siguiente comprueba su entrada.')
    else:
        L.append('- **Qué no acredita:** mantiene la continuidad, pero no acredita lo que dejaste en REFUERZO; la jornada siguiente comprueba su entrada.')
    L += ['- Empleo: si no cabe una postulación completa, registra el siguiente paso y retómalo en el siguiente bloque laboral. '
          'No agregues las horas omitidas al día siguiente.', '']
    return '\n'.join(L)


def seccion_minimo(ctx, dia, cal, s):
    sql, py = conocidos_antes(ctx, dia)
    ejemplo = []
    if sql:
        ejemplo.append('una consulta SQL que ya resolviste (p. ej. ' + ' o '.join(sql) + ')')
    if py:
        ejemplo.append('una función de Python que ya resolviste (p. ej. ' + ' o '.join(py) + ')')
    L = ['## MÍNIMO', '',
         f'{cal["minimo"]} minutos = 15 de práctica ya conocida + 5 de cierre. Rehaz sin mirar ' + ' o '.join(ejemplo) + ' y explica una decisión.',
         'No acredita contenidos: no avanza ninguna puerta, no sustituye el OBLIGATORIO de hoy (que pasa a REFUERZO) y solo sirve para mantener la continuidad. '
         'Si necesitas descansar, el descanso reemplaza la sesión.', '']
    return '\n'.join(L)


def preparaciones_dia(ctx, dia):
    return [(i, p) for i, p in ctx.nucleo.get('preparaciones', {}).items() if p['dia'] == dia]


def insertar_preparaciones(ctx, dia, texto):
    """Añade solo un bloque previo; D01 se prepara desde sus enunciados y su guía se conserva."""
    preparaciones = preparaciones_dia(ctx, dia)
    if dia == 1 or not preparaciones:
        return texto
    lineas = ['<!-- SECUENCIA:GUIA:INICIO -->', '### Preparación obligatoria antes del intento', '']
    for i, p in preparaciones:
        lineas.append(f'- [{p["titulo"]}](../../{p["archivo"]}#{p["ancla"]}) · antes de {i} · {p["min"]} min adicionales de lectura y predicción.')
    total = sum(p['min'] for _, p in preparaciones)
    lineas += ['', f'Son {total} min adicionales a la estimación BASE, registrados en CARGA_ESTIMADA.md; no se recortan los tiempos de los ejercicios. '
               'En REDUCIDO conserva la preparación de la actividad que hagas. Si pospones una actividad, recupera su preparación antes de intentarla '
               'y antes de la puerta que la requiere; MÍNIMO solo repasa lo conocido.']
    if dia == 2:
        lineas += ['', 'Antes de P02 completa las comparaciones y None de 7.6, además de su puente de decisión: una lectura pendiente no se acredita '
                   'como aprendida. Si no cabe, reduce la entrega y recupera la base antes de D03/H01/S01. La preparación de texto precede a P03 y '
                   'a su uso en P09/D10. S9 es ampliación y C01 es opcional; las tareas BASE son S2, S7, P02 y P03.']
    lineas += ['<!-- SECUENCIA:GUIA:FIN -->', '', '']
    bloque = '\n'.join(lineas)
    patron = r'<!-- SECUENCIA:GUIA:INICIO -->.*?<!-- SECUENCIA:GUIA:FIN -->\n\n'
    if '<!-- SECUENCIA:GUIA:INICIO -->' in texto:
        return re.sub(patron, lambda m: bloque, texto, count=1, flags=re.S)
    pos = texto.index('## Distribución neta')
    return texto[:pos] + bloque + texto[pos:]


def aplicar_guia(ctx, dia, d, d_cal, nl='\n'):
    carpeta = ctx.raiz / '01_PLAN_DIARIO' / 'dias'
    ruta = next(carpeta.glob(f'D{dia:02}_*.md'))
    texto = ruta.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in texto else '\n'
    t = texto.replace('\r\n', '\n')
    if d.get('titulo'):
        t = re.sub(r'^(# Día \d\d · [^\n]+\n\n)## [^\n]+', lambda m: m.group(1) + '## ' + d['titulo'], t, count=1, flags=re.M)
    if d.get('objetivo'):
        t = re.sub(r'^\*\*Objetivo de trabajo:\*\* [^\n]*', lambda m: f'**Objetivo de trabajo:** {d["objetivo"]}', t, count=1, flags=re.M)
        t = re.sub(r'^Habilidad laboral: [^\n]*', lambda m: f'Habilidad laboral: {d["objetivo"]}', t, count=1, flags=re.M)
    # «Qué estudiar» y «Distribución neta»
    a = t.index('## Qué estudiar')
    b = t.index('## Distribución neta')
    t = t[:a] + seccion_estudiar(ctx, dia, d) + '\n' + t[b:]
    b = t.index('## Distribución neta')
    lineas = t[b:].split('\n')
    j = 2
    while j < len(lineas) and not lineas[j].startswith('|'):
        j += 1
    k = j
    filas_resto = {}
    while k < len(lineas) and lineas[k].startswith('|'):
        m = re.match(r'\|([^|]+)\|(\d+)\|([^|]*)\|$', lineas[k])
        if m:
            filas_resto[m.group(1).strip()] = m.group(3)
        k += 1
    tabla = tabla_bloques(nuevos_bloques(ctx, d_cal, d), filas_resto,
                         any(info_leccion(ctx, i).get('practica_base') for i in d.get('lecciones') or []))
    t = t[:b] + '\n'.join(lineas[:j]) + '\n' + tabla + '\n' + '\n'.join(lineas[k:])
    # práctica, criterio y EXTENDIDA
    m = re.search(r'^## Práctica y archivos\n\nEntrada principal: \*\*([^*]+)\*\*', t, re.M)
    original_dataset = m.group(1) if m else 'comercial.db'
    inicio = t.index('## Práctica y archivos')
    fin = t.index('## Comprobar y entregar')
    t = t[:inicio] + bloque_practica(ctx, dia, d, original_dataset) + t[fin:]
    comando = comando_correccion(d['obligatorio'] + d['repaso'] + d['refuerzo'])
    if comando:
        t = re.sub(r'^Ejemplo de corrección:[^\n]*', lambda m: f'Ejemplo de corrección: {comando}.', t, count=1, flags=re.M)
    t = re.sub(r'^Python usa el corrector por ID\.[^\n]*',
               'Python, mini-ETL y depuración usan su corrector por ID (`corregir_python.py`, `corregir_mini_etl.py`, `corregir_depuracion.py`). '
               'Estadística/casos utilizan controles y rúbricas después del intento.', t, count=1, flags=re.M)
    inicio = t.index('## REDUCIDO')
    fin = t.index('## Empleo y clase')
    t = t[:inicio] + seccion_reducido(ctx, dia, d_cal, d) + '\n' + seccion_minimo(ctx, dia, d_cal, d) + '\n' + t[fin:]
    t = insertar_preparaciones(ctx, dia, t)
    ruta.write_bytes(t.replace('\n', nl).encode('utf-8'))


BLOQUE_D02 = ('<!-- E2:LECCIONES:INICIO -->\n'
              '### Lecciones de hoy (Etapa 2 · bloque añadido; el objetivo, los ejercicios y los tiempos de D02 no cambian)\n\n'
              '{lineas}\n\n'
              'Son {total} min de lectura frente a los 30 min del bloque «Teoría»: lee primero 1.4 y de 7.6 lo que alcances; lo que no leas queda como '
              'consulta y no se suma a otro día. La micropráctica de ambas es REFUERZO. Las demás lecciones de los capítulos 1 y 7 son consulta '
              '(clasificación en [`RUTAS.md`](../RUTAS.md)).\n'
              '<!-- E2:LECCIONES:FIN -->\n')


def aplicar_d02(ctx):
    ids = ctx.lecciones['lecciones']
    d02 = [i for i, c in ids.items() if c.get('dia') == 2]
    if not d02:
        return
    carpeta = ctx.raiz / '01_PLAN_DIARIO' / 'dias'
    ruta = next(carpeta.glob('D02_*.md'))
    texto = ruta.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in texto else '\n'
    t = texto.replace('\r\n', '\n')
    estados = {m.group(2): m.group(1) for m in re.finditer(r'^- \[([ xX])\] \[(\d+\.\d+)\b', t, re.M)}
    lineas = '\n'.join(f'- [{estados.get(i, " ")}] {enlace_leccion(ctx, i)} · NÚCLEO · lectura {info_leccion(ctx, i)["lectura"]} min.' for i in d02)
    total = sum(info_leccion(ctx, i)['lectura'] for i in d02)
    bloque = BLOQUE_D02.format(lineas=lineas, total=total)
    if '<!-- E2:LECCIONES:INICIO -->' in t:
        t = re.sub(r'<!-- E2:LECCIONES:INICIO -->.*?<!-- E2:LECCIONES:FIN -->\n', lambda m: bloque, t, flags=re.S)
    else:
        a = t.index('## Distribución neta')
        t = t[:a] + bloque + '\n' + t[a:]
    t = insertar_preparaciones(ctx, 2, t)
    ruta.write_bytes(t.replace('\n', nl).encode('utf-8'))


def aplicar_domingo(ctx, dia, d_cal):
    carpeta = ctx.raiz / '01_PLAN_DIARIO' / 'dias'
    ruta = next(carpeta.glob(f'D{dia:02}_*.md'))
    previo = ruta.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in previo else '\n'
    cab = previo.replace('\r\n', '\n').split('\n')[0]
    semana = (dia - 1) // 7 + 1
    pend = []
    for n in range((semana - 1) * 7 + 1, dia):
        s = ctx.nucleo['dias'].get(str(n))
        if s:
            pend += [norm(x)['id'] for x in s['refuerzo'][:1]]
    pend = [p for p in dict.fromkeys(pend) if tipo(p) != 'NB'][:4]
    ext = [(i, info_leccion(ctx, i)) for i, c in ctx.lecciones['lecciones'].items() if c.get('dia_ext') == dia]
    l = [cab, '', '## Domingo flexible: descanso o recuperación voluntaria', '',
         'COMPLETO, REDUCIDO y MÍNIMO: **0 minutos obligatorios**. El descanso es la opción por defecto y no genera deuda: no hay SQL, LinkedIn ni '
         'recuperación obligatoria.',
         f'Si tienes energía puedes dedicar **entre {DOMINGO_MIN[0]} y {DOMINGO_MIN[1]} minutos** a UNA de estas opciones. Elige una y no la mezcles con el estudio de otro día.', '',
         '- [ ] **Descanso real** (opción por defecto). Reservé este descanso sin convertirlo en una deuda.']
    if pend:
        l.append(f'- [ ] **Recuperación voluntaria ({DOMINGO_MIN[0]}–90 min):** rehace sin mirar el primer REFUERZO pendiente de la semana '
                 f'({", ".join(pend)}), que ya aparece en la guía de cada día. No recuperes un día completo.')
    for i, di in ext:
        l.append(f'- [ ] **EXTENDIDA (60–{DOMINGO_MIN[1]} min):** {enlace_leccion(ctx, i)} · {di["tipo"]} · '
                 f'{di["lectura"] + di["practica"]} min — {di["cuando"]}')
    l += ['', 'Reglas: si ayer fue examen, no lo revises hoy; no consultes soluciones; no hace falta publicar ni hacer commit; '
          'lo que no hagas no se traslada a otro día.']
    if dia == 42:
        l += ['', 'Hoy es la víspera de la evaluación final (23–30 de noviembre): lo más útil es dormir bien. Si estudias, que sea solo releer tus propias notas '
              'y tu `mi_trabajo/errores.md`; no abras la evaluación final ni sus soluciones.']
    l += ['', 'No requiere entrega. Habilidad: gestionar una carga sostenible.', '']
    ruta.write_bytes('\n'.join(l).replace('\n', nl).encode('utf-8'))


def clasificar(ids):
    sql, py, st, otros = [], [], [], []
    for item in ids:
        i = norm(item)['id']
        t = tipo(i)
        if t == 'SQL':
            sql.append(i)
        elif t == 'PY':
            py.append(i)
        elif t == 'ST':
            st.append(i)
        elif t != 'EXAMEN':
            otros.append(i)
    return sql, py, st, otros


def actualizar_calendario(ctx):
    for d in ctx.calendario:
        n = d['dia']
        prep = preparaciones_dia(ctx, n)
        if prep:
            d['preparaciones'] = [i for i, _ in prep]
            d['preparacion_lectura_min'] = sum(p['min'] for _, p in prep)
        inicial = ctx.nucleo.get('dias_iniciales', {}).get(str(n))
        if inicial:
            d['nucleo'] = inicial
        if n == 1:
            continue
        if n == 2:
            d['lecciones'] = [i for i, c in ctx.lecciones['lecciones'].items() if c.get('dia') == 2]
            continue
        if d['completo'] == 0:
            d['voluntario_min'] = list(DOMINGO_MIN)
            continue
        if str(n) not in ctx.nucleo['dias']:
            continue
        s = ctx.nucleo['dias'][str(n)]
        todos = s['obligatorio'] + s['repaso'] + s['refuerzo'] + s['opcional']
        sql, py, st, otros = clasificar(todos)
        if s.get('titulo'):
            d['titulo'] = s['titulo']
        if s.get('objetivo'):
            d['objetivo'] = s['objetivo']
        d['teoria'] = capitulos_dia(ctx, s)
        if s.get('dataset'):
            d['dataset'] = s['dataset']
        d['sql'], d['python'], d['estadistica'], d['otros'] = list(dict.fromkeys(sql)), py, st, otros
        d['nucleo'] = {'obligatorio': [norm(x)['id'] for x in s['obligatorio']], 'repaso': s['repaso'],
                       'refuerzo': [norm(x)['id'] for x in s['refuerzo']], 'opcional': [norm(x)['id'] for x in s['opcional']],
                       'reducido': [norm(x)['id'] for x in s['reducido']], 'puerta': (s.get('puerta') or {}).get('id')}
        d['lecciones'] = s.get('lecciones') or []
        d['criterio'] = (s.get('criterio') or {}).get('id')
        d['entra'] = [e['texto'] for e in s.get('entra') or []]
        d['reducido_detalle'] = {'lecciones': s.get('reducido_lecciones') or [], 'min': s.get('reducido_min'), 'entrega': s.get('reducido_entrega')}
        d['bloques'] = nuevos_bloques(ctx, d, s)
        d['extendida_min'] = EXTRA_MIN[(n - 1) % 7]
    (ctx.raiz / '01_PLAN_DIARIO' / 'calendario.json').write_text(json.dumps(ctx.calendario, ensure_ascii=False, indent=2), encoding='utf-8')
    with (ctx.raiz / '01_PLAN_DIARIO' / 'calendario.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dia', 'fecha', 'semana', 'titulo', 'completo_min', 'reducido_min', 'minimo_min', 'sql', 'python', 'estadistica', 'otros', 'obligatorio', 'preparaciones', 'preparacion_lectura_min'])
        for d in ctx.calendario:
            w.writerow([d['dia'], d['fecha'], d['semana'], d['titulo'], d['completo'], d['reducido'], d['minimo'], ';'.join(d['sql']),
                        ';'.join(d['python']), ';'.join(d['estadistica']), ';'.join(d['otros']), ';'.join(d.get('nucleo', {}).get('obligatorio', [])),
                        ';'.join(d.get('preparaciones', [])), d.get('preparacion_lectura_min', 0)])


def etiqueta_tipo(ctx, i):
    c = ctx.lecciones['lecciones'][i]
    if c['tipo'] == 'NÚCLEO':
        return f'núcleo · D{c["dia"]:02}'
    return 'refuerzo' if c['tipo'] == 'REFUERZO' else 'profundización'


def actualizar_indices_teoria(ctx):
    """Sincroniza clasificación y minutos de los índices con las fuentes y los encabezados de lección."""
    for f in sorted((ctx.raiz / '02_TEORIA').glob('[0-9][0-9]_*.md')):
        b = f.read_bytes().decode('utf-8')
        nl = '\r\n' if '\r\n' in b else '\n'
        lineas = b.replace('\r\n', '\n').split('\n')
        total = 0
        for k, linea in enumerate(lineas):
            m = re.match(r'^\| (\d+\.\d+) \|', linea)
            if not m or m.group(1) not in ctx.lecciones['lecciones']:
                continue
            celdas = re.split(r'(?<!\\)\|', linea)
            if len(celdas) != 7:                     # | # | Lección | Qué aprendes / KPI | Tipo | Tiempo |
                continue
            celdas[4] = f' {etiqueta_tipo(ctx, m.group(1))} '
            info = info_leccion(ctx, m.group(1))
            minutos = info['lectura'] + info['practica']
            celdas[5] = f' {minutos} min '
            total += minutos
            lineas[k] = '|'.join(celdas)
        nuevo_texto = '\n'.join(lineas)
        declarado = re.search(r'unas (?:(\d+) h)? ?(?:(\d+) min)?', nuevo_texto)
        if total and declarado and int(declarado.group(1) or 0) * 60 + int(declarado.group(2) or 0) != total:
            nuevo_texto = nuevo_texto[:declarado.start()] + f'unas {total // 60} h {total % 60} min' + nuevo_texto[declarado.end():]
        if nuevo_texto != b.replace('\r\n', '\n'):
            f.write_bytes(nuevo_texto.replace('\n', nl).encode('utf-8'))


def actualizar_plan(ctx):
    """Sincroniza los títulos de las jornadas en PLAN_V5.md con nucleo.json."""
    p = ctx.raiz / '01_PLAN_DIARIO' / 'PLAN_V5.md'
    t = p.read_text(encoding='utf-8')
    for n, s in ctx.nucleo['dias'].items():
        if s.get('titulo'):
            patron = rf'(\*\*D{int(n):02} · [^\n]*?:\*\* \[)[^\]]+(\]\(dias/D{int(n):02}_)'
            t = re.sub(patron, lambda m: m.group(1) + s['titulo'] + m.group(2), t, count=1)
    p.write_text(t, encoding='utf-8')


# ───────────────────────────── cargas y rutas ─────────────────────────────
def metricas(ctx):
    """Una fila por jornada con sus minutos de plan y estimados. Los días sin entrada en nucleo.json (D01, D02, domingos) conservan su diseño."""
    filas = []
    for d in ctx.calendario:
        n = d['dia']
        s = ctx.nucleo['dias'].get(str(n))
        fila = {'dia': n, 'fecha': d['fecha'], 'semana': d['semana'], 'titulo': d['titulo'], 'completo': d['completo'], 'L': 0, 'C': 0, 'E': 0,
                'estimado': d['completo'], 'lecciones': [], 'criterio': None, 'obl': [], 'puerta': None, 'examen': False}
        if s:
            r = reparto(ctx, d, s)
            obl = [norm(x) for x in s['obligatorio']]
            e = sum(estimar(ctx, x) for x in obl) + sum(estimar(ctx, x, repaso=True) for x in s['repaso'])
            fila.update({'L': r['L'], 'C': r['C'], 'E': e, 'estimado': d['completo'] - r['pool'] + r['L'] + r['C'] + e,
                         'lecciones': s.get('lecciones') or [], 'criterio': (s.get('criterio') or {}).get('id'),
                         'obl': [x['id'] for x in obl], 'puerta': (s.get('puerta') or {}).get('id'), 'pool': r['pool'],
                         'examen': any(x['id'].startswith('EXAMEN:') for x in obl), 'titulo': s.get('titulo') or d['titulo']})
        elif n in PROTEGIDOS:
            bl = {a.strip(): m for a, m in d['bloques']}
            pool = sum(m for a, m in bl.items() if a in POOL)
            teoria = bl.get('Teoría', 0)
            fila['pool'] = pool
            fila['L'] = teoria
            fila['E'] = pool - teoria
            if n == 2:
                ids = [i for i, c in ctx.lecciones['lecciones'].items() if c.get('dia') == 2]
                lec = sum(info_leccion(ctx, i)['lectura'] for i in ids)
                fila['lecciones'] = ids
                fila['L'] = max(teoria, lec)
                fila['estimado'] = d['completo'] + max(0, lec - teoria)
            fila['obl'] = ctx.nucleo.get('dias_iniciales', {}).get(str(n), {}).get('obligatorio', [])
        prep_min = sum(p['min'] for _, p in preparaciones_dia(ctx, n))
        # D01 concreta 16 de sus 20 minutos de teoría existentes; los demás son adicionales.
        adicional = max(0, prep_min - fila['L']) if n == 1 else prep_min
        fila['L'] += adicional
        fila['estimado'] += adicional
        bl = {a.strip(): m for a, m in d['bloques']}
        fila['X'] = sum(m for a, m in bl.items() if a.startswith('Examen'))
        fila['F'] = d['completo'] - sum(m for a, m in bl.items() if a in POOL) - fila['X'] if d['completo'] else 0
        filas.append(fila)
    return filas


def tabla_carga(ctx):
    return [(f['dia'], f['fecha'], f['titulo'], f['completo'], f['estimado'], round(f['estimado'] / f['completo'], 2))
            for f in metricas(ctx) if f['completo'] and str(f['dia']) in ctx.nucleo['dias']]


def horas(m):
    return f'{m / 60:.1f}'.replace('.', ',')


def r2(x):
    return f'{x:.2f}'.replace('.', ',')


def prerrequisitos(ctx, i):
    """Lecciones que el encabezado de la lección i declara como prerrequisito (enlaces, «lecciones A a B» o «capítulo N completo»)."""
    c = ctx.lecciones['lecciones'][i]
    texto = (ctx.raiz / '02_TEORIA' / c['archivo']).read_text(encoding='utf-8').splitlines()[2]
    texto = texto.split('Prerrequisito', 1)[1] if 'Prerrequisito' in texto else ''
    ids = re.findall(r'\[(\d+\.\d+)[ \]]', texto)
    for a, b in re.findall(r'lecciones (\d+\.\d+) a (\d+\.\d+)', texto):
        cap, x = a.split('.')
        ids += [f'{cap}.{k}' for k in range(int(x), int(b.split('.')[1]) + 1)]
    for cap in re.findall(r'cap[ií]tulo (\d+) completo', texto):
        ids += [k for k in ctx.lecciones['lecciones'] if k.split('.')[0] == cap]
    return [k for k in dict.fromkeys(ids) if k in ctx.lecciones['lecciones'] and k != i]


def resumen_semanal(ctx, filas=None):
    filas = filas or metricas(ctx)
    sem = {}
    for f in filas:
        w = f['semana']
        x = sem.setdefault(w, {'plan': 0, 'est': 0, 'L': 0, 'C': 0, 'E': 0, 'ext': 0, 'n_lec': 0, 'n_obl': 0, 'examen': 0, 'fijo': 0, 'X': 0, 'F': 0, 'ajustadas': []})
        x['X'] += f.get('X', 0)
        x['F'] += f.get('F', 0)
        if f['completo'] and f['estimado'] / f['completo'] > 1.15 and not f['examen']:
            x['ajustadas'].append(f'D{f["dia"]:02}')
        x['plan'] += f['completo']
        x['est'] += f['estimado']
        x['L'] += f['L']
        x['C'] += f['C']
        x['E'] += f['E']
        x['n_lec'] += len(f['lecciones'])
        x['n_obl'] += len([o for o in f['obl'] if not o.startswith('EXAMEN:')])
        if f['completo']:
            x['ext'] += EXTRA_MIN[(f['dia'] - 1) % 7]
    return sem


def tabla_evaluacion_final(ctx):
    ef = ctx.nucleo['evaluacion_final']
    L = ['| Fecha | Día | Antes (min) | Ahora (min) | Entrega comprobable | Qué se sustituyó |', '|---|---|---:|---:|---|---|']
    for b in ef['bloques']:
        L.append(f'| {b["fecha"]} | {b["dia"]} | {b["min_previo"]} | {b["min"]} | {b["entrega"]} | {b["cambio"]} |')
    L.append(f'| **Total** | | **{ef["total_previo_min"]}** ({horas(ef["total_previo_min"])} h) | **{ef["total_min"]}** ({horas(ef["total_min"])} h) | | |')
    return L


def escribir_carga(ctx, filas_ignoradas=None):
    filas = metricas(ctx)
    sem = resumen_semanal(ctx, filas)
    ef = ctx.nucleo['evaluacion_final']
    lineas = ['# Carga estimada por jornada (ruta BASE)', '',
              'Estimación de **primera vez** para una persona que todavía depende de ayuda externa. **No es una medición**: los tiempos de cada ejercicio '
              'son los que declara su propio enunciado (punto medio del rango «Primera vez», que ya incluye leer el enunciado, equivocarse, depurar y '
              'verificar), y los multiplicadores de respaldo (SQL ×1,5–2,25; Python ×2–3,25; estadística ×2–2,5; casos ×1,75; Excel/Power BI ×2) y las tareas de '
              'proyecto estimadas a mano son supuestos con un error razonable de ±35 %. Todavía no existen mediciones reales: registra tus minutos en '
              '`mi_trabajo/progreso.csv` y corrige esta tabla con tus datos.', '',
              '## Qué cuenta cada columna (sin dobles conteos)', '',
              '| Columna | Qué incluye | Qué NO incluye |', '|---|---|---|',
              '| **L** | Lectura de las lecciones NÚCLEO y preparaciones obligatorias (lectura/predicción); en D01, 16 min de preparación ocupan sus 20 min de teoría originales | La micropráctica REFUERZO/EXTENDIDA y los checkpoints Pandas contabilizados en E |',
              '| **C** | Actividad de criterio analítico o hito de comprensión | Su revisión posterior con los controles (se hace dentro de la misma actividad) |',
              '| **E** | Ejercicios OBLIGATORIOS y REPASO a tiempo de primera vez (incluye leer el enunciado, depurar y comprobar); PD-BASE y PD-AGR cuentan aquí una sola vez | REFUERZO, OPCIONAL y notebooks; las tareas que son parte de un examen (N2, N3, V4…) no se suman otra vez |',
              '| **X** | Examen 60 + corrección 25 + simulacro 30 = 115 min en los sábados de examen (tiempo fijo) | — |',
              '| **F** | Empleo, postulaciones, LinkedIn y cierre (tiempo fijo del plan) | — |', '',
              'Estimado = F + X + L + C + E. D01 conserva su diseño; D02 suma sus lecciones y preparaciones sobre el bloque original. '
              'La ruta EXTENDIDA (voluntaria) no está incluida.', '',
              '| Día | Fecha | Contenido | Plan (min) | L | C | E | X | F | Estimado (min) | Razón |', '|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for f in filas:
        if not f['completo']:
            continue
        lineas.append(f'| D{f["dia"]:02} | {f["fecha"]} | {f["titulo"]} | {f["completo"]} | {f["L"]} | {f["C"]} | {f["E"]} | {f["X"]} | {f["F"]} | '
                      f'{f["estimado"]} | {r2(f["estimado"] / f["completo"])} |')
    lineas += ['', '| Semana | Plan (min) | Estimado BASE (min) | Estimado BASE (h) | Razón | Jornadas AJUSTADAS (razón > 1,15, sin exámenes) |', '|---:|---:|---:|---:|---:|---|']
    for w, x in sorted(sem.items()):
        lineas.append(f'| {w} | {x["plan"]} | {x["est"]} | {horas(x["est"])} | {r2(x["est"] / x["plan"])} | {", ".join(x["ajustadas"]) or "—"} |')
    tot_p = sum(x['plan'] for x in sem.values())
    tot_e = sum(x['est'] for x in sem.values())
    lineas += ['', f'**Total de las seis semanas (42 jornadas):** plan {tot_p} min ({horas(tot_p)} h); estimado BASE de primera vez {tot_e} min ({horas(tot_e)} h), '
               f'razón {r2(tot_e / tot_p)}. La diferencia de {tot_e - tot_p} min ({horas(tot_e - tot_p)} h) es estimación, no medición: '
               'cabe dentro del margen de ±35 % y se absorbe con REDUCIDO en las jornadas AJUSTADAS; no se compensa con las horas voluntarias de EXTENDIDA.', '',
               'Una razón por encima de 1,15 en una jornada la marca como AJUSTADA: usa el modo REDUCIDO (cada jornada define una entrega menor y '
               'realizable en `RUTAS.md`) y mueve el REFUERZO; no alargues el día. Si una semana queda por encima de 1,1, la puerta se corre sin acumular '
               'horas (ver `COMPETENCIAS.md`).', '',
               '## Evaluación final: bloque posterior, NO incluido en las 90 horas', '',
               f'La evaluación final ({ef["ventana"]}) ocurre **después** de las 42 jornadas y es una séptima semana de evaluación, no parte de las seis semanas. '
               f'Antes reservaba {horas(ef["total_previo_min"])} h; ahora reserva **{horas(ef["total_min"])} h netas** ({ef["total_min"]} min), estimadas de primera vez '
               f'y no medidas. La reducción de {horas(ef["total_previo_min"] - ef["total_min"])} h sale de sustituir trabajo que ya se hizo en C06 (D36–D40) y que '
               'el alumno puede reutilizar con su propio código: no se acorta la evidencia que se exige, se evita construirla dos veces desde cero.', '']
    lineas += tabla_evaluacion_final(ctx)
    lineas += ['', f'Total del programa: {horas(tot_p)} h de plan en seis semanas (estimado {horas(tot_e)} h) + {horas(ef["total_min"])} h de evaluación final '
               f'= {horas(tot_p + ef["total_min"])} h de plan ({horas(tot_e + ef["total_min"])} h estimadas). '
               'Si no puedes dedicar la evaluación final en esas fechas, no se declara autonomía: se reprograma sin acumular horas. '
               + ef['nota'], '']
    (ctx.raiz / '01_PLAN_DIARIO' / 'CARGA_ESTIMADA.md').write_text('\n'.join(lineas), encoding='utf-8')


def escribir_rutas(ctx):
    filas = metricas(ctx)
    sem = resumen_semanal(ctx, filas)
    lec = ctx.lecciones['lecciones']
    preparacion_extra = sum(p['min'] for p in ctx.nucleo.get('preparaciones', {}).values() if p['dia'] != 1)
    L = ['# Rutas de estudio: BASE y EXTENDIDA', '',
         'Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json` y `lecciones.json`; no lo edites a mano. '
         'Las **100 lecciones** de `02_TEORIA` (más el capítulo 19) suman unas 91 horas de primera vez: no caben en seis semanas junto con los ejercicios. '
         'Por eso cada lección está clasificada una a una y **todas siguen disponibles como material de consulta**.', '',
         '## Qué significa cada clase de lección', '',
         '| Clase | Significado | Dónde aparece |', '|---|---|---|',
         '| **NÚCLEO** | Indispensable para aprender los fundamentos y poder avanzar. Su lectura cuenta dentro de las 15 h y tiene día asignado. | Ruta BASE, bloque «Lecciones» de la guía diaria. |',
         '| **REFUERZO** | Se lee cuando una competencia no está dominada o un ejercicio se atasca (cada lección dice cuándo). | EXTENDIDA y recuperación. |',
         '| **PROFUNDIZACIÓN** | Amplía más allá de la base (inferencia, BI avanzado, entrevistas, portafolio). | EXTENDIDA u otros periodos (después de la evaluación final). |', '',
         'La lectura de una lección NÚCLEO es lo que figura en su encabezado («lectura N min»). Su **micropráctica** es práctica guiada sin corrector: '
         'en BASE la sustituyen los ejercicios del día. Excepciones explícitas: los primeros 10 min de práctica de 10.1 (PD-BASE) y de 10.2 (PD-AGR) '
         'son OBLIGATORIOS y se cuentan una sola vez en ejercicios; sus otros 25 y 30 min, respectivamente, son REFUERZO.', '']
    L += ['## Preparación explícita antes de las actividades', '',
          'Los bloques siguientes son obligatorios antes del intento; no promueven lecciones completas de REFUERZO. '
          f'D01 concreta 16 de sus 20 min de teoría ya existentes. Los otros {preparacion_extra} min se añaden a la estimación BASE; '
          'no se ocultan dentro del tiempo de práctica. REDUCIDO conserva la preparación de lo que intenta y recupera lo omitido antes de su puerta.', '',
          '| Día | Antes de | Preparación | Minutos |', '|---|---|---|---:|']
    for i, p in ctx.nucleo.get('preparaciones', {}).items():
        L.append(f'| D{p["dia"]:02} | {i} | [{p["titulo"]}](../{p["archivo"]}#{p["ancla"]}) | {p["min"]} |')
    L += ['', 'D01: S1 y P01 son BASE; S10 es REFUERZO con preparación propia. D02: S2, S7, P02 y P03 son BASE; '
          'S9 es REFUERZO y C01, OPCIONAL. La guía original de D01 y los avances de D02 se conservan.', '']
    # horas por semana
    L += ['## Horas por semana', '',
          '| Semana | BASE plan (min) | BASE estimado (min / h) | Teoría y lecciones NÚCLEO | Criterio e hitos | Ejercicios OBLIGATORIOS | EXTENDIDA extra (L–S) | EXTENDIDA plan (h) | EXTENDIDA estimada (h) |',
          '|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for w, x in sorted(sem.items()):
        ext_total_lo = x['plan'] + x['ext']
        ext_total_hi = ext_total_lo + DOMINGO_MIN[1]
        L.append(f'| {w} | {x["plan"]} | {x["est"]} / {horas(x["est"])} | {x["L"]} min ({x["n_lec"]} lecc.) | {x["C"]} min | {x["E"]} min ({x["n_obl"]} ej.) | '
                 f'{x["ext"]} min | {horas(ext_total_lo)}–{horas(ext_total_hi)} | {horas(x["est"] + x["ext"])}–{horas(x["est"] + x["ext"] + DOMINGO_MIN[1])} |')
    tp = sum(x['plan'] for x in sem.values())
    te = sum(x['est'] for x in sem.values())
    L += ['', f'**BASE:** 15 h netas planificadas por semana ({tp} min en seis semanas). La estimación de primera vez es de {te} min ({horas(te)} h), '
          f'es decir {r2(te / tp)} veces lo planificado: es una estimación conservadora de ±35 %, no una medición, y por eso existen REDUCIDO, MÍNIMO y el '
          'corrimiento de puertas sin acumular horas.', '',
          f'**EXTENDIDA:** BASE más hasta {EXTRA_MIN[0]}–{EXTRA_MIN[1]} min voluntarios por jornada (lunes a sábado) y un domingo opcional de '
          f'{DOMINGO_MIN[0]}–{DOMINGO_MIN[1]} min: entre 20 y 25 horas por semana en el plan. Es voluntaria; el descanso y el cierre no se sacrifican. '
          'Si tu semana BASE ya consumió más de 16,5 horas reales, no uses EXTENDIDA esa semana: descansa.', '']
    # teoría obligatoria vs práctica
    L += ['## Teoría obligatoria frente a práctica', '',
          '| Semana | Teoría y lecciones NÚCLEO | Criterio e hitos | Ejercicios OBLIGATORIOS (estimado) | Teoría : práctica | Examen y corrección | Empleo y cierre |',
          '|---:|---:|---:|---:|---:|---:|---:|']
    for w, x in sorted(sem.items()):
        ex = sum(next((m for a, m in d['bloques'] if a.strip().startswith('Examen')), 0) for d in ctx.calendario if d['semana'] == w and d['completo'])
        resto = x['plan'] - ex - sum((f['pool'] if 'pool' in f else 0) for f in filas if f['semana'] == w)
        L.append(f'| {w} | {x["L"]} | {x["C"]} | {x["E"]} | 1 : {f'{x["E"] / x["L"]:.1f}'.replace('.', ',')} | {ex} | {resto} |' if x['L'] else f'| {w} | 0 | {x["C"]} | {x["E"]} | — | {ex} | {resto} |')
    tl = sum(x['L'] for x in sem.values())
    te2 = sum(x['E'] for x in sem.values())
    tc = sum(x['C'] for x in sem.values())
    L += ['', f'En total: **{tl} min de teoría y lectura NÚCLEO** ({horas(tl)} h; incluye los 20 min de teoría originales de D01), **{tc} min de criterio e hitos** ({horas(tc)} h) y **{te2} min de ejercicios** '
          f'obligatorios ({horas(te2)} h). La columna «Empleo y cierre» incluye el bloque laboral y los 10 minutos diarios de cierre.', '']
    # clasificación por capítulo
    L += ['## Clasificación de las 100 lecciones', '',
          '| Cap. | Tema | NÚCLEO | REFUERZO | PROFUNDIZACIÓN | Lectura NÚCLEO (min) | Total de primera vez (min) |', '|---:|---|---:|---:|---:|---:|---:|']
    nombres = {k: v for k, v in ctx.capitulos.items()}
    por_cap = {}
    for i, c in lec.items():
        cap = i.split('.')[0]
        x = por_cap.setdefault(cap, {'N': 0, 'R': 0, 'P': 0, 'lectN': 0, 'tot': 0})
        d = info_leccion(ctx, i)
        x[{'NÚCLEO': 'N', 'REFUERZO': 'R', 'PROFUNDIZACIÓN': 'P'}[c['tipo']]] += 1
        x['tot'] += d['lectura'] + d['practica']
        if c['tipo'] == 'NÚCLEO':
            x['lectN'] += d['lectura']
    tN = tR = tP = tl2 = tt = 0
    for cap in sorted(por_cap, key=int):
        x = por_cap[cap]
        tema = (ctx.raiz / '02_TEORIA' / f'{nombres[cap]}.md').read_text(encoding='utf-8').splitlines()[0].split('—', 1)[-1].strip()
        L.append(f'| {cap} | {tema} | {x["N"]} | {x["R"]} | {x["P"]} | {x["lectN"]} | {x["tot"]} |')
        tN += x['N']
        tR += x['R']
        tP += x['P']
        tl2 += x['lectN']
        tt += x['tot']
    puente_min = sum(p['min'] for p in ctx.lecciones['puente'].values())
    L.append(f'| **Total** | | **{tN}** | **{tR}** | **{tP}** | **{tl2}** | **{tt}** |')
    L += ['', f'El capítulo 19 (puente) es un archivo único: sus §1–§4 ({puente_min} min) son NÚCLEO y se leen junto a ME01–ME03 y DB01.', '']
    # lista de lecciones
    L += ['## Lección por lección', '',
          '| Lección | Clase | Día / EXTENDIDA | Lectura | Micropráctica | Cuándo leerla si no es NÚCLEO |', '|---|---|---|---:|---:|---|']
    for i, c in lec.items():
        d = info_leccion(ctx, i)
        if c['tipo'] == 'NÚCLEO':
            donde = f'D{c["dia"]:02}'
            cuando = ''
        else:
            donde = f'ext. D{c["dia_ext"]:02}' if c.get('dia_ext') else 'otros periodos'
            cuando = c['cuando']
        practica = str(d['practica'])
        if d.get('practica_base'):
            practica = f'{d["practica_base"]} BASE + {d["practica"] - d["practica_base"]} REFUERZO'
        L.append(f'| [{i} {d["titulo"]}](../02_TEORIA/{c["archivo"]}) | {c["tipo"]} | {donde} | {d["lectura"]} | {practica} | {cuando} |')
    for i, p in ctx.lecciones['puente'].items():
        L.append(f'| [Cap. 19 {p["seccion"]} · {p["titulo"]}](../02_TEORIA/{PUENTE_ARCHIVO}) | NÚCLEO | D{p["dia"]:02} | {p["min"]} | 0 | |')
    # prerrequisitos
    L += ['', '## Revisión de prerrequisitos de las lecciones NÚCLEO', '',
          'Cada lección declara sus prerrequisitos. Estado: **núcleo** = lección NÚCLEO en un día anterior o el mismo; **práctica** = lo cubre un ejercicio '
          'OBLIGATORIO anterior; **recomendada** = lectura REFUERZO que conviene hacer si el concepto no está claro (no es obligatoria).', '',
          '| Lección NÚCLEO | Día | Prerrequisito | Estado |', '|---|---|---|---|']
    for i, c in sorted(lec.items(), key=lambda kv: (kv[1].get('dia') or 99, kv[0])):
        if c['tipo'] != 'NÚCLEO':
            continue
        for p in prerrequisitos(ctx, i):
            L.append(f'| {i} | D{c["dia"]:02} | {p} | {estado_prerreq(ctx, i, p)} |')
    L.append('')
    # entrada a cada jornada
    L += ['## Qué se exige al entrar a cada jornada', '',
          'Distingue lo que ya debes poder hacer al empezar (viene de una jornada ANTERIOR: una lección NÚCLEO leída o un ejercicio OBLIGATORIO resuelto) '
          'de lo que se aprende durante la jornada. Un requisito no queda demostrado porque su nombre aparezca en un ejercicio del mismo día. '
          'Si un punto no se cumple, se hace el REFUERZO de la jornada indicada antes del OBLIGATORIO de hoy.', '',
          '| Día | Se exige al entrar | Viene de |', '|---:|---|---|']
    for n, s in sorted(ctx.nucleo['dias'].items(), key=lambda kv: int(kv[0])):
        for e in s.get('entra') or []:
            fuentes = ', '.join(fuente_entrada(ctx, p) for p in e.get('por') or []) or 'requisito externo (si falta, queda PENDIENTE)'
            L.append(f'| D{int(n):02} | {e["texto"]} | {fuentes} |')
    L.append('')
    # modo REDUCIDO
    L += ['## Modo REDUCIDO de cada jornada', '',
          'Cada jornada define una entrega menor y realizable con la preparación que necesita, no el mismo ejercicio con menos minutos. '
          'Lo que queda fuera pasa a REFUERZO y no se suma a otro día. El modo REDUCIDO mantiene la continuidad pero no cumple puertas ni acredita lo omitido; '
          'el modo MÍNIMO (20 min) rehace algo ya resuelto y tampoco acredita nada nuevo.', '',
          '| Día | Plan | Lectura mínima | Entrega reducida | Min. (lectura + entrega + cierre) | Pasa a REFUERZO |', '|---:|---:|---|---|---:|---|']
    for n, s in sorted(ctx.nucleo['dias'].items(), key=lambda kv: int(kv[0])):
        cal = next(d for d in ctx.calendario if d['dia'] == int(n))
        ex = any(norm(x)['id'].startswith('EXAMEN:') for x in s['obligatorio'])
        lecs = s.get('reducido_lecciones') or []
        Lm = lectura_ids(ctx, lecs)
        total = Lm + s['reducido_min'] + (0 if ex else 5)
        reducidos = {norm(y)['id'] for y in s['reducido']}
        pend = ', '.join(nombre_corto(ctx, x) for x in s['obligatorio'] if norm(x)['id'] not in reducidos and norm(x).get('est') != 0) or '—'
        L.append(f'| D{int(n):02} | {cal["reducido"]} | {", ".join(lecs) + f" ({Lm} min)" if lecs else "—"} | {s["reducido_entrega"]} | {total} | {pend} |')
    L.append('')
    # SQL por semana
    L += ['## SQL por semana: exigible, dentro de un examen o proyecto, y repaso opcional', '',
          'La práctica de SQL debe ser frecuente y progresiva, no una obligación diaria artificial. Cuenta como **exigible** un ejercicio SQL OBLIGATORIO o REPASO; '
          'como **integrada** la que forma parte de un examen o de un proyecto con cuadre SQL (ETL-6, C06-4); el **repaso opcional** nunca suma a la carga.', '',
          '| Semana | Jornadas con SQL exigible | Jornadas con SQL integrado en examen o proyecto | Jornadas con repaso SQL opcional | Jornadas sin SQL (Python, ETL, BI) |',
          '|---:|---|---|---|---|']
    por_semana = {}
    for d in ctx.calendario:
        if d['completo'] == 0:
            continue
        w = d['semana']
        x = por_semana.setdefault(w, {'exig': [], 'integ': [], 'opc': [], 'sin': []})
        s = ctx.nucleo['dias'].get(str(d['dia']))
        etq = f'D{d["dia"]:02}'
        if s is None:
            x['exig'].append(etq)
            continue
        items = [norm(y) for y in s['obligatorio'] + s['repaso']]
        exigible = any(tipo(y['id']) == 'SQL' and y.get('est') != 0 for y in items)
        integrado = any(y['id'].startswith('EXAMEN:') or ctx.nucleo['items_personalizados'].get(y['id'], {}).get('sql') or
                        (tipo(y['id']) == 'SQL' and y.get('est') == 0) for y in items)
        if exigible:
            x['exig'].append(etq)
        if integrado:
            x['integ'].append(etq)
        if s.get('sql_opcional'):
            x['opc'].append(etq)
        if not exigible and not integrado:
            x['sin'].append(etq)
    for w, x in sorted(por_semana.items()):
        L.append(f'| {w} | {", ".join(x["exig"]) or "—"} | {", ".join(x["integ"]) or "—"} | {", ".join(x["opc"]) or "—"} | {", ".join(x["sin"]) or "—"} |')
    L.append('')
    # evaluación final
    ef = ctx.nucleo['evaluacion_final']
    L += ['## Evaluación final: bloque posterior a las 42 jornadas', '',
          f'No forma parte de las seis semanas ni de las 90 horas. Son {horas(ef["total_min"])} h netas estimadas ({ef["ventana"]}), antes {horas(ef["total_previo_min"])} h. '
          'Detalle y sustituciones en `CARGA_ESTIMADA.md` y en `09_EVALUACION_FINAL/ENUNCIADO.md`.', '']
    L += tabla_evaluacion_final(ctx)
    L.append('')
    # 42 jornadas
    L += ['## Las 42 jornadas', '',
          '| Día | Fecha | Jornada | Plan | Lecciones NÚCLEO | Criterio / hito | Ejercicios OBLIGATORIOS | Estimado | Puerta |',
          '|---:|---|---|---:|---|---|---|---:|---|']
    for f in filas:
        if f['completo'] == 0:
            L.append(f'| D{f["dia"]:02} | {f["fecha"]} | Domingo flexible: descanso o recuperación voluntaria ({DOMINGO_MIN[0]}–{DOMINGO_MIN[1]} min) | 0 | — | — | — | 0 | |')
            continue
        lecs = ', '.join(f['lecciones']) if f['lecciones'] else '—'
        obl = ', '.join(f['obl']) if f['obl'] else '—'
        L.append(f'| D{f["dia"]:02} | {f["fecha"]} | {f["titulo"]} | {f["completo"]} | {lecs} ({f["L"]} min) | {f["criterio"] or "—"} | {obl} | {f["estimado"]} | {f["puerta"] or ""} |')
    L.append('')
    (ctx.raiz / '01_PLAN_DIARIO' / 'RUTAS.md').write_text('\n'.join(L), encoding='utf-8')


def dia_ejercicio(ctx, ej):
    """Día en que un ejercicio es OBLIGATORIO o REPASO por primera vez (D01 y D02 según el calendario original)."""
    for d in ctx.calendario:
        if d['dia'] in PROTEGIDOS:
            inicial = ctx.nucleo.get('dias_iniciales', {}).get(str(d['dia']))
            ids = inicial['obligatorio'] if inicial else d.get('sql', []) + d.get('python', []) + d.get('estadistica', []) + d.get('otros', [])
            if ej in ids:
                return d['dia']
    for n in sorted(int(k) for k in ctx.nucleo['dias']):
        s = ctx.nucleo['dias'][str(n)]
        if ej in [norm(x)['id'] for x in s['obligatorio'] + s['repaso']]:
            return n
    return None


def estado_prerreq(ctx, leccion, pre):
    c = ctx.lecciones['lecciones'][leccion]
    p = ctx.lecciones['lecciones'].get(pre)
    if p and p['tipo'] == 'NÚCLEO' and p['dia'] <= c['dia']:
        return 'núcleo'
    cob = (p or {}).get('cobertura') or {}
    if cob.get('por'):
        ok = []
        for ej in cob['por']:
            if ej in ctx.lecciones['puente']:
                ok.append(ctx.lecciones['puente'][ej]['dia'] <= c['dia'])
            else:
                dia = dia_ejercicio(ctx, ej)
                ok.append(dia is not None and dia <= c['dia'])
        if all(ok):
            return 'práctica: ' + ', '.join(cob['por'])
        return 'FALTA (' + ', '.join(cob['por']) + ' llega después)'
    if cob.get('recomendada'):
        return 'recomendada (' + cob['nota'] + ')'
    return 'FALTA'


def validar_referencias(ctx):
    errores = []
    for dia, s in ctx.nucleo['dias'].items():
        if int(dia) in PROTEGIDOS:
            errores.append(f'D{dia}: protegido, no debe estar en nucleo.json')
        for cat in ('obligatorio', 'repaso', 'refuerzo', 'opcional', 'reducido'):
            for x in s[cat]:
                i = norm(x)['id']
                t = tipo(i)
                if t == 'EXAMEN':
                    ok = (ctx.ejercicios / 'EXAMENES' / f'{i.split(":")[1]}.md').exists()
                elif t == 'CUSTOM':
                    ok = i in ctx.nucleo['items_personalizados']
                else:
                    ok = (ctx.ejercicios / ruta_ejercicio(i)).exists()
                if not ok:
                    errores.append(f'D{dia}/{cat}: no existe {i}')
        if not s['obligatorio']:
            errores.append(f'D{dia}: sin OBLIGATORIO')
        if not (set(norm(x)['id'] for x in s['reducido']) <= set(norm(x)['id'] for x in s['obligatorio'])):
            errores.append(f'D{dia}: reducido debe ser subconjunto de obligatorio')
        for i in s.get('lecciones') or []:
            if i not in ctx.lecciones['lecciones'] and i not in ctx.lecciones['puente']:
                errores.append(f'D{dia}: lección inexistente {i}')
            elif info_leccion(ctx, i)['dia'] != int(dia):
                errores.append(f'D{dia}: {i} está asignada al día {info_leccion(ctx, i)["dia"]} en lecciones.json')
        c = s.get('criterio')
        if c:
            carpeta = 'Analitico' if c['id'].startswith('AN') else 'Comprension'
            if not (ctx.ejercicios / carpeta / f'{c["id"]}.md').exists():
                errores.append(f'D{dia}: falta la actividad {c["id"]}')
        n = int(dia)
        cal = next(d for d in ctx.calendario if d['dia'] == n)
        examen = any(norm(x)['id'].startswith('EXAMEN:') for x in s['obligatorio'])
        # lo que se exige al entrar debe haber sido demostrado en una jornada anterior (no en la misma)
        if not s.get('entra'):
            errores.append(f'D{dia}: falta «entra» (qué se exige al entrar a la jornada)')
        for e in s.get('entra') or []:
            if not e.get('texto'):
                errores.append(f'D{dia}: un punto de «entra» sin texto')
            if not e.get('por') and not e.get('externo'):
                errores.append(f'D{dia}: «entra» sin fuente: {e.get("texto", "")[:60]}')
            for p in e.get('por') or []:
                dd = dia_entrada(ctx, p)
                if dd is None:
                    errores.append(f'D{dia}: «entra» cita {p}, que no es un OBLIGATORIO/REPASO ni una lección NÚCLEO')
                elif dd >= n:
                    errores.append(f'D{dia}: «entra» cita {p} (D{dd:02}), que no es anterior a la jornada')
        # modo REDUCIDO: una entrega menor y realizable, con la preparación que necesita
        for k in ('reducido_lecciones', 'reducido_min', 'reducido_entrega'):
            if k not in s:
                errores.append(f'D{dia}: falta «{k}»')
        if all(k in s for k in ('reducido_lecciones', 'reducido_min', 'reducido_entrega')):
            rl = s['reducido_lecciones']
            if not set(rl) <= set(s.get('lecciones') or []):
                errores.append(f'D{dia}: reducido_lecciones debe ser un subconjunto de las lecciones del día')
            total = lectura_ids(ctx, rl) + s['reducido_min'] + (0 if examen else 5)
            if total > cal['reducido'] + 10:
                errores.append(f'D{dia}: el modo REDUCIDO suma {total} min y el plan es {cal["reducido"]} (+10 de margen)')
            for x in s['reducido']:
                i = norm(x)['id']
                for c2 in citas_lecciones(ctx, i):
                    L = ctx.lecciones['lecciones'][c2]
                    if L['tipo'] == 'NÚCLEO' and L['dia'] == n and c2 not in rl:
                        errores.append(f'D{dia}: REDUCIDO conserva {i}, que cita la lección {c2} (NÚCLEO de hoy), y la omite')
        # un ejercicio no puede citar una lección que se enseña después
        for cat in ('obligatorio', 'repaso', 'refuerzo', 'opcional'):
            for x in s[cat]:
                i = norm(x)['id']
                for c2 in citas_lecciones(ctx, i, completo=True):
                    L = ctx.lecciones['lecciones'][c2]
                    if L['tipo'] == 'NÚCLEO' and L['dia'] > n:
                        errores.append(f'D{dia}/{cat}: {i} cita la lección {c2}, que se enseña en D{L["dia"]:02} (después)')
                if cat in ('obligatorio', 'repaso'):
                    for c2 in citas_lecciones(ctx, i):
                        if ctx.lecciones['lecciones'][c2]['tipo'] != 'NÚCLEO':
                            errores.append(f'D{dia}: {i} (OBLIGATORIO) cita la lección {c2}, que no es NÚCLEO')
    ef = ctx.nucleo.get('evaluacion_final')
    if not ef:
        errores.append('falta «evaluacion_final» en nucleo.json')
    else:
        if sum(b['min'] for b in ef['bloques']) != ef['total_min']:
            errores.append('evaluacion_final: los bloques no suman total_min')
        if sum(b['min_previo'] for b in ef['bloques']) != ef['total_previo_min']:
            errores.append('evaluacion_final: los minutos previos no suman total_previo_min')
    for i, c in ctx.lecciones['lecciones'].items():
        if c['tipo'] == 'NÚCLEO':
            s = ctx.nucleo['dias'].get(str(c['dia']))
            if c['dia'] in PROTEGIDOS:
                continue
            if not s or i not in (s.get('lecciones') or []):
                errores.append(f'{i}: NÚCLEO del día {c["dia"]} pero la jornada no la lista')
    return errores


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--raiz', default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--comprobar', action='store_true')
    args = ap.parse_args()
    ctx = Contexto(args.raiz)
    errores = validar_referencias(ctx)
    if errores:
        print('ERRORES:\n  ' + '\n  '.join(errores))
        raise SystemExit(1)
    filas = tabla_carga(ctx)
    print('Día  Plan  Estimado  Razón')
    for n, f, t, o, e, r in filas:
        print(f'D{n:02}  {o:4}  {e:8}  {r:.2f}  {t}')
    if args.comprobar:
        return
    for d in ctx.calendario:
        n = d['dia']
        if n in PROTEGIDOS or str(n) not in ctx.nucleo['dias']:
            continue
        aplicar_guia(ctx, n, ctx.nucleo['dias'][str(n)], d)
    aplicar_d02(ctx)
    for d in ctx.calendario:
        if d['completo'] == 0:
            aplicar_domingo(ctx, d['dia'], d)
    actualizar_calendario(ctx)
    actualizar_plan(ctx)
    actualizar_indices_teoria(ctx)
    ctx.calendario = json.loads((ctx.raiz / '01_PLAN_DIARIO' / 'calendario.json').read_text(encoding='utf-8'))
    escribir_carga(ctx)
    escribir_rutas(ctx)
    print('OK: guías, calendario.json/csv, CARGA_ESTIMADA.md y RUTAS.md actualizados.')


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
