from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.rag_knowledge_base import (
    RAGKnowledgeBase
)


def get_rag_knowledge_base_entries(
    db: Session
):

    return db.query(
        RAGKnowledgeBase
    ).all()


def create_rag_knowledge_base_entry(
    db: Session,
    knowledge
):

    new_knowledge = RAGKnowledgeBase(
        **knowledge.model_dump()
    )

    db.add(new_knowledge)

    db.commit()

    db.refresh(new_knowledge)

    return {
        "message":
        "RAG knowledge base entry created successfully",
        "knowledge_data": new_knowledge
    }


def update_rag_knowledge_base_entry(
    db: Session,
    knowledge_id: int,
    updated_knowledge
):

    knowledge = db.query(
        RAGKnowledgeBase
    ).filter(
        RAGKnowledgeBase.knowledge_id == knowledge_id
    ).first()

    if not knowledge:

        raise HTTPException(
            status_code=404,
            detail="Knowledge entry not found"
        )

    for key, value in updated_knowledge.model_dump().items():

        setattr(knowledge, key, value)

    db.commit()

    db.refresh(knowledge)

    return {
        "message":
        "RAG knowledge base entry updated successfully",
        "knowledge_data": knowledge
    }


def delete_rag_knowledge_base_entry(
    db: Session,
    knowledge_id: int
):

    knowledge = db.query(
        RAGKnowledgeBase
    ).filter(
        RAGKnowledgeBase.knowledge_id == knowledge_id
    ).first()

    if not knowledge:

        raise HTTPException(
            status_code=404,
            detail="Knowledge entry not found"
        )

    db.delete(knowledge)

    db.commit()

    return {
        "message":
        "RAG knowledge base entry deleted successfully"
    }