from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.patient_intake_schema import (
    PatientIntakeCreate,
    PatientIntakeUpdate
)

from app.services.patient_intake_service import (
    create_patient_intake,
    get_all_patient_intakes,
    get_patient_intake_by_id,
    update_patient_intake,
    delete_patient_intake
)

router = APIRouter(
    prefix="/patient-intakes",
    tags=["Patient Intakes"]
)


@router.get("/")
def get_all_intakes(
    db: Session = Depends(get_db)
):

    """
    Get all patient intakes API.
    """

    return get_all_patient_intakes(db)


@router.post("/")
def create_new_intake(
    intake: PatientIntakeCreate,
    db: Session = Depends(get_db)
):

    """
    Create patient intake API.
    """

    return create_patient_intake(
        db,
        intake
    )


@router.get("/{intake_id}")
def get_single_intake(
    intake_id: int,
    db: Session = Depends(get_db)
):

    """
    Get patient intake by ID API.
    """

    intake = get_patient_intake_by_id(
        db,
        intake_id
    )

    if not intake:

        raise HTTPException(
            status_code=404,
            detail="Patient intake not found"
        )

    return intake


@router.put("/{intake_id}")
def update_existing_intake(
    intake_id: int,
    intake: PatientIntakeUpdate,
    db: Session = Depends(get_db)
):

    """
    Update patient intake API.
    """

    updated_intake = update_patient_intake(
        db,
        intake_id,
        intake
    )

    if not updated_intake:

        raise HTTPException(
            status_code=404,
            detail="Patient intake not found"
        )

    return updated_intake


@router.delete("/{intake_id}")
def delete_existing_intake(
    intake_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete patient intake API.
    """

    deleted_intake = delete_patient_intake(
        db,
        intake_id
    )

    if not deleted_intake:

        raise HTTPException(
            status_code=404,
            detail="Patient intake not found"
        )

    return {
        "message":
        "Patient intake deleted successfully"
    }