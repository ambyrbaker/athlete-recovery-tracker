from sqlalchemy.orm import Session

from app.models.training_sessions import TrainingSession
from app.schemas.training_sessions import TrainingSessionCreate

def create_training_session(
    db: Session,
    training_session: TrainingSessionCreate #crud function receives user created training session here
):
    db_training_session = TrainingSession( #create sqlalchemy object
        date=training_session.date,
        session_type=training_session.session_type,
        duration_minutes=training_session.duration_minutes,
        rpe=training_session.rpe,
        notes=training_session.notes
    )

    db.add(db_training_session)
    db.commit() #save this training session to database
    db.refresh(db_training_session)

    return db_training_session

def get_training_sessions(db: Session):
    return db.query(TrainingSession).order_by(TrainingSession.date.desc(), TrainingSession.id.desc()).all() #query all the training sessions and return training session records

def get_training_session(db: Session, training_session_id: int):
    return (
        db.query(TrainingSession)
        .filter(TrainingSession.id == training_session_id)
        .first()
    )


def update_training_session(
    db: Session,
    training_session_id: int,
    training_session: TrainingSessionCreate
):
    db_session = get_training_session(db, training_session_id)

    if db_session is None:
        return None

    updates = training_session.model_dump()

    for field, value in updates.items():
        setattr(db_session, field, value)

    db.commit()
    db.refresh(db_session)

    return db_session


def delete_training_session(
    db: Session,
    training_session_id: int
):
    db_session = get_training_session(db, training_session_id)

    if db_session is None:
        return False

    db.delete(db_session)
    db.commit()

    return True
