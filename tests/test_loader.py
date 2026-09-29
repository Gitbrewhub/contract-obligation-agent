from ingestion.loader import extract_contract_text


def test_extract_contract_text_from_docx():
    text = extract_contract_text(
        "contracts/uploads/01_Software_Development_Agreement.docx"
    )

    assert text.strip() != ""