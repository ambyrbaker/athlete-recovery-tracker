from datetime import date
from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class PTSession(Base):
    __tablename__ = "pt_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date)
    exercise: Mapped[str] = mapped_column(String)
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    pain: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
