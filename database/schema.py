"""
Crea la base de datos y la tabla productos si no existen.
"""
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

CREATE_DB_SQL = "CREATE DATABASE {db};"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS productos (
    id                SERIAL PRIMARY KEY,
    nombre            TEXT        NOT NULL,
    precio_actual     NUMERIC(15, 2),
    precio_anterior   NUMERIC(15, 2),
    descuento         INTEGER,          -- porcentaje, ej: 23
    ubicacion         VARCHAR(200),
    cuotas            VARCHAR(200),
    envio_gratis      BOOLEAN     DEFAULT FALSE,
    enlace            TEXT,
    categoria         VARCHAR(100) NOT NULL,
    fecha_extraccion  TIMESTAMP   NOT NULL
);
"""


def create_database_if_not_exists():
    """
    Conecta al servidor PostgreSQL (base 'postgres') y crea la DB del proyecto
    si no existe todavía.
    """
    db_name = os.getenv("DB_NAME", "ml_scraper")
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        dbname="postgres",          # conectamos a la DB de sistema
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{db_name}";')
        print(f"[DB] Base de datos '{db_name}' creada.")
    else:
        print(f"[DB] Base de datos '{db_name}' ya existe.")

    cur.close()
    conn.close()


def create_tables():
    """Crea la tabla productos dentro de la base de datos del proyecto."""
    from database.connection import get_connection

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()
    print("[DB] Tabla 'productos' lista.")
