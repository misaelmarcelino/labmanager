from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.models.equipment import Equipment
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate
from app.services.mail_service import send_new_equipment_email

def list_equipments(db: Session):
    return db.query(Equipment).filter(Equipment.is_active == True).all()

def list_all_equipments(db: Session):
    return db.query(Equipment).all()


def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()


def create_equipment(db: Session, data: EquipmentCreate):
    equipment_data = data.dict()
    equipment = Equipment(**equipment_data)
    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    recipients = ["misael.marcelino@corpay.com.br"]


    recipients = list(set([recipient for recipient in recipients if recipient]))

    # ✅ Envia e-mail automático ao responsável
    try:
        if equipment.responsavel:
            send_new_equipment_email(
                recipients=recipients,
                codigo=equipment.codigo,
                nome_posto=equipment.nome_do_posto,
                razao_uso=equipment.razao_uso.value if hasattr(equipment.razao_uso, "value") else equipment.razao_uso,
                versao_solucao=equipment.versao_solucao,
                descricao=equipment.descricao,
                data_limite=equipment.data_limite.strftime("%d/%m/%Y")
            )
    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail de novo equipamento: {e}")

    return equipment


def update_equipment(db: Session, equipment_id: int, data: EquipmentUpdate):
    equipment = get_equipment(db, equipment_id)
    if not equipment:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(equipment, key, value)
    db.commit()
    db.refresh(equipment)
    return equipment


def deactivate_equipment(db: Session, equipment_id: int):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipamento não encontrado")

    equipment.is_active = False

    db.commit()
    db.refresh(equipment)
    return equipment


