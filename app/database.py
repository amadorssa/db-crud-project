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
    CREATE TABLE IF NOT EXISTS unidades (
        unidad_id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) UNIQUE NOT NULL,
        tipo_unidad VARCHAR(100) NOT NULL,
        direccion VARCHAR(255),
        ciudad VARCHAR(50),
        estado VARCHAR(50),
        capacidad INTEGER,
        nombre_contacto VARCHAR(100) NOT NULL,
        email_contacto VARCHAR(50),
        telefono_contacto VARCHAR(15),
        es_disponible BOOLEAN NOT NULL DEFAULT TRUE,
        creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS usuarios (
        expediente_id VARCHAR(50) PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        primer_apellido VARCHAR(50) NOT NULL,
        segundo_apellido VARCHAR(50),
        email VARCHAR(50) UNIQUE NOT NULL,
        contrasena VARCHAR(255) NOT NULL,
        es_admin BOOLEAN NOT NULL DEFAULT FALSE,
        unidad_id INTEGER,
        creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (unidad_id) REFERENCES unidades(unidad_id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS practicas (
        practica_id SERIAL PRIMARY KEY,
        alumno_id VARCHAR(50) NOT NULL,
        unidad_id INTEGER NOT NULL,
        ano INTEGER NOT NULL,
        periodo INTEGER NOT NULL,
        estatus INTEGER NOT NULL,
        creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alumno_id) REFERENCES usuarios(expediente_id) ON DELETE CASCADE,
        FOREIGN KEY (unidad_id) REFERENCES unidades(unidad_id) ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS documentos_practicas (
        documento_id SERIAL PRIMARY KEY,
        practica_id INTEGER NOT NULL,
        tipo_documento VARCHAR(20) NOT NULL,
        ruta VARCHAR(255) NOT NULL,
        es_verificado BOOLEAN NOT NULL DEFAULT FALSE,
        creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (practica_id) REFERENCES practicas(practica_id) ON DELETE CASCADE
    );
"""

def initialize_database():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute(CREATE_TABLES_SQL)
    conn.commit()
    cur.close()
    conn.close()
