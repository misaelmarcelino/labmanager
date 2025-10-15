from apscheduler.schedulers.background import BackgroundScheduler
from app.models.equipment import Equipment
from app.core.database import SessionLocal
from app.services.mail_service import send_equipment_expired_email
from datetime import datetime
import logging

logging.basicConfig(
    filename="logs/job_equipment.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

def check_expired_equipments():
    db = SessionLocal()
    try:
        expired = db.query(Equipment).filter(
            Equipment.data_limite < datetime.utcnow().date(),
            Equipment.is_active == True
        ).all()

        if not expired:
            logger.info("Nenhum equipamento expirado encontrado.")
            return
        
        for eq in expired:
            eq.is_active = False
            db.commit()
            logger.info(f"Equipamento {eq.codigo} desativado por expiração.")



            # ✅ Notificação por e-mail
            try:
                if eq.responsavel:
                    send_equipment_expired_email(
                        email=eq.responsavel,
                        codigo=eq.codigo,
                        nome_posto=eq.nome_do_posto
                    )
                    logger.info(f"E-mail de expiração enviado para {eq.responsavel}.")
                else:
                    logger.warning(f"Equipamento {eq.codigo} sem responsável definido.")
            except Exception as e:
                logger.error(f"Erro ao enviar e-mail para {eq.responsavel}: {e}")

    except Exception as e:
        logger.error(f"Erro ao verificar equipamentos expirados: {e}")
        db.rollback()
    finally:
        db.close()

# Agenda a execução diária
scheduler = BackgroundScheduler()
scheduler.add_job(check_expired_equipments, "interval", hours=24)
