from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class ActivityLog(Base):

    __tablename__ = "activity_logs"

    activity_log_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    activity_type = Column(
        String(100),
        nullable=False
    )

    entity_name = Column(
        String(100),
        nullable=False
    )

    entity_id = Column(
        Integer,
        nullable=True
    )

    activity_description = Column(
        Text,
        nullable=True
    )

    ip_address = Column(
        String(50),
        nullable=True
    )

    activity_status = Column(
        String(30),
        default="Success"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User"
    )    