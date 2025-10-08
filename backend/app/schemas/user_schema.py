from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum = RoleEnum.USER # Padrão é 'USER'

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

class UserSelfUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True

class UserCreateResponse(BaseModel):
    message: str
    user: UserResponse