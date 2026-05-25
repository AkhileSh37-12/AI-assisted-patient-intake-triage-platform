from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime

from app.db.database import Base


class Doctor(Base):
    """
    Doctor database model.
    """

    __tablename__ = "doctors"

    doctor_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    department_id = Column(
        Integer,
        nullable=False
    )

    specialization = Column(
        String(100),
        nullable=False
    )

    qualification = Column(
        String(100),
        nullable=False
    )

    availability_status = Column(
        String(30),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )