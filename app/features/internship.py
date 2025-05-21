from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from app.utils import validate_required_fields

from app.database import get_db

internship_router = APIRouter()

# ------------------- CREATE -------------------
@internship_router.post("/internships/", status_code=status.HTTP_201_CREATED)
def create_internship(payload: dict, conn=Depends(get_db)):
    required = ("alumno_id", "unidad_id", "ano", "periodo", "estatus")
    validate_required_fields(payload, required)

    internship_data = {
        "alumno_id":  payload["alumno_id"],
        "unidad_id":  payload["unidad_id"],
        "ano":        payload["ano"],
        "periodo":    payload["periodo"],
        "estatus":    payload["estatus"]
    }

    query = """
        INSERT INTO practicas (
            alumno_id, unidad_id, ano, periodo, estatus
        ) VALUES (
            %(alumno_id)s,
            %(unidad_id)s,
            %(ano)s,
            %(periodo)s,
            %(estatus)s
        );
    """

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, internship_data)
            conn.commit()
    except IntegrityError as e:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: clave foránea inválida o duplicado."
        )
    except Exception as e:
        conn.rollback()
        print("Error actualizando usuario:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al actualizar el usuario: {e}"
        )

# ------------------- READ ALL -------------------
@internship_router.get("/internships/", status_code=200)
def get_internships(conn=Depends(get_db)):
    query = "SELECT * FROM practicas ORDER BY practica_id;"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return rows

# ------------------- READ ONE -------------------
@internship_router.get("/internships/{practica_id}/", status_code=200)
def get_internship(practica_id: int, conn=Depends(get_db)):
    query = "SELECT * FROM practicas WHERE practica_id = %s;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (practica_id,))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Práctica no encontrada")
    return row

# ------------------- UPDATE -------------------
@internship_router.put("/internships/{practica_id}/", status_code=200)
def update_internship(practica_id: int, payload: dict, conn=Depends(get_db)):
    if not payload:
        raise HTTPException(status_code=400, detail="Cuerpo vacío")

    required = ("alumno_id", "unidad_id", "ano", "periodo", "estatus")
    validate_required_fields(payload, required)

    payload["practica_id"] = practica_id

    query = """
        UPDATE practicas
        SET 
            alumno_id      = %(alumno_id)s,
            unidad_id      = %(unidad_id)s,
            ano            = %(ano)s,
            periodo        = %(periodo)s,
            estatus        = %(estatus)s
        WHERE practica_id = %(practica_id)s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, payload)
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Práctica no encontrada")
            conn.commit()
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: clave foránea inválida o valores duplicados."
        )
    except Exception as e:
        conn.rollback()
        print("Error actualizando usuario:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al actualizar el usuario: {e}"
        )

# ------------------- DELETE -------------------
@internship_router.delete("/internships/{practica_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_internship(practica_id: int, conn=Depends(get_db)):
    query = "DELETE FROM practicas WHERE practica_id = %s;"

    with conn.cursor() as cur:
        cur.execute(query, (practica_id,))
        conn.commit()
