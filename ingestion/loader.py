from pathlib import Path

from ingestion.pdf_parser import extract_text_from_pdf
from ingestion.docx_parser import extract_text_from_docx


def extract_contract_text(file_path: str) -> str:
    """
    Extract text from a supported contract file.

    Supported formats:
    - PDF
    - DOCX
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Contract file not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(str(path))

    if extension == ".docx":
        return extract_text_from_docx(str(path))

    raise ValueError(
        f"Unsupported contract format: {extension}. "
        "Only PDF and DOCX files are supported."
    )