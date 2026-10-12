from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator

class PTSessionCreate(BaseModel):
    date: date
    exercise: str = Field(min_length=1, max_length=150)
    sets: int = Field(ge=1, le=100)
    reps: int = Field(ge=1, le=1000)
    duration_minutes: int = Field(ge=1, le=1440)
    pain: int = Field(ge=0, le=10)
    notes: str | None = None

    @field_validator("exercise")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Exercise is required")
        return value.strip()

class PTSessionResponse(PTSessionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
