"""Documentos derivados del plan (se regeneran desde nucleo.json y lecciones.json; no se editan a mano).

Los usa `aplicar_nucleo.py --todos` (escribe) y `aplicar_nucleo.py --todos --comprobar` (solo compara):
calendario.csv / calendario.json, CARGA_ESTIMADA.md, RUTAS.md, COMPETENCIAS.md, HITOS_Y_RECUPERACION.md y PLAN_V5.md en `01_PLAN_DIARIO/`,
las columnas «Tipo» de los índices de capítulo de `02_TEORIA/NN_*.md` y la columna «Ruta» del mapa de `02_TEORIA/UAGRM/LEEME.md`.
Dos ejecuciones seguidas producen los mismos bytes.
"""
import csv
import datetime
import io
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLAN = RAIZ / "01_PLAN_DIARIO"
MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS_SEM = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
CLASE = {"NUCLEO": "NÚCLEO", "COMPLEMENTARIA": "COMPLEMENTARIA", "EMPLEO": "EMPLEO"}
CAPITULOS = {1: "SQL desde cero", 2: "Agregar sin perder el significado", 3: "JOIN y duplicación", 4: "Subconsultas, CTE, ventanas, índices", 5: "Calidad de datos y ETL",
             6: "KPIs empresariales", 7: "Python desde cero", 8: "Funciones, archivos, errores", 9: "NumPy y Pandas básico", 10: "Pandas: transformar, unir, validar",
             11: "Estadística descriptiva", 12: "Estadística inferencial", 13: "Modelado dimensional", 14: "Power BI, Power Query y DAX", 15: "Excel como segundo camino",
             16: "Git, documentación, empleo honesto", 17: "Transferencia y autonomía", 18: "Entrevistas", 19: "Puente: de funciones a un ETL"}


def hm(m):
    return f"{m // 60} h {m % 60:02d} min" if m >= 60 else f"{m} min"


def fecha_larga(f):
    d = datetime.date.fromisoformat(f)
    return f"{d.day} de {MESES[d.month]}"


def semana_de(n):
    return (n - 1) // 7 + 1


def rango_semana(ctx, s):
    a, b = ctx.dias[(s - 1) * 7 + 1]["fecha"], ctx.dias[s * 7]["fecha"]
    da, db = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
    return f"{da.day}–{db.day} {MESES[db.month]}" if da.month == db.month else f"{da.day} {MESES[da.month]}–{db.day} {MESES[db.month]}"


def ids_base(d):
    return [e["id"] for g in d.get("practica", []) for e in g["ejercicios"]]


def sql_recup(d):
    return [e["id"] for g in d.get("practica", []) if g["grupo"] == "SQL de recuperación" for e in g["ejercicios"]]


def resumen_global(ctx):
    tot = sum(d["totales"]["total"] for d in ctx.dias.values() if d["tipo"] != "domingo")
    ref = sum(d["refuerzo"]["min"] for d in ctx.dias.values())
    sobre = [n for n, d in ctx.dias.items() if d["tipo"] != "domingo" and d.get("exceso_min", 0) > 4]
    return tot, ref, sobre


# ---------------------------------------------------------------- calendario
def calendario(ctx, actividades, reducido_de):
    filas = []
    for n in range(1, 43):
        d = ctx.dias[n]
        t = d.get("totales", {})
        lecciones = [{"id": e["id"], "parte": e["parte"]} for e in d.get("lecciones", [])]
        filas.append({
            "dia": n, "fecha": d["fecha"], "semana": semana_de(n), "titulo": d["titulo"], "tipo": d["tipo"],
            "base_min": t.get("total", 0), "techo_min": d.get("techo_min"), "exceso_min": d.get("exceso_min", 0),
            "sesiones": [{"sesion": s["sesion"], "min": s["min"]} for s in d.get("sesiones", [])],
            "reducido_min": reducido_de(ctx, n) if d["tipo"] in ("normal", "lunes") else (60 if d["tipo"] == "examen" else 0),
            "minimo_min": 0 if d["tipo"] == "domingo" else 20,
            "lecciones": lecciones, "ejercicios_base": ids_base(d), "sql_recuperacion": sql_recup(d),
            "criterio": [c["id"] for c in d.get("criterio", [])], "refuerzo": d["refuerzo"]["ids"], "refuerzo_min": d["refuerzo"]["min"],
            "examen": (d.get("examen") or {}).get("codigo"),
        })
    js = json.dumps(filas, ensure_ascii=False, indent=2) + "\n"
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["dia", "fecha", "semana", "titulo", "tipo", "base_min", "techo_min", "exceso_min", "sesiones", "reducido_min", "minimo_min", "lecciones", "ejercicios_base", "sql_recuperacion", "criterio", "refuerzo", "refuerzo_min", "examen"])
    for f in filas:
        w.writerow([f["dia"], f["fecha"], f["semana"], f["titulo"], f["tipo"], f["base_min"], f["techo_min"] if f["techo_min"] is not None else "", f["exceso_min"], len(f["sesiones"]),
                    f["reducido_min"], f["minimo_min"], ";".join(f"{l['id']}:{l['parte']}" for l in f["lecciones"]), ";".join(f["ejercicios_base"]), ";".join(f["sql_recuperacion"]),
                    ";".join(f["criterio"]), ";".join(f["refuerzo"]), f["refuerzo_min"], f["examen"] or ""])
    return {"calendario.json": js, "calendario.csv": "﻿" + buf.getvalue()}


# ---------------------------------------------------------------- CARGA_ESTIMADA
def carga(ctx):
    tot, ref, sobre = resumen_global(ctx)
    L = ["# Carga estimada por jornada (ruta BASE)", "",
         "Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json`; no lo edites a mano.", "",
         "Estimación de **primera vez** para una persona que todavía depende de ayuda externa. **No es una medición**: los minutos de cada ejercicio son el punto medio del rango «Primera vez» de su enunciado "
         "(ya incluye leer, equivocarse, depurar y verificar) y los de lectura vienen de la cabecera de cada lección; el error razonable es de ±35 %. Registra tus minutos reales en `mi_trabajo/progreso.csv` y corrige esta tabla con tus datos.", "",
         "## Qué cuenta cada columna (sin dobles conteos)", "",
         "| Columna | Qué incluye |", "|---|---|",
         "| **Teoría** | Lectura de las lecciones NÚCLEO del día (o de la parte asignada: sección inicial, resto o completa) |",
         "| **Micro** | Solo los apartados obligatorios de las microprácticas esenciales y la preparación del entorno |",
         "| **Ejerc.** | Ejercicios BASE autónomos y casos (tiempo de primera vez de cada enunciado) |",
         "| **SQL** | SQL de recuperación: variantes breves de SQL ya enseñado |",
         "| **Crit.** | Criterio analítico o hito de comprensión |",
         "| **Emp.** | Empleo (CV, GitHub, postulaciones, seguimiento) |",
         "| **Cierre/Exam.** | Cierre de 10 min; en sábado de examen, examen + corrección + simulacro = 115 min |",
         "| **Techo** | 150 min en lunes (clase UAGRM aparte), 270 en martes–viernes (objetivo 240), sin techo en examen |", "",
         "El REFUERZO es voluntario y **no** está incluido en el total BASE. La evaluación final (23–30 de noviembre, 570 min en total) es un bloque posterior y tampoco está incluida.", "",
         "| Día | Fecha | Contenido | Tipo | Teoría | Micro | Ejerc. | SQL | Crit. | Emp. | Cierre/Exam. | **BASE** | Techo | Sesiones | REFUERZO (máx.) |",
         "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for n in range(1, 43):
        d = ctx.dias[n]
        if d["tipo"] == "domingo":
            L.append(f"| D{n:02d} | {d['fecha']} | Descanso (0 min obligatorios) | domingo | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | — | — | 0 |")
            continue
        t = d["totales"]
        cierre = t["cierre"] + t.get("examen", 0)
        L.append(f"| D{n:02d} | {d['fecha']} | {d['titulo']} | {d['tipo']} | {t['teoria']} | {t['micropractica']} | {t['ejercicios']} | {t['sql_recuperacion']} | {t['criterio_hitos']} | {t['empleo']} | {cierre} | **{t['total']}** | "
                 f"{d['techo_min'] if d.get('techo_min') else '—'} | {len(d.get('sesiones', [])) or '—'} | {d['refuerzo']['min']} |")
    L += ["", "## Totales por semana", "", "| Semana | Fechas | BASE (min) | BASE (h) | REFUERZO máx. (min) | Jornadas sobre el máximo |", "|---:|---|---:|---:|---:|---:|"]
    for s in range(1, 7):
        dias = [ctx.dias[k] for k in range((s - 1) * 7 + 1, s * 7 + 1)]
        b = sum(x.get("totales", {}).get("total", 0) for x in dias)
        r = sum(x["refuerzo"]["min"] for x in dias)
        so = sum(1 for k in range((s - 1) * 7 + 1, s * 7 + 1) if k in sobre)
        horas = f"{b / 60:.1f}".replace(".", ",")
        L.append(f"| {s} | {rango_semana(ctx, s)} | {b} | {horas} | {r} | {so} |")
    L += ["", f"**Total BASE de las 42 jornadas: {tot} min = {hm(tot)}** (REFUERZO voluntario: hasta {ref} min = {hm(ref)}).", "",
          "## Por qué el total supera 240 min por día", "",
          f"El plan prioriza una formación estudiable, con teoría antes de la práctica, práctica suficiente de SQL, Python, Pandas y BI y preparación para trabajos de Analista de Datos, BI y Data Engineering. "
          f"Esa carga completa no cabe en 240 minutos por día: **{len(sobre)} jornadas superan su máximo por más de 4 minutos** (exceso total {sum(ctx.dias[k]['exceso_min'] for k in sobre)} min). "
          "En cada una, la guía divide el trabajo en **sesiones retomables** con un punto de interrupción y un entregable por sesión, para que no se presente como una sola sentada. "
          "Puedes usar más de un día real sin cambiar la fecha académica; si decides no hacerlo, usa REDUCIDO y mueve la puerta sin acumular horas.", "",
          "## Jornadas sobre su máximo", "", "| Día | BASE | Máximo | Exceso | Sesiones |", "|---:|---:|---:|---:|---|"]
    for k in sobre:
        d = ctx.dias[k]
        L.append(f"| D{k:02d} | {d['totales']['total']} | {d['techo_min']} | {d['exceso_min']} | " + ", ".join(f"{s['sesion']} ({s['min']} min)" for s in d.get("sesiones", [])) + " |")
    L.append("")
    return {"CARGA_ESTIMADA.md": "\n".join(L)}


# ---------------------------------------------------------------- RUTAS
def rutas(ctx, ordenar):
    lec = ctx.lec["lecciones"]
    clases = {}
    for i, v in lec.items():
        clases.setdefault(v["clase"], []).append(i)
    L = ["# Lecciones: clasificación y ruta de estudio", "",
         "Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json` y `lecciones.json`; no lo edites a mano.", "",
         f"Las {len(lec)} lecciones de `02_TEORIA` (los 18 capítulos más el puente del capítulo 19) tienen una sola clase. REFUERZO es una categoría de **ejercicios**, no de lecciones.", "",
         "| Clase | Significado | Dónde aparece | Lecciones |", "|---|---|---|---:|",
         f"| **NÚCLEO** | Indispensable: tiene día y minutos en la ruta BASE; toda su teoría se lee antes de los ejercicios de esa jornada | Sección A de cada guía | {len(clases.get('NUCLEO', []))} |",
         f"| **COMPLEMENTARIA** | Amplía o consulta; no está programada y ningún ejercicio BASE o REFUERZO la exige por primera vez | Material de consulta | {len(clases.get('COMPLEMENTARIA', []))} |",
         f"| **EMPLEO** | Se lee dentro del bloque de empleo de su jornada | Sección H | {len(clases.get('EMPLEO', []))} |", "",
         "Una lección puede leerse en partes: «solo la sección inicial» (la parte mínima que necesita un ejercicio), «resto» (el desarrollo) o «completa». Los minutos de cada parte se cuentan una sola vez.", "",
         "## Ruta NÚCLEO por jornada", "", "| Día | Fecha | Lecciones y partes | Lectura (min) |", "|---:|---|---|---:|"]
    for n in range(1, 43):
        d = ctx.dias[n]
        if not d.get("lecciones"):
            continue
        partes = ", ".join(f"{e['id']}" + ("" if e["parte"] == "completa" else f" ({e['parte']})") for e in ordenar(ctx, d["lecciones"]))
        L.append(f"| D{n:02d} | {d['fecha']} | {partes} | {d['totales']['teoria']} |")
    L += ["", "## Todas las lecciones", "", "| Lección | Título | Clase | Jornada(s) | Lectura (min) | Micropráctica |", "|---|---|---|---|---:|---|"]

    def clave(i):
        a, b = i.split(".")
        return int(a), int(b)
    for i in sorted(lec, key=clave):
        v = lec[i]
        partes = ", ".join(f"D{p['dia']:02d}" + ("" if p["parte"] == "completa" else f" ({p['parte']})") for p in v.get("partes", [])) or "—"
        mic = v.get("micropractica") or {}
        micro = f"obligatorios {', '.join(map(str, mic['obligatorios']))} de {mic['apartados']}" if mic.get("obligatorios") else "—"
        L.append(f"| {i} | {v['titulo']} | {CLASE[v['clase']]} | {partes} | {v.get('lectura_min', 0)} | {micro} |")
    sql_dias = [(n, sql_recup(ctx.dias[n])) for n in range(1, 43) if sql_recup(ctx.dias[n])]
    L += ["", "## SQL de recuperación (práctica frecuente y progresiva)", "",
          "Entre las lecciones de SQL (capítulos 1–4) y el final del programa, las jornadas normales incluyen una variante breve de SQL ya enseñado (SQ01–SQ17, KP01) para que el SQL no se olvide mientras se avanza en Python, Pandas, ETL y BI. "
          f"Las jornadas D08, D22 y D36 (lunes con clase UAGRM) no la llevan.", "", "| Día | Ejercicios | Minutos |", "|---:|---|---:|"]
    for n, ids in sql_dias:
        L.append(f"| D{n:02d} | {', '.join(ids)} | {ctx.dias[n]['totales']['sql_recuperacion']} |")
    L += ["", "## REFUERZO y recursos fuera de la ruta", "",
          f"- Cada jornada normal sugiere un REFUERZO voluntario (en total hasta {sum(d['refuerzo']['min'] for d in ctx.dias.values())} min), con ejercicios **diferentes** de los obligatorios y sobre contenidos ya enseñados.",
          f"- {len(ctx.nucleo['banco_refuerzo_sin_jornada'])} ejercicios existentes no tienen jornada y quedan como banco de práctica: {', '.join(ctx.nucleo['banco_refuerzo_sin_jornada'])}.",
          "- Ejercicios que exigen lecciones COMPLEMENTARIAS y por eso no están en la ruta: " + "; ".join(f"{k} ({v})" for k, v in ctx.nucleo["recursos_complementarios"].items()) + ".", ""]
    return {"RUTAS.md": "\n".join(L)}


# ---------------------------------------------------------------- COMPETENCIAS y HITOS
def puertas(ctx):
    return [(n, d["puerta"]) for n, d in sorted(ctx.dias.items()) if d.get("puerta")]


def competencias(ctx, comp_cap):
    lec = ctx.lec["lecciones"]
    L = ["# Competencias, puertas y cómo usar BASE / REFUERZO", "",
         "Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json` y `lecciones.json`; no lo edites a mano.", "",
         "Esta página reemplaza la idea de «avanzar porque llegó la fecha» por «avanzar porque demostré la base». Las fechas del plan son **objetivos académicos**, no plazos: nada de lo que sigue promete completar todo antes del 30 de noviembre.", "",
         "## Cómo se clasifica cada actividad", "",
         "| Etiqueta | Significado | Cuándo se hace |", "|---|---|---|",
         "| **Lección NÚCLEO** | Teoría indispensable de la jornada (sección A) | Primero, antes de abrir cualquier ejercicio |",
         "| **Micropráctica esencial** | Solo los apartados obligatorios de la micropráctica de una lección NÚCLEO | Después de la teoría, dentro de la sección C |",
         "| **BASE** (obligatorio, sección C) | Ejercicios y casos del día, agrupados por competencia y de menor a mayor dificultad | Siempre, después de toda la teoría |",
         "| **SQL de recuperación** | Variante breve de SQL ya enseñado (SQ01–SQ17, KP01) | En las jornadas normales, para no olvidar SQL |",
         "| **Criterio / hito** | Actividad de criterio analítico (AN) o hito de comprensión (H) | Dentro de la jornada, antes de cerrar |",
         "| **REFUERZO** (sección D) | Ejercicios **diferentes** de los obligatorios, sobre lo ya enseñado; voluntarios, no suman al tiempo BASE, no enseñan nada nuevo y **no sustituyen** una actividad pendiente | Si una puerta falló, te atascaste o sobra tiempo |",
         "| **REDUCIDO** (sección F) | Sesión corta de ≈ 60 min con lo primero de la jornada | Si ese día no puedes hacer el BASE completo; lo que no hagas sigue pendiente |",
         "| **MÍNIMO** (sección G) | 20 minutos: 15 de práctica ya conocida y 5 de cierre | Para no romper la racha; no acredita contenidos nuevos ni avanza una puerta |", "",
         "Lo que no hiciste no se suma al día siguiente: un obligatorio pendiente se retoma en el siguiente bloque disponible. Los domingos son descanso (0 min obligatorios); la recuperación voluntaria (45–120 min) nunca es obligatoria.", "",
         "## Las puertas", "",
         "Cada puerta describe lo que debes poder demostrar, con evidencia, antes de pasar al bloque siguiente. «Explicar» significa decirlo en voz alta sin leer tu código. "
         "Cada documento de examen indica qué base concreta recuperar y qué variante nueva la demuestra (S01–S06 y `08_SOLUCIONES/controles_examenes.md`).", "",
         "| Puerta | Jornada | Fecha objetivo | Qué demuestras y con qué evidencia |", "|---|---|---|---|"]
    for n, p in puertas(ctx):
        L.append(f"| **{p['id']}** | D{n:02d} | {ctx.dias[n]['fecha']} | {p['texto']} |")
    L += ["", "## Qué hacer si una puerta no se cumple en su fecha", "",
          "1. No avances al bloque siguiente; haz el REFUERZO que propone la guía.",
          "2. Mueve la secuencia completa, incluidas las fechas de las puertas siguientes. No se acumulan horas.",
          "3. No recuperes un día perdido en otro. Un día perdido se pierde; un obligatorio pendiente sigue siendo obligatorio.",
          "4. Los domingos son descanso por defecto; si tienes energía, dedica 45–120 minutos a UNA opción y no recuperes una jornada completa.", "",
          "## Competencias y dónde se entrenan", "",
          "| Competencia | Lecciones NÚCLEO | Jornadas | Lectura NÚCLEO (min) |", "|---|---|---|---:|"]
    por_cap = {}
    for i, v in lec.items():
        if v["clase"] != "NUCLEO":
            continue
        cap = int(i.split(".")[0])
        por_cap.setdefault(comp_cap[cap], []).append(i)
    orden = sorted(por_cap, key=lambda c: min(int(i.split(".")[0]) for i in por_cap[c]))

    def clave(i):
        a, b = i.split(".")
        return int(a), int(b)
    for c in orden:
        ids = sorted(por_cap[c], key=clave)
        dias = sorted({p["dia"] for i in ids for p in lec[i]["partes"]})
        mins = sum(p["lectura_min"] for i in ids for p in lec[i]["partes"])
        rango = f"D{dias[0]:02d}" if dias[0] == dias[-1] else f"D{dias[0]:02d}–D{dias[-1]:02d}"
        L.append(f"| {c} | {', '.join(ids)} | {rango} | {mins} |")
    grupos = {}
    for n, d in ctx.dias.items():
        for g in d.get("practica", []):
            for e in g["ejercicios"]:
                grupos.setdefault(g["grupo"], []).append((n, e))
    L += ["", "## Práctica BASE por competencia", "", "| Grupo | Ejercicios BASE | Minutos | Primer día | Último día |", "|---|---:|---:|---|---|"]
    for g in sorted(grupos, key=lambda k: min(n for n, _ in grupos[k])):
        xs = grupos[g]
        L.append(f"| {g} | {len(xs)} | {sum(e['min'] for _, e in xs)} | D{min(n for n, _ in xs):02d} | D{max(n for n, _ in xs):02d} |")
    L.append("")
    return {"COMPETENCIAS.md": "\n".join(L)}


def hitos(ctx):
    L = ["# Hitos, puertas y recuperación", "",
         "Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json`; no lo edites a mano.", "",
         "Una entrega debe cumplir el control y poder explicarse. Haber abierto el archivo no equivale a completar la actividad. Cada puerta exige además un **hito de comprensión** (explicar, predecir, resolver una variante nueva y justificar): un OK del corrector no basta. "
         "Los hitos son puertas de competencia: avanzas cuando demuestras la base, no cuando llega la fecha. Las fechas son objetivos. Detalle de cada puerta, evidencia y reglas: [Competencias y puertas](COMPETENCIAS.md).", "",
         "| Puerta | Jornada | Fecha objetivo | Examen | Hito o criterio de la jornada |", "|---|---|---|---|---|"]
    for n, p in puertas(ctx):
        d = ctx.dias[n]
        hito = d.get("hito") or {}
        L.append(f"| {p['id']} | D{n:02d} | {d['fecha']} | {d['examen']['codigo']} | {hito.get('id', '—')} |")
    L += ["", "Si un examen o un hito no se aprueba, cada documento de examen indica **qué base concreta recuperar y qué variante nueva la demuestra** (S01–S06 y `08_SOLUCIONES/controles_examenes.md`): no se repite la semana por defecto. "
          "La variante resuelta y la explicación de la solución son condiciones necesarias de cualquier hito.", "",
          "La recuperación reemplaza el siguiente bloque práctico; no se añade al final del día. Antes de recortar lo obligatorio, recorta el REFUERZO, la tercera publicación y la presentación estética. "
          "Las postulaciones se adaptan a vacantes pertinentes. Un día mínimo no pretende cubrir contenidos nuevos. Un domingo es descanso por defecto; la recuperación voluntaria (45–120 min) nunca es obligatoria. "
          "El calendario contempla concentración, sueño y flexibilidad; no se utiliza para diagnosticar ni prometer curación.", "",
          "Cuando una puerta se retrasa, se mueve toda la secuencia y no se acumulan horas. El plan no garantiza que todas las puertas se cumplan antes del 30 de noviembre.", ""]
    return {"HITOS_Y_RECUPERACION.md": "\n".join(L)}


# ---------------------------------------------------------------- PLAN_V5
def casillas(texto):
    """{inicio de línea sin casilla: 'x' | ' '} de las casillas actuales, para conservar lo que marcaste."""
    out = {}
    for m in re.finditer(r"^- \[([ xX])\] (.*)$", texto, re.M):
        out[m.group(2)[:60]] = m.group(1).lower()
    return out


def plan(ctx, previo):
    tot, ref, sobre = resumen_global(ctx)
    ya = casillas(previo)

    def cas(linea):
        return "- [" + ("x" if ya.get(linea[:60]) == "x" else " ") + "] " + linea
    fin = ctx.nucleo["evaluacion_final"]
    L = ["# Plan Data & BI v5 (revisión pedagógica v6)", "",
         "Este documento se genera con `herramientas/aplicar_nucleo.py` a partir de `nucleo.json`, salvo las casillas, que son tuyas y se conservan.", "",
         f"**Formación: 12 de octubre–22 de noviembre de 2026 (42 jornadas). Evaluación final: 23–30 de noviembre, un bloque posterior de 9,5 horas que no forma parte de las 42 jornadas.** "
         f"Las 42 jornadas suman **{hm(tot)} de trabajo BASE** (promedio de martes a viernes: {ctx.nucleo['resumen']['promedio_martes_viernes']} min); no son 90 horas ni 15 horas semanales. Detalle en [Carga estimada](CARGA_ESTIMADA.md).", "",
         "El punto de partida es una pasantía de BI con fuerte apoyo de IA y bases técnicas todavía en construcción. El objetivo es resolver SQL, programar Python y construir un ETL junior propio, comprobado y explicable, "
         "y llegar preparado para postular a puestos de Analista de Datos, BI y Data Engineering. El programa no garantiza empleo ni autonomía profesional avanzada en seis semanas.", "",
         "**Revisión pedagógica v6:** la teoría necesaria se lee **antes** de los ejercicios de cada jornada; la práctica BASE (SQL, Python, Pandas, estadística, ETL y BI) se agrupa por competencia y dificultad; "
         "el SQL se retoma con frecuencia mediante variantes breves; el REFUERZO es voluntario, diferente de lo obligatorio y sin teoría nueva; las jornadas que superan su máximo se dividen en sesiones retomables; "
         "no existe una ruta EXTENDIDA. Los exámenes S01–S06, sus contratos y puntuaciones, y las 42 fechas no cambian.", "",
         "## Carga y modalidades", "",
         "Las clases UAGRM del lunes (19:30–22:00) van aparte. Comienza habitualmente a las 13:00 y añade descansos de diez minutos cada 45–50 minutos; son pausas, no actividades pendientes.", "",
         "| Día | COMPLETO (BASE) | REDUCIDO | MÍNIMO |", "|---|---|---|---|",
         "| Lunes | 150 min o menos de objetivo; algunas jornadas lo superan y se dividen en sesiones | ≈ 60 min de lo primero de la guía | 20 min |",
         "| Martes a viernes | objetivo 240 min, máximo 270; las jornadas con más carga se dividen en sesiones retomables | ≈ 60 min | 20 min |",
         "| Sábado | examen (115 min) más hito o criterio, empleo y cierre: 180–185 min | evaluación sin corrección (60 min) | 20 min |",
         "| Domingo | descanso (0 min obligatorios) | descanso | descanso |", "",
         "Las modalidades son alternativas de la misma jornada. REDUCIDO no es el mismo ejercicio con menos minutos: es una sesión corta con lo primero de la guía, y lo que no hagas sigue pendiente (nunca pasa a REFUERZO ni se suma a otra jornada). "
         "MÍNIMO: quince minutos de práctica ya conocida y cinco de cierre; no acredita contenidos nuevos ni cumple puertas. Si necesitas descansar, el descanso reemplaza la sesión. "
         "Un domingo no requiere consulta, publicación ni commit; si tienes energía puedes usar **45–120 minutos voluntarios** en una sola opción.", "",
         "## Estructura de cada jornada", "",
         "A. Qué estudiar (todas las lecciones NÚCLEO, antes de cualquier ejercicio) · B. Distribución neta (y sesiones retomables si hace falta) · C. Práctica y archivos (todos los obligatorios, por competencia y dificultad) · "
         "D. REFUERZO voluntario · E. Comprobar y entregar · F. REDUCIDO · G. MÍNIMO · H. Empleo y clase. Los sábados de examen y los domingos tienen una estructura propia. "
         "Más detalle: [Rutas de estudio](RUTAS.md), [Competencias y puertas](COMPETENCIAS.md) y [Hitos y recuperación](HITOS_Y_RECUPERACION.md).", "",
         "## Método de estudio y prioridad", "",
         "Teoría breve → ejemplo explicado → micropráctica → práctica autónoma → validación → reflexión. Predice el resultado antes de ejecutar. Intenta diez minutos, comprueba, depura otros diez y recién pide una pista. "
         "Consulta la solución después del intento y explica la diferencia con tu código. De martes a viernes hay una actividad de criterio analítico (`03_EJERCICIOS/Analitico/`) y cada puerta exige un hito de comprensión.", "",
         "## Empleo", "",
         "D01–D05: CV y GitHub (sin postulaciones obligatorias). D08–D10: CV final, vacantes pertinentes y primeras candidaturas preparadas. **D11: primera postulación real** si hay CV y vacante pertinente. "
         "Después, seguimiento y hasta dos postulaciones de calidad por semana. LinkedIn: publica solo entregables terminados y verificados, nunca por calendario; no inventes experiencia.", "",
         "## Progresión", "", "| Semana | Fechas | Resultado verificable | BASE |", "|---:|---|---|---:|"]
    resultados = {1: "Filtros, agregación, Python básico, KPIs y S01 (Puerta 1)", 2: "JOIN, funciones con errores, archivos CSV, estadística descriptiva inicial y S02 (Puerta 2)",
                  3: "Pandas, merge validado, duplicados, CTE, ventanas, ABC y S03 (Puerta 3)", 4: "Mini-ETL y ETL guiado hasta claves y duplicados; S04 (Puerta 5a)",
                  5: "ETL guiado completo, modelo estrella, Excel y Power BI mínimo; S05 (Puerta 6)", 6: "Estadística inferencial y caso nuevo C06 en cinco bloques; S06 (Puerta 7)"}
    for s in range(1, 7):
        b = sum(ctx.dias[k].get("totales", {}).get("total", 0) for k in range((s - 1) * 7 + 1, s * 7 + 1))
        L.append(f"| {s} | {rango_semana(ctx, s)} | {resultados[s]} | {hm(b)} |")
    L += ["", "## Registro diario", "",
          "Marca el día cuando completaste su objetivo y puedes explicar el control. Registra modalidad, minutos reales, ayuda utilizada y siguiente base en `mi_trabajo/progreso.csv`; anota errores en `mi_trabajo/errores.md`. "
          "Guarda consultas, scripts y explicaciones propios en GitHub; los borradores y referencias no prueban aprendizaje.", "", "## Jornadas", ""]
    puerta_dia = {n: p["id"] for n, p in puertas(ctx)}
    for s in range(1, 7):
        L += [f"### Semana {s}", ""]
        for k in range((s - 1) * 7 + 1, s * 7 + 1):
            d = ctx.dias[k]
            f = datetime.date.fromisoformat(d["fecha"])
            nombre = f"dias/D{k:02d}_{d['fecha']}.md"
            if d["tipo"] == "domingo":
                extra = "descanso (0 min obligatorios)"
            else:
                extra = f"BASE {d['totales']['total']} min" + (f" en {len(d['sesiones'])} sesiones" if d.get("sesiones") else "") + (f" · REFUERZO ≤ {d['refuerzo']['min']} min" if d["refuerzo"]["min"] else "")
            L.append(cas(f"**D{k:02d} · {f.day:02d}/{f.month:02d} {DIAS_SEM[f.weekday()]}:** [{d['titulo']}]({nombre}) · {extra}."))
        hito_sem = {1: "examen S01 corregido y Puerta 1 evaluada", 2: "examen S02 corregido y Puerta 2 evaluada", 3: "examen S03 corregido y Puerta 3 evaluada",
                    4: "mini-ETL defendido y checkpoint S04 (Puerta 5a) registrados", 5: "ETL guiado completo y BI mínimo (Puerta 6) registrados con honestidad", 6: "C06 y examen S06 (Puerta 7) registrados"}[s]
        L += [cas(f"Hito semana {s}: {hito_sem} (decisión de continuidad registrada)."), ""]
    L += ["## Evaluación final", ""]
    for b in fin["bloques"]:
        f = datetime.date.fromisoformat(b["fecha"])
        L.append(cas(f"{f.day} de {MESES[f.month]}: {b['entrega']}."))
    L += ["", f"**Carga:** 570 minutos netos (9,5 h) en un bloque posterior y explícito, que no forma parte de las 42 jornadas. {fin['nota']}", "",
          "Guía completa: [Evaluación final](../09_EVALUACION_FINAL/ENUNCIADO.md). La habilidad se acredita con trabajo propio, cuadres y explicación; si falta una puerta crítica, registra la limitación y refuerza dos bases antes de una nueva variante.", ""]
    return {"PLAN_V5.md": "\n".join(L)}


# ---------------------------------------------------------------- índices de teoría
def tipo_leccion(ctx, i):
    v = ctx.lec["lecciones"][i]
    clase = CLASE[v["clase"]]
    dias = sorted({p["dia"] for p in v.get("partes", [])})
    if not dias:
        return clase
    if len(dias) == 1:
        return f"{clase} · D{dias[0]:02d}"
    return f"{clase} · D{dias[0]:02d}–D{dias[-1]:02d}"


def indices_capitulo(ctx):
    """Reescribe la columna «Tipo» de la tabla de lecciones de cada `02_TEORIA/NN_*.md`; devuelve {ruta relativa: texto}."""
    out = {}
    for p in sorted((RAIZ / "02_TEORIA").glob("[0-9][0-9]_*.md")):
        t = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        nuevo = []
        cambiado = False
        for linea in t.split("\n"):
            m = re.match(r"^\| (\d{1,2}\.\d{1,2}) \| (.*) \| ([^|]*) \| ([^|]*) \|$", linea)
            if m and m.group(1) in ctx.lec["lecciones"]:
                linea2 = f"| {m.group(1)} | {m.group(2)} | {tipo_leccion(ctx, m.group(1))} | {m.group(4)} |"
                cambiado |= linea2 != linea
                linea = linea2
            nuevo.append(linea)
        if cambiado:
            out[p.relative_to(RAIZ).as_posix()] = "\n".join(nuevo)
    return out


def mapa_uagrm(ctx):
    p = RAIZ / "02_TEORIA" / "UAGRM" / "LEEME.md"
    t = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
    nuevo = []
    for linea in t.split("\n"):
        m = re.match(r"^\| (Clase [12] · [^|]*) \| ([0-9][0-9., ]*) \| ([^|]*) \|$", linea)
        if m:
            ids = [x.strip() for x in m.group(2).split(",") if x.strip()]
            if all(i in ctx.lec["lecciones"] for i in ids):
                linea = f"| {m.group(1)} | {m.group(2)} | " + "; ".join(f"{i}: {tipo_leccion(ctx, i)}" for i in ids) + " |"
        nuevo.append(linea)
    return {p.relative_to(RAIZ).as_posix(): "\n".join(nuevo)}


def todos(ctx, comp_cap, actividades, reducido_de, ordenar):
    """{ruta relativa al repositorio: texto} de todos los derivados."""
    previo = (PLAN / "PLAN_V5.md").read_bytes().decode("utf-8-sig").replace("\r\n", "\n") if (PLAN / "PLAN_V5.md").exists() else ""
    docs = {}
    for parte in (calendario(ctx, actividades, reducido_de), carga(ctx), rutas(ctx, ordenar), competencias(ctx, comp_cap), hitos(ctx), plan(ctx, previo)):
        for nombre, texto in parte.items():
            docs[f"01_PLAN_DIARIO/{nombre}"] = texto
    docs.update(indices_capitulo(ctx))
    docs.update(mapa_uagrm(ctx))
    return docs
