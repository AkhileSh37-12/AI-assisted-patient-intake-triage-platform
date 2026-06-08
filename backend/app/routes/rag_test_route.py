from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.rag_test_schema import (
    RAGQueryRequest
)

from app.ai.rag.retrieval_service import (
    retrieve_relevant_chunks
)

router = APIRouter(
    prefix="/rag-test",
    tags=["RAG Test"]
)


@router.post("/")
def test_rag(
    request: RAGQueryRequest,
    db: Session = Depends(get_db)
):

    results = retrieve_relevant_chunks(
        db=db,
        query=request.query,
        top_k=request.top_k
    )

    return [

        {
            "knowledge_id":
            result.knowledge_id,

            "title":
            result.title,

            "specialty":
            result.medical_specialty,

            "category":
            result.category
        }

        for result in results
    ]