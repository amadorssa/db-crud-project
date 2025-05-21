from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor

from app.database import get_db

home_router = APIRouter()

@home_router.get("/stats", status_code=status.HTTP_201_CREATED)
def get_internships_by_unit_type_stats(conn=Depends(get_db)):
    query = """
        SELECT
            u.tipo_unidad,
            COUNT(p.practica_id) AS cantidad_practicas
        FROM
            unidades u
        LEFT JOIN
            practicas p ON u.unidad_id = p.unidad_id
        GROUP BY
            u.tipo_unidad
        ORDER BY
            u.tipo_unidad;
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            stats = cur.fetchall()
        return stats
    except Exception as e:
        print(f"Error fetching internship stats by unit type: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener estadísticas de prácticas por tipo de unidad."
        )