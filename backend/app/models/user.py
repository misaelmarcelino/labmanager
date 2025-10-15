from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, func, text
from app.core.database import Base
import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "tb_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)

    # ✅ Campos novos (com server_default compatível com SQLite)
    is_first_access = Column(Boolean, default=True, server_default=text("1"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=func.now(), nullable=False)
