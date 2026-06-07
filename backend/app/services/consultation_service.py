from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.consultation import Consultation


def get_consultations(
    db: Session
):

    return db.query(Consultation).all()


def create_consultation(
    db: Session,
    consultation
):

    existing_consultation = (
        db.query(Consultation)
        .filter(
            Consultation.intake_id ==
            consultation.intake_id
        )
        .first()
    )

    if existing_consultation:

        raise HTTPException(
            status_code=400,
            detail="Consultation already exists for this intake"
        )

    new_consultation = Consultation(
        **consultation.model_dump()
    )

    db.add(new_consultation)

    db.commit()

    db.refresh(new_consultation)

    return {
        "message": "Consultation created successfully",
        "consultation_data": new_consultation
    }


def update_consultation(
    db: Session,
    consultation_id: int,
    updated_consultation
):

    consultation = db.query(
        Consultation
    ).filter(
        Consultation.consultation_id == consultation_id
    ).first()

    if not consultation:

        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    for key, value in updated_consultation.model_dump().items():

        setattr(consultation, key, value)

    db.commit()

    db.refresh(consultation)

    return {
        "message": "Consultation updated successfully",
        "consultation_data": consultation
    }


def delete_consultation(
    db: Session,
    consultation_id: int
):

    consultation = db.query(
        Consultation
    ).filter(
        Consultation.consultation_id == consultation_id
    ).first()

    if not consultation:

        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    db.delete(consultation)

    db.commit()

    return {
        "message": "Consultation deleted successfully"
    }