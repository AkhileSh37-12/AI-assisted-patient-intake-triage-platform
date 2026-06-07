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

    data = call_patient(
        db,
        queue_id
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

    data = start_consultation(
        db,
        queue_id
    )

    return {
        "message": "Consultation started successfully",
        "data": data
    }
    
@router.post(
    "/queue-entries/{queue_id}/complete"
)
def complete_consultation_endpoint(
    queue_id: int,
    db: Session = Depends(get_db)
):

    data = complete_consultation(
        db,
        queue_id
    )

    return {
        "message": "Consultation completed successfully",
        "data": data
    }
    
