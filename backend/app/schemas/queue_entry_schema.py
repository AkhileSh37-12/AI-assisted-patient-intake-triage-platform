from pydantic import BaseModel, field_validator
from datetime import date, datetime


class QueueEntryBase(BaseModel):

    intake_id: int
    queue_date: date
    queue_number: int
    priority_score: int
    assigned_doctor_id: int | None = None
    queue_position: int
    queue_status: str
    department_id: int

    @field_validator("priority_score")
    @classmethod
    def validate_priority(cls, value):

        allowed = [1, 2, 3, 4]

        if value not in allowed:
            raise ValueError(
                f"Priority score must be one of: {allowed}"
            )

        return value

    @field_validator("queue_status")
    @classmethod
    def validate_status(cls, value):

        allowed = [
            "Waiting",
            "Called",
            "In Consultation",
            "Completed",
            "Skipped",
            "Cancelled"
        ]

        if value not in allowed:
            raise ValueError(
                f"Queue status must be one of: {allowed}"
            )

        return value


class QueueEntryCreate(QueueEntryBase):
    pass


class QueueEntryUpdate(QueueEntryBase):
    pass


class QueueEntryResponse(QueueEntryBase):

    queue_id: int

    called_at: datetime | None = None
    consultation_started_at: datetime | None = None
    consultation_completed_at: datetime | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True