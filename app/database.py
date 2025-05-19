import os
from dotenv import load_dotenv   # pip install python-dotenv
from psycopg2.extras import RealDictCursor
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CREATE_TABLES = os.getenv("CREATE_TABLES")

def initialize_database():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute(CREATE_TABLES
    conn.commit()
    cur.close()
    conn.close()


def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()