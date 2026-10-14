"""Verifica la integración pedagógica de la Etapa 2: lecciones, jornadas, prerrequisitos, criterio analítico, hitos de comprensión y horas.

Uso desde la raíz:
    python herramientas/verificar_etapa2.py            # ejecuta todos los grupos y vuelve a ejecutar las cifras de control
    python herramientas/verificar_etapa2.py --raiz R   # sobre una copia del paquete (sin .git se omiten las comparaciones con git)

Sale con código 1 si algún grupo falla. Los avisos (razón por jornada o por semana) no son fallos: indican dónde usar REDUCIDO.
"""
from pathlib import Path
from contextlib import closing
import argparse
import importlib.util
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def cargar_modulo(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m
    spec.loader.exec_module(m)
    return m


def leer(p):
    return Path(p).read_bytes().decode('utf-8').replace('\r\n', '\n')


class Verificador:
    def __init__(self, raiz):
        self.raiz = Path(raiz)
        self.an = cargar_modulo(HERE / 'aplicar_nucleo.py', 'aplicar_nucleo_e2')
        self.ctx = self.an.Contexto(self.raiz)
        self.avisos = []

    # ------------------------------------------------------------------ 1
    def lecciones(self):
        L = self.ctx.lecciones['lecciones']
        archivos = sorted((self.raiz / '02_TEORIA').glob('[0-9][0-9]_*/*.md'))
        assert len(archivos) == 100 == len(L), (len(archivos), len(L))
        for f in archivos:
            texto = f.read_text(encoding='utf-8')
            i = re.match(r'# (\d+\.\d+) ', texto).group(1)
            assert i in L and L[i]['archivo'] == f.relative_to(self.raiz / '02_TEORIA').as_posix(), i
            assert re.search(r'lectura \d+ \+ práctica \d+', texto), f'{i}: sin minutos'
        conteo = {}
        for i, c in L.items():
            assert c['tipo'] in ('NÚCLEO', 'REFUERZO', 'PROFUNDIZACIÓN'), i
            conteo[c['tipo']] = conteo.get(c['tipo'], 0) + 1
            if c['tipo'] == 'NÚCLEO':
                assert isinstance(c['dia'], int) and 2 <= c['dia'] <= 41 and c['dia'] % 7 != 0, f'{i}: día inválido'
            else:
                assert c['cuando'], f'{i}: falta «cuándo»'
                if c.get('dia_ext') is not None:
                    assert 3 <= c['dia_ext'] <= 41, i
        assert sum(conteo.values()) == 100
        # el puente
        puente = (self.raiz / '02_TEORIA' / self.an.PUENTE_ARCHIVO).read_text(encoding='utf-8')
        for i, p in self.ctx.lecciones['puente'].items():
            assert f'## {p["seccion"][1:]}.' in puente, f'{i}: la sección {p["seccion"]} no existe'
        # los índices de capítulo y INDICE.md dicen lo mismo que lecciones.json
        for f in sorted((self.raiz / '02_TEORIA').glob('[0-9][0-9]_*.md')):
            for m in re.finditer(r'^\| (\d+\.\d+) \|(.*)\|$', leer(f), re.M):
                i = m.group(1)
                tipo = m.group(2).split('|')[-2].strip()
                esperado = self.an_etiqueta(i)
                assert tipo == esperado, f'{f.name} {i}: «{tipo}» y debería decir «{esperado}»'
        return {'lecciones': 100, 'clasificación': conteo, 'lectura_nucleo_min': sum(self.an.info_leccion(self.ctx, i)['lectura'] for i, c in L.items() if c['tipo'] == 'NÚCLEO'),
                'puente_min': sum(p['min'] for p in self.ctx.lecciones['puente'].values())}

    def an_etiqueta(self, i):
        c = self.ctx.lecciones['lecciones'][i]
        if c['tipo'] == 'NÚCLEO':
            return f'núcleo · D{c["dia"]:02}'
        return 'refuerzo' if c['tipo'] == 'REFUERZO' else 'profundización'

    # ------------------------------------------------------------------ 2
    def jornadas(self):
        cal = self.ctx.calendario
        assert len(cal) == 42
        dias = self.ctx.nucleo['dias']
        semanas = {}
        peor = (0, None)
        for d in cal:
            n = d['dia']
            assert sum(m for _, m in d['bloques']) == d['completo'], f'D{n:02}: los bloques no suman el tiempo'
            semanas[d['semana']] = semanas.get(d['semana'], 0) + d['completo']
            if d['completo'] == 0:
                assert d.get('voluntario_min') == list(self.an.DOMINGO_MIN), f'D{n:02}: domingo sin tiempo voluntario'
                continue
            if n in self.an.PROTEGIDOS:
                continue
            s = dias[str(n)]
            bl = {a.strip(): m for a, m in d['bloques']}
            ids = s['lecciones']
            assert d.get('lecciones') == ids, f'D{n:02}: calendario y nucleo difieren en lecciones'
            assert bl.get('Lecciones', 0) == sum(self.an.info_leccion(self.ctx, i)['lectura'] for i in ids), f'D{n:02}: bloque Lecciones'
            crit = (s.get('criterio') or {}).get('min', 0)
            assert bl.get('Criterio', 0) == crit, f'D{n:02}: bloque Criterio'
            assert bl.get('Lecciones', 0) + bl.get('Criterio', 0) <= sum(bl.get(k, 0) for k in self.an.POOL), f'D{n:02}: lecciones y criterio exceden el bloque de aprendizaje'
            assert d['teoria'] == self.an.capitulos_dia(self.ctx, s), f'D{n:02}: capítulos de teoría'
        assert set(semanas.values()) == {900}, semanas
        filas = self.an.metricas(self.ctx)
        sem = self.an.resumen_semanal(self.ctx, filas)
        for f in filas:
            if f['completo'] and f['estimado'] / f['completo'] > 1.40:
                raise AssertionError(f'D{f["dia"]:02}: razón {f["estimado"] / f["completo"]:.2f} por encima de 1,40')
            if f['completo'] and f['estimado'] / f['completo'] > 1.25:
                self.avisos.append(f'D{f["dia"]:02} AJUSTADA ({f["estimado"] / f["completo"]:.2f}): usa REDUCIDO si no cabe')
        for w, x in sem.items():
            r = x['est'] / x['plan']
            assert r <= 1.25, f'semana {w}: razón {r:.2f}'
            if r > 1.10:
                self.avisos.append(f'semana {w} estimada en {x["est"]} min ({r:.2f} del plan)')
            ext_lo = (x['plan'] + x['ext']) / 60
            ext_hi = (x['plan'] + x['ext'] + self.an.DOMINGO_MIN[1]) / 60
            assert 20 <= ext_lo and ext_hi <= 25, f'semana {w}: EXTENDIDA {ext_lo:.1f}–{ext_hi:.1f} h fuera de 20–25 h'
        return {'jornadas': 42, 'minutos_semanales': semanas, 'estimado_base_min': {w: x['est'] for w, x in sem.items()},
                'extendida_h_plan': [round((x['plan'] + x['ext']) / 60, 1) for x in sem.values()]}

    # ------------------------------------------------------------------ 3
    def guias(self):
        carpeta = self.raiz / '01_PLAN_DIARIO' / 'dias'
        dias = self.ctx.nucleo['dias']
        for d in self.ctx.calendario:
            n = d['dia']
            t = leer(next(carpeta.glob(f'D{n:02}_*.md')))
            if n == 1:
                assert 'E2:' not in t and 'Criterio analítico' not in t, 'D01 no debe modificarse'
                continue
            if d['completo'] == 0:
                assert '## Domingo flexible: descanso o recuperación voluntaria' in t and '**0 minutos obligatorios**' in t, f'D{n:02}: domingo'
                assert re.search(r'45 y 120 minutos', t), f'D{n:02}: rango voluntario'
                continue
            if n == 2:
                assert '<!-- E2:LECCIONES:INICIO -->' in t and 'Distinguir nulo de cero y definir cumplimiento con su denominador' in t, 'D02: bloque de lecciones u objetivo'
                for ej in ('S2', 'S7', 'S9', 'P02', 'P03', 'C01'):
                    assert f'/{ej}.md' in t, f'D02: falta {ej}'
                for linea in ('|SQL|25|', '|Teoría|30|', '|Práctica|70|'):
                    assert linea in t, f'D02: cambió el tiempo {linea}'
                for i in (i for i, c in self.ctx.lecciones['lecciones'].items() if c.get('dia') == 2):
                    assert self.an.info_leccion(self.ctx, i)['archivo'] in t
                continue
            s = dias[str(n)]
            assert '## Criterio analítico y comprensión' in t and '## EXTENDIDA (voluntaria' in t, f'D{n:02}: faltan secciones nuevas'
            for i in s['lecciones']:
                info = self.an.info_leccion(self.ctx, i)
                assert info['archivo'] in t and f'lectura {info["lectura"]} min' in t, f'D{n:02}: no enlaza o no da el tiempo de {i}'
            if s['lecciones']:
                assert f'({sum(self.an.info_leccion(self.ctx, i)["lectura"] for i in s["lecciones"])} min de lectura)' in t, f'D{n:02}: total de lectura'
            if s.get('criterio'):
                assert f'/{s["criterio"]["id"]}.md' in t, f'D{n:02}: falta {s["criterio"]["id"]}'
            tabla = re.findall(r'^\|([^|\n]+)\|(\d+)\|', t, re.M)
            assert sum(int(m) for _, m in tabla) == d['completo'], f'D{n:02}: la tabla de la guía no suma {d["completo"]}'
        return {'guías_revisadas': 42, 'D01': 'sin cambios', 'D02': 'solo bloque de lecciones', 'domingos': 'flexibles'}

    # ------------------------------------------------------------------ 4
    def prerrequisitos(self):
        L = self.ctx.lecciones['lecciones']
        conteo = {'núcleo': 0, 'práctica': 0, 'recomendada': 0}
        recomendadas = []
        for i, c in L.items():
            if c['tipo'] != 'NÚCLEO':
                continue
            pre = self.an.prerrequisitos(self.ctx, i)
            for p in pre:
                estado = self.an.estado_prerreq(self.ctx, i, p)
                assert not estado.startswith('FALTA'), f'{i} (D{c["dia"]:02}): prerrequisito {p} {estado}'
                clave = estado.split(' ')[0].rstrip(':')
                conteo[clave] = conteo.get(clave, 0) + 1
                if clave == 'recomendada':
                    recomendadas.append(f'{i}←{p}')
            texto = (self.raiz / '02_TEORIA' / c['archivo']).read_text(encoding='utf-8').splitlines()[2]
            if re.search(r'Prerrequisitos?:\s*\S', texto) and not re.search(r'Prerrequisitos?:\s*(ninguno|nada)', texto, re.I):
                assert pre, f'{i}: prerrequisitos sin analizar ({texto[-120:]})'
        # las coberturas «por ejercicio» deben existir
        for i, c in L.items():
            for ej in (c.get('cobertura') or {}).get('por', []):
                assert ej in self.ctx.lecciones['puente'] or self.an.dia_ejercicio(self.ctx, ej) is not None, f'{i}: cobertura por {ej}, que no es OBLIGATORIO'
        return {'prerrequisitos_por_estado': conteo, 'recomendadas': recomendadas}

    # ------------------------------------------------------------------ 5
    def ejercicios_y_lecciones(self):
        L = self.ctx.lecciones['lecciones']
        citadas = {'REFUERZO': 0}
        dias = self.ctx.nucleo['dias']
        for dia, s in dias.items():
            for x in s['obligatorio'] + s['repaso']:
                i = self.an.norm(x)['id']
                if self.an.tipo(i) not in ('PY', 'SQL', 'DB', 'ME'):
                    continue
                p = self.raiz / '03_EJERCICIOS' / self.an.ruta_ejercicio(i)
                if not p.exists():
                    continue
                t = leer(p)
                cabecera = t.split('## Situación')[0]
                for m in re.finditer(r'[Ll]ecci(?:ón|ones) ([\d.]+(?:(?:,| y) [\d.]+)*)', cabecera + ' ' + '\n'.join(re.findall(r'^2\. \*\*Concepto[^\n]*', t, re.M))):
                    for ref in re.findall(r'\d+\.\d+', m.group(1)):
                        assert ref in L, f'{i}: cita la lección inexistente {ref}'
                        c = L[ref]
                        if c['tipo'] == 'PROFUNDIZACIÓN':
                            raise AssertionError(f'{i} (OBLIGATORIO en D{int(dia):02}) cita {ref}, que es PROFUNDIZACIÓN')
                        if c['tipo'] == 'NÚCLEO' and c['dia'] > int(dia):
                            raise AssertionError(f'{i} (D{int(dia):02}) cita {ref}, que se lee en D{c["dia"]:02}')
                        if c['tipo'] == 'REFUERZO':
                            citadas['REFUERZO'] += 1
        # punteros desactualizados
        for ej in [f'P{n:02}' for n in range(1, 31)]:
            if ej in ('P01', 'P03'):
                continue
            t = leer(self.raiz / '03_EJERCICIOS' / 'Python' / f'{ej}.md')
            assert '(capítulo' not in t.split('## Pistas')[-1], f'{ej}: puntero de capítulo desactualizado'
        p02 = leer(self.raiz / '03_EJERCICIOS/Python/P02.md')
        p07 = leer(self.raiz / '03_EJERCICIOS/Python/P07.md')
        assert 'capítulo 08, ejemplo de cumplimiento' not in p02 and 'lección 7.6' in p02 and 'lección 7.3' in p02, 'P02'
        assert 'capítulo 07, sumar solo entregados' not in p07 and 'lección 7.12' in p07, 'P07'
        for p in sorted((self.raiz / '03_EJERCICIOS/Estadistica').glob('ST0*.md')):
            assert not re.search(r"^\['- \[ \]", leer(p), re.M), f'{p.stem}: criterios impresos como lista de Python'
        return {'citas_a_refuerzo_en_obligatorios': citadas['REFUERZO'], 'P02': 'lecciones 7.3 y 7.6', 'P07': 'lecciones 7.12 y 7.13'}

    # ------------------------------------------------------------------ 6
    def ejecutar_control(self, chk):
        if chk['tipo'] == 'sql':
            with closing(sqlite3.connect(f'file:{self.raiz / chk["db"]}?mode=ro', uri=True)) as c:
                return [list(f) for f in c.execute(chk['sql']).fetchall()]
        r = subprocess.run([sys.executable, '-I', '-c', chk['codigo']], capture_output=True, text=True, encoding='utf-8', cwd=self.raiz,
                           env={'PYTHONIOENCODING': 'utf-8', 'SYSTEMROOT': r'C:\Windows'})
        assert r.returncode == 0, f'{chk["id"]}: {r.stderr[-400:]}'
        return r.stdout.rstrip('\n')

    def actividades(self):
        ctrl = json.loads((self.raiz / '08_SOLUCIONES/controles_analitico.json').read_text(encoding='utf-8'))['controles']
        dias = self.ctx.nucleo['dias']
        ids_dia = {s['criterio']['id']: int(d) for d, s in dias.items() if s.get('criterio')}
        an = sorted(f.stem for f in (self.raiz / '03_EJERCICIOS/Analitico').glob('AN*.md'))
        hs = sorted(f.stem for f in (self.raiz / '03_EJERCICIOS/Comprension').glob('H*.md'))
        assert len(an) == 18 and len(hs) == 8, (an, hs)
        assert set(ids_dia) == set(an) | set(hs), (set(ids_dia) ^ (set(an) | set(hs)))
        puertas = {s['puerta']['id']: int(d) for d, s in dias.items() if s.get('puerta')}
        assert len(puertas) == 8
        L = self.ctx.lecciones['lecciones']
        sql_ctrl = json.loads((self.raiz / '08_SOLUCIONES/controles_sql.json').read_text(encoding='utf-8'))
        prohibidos = set()
        for i, c in sql_ctrl.items():
            if len(c['filas']) == 1 and len(c['filas'][0]) == 1 and isinstance(c['filas'][0][0], (int, float)):
                v = c['filas'][0][0]
                prohibidos |= {str(v), f'{v:,.2f}'.replace(',', '.'), f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')} if abs(v) >= 10000 else set()
        comprobadas = 0
        for i in an + hs:
            carpeta = 'Analitico' if i.startswith('AN') else 'Comprension'
            t = leer(self.raiz / '03_EJERCICIOS' / carpeta / f'{i}.md')
            dia = ids_dia[i]
            if i.startswith('AN'):
                for sec in ('## Situación', '## Qué debes entregar', '## Reglas', '## Pistas', '## Criterios de aceptación'):
                    assert sec in t, f'{i}: falta {sec}'
                assert len(re.findall(r'^- \[ \]', t, re.M)) >= 4, f'{i}: criterios'
                assert len(re.findall(r'^[123]\. ', t.split('## Pistas')[1].split('##')[0], re.M)) == 3, f'{i}: tres pistas'
            else:
                for sec in ('## 1. Explica', '## 2. Predice', '## 3. Resuelve una variante nueva', '## 4. Justifica', '## Cómo se evalúa'):
                    assert sec in t, f'{i}: falta {sec}'
            assert f'D{dia:02}' in t, f'{i}: no dice su jornada'
            assert 'mi_trabajo/' in t and 'controles_analitico.md' in t, f'{i}: ruta de entrega o control'
            # lecciones citadas: NÚCLEO hasta ese día, o refuerzo/profundización declaradas (consulta)
            for ref in re.findall(r'\[(\d+\.\d+) ', t.split('## ')[0] + t.split('\n\n')[2] if len(t.split('\n\n')) > 2 else t):
                assert ref in L, f'{i}: lección inexistente {ref}'
                c = L[ref]
                if c['tipo'] == 'NÚCLEO':
                    assert c['dia'] <= dia, f'{i} (D{dia:02}) cita la lección {ref}, que se lee en D{c["dia"]:02}'
            for v in prohibidos:
                assert v not in t, f'{i}: publica el resultado de un ejercicio ({v})'
            # las cifras de control se vuelven a calcular
            for chk in ctrl[i]['checks']:
                res = self.ejecutar_control(chk)
                esperado = chk['esperado']
                if chk['tipo'] == 'sql':
                    res = json.loads(json.dumps(res))
                assert res == esperado, f'{chk["id"]}: salió {res!r} y el control dice {esperado!r}'
                comprobadas += 1
            for chk in ctrl[i]['checks']:
                if chk.get('enunciado'):
                    assert chk['enunciado'] in t, f'{chk["id"]}: el enunciado del hito no contiene el código controlado'
        # J5 por ruta debe sumar lo que dice el control oficial de J5
        j5 = sql_ctrl['J5']['filas']
        total = sum(f[1] for f in next(c for c in ctrl['AN06']['checks'])['esperado'])
        assert total == len(j5), (total, len(j5))
        # V4 de AN11 = control oficial de V4
        assert [list(f) for f in sql_ctrl['V4']['filas']] == next(c for c in ctrl['AN11']['checks'])['esperado']
        return {'AN': len(an), 'H': len(hs), 'cifras_de_control_recalculadas': comprobadas, 'puertas_con_hito': sorted(puertas)}

    # ------------------------------------------------------------------ 7
    def documentos(self):
        comp = leer(self.raiz / '01_PLAN_DIARIO/COMPETENCIAS.md')
        for h in [f'H0{k}' for k in range(1, 9)]:
            assert h in comp, f'COMPETENCIAS.md no menciona {h}'
        for frase in ('N1', 'criterio analítico', 'RUTAS.md'):
            assert frase.lower() in comp.lower(), f'COMPETENCIAS.md: falta «{frase}»'
        assert 'Los domingos siguen siendo descanso: sin estudio' not in comp, 'COMPETENCIAS.md: regla vieja de domingo'
        plan = leer(self.raiz / '01_PLAN_DIARIO/PLAN_V5.md')
        assert 'EXTENDIDA' in plan and 'RUTAS.md' in plan and '|Domingo |Descanso, 0 min|' not in plan, 'PLAN_V5.md sin modalidades nuevas'
        hitos = leer(self.raiz / '01_PLAN_DIARIO/HITOS_Y_RECUPERACION.md')
        assert 'hito de comprensión' in hitos.lower() and 'Un domingo es descanso.' not in hitos, 'HITOS_Y_RECUPERACION.md'
        rd = leer(self.raiz / 'README.md')
        assert 'RUTAS.md' in rd and 'Analitico' in rd and 'Comprension' in rd, 'README.md'
        uagrm = leer(self.raiz / '02_TEORIA/UAGRM/LEEME.md')
        assert 'Mapa' in uagrm and '7.' in uagrm, 'UAGRM/LEEME.md sin mapa de lecciones'
        for nombre in ('RUTAS.md', 'CARGA_ESTIMADA.md'):
            assert (self.raiz / '01_PLAN_DIARIO' / nombre).exists()
        return {'COMPETENCIAS': 'N1, hitos H01–H08 y domingo flexible', 'PLAN_V5': 'modalidades BASE y EXTENDIDA', 'UAGRM': 'mapa de lecciones'}

    # ------------------------------------------------------------------ 8
    def sincronizacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp) / 'copia'
            for carpeta in ('01_PLAN_DIARIO', '02_TEORIA', '03_EJERCICIOS'):
                shutil.copytree(self.raiz / carpeta, copia / carpeta)
            subprocess.run([sys.executable, str(HERE / 'aplicar_nucleo.py'), '--raiz', str(copia)], check=True, capture_output=True)
            distintos = []
            for p in sorted((self.raiz / '01_PLAN_DIARIO').rglob('*')):
                if p.is_file() and p.suffix in ('.md', '.json', '.csv'):
                    q = copia / p.relative_to(self.raiz)
                    if p.name in ('nucleo.json', 'lecciones.json'):
                        continue
                    if p.read_bytes().replace(b'\r\n', b'\n') != q.read_bytes().replace(b'\r\n', b'\n'):
                        distintos.append(p.relative_to(self.raiz).as_posix())
            for p in sorted((self.raiz / '02_TEORIA').glob('[0-9][0-9]_*.md')):
                if p.read_bytes().replace(b'\r\n', b'\n') != (copia / '02_TEORIA' / p.name).read_bytes().replace(b'\r\n', b'\n'):
                    distintos.append('02_TEORIA/' + p.name)
            assert not distintos, ('No sincronizados con nucleo.json/lecciones.json', distintos)
        return {'resultado': 'guías, calendario, CARGA_ESTIMADA.md, RUTAS.md y los índices de capítulo coinciden con lo que genera aplicar_nucleo.py'}

    def sin_cambios_en_mi_trabajo(self):
        if not (self.raiz / '.git').exists():
            return {'git': 'sin repositorio en esta copia: comparación omitida'}
        r = subprocess.run(['git', 'status', '--porcelain', '--', 'mi_trabajo'], capture_output=True, text=True, encoding='utf-8', cwd=self.raiz)
        assert not r.stdout.strip(), f'mi_trabajo tiene cambios: {r.stdout[:200]}'
        r = subprocess.run(['git', 'diff', '--name-only', '--', '01_PLAN_DIARIO/dias/D01_2026-10-12.md'], capture_output=True, text=True, encoding='utf-8', cwd=self.raiz)
        assert not r.stdout.strip(), 'D01 fue modificado'
        return {'mi_trabajo': 'sin cambios', 'D01': 'sin cambios'}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--raiz', default=str(HERE.parent))
    args = ap.parse_args()
    v = Verificador(args.raiz)
    grupos = [('lecciones clasificadas y sincronizadas con los capítulos', v.lecciones), ('42 jornadas: bloques, horas y semanas', v.jornadas),
              ('guías diarias sincronizadas con las lecciones', v.guias), ('prerrequisitos de las lecciones NÚCLEO', v.prerrequisitos),
              ('ejercicios ↔ lecciones y punteros reparados', v.ejercicios_y_lecciones), ('criterio analítico y hitos de comprensión', v.actividades),
              ('documentos de la ruta', v.documentos), ('generador sincronizado (copia temporal)', v.sincronizacion),
              ('D01 y mi_trabajo intactos', v.sin_cambios_en_mi_trabajo)]
    fallos = 0
    for nombre, fn in grupos:
        try:
            r = fn()
            print(f'OK    {nombre}: {json.dumps(r, ensure_ascii=False)[:420]}')
        except Exception as e:  # noqa: BLE001
            fallos += 1
            print(f'ERROR {nombre}: {type(e).__name__}: {e}')
    for a in v.avisos:
        print('AVISO ', a)
    print(f'{len(grupos) - fallos} de {len(grupos)} grupos OK')
    if fallos:
        raise SystemExit(1)


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
