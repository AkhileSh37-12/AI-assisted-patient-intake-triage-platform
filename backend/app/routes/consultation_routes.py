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

    """
    Create consultation API.
    """

    return create_consultation(
        db,
        consultation
    )


@router.put("/{consultation_id}")
def update_existing_consultation(
    consultation_id: int,
    consultation: ConsultationUpdate,
    db: Session = Depends(get_db)
):

    """
    Update consultation API.
    """

    return update_consultation(
        db,
        consultation_id,
        consultation
    )


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