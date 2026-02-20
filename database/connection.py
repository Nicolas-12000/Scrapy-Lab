"""
Conexión a PostgreSQL usando variables de entorno del .env
"""
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Retorna una conexión activa a PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        dbname=os.getenv("DB_NAME", "ml_scraper"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
