from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.ai_processing_log_schema import (
    AIProcessingLogCreate,
    AIProcessingLogUpdate
)

from app.services.ai_processing_log_service import (
    get_ai_processing_logs,
    create_ai_processing_log,
    update_ai_processing_log,
    delete_ai_processing_log
)

router = APIRouter(
    prefix="/ai-processing-logs",
    tags=["AI Processing Logs"]
)


@router.get("/")
def get_all_ai_processing_logs(
    db: Session = Depends(get_db)
):

    """
    Get all AI processing logs API.
    """

    return get_ai_processing_logs(db)


@router.post("/")
def create_new_ai_processing_log(
    log: AIProcessingLogCreate,
    db: Session = Depends(get_db)
):

    """
    Create AI processing log API.
    """

    return create_ai_processing_log(
        db,
        log
    )


@router.put("/{log_id}")
def update_existing_ai_processing_log(
    log_id: int,
    log: AIProcessingLogUpdate,
    db: Session = Depends(get_db)
):

    """
    Update AI processing log API.
    """

    return update_ai_processing_log(
        db,
        log_id,
        log
    )


@router.delete("/{log_id}")
def delete_existing_ai_processing_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete AI processing log API.
    """

    return delete_ai_processing_log(
        db,
        log_id
    )