from fastapi import FastAPI
from app.core.database import Base, engine, SessionLocal
from app.models.user import User, RoleEnum
from app.core.security import hash_password
from app.routers import user_router, auth_router


app = FastAPI(title="Lab Manager API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}


