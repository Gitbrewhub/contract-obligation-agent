from pathlib import Path

from ingestion.loader import extract_contract_text
from ingestion.chunker import chunk_text
from ingestion.embedder import generate_embedding
from database.repository import create_contract, insert_document_chunk


def ingest_contract(
    file_path: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> int:
    """
    Ingest a PDF or DOCX contract.

    Pipeline:
    1. Extract contract text
    2. Split text into chunks
    3. Generate an embedding for each chunk
    4. Store the contract and chunks in PostgreSQL
    5. Return the contract ID
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Contract file not found: {file_path}")

    # 1. Extract text
    text = extract_contract_text(str(path))

    if not text.strip():
        raise ValueError("Contract contains no extractable text")

    # 2. Split into chunks
    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    if not chunks:
        raise ValueError("No chunks were generated from the contract")

    # 3. Create contract record
    contract_id = create_contract(path.name)

    # 4. Generate embeddings and store chunks
    for chunk_index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        insert_document_chunk(
            contract_id=contract_id,
            chunk_index=chunk_index,
            content=chunk,
            embedding=embedding,
        )

    return contract_id
