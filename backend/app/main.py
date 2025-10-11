from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import equipment_router, report_router, user_router, auth_router


app = FastAPI(title="Lab Manager API")

Base.metadata.create_all(bind=engine)


# Configuração de CORS
origins = [
    "http://localhost:4200",  # frontend Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(equipment_router.router)
app.include_router(report_router.router)


@app.get("/")
def health():
    return {"status": "ok", "message": "Lab Manager API is running! acesse /docs para ver a documentação."}


