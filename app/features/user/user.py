from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201)
def create_user(payload: dict, conn = Depends(get_db)):
    """
    Crea un nuevo usuario. 
    payload debe incluir:
      expediente_id, nombre, primer_apellido, email, contrasena, foto_perfil
    opcionales: segundo_apellido, es_admin, es_activo
    """
    fields = [
        "expediente_id", "nombre", "primer_apellido", "segundo_apellido",
        "email", "contrasena", "foto_perfil", "es_admin", "es_activo"
    ]
    # Extraemos valores (None si no vienen)
    values = [ payload.get(f) for f in fields ]
    placeholders = ", ".join(["%s"] * len(fields))

    sql = f"""
        INSERT INTO usuarios ({", ".join(fields)})
        VALUES ({placeholders})
        RETURNING usuario_id;
    """
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(sql, values)
        new_id = cur.fetchone()["usuario_id"]
        conn.commit()
        return {"usuario_id": new_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()


@router.get("/")
def list_users(conn = Depends(get_db)):
    """Devuelve todos los usuarios"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM usuarios;")
    users = cur.fetchall()
    cur.close()
    return users


@router.get("/{usuario_id}")
def get_user(usuario_id: int, conn = Depends(get_db)):
    """Devuelve un usuario por su ID"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM usuarios WHERE usuario_id = %s;", (usuario_id,))
    user = cur.fetchone()
    cur.close()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{usuario_id}")
def update_user(usuario_id: int, payload: dict, conn = Depends(get_db)):
    """
    Actualiza campos de un usuario.
    payload puede incluir cualquiera de:
      expediente_id, nombre, primer_apellido, segundo_apellido,
      email, contrasena, foto_perfil, es_admin, es_activo
    """
    allowed = [
        "expediente_id", "nombre", "primer_apellido", "segundo_apellido",
        "email", "contrasena", "foto_perfil", "es_admin", "es_activo"
    ]
    set_clauses = []
    values = []

    for field in allowed:
        if field in payload:
            set_clauses.append(f"{field} = %s")
            values.append(payload[field])

    if not set_clauses:
        raise HTTPException(status_code=400, detail="Nada para actualizar")

    # Actualiza también la columna de timestamp
    set_clauses.append("actualizado_el = CURRENT_TIMESTAMP")

    sql = f"""
        UPDATE usuarios
        SET {", ".join(set_clauses)}
        WHERE usuario_id = %s;
    """
    values.append(usuario_id)

    cur = conn.cursor()
    try:
        cur.execute(sql, values)
        if cur.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        conn.commit()
        return {"detail": "Usuario actualizado"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()


@router.delete("/{usuario_id}", status_code=204)
def delete_user(usuario_id: int, conn = Depends(get_db)):
    """Elimina un usuario por su ID"""
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE usuario_id = %s;", (usuario_id,))
        if cur.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        conn.commit()
    finally:
        cur.close()
