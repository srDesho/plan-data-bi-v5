"""Aplica 01_PLAN_DIARIO/nucleo.json a las guías diarias y al calendario (idempotente).

Cada jornada queda con ejercicios OBLIGATORIO / REPASO / REFUERZO / OPCIONAL, su prerrequisito y, si corresponde,
su puerta de competencia. No toca D01 ni D02. Los minutos de cada jornada (900 por semana) no cambian.

Uso desde la raíz:
    python herramientas/aplicar_nucleo.py              # escribe guías, PLAN_V5.md (títulos), calendario.json/csv y CARGA_ESTIMADA.md
    python herramientas/aplicar_nucleo.py --comprobar  # solo valida referencias y muestra la estimación
    python herramientas/aplicar_nucleo.py --raiz RUTA  # trabaja sobre una copia del paquete
"""
from pathlib import Path
import argparse
import csv
import json
import re
import sys

PROTEGIDOS = {1, 2}                       # D01 y D02 no se modifican
MULT = {('SQL', 1): 1.5, ('SQL', 2): 1.75, ('SQL', 3): 2.25, ('PY', 1): 2.0, ('PY', 2): 2.5, ('PY', 3): 3.25,
        ('ST', 1): 2.0, ('ST', 2): 2.0, ('ST', 3): 2.5}
CASO_MIN = {'C01': 30, 'C02': 25, 'C03': 35, 'C04': 40, 'C05': 45}
PRACTICA = re.compile(r'^\|(Práctica|Examen y corrección)\|(\d+)\|[^|\n]*\|$', re.M)
ACCION = 'Resolver los OBLIGATORIOS; REFUERZO solo si la puerta no se cumplió; OPCIONAL no desplaza lo obligatorio.'
SECCIONES_TEORIA = {8: {'19_Puente_Python_a_ETL': '§1–2'}, 22: {'19_Puente_Python_a_ETL': '§3'}, 23: {'19_Puente_Python_a_ETL': '§3'},
                    24: {'19_Puente_Python_a_ETL': '§4'}}


class Contexto:
    def __init__(self, raiz):
        self.raiz = Path(raiz)
        self.nucleo = json.loads((self.raiz / '01_PLAN_DIARIO' / 'nucleo.json').read_text(encoding='utf-8'))
        self.calendario = json.loads((self.raiz / '01_PLAN_DIARIO' / 'calendario.json').read_text(encoding='utf-8'))
        self.ejercicios = self.raiz / '03_EJERCICIOS'


def norm(item):
    return item if isinstance(item, dict) else {'id': item}


def tipo(i):
    if i.startswith('EXAMEN:'):
        return 'EXAMEN'
    if i in ('C06-0', 'C06-1', 'C06-2', 'C06-3', 'C06-4') or i.startswith('ETL-'):
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
    if d.get('prerreq'):
        lineas += [f'**Antes de empezar:** {d["prerreq"]} Si no se cumple, haz REFUERZO del día anterior en lugar del OBLIGATORIO de hoy.', '']
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
    return '\n'.join(lineas) + '\n'


def aplicar_guia(ctx, dia, d, nl='\n'):
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
    if d.get('teoria'):
        principal = d['teoria'][0]
        t = re.sub(r'^- \[ \] \[Teoría principal: [^\]]+\]\([^)]*\)\.', lambda m: f'- [ ] [Teoría principal: {principal}](../../02_TEORIA/{principal}.md).', t, count=1, flags=re.M)
        if len(d['teoria']) > 1:
            apoyo = d['teoria'][1]
            secc = SECCIONES_TEORIA.get(dia, {}).get(apoyo)
            sufijo = f': solo apartados que expliquen el objetivo{" (" + secc + ")" if secc else ""}.'
            t = re.sub(r'^- \[ \] \[Apoyo: [^\]]+\]\([^)]*\)[^\n]*', lambda m: f'- [ ] [Apoyo: {apoyo}](../../02_TEORIA/{apoyo}.md){sufijo}', t, count=1, flags=re.M)
    t = PRACTICA.sub(lambda m: f'|{m.group(1)}|{m.group(2)}|{ACCION}|', t, count=1)
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
    red = ', '.join(nombre_corto(ctx, x) for x in d['reducido'])
    nuevo = f'Haz solo: {red}. El resto del OBLIGATORIO pasa a REFUERZO y no se suma a otro día.'
    t = re.sub(r'(Resuelve una consulta y un ejercicio esencial\.|Haz solo: .*? El resto del OBLIGATORIO pasa a REFUERZO y no se suma a otro día\.)',
               lambda m: nuevo, t, count=1)
    ruta.write_bytes(t.replace('\n', nl).encode('utf-8'))


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
        if n in PROTEGIDOS or str(n) not in ctx.nucleo['dias']:
            continue
        s = ctx.nucleo['dias'][str(n)]
        todos = s['obligatorio'] + s['repaso'] + s['refuerzo'] + s['opcional']
        sql, py, st, otros = clasificar(todos)
        if s.get('titulo'):
            d['titulo'] = s['titulo']
        if s.get('objetivo'):
            d['objetivo'] = s['objetivo']
        if s.get('teoria'):
            d['teoria'] = s['teoria']
        if s.get('dataset'):
            d['dataset'] = s['dataset']
        d['sql'], d['python'], d['estadistica'], d['otros'] = list(dict.fromkeys(sql)), py, st, otros
        d['nucleo'] = {'obligatorio': [norm(x)['id'] for x in s['obligatorio']], 'repaso': s['repaso'],
                       'refuerzo': [norm(x)['id'] for x in s['refuerzo']], 'opcional': [norm(x)['id'] for x in s['opcional']],
                       'reducido': [norm(x)['id'] for x in s['reducido']], 'puerta': (s.get('puerta') or {}).get('id')}
    (ctx.raiz / '01_PLAN_DIARIO' / 'calendario.json').write_text(json.dumps(ctx.calendario, ensure_ascii=False, indent=2), encoding='utf-8')
    with (ctx.raiz / '01_PLAN_DIARIO' / 'calendario.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dia', 'fecha', 'semana', 'titulo', 'completo_min', 'reducido_min', 'minimo_min', 'sql', 'python', 'estadistica', 'otros', 'obligatorio'])
        for d in ctx.calendario:
            w.writerow([d['dia'], d['fecha'], d['semana'], d['titulo'], d['completo'], d['reducido'], d['minimo'], ';'.join(d['sql']),
                        ';'.join(d['python']), ';'.join(d['estadistica']), ';'.join(d['otros']), ';'.join(d.get('nucleo', {}).get('obligatorio', []))])


def actualizar_plan(ctx):
    """Sincroniza los títulos de las jornadas en PLAN_V5.md con nucleo.json."""
    p = ctx.raiz / '01_PLAN_DIARIO' / 'PLAN_V5.md'
    t = p.read_text(encoding='utf-8')
    for n, s in ctx.nucleo['dias'].items():
        if s.get('titulo'):
            patron = rf'(\*\*D{int(n):02} · [^\n]*?:\*\* \[)[^\]]+(\]\(dias/D{int(n):02}_)'
            t = re.sub(patron, lambda m: m.group(1) + s['titulo'] + m.group(2), t, count=1)
    p.write_text(t, encoding='utf-8')


def tabla_carga(ctx):
    filas = []
    for d in ctx.calendario:
        n = d['dia']
        if d['completo'] == 0 or str(n) not in ctx.nucleo['dias']:
            continue
        s = ctx.nucleo['dias'][str(n)]
        bl = {a.strip(): b for a, b in d['bloques']}
        sql_blk = bl.get('SQL', 0)
        practica_blk = next(v for k, v in bl.items() if k.startswith('Pr') or k.startswith('Examen'))
        fijo = d['completo'] - sql_blk - practica_blk
        obl = sum(estimar(ctx, x) for x in s['obligatorio']) + sum(estimar(ctx, x, repaso=True) for x in s['repaso'])
        if any(norm(x)['id'].startswith('EXAMEN') for x in s['obligatorio']):
            sql_ex = sum(estimar(ctx, x) for x in s['obligatorio'])
            total = fijo + practica_blk + max(sql_ex, sql_blk)     # el bloque del examen tiene tiempo fijo
        else:
            total = fijo + obl
        filas.append((n, d['fecha'], s.get('titulo') or d['titulo'], d['completo'], total, round(total / d['completo'], 2)))
    return filas


def escribir_carga(ctx, filas):
    por_semana = {}
    for n, _f, _t, orig, est, _r in filas:
        w = (n - 1) // 7 + 1
        a, b = por_semana.get(w, (0, 0))
        por_semana[w] = (a + orig, b + est)
    lineas = ['# Carga estimada de lo OBLIGATORIO por jornada', '',
              'Estimación con margen para una persona que todavía depende de ayuda externa. **No es una medición**: '
              'los multiplicadores (SQL ×1,5–2,25; Python ×2–3,25; estadística ×2–2,5; casos ×1,75; Excel/Power BI ×2; tareas de proyecto estimadas a mano) '
              'son supuestos con error razonable de ±35 %. Registra tus minutos reales en `mi_trabajo/progreso.csv` y corrige esta tabla con tus datos.', '',
              'Incluye teoría, empleo y cierre (sin cambios) más los ejercicios OBLIGATORIOS y REPASO. D01 y D02 conservan su diseño original y no figuran aquí. '
              'En días de examen, el bloque de examen, corrección y simulacro tiene tiempo fijo; solo el SQL de calentamiento puede exceder su bloque.', '',
              '| Día | Fecha | Contenido | Plan (min) | Estimado (min) | Razón |', '|---:|---|---|---:|---:|---:|']
    for n, f, t, o, e, r in filas:
        lineas.append(f'| D{n:02} | {f} | {t} | {o} | {e} | {r:.2f} |')
    lineas += ['', '| Semana | Plan (min) | Estimado, jornadas listadas (min) |', '|---:|---:|---:|']
    for w, (a, b) in sorted(por_semana.items()):
        lineas.append(f'| {w} | {a} | {b} |')
    lineas += ['', 'La semana 1 solo suma D03–D06 (D01 y D02 no se modifican). Una razón por encima de 1,2 significa jornada AJUSTADA: '
               'usa el modo REDUCIDO y mueve el REFUERZO; no alargues el día. El REFUERZO y el OPCIONAL no están incluidos.', '']
    (ctx.raiz / '01_PLAN_DIARIO' / 'CARGA_ESTIMADA.md').write_text('\n'.join(lineas), encoding='utf-8')


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
        for t in s.get('teoria') or []:
            if not (ctx.raiz / '02_TEORIA' / f'{t}.md').exists():
                errores.append(f'D{dia}: falta teoría {t}')
    return errores


def ejercicios_huerfanos(ctx):
    """Ejercicios que estaban en el calendario original y ya no aparecen en ninguna categoría."""
    original = json.loads((ctx.raiz / '01_PLAN_DIARIO' / 'calendario.json').read_text(encoding='utf-8'))
    vistos = set()
    for s in ctx.nucleo['dias'].values():
        for cat in ('obligatorio', 'repaso', 'refuerzo', 'opcional'):
            vistos |= {norm(x)['id'] for x in s[cat]}
    return vistos


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
        aplicar_guia(ctx, n, ctx.nucleo['dias'][str(n)])
    actualizar_calendario(ctx)
    actualizar_plan(ctx)
    escribir_carga(ctx, filas)
    print('OK: guías, calendario.json/csv y CARGA_ESTIMADA.md actualizados.')


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
