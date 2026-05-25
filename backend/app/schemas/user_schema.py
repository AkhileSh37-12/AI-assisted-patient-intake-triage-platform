from pydantic import (
    BaseModel,
    field_validator,
    EmailStr
)

from typing import Optional
import re


class UserBase(BaseModel):
    """
    Base schema for user validation.
    """

    full_name: str
    email: EmailStr
    password_hash: str
    role_id: int
    is_active: Optional[bool] = True

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Full name cannot be empty"
            )

        if not re.match(
            r"^[A-Za-z\s]+$",
            cleaned_value
        ):
            raise ValueError(
                "Full name must contain only alphabets"
            )

        return cleaned_value

    @field_validator("password_hash")
    @classmethod
    def validate_password(cls, value):

        cleaned_value = value.strip()

        if len(cleaned_value) < 6:
            raise ValueError(
                "Password must be at least 6 characters"
            )

        return cleaned_value

    @field_validator("role_id")
    @classmethod
    def validate_role_id(cls, value):

        if value <= 0:
            raise ValueError(
                "Role ID must be positive"
            )

        return value


class UserCreate(UserBase):
    """
    Schema for creating user.
    """
    pass


class UserUpdate(UserBase):
    """
    Schema for updating user.
    """
    pass