def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Split contract text into overlapping chunks.

    Args:
        text: Extracted contract text.
        chunk_size: Maximum number of characters in each chunk.
        overlap: Number of characters shared between consecutive chunks.

    Returns:
        A list of text chunks.
    """

    if not text or not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        if end >= len(text):
            break

        start = end - overlap

    return chunks