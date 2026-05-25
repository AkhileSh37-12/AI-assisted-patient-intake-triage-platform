from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.rag_knowledge_base_schema import (
    RAGKnowledgeBaseCreate,
    RAGKnowledgeBaseUpdate
)

from app.services.rag_knowledge_base_service import (
    get_rag_knowledge_base_entries,
    create_rag_knowledge_base_entry,
    update_rag_knowledge_base_entry,
    delete_rag_knowledge_base_entry
)

router = APIRouter(
    prefix="/rag-knowledge-base",
    tags=["RAG Knowledge Base"]
)


@router.get("/")
def get_all_rag_knowledge_base_entries(
    db: Session = Depends(get_db)
):

    """
    Get all RAG knowledge base entries API.
    """

    return get_rag_knowledge_base_entries(db)


@router.post("/")
def create_new_rag_knowledge_base_entry(
    knowledge: RAGKnowledgeBaseCreate,
    db: Session = Depends(get_db)
):

    """
    Create RAG knowledge base entry API.
    """

    return create_rag_knowledge_base_entry(
        db,
        knowledge
    )


@router.put("/{knowledge_id}")
def update_existing_rag_knowledge_base_entry(
    knowledge_id: int,
    knowledge: RAGKnowledgeBaseUpdate,
    db: Session = Depends(get_db)
):

    """
    Update RAG knowledge base entry API.
    """

    return update_rag_knowledge_base_entry(
        db,
        knowledge_id,
        knowledge
    )


@router.delete("/{knowledge_id}")
def delete_existing_rag_knowledge_base_entry(
    knowledge_id: int,
    db: Session = Depends(get_db)
):

    """
    Delete RAG knowledge base entry API.
    """

    return delete_rag_knowledge_base_entry(
        db,
        knowledge_id
    )