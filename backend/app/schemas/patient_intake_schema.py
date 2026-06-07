from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from typing import Optional
from datetime import datetime


ALLOWED_INPUT_TYPES = [
    "Text",
    "Voice"
]

ALLOWED_URGENCY_LEVELS = [
    "Emergency",
    "High",
    "Medium",
    "Low"
]

ALLOWED_STATUS = [
    "Pending",
    "AI Processed",
    "Verified",
    "Queued",
    "Completed",
    "Cancelled"
]


class PatientIntakeBase(BaseModel):

    patient_id: int = Field(..., gt=0)

    symptoms_text: str = Field(
        ...,
        min_length=3,
        max_length=5000
    )

    input_type: str

    created_by_user_id: int = Field(..., gt=0)

    verified_by_user_id: Optional[int] = None

    ai_extracted_summary: Optional[str] = None

    ai_urgency_level: Optional[str] = None

    ai_confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    staff_verified: Optional[bool] = False

    final_urgency_level: Optional[str] = None

    assigned_doctor_id: Optional[int] = None

    staff_notes: Optional[str] = None

    status: Optional[str] = "Pending"

    suggested_department_id: Optional[int] = None

    final_department_id: Optional[int] = None

    @field_validator("input_type")
    @classmethod
    def validate_input_type(cls, value):

        if value not in ALLOWED_INPUT_TYPES:
            raise ValueError(
                f"Input type must be one of {ALLOWED_INPUT_TYPES}"
            )

        return value

    @field_validator(
        "ai_urgency_level",
        "final_urgency_level"
    )
    @classmethod
    def validate_urgency(cls, value):

        if value is None:
            return value

        if value not in ALLOWED_URGENCY_LEVELS:
            raise ValueError(
                f"Urgency must be one of {ALLOWED_URGENCY_LEVELS}"
            )

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):

        if value not in ALLOWED_STATUS:
            raise ValueError(
                f"Status must be one of {ALLOWED_STATUS}"
            )

        return value

    @field_validator("symptoms_text")
    @classmethod
    def validate_symptoms(cls, value):

        cleaned = value.strip()

        if len(cleaned) < 3:
            raise ValueError(
                "Symptoms text too short"
            )

        return cleaned


class PatientIntakeCreate(
    PatientIntakeBase
):
    pass


class PatientIntakeUpdate(BaseModel):

    symptoms_text: Optional[str] = None

    input_type: Optional[str] = None

    verified_by_user_id: Optional[int] = None

    ai_extracted_summary: Optional[str] = None

    ai_urgency_level: Optional[str] = None

    ai_confidence_score: Optional[float] = None

    staff_verified: Optional[bool] = None

    final_urgency_level: Optional[str] = None

    assigned_doctor_id: Optional[int] = None

    staff_notes: Optional[str] = None

    status: Optional[str] = None

    suggested_department_id: Optional[int] = None

    final_department_id: Optional[int] = None


class PatientIntakeResponse(
    PatientIntakeBase
):

    intake_id: int

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True