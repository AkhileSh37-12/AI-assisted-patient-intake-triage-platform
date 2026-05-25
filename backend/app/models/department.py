from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.database import Base


class Department(Base):
    """
    Department database model.
    """

    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    department_name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
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