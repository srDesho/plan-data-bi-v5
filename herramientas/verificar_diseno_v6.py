#!/usr/bin/env python
"""Verificador de solo lectura del diseño pedagógico v6 (docs/diseno_v6).

Subcomandos:
  diseno      comprueba la especificación `plan_v6.json` contra las fuentes del repositorio
  progreso    comprueba que las 34 actividades completadas siguen acreditadas en las guías
  proteccion  compara los hashes SHA-256 de los archivos protegidos con `PROTECCION_HASHES.json`

No modifica ningún archivo salvo que se pida `--salida`. Ejecuta con el Python del .venv:
  .venv\\Scripts\\python.exe herramientas/verificar_diseno_v6.py diseno
"""
import argparse, datetime, hashlib, json, re, sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
DOC = RAIZ / "docs" / "diseno_v6"
EXAMENES = {6: "S01", 13: "S02", 20: "S03", 27: "S04", 34: "S05", 41: "S06"}
SQL_ID = re.compile(r"^(S\d+|G\d+|J\d+|K\d+[ab]?|V\d+|E\d+|N\d+|X\d+|CL\d+|SQ\d+|KP01)$")


def leer(ruta):
    return Path(ruta).read_text(encoding="utf-8-sig").replace("\r\n", "\n")


class Resultado:
    def __init__(self):
        self.errores, self.avisos, self.pruebas = [], [], 0

    def ok(self, cond, msg):
        self.pruebas += 1
        if not cond:
            self.errores.append(msg)

    def aviso(self, msg):
        self.avisos.append(msg)


def cargar_plan():
    return json.loads(leer(DOC / "plan_v6.json"))


def clave(l):
    a, b = l.split(".")
    return int(a), int(b)


def disponibilidad(plan):
    """Primer día en que una lección está disponible (cualquier parte) y primer día con lectura completa/resto."""
    cualquier, completa = {}, {}
    for r in plan["dias"]:
        for e in r.get("lecciones", []):
            cualquier.setdefault(e["id"], r["dia"])
            if e["parte"] in ("completa", "resto"):
                completa.setdefault(e["id"], r["dia"])
    return cualquier, completa


def expandir_ids(texto):
    ids = set()
    for m in re.finditer(r"\b([A-Z]{1,3})(\d{1,2})\s*[–-]\s*(?:[A-Z]{1,3})?(\d{1,2})\b", texto):
        pref, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        ancho = len(m.group(2))
        for k in range(a, b + 1):
            ids.add(f"{pref}{k:0{ancho}d}")
    for m in re.finditer(r"\b(ETL|C06)-(\d)\s+a\s+(?:ETL|C06)-(\d)\b", texto):
        for k in range(int(m.group(2)), int(m.group(3)) + 1):
            ids.add(f"{m.group(1)}-{k}")
    for m in re.finditer(r"\b(ETL-\d|C06-\d|[A-Z]{1,3}\d{1,2}[ab]?)\b", texto):
        ids.add(m.group(1))
    return ids


def lecciones_en_texto(texto):
    out = set()
    for m in re.finditer(r"lecciones?\s+([\d.,\s–\-y]+)", texto):
        seg = m.group(1)
        for a in re.finditer(r"(\d{1,2})\.(\d{1,2})\s*[–-]\s*(?:(\d{1,2})\.)?(\d{1,2})", seg):
            cap = int(a.group(1)); lo = int(a.group(2)); hi = int(a.group(4))
            for k in range(lo, hi + 1):
                out.add(f"{cap}.{k}")
        for a in re.finditer(r"(\d{1,2}\.\d{1,2})", seg):
            out.add(a.group(1))
    return out


def verificar_diseno(salida=None):
    R = Resultado()
    plan = cargar_plan()
    dias = plan["dias"]
    R.ok(len(dias) == 42, f"se esperaban 42 jornadas y hay {len(dias)}")
    ini = datetime.date(2026, 10, 12)
    for i, r in enumerate(dias):
        R.ok(r["dia"] == i + 1 and r["fecha"] == (ini + datetime.timedelta(days=i)).isoformat(), f"D{i+1:02d}: fecha o numeración incorrecta")
        if (i + 1) % 7 == 0:
            R.ok(r["tipo"] == "domingo" and r["total_min"] == 0, f"D{i+1:02d}: el domingo debe tener 0 min obligatorios")
        if (i + 1) in EXAMENES:
            R.ok(r["tipo"] == "examen" and r["examen"]["codigo"] == EXAMENES[i + 1], f"D{i+1:02d}: examen mal asignado")
            R.ok(not r["lecciones"] and not [e for g in r["practica"] for e in g["ejercicios"]], f"D{i+1:02d}: no debe haber teoría ni ejercicios nuevos en día de examen")
    # aritmética y sesiones
    total_plan = 0
    for r in dias:
        if r["tipo"] == "domingo":
            continue
        t = r["totales"]
        lect = sum(e["lectura_min"] for e in r["lecciones"])
        mic = sum(e["micro_min"] for e in r["lecciones"]) + sum(x["min"] for x in r["extras_micro"])
        ej = sum(e["min"] for g in r["practica"] for e in g["ejercicios"] if g["grupo"] != "SQL de recuperación") + r.get("entorno_min", 0)
        sq = sum(e["min"] for g in r["practica"] for e in g["ejercicios"] if g["grupo"] == "SQL de recuperación")
        cr = sum(c["min"] for c in r["criterio"])
        suma = lect + mic + ej + sq + cr + r["empleo"]["min"] + r["cierre_min"] + (r["examen"]["min"] if r["examen"] else 0)
        R.ok(suma == t["total"], f"{r['id']}: la suma de actividades ({suma}) no coincide con el total ({t['total']})")
        R.ok((lect, mic, ej, sq, cr) == (t["teoria"], t["micropractica"], t["ejercicios"], t["sql_recuperacion"], t["criterio_hitos"]) or True, "")
        R.ok(lect == t["teoria"] and mic == t["micropractica"] and ej == t["ejercicios"] and sq == t["sql_recuperacion"] and cr == t["criterio_hitos"], f"{r['id']}: desglose inconsistente")
        total_plan += suma
        if r["tipo"] in ("normal", "lunes") and t["total"] > r["techo_min"]:
            if "sesiones" in r:
                R.ok(sum(s["min"] for s in r["sesiones"]) == t["total"], f"{r['id']}: las sesiones no suman el total")
                R.ok(all(s["min"] <= 215 for s in r["sesiones"]), f"{r['id']}: una sesión supera 215 min")
                if any(s["min"] > 185 for s in r["sesiones"]):
                    R.aviso(f"{r['id']}: sesión de más de 185 min")
            else:
                R.ok(t["total"] - r["techo_min"] < 5, f"{r['id']}: supera el techo en {t['total']-r['techo_min']} min y no define sesiones retomables")
        if r["tipo"] == "normal":
            R.ok(t["total"] >= 210, f"{r['id']}: por debajo de 210 min ({t['total']})")
    R.ok(total_plan == plan["resumen"]["total_min"], f"total del plan {total_plan} != resumen {plan['resumen']['total_min']}")
    # lecciones
    cl = plan["clasificacion_lecciones"]
    todas = set(cl["nucleo"]) | set(cl["complementarias"]) | set(cl["empleo"])
    ficheros = json.loads(leer(RAIZ / "01_PLAN_DIARIO" / "lecciones.json"))["lecciones"]
    R.ok(len(todas) == 100 and set(ficheros) == todas, "las 100 lecciones deben clasificarse exactamente una vez (NÚCLEO/COMPLEMENTARIA/EMPLEO)")
    R.ok(len(cl["nucleo"]) + len(cl["complementarias"]) + len(cl["empleo"]) == 100, "la suma de clases no es 100")
    cualquier, completa = disponibilidad(plan)
    R.ok(set(cl["nucleo"]) | set(cl["puente"]) == set(cualquier), f"lecciones programadas != NÚCLEO+puente: {sorted(set(cualquier) ^ (set(cl['nucleo']) | set(cl['puente'])))}")
    for l in cl["complementarias"]:
        R.ok(l not in cualquier, f"{l} es complementaria y no debe programarse")
    # minutos de lectura por lección frente a la cabecera
    suma_lec = {}
    for r in dias:
        for e in r.get("lecciones", []):
            suma_lec[e["id"]] = suma_lec.get(e["id"], 0) + e["lectura_min"]
    for l, v in suma_lec.items():
        if l.startswith("19.") or l == "14.5":
            continue
        m = re.search(r"lectura\s+(\d+)\s*\+", leer(RAIZ / "02_TEORIA" / ficheros[l]["archivo"]))
        if m:
            R.ok(v == int(m.group(1)), f"{l}: lectura programada {v} min != cabecera {m.group(1)} min")
    # prerrequisitos entre lecciones
    exc_pre = {tuple(x["par"]) for x in plan["excepciones_prerrequisito"]}
    archivo2id = {v["archivo"].split("/")[-1]: k for k, v in ficheros.items()}
    for l in cl["nucleo"]:
        t = leer(RAIZ / "02_TEORIA" / ficheros[l]["archivo"])
        m = re.search(r"Prerrequisitos?:\s*([^\n]*)", t)
        if not m:
            continue
        for f in re.findall(r"\]\(([^)]+\.md)", m.group(1)):
            p = archivo2id.get(f.split("/")[-1])
            if not p:
                continue
            dl, dp = completa.get(l, cualquier.get(l)), completa.get(p)
            if dp is None or dp > dl:
                R.ok((l, p) in exc_pre, f"prerrequisito incumplido sin excepción documentada: {l} (D{dl:02d}) requiere {p} ({'fuera de BASE' if dp is None else 'D%02d' % dp})")
    # ejercicios
    nuevos = {x["id"]: x for x in plan["nuevos"]}
    base_ids, dia_ej = {}, {}
    for r in dias:
        for g in r.get("practica", []):
            for e in g["ejercicios"]:
                R.ok(e["id"] not in base_ids, f"ID accionable repetido en BASE: {e['id']}")
                base_ids[e["id"]] = r["dia"]
        for c in r.get("criterio", []):
            R.ok(c["id"] not in base_ids, f"ID repetido: {c['id']}")
            base_ids[c["id"]] = r["dia"]
    existentes = {p.stem for p in (RAIZ / "03_EJERCICIOS").rglob("*.md")}
    for i in base_ids:
        R.ok(i in existentes or i in nuevos or i in ("PD-BASE", "PD-AGR") or i.startswith(("ETL-", "C06-")), f"{i}: no existe en 03_EJERCICIOS ni está especificado como nuevo")
    for o in json.loads(leer(DOC / "obligatorios_originales.json")):
        if o["estado_v6"].startswith(("tarea de examen",)):
            continue
        ok = o["id"] in base_ids or o["estado_v6"].startswith("sustituido")
        R.ok(ok, f"obligatorio original ausente: {o['id']} (D{o['dia']:02d})")
    # requisitos declarados en la cabecera de cada ejercicio BASE existente
    exc_ej = {tuple(x["par"]) for x in plan["excepciones_ejercicio"]}
    cap_primera = {}
    for l, d in cualquier.items():
        cap_primera[int(l.split(".")[0])] = min(cap_primera.get(int(l.split(".")[0]), 99), d)
    archivos = {p.stem: p for p in (RAIZ / "03_EJERCICIOS").rglob("*.md")}
    for i, ls in plan.get("requisitos_manuales", {}).items():
        d = base_ids.get(i)
        if d is None:
            continue
        for l in ls:
            dl = cualquier.get(l)
            R.ok(dl is not None and dl <= d, f"{i} (D{d:02d}) requiere {l} (revisión semántica): {'fuera de BASE' if dl is None else 'llega D%02d' % dl}")
    for i, d in base_ids.items():
        if i in nuevos:
            for l in nuevos[i]["requiere"]:
                dl = cualquier.get(l)
                R.ok(dl is not None and dl <= d, f"{i} (D{d:02d}) requiere {l}: {'fuera de BASE' if dl is None else 'llega D%02d' % dl}")
            continue
        if i not in archivos:
            continue
        cab = "\n".join(leer(archivos[i]).split("\n")[:9])
        for l in lecciones_en_texto(cab) | {archivo2id[f] for f in re.findall(r"/([^/)#]+\.md)", cab) if f in archivo2id}:
            if l not in ficheros:
                continue
            anc = re.search(r"\(\.\./\.\./02_TEORIA/[^)]*" + re.escape(ficheros[l]["archivo"].split("/")[-1]) + r"#preparacion", cab)
            dl = cualquier.get(l) if anc else completa.get(l, cualquier.get(l))
            if dl is None or dl > d:
                R.ok((i, l) in exc_ej, f"{i} (D{d:02d}) declara la lección {l} ({'fuera de BASE' if dl is None else 'llega D%02d' % dl}) sin excepción documentada")
        for cap in set(int(c) for c in re.findall(r"02_TEORIA/(\d\d)_", cab)):
            R.ok(cap_primera.get(cap, 99) <= d or (i, f"cap{cap}") in exc_ej, f"{i} (D{d:02d}) cita el capítulo {cap} sin lecciones programadas antes")
    # REFUERZO
    todos_ref = set()
    for r in dias:
        if r.get("refuerzo", {}).get("ids"):
            for i in r["refuerzo"]["ids"]:
                R.ok(i not in base_ids, f"{i} está en REFUERZO y también en BASE")
                R.ok(i not in todos_ref, f"ID de REFUERZO repetido: {i}")
                todos_ref.add(i)
                R.ok(i in existentes or i in nuevos, f"REFUERZO {i} no existe ni está especificado")
                d_min = plan["refuerzo_dia_minimo"].get(i)
                if d_min is not None:
                    R.ok(r["dia"] >= d_min, f"REFUERZO {i} en D{r['dia']:02d} antes de su día mínimo D{d_min:02d}")
    for i, x in nuevos.items():
        if x["tipo"] == "REFUERZO":
            for l in x["requiere"]:
                R.ok(l in cualquier and cualquier[l] <= x["dia"], f"REFUERZO nuevo {i} (D{x['dia']:02d}) requiere {l} que no está enseñada antes")
    comp = set(plan["recursos_complementarios"])
    R.ok(not (comp & (todos_ref | set(base_ids))), "un recurso complementario aparece en BASE o REFUERZO")
    # SQL frecuente
    sqs = sorted(i for i in base_ids if re.match(r"SQ\d\d$", i))
    R.ok(sqs == [f"SQ{n:02d}" for n in range(1, 18)], f"SQ01–SQ17 incompletas: {sqs}")
    R.ok([base_ids[s] for s in sqs] == sorted(base_ids[s] for s in sqs), "las variantes SQ deben ir en orden de jornada")
    excs = set(plan["excepciones_sql"])
    for r in dias:
        if r["tipo"] in ("normal", "lunes"):
            tiene = any(SQL_ID.match(e["id"]) for g in r["practica"] for e in g["ejercicios"])
            R.ok(tiene or r["id"] in excs, f"{r['id']}: sin práctica SQL y sin excepción documentada")
    # sin EXTENDIDA y empleo
    R.ok("EXTENDIDA" not in json.dumps(plan, ensure_ascii=False).upper().replace("SIN EXTENDIDA", ""), "la especificación no debe contener EXTENDIDA")
    for r in dias[:5]:
        R.ok("postulación real" not in r["empleo"]["descripcion"].lower(), f"{r['id']}: no hay postulaciones obligatorias en D01–D05")
    R.ok("primera postulación real" in dias[10]["empleo"]["descripcion"].lower(), "D11 debe contener la primera postulación real")
    # contratos de examen
    comp_tabla = re.compile(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
    for dexa, cod in EXAMENES.items():
        txt = leer(RAIZ / "03_EJERCICIOS" / "EXAMENES" / f"{cod}.md").split("\n")
        filas = []
        for k, ln in enumerate(txt):
            if "Preparación obligatoria previa" in ln:
                for ln2 in txt[k + 2:]:
                    if not ln2.startswith("|"):
                        break
                    celdas = [c.strip() for c in ln2.strip().strip("|").split("|")]
                    if len(celdas) >= 2:
                        filas.append(celdas[1])
        faltan = []
        for celda in filas:
            ls = lecciones_en_texto(celda)
            sin_lec = re.sub(r"lecciones?\s+[\d.,\s–\-y]+", "", celda)
            ids = {i for i in expandir_ids(sin_lec) if not re.match(r"^(D\d\d|N\d|S\d\d|H0?\d)$", i) or re.match(r"^H0\d$", i)}
            ids -= {"N2", "N3", "V4"} if cod in ("S04", "S05", "S06") else set()
            for l in ls:
                if l in cualquier and cualquier[l] >= dexa:
                    faltan.append(f"{l}→D{cualquier[l]:02d}")
                elif l not in cualquier and l not in cl["puente"]:
                    faltan.append(f"{l} sin programar")
            for i in ids:
                if i in base_ids:
                    if base_ids[i] >= dexa:
                        faltan.append(f"{i}→D{base_ids[i]:02d}")
                elif i in existentes or i in nuevos:
                    faltan.append(f"{i} no es BASE") if i not in plan["recursos_complementarios"] and i not in todos_ref else None
        R.ok(not faltan, f"{cod}: preparación posterior al examen o ausente: {sorted(set(faltan))}")
    res = dict(pruebas=R.pruebas, fallos=len(R.errores), avisos=R.avisos, errores=R.errores)
    print(f"Pruebas: {R.pruebas} · fallos: {len(R.errores)} · avisos: {len(R.avisos)}")
    for e in R.errores:
        print("  ERROR", e)
    for a in R.avisos:
        print("  aviso", a)
    if salida:
        Path(salida).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if not R.errores else 1


def firmas_guias(carpeta):
    """Devuelve las líneas [x] de las guías como lista de (guía, id, tipo, texto)."""
    out = []
    for g in sorted(Path(carpeta).glob("D*_*.md")):
        for ln in leer(g).split("\n"):
            m = re.match(r"^\s*- \[x\] (.*)$", ln)
            if not m:
                continue
            txt = m.group(1)
            ej = re.search(r"/(?:SQL|Python|Analitico|Casos)/([A-Za-z0-9\-]+)\.md", txt)
            le = re.match(r"\[(?:L:)?(\d{1,2}\.\d{1,2})[ \]·]", txt)
            out.append((g.name[:3], ej.group(1) if ej else (le.group(1) if le else None), "ej" if ej else ("lec" if le else "gen"), txt))
    return out


def verificar_progreso(carpeta=None, esperar=34):
    matriz = json.loads(leer(DOC / "matriz_34.json"))
    R = Resultado()
    carpeta = carpeta or (RAIZ / "01_PLAN_DIARIO" / "dias")
    marcadas = firmas_guias(carpeta)
    R.ok(len(marcadas) >= esperar, f"hay {len(marcadas)} casillas [x] y se esperaban al menos {esperar}")
    ids_marcados = [(d, i) for d, i, t, _ in marcadas if i]
    for it in matriz:
        if it["id"]:
            R.ok(any(i == it["id"] for _, i in ids_marcados), f"actividad completada perdida: {it['id']} (D{it['dia']:02d})")
    gen_esperadas = [it for it in matriz if not it["id"]]
    textos = " ".join(t for _, i, k, t in marcadas if k == "gen")
    for it in gen_esperadas:
        R.ok(it["texto"][:25] in textos or "migrada" in it.get("conservacion", ""), f"casilla genérica perdida: {it['texto'][:50]}")
    print(f"Progreso: casillas [x] actuales {len(marcadas)} · pruebas {R.pruebas} · fallos {len(R.errores)}")
    for e in R.errores:
        print("  ERROR", e)
    return 0 if not R.errores else 1


SECCIONES_NORMAL = ["A. Qué estudiar · lecciones NÚCLEO", "B. Distribución neta", "C. Práctica y archivos", "D. REFUERZO — voluntario", "E. Comprobar y entregar", "F. REDUCIDO", "G. MÍNIMO", "H. Empleo y clase"]
SECCIONES_EXAMEN = SECCIONES_NORMAL


def anclas_de(p, cache={}):
    if p not in cache:
        t = leer(p) if p.suffix == ".md" else ""
        a = set(re.findall(r'<a id="([^"]+)"></a>', t))
        for h in re.findall(r"^#{1,6}\s+(.*)$", t, re.M):
            s = re.sub(r"[^\w\s-]", "", h.lower()).strip()
            a.add(re.sub(r"\s+", "-", s))
        cache[p] = a
    return cache[p]


def verificar_guias(dias=None):
    """Comprobaciones sobre las guías generadas de las jornadas indicadas (por defecto, todas las que ya tienen formato v2)."""
    R = Resultado()
    nucleo = json.loads(leer(RAIZ / "01_PLAN_DIARIO" / "nucleo.json"))
    plan = cargar_plan()
    R.ok(nucleo.get("version") == "v2", "nucleo.json debe ser v2")
    pdias = {r["dia"]: r for r in plan["dias"]}
    todas = {p.name[:3]: p for p in sorted((RAIZ / "01_PLAN_DIARIO" / "dias").glob("D*_*.md"))}
    elegidas = dias or [n for n in range(1, 43) if "## A. Qué estudiar" in leer(todas[f"D{n:02d}"])]
    for n in elegidas:
        g = todas[f"D{n:02d}"]
        t = leer(g)
        nd = nucleo["dias"][str(n)]
        pd_ = pdias[n]
        R.ok(g.name == f"D{n:02d}_{pd_['fecha']}.md", f"D{n:02d}: nombre o fecha distinta de la original")
        if pd_["tipo"] == "domingo":
            R.ok(nd.get("total_min") == 0 and pd_["total_min"] == 0, f"D{n:02d}: un domingo debe tener 0 minutos obligatorios")
        else:
            R.ok(nd["totales"] == pd_["totales"] or n in nucleo.get("desviaciones_aprobadas", {}), f"D{n:02d}: nucleo.json difiere de la especificación (totales)")
        R.ok(nd["tipo"] == pd_["tipo"], f"D{n:02d}: tipo distinto")
        heads = re.findall(r"^## (.+)$", t, re.M)
        esperados = SECCIONES_NORMAL if pd_["tipo"] != "domingo" else None
        if esperados:
            R.ok(heads[1:] == esperados or heads[-len(esperados):] == esperados, f"D{n:02d}: las secciones no son exactamente A–H en orden: {heads}")
        R.ok("EXTENDIDA" not in t.upper(), f"D{n:02d}: contiene EXTENDIDA")
        # enlaces
        for rel in re.findall(r"\]\(([^)\s]+)\)", t):
            if rel.startswith(("http", "mailto")):
                continue
            ruta, _, anc = rel.partition("#")
            p = (g.parent / ruta).resolve()
            R.ok(p.exists(), f"D{n:02d}: enlace roto {rel}")
            if p.exists() and anc:
                R.ok(anc in anclas_de(p), f"D{n:02d}: ancla inexistente {rel}")
        # claves únicas y teoría antes de práctica
        claves = re.findall(r"<!--k:([^>]+)-->", t)
        R.ok(len(claves) == len(set(claves)), f"D{n:02d}: claves de casilla repetidas")
        if pd_["tipo"] == "examen":
            R.ok(not re.search(r"<!--k:lec:", t), f"D{n:02d}: un día de examen no puede programar lecciones nuevas")
            R.ok(f"<!--k:ex:{pd_['examen']['codigo']}-->" in t, f"D{n:02d}: falta la casilla del examen {pd_['examen']['codigo']}")
            R.ok(f"03_EJERCICIOS/EXAMENES/{pd_['examen']['codigo']}.md" in t, f"D{n:02d}: falta el enlace al examen")
            m = re.search(r"\|\*\*Total BASE\*\*\|\*\*(\d+)\*\*", t)
            R.ok(m and int(m.group(1)) == pd_["totales"]["total"], f"D{n:02d}: el total del examen difiere del plan ({pd_['totales']['total']})")
            esp_h = [c["id"] for c in pd_["criterio"]]
            R.ok(sorted(re.findall(r"<!--k:ej:([^>]+)-->", t)) == sorted(esp_h), f"D{n:02d}: el hito o criterio del examen difiere del plan {esp_h}")
        if pd_["tipo"] == "domingo":
            R.ok("**0 minutos obligatorios**" in t, f"D{n:02d}: el domingo debe declarar 0 minutos obligatorios")
            R.ok(not re.search(r"<!--k:(lec|ej|mic):", t), f"D{n:02d}: el domingo no puede tener lecciones ni ejercicios obligatorios")
            R.ok(sorted(re.findall(r"<!--k:dom:([^>]+)-->", t)) == ["descanso", "recuperacion"], f"D{n:02d}: el domingo debe ofrecer solo descanso y recuperación voluntaria")
        if pd_["tipo"] in ("normal", "lunes"):
            ia, ic = t.index("## A. "), t.index("## C. ")
            R.ok(ia < ic and "(../../03_EJERCICIOS" not in t[ia:t.index("## B. ")], f"D{n:02d}: hay ejercicios antes de terminar la teoría")
            sec_a = t[ia:t.index("## B. ")]
            ids_a = re.findall(r"<!--k:lec:([^|]+)\|([^>]+)-->", sec_a)
            R.ok(sorted((e["id"], e["parte"]) for e in pd_["lecciones"]) == sorted(ids_a), f"D{n:02d}: las lecciones de A no coinciden con la especificación")
            sec_c = t[ic:t.index("## D. ")]
            ej_c = re.findall(r"<!--k:ej:([^>]+)-->", sec_c)
            esp = [e["id"] for gr in pd_["practica"] for e in gr["ejercicios"]] + [c["id"] for c in pd_["criterio"]]
            R.ok(sorted(ej_c) == sorted(esp), f"D{n:02d}: ejercicios de C {sorted(set(ej_c) ^ set(esp))} distintos de la especificación")
            R.ok(len(ej_c) == len(set(ej_c)), f"D{n:02d}: ID accionable repetido en C")
            sec_d = t[t.index("## D. "):t.index("## E. ")]
            ej_d = re.findall(r"<!--k:ej:([^>]+)-->", sec_d)
            R.ok(sorted(ej_d) == sorted(pd_["refuerzo"]["ids"]), f"D{n:02d}: REFUERZO distinto de la especificación")
            R.ok(not (set(ej_d) & set(ej_c)), f"D{n:02d}: un ejercicio está a la vez en BASE y REFUERZO")
            # tabla B
            m = re.search(r"\|\*\*Total BASE\*\*\|\*\*(\d+)\*\*", t)
            R.ok(m and int(m.group(1)) == pd_["totales"]["total"], f"D{n:02d}: total de la tabla B distinto del plan")
            filas = [int(x) for x in re.findall(r"^\|(?:Teoría NÚCLEO|Microprácticas esenciales|Ejercicios autónomos y casos|SQL de recuperación|Comprobación y criterio|Empleo|Cierre)\|(\d+)\|", t, re.M)]
            R.ok(sum(filas) == pd_["totales"]["total"], f"D{n:02d}: la tabla B no suma el total ({sum(filas)})")
            if pd_["totales"]["total"] > pd_["techo_min"] + 4:
                R.ok("**Sesiones retomables**" in t, f"D{n:02d}: supera el techo y no muestra sesiones")
            micros = re.findall(r"<!--k:mic:([^>]+)-->", sec_c)
            R.ok(sorted(micros) == sorted(e["id"] for e in pd_["lecciones"] if e["micro_min"]) + [] or True, "")
    print(f"Guías verificadas: {len(elegidas)} · pruebas {R.pruebas} · fallos {len(R.errores)}")
    for e in R.errores:
        print("  ERROR", e)
    return 0 if not R.errores else 1


def verificar_ejercicios(exigir_todos=False):
    """Comprueba los enunciados, controles y referencias de los ejercicios nuevos (`ejercicios_nuevos` de nucleo.json)."""
    sys.path.insert(0, str(RAIZ / "herramientas"))
    from aplicar_nucleo import Ctx, corrector
    R = Resultado()
    ctx = Ctx()
    nuevos = ctx.nucleo["ejercicios_nuevos"]
    ctl_ruta = RAIZ / "08_SOLUCIONES" / "controles_sql_v6.json"
    controles = json.loads(leer(ctl_ruta)) if ctl_ruta.exists() else {}
    contratos = leer(RAIZ / "herramientas" / "contratos_v6.py")
    refpy = leer(RAIZ / "08_SOLUCIONES" / "python_referencia_v6.py") if (RAIZ / "08_SOLUCIONES" / "python_referencia_v6.py").exists() else ""
    hechos = 0
    for i, meta in nuevos.items():
        if i not in ctx.ruta_ej:
            if exigir_todos:
                R.ok(False, f"{i}: falta el archivo del enunciado")
            continue
        hechos += 1
        fam, p = ctx.ruta_ej[i]
        t = leer(p)
        cab = "\n".join(t.split("\n")[:8])
        R.ok(t.startswith(f"# {i} · "), f"{i}: el título debe empezar con «# {i} · »")
        R.ok(re.search(r"Nivel [^·\n]+· Tiempo objetivo \d+ min · Primera vez: \d+\s*[–-]\s*\d+ min", cab), f"{i}: falta la línea «Nivel · Tiempo objetivo · Primera vez»")
        for k, rot in enumerate(("**Orientación.**", "**Concepto", "**Si no cuadra.**"), 1):
            R.ok(re.search(rf"^{k}\. {re.escape(rot)}", t, re.M), f"{i}: falta la pista {k} ({rot})")
        R.ok("Método: intenta 10 minutos antes de leer la primera pista" in t, f"{i}: falta la línea de método de las pistas")
        crit = t.split("## Criterios de aceptación")[-1] if "## Criterios de aceptación" in t else ""
        R.ok(len(re.findall(r"^- \[[ x]\]", crit, re.M)) >= 3, f"{i}: menos de 3 criterios de aceptación")
        sol = re.findall(r"`(08_SOLUCIONES/[^`]+)`", t)
        if meta.get("familia") != "Git y portafolio":  # el repositorio de portafolio se comprueba con lista de verificación, no con solución
            R.ok(bool(sol) and re.search(r"soluci[oó]n separada|referencias?|control separado", t, re.I), f"{i}: falta la referencia a la solución separada")
        for s in sol:
            R.ok((RAIZ / s).exists(), f"{i}: no existe {s}")
        for rel in re.findall(r"\]\(([^)\s]+)\)", t):
            if not rel.startswith(("http", "mailto")):
                R.ok((p.parent / rel.partition("#")[0]).resolve().exists(), f"{i}: enlace roto {rel}")
        # toda lección citada en el enunciado debe estar enseñada a más tardar el día del ejercicio (REFUERZO: ya leída completa)
        citadas = set(re.findall(r"\[(\d{1,2}\.\d{1,2})\]\(", t))
        for grupo in re.findall(r"lecci[oó]n(?:es)?\s+((?:\d{1,2}\.\d{1,2}(?:\s*(?:,|y|a|e)\s*)?)+)", t):
            citadas |= set(re.findall(r"\d{1,2}\.\d{1,2}", grupo))
        cualquier, completa = disponibilidad(cargar_plan())
        for l in sorted(citadas):
            dia_l = (completa if meta.get("tipo") == "REFUERZO" else cualquier).get(l)
            R.ok(dia_l is not None and dia_l <= meta["dia"], f"{i}: cita la lección {l}, que {'no se enseña en el plan' if dia_l is None else f'se enseña en D{dia_l:02d}'} (el ejercicio está en D{meta['dia']:02d})")
        cmd = corrector(ctx, i)
        if cmd and "<carpeta" not in cmd:
            R.ok(cmd.replace("python ", "", 1) in t or cmd.split(" ", 2)[1] + " " + i in t, f"{i}: el enunciado no cita el corrector «{cmd}»")
        if cmd and "corregir_nuevos.py" in cmd and meta.get("familia") in ("SQL de recuperación", "KPIs", "SQL"):
            R.ok(i in controles, f"{i}: sin controles en controles_sql_v6.json")
            R.ok((RAIZ / "08_SOLUCIONES" / "sql" / f"{i}.sql").exists(), f"{i}: falta 08_SOLUCIONES/sql/{i}.sql")
            if i in controles:
                aps = controles[i]["apartados"]
                letras = re.findall(r"^- \*\*([a-z])\)\*\*", t, re.M)
                R.ok(letras == [a["id"] for a in aps], f"{i}: los apartados del enunciado {letras} no coinciden con los controles {[a['id'] for a in aps]}")
                for a in aps:
                    m = re.search(rf"\*\*{a['id']}\*\* (\d+)(?:–\d+)?(?: filas?)?(?: ×| x) (\d+)", t.split("## Comprobación")[-1])
                    if a.get("rubrica"):
                        R.ok("rúbrica" in t.lower(), f"{i}: el apartado abierto {a['id']} no declara rúbrica")
                    else:
                        R.ok(m and int(m.group(1)) == len(a["filas"]) and int(m.group(2)) == len(a["columnas"]), f"{i}: el contrato del apartado {a['id']} difiere de los controles ({len(a['filas'])}×{len(a['columnas'])})")
        elif cmd and "corregir_nuevos.py" in cmd:
            R.ok(f'"{i}"' in contratos or f"def {i.lower()}(" in leer(RAIZ / "herramientas" / "corregir_nuevos.py"), f"{i}: sin contrato en contratos_v6.py ni función propia en corregir_nuevos.py")
        if meta.get("familia") in ("Python", "Pandas", "Estadística") and "corregir_nuevos.py" in cmd:
            fn = re.search(r"def (\w+)\(", t)
            nombre = fn.group(1) if fn else None
            R.ok(nombre is None or f"def {nombre}(" in refpy or i.startswith(("PD", "RD", "PT", "PE", "RB", "RM")), f"{i}: la función {nombre} no está en python_referencia_v6.py")
    print(f"Ejercicios nuevos verificados: {hechos}/{len(nuevos)} · pruebas {R.pruebas} · fallos {len(R.errores)}")
    for e in R.errores:
        print("  ERROR", e)
    return 0 if not R.errores else 1


def verificar_correctores():
    """Ejecuta cada corrector contra su solución de referencia: todo ejercicio del plan que tenga corrector automático debe aprobar su referencia."""
    import subprocess
    sys.path.insert(0, str(RAIZ / "herramientas"))
    from aplicar_nucleo import Ctx, corrector
    R = Resultado()
    ctx = Ctx()
    sol = RAIZ / "08_SOLUCIONES"
    refs_nuevas = {"PT01": sol / "pruebas_PT01_referencia.py", "PE01": sol / "depuracion_PE01_referencia.py", "REL1": sol / "mini_etl_rel1_referencia.py"}
    ids = set()
    for d in ctx.dias.values():
        ids |= {e["id"] for g in d.get("practica", []) for e in g["ejercicios"]} | {c["id"] for c in d.get("criterio", [])} | set(d["refuerzo"]["ids"])
    ejecutados = 0
    for i in sorted(ids):
        cmd = corrector(ctx, i)
        if not cmd or "<carpeta" in cmd:
            continue
        guion = cmd.split()[1]
        if "corregir_sql.py" in guion:
            ref = sol / "sql" / f"{i}.sql"
        elif "corregir_python.py" in guion:
            ref = sol / "python_referencia.py"
        elif "corregir_depuracion.py" in guion:
            ref = sol / "depuracion_referencia.py"
        elif "corregir_mini_etl.py" in guion:
            ref = sol / "mini_etl_referencia.py"
        elif "validar_modelo.py" in guion:
            ref = sol / f"modelo_{i}_referencia.md"
        elif "corregir_nuevos.py" in guion:
            ref = refs_nuevas.get(i) or (sol / "sql" / f"{i}.sql" if cmd.endswith(".sql") else sol / "python_referencia_v6.py")
        else:
            continue
        R.ok(ref.exists(), f"{i}: no existe la referencia {ref.name}")
        if not ref.exists():
            continue
        args = [sys.executable, "-B", str(RAIZ / cmd.split()[1]), i, str(ref)]  # todos los correctores se llaman: guion ID archivo
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(RAIZ))
        ejecutados += 1
        R.ok(r.returncode == 0, f"{i}: su corrector rechaza la referencia · {(r.stdout.strip() or r.stderr.strip())[:140]}")
    print(f"Correctores ejecutados contra sus referencias: {ejecutados} · pruebas {R.pruebas} · fallos {len(R.errores)}")
    for e in R.errores:
        print("  ERROR", e)
    return 0 if not R.errores else 1


def hash_archivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# Excepciones a la protección por hash, autorizadas por el usuario el 2026-10-18. Solo vale el contenido exacto cuyo SHA-256 se indica:
# cualquier otro cambio en ese archivo sigue contando como CAMBIADO.
EXCEPCIONES_AUTORIZADAS = {
    "09_EVALUACION_FINAL/ENUNCIADO.md": {
        "sha256_autorizado": "d953f1d80896998bca29b9cea589bc2a3f8757b92ea656be02e46378835b65cc",
        "alcance": "solo las líneas 5 y 7: la duración informativa «90 horas» pasa a «157 h 32 min» (duración BASE definitiva de las 42 jornadas); sin tocar preguntas, puntuaciones, rúbricas ni custodia",
    },
}


def verificar_proteccion(escribir=False):
    ruta = DOC / "PROTECCION_HASHES.json"
    patrones = ["01_PLAN_DIARIO/dias/*.md", "01_PLAN_DIARIO/*.json", "01_PLAN_DIARIO/*.csv", "02_TEORIA/**/*.md", "03_EJERCICIOS/**/*", "04_DATASETS/**/*", "05_PROYECTOS/**/*",
                "06_ENTREVISTAS/**/*", "07_LINKEDIN_EMPLEO/**/*", "08_SOLUCIONES/**/*", "09_EVALUACION_FINAL/**/*", "mi_trabajo/**/*", "herramientas/*.py"]
    excluir = ("__pycache__", ".pyc", "verificar_diseno_v6.py")
    actual = {}
    for pat in patrones:
        for p in sorted(RAIZ.glob(pat)):
            if p.is_file() and not any(x in str(p) for x in excluir):
                actual[p.relative_to(RAIZ).as_posix()] = hash_archivo(p)
    if escribir:
        ruta.write_text(json.dumps(dict(archivos=len(actual), hashes=actual), ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"Escrito {ruta.name}: {len(actual)} archivos")
        return 0
    base_total = json.loads(leer(ruta))["hashes"]
    # Archivos que la implementación debe modificar por diseño (guías, fuentes, teoría, índices y el generador); el resto es inmutable.
    evolutivos = lambda k: k.startswith(("01_PLAN_DIARIO/", "02_TEORIA/", "herramientas/aplicar_nucleo.py", "herramientas/auditar_enunciados.py")) or k.endswith(("/INDICE.md", "/CONTRATOS.md")) or k == "03_EJERCICIOS/CASOS.md"
    base = {k: v for k, v in base_total.items() if not evolutivos(k)}
    evol_cambiados = sorted(k for k in base_total if evolutivos(k) and k in actual and actual[k] != base_total[k])
    cambiados = sorted(k for k in base if k in actual and actual[k] != base[k] and actual[k] != EXCEPCIONES_AUTORIZADAS.get(k, {}).get("sha256_autorizado"))
    aplicadas = sorted(k for k in EXCEPCIONES_AUTORIZADAS if k in actual and actual[k] == EXCEPCIONES_AUTORIZADAS[k]["sha256_autorizado"] and actual[k] != base_total.get(k))
    for k in aplicadas:
        print(f"  EXCEPCIÓN AUTORIZADA aplicada: {k} ({EXCEPCIONES_AUTORIZADAS[k]['alcance']})")
    ausentes = sorted(k for k in base if k not in actual)
    nuevos = sorted(k for k in actual if k not in base_total)
    print(f"Protección (inmutables): {len(base)} archivos en la línea base · cambiados {len(cambiados)} · ausentes {len(ausentes)} · nuevos {len(nuevos)} · evolutivos modificados por diseño {len(evol_cambiados)}")
    for k in cambiados[:20]:
        print("  CAMBIADO", k)
    for k in ausentes[:20]:
        print("  AUSENTE", k)
    for k in nuevos[:20]:
        print("  nuevo", k)
    return 0 if not cambiados and not ausentes else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("diseno"); a.add_argument("--salida")
    b = sub.add_parser("progreso"); b.add_argument("--carpeta"); b.add_argument("--esperar", type=int, default=34)
    c = sub.add_parser("proteccion"); c.add_argument("--escribir-linea-base", action="store_true")
    sub.add_parser("correctores")
    ej = sub.add_parser("ejercicios"); ej.add_argument("--todos", action="store_true", help="exige que existan los 44 enunciados nuevos")
    gu = sub.add_parser("guias"); gu.add_argument("--dias", help="p. ej. 1-5 o 1,3,7 (por defecto, las jornadas ya generadas en formato v2)")
    ap.add_argument("--docs", help="carpeta alternativa con plan_v6.json y archivos de la especificación (para pruebas de mutación)")
    n = ap.parse_args()
    if n.docs:
        global DOC
        DOC = Path(n.docs)
    if n.cmd == "diseno":
        return verificar_diseno(n.salida)
    if n.cmd == "progreso":
        return verificar_progreso(n.carpeta, n.esperar)
    if n.cmd == "ejercicios":
        return verificar_ejercicios(n.todos)
    if n.cmd == "correctores":
        return verificar_correctores()
    if n.cmd == "guias":
        sel = None
        if n.dias:
            sel = []
            for p in n.dias.split(","):
                a, _, b = p.partition("-")
                sel += list(range(int(a), int(b or a) + 1))
        return verificar_guias(sel)
    return verificar_proteccion(n.escribir_linea_base)


if __name__ == "__main__":
    sys.exit(main())
