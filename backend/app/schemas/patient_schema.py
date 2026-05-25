from pydantic import BaseModel, Field, field_validator


class PatientBase(BaseModel):
    """
    Base schema containing common patient fields.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the patient"
    )

    age: int = Field(
        ...,
        gt=0,
        lt=120,
        description="Age of the patient"
    )

    gender: str = Field(
        ...,
        description="Gender of the patient"
    )

    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Patient phone number"
    )

    address: str = Field(
        ...,
        min_length=3,
        description="Patient address"
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Full name cannot be empty or spaces only"
        )

        if not cleaned_value.replace(" ", "").isalpha():
            raise ValueError(
                "Full name must contain only alphabets"
        )

        return cleaned_value

    @field_validator("address")
    @classmethod
    def validate_address(cls, value):

        if not value.strip():
            raise ValueError(
                "Address cannot be empty or spaces only"
            )

        return value

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):

        allowed_genders = ["Male", "Female", "Other"]

        if value not in allowed_genders:
            raise ValueError(
                "Gender must be Male, Female, or Other"
            )

        return value
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value.isdigit():
            raise ValueError(
                "Phone number must contain only digits"
            )

        if len(cleaned_value) != 10:
            raise ValueError(
                "Phone number must contain exactly 10 digits"
            )

        return cleaned_value

class PatientCreate(PatientBase):
    """
    Schema used for creating a patient.
    """
    pass


class PatientUpdate(PatientBase):
    """
    Schema used for updating patient details.
    """
    pass


class PatientResponse(PatientBase):

    patient_id: int

    class Config:
        from_attributes = True