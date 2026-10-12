from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class TrainingSession(Base): #defining the training session sql model
    __tablename__ = "training_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[date] = mapped_column(Date)
    session_type: Mapped[str] = mapped_column(String)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    rpe: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)