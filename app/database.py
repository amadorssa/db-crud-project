import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS usuarios (
        usuario_id SERIAL PRIMARY KEY,
        expediente_id VARCHAR(50) UNIQUE NOT NULL,
        nombre VARCHAR(50) NOT NULL,
        primer_apellido VARCHAR(50) NOT NULL,
        segundo_apellido VARCHAR(50),
        email VARCHAR(50) UNIQUE NOT NULL,
        contrasena VARCHAR NOT NULL,
        es_admin BOOLEAN NOT NULL DEFAULT FALSE,
        es_activo BOOLEAN NOT NULL DEFAULT TRUE,
        creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
"""

def initialize_database():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute(CREATE_TABLES_SQL)
    conn.commit()
    cur.close()
    conn.close()




