from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.db.database import Base


class Role(Base):
    """
    Role database model.
    """

    __tablename__ = "roles"

    role_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    role_name = Column(
        String(30),
        nullable=False,
        unique=True
    )