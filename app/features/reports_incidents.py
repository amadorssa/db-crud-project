from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from app.utils import validate_required_fields

from app.database import get_db

report_router = APIRouter()

# ------------------- CREATE -------------------
@report_router.post("/reportes/", status_code=status.HTTP_201_CREATED)
def create_report(payload: dict, conn=Depends(get_db)):
    requeridos = (
        "alumno_id", "practica_id", "fecha", "unidad",
        "tipo_reporte", "descripcion", "anonimo"
    )
    validate_required_fields(payload, requeridos)

    datos_reporte = {
        "alumno_id":         payload["alumno_id"],
        "practica_id":       payload["practica_id"],
        "fecha":             payload["fecha"],
        "unidad":            payload["unidad"],
        "tipo_reporte":      payload["tipo_reporte"],
        "descripcion":       payload["descripcion"],
        "evidencia":         payload.get("evidencia"),
        "anonimo":           payload["anonimo"],
        "es_abierto":        payload.get("es_abierto", True),
    }

    query = """
        INSERT INTO reportes (
            alumno_id, practica_id, fecha, unidad, tipo_reporte, 
            descripcion, evidencia, anonimo, es_abierto
        ) VALUES (
            %(alumno_id)s, %(practica_id)s, %(fecha)s, %(unidad)s, %(tipo_reporte)s,
            %(descripcion)s, %(evidencia)s, %(anonimo)s, %(es_abierto)s
        );
    """

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, datos_reporte)
            conn.commit()
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: verifique alumno_id o practica_id."
        )
    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error interno al crear el reporte."
        )

# ------------------- READ ALL -------------------
@report_router.get("/reportes/", status_code=200)
def get_report(conn=Depends(get_db)):
    query = "SELECT * FROM reportes ORDER BY reporte_id;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return rows

# ------------------- READ ONE -------------------
@report_router.get("/reportes/{reporte_id}/", status_code=200)
def get_report(reporte_id: int, conn=Depends(get_db)):
    query = "SELECT * FROM reportes WHERE reporte_id = %s;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (reporte_id,))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return row

# ------------------- UPDATE -------------------
@report_router.put("/reportes/{reporte_id}/", status_code=200)
def update_report(reporte_id: int, payload: dict, conn=Depends(get_db)):
    if not payload:
        raise HTTPException(status_code=400, detail="Cuerpo vacío")

    requeridos = (
        "fecha", "tipo_reporte", "descripcion", "anonimo", "es_abierto"
    )
    validate_required_fields(payload, requeridos)
    payload["reporte_id"] = reporte_id

    query = """
        UPDATE reportes SET
            fecha            = %(fecha)s,
            tipo_reporte     = %(tipo_reporte)s,
            descripcion      = %(descripcion)s,
            evidencia        = %(evidencia)s,
            anonimo          = %(anonimo)s,
            es_abierto       = %(es_abierto)s,
            actualizado_el   = CURRENT_TIMESTAMP
        WHERE reporte_id = %(reporte_id)s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, payload)
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Reporte no encontrado")
            conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error interno al actualizar el reporte."
        )

# ------------------- DELETE -------------------
@report_router.delete("/reportes/{reporte_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(reporte_id: int, conn=Depends(get_db)):
    query = "DELETE FROM reportes WHERE reporte_id = %s;"
    with conn.cursor() as cur:
        cur.execute(query, (reporte_id,))
        conn.commit()
