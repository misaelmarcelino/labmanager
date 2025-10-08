from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Lab Manager API"
    APP_VERSION: str = "1.0.0"

    DATABASE_POSTGRES_URL: str | None = None
    DATABASE_SQLITE_URL: str | None = None
    DATABASE_ENGINE: str = "sqlite"  # pode ser 'sqlite' ou 'postgres'

    # Segurança
    SECRET_KEY: str
    DEBUG: bool = True
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Servidor
    HOST: str = "127.0.0.1"
    PORT: int = 5000
    RELOAD: bool = True

    # Servidor de e-mail
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    # Servidor Frontend
    FRONTEND_URL: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Retorna automaticamente a URL correta com base no engine ativo.
        """
        if self.DATABASE_ENGINE == "postgres" and self.DATABASE_POSTGRES_URL:
            return self.DATABASE_POSTGRES_URL
        return self.DATABASE_SQLITE_URL or "sqlite:///./labmanager.db"

    class Config:
        env_file = ".env"

settings = Settings()
