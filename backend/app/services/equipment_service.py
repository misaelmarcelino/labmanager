from sqlalchemy.orm import Session
from app.models.equipment import Equipment
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate


def list_equipments(db: Session):
    return db.query(Equipment).all()


def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()


def create_equipment(db: Session, data: EquipmentCreate, user_id: int):
    equipment = Equipment(**data.dict(), created_by=user_id)
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


def delete_equipment(db: Session, equipment_id: int):
    equipment = get_equipment(db, equipment_id)
    if not equipment:
        return None
    db.delete(equipment)
    db.commit()
    return True
