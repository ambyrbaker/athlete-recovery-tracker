from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.api.wellness import get_db
from app.models.pt import PTSession
from app.schemas.pt import PTSessionCreate, PTSessionResponse

router = APIRouter(prefix="/pt", tags=["Physical therapy"])

def find(db, record_id):
    record = db.get(PTSession, record_id)
    if record is None:
        raise HTTPException(404, "PT session not found")
    return record

@router.get("/", response_model=list[PTSessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(PTSession).order_by(PTSession.date.desc(), PTSession.id.desc()).all()

@router.post("/", response_model=PTSessionResponse, status_code=201)
def create_session(payload: PTSessionCreate, db: Session = Depends(get_db)):
    record = PTSession(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/{record_id}", response_model=PTSessionResponse)
def get_session(record_id: int, db: Session = Depends(get_db)):
    return find(db, record_id)

@router.put("/{record_id}", response_model=PTSessionResponse)
def update_session(record_id: int, payload: PTSessionCreate, db: Session = Depends(get_db)):
    record = find(db, record_id)
    for key, value in payload.model_dump().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}", status_code=204)
def delete_session(record_id: int, db: Session = Depends(get_db)):
    db.delete(find(db, record_id))
    db.commit()
    return Response(status_code=204)
