import subprocess
import uvicorn
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User, RoleEnum
from app.core.security import hash_password

def run_migrations():
    print("🔄 Executando migrações Alembic...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Migrações aplicadas com sucesso!")
    except subprocess.CalledProcessError as e:
        print("❌ Erro ao aplicar migrações:", e)

def ensure_admin_exists():
    print("👤 Verificando Admin Master...")
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@labmanager.com").first()
        if not existing:
            admin = User(
                name="Administrador Master",
                email="admin@labmanager.com",
                password=hash_password("admin123"),
                role=RoleEnum.ADMIN.value,
            )
            db.add(admin)
            db.commit()
            print("✅ Admin master criado com sucesso!")
        else:
            print("ℹ️ Admin master já existe.")
    finally:
        db.close()

def run_server():
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)

if __name__ == "__main__":
    run_migrations()
    ensure_admin_exists()
    run_server()
