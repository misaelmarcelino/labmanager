from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.equipment import Equipment
from app.models.user import User


# ============================================================
# 🧩 EQUIPAMENTOS
# ============================================================
def get_total_equipments(db: Session):
    """Retorna o total de equipamentos"""
    return db.query(func.count(Equipment.id)).scalar()


def get_total_by_status(db: Session):
    """Equipamentos agrupados por status"""
    results = (
        db.query(Equipment.status, func.count(Equipment.id))
        .group_by(Equipment.status)
        .all()
    )
    return [{"status": status, "total": total} for status, total in results]


def get_total_by_reason(db: Session):
    """Equipamentos agrupados por razão de uso"""
    results = (
        db.query(Equipment.razao_uso, func.count(Equipment.id))
        .group_by(Equipment.razao_uso)
        .all()
    )
    return [{"razao_uso": reason.value if hasattr(reason, "value") else reason, "total": total}
            for reason, total in results]


def get_updates_over_time(db: Session):
    """Equipamentos criados agrupados por data"""
    results = (
        db.query(func.date(Equipment.created_at).label("data"), func.count(Equipment.id))
        .group_by(func.date(Equipment.created_at))
        .order_by(func.date(Equipment.created_at))
        .all()
    )
    return [{"data": str(data), "total": total} for data, total in results]


# ============================================================
# 👥 USUÁRIOS
# ============================================================
def get_user_summary(db: Session):
    """Resumo geral de usuários"""
    total_users = db.query(func.count(User.id)).scalar()

    # Considerando que seu User tem um campo `role` ou `is_admin`
    admin_count = db.query(func.count(User.id)).filter(User.role == "admin").scalar()
    regular_count = db.query(func.count(User.id)).filter(User.role == "user").scalar()

    return {
        "total_users": total_users,
        "admins": admin_count,
        "regular_users": regular_count
    }
