from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.queue_entry import QueueEntry


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