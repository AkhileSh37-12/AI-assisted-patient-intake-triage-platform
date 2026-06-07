from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.patient import Patient


def create_patient_service(
    db: Session,
    patient
):

    new_patient = Patient(

    full_name=patient.get(
        "full_name"
    ),

    age=patient.get(
        "age"
    ),

    gender=patient.get(
        "gender"
    ),

    phone_number=patient.get(
        "phone_number"
    )
)

    db.add(new_patient)

    db.commit()

    db.refresh(new_patient)

    return new_patient


def get_patients_service(
    db: Session
):

    return db.query(Patient).all()


def update_patient_service(
    db: Session,
    patient_id: int,
    updated_patient
):

    patient = db.query(Patient).filter(
        Patient.patient_id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    for key, value in updated_patient.model_dump().items():

        setattr(patient, key, value)

    db.commit()

    db.refresh(patient)

    return {
        "message": "Patient updated successfully",
        "updated_patient": patient
    }


def delete_patient_service(
    db: Session,
    patient_id: int
):

    patient = db.query(Patient).filter(
        Patient.patient_id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)

    db.commit()

    return {
        "message": "Patient deleted successfully"
    }
    
def get_or_create_patient_service(
    db: Session,
    patient_data
):
    """
    Reuse an existing patient if the phone
    number already exists, otherwise create
    a new patient.
    """

    phone_number = patient_data.get(
        "phone_number"
    )

    if phone_number:

        existing_patient = (
            db.query(Patient)
            .filter(
                Patient.phone_number == phone_number
            )
            .first()
        )

        if existing_patient:
            return existing_patient

    return create_patient_service(
        db,
        patient_data
    )