from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class RAGRetrievalLog(Base):

    __tablename__ = "rag_retrieval_logs"

    retrieval_log_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    intake_id = Column(
        Integer,
        ForeignKey("patient_intakes.intake_id"),
        nullable=False
    )

    knowledge_id = Column(
        Integer,
        ForeignKey(
            "rag_knowledge_base.knowledge_id"
        ),
        nullable=False
    )

    similarity_score = Column(
        Float,
        nullable=True
    )

    retrieval_rank = Column(
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

    knowledge = relationship(
        "RAGKnowledgeBase"
    )