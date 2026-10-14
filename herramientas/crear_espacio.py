"""Crea tu espacio de aprendizaje sin sobrescribir trabajo existente."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
def crear():
    base=ROOT/'mi_trabajo'
    for name in ['sql','python','notebooks','estadistica','casos','etl','mini_etl','depuracion','powerbi','dias','examenes','transferencia','final','analitico','hitos']:(base/name).mkdir(parents=True,exist_ok=True)
    errors=base/'errores.md'
    if not errors.exists():errors.write_text('# Errores y aprendizajes\n\n|Fecha|Ejercicio|Qué falló|Cómo lo detecté|Regla próxima vez|\n|---|---|---|---|---|\n',encoding='utf-8')
    p=base/'progreso.csv'
    if not p.exists():
        days=json.loads((ROOT/'01_PLAN_DIARIO/calendario.json').read_text(encoding='utf-8'))
        with p.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f);w.writerow(['fecha','dia','nivel_elegido','minutos_reales','evidencia','puedo_explicar','ayuda_recibida','siguiente_base'])
            for d in days:w.writerow([d['fecha'],d['dia'],'','','','','',''])
    print('OK',base,'sin sobrescribir registros existentes')
if __name__=='__main__':crear()
