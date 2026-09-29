from ingestion.pipeline import ingest_contract


def test_ingest_docx_contract():
    contract_id = ingest_contract(
        "contracts/uploads/01_Software_Development_Agreement.docx"
    )

    assert contract_id > 0
    