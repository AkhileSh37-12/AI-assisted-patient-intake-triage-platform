from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.doctor import Doctor


def get_doctors(
    db: Session
):

    return db.query(Doctor).all()


def create_doctor(
    db: Session,
    doctor
):

    new_doctor = Doctor(
        **doctor.model_dump()
    )

    db.add(new_doctor)

    db.commit()

    db.refresh(new_doctor)

    return {
        "message": "Doctor created successfully",
        "doctor_data": new_doctor
    }


def update_doctor(
    db: Session,
    doctor_id: int,
    updated_doctor
):

    doctor = db.query(Doctor).filter(
        Doctor.doctor_id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    for key, value in updated_doctor.model_dump().items():

        setattr(doctor, key, value)

    db.commit()

    db.refresh(doctor)

    return {
        "message": "Doctor updated successfully",
        "doctor_data": doctor
    }


def delete_doctor(
    db: Session,
    doctor_id: int
):

    doctor = db.query(Doctor).filter(
        Doctor.doctor_id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)

    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }
    
def get_doctor_by_id(
    db: Session,
    doctor_id: int
):

    doctor = (
        db.query(Doctor)
        .filter(
            Doctor.doctor_id == doctor_id
        )
        .first()
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor