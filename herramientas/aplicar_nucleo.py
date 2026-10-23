#!/usr/bin/env python
"""Generador de las 42 jornadas (esquema v2).

Lee `01_PLAN_DIARIO/nucleo.json`, `lecciones.json` y `progreso_acreditado.json` y escribe `01_PLAN_DIARIO/dias/Dnn_AAAA-MM-DD.md` con el formato
definitivo A–H (jornadas normales) o la estructura especial de examen y domingo. No usa EXTENDIDA. Las casillas `[x]` se conservan:
las acreditadas antes del rediseño vienen de `progreso_acreditado.json` y las que marques después se leen de la propia guía
(cada casilla lleva una clave oculta `<!--k:...-->`). Es idempotente: dos ejecuciones seguidas no cambian ningún byte.

Uso (desde la raíz, con el Python del .venv):
    python herramientas/aplicar_nucleo.py --dias 1-5       # escribe esas jornadas
    python herramientas/aplicar_nucleo.py --todos          # escribe las 42
    python herramientas/aplicar_nucleo.py --dias 1-5 --comprobar   # no escribe: código 1 si algún archivo cambiaría
"""
import argparse, datetime, json, re, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLAN = RAIZ / "01_PLAN_DIARIO"
DIAS = PLAN / "dias"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
SEMANA = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
PREF = "../../"
COMP_CAP = {1: "Consultas SQL de lectura: SELECT, filtros, NULL y orden", 2: "Agregación y denominadores en SQL", 3: "JOIN, cardinalidad y conciliación",
            4: "Consultas analíticas: subconsultas, CTE y ventanas", 5: "ETL: contrato, calidad, rechazos y cargas repetibles", 6: "KPIs: definición, numerador y denominador",
            7: "Fundamentos de Python", 8: "Funciones, archivos, errores y pruebas", 9: "Pandas: lectura, perfilado y limpieza", 10: "Pandas: transformar, agrupar, unir y validar",
            11: "Estadística descriptiva", 12: "Estadística inferencial introductoria", 13: "Modelado dimensional", 14: "Power BI, Power Query y DAX",
            15: "Excel como segundo camino de cuadre", 16: "Git, documentación y portafolio", 17: "Transferencia y depuración autónoma", 18: "Entrevistas técnicas",
            19: "Puente de funciones a ETL"}
GRUPO_CAP = {1: "SQL", 2: "SQL", 3: "SQL", 4: "SQL", 5: "ETL", 6: "KPIs", 7: "Python", 8: "Python", 9: "Pandas", 10: "Pandas", 11: "Estadística", 12: "Estadística",
             13: "Excel · Power Query · BI · modelo", 14: "Excel · Power Query · BI · modelo", 15: "Excel · Power Query · BI · modelo", 16: "Git y portafolio", 17: "ETL", 18: "Git y portafolio", 19: "ETL"}
GORD = ["SQL", "SQL de recuperación", "Python", "Pandas", "Estadística", "KPIs", "ETL", "Excel · Power Query · BI · modelo", "Git y portafolio", "Otros"]
FAMILIAS = ["SQL", "Python", "Estadistica", "Analitico", "Casos", "Comprension", "Depuracion", "Puente", "EXAMENES"]
ENTREGA_FAM = {"SQL": "mi_trabajo/sql/", "Python": "mi_trabajo/python/mis_funciones.py"}
CIERRE_PREGUNTA = "¿Qué podría repetir con otras columnas sin IA y qué base necesito reforzar?"
CHECK_CIERRE = ["Un resultado coincide con un control independiente y puedo explicar el filtro o denominador.",
                "Guardé código propio y explicación en `mi_trabajo/dias/{dd}.md` y su carpeta de ejercicios.",
                "Registré un error/aprendizaje y el nivel elegido en progreso.csv.",
                "Preparé un commit del trabajo terminado; al publicar incluyo README y límites."]


def leer(p):
    return Path(p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def slug(texto):
    a = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", "_", a)[:40].strip("_").lower()


def limpio(texto):
    return re.sub(r"\]\([^)]*\)", "]", texto)


class Ctx:
    def __init__(self):
        self.nucleo = json.loads(leer(PLAN / "nucleo.json"))
        self.lec = json.loads(leer(PLAN / "lecciones.json"))
        self.prog = json.loads(leer(PLAN / "progreso_acreditado.json"))
        self.dias = {int(k): v for k, v in self.nucleo["dias"].items()}
        self.acreditadas = {a["clave"]: a for a in self.prog["acreditadas"]}
        self.ruta_ej = {}
        for fam in FAMILIAS:
            for p in sorted((RAIZ / "03_EJERCICIOS" / fam).glob("*.md")):
                self.ruta_ej.setdefault(p.stem, (fam, p))
        self.meta_cache = {}
        self.errores = []
        self.sin_archivo = set()

    def meta(self, i):
        """(título, ruta relativa al repo, nivel, minutos de primera vez, familia)"""
        if i in self.meta_cache:
            return self.meta_cache[i]
        if i in self.nucleo["items_proyecto"]:
            it = self.nucleo["items_proyecto"][i]
            r = (it["titulo"], it["enlaces"][0][1].replace("../../", "") if it["enlaces"] else "", "", it.get("est"), "Proyecto")
        elif i in self.ruta_ej:
            fam, p = self.ruta_ej[i]
            t = leer(p).split("\n")
            tit = re.sub(r"^#\s*" + re.escape(i) + r"\s*[·:-]\s*", "", t[0]).strip()
            tit = tit if tit != t[0] else t[0].lstrip("# ").strip()
            cab = "\n".join(t[:8])
            niv = re.search(r"Nivel\s+([^·\n]+?)\s*·", cab)
            pv = re.search(r"Primera vez:\s*(\d+)\s*[–-]\s*(\d+)", cab)
            r = (tit, p.relative_to(RAIZ).as_posix(), niv.group(1).strip() if niv else "", round((int(pv.group(1)) + int(pv.group(2))) / 2) if pv else None, fam)
        else:
            self.sin_archivo.add(i)
            r = (i, "", "", None, "?")
        self.meta_cache[i] = r
        return r


def hm(m):
    return f"{m // 60} h {m % 60:02d} min" if m >= 60 else f"{m} min"


def enlace(ruta, ancla=""):
    return f"{PREF}{ruta}" + (f"#{ancla}" if ancla else "")


def tit_leccion(ctx, i):
    if i.startswith("19."):
        return ctx.lec["puente"][i]["titulo"]
    return re.sub(r"^\d+\.\d+\s+", "", ctx.lec["lecciones"][i]["titulo"])


def ruta_leccion(ctx, i):
    if i.startswith("19."):
        return "02_TEORIA/19_Puente_Python_a_ETL.md"
    return "02_TEORIA/" + ctx.lec["lecciones"][i]["archivo"]


def preparacion(ctx, i):
    if i.startswith("19."):
        return ""
    t = leer(RAIZ / "02_TEORIA" / ctx.lec["lecciones"][i]["archivo"])
    m = re.search(r"Prerrequisitos?:\s*([^\n]*)", t)
    if not m:
        return ""
    a2id = {v["archivo"].split("/")[-1]: k for k, v in ctx.lec["lecciones"].items()}
    ids = [a2id[f.split("/")[-1]] for f in re.findall(r"\]\(([^)]+\.md)", m.group(1)) if f.split("/")[-1] in a2id]
    ids += [x for x in re.findall(r"lecciones?\s+(\d+\.\d+)", m.group(1)) if x not in ids]
    return ", ".join(dict.fromkeys(ids))


def ordenar_lecciones(ctx, entradas):
    """Orden de lectura dentro de la jornada: respeta el orden del plan, pero una lección va después de sus prerrequisitos del mismo día
    (todas las partes) y el «resto» de una lección va después de su sección inicial."""
    pendientes = list(entradas)
    ids_dia = {e["id"] for e in entradas}
    puestas, salida = [], []
    while pendientes:
        for e in pendientes:
            i = e["id"]
            if e["parte"] == "sec.":
                ok = True
            else:
                prereq = [p for p in preparacion(ctx, i).split(", ") if p and p in ids_dia and p != i]
                ok = all(not any(x["id"] == p and x not in puestas for x in entradas) for p in prereq)
                if e["parte"] == "resto":
                    ok = ok and all(x in puestas for x in entradas if x["id"] == i and x["parte"] == "sec.")
            # dentro de un mismo capítulo, las lecciones se leen en orden numérico (12.5 antes que 12.8)
            cap, num = (int(v) for v in i.split("."))
            ok = ok and all(x in puestas for x in entradas if int(x["id"].split(".")[0]) == cap and int(x["id"].split(".")[1]) < num)
            if ok:
                pendientes.remove(e); puestas.append(e); salida.append(e)
                break
        else:
            salida += pendientes
            break
    return salida


def dia_primer_ejercicio(ctx, texto):
    """Día más temprano (entre los ejercicios citados en `texto`) en que aparece como BASE; si no es BASE en ningún día, el más temprano en que aparece. 0 si no cita ninguno."""
    if not hasattr(ctx, "_dias_ej"):
        base, cualquiera = {}, {}
        for n, d in ctx.dias.items():
            if d.get("tipo") == "domingo":
                continue
            for g in d.get("practica", []):
                for e in g["ejercicios"]:
                    base[e["id"]] = min(base.get(e["id"], 99), n)
            for c in d.get("criterio", []):
                base[c["id"]] = min(base.get(c["id"], 99), n)
            for r in d.get("refuerzo", {}).get("ids", []):
                cualquiera[r] = min(cualquiera.get(r, 99), n)
        ctx._dias_ej = (base, cualquiera)
    base, cualquiera = ctx._dias_ej
    ids = re.findall(r"\b[A-Z]{1,3}\d+[a-z]?\b", texto)
    dias = [base.get(x, cualquiera.get(x, 0)) for x in ids]
    return min(dias) if dias else 0


def apartados_micro(ctx, i, obligatorios):
    t = leer(RAIZ / "02_TEORIA" / ctx.lec["lecciones"][i]["archivo"])
    m = re.search(r"^## Micropr[aá]ctica\s*\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if not m:
        return []
    sec = re.split(r"Cómo saber que está bien|<details>", m.group(1))[0]
    items = {int(a): re.sub(r"\s+", " ", re.sub(r"```.*?```", "", b, flags=re.S)).strip() for a, b in re.findall(r"^\s*(\d+)\.\s+(.*?)(?=^\s*\d+\.\s|\Z)", sec, re.M | re.S)}
    return [(a, items[a][:170] + ("…" if len(items[a]) > 170 else "")) for a in obligatorios if a in items]


# ---------------------------------------------------------------- casillas
def marcar(ctx, hechas, clave, texto_extra=None):
    return "x" if (clave in ctx.acreditadas or clave in hechas) else " "


def hechas_en_guia(ruta):
    out = set()
    if not ruta.exists():
        return out
    for ln in leer(ruta).split("\n"):
        m = re.match(r"^\s*- \[x\] .*<!--k:([^>]+)-->\s*$", ln)
        if m:
            out.add(m.group(1))
    return out


def caja(ctx, hechas, clave, cuerpo):
    return f"- [{marcar(ctx, hechas, clave)}] {cuerpo} <!--k:{clave}-->"


# ---------------------------------------------------------------- actividades (para sesiones y REDUCIDO)
def actividades(ctx, n, d):
    A = []
    if d.get("entorno_min"):
        A.append(("ejercicio", "Preparar el entorno (instalar y comprobar Python y SQLite)", d["entorno_min"]))
    for e in d["lecciones"]:
        parte = "" if e["parte"] == "completa" else (" (sección inicial)" if e["parte"] == "sec." else " (resto)")
        A.append(("lectura", f"Leer {e['id']} {tit_leccion(ctx, e['id'])}{parte}", e["lectura_min"]))
        if e["micro_min"]:
            A.append(("micro", f"Micropráctica esencial {e['id']}", e["micro_min"]))
    for x in d["extras_micro"]:
        A.append(("micro", x["texto"].replace("micro ", "Micropráctica esencial "), x["min"]))
    for g in d["practica"]:
        for e in g["ejercicios"]:
            A.append(("ejercicio", f"{e['id']} ({g['grupo']})", e["min"]))
    for c in d["criterio"]:
        A.append(("criterio", f"{c['id']} (criterio/hito)", c["min"]))
    A.append(("empleo", d["empleo"]["descripcion"], d["empleo"]["min"]))
    A.append(("cierre", "Guardar, comprobar y registrar aprendizaje", d["cierre_min"]))
    return A


# ---------------------------------------------------------------- jornada normal
def reducido(ctx, n):
    """Actividades de la sesión corta REDUCIDO (lo primero de la jornada hasta ≈ 60 min) y sus minutos."""
    acum, red = 0, []
    for a in actividades(ctx, n, ctx.dias[n]):
        if a[0] in ("empleo", "cierre"):
            continue
        red.append(a); acum += a[2]
        if acum >= 60:
            break
    return red, acum


def datos_texto(ctx, d):
    fams = set()
    for g in d["practica"]:
        fams.add(g["grupo"])
    for e in d["lecciones"]:
        if e["micro_min"]:
            fams.add(GRUPO_CAP[int(e["id"].split(".")[0])])
    L = []
    if fams & {"SQL", "SQL de recuperación"}:
        L.append("SQL: base `04_DATASETS/comercial.db` (diccionario en `04_DATASETS/DICCIONARIO.md`); los ejemplos de las lecciones usan la mini-base `04_DATASETS/mini_base/`.")
    if "Python" in fams:
        L.append("Python: parte de `03_EJERCICIOS/Python/plantilla.py` en `mi_trabajo/python/mis_funciones.py` y completa una función por vez; los datos están en `04_DATASETS/`.")
    if "Pandas" in fams:
        L.append("Pandas: CSV de `04_DATASETS/distribuidora/` y `04_DATASETS/`; usa el Python del `.venv` (pandas 2.2.3).")
    if "Estadística" in fams:
        L.append("Estadística: `04_DATASETS/distribuidora/drop_por_pedido.csv`, `04_DATASETS/experimento_piloto.csv` y `04_DATASETS/mini_base/`.")
    if "ETL" in fams:
        L.append("ETL: mini-ETL en `04_DATASETS/mini_etl/`; ETL de la distribuidora en `04_DATASETS/distribuidora/etl/` con el proyecto `05_PROYECTOS/etl/`; caso C06 en `04_DATASETS/transferencia/`.")
    if "Excel · Power Query · BI · modelo" in fams:
        L.append("Excel, Power Query y Power BI: `05_PROYECTOS/powerbi/` (modelo, medidas y validación manual) y los CSV de `04_DATASETS/`. Excel y Power BI Desktop exigen evidencia manual tuya: lo que no ejecutes queda como pendiente de ejecución.")
    if "Git y portafolio" in fams:
        L.append("Git: trabaja en una carpeta de práctica fuera de este repositorio.")
    return L or ["Datos: los que indica cada enunciado."]


def corrector(ctx, i):
    fam = ctx.meta(i)[4]
    sql_ctl = json.loads(leer(RAIZ / "08_SOLUCIONES" / "controles_sql.json")) if not hasattr(ctx, "_csql") else ctx._csql
    ctx._csql = sql_ctl
    nuevo = ctx.nucleo["ejercicios_nuevos"].get(i)
    if nuevo and nuevo.get("familia") == "Git y portafolio":
        return "python herramientas/verificar_portafolio.py <carpeta de tu portafolio>"
    if nuevo and nuevo.get("familia") == "Modelado":
        return f"python herramientas/validar_modelo.py {i} mi_trabajo/modelo/{i}.md"
    if nuevo and i not in sql_ctl:
        if i == "PT01":
            return "python herramientas/corregir_nuevos.py PT01 mi_trabajo/python/pruebas_PT01.py"
        if i == "PE01":
            return "python herramientas/corregir_nuevos.py PE01 mi_trabajo/depuracion/PE01.py"
        entrega = {"SQL de recuperación": f"mi_trabajo/sql/{i}.sql", "KPIs": f"mi_trabajo/sql/{i}.sql", "SQL": f"mi_trabajo/sql/{i}.sql",
                   "Python": "mi_trabajo/python/mis_funciones.py", "Pandas": "mi_trabajo/python/mis_funciones.py",
                   "Estadística": f"mi_trabajo/estadistica/{i}.py", "ETL": "mi_trabajo/mini_etl/mini_etl.py"}.get(nuevo.get("familia"))
        return f"python herramientas/corregir_nuevos.py {i} {entrega}" if entrega else ""
    if fam == "SQL":
        return f"python herramientas/corregir_sql.py {i} mi_trabajo/sql/{i}.sql" if i in sql_ctl else f"python herramientas/corregir_nuevos.py {i} mi_trabajo/sql/{i}.sql"
    if fam == "Python":
        return f"python herramientas/corregir_python.py {i} mi_trabajo/python/mis_funciones.py"
    if fam == "Depuracion":
        return f"python herramientas/corregir_depuracion.py {i} mi_trabajo/depuracion/{i}.py"
    if fam == "Puente":
        return f"python herramientas/corregir_mini_etl.py {i}"
    if i in ctx.nucleo["ejercicios_nuevos"] and ctx.nucleo["ejercicios_nuevos"][i].get("familia") in ("Python", "Pandas", "KPIs", "Estadística"):
        return f"python herramientas/corregir_nuevos.py {i} <tu archivo en mi_trabajo/>"
    return ""


def render_normal(ctx, n):
    d = ctx.dias[n]
    f = datetime.date.fromisoformat(d["fecha"])
    dd = f"D{n:02d}"
    ruta = DIAS / f"{dd}_{d['fecha']}.md"
    hechas = hechas_en_guia(ruta)
    t = d["totales"]
    L = [f"# Día {n:02d} · {SEMANA[f.weekday()]} {d['fecha']}", "", f"## {d['titulo']}", "",
         f"**Objetivo de trabajo:** {d['objetivo']}", ""]
    ses = d.get("sesiones")
    carga = f"**Carga BASE: {t['total']} min ({hm(t['total'])}).**"
    if ses:
        if d["tipo"] == "lunes":
            carga += f" Supera el máximo de {d['techo_min']} min de un lunes con clase, por eso está dividida en {len(ses)} sesiones retomables (sección B): puedes usar más de un día real sin cambiar la fecha académica."
        else:
            carga += f" Supera el máximo de {d['techo_min']} min (el objetivo es 240), por eso está dividida en {len(ses)} sesiones retomables (sección B): no es una sola sentada de cuatro horas; puedes usar más de un día real sin cambiar la fecha académica."
    if d["tipo"] == "lunes":
        carga += " Lunes: la clase UAGRM (19:30–22:00) va aparte de este tiempo autónomo."
    L += [carga, f"REFUERZO es voluntario y se cuenta aparte ({d['refuerzo']['min']} min sugeridos como máximo). REDUCIDO y MÍNIMO están al final.", ""]
    # ---------------- A
    L += ["## A. Qué estudiar · lecciones NÚCLEO", "",
          "Lee **toda** la teoría de esta jornada antes de abrir la sección C. Cada lección dice cuánto dura la lectura; las microprácticas esenciales están en C.", ""]
    teoria = 0
    for e in ordenar_lecciones(ctx, d["lecciones"]):
        i = e["id"]
        anc ={"completa": "", "sec.": {"1.2": "preparacion-s1", "7.4": "preparacion-p01", "1.6": "preparacion-s2", "7.5": "preparacion-p03", "7.10": "preparacion-p02", "14.5": "seccion-inicial"}.get(i, ""), "resto": "desarrollo"}[e["parte"]]
        rot = {"completa": "", "sec.": " · solo la sección inicial", "resto": " · resto de la lección (el desarrollo)"}[e["parte"]]
        if i == "14.5":
            rot = " · solo los pasos 1, 2 y 6 del ejemplo"
        comp = COMP_CAP[int(i.split(".")[0])]
        prep = preparacion(ctx, i)
        clave = f"lec:{i}|{e['parte']}"
        cuerpo = f"[{i} · {tit_leccion(ctx, i)}]({enlace(ruta_leccion(ctx, i), anc)}) · NÚCLEO{rot} · lectura {e['lectura_min']} min · Competencia: {comp}" + (f" · Preparación: {prep}" if prep and e["parte"] != "sec." else "")
        L.append(caja(ctx, hechas, clave, cuerpo))
        teoria += e["lectura_min"]
    L += ["", f"Teoría de la jornada: **{teoria} min**.", ""]
    if n >= 15:
        pass
    # ---------------- B
    ent = d.get("entorno_min", 0)
    hay_sql = any(re.match(r"^(S\d+|G\d+|J\d+|K\d+[ab]?|V\d+|E\d+|N\d+|X\d+|CL\d+|KP01)$", e["id"]) for g in d["practica"] for e in g["ejercicios"])
    if t["sql_recuperacion"]:
        nota_sql = "Variantes breves de SQL ya enseñado."
    elif hay_sql:
        nota_sql = "SQL ya integrado en los ejercicios del día; no se duplica."
    else:
        nota_sql = "Sin variante hoy: " + ("lunes de clase UAGRM." if d["tipo"] == "lunes" else "el bloque principal ya contiene SQL.")
    L += ["## B. Distribución neta", "", "|Bloque|Minutos|Qué incluye|", "|---|---:|---|",
          f"|Teoría NÚCLEO|{t['teoria']}|Lectura de las lecciones de la sección A.|",
          f"|Microprácticas esenciales|{t['micropractica']}|Solo los apartados obligatorios (sección C); el resto de cada micropráctica es autocomprobación.|",
          f"|Ejercicios autónomos y casos|{t['ejercicios']}|Ejercicios BASE de la sección C" + (f", incluida la preparación del entorno ({ent} min)." if ent else ".") + "|",
          f"|SQL de recuperación|{t['sql_recuperacion']}|{nota_sql}|",
          f"|Comprobación y criterio|{t['criterio_hitos']}|" + (", ".join(c["id"] for c in d["criterio"]) if d["criterio"] else "Las comprobaciones de cada ejercicio van dentro de su tiempo.") + "|",
          f"|Empleo|{t['empleo']}|{d['empleo']['descripcion']}.|",
          f"|Cierre|{t['cierre']}|Guardar, comprobar y registrar aprendizaje.|",
          f"|**Total BASE**|**{t['total']}**|REFUERZO voluntario no incluido.|", "",
          "Los minutos de ejercicios son el punto medio del rango «Primera vez» de cada enunciado y los de lectura vienen de la cabecera de cada lección: son estimaciones (±35 %), no mediciones. Inicio habitual 13:00; las pausas de diez minutos van fuera del tiempo neto.", ""]
    if ses:
        L += ["**Sesiones retomables**", "", "|Sesión|Min|Qué incluye|Entregable|Punto de interrupción|", "|---|---:|---|---|---|"]
        for s in ses:
            inc = "; ".join(re.sub(r"^(Leer \S+) \S+ ", r"\1 ", a["texto"]) .replace("Micropráctica obligatoria", "Micropráctica") + f" ({a['min']})" for a in s["actividades"])
            L.append(f"|{s['sesion']}|{s['min']}|{inc}|{s['entregable']}|{s['punto_de_interrupcion']}|")
        L.append("")
    # ---------------- C
    L += ["## C. Práctica y archivos", ""] + [f"- {x}" for x in datos_texto(ctx, d)] + [""]
    ant = [m for m in range(n - 1, 0, -1) if m in ctx.dias and ctx.dias[m]["tipo"] in ("normal", "lunes")]
    if ant:
        p = ant[0]
        ids = [e["id"] for g in ctx.dias[p]["practica"] for e in g["ejercicios"]][:6]
        L += [f"**Antes de empezar:** las actividades BASE de D{p:02d} ({', '.join(ids)}) deben estar hechas. Si algo falta, retómalo primero: sigue siendo obligatorio y no pasa a REFUERZO.", ""]
    else:
        L += ["**Antes de empezar:** no se exige conocimiento previo de SQL ni de Python. Lo que ya hiciste en el diseño anterior se conserva marcado.", ""]
    L += ["Todos los ejercicios obligatorios están aquí, **después de toda la teoría**, agrupados por competencia y de menor a mayor dificultad. Un ejemplo resuelto de una lección no sustituye un ejercicio autónomo.", ""]
    grupos = {}
    for e in d["lecciones"]:
        if e["micro_min"]:
            g = GRUPO_CAP[int(e["id"].split(".")[0])]
            grupos.setdefault(g, {"micro": [], "ej": []})["micro"].append(("lec", e))
    for x in d["extras_micro"]:
        ids = re.findall(r"\d+\.\d+", x["texto"])
        for i in ids:
            grupos.setdefault("Python", {"micro": [], "ej": []})["micro"].append(("extra", {"id": i, "micro_min": ctx.lec["lecciones"][i]["micropractica"]["minutos_obligatorios"], "micro_apartados_obligatorios": ctx.lec["lecciones"][i]["micropractica"]["obligatorios"]}))
    for g in d["practica"]:
        grupos.setdefault(g["grupo"], {"micro": [], "ej": []})["ej"] += g["ejercicios"]
    if ent:
        L += ["### Entorno", "", caja(ctx, hechas, f"ent:{dd}", f"Preparar el entorno: crea el `.venv` e instala `requirements.txt`, abre `04_DATASETS/comercial.db` y ejecuta `python herramientas/comprobar_entorno.py` · ENTORNO · {ent} min"), ""]
    for g in GORD:
        if g not in grupos:
            continue
        L += [f"### {g}", ""]
        for kind, e in grupos[g]["micro"]:
            i = e["id"]
            clave = f"mic:{i}"
            ap = e["micro_apartados_obligatorios"]
            lm = ctx.lec["lecciones"][i]["micropractica"]
            cuerpo = f"[Micropráctica {i} · {tit_leccion(ctx, i)}]({enlace(ruta_leccion(ctx, i), 'micropractica')}) · MICROPRÁCTICA ESENCIAL · {e['micro_min']} min · obligatorio{'s' if len(ap) > 1 else ''}: apartado{'s' if len(ap) > 1 else ''} {', '.join(map(str, ap))} (la micropráctica tiene {lm['apartados']})"
            primera = min((p["dia"] for p in ctx.lec["lecciones"][i]["partes"]), default=n)
            if primera < n:
                cuerpo += f" · lección leída en D{primera:02d}"
            L.append(caja(ctx, hechas, clave, cuerpo))
            for a, txt in apartados_micro(ctx, i, ap):
                L.append(f"  - Apartado {a}: {txt}")
            cubre = {a: b for a, b in lm["integrado_en"].items() if not b.startswith(("autocomprobación", "(ampliación"))}
            auto = [a for a, b in lm["integrado_en"].items() if b.startswith(("autocomprobación", "(ampliación"))]
            if cubre:
                ya = {a: b for a, b in cubre.items() if dia_primer_ejercicio(ctx, b) <= n}
                luego = {a: b for a, b in cubre.items() if a not in ya}
                if ya:
                    L.append("  - Los demás apartados quedan como autocomprobación porque ya los entrena: " + ", ".join(f"ap. {a} → {b}" for a, b in ya.items()) + ".")
                if luego:
                    plural = len(luego) > 1
                    L.append(f"  - {'Los apartados' if plural else 'El apartado'} " + ", ".join(luego) + f" {'son' if plural else 'es'} autocomprobación ahora y se {'entrenan' if plural else 'entrena'} más adelante: " + ", ".join(f"ap. {a} → {b} (D{dia_primer_ejercicio(ctx, b):02d})" for a, b in luego.items()) + ".")
            if auto:
                L.append(f"  - Apartado(s) {', '.join(auto)}: autocomprobación dentro de la lección (sin casilla).")
        for e in sorted(grupos[g]["ej"], key=lambda x: (x["nivel"], x["id"])):
            i = e["id"]
            tit, ruta_e, niv, pv, fam = ctx.meta(i)
            tipo = {"original": "OBLIGATORIO", "promovido": "OBLIGATORIO (antes opcional)", "nuevo": "OBLIGATORIO (nuevo)"}.get(e["origen"], "OBLIGATORIO")
            if g == "SQL de recuperación":
                tipo = "SQL DE RECUPERACIÓN"
            cuerpo = f"[{i} · {tit}]({PREF + ruta_e if ruta_e else ''}) · {tipo} · nivel {e['nivel']}/3 · {e['min']} min"
            if i in ctx.nucleo["ejercicios_nuevos"] and ctx.nucleo["ejercicios_nuevos"][i].get("micro_integrada") and g == "SQL de recuperación":
                micro_int = ctx.nucleo["ejercicios_nuevos"][i]["micro_integrada"].strip()
                if micro_int.startswith("("):
                    cuerpo += f" · {micro_int.strip('()')}"
                elif micro_int not in ("—", "-"):
                    cuerpo += f" · integra la micropráctica {micro_int}"
            L.append(caja(ctx, hechas, f"ej:{i}", cuerpo))
            if i in ctx.nucleo["items_proyecto"]:
                it = ctx.nucleo["items_proyecto"][i]
                L.append("  - " + it["nota"] + " " + " ".join(f"[{a}]({b})" for a, b in it["enlaces"]))
        L.append("")
    if d["criterio"]:
        L += ["### Criterio analítico y comprensión", ""]
        for c in d["criterio"]:
            i = c["id"]
            tit, ruta_e, niv, pv, fam = ctx.meta(i)
            L.append(caja(ctx, hechas, f"ej:{i}", f"[{i} · {tit}]({PREF + ruta_e}) · CRITERIO · {c['min']} min"))
        L += ["", "Escribe tu respuesta en `mi_trabajo/analitico/` con el mismo nombre del archivo. No hay corrector: compara con la rúbrica del enunciado y, solo después de escribir, con `08_SOLUCIONES/controles_analitico.md`.", ""]
    # ---------------- D
    L += ["## D. REFUERZO — voluntario", "",
          "Ejercicios **diferentes** de los obligatorios, sobre conocimientos que ya estudiaste. No suman al tiempo BASE, no enseñan nada nuevo y **no sustituyen ninguna actividad pendiente**: lo obligatorio no hecho sigue siendo obligatorio.", ""]
    if d["refuerzo"]["ids"]:
        for i in d["refuerzo"]["ids"]:
            tit, ruta_e, niv, pv, fam = ctx.meta(i)
            mm = ctx.nucleo["ejercicios_nuevos"].get(i, {}).get("min") or pv
            L.append(caja(ctx, hechas, f"ej:{i}", f"[{i} · {tit}]({PREF + ruta_e}) · REFUERZO{' (nuevo)' if i in ctx.nucleo['ejercicios_nuevos'] else ''} · ≈ {mm} min"))
    else:
        L.append("Hoy no se propone REFUERZO: no hay un ejercicio útil sobre lo ya enseñado que no sea una repetición.")
    L.append("")
    # ---------------- E
    L += ["## E. Comprobar y entregar", ""]
    cmds = []
    for g in d["practica"]:
        for e in g["ejercicios"]:
            c = corrector(ctx, e["id"])
            if c:
                cmds.append(f"- `{c}`")
    if cmds:
        L += ["Correctores de hoy (úsalos **después** de tu intento):", ""] + cmds + [""]
    L += ["Los casos, la estadística y las pruebas sin corrector se comparan con su rúbrica y sus controles después de escribir tu respuesta. Excel y Power BI exigen ejecutar la lista manual del enunciado; lo que no ejecutes queda registrado como pendiente.", "",
          "No abras las soluciones antes de intentar. Guarda tu código y tu explicación con tus palabras; anota al menos un error o aprendizaje.", ""]
    for k, txt in enumerate(CHECK_CIERRE):
        txt = txt.replace("{dd}", dd)
        L.append(f"- [{marcar(ctx, hechas, 'gen:' + slug(txt) + '|' + dd)}] {txt} <!--k:gen:{slug(txt)}|{dd}-->")
    const = [a for a in ctx.prog["acreditadas"] if a["clave"].startswith("gen:") and a["dia_original"] == n and slug(CHECK_CIERRE[0]) not in a["clave"] and not any(slug(c.replace("{dd}", dd)) in a["clave"] for c in CHECK_CIERRE)]
    if const:
        L += ["", "**Constancias previas conservadas** (acreditadas en el diseño anterior; no acreditan lecciones ni ejercicios del plan nuevo):", ""]
        for a in const:
            L.append(f"- [x] {a['linea_original']} <!--k:{a['clave']}-->")
    if ses:
        L += ["", "Al cerrar cada sesión: guarda el archivo, el último control y el siguiente paso en `mi_trabajo/dias/" + dd + ".md`."]
    L.append("")
    # ---------------- F
    red, acum = reducido(ctx, n)
    L += ["## F. REDUCIDO", "",
          f"Para un día con menos tiempo: haz una **sesión corta de ≈ {acum} min** con lo primero de la jornada, en este orden, y guarda dónde te quedaste:", ""]
    L += [f"- {a[1]} ({a[2]} min)" for a in red]
    L += ["", "Todo lo que no hagas sigue **OBLIGATORIO PENDIENTE** y se retoma en el siguiente bloque disponible, sin pasar a REFUERZO ni sumarse a otra jornada. REDUCIDO no acredita las competencias pendientes. Mantén el empleo y el cierre en sus bloques; si no caben, registra su siguiente paso.", ""]
    # ---------------- G
    prev_sql = next((e["id"] for m in ant for g in ctx.dias[m]["practica"] if g["grupo"] == "SQL" for e in g["ejercicios"]), None)
    prev_py = next((e["id"] for m in ant for g in ctx.dias[m]["practica"] if g["grupo"] == "Python" for e in g["ejercicios"]), None)
    ej_ant = " o ".join(x for x in (prev_sql, prev_py) if x)
    L += ["## G. MÍNIMO", "",
          "20 minutos = 15 de práctica ya conocida + 5 de cierre. " + (f"Rehaz sin mirar una consulta o función que ya resolviste (por ejemplo {ej_ant}) y explica una decisión." if ej_ant else "Repite sin mirar una consulta o función que ya hayas escrito y explica una decisión."),
          "No acredita contenidos nuevos, no avanza ninguna puerta y no sustituye lo obligatorio de hoy. Si necesitas descansar, el descanso reemplaza la sesión.", ""]
    # ---------------- H
    L += ["## H. Empleo y clase", "", f"{d['empleo']['descripcion']} ({d['empleo']['min']} min).",
          "Publica en LinkedIn solo resultados propios terminados y verificados (consultas explicadas, análisis, paneles, ETL o proyectos); no por calendario. No inventes experiencia."]
    if d["tipo"] == "lunes":
        L.append("Clase UAGRM: lunes 19:30–22:00, fuera del bloque autónomo; lleva una pregunta sobre código propio.")
    L += [f"Pregunta de cierre: {CIERRE_PREGUNTA}", ""]
    return "\n".join(L)


# ---------------------------------------------------------------- examen y domingo
def render_examen(ctx, n):
    d = ctx.dias[n]
    f = datetime.date.fromisoformat(d["fecha"])
    dd = f"D{n:02d}"
    hechas = hechas_en_guia(DIAS / f"{dd}_{d['fecha']}.md")
    cod = d["examen"]["codigo"]
    num = cod[1:]
    hito = d["hito"]["id"] if d.get("hito") else None
    t = d["totales"]
    L = [f"# Día {n:02d} · {SEMANA[f.weekday()]} {d['fecha']}", "", f"## {d['titulo']}", "", f"**Objetivo de trabajo:** {d['objetivo']}", "",
          f"**Carga BASE: {t['total']} min ({hm(t['total'])}).** No hay teoría ni ejercicios nuevos: el sábado prioriza examen y corrección.", "",
          "## A. Qué estudiar · lecciones NÚCLEO", "", "No hay lecciones nuevas en un día de examen. Antes de empezar repasa solo lo que ya estudiaste en la semana; no consultes soluciones.", "",
          "## B. Distribución neta", "", "|Bloque|Minutos|Qué incluye|", "|---|---:|---|"]
    if hito:
        L.append(f"|Hito / criterio|{t['criterio_hitos']}|{hito}: se hace dentro del bloque de criterio de la jornada.|")
    L += [f"|Examen, corrección y simulacro|115|Examen 60 + corrección y explicación oral 25 + simulacro 30.|", f"|Empleo|{t['empleo']}|{d['empleo']['descripcion']}.|", f"|Cierre|{t['cierre']}|Guardar, comprobar y registrar aprendizaje.|",
          f"|**Total BASE**|**{t['total']}**||", "", "Inicio habitual 13:00; las pausas de diez minutos van fuera del tiempo neto.", "",
          "## C. Práctica y archivos", "",
          caja(ctx, hechas, f"ex:{cod}", f"[Examen {cod}]({PREF}03_EJERCICIOS/EXAMENES/{cod}.md) y [simulacro semanal]({PREF}06_ENTREVISTAS/SIMULACRO_{num}.md) · 115 min")]
    if hito:
        tit, ruta_e, *_ = ctx.meta(hito)
        L.append(caja(ctx, hechas, f"ej:{hito}", f"[{hito} · {tit}]({PREF + ruta_e}) · {'HITO DE COMPRENSIÓN' if hito.startswith('H') else 'CRITERIO'} · {d['hito']['min']} min"))
    L += ["", "### Puerta de competencia", "", d["puerta"]["texto"], "",
          "Las fechas son objetivos académicos, no plazos. Si la puerta no se cumple, no avanzas al bloque siguiente: haces REFUERZO de la semana y la secuencia se corre sin acumular horas (ver `01_PLAN_DIARIO/HITOS_Y_RECUPERACION.md`). El contrato, los criterios y las puntuaciones del examen no cambian.", "",
          "## D. REFUERZO — voluntario", "", "No se propone REFUERZO el día del examen. Después de la corrección, usa el REFUERZO de la semana (secciones D de las jornadas anteriores) para lo que falló; no introduce temas nuevos.", "",
          "## E. Comprobar y entregar", "", f"Corrige el examen con `03_EJERCICIOS/EXAMENES/{cod}.md` y los controles de `08_SOLUCIONES/controles_examenes.md` solo **después** de entregar.", ""]
    for txt in CHECK_CIERRE:
        txt = txt.replace("{dd}", dd)
        L.append(f"- [{marcar(ctx, hechas, 'gen:' + slug(txt) + '|' + dd)}] {txt} <!--k:gen:{slug(txt)}|{dd}-->")
    L += ["", "## F. REDUCIDO", "", "60 minutos: haz solo la evaluación del examen, sin consultar nada. La corrección (25 min) y el simulacro (30 min) quedan **pendientes** y se hacen en el siguiente bloque disponible, sin sumar horas a otro día.",
          "Una evaluación sin corrección no cierra la puerta.", "",
          "## G. MÍNIMO", "", "20 minutos: si hoy no puedes hacer el examen, repasa sin mirar un ejercicio ya resuelto y reprograma el examen en el siguiente bloque disponible. No acredita nada.", "",
          "## H. Empleo y clase", "", f"{d['empleo']['descripcion']} ({d['empleo']['min']} min).", f"Pregunta de cierre: {CIERRE_PREGUNTA}", ""]
    return "\n".join(L)


def render_domingo(ctx, n):
    d = ctx.dias[n]
    f = datetime.date.fromisoformat(d["fecha"])
    semana = [m for m in range(n - 6, n) if m in ctx.dias and ctx.dias[m]["tipo"] in ("normal", "lunes") and ctx.dias[m]["refuerzo"]["ids"]]
    ids = [i for m in semana for i in ctx.dias[m]["refuerzo"]["ids"]][:4]
    hechas = hechas_en_guia(DIAS / f"D{n:02d}_{d['fecha']}.md")
    L = [f"# Día {n:02d} · {SEMANA[f.weekday()]} {d['fecha']}", "", "## Domingo flexible: descanso o recuperación voluntaria", "",
         "COMPLETO, REDUCIDO y MÍNIMO: **0 minutos obligatorios**. El descanso es la opción por defecto y no genera deuda: no hay SQL, LinkedIn, REFUERZO ni recuperación obligatoria.",
         "Si tienes energía puedes dedicar **entre 45 y 120 minutos** a UNA de estas opciones. Elige una y no la mezcles con el estudio de otro día.", "",
         caja(ctx, hechas, "dom:descanso", "**Descanso real** (opción por defecto)."),
         caja(ctx, hechas, "dom:recuperacion", "**Recuperación voluntaria (45–90 min):** rehaz sin mirar un REFUERZO o una actividad pendiente de la semana" + (f" (por ejemplo {', '.join(ids)})" if ids else "") + ". No recuperes un día completo."), "",
         "Reglas: si ayer fue examen, no lo revises hoy; no consultes soluciones; no hace falta publicar ni hacer commit; lo que no hagas no se traslada a otro día. Una actividad BASE pendiente sigue siendo obligatoria en su jornada.", "",
         "No requiere entrega. Habilidad: gestionar una carga sostenible.", ""]
    return "\n".join(L)


def render(ctx, n):
    t = ctx.dias[n]["tipo"]
    return {"normal": render_normal, "lunes": render_normal, "examen": render_examen, "domingo": render_domingo}[t](ctx, n)


def parse_dias(txt, ctx):
    if txt is None:
        return list(range(1, 43))
    out = []
    for p in txt.split(","):
        if "-" in p:
            a, b = p.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(p))
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dias")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--comprobar", action="store_true")
    a = ap.parse_args()
    if not a.dias and not a.todos:
        raise SystemExit(__doc__)
    ctx = Ctx()
    cambios = 0
    for n in parse_dias(a.dias, ctx):
        texto = render(ctx, n).rstrip("\n") + "\n"
        ruta = DIAS / f"D{n:02d}_{ctx.dias[n]['fecha']}.md"
        actual = ruta.read_bytes().decode("utf-8-sig").replace("\r\n", "\n") if ruta.exists() else None
        if actual != texto:
            cambios += 1
            if not a.comprobar:
                ruta.write_bytes(texto.encode("utf-8"))
            print(("CAMBIARÍA " if a.comprobar else "escrito ") + ruta.relative_to(RAIZ).as_posix())
    if ctx.sin_archivo:
        print("SIN ARCHIVO de ejercicio:", ", ".join(sorted(ctx.sin_archivo)))
        return 2
    if not a.dias:  # --todos: además de las 42 guías, los documentos derivados
        import derivados_v6
        docs = derivados_v6.todos(ctx, COMP_CAP, actividades, lambda c, n: reducido(c, n)[1], ordenar_lecciones)
        for rel, texto in sorted(docs.items()):
            texto = texto.rstrip("\n") + "\n"
            ruta = RAIZ / rel
            bruto = ruta.read_bytes().decode("utf-8") if ruta.exists() else None
            actual = bruto.replace("\r\n", "\n") if bruto is not None else None
            if actual != texto:
                cambios += 1
                if not a.comprobar:
                    ruta.write_bytes((texto.replace("\n", "\r\n") if bruto and "\r\n" in bruto else texto).encode("utf-8"))  # conserva los saltos de línea del archivo existente
                print(("CAMBIARÍA " if a.comprobar else "escrito ") + rel)
    print(f"Jornadas con cambios: {cambios}")
    return 1 if (a.comprobar and cambios) else 0


if __name__ == "__main__":
    sys.exit(main())
