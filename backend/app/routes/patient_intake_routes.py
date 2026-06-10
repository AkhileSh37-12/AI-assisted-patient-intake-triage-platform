import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.telemetry.tracing import logger

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

from app.services.doctor_service import (
    get_doctor_by_id
)

from app.telemetry.tracing import tracer

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

    with tracer.start_as_current_span(
        "staff_verification"
    ) as span:

        span.set_attribute(
            "intake.id",
            intake_id
        )

        span.set_attribute(
            "workflow.id",
            f"intake_{intake_id}"
        )

        span.set_attribute(
            "verified.by",
            request.verified_by_user_id
        )

        span.add_event(
            "Verification workflow started"
        )

        logger.info(
            f"Verification started for intake={intake_id}"
        )

        department = get_department_by_name(
            db,
            request.department_name
        )

        # ----------------------------------
        # Intake Verification
        # ----------------------------------

        with tracer.start_as_current_span(
            "intake_verification"
        ) as child_span:

            child_span.set_attribute(
                "workflow.id",
                f"intake_{intake_id}"
            )

            child_span.set_attribute(
                "department.name",
                request.department_name
            )

            child_span.set_attribute(
                "urgency.level",
                request.final_urgency_level
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

            child_span.set_attribute(
                "patient.id",
                verified_intake.patient_id
            )

            child_span.add_event(
                "Patient intake verified"
            )
            
            logger.info(
                f"Intake verified: intake_id={verified_intake.intake_id}"
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

        # ----------------------------------
        # Doctor Assignment
        # ----------------------------------

        with tracer.start_as_current_span(
            "doctor_assignment"
        ) as child_span:

            child_span.set_attribute(
                "workflow.id",
                f"intake_{intake_id}"
            )

            if request.assigned_doctor_id:

                assigned_doctor = get_doctor_by_id(
                    db,
                    request.assigned_doctor_id
                )

            else:

                assigned_doctor = assign_doctor(
                    db,
                    department.department_id
                )

            if (
                assigned_doctor.department_id
                != department.department_id
            ):

                raise HTTPException(
                    status_code=400,
                    detail=
                    "Doctor does not belong to selected department"
                )
                
                logger.error(
                    f"Doctor department mismatch for intake={intake_id}"
                )

            child_span.set_attribute(
                "doctor.id",
                assigned_doctor.doctor_id
            )

            child_span.set_attribute(
                "department.id",
                department.department_id
            )

            child_span.add_event(
                "Doctor assigned"
            )
            
            logger.info(
                f"Doctor assigned: doctor_id={assigned_doctor.doctor_id}, department={department.department_name}"
            )

        # ----------------------------------
        # Queue Creation
        # ----------------------------------

        with tracer.start_as_current_span(
            "queue_creation"
        ) as child_span:

            child_span.set_attribute(
                "workflow.id",
                f"intake_{intake_id}"
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

            child_span.set_attribute(
                "queue.id",
                saved_queue.queue_id
            )

            child_span.set_attribute(
                "queue.number",
                saved_queue.queue_number
            )

            child_span.set_attribute(
                "queue.position",
                saved_queue.queue_position
            )

            child_span.add_event(
                "Queue created"
            )
            
            logger.info(
                f"Queue created: queue_id={saved_queue.queue_id}"
            )

        # ----------------------------------
        # Intake Update
        # ----------------------------------

        with tracer.start_as_current_span(
            "intake_update"
        ) as child_span:

            child_span.set_attribute(
                "workflow.id",
                f"intake_{intake_id}"
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

            child_span.add_event(
                "Intake updated"
            )
            
            logger.info(
                f"Verification completed for intake={intake_id}"
            )

        span.add_event(
            "Verification workflow completed"
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