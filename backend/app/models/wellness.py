
from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WellnessLog(Base):
    __tablename__ = "wellness_logs"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    date: Mapped[date] = mapped_column(Date, nullable=False)

    sleep_hours: Mapped[float] = mapped_column(Float, nullable=False)

    sleep_quality: Mapped[int] = mapped_column(Integer, nullable=False)

    soreness: Mapped[int] = mapped_column(Integer, nullable=False)

    stress: Mapped[int] = mapped_column(Integer, nullable=False)

    pain: Mapped[int] = mapped_column(Integer, nullable=False)

    notes: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
