
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud.wellness import (
    create_wellness_log,
    get_wellness_logs,
    get_wellness_log,
    update_wellness_log,
    delete_wellness_log,
)
from app.schemas.wellness import WellnessLogCreate, WellnessLogResponse


router = APIRouter(
    prefix="/wellness",
    tags=["Wellness"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=WellnessLogResponse, status_code=201)
def create_log(
    wellness: WellnessLogCreate,
    db: Session = Depends(get_db)
):
    return create_wellness_log(db, wellness)


@router.get("/", response_model=list[WellnessLogResponse])
def read_logs(db: Session = Depends(get_db)):
    return get_wellness_logs(db)


@router.get("/{wellness_id}", response_model=WellnessLogResponse)
def read_log(wellness_id: int, db: Session = Depends(get_db)):
    log = get_wellness_log(db, wellness_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Wellness log not found")
    return log


@router.put("/{wellness_id}", response_model=WellnessLogResponse)
def update_log(
    wellness_id: int,
    wellness: WellnessLogCreate,
    db: Session = Depends(get_db)
):
    log = update_wellness_log(db, wellness_id, wellness)
    if log is None:
        raise HTTPException(status_code=404, detail="Wellness log not found")
    return log


@router.delete("/{wellness_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(wellness_id: int, db: Session = Depends(get_db)):
    deleted = delete_wellness_log(db, wellness_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Wellness log not found")
    return None
