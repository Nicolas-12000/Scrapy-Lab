"""
Carga el archivo CSV generado por Scrapy hacia la tabla productos en PostgreSQL.
"""
import os
from datetime import datetime

import pandas as pd

from database.connection import get_connection

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "productos.csv")

INSERT_SQL = """
INSERT INTO productos
    (nombre, precio_actual, precio_anterior, descuento,
     ubicacion, cuotas, envio_gratis, enlace, categoria, fecha_extraccion)
VALUES
    (%(nombre)s, %(precio_actual)s, %(precio_anterior)s, %(descuento)s,
     %(ubicacion)s, %(cuotas)s, %(envio_gratis)s, %(enlace)s, %(categoria)s,
     %(fecha_extraccion)s)
ON CONFLICT DO NOTHING;
"""


def load_csv_to_db(csv_path: str = CSV_PATH) -> int:
    """
    Lee el CSV, limpia los datos y los inserta en PostgreSQL.
    Retorna la cantidad de filas insertadas.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"[LOADER] {len(df)} filas leídas desde {csv_path}")

    # --- Limpieza básica ---
    df["nombre"] = df["nombre"].fillna("").str.strip()
    df = df[df["nombre"] != ""]  # descartar filas sin nombre

    df["precio_actual"] = pd.to_numeric(df["precio_actual"], errors="coerce")
    df["precio_anterior"] = pd.to_numeric(df["precio_anterior"], errors="coerce")
    df["descuento"] = pd.to_numeric(df["descuento"], errors="coerce").astype("Int64")

    # Booleano: puede venir como "True"/"False" string
    df["envio_gratis"] = df["envio_gratis"].astype(str).str.lower().isin(
        ["true", "1", "yes", "sí"]
    )

    df["fecha_extraccion"] = pd.to_datetime(
        df["fecha_extraccion"], errors="coerce"
    ).fillna(datetime.utcnow())

    # Convertir NaN de pandas a None (NULL en SQL)
    df = df.where(pd.notnull(df), None)

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    for row in df.to_dict(orient="records"):
        try:
            cur.execute(INSERT_SQL, row)
            inserted += cur.rowcount
        except Exception as exc:
            conn.rollback()
            print(f"  [WARN] Fila saltada: {exc}")
            continue

    conn.commit()
    cur.close()
    conn.close()

    print(f"[LOADER] {inserted} filas insertadas en la base de datos.")
    return inserted
