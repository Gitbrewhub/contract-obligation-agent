from database.repository import create_contract, insert_obligation
from database.retrieval import get_obligations_by_contract


def test_get_obligations_by_contract():
    contract_id = create_contract(
        "retrieval_test_contract.docx"
    )

    insert_obligation(
        contract_id=contract_id,
        party_responsible="Supplier",
        obligation_text="Submit monthly report",
        deadline="within 10 days",
        clause_reference="4.2",
        verification_status="VERIFIED",
        grounding_score=0.91,
        risk_tier="MEDIUM",
        days_until_deadline=14,
        source_chunk_id=None,
    )

    insert_obligation(
        contract_id=contract_id,
        party_responsible="Customer",
        obligation_text="Pay the invoice",
        deadline="within 30 days",
        clause_reference="5.1",
        verification_status="VERIFIED",
        grounding_score=0.88,
        risk_tier="LOW",
        days_until_deadline=25,
        source_chunk_id=None,
    )

    obligations = get_obligations_by_contract(
        contract_id
    )

    assert len(obligations) == 2

    assert obligations[0]["party_responsible"] == "Supplier"
    assert obligations[0]["obligation_text"] == (
        "Submit monthly report"
    )
    assert obligations[0]["verification_status"] == "VERIFIED"

    assert obligations[1]["party_responsible"] == "Customer"
    assert obligations[1]["risk_tier"] == "LOW"