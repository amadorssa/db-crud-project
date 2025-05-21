from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from app.utils import validate_required_fields

from app.database import get_db

user_router = APIRouter()

# ------------------- CREATE -------------------
@user_router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(payload: dict, conn=Depends(get_db)):
    required = ("expediente_id", "nombre", "primer_apellido", "email", "contrasena")
    validate_required_fields(payload, required)

    user_data = {
        "expediente_id":    payload["expediente_id"],
        "unidad_id":        payload.get("unidad_id"),
        "nombre":           payload["nombre"],
        "primer_apellido":  payload["primer_apellido"],
        "segundo_apellido": payload.get("segundo_apellido"),
        "email":            payload["email"],
        "contrasena":       payload["contrasena"],
        "es_admin":         payload.get("es_admin", False),
        "unidad_id":        payload.get("unidad_id")
    }

    query = """
        INSERT INTO usuarios (
            expediente_id, unidad_id, nombre, primer_apellido, segundo_apellido,
            email, contrasena, es_admin, unidad_id) 
        VALUES (
            %(expediente_id)s, 
            %(unidad_id)s,
            %(nombre)s, 
            %(primer_apellido)s, 
            %(segundo_apellido)s,
            %(email)s, 
            %(contrasena)s, 
            %(es_admin)s, 
            %(unidad_id)s
        );
        """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, user_data)
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
            detail="Error interno al crear el usuario."
        )


# ------------------- READ ALL -------------------
@user_router.get("/users/", status_code=200)
def get_users(conn=Depends(get_db)):
    query = "SELECT * FROM usuarios ORDER BY expediente_id;"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        rows = cur.fetchall()
    return rows


# ------------------- READ ONE -------------------
@user_router.get("/users/{expediente_id}/", status_code=200)
def get_user(expediente_id: str, conn=Depends(get_db)):
    query = "SELECT * FROM usuarios WHERE expediente_id = %s;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (expediente_id,))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return row


# ------------------- UPDATE -------------------
@user_router.put("/users/{expediente_id}/", status_code=200)
def update_user(expediente_id: str, payload: dict, conn=Depends(get_db)):
    if not payload:
        raise HTTPException(status_code=400, detail="Cuerpo vacío")

    required = ("expediente_id", "nombre", "primer_apellido", "email", "contrasena")
    validate_required_fields(payload, required)    
    payload["expediente_id"] = expediente_id
    
    query = """
        UPDATE usuarios 
        SET 
            expediente_id   = %(expediente_id)s,
            unidad_id       = %(unidad_id)s,
            nombre          = %(nombre)s,
            primer_apellido = %(primer_apellido)s,
            segundo_apellido= %(segundo_apellido)s,
            email           = %(email)s,
            contrasena       = %(contrasena)s,
            es_admin        = %(es_admin)s,
            actualizado_el  = CURRENT_TIMESTAMP
        WHERE expediente_id = %(expediente_id)s;
        """
    try:
        with conn.cursor() as cur:
            cur.execute(query, payload)
            # Si no encontró fila para actualizar:
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: expediente_id o email duplicado."
        )
    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error interno al actualizar el usuario."
        )

# ------------------- DELETE -------------------
@user_router.delete("/users/{expediente_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(expediente_id: str, conn=Depends(get_db)):
    query = "DELETE FROM usuarios WHERE expediente_id = %s;"

    with conn.cursor() as cur:
        cur.execute(query, (expediente_id,))
        conn.commit()