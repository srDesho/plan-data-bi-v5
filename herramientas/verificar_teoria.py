"""Verifica la teoría (02_TEORIA): ejecuta los ejemplos, compara con lo que muestran las lecciones y revisa el formato.

Convención de los bloques de código en las lecciones:
  ```sql       …``` + ```resultado …```   se ejecuta sobre una COPIA de 04_DATASETS/mini_base/mini_base.db y se compara el resultado
  ```python    …``` + ```salida …```      se ejecuta (carpeta temporal con copia de mini_base) y se compara lo impreso
  ```python    …``` + ```error …```       debe fallar; se compara la última línea del error (p. ej. KeyError: 'monto')
  ```sql / ```python sin bloque de salida  se ejecuta y solo se exige que no falle
  ```py / ```sqlplantilla / ```traceback / ```texto   no se ejecutan (fragmentos, plantillas o salidas mostradas)

Uso desde la raíz:
  python herramientas/verificar_teoria.py               # verifica todo (código de salida 0 si todo pasa)
  python herramientas/verificar_teoria.py --rellenar    # reescribe los bloques de salida con lo que de verdad imprime el código
  python herramientas/verificar_teoria.py --archivo 02_TEORIA/07_Python_basico   # limita a archivos cuya ruta contenga el texto
"""
from contextlib import closing, redirect_stdout
from pathlib import Path
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TEO = ROOT / '02_TEORIA'
MINI = ROOT / '04_DATASETS' / 'mini_base'
sys.dont_write_bytecode = True

FENCE = re.compile(r'^```([^\n`]*)\n(.*?)^```[ \t]*$', re.S | re.M)
SALIDAS = {'resultado', 'salida', 'error'}
REQUERIDOS = [('Para qué sirve', r'^## .*para qu[eé] sirve'), ('Términos', r'^## .*t[eé]rminos'), ('Ejemplo', r'^## .*ejemplo'),
              ('Errores', r'^## .*errores'), ('Para comprobar', r'^## .*para comprobar'),
              ('Micropráctica', r'^## .*micropr[aá]ctica'), ('Ejercicios', r'^## .*ejercicios')]

# término -> (expresión, capítulo desde el cual se controla). El primer apartado donde aparece debe definirlo en **negrita**.
TERMINOS = {
    'variable': (r'variables?', 7), 'mutable': (r'(in)?mutables?', 7), 'secuencia': (r'secuencias?', 7),
    'iteración': (r'iteraci[óo]n(es)?', 7), 'acumulador': (r'acumuladore?s?', 7), 'argumento': (r'argumentos?', 7),
    'parámetro': (r'par[áa]metros?', 7), 'retorno': (r'retorno', 7), 'bucle': (r'bucles?', 7),
    'diccionario': (r'diccionarios?', 7), 'lista por comprensión': (r'listas? por comprensi[óo]n', 7), 'expresión regular': (r'expresi[óo]n(es)? regulares?', 1), 'tupla': (r'tuplas?', 7), 'excepción': (r'excepci[óo]n(es)?', 7),
    'traceback': (r'tracebacks?', 7), 'granularidad': (r'granularidad', 1), 'cardinalidad': (r'cardinalidad', 1),
    'DataFrame': (r'DataFrames?', 1), 'varianza': (r'varianza', 1), 'hipótesis nula': (r'hip[óo]tesis nula', 1),
    'contexto de filtro': (r'contexto de filtro', 1), 'clave primaria': (r'clave primaria', 1), 'clave foránea': (r'clave for[áa]nea', 1),
    'NULL': (r'NULL', 1), 'subconsulta': (r'subconsultas?', 1), 'CTE': (r'CTEs?', 1), 'p-valor': (r'p-valor', 1),
    'nivel de significancia': (r'nivel de significancia', 1), 'intervalo de confianza': (r'intervalos? de confianza', 1),
    'desviación estándar': (r'desviaci[óo]n est[áa]ndar', 1), 'percentil': (r'percentil(es)?', 1), 'cuartil': (r'cuartil(es)?', 1),
    'idempotencia': (r'idempoten\w+', 1), 'esquema estrella': (r'esquema estrella', 1), 'tabla de hechos': (r'tablas? de hechos', 1),
    'medida': (r'medidas?', 14), 'outlier': (r'outliers?|at[íi]picos?', 1), 'z-score': (r'z-score|puntaje z', 1),
    'correlación': (r'correlaci[óo]n', 1), 'población': (r'poblaci[óo]n', 1), 'muestra': (r'muestras|muestra (aleatoria|estad[íi]stica|representativa)|tamaño de (la )?muestra', 1),
    'DataFrame': (r'DataFrames?', 1), 'agregación': (r'funci[óo]n(es)? (de )?agregaci[óo]n|funciones agregadas?', 1), 'clave': (r'claves?', 1),
}

# Cadenas que publicaron resultados de ejercicios en la versión anterior de la teoría (no deben volver).
PROHIBIDAS = [r'426[,.]76', r'214[,.]125', r'555[,.]75', r'341[,.]625', r'1[,.]7697', r'1\.468\.924', r'300\.922', r'\b8[,.]81\b',
              r'218[,.]33', r'267[,.]23', r'216[,.]73', r'\b141 (outliers|at[íi]picos)', r'A=41']


# ---------------------------------------------------------------- utilidades
def leer(p):
    return Path(p).read_text(encoding='utf-8')


def archivos(filtro=None):
    res = []
    for p in sorted(TEO.rglob('*.md')):
        rel = p.relative_to(ROOT).as_posix()
        if '/UAGRM/' in rel or (filtro and filtro not in rel):
            continue
        res.append(p)
    return res


def es_leccion(p):
    return p.parent != TEO


def clave_orden(p):
    rel = p.relative_to(TEO).as_posix()
    m = re.match(r'(\d{2})_', rel)
    return (int(m.group(1)) if m else 99, 0 if not es_leccion(p) else 1, rel)


def bloques(texto):
    return [(m.start(), m.end(), m.group(1).strip(), m.group(2)) for m in FENCE.finditer(texto)]


def normalizar(s):
    return '\n'.join(l.rstrip() for l in s.strip().splitlines())


def pares(texto):
    """Devuelve [(bloque_codigo, bloque_salida_o_None)] para los bloques ejecutables."""
    bl = bloques(texto)
    res = []
    for i, b in enumerate(bl):
        if b[2] in ('sql', 'python'):
            sig = bl[i + 1] if i + 1 < len(bl) else None
            if sig and sig[2] in SALIDAS and len(texto[b[1]:sig[0]].strip()) <= 400:
                res.append((b, sig))
            else:
                res.append((b, None))
    return res


# ---------------------------------------------------------------- ejecución
def formatear(v):
    return 'NULL' if v is None else str(v)


def ejecutar_sql(codigo):
    with closing(sqlite3.connect(MINI / 'mini_base.db')) as src, closing(sqlite3.connect(':memory:')) as con:
        src.backup(con)
        acumulado, ultimo, cab, filas = '', None, None, None
        for linea in codigo.splitlines(keepends=True):
            acumulado += linea
            if sqlite3.complete_statement(acumulado):
                ultimo = con.execute(acumulado)
                acumulado = ''
                filas = ultimo.fetchall() if ultimo.description else None
                cab = [d[0] for d in ultimo.description] if ultimo.description else None
        if acumulado.strip() and not acumulado.strip().startswith('--'):
            raise ValueError('sentencia SQL sin punto y coma final')
        if ultimo is None or cab is None:
            return 'OK'
        return '\n'.join([' | '.join(cab)] + [' | '.join(formatear(v) for v in f) for f in filas])


def ejecutar_python(codigo):
    """Devuelve (stdout, excepción|None). Trabaja en una carpeta temporal con copia de mini_base."""
    with tempfile.TemporaryDirectory(prefix='teoria_', ignore_cleanup_errors=True) as td:
        destino = Path(td) / '04_DATASETS' / 'mini_base'
        shutil.copytree(MINI, destino)
        antes = set(sys.modules)
        viejo = os.getcwd()
        os.chdir(td)
        sys.path.insert(0, td)
        buf = io.StringIO()
        error = None
        try:
            with redirect_stdout(buf):
                exec(compile(codigo, '<leccion>', 'exec'), {'__name__': '__main__'})
        except BaseException as e:  # noqa: BLE001 - se informa el error esperado o inesperado
            error = e
        finally:
            os.chdir(viejo)
            sys.path.remove(td)
            for n in set(sys.modules) - antes:
                f = getattr(sys.modules[n], '__file__', None)
                if f and str(td) in str(f):
                    del sys.modules[n]
        return buf.getvalue(), error


def evaluar_bloque(lang, codigo, salida):
    """Ejecuta un bloque. Devuelve (texto_real, problema|None). texto_real es lo que debería mostrarse en el bloque de salida."""
    esperado_error = salida is not None and salida[2] == 'error'
    if lang == 'sql':
        try:
            return ejecutar_sql(codigo), None
        except Exception as e:  # noqa: BLE001
            ultima = f'{type(e).__name__}: {e}'
            if esperado_error:
                return ultima, None
            return None, f'SQL falló: {ultima}'
    texto, error = ejecutar_python(codigo)
    if error is not None:
        ultima = f'{type(error).__name__}: {error}'
        if esperado_error:
            return ultima, None
        return None, f'Python falló: {ultima}'
    if esperado_error:
        return None, 'se esperaba un error y el código terminó bien'
    return texto, None


# ---------------------------------------------------------------- comprobaciones
def comprobar_ejemplos(rellenar, filtro):
    problemas, n = [], 0
    for p in archivos(filtro):
        texto = leer(p)
        cambios = []
        for (b, s) in pares(texto):
            n += 1
            lang, codigo = b[2], b[3]
            real, prob = evaluar_bloque(lang, codigo, s)
            where = f'{p.relative_to(ROOT).as_posix()}:{texto[:b[0]].count(chr(10)) + 2}'
            if prob:
                problemas.append(f'{where}: {prob}')
                continue
            if s is None:
                continue
            if s[2] == 'error':
                mostrada = normalizar(s[3]).splitlines()
                if not normalizar(real).splitlines()[-1].startswith(mostrada[-1] if mostrada else 'sin-texto'):
                    if rellenar:
                        cambios.append((s, real))
                    else:
                        problemas.append(f'{where}: el error esperado era «{normalizar(s[3])}» y fue «{normalizar(real)}»')
            elif normalizar(s[3]) != normalizar(real):
                if rellenar:
                    cambios.append((s, real))
                else:
                    problemas.append(f'{where}: la salida mostrada no coincide.\n--- mostrada\n{normalizar(s[3])}\n--- real\n{normalizar(real)}')
        if rellenar and cambios:
            for s, real in sorted(cambios, key=lambda c: -c[0][0]):
                inicio = texto.index('\n', s[0]) + 1
                fin = s[1] - 3
                texto = texto[:inicio] + real.strip('\n') + '\n' + texto[fin:]
            Path(p).write_text(texto, encoding='utf-8', newline='\n')
    return problemas, n


def comprobar_formato(filtro):
    problemas = []
    for p in archivos(filtro):
        if not es_leccion(p):
            continue
        t = leer(p)
        rel = p.relative_to(ROOT).as_posix()
        if not re.search(r'^> .*Tiempo estimado:\s*\d+\s*min', '\n'.join(t.splitlines()[:10]), re.M | re.I):
            problemas.append(f'{rel}: falta la línea «> … Tiempo estimado: N min» al inicio')
        for nombre, patron in REQUERIDOS:
            if not re.search(patron, t, re.M | re.I):
                problemas.append(f'{rel}: falta el apartado «{nombre}»')
        if len(re.findall(r'^```', t, re.M)) % 2:
            problemas.append(f'{rel}: bloque de código sin cerrar')
        if len(t.split()) < 450:
            problemas.append(f'{rel}: muy corta ({len(t.split())} palabras)')
    return problemas


def comprobar_enlaces(filtro):
    problemas = []
    for p in archivos(filtro):
        t = leer(p)
        sin_codigo = FENCE.sub('', t)
        for m in re.finditer(r'\[[^\]]*\]\(([^)\s]+)\)', sin_codigo):
            destino = m.group(1)
            if destino.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            ruta = (p.parent / destino.split('#')[0]).resolve()
            if not ruta.exists():
                problemas.append(f'{p.relative_to(ROOT).as_posix()}: enlace roto → {destino}')
    return problemas


def quitar_codigo(t):
    sin_enlaces = re.sub(r'\[[^\]]*\]\([^)]*\)', ' ', t)
    return re.sub(r'`[^`\n]*`', ' ', FENCE.sub(' ', sin_enlaces))


def comprobar_terminos(filtro):
    """El primer apartado (en orden de lectura) donde aparece un término controlado debe definirlo en negrita."""
    problemas, vistos = [], set()
    for p in sorted(archivos(), key=clave_orden):
        if not es_leccion(p) and not p.name.startswith('19_'):
            continue
        cap = clave_orden(p)[0]
        t = leer(p)
        limpio = quitar_codigo(t)
        for term, (expr, desde) in TERMINOS.items():
            if term in vistos or cap < desde:
                continue
            flags = 0 if term in ('NULL', 'CTE', 'DataFrame') else re.I
            if re.search(rf'(?<![\w-]){expr}(?![\w-])', limpio, flags):
                vistos.add(term)
                negrita = re.search(rf'\*\*[^*\n]*(?<![\w-]){expr}(?![\w-])[^*\n]*\*\*', t, flags)
                if not negrita and (not filtro or filtro in p.relative_to(ROOT).as_posix()):
                    problemas.append(f'{p.relative_to(ROOT).as_posix()}: usa «{term}» antes de definirlo en negrita')
    return problemas


def comprobar_tiempos(filtro):
    """Cada fila de la tabla de un capítulo debe repetir el tiempo de su lección y el total debe ser la suma."""
    problemas = []
    for idx in sorted(TEO.glob('[0-9][0-9]_*.md')):
        carpeta = TEO / idx.stem
        if not carpeta.is_dir() or (filtro and filtro not in idx.relative_to(ROOT).as_posix()):
            continue
        texto = leer(idx)
        suma = 0
        for m in re.finditer(r'^\|[^|]*\|\s*\[[^\]]*\]\(([^)]+\.md)\)[^\n]*\|\s*(\d+) min \|\s*$', texto, re.M):
            leccion = (TEO / m.group(1))
            suma += int(m.group(2))
            if not leccion.exists():
                problemas.append(f'{idx.name}: la tabla enlaza una lección que no existe ({m.group(1)})')
                continue
            h = re.search(r'Tiempo estimado:\s*(\d+)\s*min', leer(leccion))
            if not h or int(h.group(1)) != int(m.group(2)):
                problemas.append(f'{idx.name}: {leccion.name} declara {h.group(1) if h else "?"} min y la tabla {m.group(2)} min')
        tot = re.search(r'unas (?:(\d+) h)? ?(?:(\d+) min)?', texto)
        if suma and tot:
            declarado = int(tot.group(1) or 0) * 60 + int(tot.group(2) or 0)
            if declarado != suma:
                problemas.append(f'{idx.name}: el total dice {declarado} min y la suma de la tabla es {suma} min')
        lecciones_en_disco = len(list(carpeta.glob('*.md')))
        filas = len(re.findall(r'\]\(' + re.escape(idx.stem) + r'/[^)]+\.md\)', texto))
        if lecciones_en_disco != filas:
            problemas.append(f'{idx.name}: hay {lecciones_en_disco} lecciones en la carpeta y {filas} enlaces en el índice')
    return problemas


def comprobar_glosario():
    """Cada término del glosario debe estar definido en negrita en la lección que enlaza."""
    problemas = []
    texto = leer(TEO / 'GLOSARIO.md')
    entradas = re.findall(r'^- \*\*([^*]+)\*\* — .*?\[[^\]]*\]\(([^)]+\.md)\)\s*$', texto, re.M)
    if len(entradas) < 80:
        problemas.append(f'GLOSARIO.md: solo se reconocen {len(entradas)} entradas')
    for termino, ruta in entradas:
        archivo = TEO / ruta
        if not archivo.exists():
            problemas.append(f'GLOSARIO.md: «{termino}» enlaza a un archivo que no existe ({ruta})')
            continue
        base = re.sub(r'\s*\(.*?\)\s*', ' ', termino).replace('`', '').strip().lower()
        negritas = [re.sub(r'[`]', '', b).lower() for b in re.findall(r'\*\*([^*\n]+)\*\*', leer(archivo))]
        if not any(base in b for b in negritas):
            problemas.append(f'GLOSARIO.md: «{termino}» no está definido en negrita en {ruta}')
    return problemas


def valores_prohibidos():
    pats = list(PROHIBIDAS)
    try:
        ctrl = json.loads(leer(ROOT / '08_SOLUCIONES' / 'controles_sql.json'))
        for c in ctrl.values():
            if len(c['filas']) == 1 and len(c['filas'][0]) == 1 and isinstance(c['filas'][0][0], (int, float)) and abs(c['filas'][0][0]) >= 10000:
                v = c['filas'][0][0]
                pats.append(re.escape(f'{v:,.0f}'.replace(',', '.')))
                pats.append(re.escape(f'{v:.2f}'))
    except Exception:  # noqa: BLE001
        pass
    return pats


def comprobar_fugas(filtro):
    problemas = []
    pats = valores_prohibidos()
    soluciones = {}
    for f in (ROOT / '08_SOLUCIONES' / 'sql').glob('*.sql'):
        s = re.sub(r'\s+', ' ', re.sub(r'--[^\n]*', '', leer(f))).strip().rstrip(';').lower()
        if len(s) > 30:
            soluciones[s] = f.stem
    for p in archivos(filtro):
        t = leer(p)
        rel = p.relative_to(ROOT).as_posix()
        for pat in pats:
            if re.search(pat, t):
                problemas.append(f'{rel}: contiene un valor que pertenece a un ejercicio ({pat})')
        for b in bloques(t):
            if b[2] == 'sql':
                s = re.sub(r'\s+', ' ', re.sub(r'--[^\n]*', '', b[3])).strip().rstrip(';').lower()
                if s in soluciones:
                    problemas.append(f'{rel}: un ejemplo SQL coincide con la solución de {soluciones[s]}')
    return problemas


def resumen_tiempos():
    por_cap = {}
    for p in archivos():
        if es_leccion(p):
            m = re.search(r'Tiempo estimado:\s*(\d+)\s*min', leer(p))
            if m:
                por_cap.setdefault(p.parent.name, []).append(int(m.group(1)))
    return por_cap


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    args = sys.argv[1:]
    rellenar = '--rellenar' in args
    filtro = args[args.index('--archivo') + 1] if '--archivo' in args else None
    grupos = []
    pe, n = comprobar_ejemplos(rellenar, filtro)
    grupos.append((f'ejemplos ejecutados ({n} bloques)', pe))
    grupos.append(('formato de lecciones', comprobar_formato(filtro)))
    grupos.append(('enlaces internos', comprobar_enlaces(filtro)))
    grupos.append(('tiempos y lecciones de cada capítulo', comprobar_tiempos(filtro)))
    grupos.append(('términos definidos antes de usarlos', comprobar_terminos(filtro)))
    grupos.append(('glosario enlazado a su definición', comprobar_glosario()))
    grupos.append(('fugas de ejercicios', comprobar_fugas(filtro)))
    ok = True
    for nombre, prob in grupos:
        print(('OK   ' if not prob else 'ERROR'), nombre)
        for x in prob:
            print('      -', x)
        ok = ok and not prob
    tiempos = resumen_tiempos()
    if tiempos:
        print('Tiempo estimado por capítulo (min):', {k: sum(v) for k, v in tiempos.items()})
    palabras = sum(len(leer(p).split()) for p in archivos(filtro))
    print(f'Archivos: {len(archivos(filtro))} · palabras: {palabras}')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
