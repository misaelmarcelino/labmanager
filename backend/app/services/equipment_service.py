from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.models.equipment import Equipment
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate


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
