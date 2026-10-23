"""Integridad de la corrección V5. No ejecuta soluciones ni acredita al estudiante.

Sin --dias revisa duplicados D04-D42; --dias limita la muestra de trabajo.
La protección de archivos fuera de muestra se comprueba siempre.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUESTRA = {4, 5, 8, 9, 10, 11, 12, 13}
PROTEGIDOS = {1, 2, 3}
EXAMENES = {6, 13, 20, 27, 34, 41}
PREFIJOS_INMUTABLES = (
    'mi_trabajo/', '04_DATASETS/', '03_EJERCICIOS/', '05_PROYECTOS/',
    '06_ENTREVISTAS/', '07_LINKEDIN_EMPLEO/', '08_SOLUCIONES/',
    '09_EVALUACION_FINAL/',
)
CORRECTORES = {
    'herramientas/contratos_python.py', 'herramientas/corregir_sql.py',
    'herramientas/corregir_python.py', 'herramientas/corregir_mini_etl.py',
    'herramientas/corregir_depuracion.py', 'herramientas/controles_examenes.py',
    'herramientas/validar_etl_distribuidora.py', 'herramientas/validar_final.py',
    '03_EJERCICIOS/SQL/CONTRATOS.md',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cargar(path):
    return json.loads(path.read_text(encoding='utf-8'))


def texto_vigente(texto):
    """Ignora código y comentarios: sus casillas no son tareas ejecutables."""
    fence = None
    comment = False
    for numero, linea in enumerate(texto.splitlines(), 1):
        if comment:
            if '-->' in linea:
                comment = False
            continue
        if '<!--' in linea and '-->' not in linea:
            comment = True
            continue
        m = re.match(r'^\s*(`{3,}|~{3,})', linea)
        if m:
            if fence is None:
                fence = m[1][0]
            elif fence == m[1][0]:
                fence = None
            continue
        if fence is None:
            yield numero, linea


def id_actividad(linea):
    m = re.search(r'<!--\s*actividad:([^>]+?)\s*-->', linea)
    if m:
        return m[1].strip()
    m = re.search(r'\]\([^)]*03_EJERCICIOS/([^)/]+)/([^)/#]+)(?:#[^)]*)?\)', linea)
    if m:
        ident = Path(m[2]).stem
        return 'EXAMEN:' + ident if m[1] == 'EXAMENES' else ident
    m = re.search(r'\[([0-9]+\.[0-9]+)\s', linea)
    if m:
        return 'L:' + m[1]
    return None


def actividades(texto):
    out = []
    for numero, linea in texto_vigente(texto):
        m = re.match(r'^\s*- \[([ xX])\]\s+', linea)
        if m:
            ident = id_actividad(linea)
            if ident:
                out.append({'id': ident, 'completada': m[1].lower() == 'x',
                            'linea': numero, 'texto': linea})
    return out


def duplicados(texto):
    grupos = collections.defaultdict(list)
    for a in actividades(texto):
        grupos[a['id']].append(a['linea'])
    return {k: v for k, v in grupos.items() if len(v) > 1}


def guia(raiz, dia):
    return next((raiz / '01_PLAN_DIARIO/dias').glob(f'D{dia:02}_*.md'))


def seccion(texto, titulo):
    patron = r'^## ' + re.escape(titulo) + r'\s*\n(.*?)(?=^## |\Z)'
    m = re.search(patron, texto, re.M | re.S)
    return m[1].strip() if m else None


def filas_empleo(texto):
    return [linea.strip() for linea in texto.splitlines()
            if re.match(r'^\|(?:Empleo(?:/UAGRM)?|Postulaci[oó]n(?:es)?|LinkedIn|CV)\|', linea)]


def norm(item):
    return item['id'] if isinstance(item, dict) else item


def verificar(raiz, dias):
    errores = []
    checks = []
    def check(nombre, condicion, detalle=None):
        checks.append({'prueba': nombre, 'estado': 'OK' if condicion else 'ERROR', 'detalle': detalle})
        if not condicion:
            errores.append(nombre)

    proteccion = cargar(raiz / 'docs/auditorias/PROTECCION_BASE_8168909.json')
    backup = Path(proteccion['backup'])
    base = backup / 'repositorio'
    check('manifiesto externo existente', (backup / 'MANIFIESTO_SHA256.json').is_file())
    if (backup / 'MANIFIESTO_SHA256.json').is_file():
        check('hash manifiesto externo', sha(backup / 'MANIFIESTO_SHA256.json') == proteccion['backup_manifest_sha256'])
    alterados = []
    for rel, valor in proteccion['archivos'].items():
        protegido = rel.startswith(PREFIJOS_INMUTABLES) or rel in CORRECTORES
        m = re.match(r'01_PLAN_DIARIO/dias/D(\d\d)_', rel)
        if m and int(m[1]) not in MUESTRA:
            protegido = True
        if protegido and (not (raiz / rel).is_file() or sha(raiz / rel) != valor):
            alterados.append(rel)
    check('archivos personales, contratos, empleo, exámenes y jornadas fuera de muestra intactos', not alterados, alterados)

    expected = collections.Counter()
    for item in proteccion['casillas_completadas']:
        ident = id_actividad(item['texto'])
        if ident:
            expected[(item['archivo'], ident)] += 1
    actual = collections.Counter()
    for p in sorted((raiz / '01_PLAN_DIARIO/dias').glob('*.md')):
        rel = p.relative_to(raiz).as_posix()
        for a in actividades(p.read_text(encoding='utf-8')):
            if a['completada']:
                actual[(rel, a['id'])] += 1
    perdidas = [list(k) for k, v in expected.items() if actual[k] < v]
    nuevas = [list(k) for k, v in actual.items() if v > expected[k]]
    check('realizaciones identificables conservadas', not perdidas, perdidas)
    check('ninguna actividad nueva acreditada', not nuevas, nuevas)
    # También preserva las marcas genéricas de cierre en D01/D02 mediante hash literal.
    total = sum(len(re.findall(r'^\s*- \[[xX]\]', p.read_text(encoding='utf-8'), re.M))
                for p in (raiz / '01_PLAN_DIARIO/dias').glob('*.md'))
    check('34 casillas completadas originales, sin duplicar ni acreditar', total == 34, {'esperadas': 34, 'actuales': total})
    check('cinco casillas vigentes completadas D04', len([a for a in actividades(guia(raiz, 4).read_text(encoding='utf-8')) if a['completada']]) == 5)

    for d in sorted(dias - PROTEGIDOS):
        texto = guia(raiz, d).read_text(encoding='utf-8')
        du = duplicados(texto)
        check(f'D{d:02}: cero IDs accionables duplicados', not du, du)
    for d in sorted(MUESTRA):
        viejo = guia(base, d).read_text(encoding='utf-8')
        nuevo = guia(raiz, d).read_text(encoding='utf-8')
        check(f'D{d:02}: bloque de empleabilidad íntegro', seccion(viejo, 'Empleo y clase') == seccion(nuevo, 'Empleo y clase'))
        # El formato editorial puede cambiar; se preservan nombre, minutos y acción de cada bloque.
        faltantes = [fila for fila in filas_empleo(viejo) if fila not in nuevo]
        check(f'D{d:02}: filas y minutos de empleo íntegros', not faltantes, faltantes)

    fuente = cargar(raiz / '01_PLAN_DIARIO/nucleo.json')
    original = cargar(base / '01_PLAN_DIARIO/nucleo.json')
    current_ob = {norm(x) for s in list(fuente['dias'].values()) + list(fuente.get('dias_iniciales', {}).values()) for x in s.get('obligatorio', [])}
    old_ob = {norm(x) for s in list(original['dias'].values()) + list(original.get('dias_iniciales', {}).values()) for x in s.get('obligatorio', [])}
    check('obligaciones BASE 8168909 conservadas en fuentes', not (old_ob - current_ob), sorted(old_ob - current_ob))
    historial_acreditado = {ident for (_, ident) in expected}
    deuda_historica = set(proteccion['obligatorios_historicos_reclasificados']) - current_ob - historial_acreditado
    check('obligaciones históricas restituidas o acreditadas previamente', not deuda_historica, sorted(deuda_historica))
    posiciones = {}
    for ndia, ficha in fuente['dias'].items():
        for indice, actividad in enumerate(ficha.get('ruta_integral', [])):
            posiciones[actividad['id']] = (int(ndia), indice, actividad)
    for d in sorted(MUESTRA):
        s = fuente['dias'][str(d)]
        ruta = s.get('ruta_integral', [])
        if d == 13:
            check('D13: modo editorial sin ruta obligatoria nueva', s.get('modo_integral') == 'editorial' and not ruta)
            texto = guia(raiz, d).read_text(encoding='utf-8')
            esperado = {norm(x) for cat in ('obligatorio', 'repaso', 'refuerzo', 'opcional', 'extendida') for x in s.get(cat, [])}
            if s.get('criterio'):
                esperado.add(s['criterio']['id'])
            actual_ejercicios = {a['id'] for a in actividades(texto) if not a['id'].startswith(('L:', 'MP-'))}
            check('D13: ejercicios vigentes coinciden con fuente editorial', esperado == actual_ejercicios, {'fuente': sorted(esperado), 'guia': sorted(actual_ejercicios)})
            distribucion = seccion(texto, 'Distribución neta') or ''
            minutos_tabla = sum(int(m[1]) for m in re.finditer(r'^\|[^|]+\|(\d+)\|', distribucion, re.M))
            marca = re.search(r'<!--\s*base_min:(\d+)\s*-->', texto)
            cabecera = re.search(r'COMPLETO (\d+) min', texto)
            check('D13: encabezado y tabla iguales sin recortar examen', minutos_tabla == 175 and marca is not None and int(marca[1]) == minutos_tabla and cabecera is not None and int(cabecera[1]) == minutos_tabla)
            sesiones = seccion(texto, 'Sesiones retomables') or seccion(texto, 'Sesiones retomables y minutos') or ''
            min_sesiones = sum(int(m[1]) for m in re.finditer(r'^\|[^|]+\|\s*(\d+)\s*\|', sesiones, re.M))
            check('D13: sesiones del examen original y empleo suman 175', min_sesiones == 175, min_sesiones)
            continue
        check(f'D{d:02}: fuente con secuencia de actividades', bool(ruta))
        ids = [a['id'] for a in ruta]
        check(f'D{d:02}: IDs únicos en fuente', len(ids) == len(set(ids)))
        sesiones = s.get('sesiones_integrales', [])
        programadas = [i for ses in sesiones for i in ses['actividades']]
        requeridas = [a['id'] for a in ruta if a['tipo'] not in {'refuerzo', 'extendida'} and a.get('estado_acreditacion') != 'historico']
        check(f'D{d:02}: sesiones cubren BASE una vez y en orden', programadas == requeridas, {'sesiones': programadas, 'base': requeridas})
        texto = guia(raiz, d).read_text(encoding='utf-8')
        render_ids = [a['id'] for a in actividades(texto)]
        orden_render = [a['id'] for a in ruta if a['tipo'] not in {'refuerzo', 'extendida'} or a.get('estado_acreditacion') == 'historico']
        orden_render += [a['id'] for tipo in ('refuerzo', 'extendida') for a in ruta if a['tipo'] == tipo and a.get('estado_acreditacion') != 'historico']
        check(f'D{d:02}: cada actividad fuente aparece una vez y en orden en guía', render_ids == orden_render, {'fuente': orden_render, 'guia': render_ids})
        for pos, a in enumerate(ruta):
            check(f'D{d:02}/{a["id"]}: minutos no negativos', isinstance(a['minutos'], (int, float)) and a['minutos'] >= 0)
            for dep in a.get('prerrequisitos', []):
                if isinstance(dep, str) and dep in ids:
                    check(f'D{d:02}/{a["id"]}: {dep} anterior', ids.index(dep) < pos)
                if dep in posiciones and a['tipo'] not in {'refuerzo', 'extendida'}:
                    dep_dia, dep_pos, dep_actividad = posiciones[dep]
                    check(f'D{d:02}/{a["id"]}: {dep} preparación obligatoria anterior',
                          (dep_dia, dep_pos) < (d, pos) and dep_actividad['tipo'] not in {'refuerzo', 'extendida'},
                          {'dia': dep_dia, 'orden': dep_pos, 'tipo': dep_actividad['tipo']})
            if a.get('ruta'):
                url = a['ruta']
                destino, _, ancla = url.partition('#')
                archivo = raiz / destino
                check(f'D{d:02}/{a["id"]}: enlace interno existente', archivo.is_file())
                if ancla and archivo.is_file():
                    contenido = archivo.read_text(encoding='utf-8')
                    titulos = re.findall(r'^#+\s+(.+)', contenido, re.M)
                    slugs = {re.sub(r'[^\w\s-]', '', t.lower()).strip().replace(' ', '-') for t in titulos}
                    check(f'D{d:02}/{a["id"]}: ancla interna existente', ancla in slugs or f'id="{ancla}"' in contenido, ancla)
            if a.get('estado_acreditacion') == 'historico':
                evidencias = a.get('evidencia', [])
                check(f'D{d:02}/{a["id"]}: evidencia conservada visible en guía', bool(evidencias) and all(e['ruta'] in texto and (raiz / e['ruta']).is_file() for e in evidencias))
            if a['tipo'] == 'nucleo' and not a.get('estado_acreditacion') == 'historico':
                url = a.get('ruta', '').split('#')[0]
                micros = [j for j, otra in enumerate(ruta) if otra['tipo'] == 'micropractica' and otra.get('ruta', '').split('#')[0] == url]
                equivalentes = a.get('equivalente_micro', [])
                equivalentes_validos = [j for j, otra in enumerate(ruta) if otra['id'] in equivalentes and otra['tipo'] in {'obligatorio', 'micropractica'} and otra['minutos'] > 0]
                check(f'D{d:02}/{a["id"]}: micropráctica esencial posterior', any(j > pos for j in micros + equivalentes_validos), {'micro': micros, 'equivalente_explicitado': equivalentes_validos})
        calendario_base = cargar(base / '01_PLAN_DIARIO/calendario.json')
        cal_dia = next(c for c in calendario_base if c['dia'] == d)
        pool = {'SQL', 'Teoría', 'Teoría/retro', 'Práctica', 'Lecciones', 'Criterio'}
        fijos = sum(m for nombre, m in cal_dia['bloques'] if nombre.strip() not in pool and not nombre.strip().startswith('Examen'))
        base_min = sum(a['minutos'] for a in ruta if a['tipo'] not in {'refuerzo', 'extendida'}) + fijos
        # Los metadatos constituyen contrato de salida, sin depender de redondeos editoriales.
        marca = re.search(r'<!--\s*base_min:(\d+)\s*-->', texto)
        check(f'D{d:02}: minutos BASE calculados desde actividades', marca is not None and int(marca[1]) == base_min, {'fuente_min': base_min, 'marca_min': int(marca[1]) if marca else None})
        cabecera = re.search(r'\*\*BASE(?: pendiente)? estimado:\s*(\d+) min', texto)
        check(f'D{d:02}: encabezado visible suma BASE', cabecera is not None and int(cabecera[1]) == base_min)
        tabla = seccion(texto, 'Distribución neta') or ''
        total_tabla = sum(int(m[1]) for m in re.finditer(r'^\|[^|]+\|(\d+)\|', tabla, re.M))
        check(f'D{d:02}: distribución por categorías suma BASE', total_tabla == base_min, total_tabla)
        tabla_sesiones = seccion(texto, 'Sesiones retomables y minutos') or ''
        tramos = [int(m[1]) for m in re.finditer(r'^\|[^|]+\|[^|]+\|\s*(\d+)\s*\|', tabla_sesiones, re.M)]
        check(f'D{d:02}: sesiones retomables suman BASE y tramos hasta 75 min', sum(tramos) == base_min and all(0 < m <= 75 for m in tramos), tramos)

    return {'base': proteccion['base_head'], 'dias_duplicados_revisados': sorted(dias - PROTEGIDOS),
            'exclusion_explicita': sorted(PROTEGIDOS), 'fallos': len(errores),
            'pruebas': checks, 'limites': ['Revisión semántica y suficiencia documentadas aparte; estas aserciones no certifican dominio.',
                                         'Fuera de muestra sigue pendiente regeneración aprobada.',
                                         'No acredita ejecución manual de Excel o Power BI.']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--raiz', type=Path, default=ROOT)
    ap.add_argument('--dias', help='Lista coma; por defecto todos D04-D42')
    ap.add_argument('--salida', type=Path)
    args = ap.parse_args()
    dias = {int(x) for x in args.dias.split(',')} if args.dias else set(range(4, 43))
    if not dias <= set(range(1, 43)):
        ap.error('Días fuera de D01-D42')
    result = verificar(args.raiz, dias)
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'fallos': result['fallos'], 'pruebas': len(result['pruebas']), 'errores': [p for p in result['pruebas'] if p['estado'] == 'ERROR']}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['fallos']))


if __name__ == '__main__':
    main()
