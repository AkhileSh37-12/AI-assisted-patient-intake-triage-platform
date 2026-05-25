from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from typing import Optional
from datetime import datetime


ALLOWED_ACTIVITY_STATUS = [
    "Success",
    "Failed",
    "Warning"
]


class ActivityLogBase(BaseModel):

    user_id: int = Field(..., gt=0)

    activity_type: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    entity_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    entity_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    activity_description: Optional[str] = Field(
        default=None,
        max_length=5000
    )

    ip_address: Optional[str] = Field(
        default=None,
        max_length=50
    )

    activity_status: Optional[str] = "Success"

    @field_validator("activity_status")
    @classmethod
    def validate_status(cls, value):

        if value not in ALLOWED_ACTIVITY_STATUS:

            raise ValueError(
                f"Activity status must be one of {ALLOWED_ACTIVITY_STATUS}"
            )

        return value


class ActivityLogCreate(
    ActivityLogBase
):
    pass


class ActivityLogUpdate(BaseModel):

    activity_description: Optional[str] = None

    ip_address: Optional[str] = None

    activity_status: Optional[str] = None


class ActivityLogResponse(
    ActivityLogBase
):

    activity_log_id: int

    created_at: datetime

    class Config:
        from_attributes = True