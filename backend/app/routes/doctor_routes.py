from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.doctor_schema import (
    DoctorCreate,
    DoctorUpdate
)

from app.services.doctor_service import (
    get_doctors,
    create_doctor,
    update_doctor,
    delete_doctor
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.get("/")
def get_all_doctors(
    db: Session = Depends(get_db)
):

    """
    Get all doctors API.
    """

    return get_doctors(db)


@router.post("/")
def create_new_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):

    """
    Create doctor API.
    """

    return create_doctor(
        db,
        doctor
    )


@router.put("/{doctor_id}")
def update_existing_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db)
):

    """
    Update doctor API.
    """

    return update_doctor(
        db,
        doctor_id,
        doctor
    )


@router.delete("/{doctor_id}")
def delete_existing_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete doctor API.
    """

    return delete_doctor(
        db,
        doctor_id
    )