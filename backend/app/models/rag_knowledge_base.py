from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.db.database import Base

from pgvector.sqlalchemy import Vector

class RAGKnowledgeBase(Base):

    __tablename__ = "rag_knowledge_base"

    knowledge_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    source = Column(
        String(255),
        nullable=True
    )

    content = Column(
        Text,
        nullable=False
    )

    medical_specialty = Column(
        String(100),
        nullable=True
    )

    keywords = Column(
        Text,
        nullable=True
    )

    chunk_index = Column(
        Integer,
        nullable=True
    )
    
    embedding = Column(
        Vector(384),
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