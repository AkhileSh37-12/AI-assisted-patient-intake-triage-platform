from pydantic import BaseModel, field_validator
from typing import Optional
import re


class DepartmentBase(BaseModel):
    """
    Base schema for Department validation.
    """

    department_name: str
    description: str
    is_active: Optional[bool] = True

    @field_validator("department_name")
    @classmethod
    def validate_department_name(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Department name cannot be empty"
            )

        if not re.match(r"^[A-Za-z\s]+$", cleaned_value):
            raise ValueError(
                "Department name must contain only alphabets"
            )

        return cleaned_value


    @field_validator("description")
    @classmethod
    def validate_description(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Description cannot be empty"
            )

        return cleaned_value


class DepartmentCreate(DepartmentBase):
    """
    Schema for creating department.
    """
    pass


class DepartmentUpdate(DepartmentBase):
    """
    Schema for updating department.
    """
    pass