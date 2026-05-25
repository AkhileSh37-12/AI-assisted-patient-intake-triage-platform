from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.rag_retrieval_log_schema import (
    RAGRetrievalLogCreate,
    RAGRetrievalLogUpdate
)

from app.services.rag_retrieval_log_service import (
    get_rag_retrieval_logs,
    create_rag_retrieval_log,
    update_rag_retrieval_log,
    delete_rag_retrieval_log
)

router = APIRouter(
    prefix="/rag-retrieval-logs",
    tags=["RAG Retrieval Logs"]
)


@router.get("/")
def get_all_rag_retrieval_logs(
    db: Session = Depends(get_db)
):

    """
    Get all RAG retrieval logs API.
    """

    return get_rag_retrieval_logs(db)


@router.post("/")
def create_new_rag_retrieval_log(
    retrieval_log: RAGRetrievalLogCreate,
    db: Session = Depends(get_db)
):

    """
    Create RAG retrieval log API.
    """

    return create_rag_retrieval_log(
        db,
        retrieval_log
    )


@router.put("/{retrieval_log_id}")
def update_existing_rag_retrieval_log(
    retrieval_log_id: int,
    retrieval_log: RAGRetrievalLogUpdate,
    db: Session = Depends(get_db)
):

    """
    Update RAG retrieval log API.
    """

    return update_rag_retrieval_log(
        db,
        retrieval_log_id,
        retrieval_log
    )


@router.delete("/{retrieval_log_id}")
def delete_existing_rag_retrieval_log(
    retrieval_log_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete RAG retrieval log API.
    """

    return delete_rag_retrieval_log(
        db,
        retrieval_log_id
    )