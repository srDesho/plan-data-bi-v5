"""
ETL DE REFERENCIA · NO LO ABRAS ANTES DE INTENTAR EL TUYO (semana 3)
====================================================================
Entrada : datos_practica/etl/ventas_erp_raw.csv  (exportación sucia de un ERP inventado, separador ;)
          datos_practica/etl/vendedores_por_ruta.csv
Salida  : etl_salida.db con tres capas
          - bronze_ventas_raw      : el archivo tal cual llegó
          - silver_ventas          : limpio y tipado
          - gold_ventas_cliente_mes: resumen listo para Power BI
Cuadre  : el total de ventas entregadas debe dar 1 468 924,50 Bs, igual que la consulta J2 en SQL.

Uso:  python etl_referencia.py
"""
import logging
import re
import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "datos_practica" / "etl" / "ventas_erp_raw.csv"
VEND = BASE / "datos_practica" / "etl" / "vendedores_por_ruta.csv"
DB_OUT = BASE / "etl_salida.db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("etl")


# ------------------------------------------------------------------ EXTRACT
def extraer() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(RAW, sep=";", dtype=str, keep_default_na=False)
    vend = pd.read_csv(VEND, sep=";", dtype=str)
    log.info("extraídas %s filas y %s columnas", *raw.shape)
    return raw, vend


# ---------------------------------------------------------------- TRANSFORM
def _parsear_fecha(s: str) -> pd.Timestamp:
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return pd.to_datetime(s, format="%Y-%m-%d")
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s):
        return pd.to_datetime(s, format="%d/%m/%Y")
    if re.fullmatch(r"\d{2}-\d{2}-\d{2}", s):
        return pd.to_datetime(s, format="%d-%m-%y")
    raise ValueError(f"formato de fecha no reconocido: {s!r}")


def transformar(raw: pd.DataFrame, vend: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    for c in df.columns:
        df[c] = df[c].str.strip()

    df["fecha"] = df["fecha"].map(_parsear_fecha)
    df["cliente"] = df["cliente"].str.replace(r"\s+", " ", regex=True).str.title()
    df["ruta"] = df["ruta"].str.upper()
    df["estado"] = df["estado"].str.lower()
    df["cantidad"] = df["cantidad"].astype(float).astype(int)
    df["precio_unitario"] = (
        df["precio_unitario"].str.replace("Bs", "", regex=False).str.replace(",", ".", regex=False).str.strip().astype(float)
    )

    # vendedor vacío: se recupera con la ruta
    ruta_a_vendedor = dict(zip(vend["ruta"], vend["nombre"]))
    vacios = df["vendedor"] == ""
    df.loc[vacios, "vendedor"] = df.loc[vacios, "ruta"].map(ruta_a_vendedor)
    log.info("vendedores recuperados por ruta: %s", int(vacios.sum()))

    antes = len(df)
    df = df.drop_duplicates(subset=["nro_pedido", "producto"])
    log.info("duplicados eliminados: %s", antes - len(df))

    df["monto"] = df["cantidad"] * df["precio_unitario"]
    return df


# ----------------------------------------------------------------- VALIDAR
def validar(df: pd.DataFrame) -> None:
    assert df.isna().sum().sum() == 0, "quedaron nulos"
    assert (df["vendedor"] == "").sum() == 0, "quedaron vendedores vacíos"
    assert set(df["estado"]) == {"entregado", "anulado"}, "estados raros"
    assert df["cliente"].nunique() == 120, "los nombres de cliente no quedaron unificados"
    assert df["nro_pedido"].nunique() == 3600, "faltan o sobran pedidos"
    assert len(df) == 16178, "la cantidad de líneas no cuadra"
    entregado = df.loc[df["estado"] == "entregado", "monto"].sum()
    assert round(entregado, 2) == 1468924.50, f"el total no cuadra: {entregado}"
    log.info("validaciones OK · ventas entregadas = %.2f Bs", entregado)


# -------------------------------------------------------------------- LOAD
def cargar(raw: pd.DataFrame, silver: pd.DataFrame) -> None:
    gold = (
        silver[silver["estado"] == "entregado"]
        .assign(mes=lambda d: d["fecha"].dt.strftime("%Y-%m"))
        .groupby(["cliente", "mes"], as_index=False)
        .agg(pedidos=("nro_pedido", "nunique"), unidades=("cantidad", "sum"), ventas_bs=("monto", "sum"))
    )
    silver_out = silver.assign(fecha=silver["fecha"].dt.strftime("%Y-%m-%d"))
    with sqlite3.connect(DB_OUT) as con:
        raw.to_sql("bronze_ventas_raw", con, if_exists="replace", index=False)
        silver_out.to_sql("silver_ventas", con, if_exists="replace", index=False)
        gold.to_sql("gold_ventas_cliente_mes", con, if_exists="replace", index=False)
    log.info("cargado en %s (bronze %s · silver %s · gold %s filas)", DB_OUT.name, len(raw), len(silver), len(gold))


def main() -> None:
    raw, vend = extraer()
    silver = transformar(raw, vend)
    validar(silver)
    cargar(raw, silver)


if __name__ == "__main__":
    main()
