from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from typing import Optional
from datetime import datetime


ALLOWED_CONSULTATION_STATUS = [
    "In Progress",
    "Completed",
    "Cancelled"
]

ALLOWED_FOLLOW_UP = [
    "Yes",
    "No"
]


class ConsultationBase(BaseModel):

    intake_id: int = Field(..., gt=0)

    doctor_id: int = Field(..., gt=0)

    diagnosis: Optional[str] = Field(
        default=None,
        max_length=5000
    )

    prescription: Optional[str] = Field(
        default=None,
        max_length=5000
    )

    consultation_notes: Optional[str] = Field(
        default=None,
        max_length=5000
    )

    follow_up_required: Optional[str] = "No"

    consultation_status: Optional[str] = "In Progress"

    @field_validator("follow_up_required")
    @classmethod
    def validate_follow_up(cls, value):

        if value not in ALLOWED_FOLLOW_UP:

            raise ValueError(
                f"Follow up must be one of {ALLOWED_FOLLOW_UP}"
            )

        return value

    @field_validator("consultation_status")
    @classmethod
    def validate_status(cls, value):

        if value not in ALLOWED_CONSULTATION_STATUS:

            raise ValueError(
                f"Consultation status must be one of {ALLOWED_CONSULTATION_STATUS}"
            )

        return value


class ConsultationCreate(
    ConsultationBase
):
    pass


class ConsultationUpdate(BaseModel):

    diagnosis: Optional[str] = None

    prescription: Optional[str] = None

    consultation_notes: Optional[str] = None

    follow_up_required: Optional[str] = None

    consultation_status: Optional[str] = None


class ConsultationResponse(
    ConsultationBase
):

    consultation_id: int

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True