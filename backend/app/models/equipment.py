from sqlalchemy import Column, DateTime, Integer, String, Enum, Date
from datetime import datetime
from app.core.database import Base
import enum


class ReasonForUseEnum(str, enum.Enum):
    ABASTECE = "ABASTECE"
    ESTACIONE = "ESTACIONE"
    DRIVE = "DRIVE"
    CONCESSIONARIA = "CONCESSIONARIA"
    OUTROS = "OUTROS"


class Equipment(Base):
    __tablename__ = "tb_equipments"

    id = Column(Integer, primary_key=True, index=True)
    nome_do_posto = Column(String, nullable=False)
    razao_uso = Column(Enum(ReasonForUseEnum), nullable=False)
    versao_solucao = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_limite = Column(Date, nullable=False)
    responsavel = Column(String, nullable=False)
    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)