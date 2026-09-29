from sqlalchemy import text

from database.db import engine


def create_contract(filename: str) -> int:
    """
    Create a contract record and return its database ID.
    """

    query = text("""
        INSERT INTO contracts (filename)
        VALUES (:filename)
        RETURNING id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "filename": filename,
            },
        )

        return result.scalar_one()


def insert_document_chunk(
    contract_id: int,
    chunk_index: int,
    content: str,
    embedding: list[float],
) -> int:
    """
    Store a document chunk and its embedding.
    """

    query = text("""
        INSERT INTO document_chunks (
            contract_id,
            chunk_index,
            content,
            embedding
        )
        VALUES (
            :contract_id,
            :chunk_index,
            :content,
            :embedding
        )
        RETURNING id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "contract_id": contract_id,
                "chunk_index": chunk_index,
                "content": content,
                "embedding": embedding,
            },
        )

        return result.scalar_one()


def insert_obligation(
    contract_id: int,
    party_responsible: str | None,
    obligation_text: str,
    deadline: str | None,
    clause_reference: str | None,
    verification_status: str,
    grounding_score: float | None,
    risk_tier: str | None,
    days_until_deadline: int | None,
    source_chunk_id: int | None,
) -> int:
    """
    Store an analyzed contractual obligation
    and return its database ID.
    """

    query = text("""
        INSERT INTO obligations (
            contract_id,
            party_responsible,
            obligation_text,
            deadline,
            clause_reference,
            verification_status,
            grounding_score,
            risk_tier,
            days_until_deadline,
            source_chunk_id
        )
        VALUES (
            :contract_id,
            :party_responsible,
            :obligation_text,
            :deadline,
            :clause_reference,
            :verification_status,
            :grounding_score,
            :risk_tier,
            :days_until_deadline,
            :source_chunk_id
        )
        RETURNING id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "contract_id": contract_id,
                "party_responsible": party_responsible,
                "obligation_text": obligation_text,
                "deadline": deadline,
                "clause_reference": clause_reference,
                "verification_status": verification_status,
                "grounding_score": grounding_score,
                "risk_tier": risk_tier,
                "days_until_deadline": days_until_deadline,
                "source_chunk_id": source_chunk_id,
            },
        )

        return result.scalar_one()