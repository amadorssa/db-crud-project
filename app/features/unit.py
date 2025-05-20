from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from app.utils import validate_required_fields

from app.database import get_db

unit_router = APIRouter()

# ------------------- CREATE -------------------
@unit_router.post("/units/", status_code=status.HTTP_201_CREATED)
def create_unit(payload: dict, conn=Depends(get_db)):
    required = ("admin_id", "nombre", "tipo_unidad", "nombre_contacto")
    validate_required_fields(payload, required)

    unit_data = {
        "admin_id":    payload["admin_id"],
        "nombre":           payload["nombre"],
        "tipo_unidad":  payload["tipo_unidad"],
        "direccion": payload.get("direccion"),
        "ciudad":            payload.get("ciudad"),
        "estado":       payload.get("estado"),
        "capacidad":         payload.get("capacidad"),
        "nombre_contacto":  payload["nombre_contacto"],
        "email_contacto":   payload.get("email_contacto"),
        "telefono_contacto": payload.get("telefono_contacto"),
        "es_disponible":    payload.get("es_disponible", True),
        "es_activo":        payload.get("es_activo", True),
    }

    query = """
        INSERT INTO unidades (
            admin_id, nombre, tipo_unidad, direccion, ciudad, estado, capacidad,
            nombre_contacto, email_contacto, telefono_contacto,
            es_disponible, es_activo
        ) VALUES (
            %(admin_id)s, %(nombre)s, %(tipo_unidad)s, %(direccion)s, %(ciudad)s,
            %(estado)s, %(capacidad)s, %(nombre_contacto)s, %(email_contacto)s,
            %(telefono_contacto)s, %(es_disponible)s, %(es_activo)s
        );
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, unit_data)
            conn.commit()

    except IntegrityError as e:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: registro duplicado."
        )
    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error interno al crear la unidad."
        )


# ------------------- READ ALL -------------------
@unit_router.get("/units/", status_code=200)
def get_units(conn=Depends(get_db)):
    query = "SELECT * FROM unidades ORDER BY unidad_id;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return rows


# ------------------- READ ONE -------------------
@unit_router.get("/units/{unidad_id}/", status_code=200)
def get_unit(unidad_id: int, conn=Depends(get_db)):
    query = "SELECT * FROM unidades WHERE unidad_id = %s;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (unidad_id,))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return row


# ------------------- UPDATE -------------------
@unit_router.put("/units/{unidad_id}/", status_code=200)
def update_unit(unidad_id: int, payload: dict, conn=Depends(get_db)):
    if not payload:
        raise HTTPException(status_code=400, detail="Cuerpo vacío")

    required = ("admin_id", "nombre", "tipo_unidad", "nombre_contacto")
    validate_required_fields(payload, required)
    payload["unidad_id"] = unidad_id

    query = """
        UPDATE unidades SET
            admin_id = %(admin_id)s,
            nombre = %(nombre)s,
            tipo_unidad = %(tipo_unidad)s,
            capacidad = %(capacidad)s,
            nombre_contacto = %(nombre_contacto)s,
            email_contacto = %(email_contacto)s,
            telefono_contacto = %(telefono_contacto)s,
            es_disponible = %(es_disponible)s,
            es_activo = %(es_activo)s,
            actualizado_el = CURRENT_TIMESTAMP
        WHERE unidad_id = %(unidad_id)s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, payload)
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Unidad no encontrada")
            conn.commit()
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: nombre duplicado o admin_id inválido."
        )
    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error interno al actualizar la unidad."
        )

# ------------------- DELETE -------------------
@unit_router.delete("/units/{unidad_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit(unidad_id: int, conn=Depends(get_db)):
    query = "DELETE FROM unidades WHERE unidad_id = %s;"
    with conn.cursor() as cur:
        cur.execute(query, (unidad_id,))
        conn.commit()
