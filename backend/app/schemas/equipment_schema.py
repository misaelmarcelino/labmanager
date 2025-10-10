from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class EquipmentStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class EquipmentBase(BaseModel):
    name: str
    serial_number: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    status: Optional[EquipmentStatus] = None


class EquipmentResponse(EquipmentBase):
    id: int
    status: EquipmentStatus
    created_at: datetime

    class Config:
        orm_mode = True
