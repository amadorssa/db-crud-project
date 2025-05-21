from typing import Iterable, Tuple, Dict, Any
from fastapi import HTTPException
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor
from datetime import datetime

def validate_required_fields(payload: Dict, required_fields: Iterable[str]) -> None:
    missing = [f for f in required_fields if not payload.get(f)]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Campos faltantes: {', '.join(missing)}"
        )


def get_current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
