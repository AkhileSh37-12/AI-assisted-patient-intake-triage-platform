from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.queue_entry import QueueEntry

from app.models.consultation import Consultation

from app.services.activity_log_service import (
    log_activity
)

def create_queue_entry_service(db: Session, queue_entry_data):

    new_queue_entry = QueueEntry(
        **queue_entry_data.model_dump()
    )

    db.add(new_queue_entry)

    db.commit()

    db.refresh(new_queue_entry)

    return new_queue_entry


def get_all_queue_entries_service(db: Session):

    return db.query(QueueEntry).all()


def get_queue_entry_by_id_service(
    db: Session,
    queue_id: int
):

    queue_entry = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id
    ).first()

    if not queue_entry:
        raise HTTPException(
            status_code=404,
            detail="Queue entry not found"
        )

    return queue_entry


def update_queue_entry_service(
    db: Session,
    queue_id: int,
    updated_data
):

    queue_entry = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id
    ).first()

    if not queue_entry:
        raise HTTPException(
            status_code=404,
            detail="Queue entry not found"
        )

    for key, value in updated_data.model_dump().items():
        setattr(queue_entry, key, value)

    db.commit()

    db.refresh(queue_entry)

    return queue_entry


def delete_queue_entry_service(
    db: Session,
    queue_id: int
):

    queue_entry = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id
    ).first()

    if not queue_entry:
        raise HTTPException(
            status_code=404,
            detail="Queue entry not found"
        )

    db.delete(queue_entry)

    db.commit()

    return True

from datetime import date
from datetime import datetime

def get_next_queue_number(
    db: Session
):

    today = date.today()

    latest_entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.queue_date == today
        )
        .order_by(
            QueueEntry.queue_number.desc()
        )
        .first()
    )

    if not latest_entry:
        return 1

    return latest_entry.queue_number + 1

def get_next_queue_position(
    db: Session,
    department_id: int
):

    waiting_count = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.department_id == department_id,
            QueueEntry.queue_status == "Waiting"
        )
        .count()
    )

    return waiting_count + 1

def call_patient(
    db: Session,
    queue_id: int
):

    queue_entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.queue_id == queue_id
        )
        .first()
    )

    if not queue_entry:

        raise HTTPException(
            status_code=404,
            detail="Queue entry not found"
        )

    queue_entry.queue_status = "Called"

    queue_entry.called_at = datetime.utcnow()

    db.commit()

    db.refresh(queue_entry)
    
    log_activity(

        db=db,

        user_id=1,

        activity_type="Patient Called",

        entity_name="Queue Entry",

        entity_id=queue_entry.queue_id,

        activity_description=
        "Patient called for consultation"
    )
    
    return queue_entry

def start_consultation(
    db: Session,
    queue_id: int
):

    queue_entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.queue_id == queue_id
        )
        .first()
    )

    if not queue_entry:

        raise HTTPException(
            status_code=404,
            detail="Queue entry not found"
        )

    existing_consultation = (
        db.query(Consultation)
        .filter(
            Consultation.intake_id ==
            queue_entry.intake_id
        )
        .first()
    )

    if not existing_consultation:

        consultation = Consultation(

            intake_id=
            queue_entry.intake_id,

            doctor_id=
            queue_entry.assigned_doctor_id,

            consultation_status=
            "In Progress"
        )

        db.add(
            consultation
        )

    queue_entry.queue_status = (
        "In Consultation"
    )

    queue_entry.consultation_started_at = (
        datetime.utcnow()
    )

    db.commit()

    db.refresh(queue_entry)

    log_activity(

        db=db,

        user_id=1,

        activity_type="Consultation Started",

        entity_name="Consultation",

        entity_id=queue_entry.intake_id,

        activity_description=
        f"Consultation started with doctor {queue_entry.assigned_doctor_id}"
    )

    return queue_entry

def complete_consultation(
    db: Session,
    queue_id: int
):

    queue_entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.queue_id == queue_id
        )
        .first()
    )

    if not queue_entry:

        raise HTTPException(
            status_code=404,
            detail="Queue entry not found"
        )

    consultation = (
        db.query(Consultation)
        .filter(
            Consultation.intake_id ==
            queue_entry.intake_id
        )
        .first()
    )

    if consultation:

        consultation.consultation_status = (
            "Completed"
        )

    queue_entry.queue_status = (
        "Completed"
    )

    queue_entry.consultation_completed_at = (
        datetime.utcnow()
    )

    db.commit()

    db.refresh(queue_entry)

    log_activity(

        db=db,

        user_id=1,

        activity_type="Consultation Completed",

        entity_name="Consultation",

        entity_id=queue_entry.intake_id,

        activity_description=
        "Consultation completed successfully"
    )

    return queue_entry