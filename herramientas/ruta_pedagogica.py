"""Renderizado acotado de la muestra pedagógica, sin modificar salidas globales.

Las actividades tienen identidad propia; las sesiones solo las referencian.
El progreso procede del documento existente, nunca de un supuesto del catálogo.
"""
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess


PROTEGIDOS = {1, 2, 3}
VOLUNTARIOS = {'refuerzo', 'extendida'}
TIPOS = {'nucleo', 'micropractica', 'obligatorio', 'repaso', 'aplicacion',
         'criterio', 'evaluacion', 'refuerzo', 'extendida'}
ETIQUETAS = {'nucleo': 'NÚCLEO', 'micropractica': 'MICROPRÁCTICA ESENCIAL',
             'obligatorio': 'OBLIGATORIO', 'repaso': 'REPASO',
             'aplicacion': 'APLICACIÓN EMPRESARIAL', 'criterio': 'COMPROBACIÓN',
             'evaluacion': 'EVALUACIÓN', 'refuerzo': 'REFUERZO CONDICIONAL',
             'extendida': 'EXTENDIDA'}
FIRMA = re.compile(r'^<!-- ruta:lineas-generadas (\[.*\]) -->$', re.M)
ACTIVIDAD = re.compile(r'<!-- actividad:([^>]+) -->')
CASILLA = re.compile(r'^\s*(?:>\s*)?- \[([ xX])\]')


def huella_linea(linea):
    """El cambio legítimo de [ ] a [x] no convierte la línea en una nota."""
    normal = re.sub(r'^(\s*(?:>\s*)?- \[)[xX](\])', r'\1 \2', linea).strip()
    return sha256(normal.encode('utf-8')).hexdigest()[:20]


def id_linea(linea):
    m = ACTIVIDAD.search(linea)
    if m:
        return m.group(1).strip()
    m = re.search(r'03_EJERCICIOS/([^\s)]+)', linea)
    if m:
        destino = m.group(1).split('#', 1)[0]
        stem = Path(destino).stem
        return 'EXAMEN:' + stem if destino.startswith('EXAMENES/') else stem
    m = re.search(r'\[(\d+\.\d+)(?:[ ·\]])', linea)
    return 'L:' + m.group(1) if m else None


def lineas_accionables(texto):
    """Casillas vigentes: excluye citas, comentarios y ejemplos en código."""
    fence, comentario = None, False
    for numero, linea in enumerate(texto.splitlines()):
        if comentario:
            if '-->' in linea:
                comentario = False
            continue
        if '<!--' in linea and '-->' not in linea:
            comentario = True
            continue
        marca = re.match(r'^\s*(`{3,}|~{3,})', linea)
        if marca:
            if fence is None:
                fence = marca.group(1)
            elif marca.group(1)[0] == fence[0] and len(marca.group(1)) >= len(fence):
                fence = None
            continue
        if fence is None and re.match(r'^\s*- \[[ xX]\]', linea):
            yield numero, linea


def estados_existentes(texto):
    estados, originales = {}, {}
    for _, linea in lineas_accionables(texto):
        m = CASILLA.match(linea)
        identidad = id_linea(linea) if m else None
        if identidad:
            marcado = m.group(1).lower() == 'x'
            estados[identidad] = estados.get(identidad, False) or marcado
            if marcado or identidad not in originales:
                originales[identidad] = re.sub(r'^\s*>\s?', '', linea)
    return estados, originales


def notas_personales(ctx, ruta, texto):
    """Conserva inserciones personales sin volver a publicar instrucciones viejas.

    La primera migración compara con HEAD solo en una copia que tenga Git.
    Las siguientes usan firmas de líneas generadas, sin guardar la guía antigua.
    Las copias sin Git conservan notas explícitas, citas y fragmentos de código.
    """
    conocidas = None
    m = FIRMA.search(texto)
    if m:
        conocidas = set(json.loads(m.group(1)))
    elif (ctx.raiz / '.git').exists():
        relativa = ruta.relative_to(ctx.raiz).as_posix()
        r = subprocess.run(['git', '-c', 'safe.directory=' + str(ctx.raiz), '--no-optional-locks',
                            'show', 'HEAD:' + relativa], cwd=ctx.raiz, capture_output=True)
        if r.returncode == 0:
            conocidas = {huella_linea(x) for x in r.stdout.decode('utf-8').splitlines()}
    lineas = texto.splitlines()
    bloques, reservadas = [], set()
    for inicio, linea in enumerate(lineas):
        encabezado = re.match(r'^(#{1,6})\s+(?:Notas personales|Apuntes|Evidencias)(?:\s.*)?$', linea, re.I)
        if not encabezado or linea == '## Notas personales conservadas' or inicio in reservadas:
            continue
        nivel = len(encabezado.group(1))
        fin = inicio + 1
        while fin < len(lineas):
            siguiente = re.match(r'^(#{1,6})\s+', lineas[fin])
            if (siguiente and len(siguiente.group(1)) <= nivel) or FIRMA.fullmatch(lineas[fin]):
                break
            fin += 1
        bloques.append((None, '\n'.join(lineas[inicio:fin]).rstrip()))
        reservadas.update(range(inicio, fin))
    # El código personal se conserva como bloque completo, incluidos sus cierres
    # y líneas vacías. Las firmas no sirven para descartar apuntes ya versionados.
    inicio = 0
    while inicio < len(lineas):
        marca = re.match(r'^\s*(`{3,}|~{3,})', lineas[inicio])
        if inicio in reservadas or not marca:
            inicio += 1
            continue
        fin = inicio + 1
        while fin < len(lineas):
            cierre = re.match(r'^\s*(`{3,}|~{3,})', lineas[fin])
            if cierre and cierre.group(1)[0] == marca.group(1)[0] and len(cierre.group(1)) >= len(marca.group(1)):
                break
            fin += 1
        if fin == len(lineas):
            raise ValueError('Hay un bloque de código sin cerrar; conserva su límite antes de regenerar')
        bloques.append((None, '\n'.join(lineas[inicio:fin + 1])))
        reservadas.update(range(inicio, fin + 1))
        inicio = fin + 1
    notas, contexto, codigo = list(bloques), None, False
    for numero, linea in enumerate(lineas):
        if numero in reservadas:
            continue
        asociada = re.match(r'^\*\*Actividad asociada: (.+)\.\*\*$', linea)
        if asociada:
            contexto = asociada.group(1)
        if CASILLA.match(linea) and id_linea(linea):
            contexto = id_linea(linea)
        if FIRMA.fullmatch(linea) or '<!-- ruta:' in linea:
            continue
        if linea.lstrip().startswith(('```', '~~~')):
            codigo = not codigo
        if CASILLA.match(linea):
            if conocidas is not None and huella_linea(linea) not in conocidas:
                contenido = re.sub(r'^\s*(?:>\s*)?- \[[ xX]\]\s*', '', linea)
                notas.append((id_linea(linea), 'Evidencia o edición conservada: ' + contenido))
            continue
        if not linea.strip():
            continue
        nueva = conocidas is not None and huella_linea(linea) not in conocidas
        explicita = bool(re.match(r'^\s*(?:>\s*)?(?:NOTA(?:S)?(?: PERSONAL(?:ES)?)?|ANOTACI[ÓO]N|EVIDENCIA PERSONAL)\s*:', linea, re.I))
        if nueva or explicita or (conocidas is None and (codigo or linea.startswith('>'))):
            if linea.startswith('## Notas personales') or linea.startswith('**Actividad asociada:'):
                continue
            notas.append((contexto, linea))
    # No repetir notas en una regeneración posterior.
    return list(dict.fromkeys(notas))


def ruta_local(ctx, actividad):
    relativa = actividad.get('ruta', '').split('#', 1)[0]
    if not relativa:
        return None
    archivo = (ctx.raiz / relativa).resolve()
    if not archivo.is_relative_to(ctx.raiz.resolve()):
        raise ValueError(f'{actividad["id"]}: ruta fuera del repositorio')
    return archivo


def historial(a):
    return a.get('estado_acreditacion') == 'historico'


def requeridas(ficha):
    return [a for a in ficha['ruta_integral'] if a['tipo'] not in VOLUNTARIOS and not historial(a)]


def bloques_fijos(cal):
    pool = {'SQL', 'Teoría', 'Teoría/retro', 'Práctica', 'Lecciones', 'Criterio'}
    return [(nombre.strip(), minutos) for nombre, minutos in cal['bloques']
            if nombre.strip() not in pool and not nombre.strip().startswith('Examen')]


def validar_ruta(ctx, dia):
    ficha = ctx.nucleo['dias'].get(str(dia))
    if not ficha:
        raise ValueError(f'D{dia:02}: falta fuente de jornada')
    if ficha.get('modo_integral') == 'editorial':
        return
    actividades = ficha.get('ruta_integral')
    if not isinstance(actividades, list) or not actividades:
        raise ValueError(f'D{dia:02}: falta ruta_integral ordenada')
    vistos = set()
    por_id = {a.get('id'): a for a in actividades}
    for a in actividades:
        identidad = a.get('id')
        if not identidad or identidad in vistos:
            raise ValueError(f'D{dia:02}: identidad vacía o duplicada: {identidad}')
        if a.get('tipo') not in TIPOS:
            raise ValueError(f'{identidad}: tipo desconocido')
        if type(a.get('minutos')) is not int or a['minutos'] < 0:
            raise ValueError(f'{identidad}: minutos inválidos')
        if historial(a) and a['minutos'] != 0:
            raise ValueError(f'{identidad}: el registro histórico no suma minutos nuevos')
        if not historial(a) and a['tipo'] not in VOLUNTARIOS and a['minutos'] == 0:
            raise ValueError(f'{identidad}: obligación nueva sin tiempo')
        archivo = ruta_local(ctx, a)
        if archivo is not None and not archivo.is_file():
            raise ValueError(f'{identidad}: no existe {a["ruta"]}')
        if a['tipo'] == 'micropractica' and not a.get('comprobacion'):
            raise ValueError(f'{identidad}: micropráctica sin comprobación')
        for evidencia in a.get('evidencia', []):
            archivo_evidencia = ruta_local(ctx, {'id': identidad, 'ruta': evidencia.get('ruta', '')})
            if archivo_evidencia is None or not archivo_evidencia.is_file():
                raise ValueError(f'{identidad}: no existe la evidencia conservada {evidencia.get("ruta", "")}')
        for pre in a.get('prerrequisitos', []):
            if pre in por_id and a['tipo'] not in VOLUNTARIOS and not historial(a):
                anterior = por_id[pre]
                if anterior['tipo'] in VOLUNTARIOS and not historial(anterior):
                    raise ValueError(f'{identidad}: el prerrequisito {pre} es voluntario; necesita preparación obligatoria')
            if pre in por_id and pre not in vistos:
                raise ValueError(f'{identidad}: prerrequisito {pre} posterior dentro de la jornada')
        vistos.add(identidad)
    # Las listas legacy siguen siendo el contrato de clasificación de la muestra.
    originales = {x['id'] if isinstance(x, dict) else x for x in ficha['obligatorio']}
    cubiertos = {a['id'] for a in actividades if a['tipo'] not in VOLUNTARIOS or historial(a)}
    if originales - cubiertos:
        raise ValueError(f'D{dia:02}: obligaciones sin representar: {sorted(originales - cubiertos)}')
    sesiones = ficha.get('sesiones_integrales', [])
    if sesiones:
        ids = [i for sesion in sesiones for i in sesion['actividades']]
        if ids != [a['id'] for a in requeridas(ficha)]:
            raise ValueError(f'D{dia:02}: las sesiones deben cubrir cada obligación vigente una vez y en orden')


def enlace_actividad(a):
    titulo = a.get('titulo') or a['id']
    destino = a.get('ruta')
    if destino:
        if a.get('seccion') and '#' not in destino:
            destino += '#' + a['seccion'].lstrip('#')
        return f'[{a["id"]} · {titulo}](../../{destino})'
    return f'**{a["id"]} · {titulo}**'


def competencia_legible(ctx, competencia):
    areas = {'SQL': 'Consultas SQL y validación de resultados',
             'Python': 'Programación en Python y contratos de funciones',
             'Pandas': 'Análisis y validación de tablas con Pandas',
             'Estadistica': 'Estadística e interpretación de resultados',
             'Analitico': 'Criterio analítico y decisiones empresariales',
             'Depuracion': 'Depuración y lectura de trazas',
             'depuracion': 'Depuración y lectura de trazas'}
    if competencia in areas:
        return areas[competencia]
    fuente = ctx.lecciones.get('lecciones', {}).get(competencia)
    if fuente:
        texto = (ctx.raiz / '02_TEORIA' / fuente['archivo']).read_text(encoding='utf-8')
        m = re.search(r'^# \d+\.\d+ (.+)$', texto, re.M)
        if m:
            return m.group(1).strip()
    return competencia.replace('_', ' ')


def lineas_actividad(ctx, a, estado=False):
    l = [f'- [{"x" if estado else " "}] {enlace_actividad(a)} · **{ETIQUETAS[a["tipo"]]}** · {a["minutos"]} min. <!-- actividad:{a["id"]} -->']
    for clave, nombre in [('instruccion', 'Haz'), ('entregable', 'Entrega'), ('comprobacion', 'Comprueba')]:
        if a.get(clave):
            l.append(f'  - **{nombre}:** {a[clave]}')
    if a.get('competencias'):
        l.append('  - **Competencia:** ' + '; '.join(competencia_legible(ctx, c) for c in a['competencias']) + '.')
    for evidencia in a.get('evidencia', []):
        descripcion = evidencia.get('descripcion') or 'Archivo existente'
        l.append(f'  - **Evidencia conservada:** [{descripcion}](../../{evidencia["ruta"]}). '
                 'La referencia conserva el registro; no atribuye una validación nueva.')
    l.append('')
    return l


def sesiones(ficha, fijos):
    actividades = {a['id']: a for a in requeridas(ficha)}
    grupos = ficha.get('sesiones_integrales') or [
        {'id': f'S{n:02}', 'titulo': a.get('titulo', a['id']), 'actividades': [a['id']]}
        for n, a in enumerate(actividades.values(), 1)]
    filas = []
    for grupo in grupos:
        ids = grupo['actividades']
        minutos = sum(actividades[i]['minutos'] for i in ids)
        # Los tramos referencian una misma actividad; no crean otras casillas.
        restante, tramo = minutos, 1
        while restante:
            usados = min(75, restante)
            sufijo = f' · tramo {tramo}' if minutos > 75 else ''
            filas.append((grupo['id'] + sufijo, grupo.get('titulo', ''), usados, ', '.join(ids)))
            restante -= usados
            tramo += 1
    for nombre, minutos in fijos:
        if minutos:
            filas.append((nombre, 'Bloque original conservado', minutos, ''))
    return filas


def seccion_original(texto, titulo, siguiente=None):
    patron = r'^## ' + re.escape(titulo) + r'[^\n]*\n.*?(?=^## |\Z)'
    m = re.search(patron, texto, re.M | re.S)
    return m.group().strip() if m else ''


def firmar(texto):
    generado = texto.split('## Notas personales conservadas', 1)[0]
    firmas = sorted({huella_linea(x) for x in generado.splitlines() if x.strip()})
    return texto.rstrip() + '\n\n<!-- ruta:lineas-generadas ' + json.dumps(firmas, separators=(',', ':')) + ' -->\n'


def renderizar_guia(ctx, dia, ficha, cal, original, ruta):
    estados, lineas_previas = estados_existentes(original)
    cierre_previo = seccion_original(original, 'Comprobar y entregar')
    sin_identidad = [linea for _, linea in lineas_accionables(original)
                    if CASILLA.match(linea) and CASILLA.match(linea).group(1).lower() == 'x'
                    and not id_linea(linea) and linea not in cierre_previo.splitlines()]
    if sin_identidad:
        raise ValueError(f'D{dia:02}: hay casillas completadas sin identidad; asigna una identidad conservando su evidencia antes de regenerar')
    actividades = ficha['ruta_integral']
    existentes = {a['id'] for a in actividades}
    faltan = {i for i, completada in estados.items() if completada and i not in existentes}
    if faltan:
        raise ValueError(f'D{dia:02}: conservar antes los registros completados {sorted(faltan)}')
    for a in actividades:
        if historial(a) and not estados.get(a['id']):
            raise ValueError(f'{a["id"]}: el catálogo atribuye avance histórico que no existe')
    fijos = bloques_fijos(cal)
    base = sum(a['minutos'] for a in requeridas(ficha)) + sum(m for _, m in fijos)
    voluntario = sum(a['minutos'] for a in actividades if a['tipo'] in VOLUNTARIOS and not historial(a))
    titulo_carga = 'BASE pendiente estimado' if any(historial(a) for a in actividades) else 'BASE estimado'
    l = [original.splitlines()[0], '', '## ' + (ficha.get('titulo') or cal['titulo']), '',
         '**Objetivo de trabajo:** ' + (ficha.get('objetivo') or cal.get('objetivo', '')), '',
         f'**{titulo_carga}: {base} min ({base / 60:.1f} h), en sesiones retomables.** Voluntario separado: {voluntario} min. '
         'La fecha identifica la secuencia académica; puedes emplear varios días reales.', '',
         f'<!-- base_min:{base} -->', '',
         '<!-- ruta:integral:inicio -->', '## Competencias y prerrequisitos', '']
    competencias = list(dict.fromkeys(competencia_legible(ctx, c) for a in requeridas(ficha) for c in a.get('competencias', [])))
    l += ['- ' + c for c in competencias]
    l += ['', 'Antes de comenzar:']
    l += ['- ' + e['texto'] for e in ficha.get('entra', [])]
    l += ['', 'Si falta una base, recupérala antes de la actividad que la utiliza. Las obligaciones conservan su condición pendiente.', '']
    historicas = [a for a in actividades if historial(a)]
    if historicas:
        l += ['**Avance acreditado conservado:** las casillas ya marcadas permanecen marcadas una sola vez en la ruta. '
              'Sus 0 min significan que no hay trabajo pendiente que repetir; no estiman el tiempo real invertido. '
              'Esta cifra pendiente no representa la duración académica integral de D04. Las microprácticas nuevas quedan pendientes.', '']
    l += ['## Ruta obligatoria en orden', '',
          'Sigue los pasos en este orden: explicación y ejemplo, micropráctica, trabajo autónomo y comprobación. '
          'Una casilla de lectura anterior no acredita una práctica nueva.', '']
    ruta_activa = [a for a in actividades if a['tipo'] not in VOLUNTARIOS or historial(a)]
    for n, a in enumerate(ruta_activa, 1):
        l += [f'### Paso {n} · {ETIQUETAS[a["tipo"]]}', '']
        if historial(a):
            l += lineas_actividad(ctx, a, True)
            l += ['Realización acreditada previamente; conserva tu evidencia y continúa sin repetirla. '
                  'La lectura completada no marca como hecha ninguna micropráctica nueva.', '']
        else:
            l += lineas_actividad(ctx, a, estados.get(a['id'], False))
    if ficha.get('puerta'):
        l += ['## Puerta de competencia', '', ficha['puerta']['texto'], '']
    for tipo in ('refuerzo', 'extendida'):
        l += ['## ' + ETIQUETAS[tipo], '']
        items = [a for a in actividades if a['tipo'] == tipo and not historial(a)]
        if not items:
            l += ['Sin tareas adicionales asignadas.', '']
        for a in items:
            l += lineas_actividad(ctx, a, estados.get(a['id'], False))
    l += ['## REDUCIDO', '',
          'Completa una sesión retomable hasta su comprobación y registra dónde retomar. No omitas los prerrequisitos de lo que intentes. '
          'Mantén el empleo y el cierre en sus bloques originales; si debes interrumpirlos, registra también su siguiente paso.', '',
          '**OBLIGATORIO PENDIENTE:** todo paso obligatorio de esta guía que quede sin completar. Retómalo en orden antes del ejercicio o evaluación '
          'que dependa de él. No se convierte en REFUERZO. Esta modalidad no acredita las competencias pendientes.', '',
          '## MÍNIMO', '',
          'Quince minutos de memoria sobre una consulta o función previamente resuelta, más cinco minutos de cierre. '
          'No acredita contenidos nuevos. La ruta pendiente conserva la condición **OBLIGATORIO PENDIENTE**; registra el punto de recuperación.', '',
          '## Sesiones retomables y minutos', '', '| Sesión | Propósito | Minutos | Actividades (referencia) |', '|---|---|---:|---|']
    for sid, titulo, minutos, ids in sesiones(ficha, fijos):
        l.append(f'| {sid} | {titulo} | {minutos} | {ids} |')
    l += [f'| **Total BASE** | | **{base}** | |', '',
          'Al interrumpir: guarda el archivo, el último control y el siguiente paso. Las pausas van fuera de estos minutos; '
          'los tramos de una actividad comparten una única casilla.', '',
          '## Distribución neta', '', '|Bloque|Minutos|Acción|', '|---|---:|---|']
    for tipo in ETIQUETAS:
        if tipo in VOLUNTARIOS:
            continue
        cantidad = sum(a['minutos'] for a in requeridas(ficha) if a['tipo'] == tipo)
        if cantidad:
            l.append(f'|{ETIQUETAS[tipo]}|{cantidad}|Actividades de la ruta obligatoria, contabilizadas una vez.|')
    for nombre, minutos in fijos:
        patron = r'^\|' + re.escape(nombre) + r'\|' + str(minutos) + r'\|[^\n]*\|$'
        fila_original = re.search(patron, original, re.M)
        if not fila_original:
            raise ValueError(f'D{dia:02}: no se encontró el bloque original completo de {nombre}')
        l.append(fila_original.group())
    l += [f'|**Total BASE**|**{base}**|Carga pendiente; actividades voluntarias separadas.|', '', '## Comprobar y entregar', '',
          'Conserva cada entrega y su comprobación en tu espacio personal. Usa los correctores originales indicados por cada enunciado, '
          'sin consultar soluciones antes del intento. Registra errores, ayuda utilizada y obligaciones pendientes.', '']
    l += [x for x in cierre_previo.splitlines() if CASILLA.match(x) and not id_linea(x)]
    l += ['', seccion_original(original, 'Empleo y clase'), '',
          '## Registro de progreso', '',
          f'Registra modalidad, minutos reales, entregas y siguiente paso en `mi_trabajo/progreso.csv` y `mi_trabajo/dias/D{dia:02}.md`. '
          'Marca únicamente el trabajo realmente realizado. UAGRM y la evaluación final privada se contabilizan aparte.', '',
          '<!-- ruta:integral:fin -->', '']
    publicadas = set('\n'.join(l).splitlines())
    notas = [(i, linea) for i, linea in notas_personales(ctx, ruta, original) if linea not in publicadas]
    if notas:
        l += ['## Notas personales conservadas', '']
        for identidad, linea in notas:
            if identidad:
                l.append(f'**Actividad asociada: {identidad}.**')
            l += [linea, '']
    return firmar('\n'.join(l))


def deduplicar_editorial(texto):
    """Mantiene una casilla por identidad, heredando cualquier marca existente."""
    estados, _ = estados_existentes(texto)
    accionables = {numero for numero, _ in lineas_accionables(texto)}
    vistos, salida = set(), []
    for numero, linea in enumerate(texto.splitlines()):
        if numero in accionables:
            identidad = id_linea(linea)
            if identidad:
                if identidad in vistos:
                    continue
                vistos.add(identidad)
                if estados.get(identidad):
                    linea = re.sub(r'^- \[[ xX]\]', '- [x]', linea)
        salida.append(linea)
    return '\n'.join(salida) + '\n'


def validar_orden_publicado(ficha, texto, dia):
    actividades = ficha['ruta_integral']
    esperado = [a['id'] for a in actividades if a['tipo'] not in VOLUNTARIOS or historial(a)]
    esperado += [a['id'] for a in actividades if a['tipo'] == 'refuerzo' and not historial(a)]
    esperado += [a['id'] for a in actividades if a['tipo'] == 'extendida' and not historial(a)]
    actual = [id_linea(linea) for _, linea in lineas_accionables(texto) if id_linea(linea)]
    if actual != esperado:
        raise ValueError(f'D{dia:02}: el orden de las casillas publicadas difiere de la ruta obligatoria y las categorías')


def renderizar_editorial(ctx, dia, ficha, cal, original):
    texto = deduplicar_editorial(original)
    # Trasladar una lectura antes del examen no cambia el examen ni sus criterios.
    if dia == 13 and '11.3' not in ficha.get('lecciones', []):
        if re.search(r'^- \[[xX]\] \[11\.[13]', texto, re.M):
            raise ValueError('D13: una lectura trasladada tiene progreso real; conserva esa evidencia antes de trasladar su registro')
        texto = re.sub(r'^- \[[ xX]\] \[11\.3[^\n]*\n', '', texto, flags=re.M)
        texto = re.sub(r'^- \[[ xX]\] Predice el resultado de un ejemplo[^\n]*\n', '', texto, flags=re.M)
        texto = re.sub(r'^\|Lecciones\|25\|[^\n]*\n', '', texto, flags=re.M)
        destino = ctx.lecciones['lecciones']['11.3'].get('dia', 5)
        texto = re.sub(r'^## Qué estudiar[^\n]*', '## Preparación ya realizada', texto, count=1, flags=re.M)
        texto = texto.replace('**Se aprende hoy** (no se exige al entrar): Media, mediana y moda.',
                              f'Media, mediana y moda se estudian en D{destino:02}; hoy no hay enseñanza nueva antes del examen.')
        texto = re.sub(r'^Consulta: \[11_Estadistica_descriptiva\][^\n]*',
                       f'La lectura 11.3 se trasladó a D{destino:02}. Esta referencia es informativa; no repitas esa entrega aquí.', texto, flags=re.M)
        texto = texto.replace('COMPLETO 200 min', 'COMPLETO 175 min')
        texto = re.sub(r'^### OBLIGATORIO[^\n]*',
                       '### OBLIGATORIO · examen, corrección y simulacro: 115 min', texto, count=1, flags=re.M)
        texto = texto.replace(' Lo que aparece en el bloque «Lecciones» y en los ejercicios de hoy se aprende hoy: no se exige al entrar.', '')
        # La lección 11.1 ya es obligatoria en D05; no se ofrece de nuevo como
        # tarea voluntaria. La referencia deja visible el traslado.
        texto = re.sub(r'^- \[[ xX]\] \[11\.1[^\n]*\n', '', texto, flags=re.M)
        referencia = 'La lección 11.1 está programada como NÚCLEO en D05; aquí solo se referencia y no tiene otra casilla.'
        if referencia not in texto:
            texto = texto.replace('## Preparación ya realizada\n', '## Preparación ya realizada\n\n' + referencia + '\n', 1)
        # Las lecturas de recuperación son REFUERZO; no se presentan como una
        # segunda clase de actividad en EXTENDIDA.
        lectura = re.search(r'^- \[[ xX]\] \[8\.7[^\n]*', texto, re.M)
        if lectura:
            linea = lectura.group()
            texto = re.sub(r'^- \[[ xX]\] \[8\.7[^\n]*\n?', '', texto, flags=re.M)
            cabecera = re.search(r'^### REFUERZO[^\n]*\n', texto, re.M)
            if cabecera:
                texto = texto[:cabecera.end()] + '\n' + linea + '\n\n' + texto[cabecera.end():].lstrip('\n')
        extendida = re.search(r'^## EXTENDIDA[^\n]*\n.*?(?=^## |\Z)', texto, re.M | re.S)
        if extendida and not list(lineas_accionables(extendida.group())):
            texto = texto[:extendida.start()] + '## EXTENDIDA\n\nSin tareas adicionales asignadas.\n\n' + texto[extendida.end():]
    texto = texto.replace('que pasa a REFUERZO', 'que conserva la condición de OBLIGATORIO PENDIENTE')
    texto = texto.replace('lo que falte lo medirá el examen y se recupera con su REFUERZO.',
                          'completa las obligaciones pendientes antes del examen.')
    texto = texto.replace('Si algún punto no se cumple, haz primero el REFUERZO de esa jornada anterior en lugar del OBLIGATORIO de hoy.',
                          'Si algún punto no se cumple, recupera primero esa base; la evaluación conserva la condición de OBLIGATORIO PENDIENTE.')
    texto = texto.replace('La corrección (25 min) y el simulacro (30 min) se hacen en el siguiente bloque disponible, sin sumar horas.',
                          'La corrección (25 min) y el simulacro (30 min) conservan la condición de OBLIGATORIO PENDIENTE; reserva sus 55 min en sesiones posteriores.')
    texto = texto.replace('60 minutos: haz solo la evaluación del examen (S02), de 60 minutos, sin consultar nada.',
                          '60 minutos: haz la evaluación de S02 con las reglas y consultas permitidas en su contrato original.')
    if dia == 13:
        tabla_sesiones = ('## Sesiones retomables\n\n'
                          '|Sesión|Minutos|Referencia sin casilla adicional|\n|---|---:|---|\n'
                          '|Examen|60|S02 íntegro, según su contrato original.|\n'
                          '|Corrección|25|Corrección del mismo examen.|\n'
                          '|Simulacro|30|Simulacro semanal 02.|\n'
                          '|Hito|20|H02, la única casilla existente del hito.|\n'
                          '|Postulaciones|30|Bloque laboral original.|\n'
                          '|Cierre|10|Registro y comprobación final.|\n\n')
        texto = re.sub(r'^## Sesiones retomables\n.*?(?=^## |\Z)', '', texto, flags=re.M | re.S)
        texto = texto.replace('## Comprobar y entregar', tabla_sesiones + '## Comprobar y entregar', 1)
    distribucion = seccion_original(texto, 'Distribución neta')
    total = sum(int(m) for m in re.findall(r'^\|[^|\n]+\|(\d+)\|', distribucion, re.M))
    texto = re.sub(r'^<!-- base_min:\d+ -->\n?', '', texto, flags=re.M)
    primera, resto = texto.split('\n', 1)
    texto = primera + f'\n\n<!-- base_min:{total} -->\n\n' + resto.lstrip('\n')
    return texto


def generar_seleccion(ctx, dias, comprobar=False):
    if not dias or len(dias) != len(set(dias)):
        raise ValueError('Indica jornadas distintas con --dias.')
    aprobados = set(ctx.nucleo.get('correccion_integral', {}).get('alcance_autorizado', []))
    if set(dias) - aprobados:
        raise ValueError(f'Jornadas fuera de la muestra autorizada: {sorted(set(dias) - aprobados)}')
    if set(dias) & PROTEGIDOS:
        raise ValueError('D01–D03 están protegidos byte a byte.')
    protegidos = {p: p.read_bytes() for n in PROTEGIDOS for p in (ctx.raiz / '01_PLAN_DIARIO/dias').glob(f'D{n:02}_*.md')}
    pendientes = []
    for dia in sorted(dias):
        validar_ruta(ctx, dia)
        ficha = ctx.nucleo['dias'][str(dia)]
        cal = next(d for d in ctx.calendario if d['dia'] == dia)
        ruta = next((ctx.raiz / '01_PLAN_DIARIO/dias').glob(f'D{dia:02}_*.md'))
        anterior = ruta.read_bytes()
        original = anterior.decode('utf-8').replace('\r\n', '\n')
        if ficha.get('modo_integral') == 'editorial':
            nuevo = renderizar_editorial(ctx, dia, ficha, cal, original)
        else:
            nuevo = renderizar_guia(ctx, dia, ficha, cal, original, ruta)
            validar_orden_publicado(ficha, nuevo, dia)
        nl = '\r\n' if b'\r\n' in anterior else '\n'
        pendientes.append((ruta, anterior, nuevo.replace('\n', nl).encode('utf-8')))
    if not comprobar:
        # Validar toda la selección antes de escribir la primera guía.
        if any(p.read_bytes() != antes for p, antes, _ in pendientes):
            raise RuntimeError('Una guía cambió durante la preparación; no se escribió la muestra.')
        for ruta, anterior, nuevo in pendientes:
            if nuevo != anterior:
                ruta.write_bytes(nuevo)
        if any(p.read_bytes() != contenido for p, contenido in protegidos.items()):
            raise RuntimeError('Cambió una jornada histórica protegida.')
    print(('COMPROBADO' if comprobar else 'MUESTRA GENERADA') + ': ' + ', '.join(f'D{d:02}' for d in sorted(dias)) +
          '. D01–D03 y las salidas globales se conservan.')
