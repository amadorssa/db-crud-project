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
        "es_activo":        payload.get("es_activo", True),
    }

    query ="""
        INSERT INTO documentos_practicas (
            practica_id, tipo_documento, ruta, es_verificado, es_activo,
            creado_el, actualizado_el
        ) 
        VALUES (
            %(practica_id)s, 
            %(tipo_documento)s, 
            %(ruta)s, 
            %(es_verificado)s, 
            %(es_activo)s,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
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
        raise HTTPException(
            status_code=500,
            detail="Error interno al crear el documento."
        )

# ------------------- READ ALL -------------------
@document_router.get("/documents/", status_code=200)
def get_documents(conn=Depends(get_db)):
    query = """
        SELECT * FROM documentos_practicas WHERE es_activo = TRUE ORDER BY documento_id;
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        documents = cur.fetchall()
    return documents

# ------------------- READ ONE -------------------
@document_router.get("/documents/{document_id}/", status_code=200)
def get_document(document_id: int, conn=Depends(get_db)):
    query = """
        SELECT * FROM documentos_practicas
        WHERE documento_id = %s AND es_activo = TRUE;
    """
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
    query = """
        UPDATE documentos_practicas
        SET
    	    practica_id = %s,
            tipo_documento = %s,
            ruta = %s,
            es_verificado = %s,
            es_activo = %s,
            actualizado_el = CURRENT_TIMESTAMP
        WHERE documento_id = %s;
    """
    
    
    document_data = (
        payload.get("practica_id"),
        payload.get("tipo_documento"),
        payload.get("ruta"),
        payload.get("es_verificado", False),
        payload.get("es_activo", True),
        document_id
    )
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, document_data)
        conn.commit()
    
    if cur.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado."
        )



# ------------------- DELETE -------------------
@document_router.delete("/documents/{document_id}/", status_code=200)
def delete_document(document_id: int, conn=Depends(get_db)):
    query = " DELETE FROM documentos_practicas WHERE documento_id = %s;"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (document_id,))
        conn.commit()
