from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.schemas.queue_entry_schema import (
    QueueEntryCreate,
    QueueEntryUpdate
)

from app.services.queue_entry_service import (
    create_queue_entry_service,
    get_all_queue_entries_service,
    get_queue_entry_by_id_service,
    update_queue_entry_service,
    delete_queue_entry_service,
    call_patient,
    start_consultation,
    complete_consultation
)
from app.telemetry.tracing import (
    tracer,
    logger
)

router = APIRouter(
    tags=["Queue Entries"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/queue-entries")
def create_queue_entry(
    queue_entry: QueueEntryCreate,
    db: Session = Depends(get_db)
):

    data = create_queue_entry_service(
        db,
        queue_entry
    )

    return {
        "message": "Queue entry created successfully",
        "data": data
    }


@router.get("/queue-entries")
def get_queue_entries(
    db: Session = Depends(get_db)
):

    return get_all_queue_entries_service(db)


@router.get("/queue-entries/{queue_id}")
def get_queue_entry(
    queue_id: int,
    db: Session = Depends(get_db)
):

    return get_queue_entry_by_id_service(
        db,
        queue_id
    )


@router.put("/queue-entries/{queue_id}")
def update_queue_entry(
    queue_id: int,
    updated_data: QueueEntryUpdate,
    db: Session = Depends(get_db)
):

    data = update_queue_entry_service(
        db,
        queue_id,
        updated_data
    )

    return {
        "message": "Queue entry updated successfully",
        "data": data
    }


@router.delete("/queue-entries/{queue_id}")
def delete_queue_entry(
    queue_id: int,
    db: Session = Depends(get_db)
):

    delete_queue_entry_service(
        db,
        queue_id
    )

    return {
        "message": "Queue entry deleted successfully"
    }


@router.post(
    "/queue-entries/{queue_id}/call"
)
def call_patient_endpoint(
    queue_id: int,
    db: Session = Depends(get_db)
):
    with tracer.start_as_current_span(
        "patient_call"
    ) as span:

        span.set_attribute(
            "queue.id",
            queue_id
        )
        
        logger.info(
            f"Calling patient: queue_id={queue_id}"
        )

        try:

            with tracer.start_as_current_span(
                "queue_lookup"
            ):

                pass

            with tracer.start_as_current_span(
                "status_update"
            ):

                pass

            with tracer.start_as_current_span(
                "patient_notification"
            ) as child_span:

                data = call_patient(
                    db,
                    queue_id
                )

                child_span.set_attribute(
                    "queue.id",
                    data.queue_id
                )

                child_span.set_attribute(
                    "intake.id",
                    data.intake_id
                )

                child_span.set_attribute(
                    "queue.status",
                    data.queue_status
                )

        except Exception as e:

            logger.error(
                f"Patient call failed: queue_id={queue_id}, error={str(e)}"
            )

            raise

        span.add_event(
            "Patient called"
        )
        
        span.add_event(
            "Patient notified"
        )

        logger.info(
            f"Patient called successfully: queue_id={queue_id}"
        )

        return {
            "message": "Patient called successfully",
            "data": data
        }


@router.post(
    "/queue-entries/{queue_id}/start"
)
def start_consultation_endpoint(
    queue_id: int,
    db: Session = Depends(get_db)
):

    with tracer.start_as_current_span(
        "consultation_start"
    ) as span:

        span.set_attribute(
            "queue.id",
            queue_id
        )

        logger.info(
            f"Starting consultation: queue_id={queue_id}"
        )

        try:

            with tracer.start_as_current_span(
                "queue_lookup"
            ):

                pass

            with tracer.start_as_current_span(
                "status_update"
            ):

                pass

            with tracer.start_as_current_span(
                "consultation_state_change"
            ) as child_span:

                data = start_consultation(
                    db,
                    queue_id
                )

                child_span.set_attribute(
                    "queue.id",
                    data.queue_id
                )

                child_span.set_attribute(
                    "intake.id",
                    data.intake_id
                )

                child_span.set_attribute(
                    "queue.status",
                    data.queue_status
                )

        except Exception as e:

            logger.error(
                f"Consultation start failed: queue_id={queue_id}, error={str(e)}"
            )

            raise

        span.add_event(
            "Consultation started"
        )
        
        span.add_event(
            "Doctor began consultation"
        )
        
        logger.info(
            f"Consultation started: queue_id={queue_id}"
        )

        return {
            "message":
            "Consultation started successfully",
            "data": data
        }
    
@router.post(
    "/queue-entries/{queue_id}/complete"
)
def complete_consultation_endpoint(
    queue_id: int,
    db: Session = Depends(get_db)
):

    with tracer.start_as_current_span(
        "consultation_complete"
    ) as span:

        span.set_attribute(
            "queue.id",
            queue_id
        )
        
        logger.info(
            f"Completing consultation: queue_id={queue_id}"
        )

        try:

            with tracer.start_as_current_span(
                "queue_lookup"
            ):

                pass

            with tracer.start_as_current_span(
                "status_update"
            ):

                pass

            with tracer.start_as_current_span(
                "workflow_completion"
            ) as child_span:

                data = complete_consultation(
                    db,
                    queue_id
                )

                child_span.set_attribute(
                    "queue.id",
                    data.queue_id
                )

                child_span.set_attribute(
                    "intake.id",
                    data.intake_id
                )

                child_span.set_attribute(
                    "queue.status",
                    data.queue_status
                )

                child_span.add_event(
                    "Workflow completed"
                )

        except Exception as e:

            logger.error(
                f"Consultation completion failed: queue_id={queue_id}, error={str(e)}"
            )

            raise

        span.add_event(
            "Consultation completed"
        )
        
        span.add_event(
            "Queue closed"
        )
        
        logger.info(
            f"Consultation completed: queue_id={queue_id}"
        )

        return {
            "message":
            "Consultation completed successfully",
            "data": data
        }
