
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class WellnessLogCreate(BaseModel):
    date: date
    sleep_hours: float = Field(ge=0, le=24)
    sleep_quality: int = Field(ge=1, le=10)
    soreness: int = Field(ge=1, le=10)
    stress: int = Field(ge=1, le=10)
    pain: int = Field(ge=0, le=10)
    notes: str | None = None


class WellnessLogResponse(WellnessLogCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
