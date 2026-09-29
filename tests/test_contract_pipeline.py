from datetime import datetime

from pipeline.contract_pipeline import process_contract


def test_process_contract():
    contract_path = (
        "contracts/uploads/"
        "01_Software_Development_Agreement.docx"
    )

    results = process_contract(
        contract_path,
        reference_date=datetime(2026, 9, 16),
    )

    assert isinstance(results, list)

    for result in results:
        assert "party_responsible" in result
        assert "obligation_text" in result
        assert "deadline" in result
        assert "clause_reference" in result
        assert "verification_status" in result
        assert "grounding_score" in result
        assert "days_until_deadline" in result
        assert "risk_tier" in result
        assert "source_chunk_index" in result