from ingestion.pdf_parser import extract_text_from_pdf


def test_extract_text_from_pdf():
    text = extract_text_from_pdf(
        "contracts/uploads/sample_contract.pdf"
    )

    assert text.strip() != ""