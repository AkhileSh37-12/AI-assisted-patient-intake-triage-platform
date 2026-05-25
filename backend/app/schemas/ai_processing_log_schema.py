from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from typing import Optional
from datetime import datetime


ALLOWED_PROCESSING_STATUS = [
    "Success",
    "Failed",
    "Partial"
]


class AIProcessingLogBase(BaseModel):

    intake_id: int = Field(..., gt=0)

    ai_model_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    processing_stage: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    input_data: Optional[str] = None

    output_data: Optional[str] = None

    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    processing_status: Optional[str] = "Success"

    error_message: Optional[str] = None

    processing_time_ms: Optional[int] = Field(
        default=None,
        ge=0
    )

    @field_validator("processing_status")
    @classmethod
    def validate_status(cls, value):

        if value not in ALLOWED_PROCESSING_STATUS:

            raise ValueError(
                f"Processing status must be one of {ALLOWED_PROCESSING_STATUS}"
            )

        return value


class AIProcessingLogCreate(
    AIProcessingLogBase
):
    pass


class AIProcessingLogUpdate(BaseModel):

    output_data: Optional[str] = None

    confidence_score: Optional[float] = None

    processing_status: Optional[str] = None

    error_message: Optional[str] = None

    processing_time_ms: Optional[int] = None


class AIProcessingLogResponse(
    AIProcessingLogBase
):

    log_id: int

    created_at: datetime

    class Config:
        from_attributes = True