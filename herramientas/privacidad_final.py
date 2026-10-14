"""Publicación de controles de la evaluación final sin respuestas ni diagnósticos privados."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import logging
from pathlib import Path
import re
import sys


MENSAJE_RESERVADO = 'Falló un control de la evaluación final; detalle reservado.'
ESTADOS = {'OK', 'ERROR', 'OMITIDA'}
NOMBRES_CONTROLES = {
    'referencia privada no disponible', 'referencia privada', 'segunda ejecución sin cambios',
    'validador fila por fila', 'columna_ausente', 'catalogo_duplicado', 'clave_en_conflicto',
    'duplicado_exacto_descartado', 'cantidad_fraccionaria_rechazada', 'salida_previa_preservada',
    'salidas, errores, registros y artefactos ficticios', 'evidencia pública',
    'archivos reservados', 'documentos finales',
}
PROHIBIDOS = {
    'referencia_final.py', 'generar_final.py', 'verdad_silver.csv', 'verdad_gold.csv',
    'verdad_escalares.json', 'silver_final_esperada.csv', 'controles_final.json',
}
EXCLUIR = {'.git', '.venv', '__pycache__', 'mi_trabajo'}


class FalloPrivado(AssertionError):
    """Un fallo cuyo detalle original permanece en memoria y nunca se publica."""


def ejecutar_privado(fn):
    """Descarta stdout, stderr y logging; no encadena excepciones que puedan contener respuestas."""
    nivel_anterior = logging.root.manager.disable
    try:
        logging.disable(sys.maxsize)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            try:
                return fn()
            except (Exception, SystemExit):
                raise FalloPrivado(MENSAJE_RESERVADO) from None
    finally:
        logging.disable(nivel_anterior)


def controles_publicos(nombres, estado='OK'):
    if not isinstance(estado, str) or estado not in ESTADOS:
        raise ValueError('Estado de control no permitido')
    if any(not isinstance(n, str) or n not in NOMBRES_CONTROLES for n in nombres):
        raise ValueError('Nombre de control no permitido')
    return {'estado': estado, 'controles': [{'nombre': n, 'estado': estado} for n in nombres]}


def registrar_prueba(nombre, fn, privado=False):
    """Convierte un control en registro público, incluidos fallos y omisiones reales."""
    try:
        evidencia = ejecutar_privado(fn) if privado else fn()
        estado = evidencia.get('estado', 'OK') if isinstance(evidencia, dict) else 'OK'
        if not isinstance(estado, str) or estado not in ESTADOS:
            raise ValueError('Estado de prueba no permitido')
        return {'prueba': nombre, 'estado': estado, 'evidencia': evidencia}
    except Exception as exc:
        if privado:
            return {'prueba': nombre, 'estado': 'ERROR', 'detalle': MENSAJE_RESERVADO}
        return {'prueba': nombre, 'estado': 'ERROR', 'tipo': type(exc).__name__, 'detalle': str(exc)}


def _controles_seguros(evidencia):
    if not isinstance(evidencia, dict) or set(evidencia) != {'estado', 'controles'}:
        return False
    if not isinstance(evidencia['estado'], str) or evidencia['estado'] not in ESTADOS or not isinstance(evidencia['controles'], list):
        return False
    return all(isinstance(c, dict) and set(c) == {'nombre', 'estado'}
               and isinstance(c['nombre'], str) and c['nombre'] in NOMBRES_CONTROLES
               and isinstance(c['estado'], str) and c['estado'] in ESTADOS
               for c in evidencia['controles'])


def problemas_evidencia_final(reporte):
    """Valida el esquema público. Los mensajes no incluyen ni claves ni valores recibidos."""
    problemas = []
    if not isinstance(reporte, dict) or not isinstance(reporte.get('pruebas'), list):
        return ['informe de pruebas con estructura no válida']
    for prueba in reporte['pruebas']:
        if not isinstance(prueba, dict):
            problemas.append('entrada de prueba con estructura no válida')
            continue
        evidencia = prueba.get('evidencia', {})
        nombre = prueba.get('prueba', '')
        if isinstance(nombre, str) and nombre.startswith('Validadores:') and prueba.get('estado') == 'ERROR':
            if set(prueba) != {'prueba', 'estado', 'detalle'} or prueba.get('detalle') != MENSAJE_RESERVADO:
                problemas.append('el informe publica un diagnóstico privado de las mutaciones')
        # El informe histórico 5.1 conserva únicamente el texto de omisión.
        if isinstance(evidencia, dict) and 'final' in evidencia:
            antigua = evidencia['final']
            if not (isinstance(antigua, str) and antigua.lower().startswith('omitid')):
                problemas.append('el informe publica resultados reservados del final')
        if isinstance(nombre, str) and ('Evaluación final:' in nombre or 'Pruebas adversas del final' in nombre):
            estado = prueba.get('estado')
            if estado == 'ERROR':
                if set(prueba) != {'prueba', 'estado', 'detalle'} or prueba.get('detalle') != MENSAJE_RESERVADO:
                    problemas.append('el informe publica un diagnóstico privado del final')
            elif set(prueba) != {'prueba', 'estado', 'evidencia'}:
                problemas.append('el registro del final contiene campos no publicables')
            elif not isinstance(estado, str) or estado not in {'OK', 'OMITIDA'} or not _controles_seguros(evidencia):
                problemas.append('la evidencia del final debe contener solo controles y estados')
            elif estado != evidencia['estado']:
                problemas.append('el estado del final no coincide con su evidencia')
        if isinstance(evidencia, dict) and isinstance(evidencia.get('pruebas'), dict):
            final = evidencia['pruebas'].get('Evaluación final', [])
            if not isinstance(final, list) or any(not isinstance(p, dict) or set(p) != {'prueba', 'resultado'}
                                                 for p in final):
                problemas.append('las mutaciones del final publican detalles reservados')
    return problemas


def _json_final_fuera_informe(datos):
    if isinstance(datos, dict):
        if 'final' in datos and not (isinstance(datos['final'], str) and datos['final'].lower().startswith('omitid')):
            return True
        if isinstance(datos.get('prueba'), str) and ('Evaluación final:' in datos['prueba'] or 'Pruebas adversas del final' in datos['prueba']):
            return bool(problemas_evidencia_final({'pruebas': [datos]}))
        return any(_json_final_fuera_informe(v) for v in datos.values())
    return isinstance(datos, list) and any(_json_final_fuera_informe(v) for v in datos)


def problemas_texto_final(texto):
    """Detecta publicaciones etiquetadas de controles sin almacenar sus valores esperados."""
    patron = (r'(?i)\b(?:bronze|silver|gold(?:_filas)?|rechazados|duplicados_exactos|documentos|ventas(?:_centavos|_bs)?)'
              r'\s*(?:(?:esperad[oa]s?|total(?:es)?|de control)\s*)?[:=]\s*[\d]')
    return ['un documento del final publica una cifra de control'] if re.search(patron, texto) else []


def auditar_artefactos(raiz, reporte=None):
    """Inspecciona artefactos publicables; evita el trabajo del alumno y la custodia externa."""
    raiz = Path(raiz)
    problemas = []
    for p in raiz.rglob('*'):
        rel = p.relative_to(raiz)
        if EXCLUIR & set(rel.parts) or not p.is_file():
            continue
        if p.name in PROHIBIDOS:
            problemas.append('el paquete contiene un archivo reservado de la custodia')
        if rel.parts[0] == '10_VALIDACION' and 'final' in p.stem.casefold() and p.suffix.casefold() in {'.json', '.txt', '.log', '.csv', '.db', '.sqlite'}:
            problemas.append('el paquete contiene un artefacto de salida privado del final')
    validacion = raiz / '10_VALIDACION'
    for p in validacion.rglob('*.json'):
        # El informe que se está generando sustituye al anterior; no se audita una copia obsoleta.
        if reporte is not None and p.name == 'resultados_pruebas.json':
            continue
        try:
            datos = json.loads(p.read_text(encoding='utf-8'))
        except (ValueError, OSError):
            problemas.append('un informe público no se puede verificar')
        else:
            if isinstance(datos, dict) and isinstance(datos.get('pruebas'), list):
                problemas.extend(problemas_evidencia_final(datos))
            elif _json_final_fuera_informe(datos):
                problemas.append('un artefacto JSON publica evidencia reservada del final')
    for p in validacion.rglob('*'):
        if p.is_file() and p.suffix.casefold() in {'.log', '.txt'}:
            texto = p.read_text(encoding='utf-8', errors='replace')
            if re.search(r'(?i)(?:evaluaci[oó]n final|evidencia[./ ]+final|referencia_final).*?(?:ventas|silver|bronze|documentos|gold_filas|[0-9]{4,})', texto):
                problemas.append('un registro de texto publica evidencia reservada del final')
    if reporte is not None:
        problemas.extend(problemas_evidencia_final(reporte))
    carpeta = raiz / '09_EVALUACION_FINAL'
    for rel in ('ENUNCIADO.md', 'RUBRICA.md', 'datos/DICCIONARIO.md'):
        p = carpeta / rel
        if p.exists():
            problemas.extend(problemas_texto_final(p.read_text(encoding='utf-8')))
    return problemas
