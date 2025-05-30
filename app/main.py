import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from app.database import initialize_database
from app.features.user import user_router

load_dotenv()

app = FastAPI(    
    title="Medical Internships Platform",
    description="API for managing medical internships and related data",
    version="1.0.0",
    )

# ---------- CORS ----------
origins = [
    "http://localhost:3002",
    "http://127.0.0.1:3002",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Base de datos ----------
@app.on_event("startup")
def startup_db():
    initialize_database()

# ---------- Frontend ----------
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/user", response_class=HTMLResponse)
def serve_user_page():
    return FileResponse("frontend/src/features/user/UserPage.html")

# ---------- API ----------
app.include_router(user_router, tags=["users"])