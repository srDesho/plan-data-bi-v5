"""Inventario pedagógico reproducible; no ejecuta ejercicios ni abre soluciones.

Compara un respaldo externo inmutable con las fuentes actuales. Por defecto es
solo lectura; --escribir crea exclusivamente los tres archivos INVENTARIO_*.
La clasificación histórica es evidencia adicional: nunca se sustituye por la
clasificación del HEAD cuando aquella impuso una obligación mayor.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

REVISIONES = ('78194fb', '559e612', '6ac1af8', 'a6b20f3', '4909893')
PLAN = '01_PLAN_DIARIO/'
SALIDAS = ('INVENTARIO_EJERCICIOS_ANTES_DESPUES.md',
           'INVENTARIO_EJERCICIOS_ANTES_DESPUES.json',
           'INVENTARIO_EJERCICIOS_ANTES_DESPUES.csv')
FAMILIAS = {'SQL': 'SQL', 'Python': 'Python/Pandas', 'Estadistica': 'Estadística',
            'Analitico': 'Criterio analítico', 'Comprension': 'Hito',
            'Depuracion': 'Depuración', 'Puente': 'Mini-ETL',
            'EXAMENES': 'Examen', 'Notebooks': 'Notebook guiado', 'Casos': 'Caso'}
LECCIONES_P = {
    'P01': ['7.2', '7.3', '7.4'], 'P02': ['7.3', '7.6', '7.10'],
    'P03': ['7.5'], 'P04': ['7.9'], 'P05': ['7.8', '7.9'],
    'P06': ['7.9', '7.11'], 'P07': ['7.10', '7.11', '7.12', '7.13'],
    'P08': ['7.10', '8.1'], 'P09': ['7.5', '7.7', '8.1', '8.5'],
    'P10': ['7.5', '8.4', '8.5'], 'P11': ['7.7', '8.5'],
    'P12': ['8.4'], 'P13': ['7.11', '8.3'], 'P14': ['8.4', '11.3'],
    'P15': ['7.9', '8.5'], 'P16': ['7.11', '7.13', '8.4'],
    'P17': ['9.2'], 'P18': ['9.4', '10.2'], 'P19': ['9.4', '9.6', '10.1'],
    'P20': ['10.1', '10.2'], 'P21': ['3.1', '10.3'], 'P22': ['9.5'],
    'P23': ['9.3', '9.5'], 'P24': ['9.6'], 'P25': ['9.6', '10.1', '10.2'],
    'P26': ['6.5', '10.1', '10.2'], 'P27': ['11.5', '9.4'],
    'P28': ['5.2', '10.3', '10.5'], 'P29': ['8.3'], 'P30': ['5.3', '8.5']}
CONCEPTOS = [
    (r'\bJOIN\b|\bmerge\b|cardinalidad', 'claves, cardinalidad y uniones', ['3.1', '3.2']),
    (r'LEFT JOIN|sin compra|no compraron|nunca tuvieron', 'ausencias y conservación de filas', ['3.3']),
    (r'GROUP BY|groupby|por ruta|por categoría|por tipo', 'agregación a la granularidad pedida', ['2.2']),
    (r'HAVING|filtra grupos', 'filtro de grupos frente a filas', ['2.2']),
    (r'subconsulta|\bCTE\b', 'resultados intermedios y consultas anidadas', ['4.1', '4.2']),
    (r'ventana|acumulad|ranking|\bLAG\b|ROW_NUMBER', 'ventanas, orden y empates', ['4.3']),
    (r'redonde|decimales|\bROUND\b', 'precisión y redondeo al presentar', ['2.4']),
    (r'fecha|recencia|por mes|mensual', 'formatos de fecha y corte reproducible', ['2.4', '4.4']),
    (r'porcentaje|denominador|promedio|ticket|drop size', 'numerador, denominador y grano', ['2.3']),
    (r'duplicad|conflicto|rechaz|reconcili|cuadre', 'calidad, rechazos y reconciliación', ['5.2', '5.3']),
    (r'CSV|archivo|JSON|ruta.*Path', 'archivos, rutas y serialización', ['8.3']),
    (r'ValueError|excepci|traceback', 'validación y errores explícitos', ['8.5', '8.6']),
    (r'hipótesis|Welch|chi.cuadrado|valor p|intervalo de confianza', 'inferencia y límites de interpretación', ['12.1']),
    (r'percentil|cuartil|atípico', 'distribución, cuantiles y atípicos', ['11.5', '11.6']),
    (r'media|mediana|moda', 'medidas de posición y observación', ['11.1', '11.3']),
    (r'Power BI|DAX|CALCULATE|medida', 'modelo y contexto de filtro BI', ['13.2', '14.1']),
    (r'Excel|tabla dinámica|BUSCAR|SUMAR.SI', 'tablas, fórmulas y conciliación Excel', ['15.1', '15.2', '15.3']),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def leer(root: Path, rel: str) -> str:
    path = (root / rel.split('#')[0]).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Ruta fuera del repositorio: {rel}')
    if '08_SOLUCIONES' in path.parts or 'mi_trabajo' in path.parts:
        raise ValueError('No se leen soluciones ni archivos personales')
    return path.read_text(encoding='utf-8-sig') if path.exists() else ''


def json_fuente(root: Path, nombre: str):
    return json.loads(leer(root, PLAN + nombre))


def normalizar(item):
    return item if isinstance(item, dict) else {'id': item}


def plan_asignaciones(root: Path):
    nucleo = json_fuente(root, 'nucleo.json')
    calendario = json_fuente(root, 'calendario.json')
    asignaciones = defaultdict(list)
    for cal in calendario:
        dia = int(cal['dia'])
        fuente = nucleo.get('dias_iniciales', {}).get(str(dia), {}) if dia <= 2 else nucleo.get('dias', {}).get(str(dia), {})
        if not fuente:
            fuente = cal.get('nucleo', {})
        for clase in ('obligatorio', 'repaso', 'refuerzo', 'opcional'):
            for item in fuente.get(clase, []):
                item = normalizar(item)
                asignaciones[item['id']].append({'dia': dia, 'clase': clase.upper(),
                    'fuente': f'{PLAN}nucleo.json', 'minutos_explicitos': item.get('est')})
        criterio = fuente.get('criterio')
        if criterio:
            asignaciones[criterio['id']].append({'dia': dia, 'clase': 'OBLIGATORIO (CRITERIO/HITO)',
                'fuente': PLAN + 'nucleo.json', 'minutos_explicitos': criterio.get('min')})
    return nucleo, asignaciones


def historia(backup: Path):
    registros = defaultdict(list)
    for revision in REVISIONES:
        comando = ['git', '-c', f'safe.directory={backup.as_posix()}', '-C', str(backup),
                   'show', f'{revision}:{PLAN}nucleo.json']
        resultado = subprocess.run(comando, capture_output=True, check=True, encoding='utf-8')
        datos = json.loads(resultado.stdout)
        for dia, fuente in datos.get('dias', {}).items():
            for item in fuente.get('obligatorio', []):
                item = normalizar(item)
                registros[item['id']].append({'commit': revision, 'dia': int(dia),
                    'clase': 'OBLIGATORIO', 'fuente': f'{revision}:{PLAN}nucleo.json'})
        for dia, fuente in datos.get('dias_iniciales', {}).items():
            for item in fuente.get('obligatorio', []):
                registros[normalizar(item)['id']].append({'commit': revision, 'dia': int(dia),
                    'clase': 'OBLIGATORIO', 'fuente': f'{revision}:{PLAN}nucleo.json'})
    return registros


def progreso_guias(root: Path):
    estados = defaultdict(list)
    for path in sorted((root / PLAN / 'dias').glob('D??_*.md')):
        for numero, linea in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            if not re.match(r'^\s*- \[[xX]\]', linea):
                continue
            enlace = re.search(r'\]\(\.\./\.\./([^)]*)\)', linea)
            if enlace:
                rel = enlace[1].split('#')[0]
                estados[rel].append({'guia': path.relative_to(root).as_posix(), 'linea': numero,
                                    'enlace': enlace[1],
                                    'estado': 'casilla completada conservada'})
    return estados


def casillas(texto: str):
    return [{'linea': n, 'texto': linea.strip()} for n, linea in enumerate(texto.splitlines(), 1)
            if re.match(r'^\s*- \[[xX]\]', linea)]


def linea_referencia(rel: str, texto: str, patron: str):
    for i, linea in enumerate(texto.splitlines(), 1):
        if re.search(patron, linea, re.I):
            return f'{rel}:{i}'
    return rel


def tiempo(texto: str):
    objetivo = re.search(r'Tiempo objetivo\s*(\d+)\s*min', texto, re.I)
    primera = re.search(r'Primera vez:\s*[≈~]?\s*(\d+)(?:\s*[–-]\s*(\d+))?\s*min', texto, re.I)
    leccion = re.search(r'Tiempo estimado:\s*(\d+)\s*min', texto, re.I)
    return {'objetivo_min': int(objetivo[1]) if objetivo else None,
            'primera_vez_min': [int(primera[1]), int(primera[2] or primera[1])] if primera else None,
            'leccion_total_min': int(leccion[1]) if leccion else None,
            'lectura_min': int(m[1]) if (m := re.search(r'lectura\s*(\d+)', texto)) else None,
            'practica_min': int(m[1]) if (m := re.search(r'práctica\s*(\d+)', texto)) else None,
            'advertencia': 'Estimación declarada; null significa no desglosado, no cero.'}


def extractos(texto: str, patron: str, maximo=5):
    return [linea.strip() for linea in texto.splitlines() if re.search(patron, linea, re.I)][:maximo]


def describir(ident: str, rel: str, texto: str, familia: str, lecciones: dict):
    titulo = next((x.lstrip('# ').strip() for x in texto.splitlines() if x.startswith('# ')), ident)
    nivel = re.search(r'Nivel\s+(\d/3|inicial)', texto, re.I)
    # El enunciado es evidencia, las pistas posteriores no acreditan enseñanza previa.
    enunciado = texto.split('## Pistas')[0].split('## Comprobación')[0]
    conceptos, apoyos = [], list(LECCIONES_P.get(ident, []))
    for patron, concepto, lecs in CONCEPTOS:
        if re.search(patron, enunciado, re.I):
            conceptos.append(concepto)
            if familia == 'SQL':
                apoyos.extend(lecs)
    if familia == 'SQL':
        apoyos.extend(['1.1', '1.2', '1.3'])
    if familia == 'Python/Pandas':
        conceptos.insert(0, 'función con parámetros, retorno y contrato verificable')
    if familia in ('Lección', 'Puente teórico'):
        conceptos = [titulo]
    return {
        'tema': titulo, 'competencias': list(dict.fromkeys(conceptos)) or [titulo],
        'dificultad': nivel[1] if nivel else 'No graduada en el recurso',
        'prerrequisitos_reales': {
            'declarados': extractos(texto, r'Prerrequisit|Requisito|^Lee |Lecciones de apoyo|^Lecciones:'),
            'conceptos_del_enunciado': list(dict.fromkeys(conceptos)),
            'lecciones_preparatorias': [
                {'id': i, 'ruta': '02_TEORIA/' + lecciones[i]['archivo']} for i in dict.fromkeys(apoyos) if i in lecciones],
            'metodo': 'Extracción de prerrequisitos declarados y mapa de conceptos del enunciado; no acredita suficiencia ni secuencia por sí sola.'},
        'entregable': extractos(texto, r'mi_trabajo/|^Entrega:|^\*\*Devuelve:|^Devuelve:|^Qué debes entregar|^\*\*Qué'),
        'comprobacion': extractos(texto, r'Corrector:|corregir_.*\.py|validar_.*\.py|Cómo saber que está bien|rúbrica|^Aceptación:|^Contrato de resultado:'),
        'referencias': [linea_referencia(rel, texto, r'^# '), linea_referencia(rel, texto, r'Prerrequisit|Requisito|^Lee ')],
    }


def recursos(root: Path):
    lecciones = json_fuente(root, 'lecciones.json')
    resultado = {}
    for ident, dato in lecciones['lecciones'].items():
        resultado['L:' + ident] = {'ruta': '02_TEORIA/' + dato['archivo'], 'familia': 'Lección',
            'clasificacion': dato['tipo'], 'dia': dato.get('dia', dato.get('dia_ext'))}
    for ident, dato in lecciones.get('puente', {}).items():
        resultado['L:' + ident] = {'ruta': '02_TEORIA/19_Puente_Python_a_ETL.md', 'familia': 'Puente teórico',
            'clasificacion': 'NÚCLEO', 'dia': dato.get('dia'), 'seccion': dato['seccion'], 'minutos': dato['min']}
    for carpeta, familia in FAMILIAS.items():
        extension = '*.ipynb' if carpeta == 'Notebooks' else '*.md'
        for path in sorted((root / '03_EJERCICIOS' / carpeta).glob(extension)):
            if path.stem in ('INDICE', 'CONTRATOS'):
                continue
            ident = ('EXAMEN:' if carpeta == 'EXAMENES' else '') + path.stem
            tipo = ('Excel' if path.stem.startswith('EX0') else 'Power BI' if path.stem.startswith('PB0') else familia)
            resultado[ident] = {'ruta': path.relative_to(root).as_posix(), 'familia': tipo}
    nucleo, _ = plan_asignaciones(root)
    for numero, dia in nucleo.get('dias', {}).items():
        puerta = dia.get('puerta')
        if puerta:
            resultado['PUERTA:' + puerta['id']] = {'ruta': PLAN + 'COMPETENCIAS.md',
                'familia': 'Puerta/checkpoint', 'clasificacion': 'OBLIGATORIO (CONDICIÓN DE AVANCE)',
                'dia': int(numero), 'titulo': puerta['texto'], 'padre': None}
    for ident, dato in nucleo.get('preparaciones', {}).items():
        resultado['PREPARACION:' + ident] = {'ruta': dato['archivo'] + '#' + dato['ancla'],
            'familia': 'Sección preparatoria', 'clasificacion': 'OBLIGATORIO (SECCIÓN)',
            'dia': dato['dia'], 'titulo': dato['titulo'], 'minutos': dato['min'],
            'padre': 'L:' + dato['leccion']}
    for ident, dato in nucleo.get('items_personalizados', {}).items():
        rel = dato['enlaces'][0][1].removeprefix('../../')
        resultado[ident] = {'ruta': rel, 'familia': 'Fase ETL' if ident.startswith('ETL-') else 'Subrecurso/checkpoint',
            'minutos': dato.get('est'), 'titulo': dato['titulo'], 'nota': dato.get('nota', ''),
            'padre': 'PROYECTO:ETL' if ident.startswith('ETL-') else 'C06' if ident.startswith('C06-') else 'L:10.1' if ident == 'PD-BASE' else 'L:10.2'}
    for nombre, ruta in [('SQL', '05_PROYECTOS/sql/README.md'), ('ETL', '05_PROYECTOS/etl/README.md'),
                          ('BI', '05_PROYECTOS/powerbi/MODELO.md')]:
        resultado['PROYECTO:' + nombre] = {'ruta': ruta, 'familia': 'Proyecto integrador'}
    for path in sorted((root / '06_ENTREVISTAS').glob('SIMULACRO_*.md')):
        resultado['ENTREVISTA:' + path.stem] = {'ruta': path.relative_to(root).as_posix(), 'familia': 'Simulacro laboral'}
    resultado['FINAL:PRIVADA'] = {'ruta': '09_EVALUACION_FINAL/ENUNCIADO.md', 'familia': 'Evaluación final privada',
        'clasificacion': 'OBLIGATORIO SEPARADO', 'privado': True}
    return resultado, lecciones


def actividades_integrales(nucleo):
    propuestas = defaultdict(list)
    for numero, dia in nucleo.get('dias', {}).items():
        ruta = dia.get('ruta_integral', [])
        if isinstance(ruta, dict):
            ruta = ruta.get('actividades', [])
        for actividad in ruta:
            ident = actividad['id']
            propuestas[ident].append({'dia': int(numero), 'clase': 'OBLIGATORIO',
                'fuente': PLAN + 'nucleo.json/ruta_integral', **actividad})
    return propuestas


def propuestas_globales(nucleo):
    propuestas = {}
    fuente = nucleo.get('propuestas_globales', {})
    for dato in fuente.get('obligaciones_conservadas', []):
        propuestas[dato['id']] = dato
    for dato in fuente.get('ofertas_reubicadas_por_prerrequisitos', []):
        for ident in dato['ids']:
            propuestas[ident] = {**dato, 'id': ident, 'prerrequisitos': dato.get('prerrequisitos', dato.get('antes', []))}
    return propuestas


def construir(actual: Path, backup: Path):
    originales, lecciones_antes = recursos(backup)
    actuales, lecciones_despues = recursos(actual)
    base, asignaciones_antes = plan_asignaciones(backup)
    propuesta, asignaciones_despues = plan_asignaciones(actual)
    historicas = historia(backup)
    progreso = progreso_guias(backup)
    rutas = actividades_integrales(propuesta)
    globales = propuestas_globales(propuesta)
    for ident, actividades in rutas.items():
        if ident not in actuales:
            a = actividades[0]
            actuales[ident] = {'ruta': a.get('ruta', ''), 'familia': 'Micropráctica/sección' if a.get('tipo') == 'micropractica' or ident.startswith('MP-') else 'Actividad de sesión',
                'titulo': a.get('titulo', ident), 'padre': a.get('leccion')}
    filas, errores, pendientes = [], [], []
    manifiesto_path = backup.parent / 'MANIFIESTO_SHA256.json'
    manifiesto = json.loads(manifiesto_path.read_text(encoding='utf-8-sig'))
    if manifiesto.get('base_head') != '816890969e3963ffa8c1bb10b2a444c09eb3e748':
        raise ValueError('El manifiesto no identifica el HEAD de protección esperado')
    publicas = {d['ruta'].split('#')[0] for d in originales.values()}
    publicas.update(PLAN + x for x in ('nucleo.json', 'lecciones.json', 'calendario.json'))
    publicas.update(p.relative_to(backup).as_posix() for p in (backup / PLAN / 'dias').glob('D??_*.md'))
    for rel in sorted(publicas):
        esperada = manifiesto['archivos'].get(rel)
        if not esperada or sha(backup / rel) != esperada:
            raise ValueError(f'Baseline no coincide con manifiesto protegido: {rel}')
    for ident in sorted(set(originales) | set(actuales)):
        antes, despues = originales.get(ident), actuales.get(ident)
        dato = despues or antes
        rel = dato['ruta']
        privado = dato.get('privado', False)
        texto = '' if privado else leer(actual if despues else backup, rel)
        if dato['familia'] == 'Notebook guiado' and texto:
            nb = json.loads(texto)
            texto = '\n'.join(''.join(c.get('source', [])) for c in nb.get('cells', []) if c.get('cell_type') == 'markdown')
        descriptivo = describir(ident, rel, texto, dato['familia'], lecciones_despues['lecciones'])
        if dato.get('titulo'):
            descriptivo['tema'] = dato['titulo']
        if dato.get('nota'):
            descriptivo['entregable'].insert(0, dato['nota'])
        a_antes = asignaciones_antes.get(ident, [])
        a_despues = asignaciones_despues.get(ident, [])
        clases_antes = sorted({a['clase'] for a in a_antes}) or ([antes['clasificacion']] if antes and 'clasificacion' in antes else ['DISPONIBLE; SIN ASIGNACIÓN CANÓNICA'])
        clases_despues = sorted({a['clase'] for a in a_despues}) or ([despues['clasificacion']] if despues and 'clasificacion' in despues else ['DISPONIBLE; SIN ASIGNACIÓN CANÓNICA'])
        clases_fuente = list(clases_despues)
        ruta_obligatoria = any(a.get('tipo') not in ('refuerzo', 'extendida') for a in rutas.get(ident, []))
        if ruta_obligatoria:
            clases_despues = ['NÚCLEO' if ident.startswith('L:') else 'OBLIGATORIO (RUTA INTEGRAL)']
        propuesta_global = globales.get(ident)
        if propuesta_global:
            clases_despues = [propuesta_global.get('clasificacion', 'REFUERZO PROPUESTO; REUBICADO')]
        obligatoria = any(c.startswith('OBLIGATORIO') for c in clases_antes) or ident in historicas
        marcas_originales = progreso.get(rel.split('#')[0], [])
        if '#' in rel:
            # Completar una lección no acredita automáticamente cada sección o
            # nueva micropráctica que apunte al mismo archivo.
            marcas_originales = [e for e in marcas_originales if e['enlace'] == rel]
        # S3/S5 ya constan completos en D03, que permanece inmutable. La revisión
        # histórica los reconoce; no impone repetirlos ni inventa otra casilla.
        acreditada_historicamente = ident in ('S3', 'S5') and any('/D03_' in x['guia'] for x in marcas_originales)
        restaurar = obligatoria and not (any(c.startswith('OBLIGATORIO') for c in clases_fuente) or ruta_obligatoria) and not acreditada_historicamente
        if restaurar:
            clases_despues = list(dict.fromkeys(['OBLIGATORIO HISTÓRICO; RESTAURACIÓN PENDIENTE'] + clases_despues))
            pendientes.append(ident)
        if acreditada_historicamente:
            clases_despues = ['OBLIGATORIO HISTÓRICO ACREDITADO D03; SIN NUEVA DEUDA']
        origen = sorted({a['dia'] for a in a_antes}) or ([antes['dia']] if antes and antes.get('dia') else [])
        destino = sorted({a['dia'] for a in rutas.get(ident, [])}) or sorted({a['dia'] for a in a_despues}) or ([despues['dia']] if despues and despues.get('dia') else [])
        if propuesta_global and propuesta_global.get('destino_propuesto'):
            destino = [propuesta_global['destino_propuesto']]
        generado = []
        for a in rutas.get(ident, []):
            guia = next((actual / PLAN / 'dias').glob(f'D{a["dia"]:02}_*.md'), None)
            marca = re.compile(r'<!--\s*actividad:' + re.escape(ident) + r'\s*-->')
            if guia and marca.search(guia.read_text(encoding='utf-8-sig')):
                generado.append(a['dia'])
        existencia = (actual / rel.split('#')[0]).is_file() if rel else False
        if antes and not existencia:
            errores.append(f'Recurso original ausente: {ident} {rel}')
        texto_antes = '' if privado or not antes else leer(backup, antes['ruta'])
        if rutas.get(ident):
            competencias_sesion = [c for a in rutas[ident] for c in a.get('competencias', [])]
            if competencias_sesion:
                descriptivo['competencias'] = list(dict.fromkeys(descriptivo['competencias'] + competencias_sesion))
            descriptivo['entregable'].extend(a['entregable'] for a in rutas[ident] if a.get('entregable'))
            descriptivo['comprobacion'].extend(a['comprobacion'] for a in rutas[ident] if a.get('comprobacion'))
            descriptivo['prerrequisitos_reales']['declarados_en_sesion'] = [a.get('prerrequisitos', []) for a in rutas[ident]]
        if propuesta_global:
            descriptivo['prerrequisitos_reales']['declarados_en_propuesta_global'] = propuesta_global.get('prerrequisitos', [])
        personal = []
        for carpeta in ('sql', 'python', 'analitico', 'hitos'):
            patron_personal = ident + '.*' if re.fullmatch(r'[A-Za-z0-9_-]+', ident) else '__sin_correspondencia__'
            for path in (actual / 'mi_trabajo' / carpeta).glob(patron_personal):
                personal.append(path.relative_to(actual).as_posix())
        filas.append({'id': ident, 'familia': dato['familia'], 'ruta': rel,
            **descriptivo, 'original': {'clasificacion': clases_antes, 'jornadas': origen,
                'tiempo': tiempo(texto_antes), 'asignaciones': a_antes,
                'minutos_asignados': antes.get('minutos') if antes else None,
                'sha256': sha(backup / antes['ruta'].split('#')[0]) if antes else None},
            'historico_obligatorio': historicas.get(ident, []),
            'propuesto': {'clasificacion': clases_despues, 'jornadas': destino,
                'clasificacion_fuente_anterior_a_ruta_integral': clases_fuente,
                'propuesta_global_no_implementada': propuesta_global,
                'tiempo': tiempo(texto), 'minutos_sesion': sum(a.get('minutos', 0) for a in rutas.get(ident, [])) or dato.get('minutos'),
                'sesiones': rutas.get(ident, []), 'jornadas_con_aparicion_en_guia': generado,
                'estado': 'Obligación histórica acreditada en D03 inmutable' if acreditada_historicamente else 'Muestra en guía; revisar secuencia' if generado else 'Propuesta global; no implementada' if propuesta_global else 'Propuesta en fuente; no regenerada' if rutas.get(ident) else 'Conservado; revisión integral pendiente',
                'restauracion_pendiente': restaurar},
            'justificacion_traslado': 'Restaurar obligación histórica; destino y práctica previos aún deben cerrarse.' if restaurar else 'Enseñar y practicar prerrequisitos antes de la tarea; detalle en ruta_integral.' if origen != destino else 'Sin traslado registrado.',
            'progreso': {'casillas_completadas_originales': marcas_originales,
                'criterios_completados_en_recurso_original': casillas(texto_antes),
                'obligacion_historica_acreditada': acreditada_historicamente,
                'archivos_personales_existentes_sin_leer': personal,
                'advertencia': 'Existencia de archivo o casilla parcial no acredita dominio ni finalización total.'},
            'independiente': dato['familia'] not in ('Fase ETL', 'Subrecurso/checkpoint', 'Micropráctica/sección', 'Actividad de sesión', 'Puerta/checkpoint', 'Sección preparatoria'),
            'practica_autonoma_independiente': dato['familia'] in ('SQL', 'Python/Pandas', 'Estadística', 'Excel', 'Power BI', 'Mini-ETL', 'Depuración', 'Criterio analítico', 'Caso') and ident != 'C06',
            'padre': dato.get('padre'), 'original_disponible': existencia,
            'revision_semantica': 'Preparación y orden explícitos en la muestra; revisar evidencia del alumno.' if rutas.get(ident) else 'Mapa preliminar; revisión semántica integral pendiente fuera de muestra.',
            'contenido_privado_no_leido': privado})
    # Protección histórica: bytes D01–D03 y todas las marcas completadas D04.
    proteccion = []
    progreso_actual = progreso_guias(actual)
    for rel, marcas in progreso.items():
        por_guia = Counter(x['guia'] for x in marcas)
        ahora_por_guia = Counter(x['guia'] for x in progreso_actual.get(rel, []))
        for guia, cantidad in por_guia.items():
            if ahora_por_guia[guia] < cantidad:
                errores.append(f'Casillas previas perdidas: {guia} -> {rel}')
    for n in range(1, 5):
        original = next((backup / PLAN / 'dias').glob(f'D{n:02}_*.md'))
        current = actual / original.relative_to(backup)
        identicas = sha(original) == sha(current)
        if n <= 3 and not identicas:
            errores.append(f'D{n:02}: bytes protegidos modificados')
        completadas_antes = {r: len([e for e in evid if e['guia'].startswith(f'{PLAN}dias/D{n:02}_')]) for r, evid in progreso.items()}
        completadas_ahora = progreso_actual
        perdidas = [r for r, cantidad in completadas_antes.items() if cantidad and len([e for e in completadas_ahora.get(r, []) if e['guia'].startswith(f'{PLAN}dias/D{n:02}_')]) < cantidad]
        if perdidas:
            errores.append(f'D{n:02}: marcas completadas perdidas: {perdidas}')
        proteccion.append({'dia': n, 'sha256_original': sha(original), 'sha256_actual': sha(current),
            'bytes_identicos': identicas, 'casillas_completadas_perdidas': perdidas})
    return {'version': 1, 'alcance': 'Inventario y reconciliación provisional; no certifica la corrección global.',
        'baseline': {'ruta': str(backup), 'commit': '816890969e3963ffa8c1bb10b2a444c09eb3e748',
            'historia_nucleo': list(REVISIONES), 'manifiesto': str(manifiesto_path),
            'sha256_manifiesto': sha(manifiesto_path), 'fuentes_publicas_verificadas': len(publicas)},
        'reglas': ['Una fila por ID canónico; SQL N1 y notebook N01 son distintos.',
            'Fases, secciones y checkpoints se identifican sin contarlos como ejercicios independientes.',
            'Las soluciones, datos privados y código personal no se leen ni se ejecutan.',
            'D01–D03 se conservan byte a byte; las casillas completas D04 se preservan.',
            'Una propuesta en fuente no equivale a jornada regenerada ni a actividad completada.'],
        'resumen': {'recursos': len(filas), 'por_familia': dict(sorted(Counter(f['familia'] for f in filas).items())),
            'historicos_obligatorios_distintos': len(historicas),
            'obligaciones_pendientes_de_restauracion': pendientes,
            'jornadas_muestra_pendientes_de_regeneracion': sorted({a['dia'] for f in filas for a in f['propuesto']['sesiones'] if a['dia'] not in f['propuesto']['jornadas_con_aparicion_en_guia']}),
            'recursos_originales_ausentes': [f['id'] for f in filas if f['original']['sha256'] and not f['original_disponible']]},
        'proteccion': proteccion, 'errores': errores, 'recursos': filas}


def compacto(valor):
    if isinstance(valor, (list, dict)):
        valor = json.dumps(valor, ensure_ascii=False, separators=(',', ':'))
    return str(valor).replace('|', '\\|').replace('\n', ' ')


def markdown(datos):
    r = datos['resumen']
    lineas = ['# Inventario de recursos: antes y después (reconciliación provisional)', '',
        datos['alcance'], '', f'Baseline externo: `{datos["baseline"]["ruta"]}`; HEAD `{datos["baseline"]["commit"]}`.', '',
        'El JSON y CSV adjuntos contienen los campos completos por recurso: competencia, dificultad, clasificación, jornadas, tiempos declarados, prerrequisitos, lecciones, entregable, comprobación, justificación y progreso observado.', '',
        '## Alcance y límites', ''] + ['- ' + regla for regla in datos['reglas']]
    lineas += ['', f'Total: {r["recursos"]} recursos/subrecursos; unión histórica: {r["historicos_obligatorios_distintos"]} ID que alguna revisión declaró obligatorios.', '',
        '| Familia | Recursos |', '|---|---:|']
    lineas += [f'| {k} | {v} |' for k, v in r['por_familia'].items()]
    lineas += ['', '## Obligaciones históricas aún por restaurar', '',
        'Los ID siguientes conservan su material, pero su asignación obligatoria global todavía no está aplicada. No se declara cumplida la reconciliación mientras queden pendientes:', '',
        ', '.join(f'`{i}`' for i in r['obligaciones_pendientes_de_restauracion']) or 'Ninguna en la comparación actual.', '',
        '## Protección del progreso', '', '| Día | Bytes idénticos | Casillas completadas perdidas |', '|---|---|---|']
    lineas += [f'| D{x["dia"]:02} | {x["bytes_identicos"]} | {compacto(x["casillas_completadas_perdidas"])} |' for x in datos['proteccion']]
    lineas += ['', '## Registro por recurso', '',
        'Los destinos vacíos o conservados fuera de muestra siguen sujetos al mapa de competencias. Los tiempos null no se interpretan como cero. La práctica de una fase no se vuelve a sumar como proyecto padre.', '',
        '| ID / recurso | Clase y día originales | Obligación histórica | Clase y día propuestos | Minutos de sesión | Estado / progreso |',
        '|---|---|---|---|---:|---|']
    for f in datos['recursos']:
        a, d = f['original'], f['propuesto']
        p = f['progreso']
        lineas.append(f'| `{f["id"]}` [{compacto(f["tema"])}](../../{f["ruta"]}) | {compacto(a["clasificacion"])}; {compacto(a["jornadas"])} | {compacto(sorted({x["dia"] for x in f["historico_obligatorio"]}))} | {compacto(d["clasificacion"])}; {compacto(d["jornadas"])} | {d["minutos_sesion"] if d["minutos_sesion"] is not None else "pendiente"} | {d["estado"]}; {len(p["casillas_completadas_originales"])} marcas previas; {len(p["archivos_personales_existentes_sin_leer"])} archivos personales existentes |')
    lineas += ['', '## Competencias, preparación y comprobación', '',
        '| ID | Competencias / dificultad | Prerrequisitos declarados y conceptos | Lecciones de preparación | Entregable / comprobación | Justificación |', '|---|---|---|---|---|---|']
    for f in datos['recursos']:
        p = f['prerrequisitos_reales']
        lineas.append('| ' + ' | '.join(compacto(x) for x in [f['id'], [f['competencias'], f['dificultad']], [p['declarados'], p['conceptos_del_enunciado']], [x['id'] for x in p['lecciones_preparatorias']], [f['entregable'], f['comprobacion']], f['justificacion_traslado']]) + ' |')
    lineas += ['', '## Fallos de protección o disponibilidad', '', '\n'.join('- ' + x for x in datos['errores']) or 'No se detectaron pérdidas de archivos originales ni de las marcas protegidas.', '',
        'Esto no equivale a aceptar la secuencia completa: las obligaciones pendientes y los prerrequisitos requieren revisión semántica y autorización de la siguiente muestra.', '']
    return '\n'.join(lineas)


def csv_texto(datos):
    salida = io.StringIO(newline='')
    campos = ['id', 'ruta', 'familia', 'tema', 'competencias', 'dificultad', 'original',
              'historico_obligatorio', 'prerrequisitos_reales', 'propuesto', 'entregable',
              'comprobacion', 'justificacion_traslado', 'progreso', 'independiente', 'padre']
    writer = csv.DictWriter(salida, fieldnames=campos, lineterminator='\n')
    writer.writeheader()
    for fila in datos['recursos']:
        writer.writerow({k: json.dumps(fila[k], ensure_ascii=False, separators=(',', ':')) if isinstance(fila[k], (list, dict)) else fila[k] for k in campos})
    return salida.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raiz', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--comprobar', action='store_true', help='Alias explícito del modo predeterminado de solo lectura')
    parser.add_argument('--escribir', action='store_true', help='Escribe exclusivamente los tres archivos INVENTARIO en docs/auditorias')
    args = parser.parse_args()
    if args.escribir and args.comprobar:
        parser.error('--escribir y --comprobar son mutuamente excluyentes')
    datos = construir(args.raiz.resolve(), args.baseline.resolve())
    if args.escribir:
        destino = args.raiz.resolve() / 'docs/auditorias'
        destino.mkdir(parents=True, exist_ok=True)
        textos = (markdown(datos), json.dumps(datos, ensure_ascii=False, indent=2) + '\n', csv_texto(datos))
        for nombre, contenido in zip(SALIDAS, textos):
            (destino / nombre).write_text(contenido, encoding='utf-8', newline='\n')
    print(json.dumps({'resumen': datos['resumen'], 'proteccion': datos['proteccion'], 'errores': datos['errores'], 'archivos_escritos': list(SALIDAS) if args.escribir else []}, ensure_ascii=False, indent=2))
    return 1 if datos['errores'] else 0


if __name__ == '__main__':
    sys.exit(main())
