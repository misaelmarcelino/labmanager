import os
from pathlib import Path
import sys
import uvicorn
from alembic import command
from alembic.config import Config
from app.core.config import Settings, get_settings
from app.core.database import SessionLocal
from app.models.user import User, RoleEnum
from app.core.security import hash_password
from app.shared.config.base_dir import get_base_dir
from app.shared.config.logging import LOGGING_CONFIG
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)

settings = get_settings()


def run_migrations():
    logging.info("🔄 Executando migrações Alembic via API...")
    # print("🔄 Executando migrações Alembic via API...")

    # Detecta se está rodando empacotado
    base_dir = get_base_dir()

    alembic_ini = base_dir / "alembic.ini"

    if not alembic_ini.exists():
        logging.warning(f"⚠️ Arquivo alembic.ini não encontrado em {alembic_ini}")
        # print(f"⚠️ Arquivo alembic.ini não encontrado em {alembic_ini}")
        return

    alembic_cfg = Config(str(alembic_ini))

    # 🔧 Corrige manualmente o caminho do diretório migrations
    migrations_path = base_dir / "migrations"
    alembic_cfg.set_main_option("script_location", str(migrations_path))

    if not os.path.exists(migrations_path):
        logging.warning(f"⚠️ Diretório de migrações não encontrado em {migrations_path}")
        # print(f"⚠️ Diretório de migrações não encontrado em {migrations_path}")
        return

    # Executa as migrações
    command.upgrade(alembic_cfg, "head")

def ensure_admin_exists():
    logging.info("👤 Verificando Admin Master...")
    # print("👤 Verificando Admin Master...")
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.ADMIN_MASTER_EMAIL).first()
        if not existing:
            admin = User(
                name="Administrador Master",
                email= settings.ADMIN_MASTER_EMAIL,
                password=hash_password(settings.ADMIN_MASTER_PASSWORD),
                role=RoleEnum.ADMIN.value,
                is_first_access=False
            )
            db.add(admin)
            db.commit()
            logging.info("✅ Admin master criado com sucesso!")
        else:
            logging.info("ℹ️ Admin master já existe.")
    finally:
        db.close()

from colorama import Fore, Style

def run_server():

    LOG_PATH = get_base_dir() / "logs"
    LOG_PATH.mkdir(exist_ok=True)
    
    reload_mode = settings.RELOAD and not getattr(sys, 'frozen', False)
    logging.info(f"🚀 Iniciando servidor FastAPI em http://{settings.HOST}:{settings.PORT} ...")
    # print(f"{Fore.CYAN}🚀 Iniciando servidor FastAPI em http://127.0.0.1:{settings.PORT} ...{Style.RESET_ALL}")

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=reload_mode, log_config=LOGGING_CONFIG, access_log=True, )


if __name__ == "__main__":
    run_migrations()
    ensure_admin_exists()
    run_server()
