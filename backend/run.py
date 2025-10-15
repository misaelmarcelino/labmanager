import os
import sys
import uvicorn
from alembic import command
from alembic.config import Config
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User, RoleEnum
from app.core.security import hash_password

def run_migrations():
    print("🔄 Executando migrações Alembic via API...")

    # Detecta se está rodando empacotado
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS  # Pasta temporária onde o PyInstaller extrai os arquivos
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    alembic_ini = os.path.join(base_dir, "alembic.ini")

    if not os.path.exists(alembic_ini):
        print(f"⚠️ Arquivo alembic.ini não encontrado em {alembic_ini}")
        return

    alembic_cfg = Config(alembic_ini)

    # 🔧 Corrige manualmente o caminho do diretório migrations
    migrations_path = os.path.join(base_dir, "migrations")
    alembic_cfg.set_main_option("script_location", migrations_path)

    if not os.path.exists(migrations_path):
        print(f"⚠️ Diretório de migrações não encontrado em {migrations_path}")
        return

    # Executa as migrações
    command.upgrade(alembic_cfg, "head")

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
                is_first_access=False
            )
            db.add(admin)
            db.commit()
            print("✅ Admin master criado com sucesso!")
        else:
            print("ℹ️ Admin master já existe.")
    finally:
        db.close()

from colorama import Fore, Style

def run_server():
    reload_mode = settings.RELOAD and not getattr(sys, 'frozen', False)
    print(f"{Fore.CYAN}🚀 Iniciando servidor FastAPI em http://127.0.0.1:{settings.PORT} ...{Style.RESET_ALL}")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=reload_mode)


if __name__ == "__main__":
    run_migrations()
    ensure_admin_exists()
    run_server()
