from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.rag_knowledge_base import (
    RAGKnowledgeBase
)

from app.ai.rag.embedding_service import (
    generate_embedding
)

def get_rag_knowledge_base_entries(
    db: Session
):

    entries = db.query(
        RAGKnowledgeBase
    ).all()

    return [
        {
            "knowledge_id": entry.knowledge_id,
            "title": entry.title,
            "category": entry.category,
            "source": entry.source,
            "content": entry.content,
            "medical_specialty": entry.medical_specialty,
            "keywords": entry.keywords,
            "chunk_index": entry.chunk_index,
            "created_at": entry.created_at,
            "updated_at": entry.updated_at
        }
        for entry in entries
    ]


def create_rag_knowledge_base_entry(
    db: Session,
    knowledge
):

    embedding_text = f"""
    {knowledge.title}

    {knowledge.content}

    {knowledge.keywords or ""}
    """

    embedding = generate_embedding(
        embedding_text
    )

    new_knowledge = RAGKnowledgeBase(

        title=knowledge.title,

        category=knowledge.category,

        source=knowledge.source,

        content=knowledge.content,

        medical_specialty=
        knowledge.medical_specialty,

        keywords=knowledge.keywords,

        chunk_index=
        knowledge.chunk_index,

        embedding=embedding
    )

    db.add(new_knowledge)

    db.commit()

    db.refresh(new_knowledge)

    return {
        "message":
        "RAG knowledge base entry created successfully",
        "knowledge_id":
        new_knowledge.knowledge_id
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
    
    embedding_text = f"""
    {knowledge.title}

    {knowledge.content}

    {knowledge.keywords or ""}
    """

    knowledge.embedding = generate_embedding(
        embedding_text
    )
    
    db.commit()

    db.refresh(knowledge)

    return {
        "message":
        "RAG knowledge base entry updated successfully",

        "knowledge_id":
        knowledge.knowledge_id
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