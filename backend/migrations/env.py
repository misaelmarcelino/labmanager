from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.database import Base
from app.models.user import User  # importe todos os modelos aqui
from app.core.config import get_settings

settings = get_settings()

# Configuração do arquivo ini
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Definir o metadata do SQLAlchemy
target_metadata = Base.metadata

# Atualiza a string de conexão do Alembic
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

def run_migrations_offline():
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), #type: ignore[arg-type]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
