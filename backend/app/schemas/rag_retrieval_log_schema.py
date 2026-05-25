from pydantic import (
    BaseModel,
    Field
)

from typing import Optional
from datetime import datetime


class RAGRetrievalLogBase(BaseModel):

    intake_id: int = Field(..., gt=0)

    knowledge_id: int = Field(..., gt=0)

    similarity_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    retrieval_rank: Optional[int] = Field(
        default=None,
        ge=1
    )


class RAGRetrievalLogCreate(
    RAGRetrievalLogBase
):
    pass


class RAGRetrievalLogUpdate(BaseModel):

    similarity_score: Optional[float] = None

    retrieval_rank: Optional[int] = None


class RAGRetrievalLogResponse(
    RAGRetrievalLogBase
):

    retrieval_log_id: int

    created_at: datetime

    class Config:
        from_attributes = True