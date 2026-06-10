from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.patient_intake import PatientIntake
from app.schemas.patient_intake_schema import (
    PatientIntakeCreate,
    PatientIntakeUpdate
)


def create_patient_intake(
    db: Session,
    intake: PatientIntakeCreate
):

    try:

        db_intake = PatientIntake(
            **intake.model_dump()
        )

        db.add(db_intake)

        db.commit()

        db.refresh(db_intake)

        return db_intake

    except SQLAlchemyError as e:

        db.rollback()

        raise Exception(
            f"Database error: {str(e)}"
        )


def get_all_patient_intakes(
    db: Session
):

    return (
        db.query(PatientIntake)
        .order_by(
            PatientIntake.intake_id.desc()
        )
        .all()
    )


def get_patient_intake_by_id(
    db: Session,
    intake_id: int
):

    return (
        db.query(PatientIntake)
        .filter(
            PatientIntake.intake_id == intake_id
        )
        .first()
    )


def update_patient_intake(
    db: Session,
    intake_id: int,
    intake_update: PatientIntakeUpdate
):

    try:

        db_intake = get_patient_intake_by_id(
            db,
            intake_id
        )

        if not db_intake:
            return None

        update_data = intake_update.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_intake, key, value)

        db.commit()

        db.refresh(db_intake)

        return db_intake

    except SQLAlchemyError as e:

        db.rollback()

        raise Exception(
            f"Database error: {str(e)}"
        )


def delete_patient_intake(
    db: Session,
    intake_id: int
):

    try:

        db_intake = get_patient_intake_by_id(
            db,
            intake_id
        )

        if not db_intake:
            return None

        db.delete(db_intake)

        db.commit()

        return db_intake

    except SQLAlchemyError as e:

        db.rollback()

        raise Exception(
            f"Database error: {str(e)}"
        )
        
def verify_patient_intake(
    db: Session,
    intake_id: int,
    verified_by_user_id: int,
    final_urgency_level: str,
    final_department_id: int,
    staff_notes: str | None = None
):

    intake = get_patient_intake_by_id(
        db,
        intake_id
    )

    if not intake:
        return None

    intake.staff_verified = True

    intake.verified_by_user_id = (
        verified_by_user_id
    )

    intake.final_urgency_level = (
        final_urgency_level
    )

    intake.final_department_id = (
        final_department_id
    )

    intake.staff_notes = (
        staff_notes
    )

    intake.status = "Verified"

    db.commit()

    db.refresh(intake)

    return intake