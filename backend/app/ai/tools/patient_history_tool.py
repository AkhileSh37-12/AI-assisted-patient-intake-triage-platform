from sqlalchemy.orm import Session

from app.models.patient_intake import (
    PatientIntake
)


def get_patient_history(
    patient_id: int,
    db: Session
):

    previous_intakes = (

        db.query(
            PatientIntake
        )

        .filter(
            PatientIntake.patient_id == patient_id
        )

        .order_by(
            PatientIntake.created_at.desc()
        )
    )

    return [

        {
            "intake_id": intake.intake_id,
            "symptoms": intake.symptoms_text,
            "urgency": intake.ai_urgency_level,
            "status": intake.status
        }

        for intake in previous_intakes
    ]