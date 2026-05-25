from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class AIProcessingLog(Base):

    __tablename__ = "ai_processing_logs"

    log_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    intake_id = Column(
        Integer,
        ForeignKey("patient_intakes.intake_id"),
        nullable=False
    )

    ai_model_name = Column(
        String(100),
        nullable=False
    )

    processing_stage = Column(
        String(100),
        nullable=False
    )

    input_data = Column(
        Text,
        nullable=True
    )

    output_data = Column(
        Text,
        nullable=True
    )

    confidence_score = Column(
        Float,
        nullable=True
    )

    processing_status = Column(
        String(30),
        default="Success"
    )

    error_message = Column(
        Text,
        nullable=True
    )

    processing_time_ms = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    intake = relationship(
        "PatientIntake"
    )