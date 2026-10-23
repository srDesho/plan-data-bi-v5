"""Referencias de los ejercicios nuevos del plan v6 (Python). Ábrelo solo después de tu intento."""


def con_descuento(precio, porcentaje):  # RP01
    if porcentaje < 0 or porcentaje > 100:
        return None
    return round(precio * (1 - porcentaje / 100), 2)


def clasificar_stock(stock, minimo):  # RP02
    if stock is None or minimo is None:
        return "sin dato"
    if stock == 0:
        return "agotado"
    if stock < minimo:
        return "reponer"
    return "ok"


def unidades_por_categoria(lineas):  # RP03
    totales = {}
    for categoria, unidades in lineas:
        totales[categoria] = totales.get(categoria, 0) + unidades
    return totales


def mejor_tienda(registros):  # RP04
    totales = {}
    for r in registros:
        totales[r["tienda"]] = totales.get(r["tienda"], 0) + r["ventas"]
    if not totales:
        return None
    mejor = None
    for tienda in sorted(totales):
        if mejor is None or totales[tienda] > totales[mejor]:
            mejor = tienda
    return (mejor, totales[mejor])


def leer_inventario(ruta):  # RP05
    import csv
    validas, rechazadas = [], []
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        lector = csv.reader(archivo)
        cabecera = next(lector)
        for fila in lector:
            if not fila:
                continue
            linea = lector.line_num
            if len(fila) != len(cabecera):
                rechazadas.append((linea, "columnas incorrectas"))
                continue
            if any(campo.strip() == "" for campo in fila):
                rechazadas.append((linea, "campo vacío"))
                continue
            try:
                numeros = [int(campo) for campo in fila]
            except ValueError:
                rechazadas.append((linea, "no numérico"))
                continue
            if any(x < 0 for x in numeros):
                rechazadas.append((linea, "negativo"))
                continue
            validas.append(dict(zip(cabecera, numeros)))
    return validas, rechazadas


def tabla_frecuencias(valores):  # RS01
    conteo = {}
    for v in valores:
        conteo[v] = conteo.get(v, 0) + 1
    total = len(valores)
    filas = [(k, f, round(100 * f / total, 1)) for k, f in conteo.items()]
    return sorted(filas, key=lambda t: (-t[1], t[0]))


def filtrar_entregas(pedidos, clientes, ruta, mes):  # PD01
    ids = clientes.loc[clientes["ruta"] == ruta, "cliente_id"]
    mascara = (pedidos["estado"] == "entregado") & pedidos["cliente_id"].isin(ids) & pedidos["fecha"].astype(str).str.startswith(mes)
    columnas = ["pedido_id", "cliente_id", "fecha"]
    return pedidos.loc[mascara, columnas].sort_values(["fecha", "pedido_id"]).reset_index(drop=True)


def productos_a_reponer(inventario):  # RD01
    d = inventario.loc[inventario["salidas_unidades"] > inventario["stock_final"], ["producto_id", "salidas_unidades", "stock_final"]].copy()
    d["diferencia"] = d["salidas_unidades"] - d["stock_final"]
    return d.sort_values(["diferencia", "producto_id"], ascending=[False, True]).reset_index(drop=True)


def resumen_centro_dispersion(valores):  # RS02
    n = len(valores)
    ordenados = sorted(valores)
    media = sum(valores) / n
    mitad = n // 2
    mediana = ordenados[mitad] if n % 2 else (ordenados[mitad - 1] + ordenados[mitad]) / 2
    if n < 2:
        desviacion = cv = None
    else:
        desviacion = (sum((x - media) ** 2 for x in valores) / (n - 1)) ** 0.5
        cv = None if media == 0 else desviacion / media
    return {"n": n, "media": round(media, 2), "mediana": round(mediana, 2),
            "desviacion": None if desviacion is None else round(desviacion, 2), "cv": None if cv is None else round(cv, 3)}


def limpiar_ventas(df):  # RD02
    import math
    import re
    from datetime import datetime
    import pandas as pd
    validas, rechazadas = [], []
    for fila in df.to_dict("records"):
        motivos = []
        fecha = str(fila["fecha"]).strip()
        iso = None
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
            formato = "%Y-%m-%d"
        elif re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha):
            formato = "%d/%m/%Y"
        else:
            formato = None
        if formato:
            try:
                iso = datetime.strptime(fecha, formato).strftime("%Y-%m-%d")
            except ValueError:
                iso = None
        if iso is None:
            motivos.append("fecha")
        texto = str(fila["monto"]).strip().replace("Bs", "").strip()
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")
        try:
            monto = float(texto)
            if not math.isfinite(monto) or monto < 0:
                raise ValueError(texto)
        except ValueError:
            monto = None
            motivos.append("monto")
        if motivos:
            rechazadas.append({"id": fila["id"], "fecha": fila["fecha"], "monto": fila["monto"], "motivo": ";".join(motivos)})
        else:
            validas.append({"id": fila["id"], "fecha": iso, "monto": monto})
    return (pd.DataFrame(validas, columns=["id", "fecha", "monto"]),
            pd.DataFrame(rechazadas, columns=["id", "fecha", "monto", "motivo"]))


def cercas_tukey(valores):  # RS03
    n = len(valores)
    if n < 4:
        raise ValueError("se necesitan al menos 4 datos")
    ordenados = sorted(valores)

    def percentil(p):
        posicion = (n - 1) * p / 100
        base = int(posicion)
        resto = posicion - base
        if base + 1 < n:
            return ordenados[base] + resto * (ordenados[base + 1] - ordenados[base])
        return ordenados[base]

    q1, q3 = percentil(25), percentil(75)
    iqr = q3 - q1
    inferior, superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return {"q1": round(q1, 2), "q3": round(q3, 2), "iqr": round(iqr, 2),
            "cerca_inferior": round(inferior, 2), "cerca_superior": round(superior, 2),
            "atipicos": sum(1 for x in valores if x < inferior or x > superior)}


def ic_media(valores, confianza=0.95):  # RS04
    from scipy import stats
    n = len(valores)
    if n < 2:
        raise ValueError("se necesitan al menos 2 datos")
    media = sum(valores) / n
    error = stats.sem(valores)
    inferior, superior = stats.t.interval(confianza, n - 1, loc=media, scale=error)
    return {"n": n, "media": round(media, 2), "error_estandar": round(float(error), 3),
            "inferior": round(float(inferior), 2), "superior": round(float(superior), 2)}


def compara_con_meta(valores, meta, confianza=0.95):  # RS04
    ic = ic_media(valores, confianza)
    if meta < ic["inferior"]:
        return "por encima de la meta"
    if meta > ic["superior"]:
        return "por debajo de la meta"
    return "no distinguible de la meta"


def prueba_permutacion(a, b, repeticiones=10000, semilla=None):  # RS05
    import random
    if not a or not b:
        raise ValueError("los dos grupos necesitan datos")
    azar = random.Random(semilla)
    observada = sum(a) / len(a) - sum(b) / len(b)
    junto = list(a) + list(b)
    na = len(a)
    extremos = 0
    for _ in range(repeticiones):
        azar.shuffle(junto)
        dif = sum(junto[:na]) / na - sum(junto[na:]) / (len(junto) - na)
        if abs(dif) >= abs(observada) - 1e-9:
            extremos += 1
    return {"diferencia": round(observada, 2), "p_valor": (extremos + 1) / (repeticiones + 1)}


def welch_y_efecto(a, b):  # RS06
    from scipy import stats
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        raise ValueError("cada grupo necesita al menos 2 datos")
    ma, mb = sum(a) / na, sum(b) / nb
    va = sum((x - ma) ** 2 for x in a) / (na - 1)
    vb = sum((x - mb) ** 2 for x in b) / (nb - 1)
    dif = ma - mb
    ee = (va / na + vb / nb) ** 0.5
    gl = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    prueba = stats.ttest_ind(a, b, equal_var=False)
    critico = stats.t.ppf(0.975, gl)
    return {"diferencia": round(dif, 2), "t": round(float(prueba.statistic), 3), "gl": round(gl, 1), "p_valor": round(float(prueba.pvalue), 4),
            "ic_inferior": round(dif - critico * ee, 2), "ic_superior": round(dif + critico * ee, 2), "dif_relativa_pct": round(100 * dif / mb, 1)}
