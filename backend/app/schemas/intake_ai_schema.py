from pydantic import BaseModel


class IntakeAIRequest(BaseModel):

    patient_input: str