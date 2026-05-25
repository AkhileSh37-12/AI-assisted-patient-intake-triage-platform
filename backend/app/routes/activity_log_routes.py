from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.activity_log_schema import (
    ActivityLogCreate,
    ActivityLogUpdate
)

from app.services.activity_log_service import (
    get_activity_logs,
    create_activity_log,
    update_activity_log,
    delete_activity_log
)

router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"]
)


@router.get("/")
def get_all_activity_logs(
    db: Session = Depends(get_db)
):

    """
    Get all activity logs API.
    """

    return get_activity_logs(db)


@router.post("/")
def create_new_activity_log(
    activity_log: ActivityLogCreate,
    db: Session = Depends(get_db)
):

    """
    Create activity log API.
    """

    return create_activity_log(
        db,
        activity_log
    )


@router.put("/{activity_log_id}")
def update_existing_activity_log(
    activity_log_id: int,
    activity_log: ActivityLogUpdate,
    db: Session = Depends(get_db)
):

    """
    Update activity log API.
    """

    return update_activity_log(
        db,
        activity_log_id,
        activity_log
    )


@router.delete("/{activity_log_id}")
def delete_existing_activity_log(
    activity_log_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete activity log API.
    """

    return delete_activity_log(
        db,
        activity_log_id
    )