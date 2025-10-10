from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import report_service


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """Resumo geral do dashboard"""
    return {
        "equipments": {
            "total": report_service.get_total_equipments(db),
            "by_status": report_service.get_total_by_status(db),
            "by_reason": report_service.get_total_by_reason(db),
            "updates_over_time": report_service.get_updates_over_time(db)
        },
        "users": report_service.get_user_summary(db)
    }



@router.get("/by-status")
def get_by_status(db: Session = Depends(get_db)):
    return report_service.get_total_by_status(db)


@router.get("/by-reason")
def get_by_reason(db: Session = Depends(get_db)):
    return report_service.get_total_by_reason(db)


@router.get("/updates")
def get_updates(db: Session = Depends(get_db)):
    return report_service.get_updates_over_time(db)



