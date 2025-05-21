import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from app.database import initialize_database
from app.features.user import user_router
from app.features.documents import document_router
from app.features.unit import unit_router
from app.features.internship import internship_router
from app.features.reports_incidents import report_router
from app.features.home import home_router

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

@app.get("/document", response_class=HTMLResponse)
def serve_document_page():
    return FileResponse("frontend/src/features/document/DocumentPage.html")
  
@app.get("/unit", response_class=HTMLResponse)
def serve_unit_page():
    return FileResponse("frontend/src/features/unit/UnitPage.html")

@app.get("/internship", response_class=HTMLResponse)
def serve_internship_page():
    return FileResponse("frontend/src/features/internship/InternshipPage.html")

@app.get("/home", response_class=HTMLResponse)
def serve_home_page():
    return FileResponse("frontend/src/features/home/HomePage.html")

@app.get("/reportes", response_class=HTMLResponse)
def serve_user_page():
    return FileResponse("frontend/src/features/report/ReportPage.html")  

@app.get("/", response_class=HTMLResponse)
def serve_home_page():
    return FileResponse("frontend/src/features/home/HomePage.html")

# ---------- API ----------
app.include_router(user_router, tags=["users"])
app.include_router(unit_router, tags=["units"])
app.include_router(internship_router, tags=["internships"])
app.include_router(document_router, tags=["documents"])
app.include_router(report_router, tags=["reportes"])
app.include_router(home_router, tags=["home"])
