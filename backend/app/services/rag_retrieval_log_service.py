from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.rag_retrieval_log import (
    RAGRetrievalLog
)


def get_rag_retrieval_logs(
    db: Session
):

    return db.query(
        RAGRetrievalLog
    ).all()


def create_rag_retrieval_log(
    db: Session,
    retrieval_log
):

    new_log = RAGRetrievalLog(
        **retrieval_log.model_dump()
    )

    db.add(new_log)

    db.commit()

    db.refresh(new_log)

    return {
        "message":
        "RAG retrieval log created successfully",
        "retrieval_log_data": new_log
    }


def update_rag_retrieval_log(
    db: Session,
    retrieval_log_id: int,
    updated_log
):

    log = db.query(
        RAGRetrievalLog
    ).filter(
        RAGRetrievalLog.retrieval_log_id ==
        retrieval_log_id
    ).first()

    if not log:

        raise HTTPException(
            status_code=404,
            detail="RAG retrieval log not found"
        )

    for key, value in updated_log.model_dump().items():

        setattr(log, key, value)

    db.commit()

    db.refresh(log)

    return {
        "message":
        "RAG retrieval log updated successfully",
        "retrieval_log_data": log
    }


def delete_rag_retrieval_log(
    db: Session,
    retrieval_log_id: int
):

    log = db.query(
        RAGRetrievalLog
    ).filter(
        RAGRetrievalLog.retrieval_log_id ==
        retrieval_log_id
    ).first()

    if not log:

        raise HTTPException(
            status_code=404,
            detail="RAG retrieval log not found"
        )

    db.delete(log)

    db.commit()

    return {
        "message":
        "RAG retrieval log deleted successfully"
    }