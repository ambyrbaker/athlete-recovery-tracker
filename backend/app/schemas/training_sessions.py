from datetime import date

from pydantic import BaseModel, Field, field_validator


class TrainingSessionCreate(BaseModel):
    date: date
    session_type: str = Field(min_length=1, max_length=100)
    duration_minutes: int = Field(gt=0, le=1440)
    rpe: int = Field(ge=1, le=10)
    notes: str | None = None

    @field_validator("session_type")
    @classmethod
    def nonblank_type(cls, value):
        if not value.strip():
            raise ValueError("Session type is required")
        return value.strip()

    #this is the data that someone sends whenever they enter the training session data

class TrainingSessionResponse(BaseModel):
    id: int
    date: date
    session_type: str
    duration_minutes: int
    rpe: int
    notes: str | None = None

    model_config = {
        "from_attributes": True
    }