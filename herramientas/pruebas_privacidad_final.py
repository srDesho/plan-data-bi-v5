"""Regresiones de privacidad con respuestas ficticias; no consulta la custodia ni datos finales."""
import ast
import copy
import io
import json
import logging
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from contextlib import redirect_stderr, redirect_stdout

from privacidad_final import (
    MENSAJE_RESERVADO, auditar_artefactos, controles_publicos, ejecutar_privado,
    problemas_evidencia_final, problemas_texto_final, registrar_prueba,
)

CENTINELA = 'RESPUESTA_FICTICIA_NO_PUBLICABLE_9876543210123'
PRUEBA = 'Evaluación final: referencia privada, segunda ejecución y validador'


def funcion_final_ficticia(antigua=False, falla=False, disponible=True):
    """Ejecuta la función real con dependencias ficticias y sin importar el verificador completo."""
    fuente = Path(__file__).with_name('verificar_paquete.py').read_text(encoding='utf-8')
    funcion = next(n for n in ast.walk(ast.parse(fuente))
                   if isinstance(n, ast.FunctionDef) and n.name == 'final_con_custodia')
    funcion = copy.deepcopy(funcion)
    if antigua:
        # La devolución anterior publicaba directamente el resultado de la referencia.
        funcion.body[-1] = ast.parse("return {'final': first, 'validador': 'validación'}").body[0]

    def referencia(*args):
        print(CENTINELA)
        print(CENTINELA, file=sys.stderr)
        logging.warning(CENTINELA)
        if falla:
            raise ValueError(CENTINELA)
        return {'ventas_centavos': CENTINELA, 'silver': CENTINELA}

    def modulo(ruta, nombre):
        return SimpleNamespace(ejecutar=referencia, validar=lambda salida: CENTINELA)

    scope = {'ROOT': Path('raiz_ficticia'), 'tmp': Path('temporal_ficticio'),
             'Path': Path, 'custodia': lambda: 'custodia_ficticia' if disponible else None,
             'module': modulo, 'controles_publicos': controles_publicos}
    codigo = ast.fix_missing_locations(ast.Module(body=[funcion], type_ignores=[]))
    exec(compile(codigo, '<función final con referencias ficticias>', 'exec'), scope)
    return scope['final_con_custodia']


class PrivacidadFinal(unittest.TestCase):
    def test_devolucion_anterior_expone_y_actual_no(self):
        viejo = registrar_prueba(PRUEBA, funcion_final_ficticia(antigua=True), privado=True)
        actual = registrar_prueba(PRUEBA, funcion_final_ficticia(), privado=True)
        self.assertIn(CENTINELA, json.dumps(viejo))
        self.assertTrue(problemas_evidencia_final({'pruebas': [viejo]}))
        self.assertNotIn(CENTINELA, json.dumps(actual))
        self.assertFalse(problemas_evidencia_final({'pruebas': [actual]}))

    def test_stdout_stderr_logging_preexistente_descartados(self):
        salida, errores, log = io.StringIO(), io.StringIO(), io.StringIO()
        handler = logging.StreamHandler(log)
        logging.root.addHandler(handler)
        nivel = logging.root.manager.disable
        try:
            with redirect_stdout(salida), redirect_stderr(errores):
                registrar_prueba(PRUEBA, funcion_final_ficticia(), privado=True)
        finally:
            logging.root.removeHandler(handler)
        self.assertEqual(salida.getvalue() + errores.getvalue() + log.getvalue(), '')
        self.assertEqual(logging.root.manager.disable, nivel)

    def test_error_publico_sin_mensaje_original_ni_causa(self):
        salida, errores = io.StringIO(), io.StringIO()
        with redirect_stdout(salida), redirect_stderr(errores):
            registro = registrar_prueba(PRUEBA, funcion_final_ficticia(falla=True), privado=True)
        self.assertEqual(registro['estado'], 'ERROR')
        self.assertEqual(registro['detalle'], MENSAJE_RESERVADO)
        self.assertNotIn(CENTINELA, json.dumps(registro) + salida.getvalue() + errores.getvalue())
        self.assertFalse(problemas_evidencia_final({'pruebas': [registro]}))
        try:
            ejecutar_privado(lambda: (_ for _ in ()).throw(ValueError(CENTINELA)))
        except AssertionError as exc:
            self.assertTrue(exc.__suppress_context__)
            self.assertIsNone(exc.__cause__)
            self.assertNotIn(CENTINELA, str(exc))
        else:
            self.fail('Se aceptó un control privado fallido')

    def test_omision_es_estado_externo_real(self):
        registro = registrar_prueba(PRUEBA, funcion_final_ficticia(disponible=False), privado=True)
        self.assertEqual(registro['estado'], 'OMITIDA')
        self.assertFalse(problemas_evidencia_final({'pruebas': [registro]}))

    def test_artifacto_json_con_metricas_reservadas_se_rechaza_sin_eco(self):
        with tempfile.TemporaryDirectory(prefix='privacidad_ficticia_') as temporal:
            raiz = Path(temporal)
            carpeta = raiz / '10_VALIDACION'
            carpeta.mkdir()
            viejo = {'pruebas': [{'prueba': PRUEBA, 'estado': 'OK',
                                 'evidencia': {'final': {'ventas_centavos': CENTINELA}}}]}
            (carpeta / 'resultados_pruebas.json').write_text(json.dumps(viejo), encoding='utf-8')
            problemas = auditar_artefactos(raiz)
            self.assertTrue(problemas)
            self.assertNotIn(CENTINELA, ' '.join(problemas))
            actual = {'pruebas': [registrar_prueba(PRUEBA, funcion_final_ficticia(), privado=True)]}
            self.assertFalse(auditar_artefactos(raiz, reporte=actual))

    def test_log_y_archivo_privado_se_rechazan_sin_eco(self):
        with tempfile.TemporaryDirectory(prefix='privacidad_ficticia_') as temporal:
            raiz = Path(temporal)
            carpeta = raiz / '10_VALIDACION'
            carpeta.mkdir()
            (carpeta / 'final_stdout.log').write_text(CENTINELA, encoding='utf-8')
            (raiz / 'verdad_gold.csv').write_text(CENTINELA, encoding='utf-8')
            problemas = auditar_artefactos(raiz)
            self.assertEqual(len(problemas), 2)
            self.assertNotIn(CENTINELA, ' '.join(problemas))

    def test_documento_con_cifra_etiquetada_sin_lista_de_respuestas(self):
        problemas = problemas_texto_final('ventas_centavos = 9876543210123')
        self.assertTrue(problemas)
        self.assertNotIn('9876543210123', ' '.join(problemas))
        self.assertFalse(problemas_texto_final('monto_centavos = cantidad × precio; umbral de rúbrica: 80'))

    def test_rechaza_detalle_privado_en_mutaciones_y_errores(self):
        informe = {'pruebas': [{'prueba': 'Validadores: referencias', 'estado': 'OK', 'evidencia': {
            'pruebas': {'Evaluación final': [{'prueba': 'mutación ficticia', 'resultado': 'rechazada', 'detalle': CENTINELA}]}}}]}
        self.assertTrue(problemas_evidencia_final(informe))
        error = {'pruebas': [{'prueba': PRUEBA, 'estado': 'ERROR', 'detalle': CENTINELA}]}
        self.assertTrue(problemas_evidencia_final(error))

    def test_nombre_de_control_no_admite_resultados_arbitrarios(self):
        registro = {'prueba': PRUEBA, 'estado': 'OK', 'evidencia': {
            'estado': 'OK', 'controles': [{'nombre': 'ventas=' + CENTINELA, 'estado': 'OK'}]}}
        problemas = problemas_evidencia_final({'pruebas': [registro]})
        self.assertTrue(problemas)
        self.assertNotIn(CENTINELA, ' '.join(problemas))

    def test_registro_exitoso_no_admite_detalle_adicional(self):
        registro = registrar_prueba(PRUEBA, funcion_final_ficticia(), privado=True)
        registro['detalle'] = CENTINELA
        self.assertTrue(problemas_evidencia_final({'pruebas': [registro]}))

    def test_estado_privado_arbitrario_no_se_publica(self):
        registro = registrar_prueba(PRUEBA, lambda: {'estado': CENTINELA}, privado=True)
        self.assertEqual(registro['estado'], 'ERROR')
        self.assertNotIn(CENTINELA, json.dumps(registro))

    def test_artifactos_adicionales_json_y_texto_se_detectan(self):
        with tempfile.TemporaryDirectory(prefix='privacidad_ficticia_') as temporal:
            raiz = Path(temporal)
            carpeta = raiz / '10_VALIDACION'
            carpeta.mkdir()
            (carpeta / 'evidencia_final.json').write_text(json.dumps({'ventas_centavos': CENTINELA}), encoding='utf-8')
            (carpeta / 'evidencia_extra.json').write_text(json.dumps({'evidencia': {'final': {'silver': CENTINELA}}}), encoding='utf-8')
            (carpeta / 'ejecucion.log').write_text('evidencia.final.ventas_centavos=' + CENTINELA, encoding='utf-8')
            (carpeta / 'errores.json').write_text(json.dumps({'pruebas': [
                {'prueba': PRUEBA, 'estado': 'ERROR', 'detalle': CENTINELA}]}), encoding='utf-8')
            problemas = auditar_artefactos(raiz)
            self.assertEqual(len(problemas), 4)
            self.assertNotIn(CENTINELA, ' '.join(problemas))

    def test_metricas_publicas_c06_y_etl_se_conservan(self):
        informe = {'pruebas': [{'prueba': 'ETL de C06 y validador fila por fila', 'estado': 'OK',
                               'evidencia': {'transferencia': {'ventas_centavos': 123456}, 'validador': 'OK'}}]}
        self.assertFalse(problemas_evidencia_final(informe))


def ejecutar():
    resultado = unittest.TestResult()
    unittest.defaultTestLoader.loadTestsFromTestCase(PrivacidadFinal).run(resultado)
    if not resultado.wasSuccessful():
        raise AssertionError('Fallaron regresiones de privacidad con referencias ficticias')
    return resultado.testsRun


if __name__ == '__main__':
    print(f'OK: {ejecutar()} regresiones de privacidad con referencias ficticias')
