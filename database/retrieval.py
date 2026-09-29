from sqlalchemy import text

from database.db import engine
from ingestion.embedder import generate_embedding


def search_similar_chunks(
    query: str,
    contract_id: int,
    top_k: int = 5,
) -> list[dict]:
    """
    Find the most semantically similar contract chunks
    for a given query.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    query_embedding = generate_embedding(query)

    sql = text("""
        SELECT
            id,
            chunk_index,
            content,
            1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM document_chunks
        WHERE contract_id = :contract_id
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
    """)

    with engine.connect() as connection:
        result = connection.execute(
            sql,
            {
                "embedding": str(query_embedding),
                "contract_id": contract_id,
                "top_k": top_k,
            },
        )

        return [
            {
                "id": row.id,
                "chunk_index": row.chunk_index,
                "content": row.content,
                "similarity": float(row.similarity),
            }
            for row in result
        ]


def get_obligations_by_contract(
    contract_id: int,
) -> list[dict]:
    """
    Retrieve all obligations belonging to a contract.
    """

    sql = text("""
        SELECT
            id,
            contract_id,
            party_responsible,
            obligation_text,
            deadline,
            clause_reference,
            verification_status,
            grounding_score,
            risk_tier,
            days_until_deadline,
            source_chunk_id,
            created_at
        FROM obligations
        WHERE contract_id = :contract_id
        ORDER BY id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            sql,
            {
                "contract_id": contract_id,
            },
        )

        return [
            {
                "id": row.id,
                "contract_id": row.contract_id,
                "party_responsible": row.party_responsible,
                "obligation_text": row.obligation_text,
                "deadline": row.deadline,
                "clause_reference": row.clause_reference,
                "verification_status": (
                    row.verification_status
                ),
                "grounding_score": (
                    float(row.grounding_score)
                    if row.grounding_score is not None
                    else None
                ),
                "risk_tier": row.risk_tier,
                "days_until_deadline": (
                    row.days_until_deadline
                ),
                "source_chunk_id": row.source_chunk_id,
                "created_at": row.created_at,
            }
            for row in result
        ]