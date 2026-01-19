from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Lab Manager API"
    APP_VERSION: str = "1.0.0"

    # Database
    DATABASE_ENGINE: str = "sqlite"  # sqlite | postgres
    DATABASE_POSTGRES_URL: str | None = None
    DATABASE_SQLITE_URL: str | None = None

    # Segurança
    SECRET_KEY: str = Field(..., validation_alias="SECRET_KEY")
    DEBUG: bool = True
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Servidor
    HOST: str = "127.0.0.1"
    PORT: int = 5000
    RELOAD: bool = True

    # E-mail
    SMTP_SERVER: str = Field(..., validation_alias="SMTP_SERVER")
    SMTP_PORT: int = Field(..., validation_alias="SMTP_PORT")
    SMTP_SECURITY: str = "STARTTLS"
    SMTP_CREDENTIAL_NAME: Optional[str] = None

    URL: str = Field(..., validation_alias="URL")
    # Frontend
    FRONTEND_URL: str = Field(..., validation_alias="FRONTEND_URL")

    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_ENGINE == "postgres" and self.DATABASE_POSTGRES_URL:
            return self.DATABASE_POSTGRES_URL
        return self.DATABASE_SQLITE_URL or "sqlite:///./labmanager.db"

    class Config:
        env_file = ".env.prod"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore


