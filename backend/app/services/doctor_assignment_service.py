from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.doctor import Doctor
from app.models.queue_entry import QueueEntry


def assign_doctor(
    db: Session,
    department_id: int
):

    available_doctors = (

        db.query(Doctor)

        .filter(
            Doctor.department_id == department_id,
            Doctor.availability_status == "Available"
        )

        .all()
    )

    if not available_doctors:

        raise HTTPException(
            status_code=404,
            detail="No available doctor found for department"
        )

    selected_doctor = None

    minimum_load = float("inf")

    for doctor in available_doctors:

        active_patients = (

            db.query(QueueEntry)

            .filter(
                QueueEntry.assigned_doctor_id == doctor.doctor_id,
                QueueEntry.queue_status.in_(
                    [
                        "Waiting",
                        "Called",
                        "In Consultation"
                    ]
                )
            )

            .count()
        )

        if active_patients < minimum_load:

            minimum_load = active_patients

            selected_doctor = doctor

    return selected_doctor