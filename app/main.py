import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from app.database import initialize_database, get_db
from features.user import user_router

load_dotenv()

app = FastAPI(    
    title="Medical Internships Platform",
    description="API for managing medical internships and related data",
    version="1.0.0",
    )

@app.on_event("startup")
async def initialize_database():
    initialize_database()

app.include_router(user_router, prefix="/usuarios")
