from sqlalchemy.orm import Session

from app.models.rag_knowledge_base import (
    RAGKnowledgeBase
)

from app.ai.rag.embedding_service import (
    generate_embedding
)


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    top_k: int = 3
):

    query_embedding = generate_embedding(
        query
    )

    results = (
        db.query(RAGKnowledgeBase)
        .order_by(
            RAGKnowledgeBase.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(10)
        .all()
    )

    unique_results = []
    seen_titles = set()

    for item in results:

        if item.title not in seen_titles:

            unique_results.append(item)

            seen_titles.add(
                item.title
            )

        if len(unique_results) == top_k:

            break

    return unique_results