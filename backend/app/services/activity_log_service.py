from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.activity_log import ActivityLog

from app.schemas.activity_log_schema import (
    ActivityLogCreate
)

def get_activity_logs(
    db: Session
):

    return db.query(
        ActivityLog
    ).all()


def create_activity_log(
    db: Session,
    activity_log
):

    new_log = ActivityLog(
        **activity_log.model_dump()
    )

    db.add(new_log)

    db.commit()

    db.refresh(new_log)

    return {
        "message":
        "Activity log created successfully",
        "activity_log_data": new_log
    }


def update_activity_log(
    db: Session,
    activity_log_id: int,
    updated_log
):

    log = db.query(
        ActivityLog
    ).filter(
        ActivityLog.activity_log_id == activity_log_id
    ).first()

    if not log:

        raise HTTPException(
            status_code=404,
            detail="Activity log not found"
        )

    for key, value in updated_log.model_dump().items():

        setattr(log, key, value)

    db.commit()

    db.refresh(log)

    return {
        "message":
        "Activity log updated successfully",
        "activity_log_data": log
    }


def delete_activity_log(
    db: Session,
    activity_log_id: int
):

    log = db.query(
        ActivityLog
    ).filter(
        ActivityLog.activity_log_id == activity_log_id
    ).first()

    if not log:

        raise HTTPException(
            status_code=404,
            detail="Activity log not found"
        )

    db.delete(log)

    db.commit()

    return {
        "message":
        "Activity log deleted successfully"
    }
    
def log_activity(
    db: Session,
    user_id: int,
    activity_type: str,
    entity_name: str,
    entity_id: int,
    activity_description: str
):

    activity_log = ActivityLogCreate(

        user_id=user_id,

        activity_type=activity_type,

        entity_name=entity_name,

        entity_id=entity_id,

        activity_description=activity_description,

        activity_status="Success"
    )

    create_activity_log(
        db,
        activity_log
    )