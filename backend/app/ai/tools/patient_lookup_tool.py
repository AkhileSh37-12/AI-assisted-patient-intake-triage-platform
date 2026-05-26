from sqlalchemy.orm import Session

from app.models.patient import Patient


class PatientLookupTool:

    @staticmethod
    def get_patient_by_id(
        patient_id: int,
        db: Session
    ):

        return (
            db.query(Patient)
            .filter(
                Patient.patient_id == patient_id
            )
            .first()
        )