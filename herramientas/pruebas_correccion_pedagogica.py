"""Pruebas de conservación, duplicados, mutaciones y regeneración en copia.

No modifica el repositorio de trabajo ni consulta respuestas del final privado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from verificar_integridad_pedagogica import actividades, duplicados, guia, verificar, MUESTRA

ROOT = Path(__file__).resolve().parents[1]


def ejecutar(raiz):
    r = subprocess.run([sys.executable, '-B', str(raiz / 'herramientas/aplicar_nucleo.py'),
                        '--raiz', str(raiz), '--dias', ','.join(map(str, sorted(MUESTRA)))],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise AssertionError(r.stdout + r.stderr)
    return r.stdout


def hashes(raiz):
    return {p.relative_to(raiz).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in raiz.rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--salida', type=Path)
    args = ap.parse_args()
    resultados = []

    def registrar(nombre, fn):
        try:
            detalle = fn()
            resultados.append({'prueba': nombre, 'estado': 'OK', 'detalle': detalle})
            print('OK   ' + nombre, flush=True)
        except Exception as exc:
            resultados.append({'prueba': nombre, 'estado': 'ERROR', 'detalle': str(exc)})
            print('ERROR ' + nombre + ': ' + str(exc)[:500], flush=True)

    def parser():
        doble = '- [ ] [SQL J2](../../03_EJERCICIOS/SQL/J2.md)\n- [x] [J2 otra etiqueta](../../03_EJERCICIOS/SQL/J2.md)'
        assert 'J2' in duplicados(doble)
        metadata = '- [ ] **J2** <!-- actividad:J2 -->\n- [x] **J2** <!-- actividad:J2 -->'
        assert 'J2' in duplicados(metadata)
        informativo = '- [ ] [SQL J2](../../03_EJERCICIOS/SQL/J2.md)\nConsulta [J2](../../03_EJERCICIOS/SQL/J2.md)\n```md\n- [ ] [J2](../../03_EJERCICIOS/SQL/J2.md)\n```\n'
        assert not duplicados(informativo)
        fases = '- [ ] C06 extracción <!-- actividad:C06-1 -->\n- [ ] C06 validación <!-- actividad:C06-2 -->'
        assert not duplicados(fases)
        namespaces = '- [ ] [S1](../../03_EJERCICIOS/SQL/S1.md)\n- [ ] [S01](../../03_EJERCICIOS/EXAMENES/S01.md)'
        assert len(actividades(namespaces)) == 2 and not duplicados(namespaces)
        return 'Detecta copias pendientes/completadas, distingue referencias, código, fases y namespaces.'
    registrar('extractor de actividades accionables', parser)

    with tempfile.TemporaryDirectory(prefix='correccion_v5_') as td:
        copia = Path(td) / 'paquete'
        # Incluir incluso cachés personales existentes: la copia debe reflejar
        # todos los archivos protegidos, aunque no sean entradas del curso.
        shutil.copytree(ROOT, copia, ignore=shutil.ignore_patterns('.git', '.venv'))
        proteccion = json.loads((copia / 'docs/auditorias/PROTECCION_BASE_8168909.json').read_text(encoding='utf-8'))
        base = Path(proteccion['backup']) / 'repositorio'
        for dia in MUESTRA:
            shutil.copy2(guia(base, dia), guia(copia, dia))
        # Nota explícita adicional sobre una realización: debe sobrevivir a la migración.
        p4 = guia(copia, 4)
        t = p4.read_text(encoding='utf-8')
        line = next(line for line in t.splitlines() if '- [x] [SQL G2]' in line)
        nota = '> Evidencia personal de G2 (prueba de conservación): explique el filtro sin ayuda.'
        p4.write_text(t.replace(line, line + '\n' + nota, 1), encoding='utf-8')

        def primera():
            ejecutar(copia)
            res = verificar(copia, MUESTRA)
            assert not res['fallos'], [p for p in res['pruebas'] if p['estado'] == 'ERROR']
            assert nota in guia(copia, 4).read_text(encoding='utf-8'), 'Nota personal perdida'
            return {'aserciones': len(res['pruebas']), 'fallos': res['fallos']}
        registrar('primera generación desde guías base con progreso y nota personal', primera)

        def idempotencia():
            antes = hashes(copia)
            ejecutar(copia)
            segunda = hashes(copia)
            ejecutar(copia)
            tercera = hashes(copia)
            cambios1 = [p for p in set(antes) | set(segunda) if antes.get(p) != segunda.get(p)]
            cambios2 = [p for p in set(segunda) | set(tercera) if segunda.get(p) != tercera.get(p)]
            assert not cambios1 and not cambios2, {'segunda': cambios1, 'tercera': cambios2}
            res = verificar(copia, MUESTRA)
            assert not res['fallos'], [p for p in res['pruebas'] if p['estado'] == 'ERROR']
            assert nota in guia(copia, 4).read_text(encoding='utf-8')
            return {'regeneraciones_consecutivas': 2, 'archivos_cambiados': 0, 'aserciones': len(res['pruebas'])}
        registrar('dos regeneraciones consecutivas estables y verificadas', idempotencia)

        def mutar(nombre, ruta, cambio, error_esperado):
            def prueba():
                original = ruta.read_bytes()
                try:
                    ruta.write_text(cambio(original.decode('utf-8')), encoding='utf-8')
                    res = verificar(copia, MUESTRA)
                    errores = [p['prueba'] for p in res['pruebas'] if p['estado'] == 'ERROR']
                    assert any(error_esperado in e for e in errores), errores
                    return {'rechazada': True, 'motivo': error_esperado}
                finally:
                    ruta.write_bytes(original)
            registrar(nombre, prueba)

        def duplicar(t):
            linea = next(linea for linea in t.splitlines() if '<!-- actividad:' in linea and '- [ ]' in linea)
            return t + '\n' + linea + '\n'
        mutar('mutación: duplicación entre categorías', guia(copia, 8), duplicar, 'cero IDs accionables duplicados')
        def desmarcar(t):
            return re.sub(r'^- \[x\]([^\n]*<!-- actividad:G2 -->)', r'- [ ]\1', t, count=1, flags=re.M)
        mutar('mutación: realización G2 desmarcada', guia(copia, 4), desmarcar, 'realizaciones identificables conservadas')
        mutar('mutación: D03 alterado', guia(copia, 3), lambda t: t + '\nCambio prohibido\n', 'jornadas fuera de muestra intactos')
        mutar('mutación: tiempo de guía falseado', guia(copia, 8), lambda t: re.sub(r'base_min:(\d+)', lambda m: 'base_min:' + str(int(m[1]) + 1), t, count=1), 'minutos BASE calculados')

        def degradar(t):
            d = json.loads(t)
            for s in d['dias'].values():
                s['obligatorio'] = [x for x in s.get('obligatorio', []) if (x.get('id') if isinstance(x, dict) else x) != 'G1']
            return json.dumps(d, ensure_ascii=False, indent=2)
        mutar('mutación: obligación histórica G1 degradada', copia / '01_PLAN_DIARIO/nucleo.json', degradar, 'obligaciones históricas restituidas')

        def omitir_micro(t):
            d = json.loads(t)
            ruta = d['dias']['8']['ruta_integral']
            elegida = next(a for a in ruta if a['tipo'] == 'micropractica')
            d['dias']['8']['ruta_integral'] = [a for a in ruta if a['id'] != elegida['id']]
            return json.dumps(d, ensure_ascii=False, indent=2)
        mutar('mutación: micropráctica esencial omitida', copia / '01_PLAN_DIARIO/nucleo.json', omitir_micro, 'micropráctica esencial posterior')

        def mover_fuera_orden(t):
            lineas = t.splitlines()
            posiciones = [i for i, linea in enumerate(lineas) if '<!-- actividad:' in linea and '- [ ]' in linea]
            i, j = posiciones[:2]
            lineas[i], lineas[j] = lineas[j], lineas[i]
            return '\n'.join(lineas) + '\n'
        mutar('mutación: práctica publicada antes de enseñanza', guia(copia, 8), mover_fuera_orden, 'en orden en guía')

        def requisito_voluntario(t):
            d = json.loads(t)
            s = d['dias']['8']
            for a in s['ruta_integral']:
                if a['id'] == 'L:8.1':
                    a['tipo'] = 'refuerzo'
            for ses in s['sesiones_integrales']:
                ses['actividades'] = [x for x in ses['actividades'] if x != 'L:8.1']
            s['sesiones_integrales'] = [ses for ses in s['sesiones_integrales'] if ses['actividades']]
            return json.dumps(d, ensure_ascii=False, indent=2)
        mutar('mutación: requisito esencial relegado a voluntario', copia / '01_PLAN_DIARIO/nucleo.json', requisito_voluntario, 'preparación obligatoria anterior')

        def impedir_requisito_voluntario():
            p = copia / '01_PLAN_DIARIO/nucleo.json'
            original = p.read_bytes()
            try:
                p.write_text(requisito_voluntario(original.decode('utf-8')), encoding='utf-8')
                r = subprocess.run([sys.executable, '-B', str(copia / 'herramientas/aplicar_nucleo.py'), '--raiz', str(copia), '--dias', '8'], capture_output=True, text=True, encoding='utf-8', errors='replace')
                assert r.returncode != 0 and 'voluntar' in (r.stdout + r.stderr).lower(), r.stdout + r.stderr
                return 'El generador rechaza la fuente antes de escribir la guía.'
            finally:
                p.write_bytes(original)
        registrar('generador rechaza requisito esencial voluntario', impedir_requisito_voluntario)

        def proteger_global():
            r = subprocess.run([sys.executable, '-B', str(copia / 'herramientas/aplicar_nucleo.py'), '--raiz', str(copia)], capture_output=True, text=True, encoding='utf-8', errors='replace')
            assert r.returncode != 0 and 'no autorizada' in (r.stdout + r.stderr).lower(), r.stdout + r.stderr
            return 'Se requiere selección explícita; no se genera fuera de muestra.'
        registrar('regeneración global sin aprobación rechazada', proteger_global)

    informe = {'fallos': sum(p['estado'] == 'ERROR' for p in resultados), 'pruebas': resultados,
               'alcance': 'muestra D04,D05,D08-D13; todas las mutaciones y regeneraciones en copia temporal'}
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(bool(informe['fallos']))


if __name__ == '__main__':
    main()
