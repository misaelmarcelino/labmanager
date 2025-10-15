from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class ReasonForUseEnum(str, Enum):
    ABASTECE = "ABASTECE"
    ESTACIONE = "ESTACIONE"
    DRIVE = "DRIVE"
    CONCESSIONARIA = "CONCESSIONARIA"
    OUTROS = "OUTROS"


class EquipmentStatus(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"


# 🔹 Base comum
class EquipmentBase(BaseModel):
    codigo: str
    nome_do_posto: str
    razao_uso: ReasonForUseEnum
    versao_solucao: str
    descricao: str
    data_limite: date
    responsavel: str
    status: EquipmentStatus = EquipmentStatus.PENDENTE


# 🔹 Criação
class EquipmentCreate(EquipmentBase):
    pass


# 🔹 Atualização
class EquipmentUpdate(BaseModel):
    codigo: Optional[str] = None
    nome_do_posto: Optional[str] = None
    razao_uso: Optional[ReasonForUseEnum] = None
    versao_solucao: Optional[str] = None
    descricao: Optional[str] = None
    data_limite: Optional[date] = None
    responsavel: Optional[str] = None
    status: Optional[EquipmentStatus] = None


# 🔹 Resposta
class EquipmentResponse(EquipmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
