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
    delete_patient_intake,
    verify_patient_intake
)

from app.schemas.patient_intake_schema import IntakeVerificationRequest

from app.services.department_service import (
    get_department_by_name
)
from app.services.doctor_assignment_service import (
    assign_doctor
)
from app.services.queue_entry_service import (
    create_queue_entry_service,
    get_next_queue_number,
    get_next_queue_position
)
from app.schemas.queue_entry_schema import (
    QueueEntryCreate
)
from datetime import date

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
    
@router.post("/{intake_id}/verify")
def verify_intake(
    intake_id: int,
    request: IntakeVerificationRequest,
    db: Session = Depends(get_db)
):

    department = get_department_by_name(
        db,
        request.department_name
    )

    verified_intake = verify_patient_intake(
        db=db,
        intake_id=intake_id,
        verified_by_user_id=
        request.verified_by_user_id,
        final_urgency_level=
        request.final_urgency_level,
        final_department_id=
        department.department_id,
        staff_notes=
        request.staff_notes
    )
    
    if not verified_intake:
    
            raise HTTPException(
                status_code=404,
                detail="Patient intake not found"
            )

    priority_map = {
        "Emergency": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    priority_score = priority_map.get(
        verified_intake.final_urgency_level,
        4
    )

    assigned_doctor = assign_doctor(
        db,
        department.department_id
    )

    queue_number = get_next_queue_number(
        db
    )

    queue_position = get_next_queue_position(
        db,
        assigned_doctor.doctor_id
    )

    queue_entry = QueueEntryCreate(

        intake_id=
        verified_intake.intake_id,

        queue_date=
        date.today(),

        queue_number=
        queue_number,

        priority_score=
        priority_score,

        assigned_doctor_id=
        assigned_doctor.doctor_id,

        queue_position=
        queue_position,

        queue_status="Waiting",

        department_id=
        department.department_id
    )

    saved_queue = create_queue_entry_service(
        db,
        queue_entry
    )

    verified_intake.assigned_doctor_id = (
        assigned_doctor.doctor_id
    )

    verified_intake.status = (
        "Queued"
    )

    db.commit()

    db.refresh(
        verified_intake
    )

    return {

        "message":
        "Patient verified and queued",

        "intake_id":
        verified_intake.intake_id,

        "doctor_id":
        assigned_doctor.doctor_id,

        "queue_id":
        saved_queue.queue_id,

        "queue_number":
        saved_queue.queue_number,

        "queue_position":
        saved_queue.queue_position,

        "department":
        department.department_name,

        "status":
        verified_intake.status
    }