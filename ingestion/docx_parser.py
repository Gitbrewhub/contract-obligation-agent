from docx import Document


def extract_text_from_docx(docx_path: str) -> str:
    """
    Extract text from paragraphs in a DOCX document.
    """

    document = Document(docx_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)