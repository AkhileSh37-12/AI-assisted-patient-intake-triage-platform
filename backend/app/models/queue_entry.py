from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.database import Base


class QueueEntry(Base):
    """
    QueueEntry model stores patient queue workflow details.
    """

    __tablename__ = "queue_entries"

    queue_id = Column(Integer, primary_key=True, index=True)

    
    intake_id = Column(
        Integer,
        ForeignKey("patient_intakes.intake_id"),
        unique=True,
        nullable=False
    )
    
    intake = relationship(
        "PatientIntake",
        back_populates="queue_entry"
    )

    queue_date = Column(Date, nullable=False)

    queue_number = Column(Integer, nullable=False)

    priority_score = Column(Integer, nullable=False)

    assigned_doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=True
    )

    queue_position = Column(Integer, nullable=False)

    queue_status = Column(String(30), nullable=False)

    called_at = Column(DateTime, nullable=True)

    consultation_started_at = Column(DateTime, nullable=True)

    consultation_completed_at = Column(DateTime, nullable=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )