
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud.training_sessions import (
    create_training_session,
    get_training_sessions,
    get_training_session,
    update_training_session,
    delete_training_session,
)
from app.schemas.training_sessions import (
    TrainingSessionCreate,
    TrainingSessionResponse,
)

router = APIRouter(
    prefix="/training",
    tags=["Training"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TrainingSessionResponse, status_code=201)
def create_session(
    training_session: TrainingSessionCreate,
    db: Session = Depends(get_db)
):
    return create_training_session(db, training_session)


@router.get("/", response_model=list[TrainingSessionResponse])
def read_training_sessions(db: Session = Depends(get_db)):
    return get_training_sessions(db)


@router.get("/{training_session_id}", response_model=TrainingSessionResponse)
def read_training_session(
    training_session_id: int,
    db: Session = Depends(get_db)
):
    session = get_training_session(db, training_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Training session not found")
    return session


@router.put("/{training_session_id}", response_model=TrainingSessionResponse)
def update_session(
    training_session_id: int,
    training_session: TrainingSessionCreate,
    db: Session = Depends(get_db)
):
    session = update_training_session(db, training_session_id, training_session)
    if session is None:
        raise HTTPException(status_code=404, detail="Training session not found")
    return session


@router.delete("/{training_session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    training_session_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_training_session(db, training_session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Training session not found")
    return None
