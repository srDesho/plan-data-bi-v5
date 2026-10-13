"""Regenera 10_VALIDACION/MANIFIESTO_SHA256.json (SHA-256 de cada archivo del paquete).

Excluye el propio manifiesto, `.venv`, `.git`, `__pycache__`, `mi_trabajo` (tu trabajo), `.gitignore` y los informes sueltos de la raíz
(`AUDITORIA_*.md`, `INFORME_*.md`). Uso desde la raíz:  python herramientas/regenerar_manifiesto.py [--comprobar]
`--comprobar` no escribe: lista los archivos cuyo hash difiere del manifiesto (código de salida 1 si hay diferencias).
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / '10_VALIDACION' / 'MANIFIESTO_SHA256.json'
EXCLUIR_DIRS = {'.venv', '.git', '__pycache__', 'mi_trabajo'}


def archivos():
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if EXCLUIR_DIRS & set(rel.parts) or p == DESTINO or rel.as_posix() == '.gitignore':
            continue
        if len(rel.parts) == 1 and rel.name.startswith(('AUDITORIA_', 'INFORME_')):
            continue
        yield rel.as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    actuales = dict(archivos())
    if '--comprobar' in sys.argv:
        previo = json.loads(DESTINO.read_text(encoding='utf-8'))['archivos']
        distintos = sorted(k for k in set(actuales) | set(previo) if actuales.get(k) != previo.get(k))
        print('Manifiesto vigente' if not distintos else f'{len(distintos)} archivos difieren: {distintos[:15]}')
        raise SystemExit(1 if distintos else 0)
    DESTINO.write_text(json.dumps({'algoritmo': 'SHA256', 'excluye': 'el propio manifiesto, mi_trabajo, .gitignore e informes sueltos de la raíz', 'archivos': actuales},
                                  ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Manifiesto escrito: {len(actuales)} archivos')


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
