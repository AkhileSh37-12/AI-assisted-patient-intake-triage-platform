from pydantic import (
    BaseModel,
    Field
)

from typing import Optional
from datetime import datetime


class RAGKnowledgeBaseBase(BaseModel):

    title: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    source: Optional[str] = Field(
        default=None,
        max_length=255
    )

    content: str = Field(
        ...,
        min_length=5
    )

    medical_specialty: Optional[str] = Field(
        default=None,
        max_length=100
    )

    keywords: Optional[str] = None

    chunk_index: Optional[int] = Field(
        default=None,
        ge=0
    )


class RAGKnowledgeBaseCreate(
    RAGKnowledgeBaseBase
):
    pass


class RAGKnowledgeBaseUpdate(BaseModel):

    title: Optional[str] = None

    category: Optional[str] = None

    source: Optional[str] = None

    content: Optional[str] = None

    medical_specialty: Optional[str] = None

    keywords: Optional[str] = None

    chunk_index: Optional[int] = None


class RAGKnowledgeBaseResponse(
    RAGKnowledgeBaseBase
):

    knowledge_id: int

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True