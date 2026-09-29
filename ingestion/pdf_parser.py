import fitz


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from every page of a PDF.
    """
    document = fitz.open(pdf_path)

    pages = []

    for page in document:
        text = page.get_text()
        pages.append(text)

    document.close()

    return "\n".join(pages)