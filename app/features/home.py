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

@home_router.get("/stats/status", status_code=status.HTTP_200_OK)
def get_internships_by_status(conn=Depends(get_db)):
    query = """
        SELECT
            p.estatus,
            COUNT(*) AS cantidad_practicas
        FROM
            practicas p
        GROUP BY
            p.estatus
        ORDER BY
            p.estatus;
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Error fetching stats by estatus: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener estadísticas por estatus.")

@home_router.get("/stats/documents", status_code=status.HTTP_200_OK)
def get_documents_stats(conn=Depends(get_db)):
    query = """
        SELECT
            d.tipo_documento,
            COUNT(*) AS cantidad_documentos
        FROM
            documentos_practicas d
        GROUP BY
            d.tipo_documento
        ORDER BY
            d.tipo_documento;
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Error fetching documents stats: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener estadísticas de documentos.")

@home_router.get("/stats/reports", status_code=status.HTTP_200_OK)
def get_reports_stats(conn=Depends(get_db)):
    query = """
        SELECT
            r.tipo_reporte,
            COUNT(*) AS cantidad_reportes
        FROM
            reportes r
        GROUP BY
            r.tipo_reporte
        ORDER BY
            r.tipo_reporte;
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Error fetching reports stats: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener estadísticas de reportes.")

@home_router.get("/stats/users", status_code=status.HTTP_200_OK)
def get_practices_by_user(conn=Depends(get_db)):
    query = """
        SELECT
            u.expediente_id,
            CONCAT(u.nombre, ' ', u.primer_apellido, ' ', COALESCE(u.segundo_apellido, '')) AS nombre_completo,
            COUNT(p.practica_id) AS cantidad_practicas
        FROM
            usuarios u
        LEFT JOIN
            practicas p ON u.expediente_id = p.alumno_id
        GROUP BY
            u.expediente_id, u.nombre, u.primer_apellido, u.segundo_apellido
        ORDER BY
            cantidad_practicas DESC;
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Error fetching user practices stats: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener estadísticas por alumno.")
