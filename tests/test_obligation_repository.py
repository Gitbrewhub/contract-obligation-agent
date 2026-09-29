from database.repository import (
    create_contract,
    insert_document_chunk,
    insert_obligation,
)


def test_insert_obligation():
    contract_id = create_contract(
        "repository_obligation_test.docx"
    )

    chunk_id = insert_document_chunk(
        contract_id=contract_id,
        chunk_index=0,
        content=(
            "The Supplier shall submit a monthly report "
            "within 10 days."
        ),
        embedding=[0.1] * 384,
    )

    obligation_id = insert_obligation(
        contract_id=contract_id,
        party_responsible="Supplier",
        obligation_text="Submit a monthly report",
        deadline="within 10 days",
        clause_reference="4.2",
        verification_status="VERIFIED",
        grounding_score=0.91,
        risk_tier="MEDIUM",
        days_until_deadline=14,
        source_chunk_id=chunk_id,
    )

    assert isinstance(obligation_id, int)
    assert obligation_id > 0