from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class PatientIntake(Base):

    __tablename__ = "patient_intakes"

    intake_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    symptoms_text = Column(
        Text,
        nullable=False
    )

    input_type = Column(
        String(20),
        nullable=False
    )

    created_by_user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    verified_by_user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=True
    )

    ai_extracted_summary = Column(
        Text,
        nullable=True
    )

    ai_urgency_level = Column(
        String(20),
        nullable=True
    )

    ai_confidence_score = Column(
        Float,
        nullable=True
    )

    staff_verified = Column(
        Boolean,
        default=False
    )

    final_urgency_level = Column(
        String(20),
        nullable=True
    )

    assigned_doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=True
    )

    staff_notes = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        default="Pending"
    )

    suggested_department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=True
    )

    final_department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=True
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

    patient = relationship("Patient")

    created_by_user = relationship(
        "User",
        foreign_keys=[created_by_user_id]
    )

    verified_by_user = relationship(
        "User",
        foreign_keys=[verified_by_user_id]
    )

    assigned_doctor = relationship("Doctor")

    suggested_department = relationship(
        "Department",
        foreign_keys=[suggested_department_id]
    )

    final_department = relationship(
        "Department",
        foreign_keys=[final_department_id]
    )

    queue_entry = relationship(
        "QueueEntry",
        back_populates="intake",
        uselist=False
    )