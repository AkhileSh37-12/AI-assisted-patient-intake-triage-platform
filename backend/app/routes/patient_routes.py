from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.patient_schema import (
    PatientCreate,
    PatientUpdate
)

from app.services.patient_service import (
    create_patient_service,
    get_patients_service,
    update_patient_service,
    delete_patient_service
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    """
    Create a new patient.
    """

    return create_patient_service(
        db,
        patient
    )


@router.get("/")
def get_patients(
    db: Session = Depends(get_db)
):

    """
    Retrieve all patients.
    """

    return get_patients_service(db)


@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    updated_patient: PatientUpdate,
    db: Session = Depends(get_db)
):

    """
    Update patient details.
    """

    return update_patient_service(
        db,
        patient_id,
        updated_patient
    )


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete patient details.
    """

    return delete_patient_service(
        db,
        patient_id
    )