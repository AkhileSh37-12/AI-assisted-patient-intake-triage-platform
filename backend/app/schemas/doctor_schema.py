from pydantic import (
    BaseModel,
    field_validator
)

from typing import Optional
import re


class DoctorBase(BaseModel):
    """
    Base schema for doctor validation.
    """

    user_id: int
    department_id: int
    specialization: str
    qualification: str
    availability_status: str

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value):

        if value <= 0:
            raise ValueError(
                "User ID must be positive"
            )

        return value

    @field_validator("department_id")
    @classmethod
    def validate_department_id(cls, value):

        if value <= 0:
            raise ValueError(
                "Department ID must be positive"
            )

        return value

    @field_validator("specialization")
    @classmethod
    def validate_specialization(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Specialization cannot be empty"
            )

        if not re.match(
            r"^[A-Za-z\s]+$",
            cleaned_value
        ):
            raise ValueError(
                "Specialization must contain only alphabets"
            )

        return cleaned_value

    @field_validator("qualification")
    @classmethod
    def validate_qualification(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Qualification cannot be empty"
            )

        return cleaned_value

    @field_validator("availability_status")
    @classmethod
    def validate_availability_status(
        cls,
        value
    ):

        allowed_status = [
            "Available",
            "Busy",
            "Offline"
        ]

        if value not in allowed_status:
            raise ValueError(
                "Invalid availability status"
            )

        return value


class DoctorCreate(DoctorBase):
    """
    Schema for creating doctor.
    """
    pass


class DoctorUpdate(DoctorBase):
    """
    Schema for updating doctor.
    """
    pass