from pydantic import (
    BaseModel,
    field_validator
)

import re


class RoleBase(BaseModel):
    """
    Base schema for role validation.
    """

    role_name: str

    @field_validator("role_name")
    @classmethod
    def validate_role_name(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Role name cannot be empty"
            )

        if not re.match(
            r"^[A-Za-z\s]+$",
            cleaned_value
        ):
            raise ValueError(
                "Role name must contain only alphabets"
            )

        return cleaned_value


class RoleCreate(RoleBase):
    """
    Schema for creating role.
    """
    pass


class RoleUpdate(RoleBase):
    """
    Schema for updating role.
    """
    pass