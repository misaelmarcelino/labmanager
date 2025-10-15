from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.equipment_schema import EquipmentCreate, EquipmentUpdate, EquipmentResponse
from app.services import equipment_service
from app.models.equipment import Equipment

router = APIRouter(prefix="/equipments", tags=["Equipments"])


@router.get("/", response_model=List[EquipmentResponse] )
def list_all_actives(db: Session = Depends(get_db)):
    return equipment_service.list_equipments(db)

@router.get("/all", response_model=List[EquipmentResponse])
def list_all_equipments(db: Session = Depends(get_db)):
    return equipment_service.list_all_equipments(db)

@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_one(equipment_id: int, db: Session = Depends(get_db)):
    equipment = equipment_service.get_equipment(db, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: EquipmentCreate,
    db: Session = Depends(get_db),
):
    return equipment_service.create_equipment(db, data)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db)):
    equipment = equipment_service.update_equipment(db, equipment_id, data)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.delete("/{equipment_id}", status_code=status.HTTP_200_OK)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = equipment_service.deactivate_equipment(db, equipment_id)
    return {"message": "Equipamento desativado com sucesso", "equipment": equipment}

