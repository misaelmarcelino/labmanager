# app/jobs/job_equipment.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.equipment import Equipment
from app.core.database import SessionLocal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def check_expired_equipments():
    db = SessionLocal()
    try:
        expired = db.query(Equipment).filter(
            Equipment.data_limite < datetime.utcnow().date(),
            Equipment.is_active == True
        ).all()
        for eq in expired:
            eq.is_active = False
            logger.info(f"Equipamento {eq.codigo} desativado por expiração.")
        if expired:
            db.commit()
        else:
            logger.info("Nenhum equipamento expirado encontrado.")
    except Exception as e:
        logger.error(f"Erro ao verificar equipamentos expirados: {e}")
        db.rollback()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(check_expired_equipments, "interval", hours=24)
