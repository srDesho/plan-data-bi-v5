#!/usr/bin/env python
"""Construye (una sola vez) las fuentes canónicas v2 a partir de la especificación aprobada.

  01_PLAN_DIARIO/nucleo.json              plan de las 42 jornadas (esquema v2)
  01_PLAN_DIARIO/lecciones.json           las 100 lecciones + el puente (clase, partes, anclas, micropráctica)
  01_PLAN_DIARIO/progreso_acreditado.json las 34 realizaciones acreditadas, con clave estable

Después de ejecutarla, esos archivos son la fuente de verdad y se editan a mano o con herramientas; la especificación
`docs/diseno_v6/plan_v6.json` queda como referencia congelada. Por seguridad NO sobrescribe si los archivos ya son v2:
usa --forzar solo si sabes lo que haces.

    .venv\\Scripts\\python.exe herramientas/construir_fuentes_v6.py
"""
import json, re, subprocess, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOC = RAIZ / "docs" / "diseno_v6"
PLAN_DIR = RAIZ / "01_PLAN_DIARIO"
sys.stdout.reconfigure(encoding="utf-8")


def leer(p):
    return Path(p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def git_head(ruta):
    r = subprocess.run(["git", "-C", str(RAIZ), "show", f"HEAD:{ruta}"], capture_output=True)
    return r.stdout.decode("utf-8-sig").replace("\r\n", "\n")


OBJETIVO = {
 1: "Instalar el entorno, leer una tabla (fila y columna) y escribir tu primera consulta y tu primera función.",
 2: "Filtrar con WHERE, tratar NULL y texto, y decidir con booleanos antes de calcular un porcentaje.",
 3: "Guardar varios valores con listas y diccionarios y recortar resultados con ORDER BY y LIMIT.",
 4: "Contar, sumar y promediar con SQL y repetir pasos en Python con bucles y acumuladores.",
 5: "Agrupar con GROUP BY y HAVING, elegir el denominador correcto y recorrer registros en Python.",
 6: "Resolver el examen S01 sin soluciones y explicar un KPI a gerencia.",
 8: "Convertir y validar valores y escribir funciones con contrato.",
 9: "Unir tablas con INNER JOIN conociendo la cardinalidad, rechazar datos inválidos con excepciones y leer un traceback.",
 10: "Leer y escribir CSV, usar módulos y publicar tu primer repositorio de portafolio.",
 11: "Conservar ausentes con LEFT JOIN, detectar el JOIN que duplica, calcular con fechas y hacer tu primera postulación real.",
 12: "Definir un KPI con su ficha, depurar con pruebas y leer frecuencias, media y mediana.",
 13: "Resolver el examen S02 sin soluciones y explicar un cuadre entre JOIN y archivos.",
 15: "Cargar un CSV como DataFrame y perfilarlo antes de usarlo.",
 16: "Limpiar nulos y duplicados exactos y calcular el drop size.",
 17: "Agrupar y unir con Pandas validando la cardinalidad, filtrar y clasificar con CASE.",
 18: "Dividir consultas largas con subconsultas y CTE, usar funciones de ventana y describir datos con centro y dispersión.",
 19: "Clasificar con ABC, controlar la calidad de un DataFrame y escribir pruebas propias.",
 20: "Resolver el examen S03 sin soluciones y defender una decisión sobre duplicados y claves.",
 22: "Entender las capas del ETL, extraer y perfilar (mini-ETL 1).",
 23: "Escribir el contrato de datos y transformar con reglas y rechazos (mini-ETL 2).",
 24: "Validar, cuadrar y cargar a SQLite de forma repetible (mini-ETL 3).",
 25: "Medir cumplimiento y productividad, probar con assert, calcular percentiles y empezar el ETL guiado.",
 26: "Modelar hechos y dimensiones, evitar errores silenciosos y completar las etapas 2 y 3 del ETL.",
 27: "Resolver el examen S04 sin soluciones y defender el mini-ETL.",
 29: "Construir un modelo estrella, avanzar el ETL (Silver) y medir productividad con variación.",
 30: "Conocer el flujo de Power BI, preparar Excel y cerrar Gold, carga y cuadre SQL del ETL.",
 31: "Cuadrar en Excel con tabla dinámica y fórmulas y transformar con Power Query.",
 32: "Construir la tabla de fechas y el modelo con relaciones en Power BI, y limpiar con Power Query.",
 33: "Escribir medidas DAX con CALCULATE y armar un panel mínimo defendible.",
 34: "Resolver el examen S05 sin soluciones y cuadrar ETL, Excel y Power BI.",
 36: "Planificar el caso C06 (contrato y plan) y entender el muestreo y la variabilidad.",
 37: "Extraer y perfilar C06, estimar con intervalos de confianza y evitar errores silenciosos.",
 38: "Silver y rechazos de C06, plantear hipótesis, entender el p-valor e interpretar con honestidad.",
 39: "Gold y cuadres de C06 y comparar dos promedios con la prueba de Welch.",
 40: "SQLite, repetición y README de C06; interpretar pruebas y prepararte para defender.",
 41: "Resolver el examen S06 sin soluciones y defender tu ETL con un caso nuevo.",
}
PUENTE_TIT = {"19.1": "Leer un error en lugar de temerle", "19.2": "Rechazar con ValueError y dejar rastro",
              "19.3": "De funciones a un programa: extraer, transformar, validar, cargar", "19.4": "Cargar a SQLite en Windows: cierra la conexión"}
PREP_ANCLAS = {"1.2": "preparacion-s1", "7.4": "preparacion-p01", "1.6": "preparacion-s2", "7.5": "preparacion-p03", "7.10": "preparacion-p02", "14.5": "seccion-inicial"}
PARTE_CLAVE = {"1.4": "completa", "7.6": "completa", "1.6": "resto", "7.8": "completa", "7.9": "completa", "2.1": "completa", "7.10": "resto"}


def construir(forzar=False):
    destino = PLAN_DIR / "nucleo.json"
    if destino.exists() and not forzar:
        try:
            if json.loads(leer(destino)).get("version") == "v2":
                raise SystemExit("nucleo.json ya es v2; usa --forzar para reconstruirlo")
        except json.JSONDecodeError:
            pass
    plan = json.loads(leer(DOC / "plan_v6.json"))
    viejo = json.loads(git_head("01_PLAN_DIARIO/nucleo.json"))
    mic = json.loads(leer(DOC / "micropracticas.json"))
    dias = {}
    for r in plan["dias"]:
        n = r["dia"]
        d = {k: v for k, v in r.items() if k not in ("id",)}
        d["objetivo"] = OBJETIVO.get(n)
        if r["tipo"] == "examen":
            v = viejo["dias"][str(n)]
            d["puerta"] = v["puerta"]
            d["hito"] = v.get("criterio")
        dias[str(n)] = d
    nuevos = {x["id"]: x for x in plan["nuevos"]}
    nucleo = {
        "version": "v2",
        "nota": "Fuente canónica del plan de 42 jornadas (esquema v2). Generada desde docs/diseno_v6/plan_v6.json; lee `herramientas/aplicar_nucleo.py`.",
        "calendario": {"inicio": "2026-10-12", "jornadas": 42, "clases_uagrm": "lunes 19:30–22:00 (aparte del tiempo autónomo)"},
        "resumen": plan["resumen"],
        "dias": dias,
        "clasificacion_lecciones": plan["clasificacion_lecciones"],
        "ejercicios_nuevos": nuevos,
        "items_proyecto": viejo["items_personalizados"],
        "requisitos_manuales": plan["requisitos_manuales"],
        "excepciones_prerrequisito": plan["excepciones_prerrequisito"],
        "excepciones_ejercicio": plan["excepciones_ejercicio"],
        "excepciones_sql": plan["excepciones_sql"],
        "refuerzo_dia_minimo": plan["refuerzo_dia_minimo"],
        "recursos_complementarios": plan["recursos_complementarios_motivo"],
        "banco_refuerzo_sin_jornada": plan["banco_refuerzo_sin_jornada"],
        "evaluacion_final": viejo["evaluacion_final"],
    }
    # ---- lecciones
    ant = json.loads(git_head("01_PLAN_DIARIO/lecciones.json"))
    cl = plan["clasificacion_lecciones"]
    partes = {}
    for r in plan["dias"]:
        for e in r.get("lecciones", []):
            partes.setdefault(e["id"], []).append({"parte": e["parte"], "dia": r["dia"], "lectura_min": e["lectura_min"], "micro_min": e["micro_min"]})
    lecs = {}
    for k, v in ant["lecciones"].items():
        txt = leer(RAIZ / "02_TEORIA" / v["archivo"])
        tit = txt.split("\n")[0].lstrip("# ").strip()
        m = re.search(r"Tiempo estimado:\s*(\d+)\s*min\s*\(lectura\s*(\d+)\s*\+\s*pr[aá]ctica\s*(\d+)", txt)
        clase = "NUCLEO" if k in cl["nucleo"] else ("EMPLEO" if k in cl["empleo"] else "COMPLEMENTARIA")
        anclas = {a: (f'<a id="{a}"></a>' in txt) for a in ("preparacion-s1", "preparacion-p01", "preparacion-s2", "preparacion-p03", "preparacion-p02", "desarrollo", "micropractica", "seccion-inicial")}
        mm = mic.get(k)
        lecs[k] = {"archivo": v["archivo"], "titulo": tit, "clase": clase,
                   "total_min": int(m.group(1)) if m else None, "lectura_min": int(m.group(2)) if m else None, "practica_min": int(m.group(3)) if m else None,
                   "partes": partes.get(k, []), "anclas": [a for a, ok in anclas.items() if ok],
                   "micropractica": ({"apartados": mm["apartados_totales"], "obligatorios": mm["obligatorios"], "integrado_en": mm["integrado_en"], "minutos_obligatorios": mm["minutos_obligatorios"]} if mm else None)}
    puente = {k: {"titulo": t, "archivo": "19_Puente_Python_a_ETL.md", "seccion": f"§{k.split('.')[1]}", "partes": partes.get(k, []), "clase": "NUCLEO"} for k, t in PUENTE_TIT.items()}
    lecciones = {"version": "v2", "nota": "Clase de cada lección: NUCLEO (programada en BASE), COMPLEMENTARIA (recurso fuera de BASE) o EMPLEO (se lee dentro del tiempo de empleo). Sin REFUERZO ni PROFUNDIZACIÓN: REFUERZO es una categoría de ejercicios.",
                 "lecciones": lecs, "puente": puente}
    # ---- progreso
    m34 = json.loads(leer(DOC / "matriz_34.json"))
    crudas = []
    for dia, nombre in ((1, "D01_2026-10-12"), (2, "D02_2026-10-13"), (3, "D03_2026-10-14"), (4, "D04_2026-10-15")):
        for ln in git_head(f"01_PLAN_DIARIO/dias/{nombre}.md").split("\n"):
            m = re.match(r"^\s*- \[x\] (.*)$", ln)
            if m:
                crudas.append(m.group(1))
    assert len(crudas) == len(m34) == 34, (len(crudas), len(m34))
    prog = []
    for it, cruda in zip(m34, crudas):
        if it["tipo"] == "lección":
            clave = f"lec:{it['id']}|{PARTE_CLAVE[it['id']]}"
        elif it["id"]:
            clave = f"ej:{it['id']}"
        else:
            ascii_ = unicodedata.normalize("NFKD", it["texto"]).encode("ascii", "ignore").decode()
            clave = "gen:" + re.sub(r"\W+", "_", ascii_)[:40].strip("_").lower() + f"|D{it['dia']:02d}"
        prog.append({"n": it["n"], "clave": clave, "dia_original": it["dia"], "id": it["id"], "tipo": it["tipo"], "texto_original": it["texto"], "linea_original": cruda,
                     "evidencia": it["evidencia"], "sha256_evidencia": it["sha256_evidencia"], "ubicacion_nueva": it["ubicacion_nueva"], "estado": "completado"})
    progreso = {"version": "v1", "nota": "Realizaciones acreditadas antes del rediseño. El generador marca [x] solo estas claves; nunca marca actividades nuevas.", "acreditadas": prog}
    for nombre, obj in (("nucleo.json", nucleo), ("lecciones.json", lecciones), ("progreso_acreditado.json", progreso)):
        (PLAN_DIR / nombre).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print("escrito", nombre)


if __name__ == "__main__":
    construir("--forzar" in sys.argv)
