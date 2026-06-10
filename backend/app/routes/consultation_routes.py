from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.consultation_schema import (
    ConsultationCreate,
    ConsultationUpdate
)

from app.services.consultation_service import (
    get_consultations,
    create_consultation,
    update_consultation,
    delete_consultation
)
from app.telemetry.tracing import (
    tracer,
    logger
)

router = APIRouter(
    prefix="/consultations",
    tags=["Consultations"]
)


@router.get("/")
def get_all_consultations(
    db: Session = Depends(get_db)
):

    """
    Get all consultations API.
    """

    return get_consultations(db)


@router.post("/")
def create_new_consultation(
    consultation: ConsultationCreate,
    db: Session = Depends(get_db)
):

    with tracer.start_as_current_span(
        "consultation_creation"
    ) as span:

        span.add_event(
            "Consultation creation started"
        )
        
        logger.info(
            f"Consultation creation started for intake={consultation.intake_id}"
        )
        
        span.set_attribute(
            "intake.id",
            consultation.intake_id
        )

        span.set_attribute(
            "doctor.id",
            consultation.doctor_id
        )

        span.set_attribute(
            "consultation.status",
            consultation.consultation_status
        )

        span.set_attribute(
            "follow_up.required",
            consultation.follow_up_required
        )
                
        with tracer.start_as_current_span(
            "intake_validation"
        ) as child_span:

            child_span.set_attribute(
                "intake.id",
                consultation.intake_id
            )

        with tracer.start_as_current_span(
            "consultation_save"
        ) as child_span:

            data = create_consultation(
                db,
                consultation
            )

            child_span.set_attribute(
                "consultation.id",
                data.consultation_id
            )

        with tracer.start_as_current_span(
            "audit_logging"
        ) as child_span:

            child_span.set_attribute(
                "consultation.id",
                data.consultation_id
            )

        span.set_attribute(
            "consultation.id",
            data.consultation_id
        )

        span.set_attribute(
            "patient.id",
            data.patient_id
        )

        span.set_attribute(
            "doctor.id",
            data.doctor_id
        )

        span.add_event(
            "Consultation created"
        )
        
        logger.info(
            f"Consultation created: consultation_id={data.consultation_id}, doctor_id={data.doctor_id}"
        )

        return data


@router.put("/{consultation_id}")
def update_existing_consultation(
    consultation_id: int,
    consultation: ConsultationUpdate,
    db: Session = Depends(get_db)
):

    with tracer.start_as_current_span(
        "consultation_update"
    ) as span:

        span.set_attribute(
            "consultation.id",
            consultation_id
        )

        logger.info(
            f"Updating consultation: consultation_id={consultation_id}"
        )

        try:

            with tracer.start_as_current_span(
                "consultation_lookup"
            ):

                pass

            with tracer.start_as_current_span(
                "consultation_modify"
            ) as child_span:

                data = update_consultation(
                    db,
                    consultation_id,
                    consultation
                )

                consultation_record = data["consultation_data"]

                child_span.set_attribute(
                    "consultation.id",
                    consultation_record.consultation_id
                )

                child_span.set_attribute(
                    "intake.id",
                    consultation_record.intake_id
                )

                child_span.set_attribute(
                    "doctor.id",
                    consultation_record.doctor_id
                )

                child_span.set_attribute(
                    "diagnosis",
                    consultation_record.diagnosis
                )
                
                child_span.set_attribute(
                    "consultation.notes",
                    consultation_record.consultation_notes
                )

                child_span.set_attribute(
                    "prescription",
                    consultation_record.prescription
                )

                child_span.set_attribute(
                    "consultation.status",
                    consultation_record.consultation_status
                )

                child_span.set_attribute(
                    "follow.up.required",
                    consultation_record.follow_up_required
                )

                child_span.add_event(
                    "Consultation updated"
                )
                

            with tracer.start_as_current_span(
                "consultation_save"
            ):

                pass

        except Exception as e:

            logger.error(
                f"Consultation update failed: {str(e)}"
            )

            raise

        span.add_event(
            "Consultation updated"
        )

        logger.info(
            f"Consultation updated successfully: consultation_id={consultation_id}"
        )

        return data


@router.delete("/{consultation_id}")
def delete_existing_consultation(
    consultation_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete consultation API.
    """

    return delete_consultation(
        db,
        consultation_id
    )