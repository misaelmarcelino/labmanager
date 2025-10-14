from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.core.database import Base, engine
from app.routers import auth_router, user_router, equipment_router, report_router

app = FastAPI(title="Lab Manager API")

# 🔹 Criar tabelas se ainda não existirem
Base.metadata.create_all(bind=engine)

# 🔹 CORS (frontend local e backend servindo build Angular)
origins = [
    "http://localhost:4200",  # ambiente Angular dev
    "http://localhost:5000",  # build Angular servido pelo backend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Routers da API
app.include_router(auth_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(equipment_router.router, prefix="/api")
app.include_router(report_router.router, prefix="/api")

# ===============================================
# SERVIR O FRONTEND ANGULAR
# ===============================================
# Caminho absoluto do diretório 'static'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/app
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")    # backend/static

# Middleware SPA (Angular)
@app.middleware("http")
async def angular_spa_handler(request: Request, call_next):
    path = request.url.path

    # 🔹 Se a rota começar com /api, deixa o backend responder
    if path.startswith("/api"):
        return await call_next(request)

    # 🔹 Caminho do arquivo solicitado
    file_path = os.path.join(STATIC_DIR, path.lstrip("/"))

    # 🔹 Se o arquivo existe, servir diretamente
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # 🔹 Caso contrário, devolver o index.html (rota SPA)
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

# Servir também os arquivos de /assets/
app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")
