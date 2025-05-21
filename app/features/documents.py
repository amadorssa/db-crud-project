from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from app.utils import validate_required_fields

from app.database import get_db

document_router = APIRouter()


# ------------------- CREATE -------------------
@document_router.post("/documents/", status_code=status.HTTP_201_CREATED)
def create_document(payload: dict, conn=Depends(get_db)):
    required = ("practica_id", "tipo_documento", "ruta")
    validate_required_fields(payload, required)
    
    document_data = {
        "practica_id":      payload["practica_id"],
        "tipo_documento":   payload["tipo_documento"],
        "ruta":             payload["ruta"],
        "es_verificado":    payload.get("es_verificado", False),
    }

    query ="""
        INSERT INTO documentos_practicas (
            practica_id, tipo_documento, ruta, es_verificado
        ) 
        VALUES (
            %(practica_id)s, 
            %(tipo_documento)s, 
            %(ruta)s, 
            %(es_verificado)s
        );
    """
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, document_data)
            conn.commit()
            
    except IntegrityError as e:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Violación de integridad: registro duplicado."
        )
    except Exception as e:
        conn.rollback()
        print("Error actualizando usuario:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al actualizar el usuario: {e}"
        )

# ------------------- READ ALL -------------------
@document_router.get("/documents/", status_code=200)
def get_documents(conn=Depends(get_db)):
    query = "SELECT * FROM documentos_practicas ORDER BY documento_id;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        documents = cur.fetchall()
    return documents

# ------------------- READ ONE -------------------
@document_router.get("/documents/{document_id}/", status_code=200)
def get_document(document_id: int, conn=Depends(get_db)):
    query = "SELECT * FROM documentos_practicas WHERE documento_id = %s;"
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (document_id,))
        document = cur.fetchone()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado."
        )

    return document

# ------------------- UPDATE -------------------
@document_router.put("/documents/{document_id}/", status_code=200)
def update_document(
    document_id: int, 
    payload: dict, 
    conn=Depends(get_db)
):
    if not payload:
        raise HTTPException(status_code=400, detail="Cuerpo vacío")

    required = ("practica_id", "tipo_documento", "ruta", "es_verificado")
    validate_required_fields(payload, required)

    query = """
        UPDATE documentos_practicas
        SET
    	    practica_id = %(practica_id)s,
            tipo_documento = %(tipo_documento)s,
            ruta = %(ruta)s,
            es_verificado = %(es_verificado)s
        WHERE documento_id = %(practica_id)s;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, payload)
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Documento no encontrado")
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
@document_router.delete("/documents/{document_id}/", status_code=200)
def delete_document(document_id: int, conn=Depends(get_db)):
    query = " DELETE FROM documentos_practicas WHERE documento_id = %s;"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (document_id,))
        conn.commit()
