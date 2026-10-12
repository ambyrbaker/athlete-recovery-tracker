
from sqlalchemy.orm import Session

from app.models.wellness import WellnessLog
from app.schemas.wellness import WellnessLogCreate


def create_wellness_log(db: Session, wellness: WellnessLogCreate):
    db_log = WellnessLog(**wellness.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_wellness_logs(db: Session):
    return db.query(WellnessLog).order_by(WellnessLog.date.desc(), WellnessLog.id.desc()).all()


def get_wellness_log(db: Session, wellness_id: int):
    return db.query(WellnessLog).filter(
        WellnessLog.id == wellness_id
    ).first()


def update_wellness_log(
    db: Session,
    wellness_id: int,
    wellness: WellnessLogCreate
):
    db_log = get_wellness_log(db, wellness_id)

    if db_log is None:
        return None

    for field, value in wellness.model_dump().items():
        setattr(db_log, field, value)

    db.commit()
    db.refresh(db_log)
    return db_log


def delete_wellness_log(db: Session, wellness_id: int):
    db_log = get_wellness_log(db, wellness_id)

    if db_log is None:
        return False

    db.delete(db_log)
    db.commit()
    return True
