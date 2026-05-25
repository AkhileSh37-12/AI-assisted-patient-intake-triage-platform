from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Consultation(Base):

    __tablename__ = "consultations"

    consultation_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    intake_id = Column(
        Integer,
        ForeignKey("patient_intakes.intake_id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    diagnosis = Column(
        Text,
        nullable=True
    )

    prescription = Column(
        Text,
        nullable=True
    )

    consultation_notes = Column(
        Text,
        nullable=True
    )

    follow_up_required = Column(
        String(10),
        default="No"
    )

    consultation_status = Column(
        String(30),
        default="In Progress"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    intake = relationship(
        "PatientIntake"
    )

    doctor = relationship(
        "Doctor"
    )