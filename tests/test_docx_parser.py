from ingestion.docx_parser import extract_text_from_docx


def test_extract_text_from_docx():
    text = extract_text_from_docx(
        "contracts/uploads/01_Software_Development_Agreement.docx"
    )

    assert text.strip() != ""