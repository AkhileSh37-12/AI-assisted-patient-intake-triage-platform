from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.ai_processing_log import (
    AIProcessingLog
)


def get_ai_processing_logs(
    db: Session
):

    return db.query(
        AIProcessingLog
    ).all()


def create_ai_processing_log(
    db: Session,
    log
):

    new_log = AIProcessingLog(
        **log.model_dump()
    )

    db.add(new_log)

    db.commit()

    db.refresh(new_log)

    return {
        "message":
        "AI processing log created successfully",
        "log_data": new_log
    }


def update_ai_processing_log(
    db: Session,
    log_id: int,
    updated_log
):

    log = db.query(
        AIProcessingLog
    ).filter(
        AIProcessingLog.log_id == log_id
    ).first()

    if not log:

        raise HTTPException(
            status_code=404,
            detail="AI processing log not found"
        )

    for key, value in updated_log.model_dump().items():

        setattr(log, key, value)

    db.commit()

    db.refresh(log)

    return {
        "message":
        "AI processing log updated successfully",
        "log_data": log
    }


def delete_ai_processing_log(
    db: Session,
    log_id: int
):

    log = db.query(
        AIProcessingLog
    ).filter(
        AIProcessingLog.log_id == log_id
    ).first()

    if not log:

        raise HTTPException(
            status_code=404,
            detail="AI processing log not found"
        )

    db.delete(log)

    db.commit()

    return {
        "message":
        "AI processing log deleted successfully"
    }

from app.schemas.ai_processing_log_schema import (
    AIProcessingLogCreate
)


def log_ai_processing(
    db: Session,
    intake_id: int,
    ai_model_name: str,
    processing_stage: str,
    input_data: str,
    output_data: str,
    confidence_score: float | None = None
):

    log = AIProcessingLogCreate(

        intake_id=intake_id,

        ai_model_name=ai_model_name,

        processing_stage=processing_stage,

        input_data=input_data,

        output_data=output_data,

        confidence_score=confidence_score,

        processing_status="Success"
    )

    create_ai_processing_log(
        db,
        log
    )