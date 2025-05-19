# app/features/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.extras import RealDictCursor

from app.database import get_db

user_router = APIRouter()

# ------------------- CREATE -------------------
@user_router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(payload: dict, conn=Depends(get_db)):
    required = (
        "expediente_id",
        "nombre",
        "primer_apellido",
        "email",
        "contrasena",
    )
    missing = [f for f in required if f not in payload or payload[f] is None]
    if missing:
        raise HTTPException(
            status_code=400, detail=f"Campos faltantes: {', '.join(missing)}"
        )

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            INSERT INTO usuarios (
                expediente_id, nombre, primer_apellido, segundo_apellido,
                email, contrasena, es_admin, es_activo
            ) VALUES (
                %(expediente_id)s, %(nombre)s, %(primer_apellido)s, %(segundo_apellido)s,
                %(email)s, %(contrasena)s, %(es_admin)s, %(es_activo)s
            )
            RETURNING *;
            """,
            {
                **payload,
                "segundo_apellido": payload.get("segundo_apellido"),
                "es_admin": payload.get("es_admin", False),
                "es_activo": payload.get("es_activo", True),
            },
        )
        row = cur.fetchone()
        conn.commit()
    return row


# ------------------- READ ALL -------------------
@user_router.get("/users/", status_code=200)
def get_users(conn=Depends(get_db)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM usuarios ORDER BY usuario_id;")
        rows = cur.fetchall()
    return rows


# ------------------- READ ONE -------------------
@user_router.get("/users/{usuario_id}/", status_code=200)
def get_user(usuario_id: int, conn=Depends(get_db)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM usuarios WHERE usuario_id = %s;", (usuario_id,))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return row


# ------------------- UPDATE -------------------
@user_router.put("/users/{usuario_id}/", status_code=200)
def update_user(usuario_id: int, payload: dict, conn=Depends(get_db)):
    if not payload:
        raise HTTPException(status_code=400, detail="Cuerpo vacío")

    # Construye dinámicamente el SET columna = valor
    set_parts = ", ".join(f"{k} = %({k})s" for k in payload.keys())

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            f"""
            UPDATE usuarios
            SET {set_parts}, actualizado_el = CURRENT_TIMESTAMP
            WHERE usuario_id = %(usuario_id)s
            RETURNING *;
            """,
            {**payload, "usuario_id": usuario_id},
        )
        row = cur.fetchone()
        conn.commit()

    if row is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return row


# ------------------- DELETE -------------------
@user_router.delete("/users/{usuario_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usuario_id: int, conn=Depends(get_db)):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM usuarios WHERE usuario_id = %s RETURNING usuario_id;",
            (usuario_id,),
        )
        deleted = cur.fetchone()
        conn.commit()

    if deleted is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # 204 → sin cuerpo de respuesta
