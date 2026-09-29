from datetime import datetime
from pathlib import Path

from agents.extraction_agent import extract_obligations
from agents.risk_engine import evaluate_obligation
from agents.validation import validate_obligations
from agents.verification_agent import verify_with_nvidia

from database.repository import (
    create_contract,
    insert_document_chunk,
    insert_obligation,
)

from database.retrieval import search_similar_chunks

from ingestion.chunker import chunk_text
from ingestion.embedder import generate_embedding
from ingestion.loader import extract_contract_text

from utils.deadline_parser import parse_deadline


def process_contract(
    file_path: str,
    reference_date: datetime | None = None,
) -> list[dict]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Contract file not found: {file_path}"
        )

    if reference_date is None:
        reference_date = datetime.now()

    # ---------------------------------------------------------
    # 1. Extract contract text
    # ---------------------------------------------------------

    contract_text = extract_contract_text(
        str(path)
    )

    if not contract_text.strip():
        raise ValueError(
            "Contract contains no extractable text"
        )

    # ---------------------------------------------------------
    # 2. Chunk contract
    # ---------------------------------------------------------

    chunks = chunk_text(contract_text)

    if not chunks:
        raise ValueError(
            "No chunks were generated"
        )

    # ---------------------------------------------------------
    # 3. Create contract record
    # ---------------------------------------------------------

    contract_id = create_contract(
        path.name
    )

    results = []

    # ---------------------------------------------------------
    # 4. Process chunks
    # ---------------------------------------------------------

    for chunk_index, chunk in enumerate(chunks):

        # -----------------------------------------------------
        # Store chunk + embedding
        # -----------------------------------------------------

        embedding = generate_embedding(
            chunk
        )

        source_chunk_id = insert_document_chunk(
            contract_id=contract_id,
            chunk_index=chunk_index,
            content=chunk,
            embedding=embedding,
        )

        # -----------------------------------------------------
        # Extract obligations
        # -----------------------------------------------------

        extracted = extract_obligations(
            chunk
        )

        # -----------------------------------------------------
        # Validate obligations
        # -----------------------------------------------------

        validated = validate_obligations(
            extracted
        )

        # -----------------------------------------------------
        # Process each obligation
        # -----------------------------------------------------

        for obligation in validated:

            # -------------------------------------------------
            # Parse deadline
            # -------------------------------------------------

            deadline_date = parse_deadline(
                obligation.deadline
            )

            # -------------------------------------------------
            # Retrieve relevant source chunks
            # -------------------------------------------------

            similar_chunks = search_similar_chunks(
                query=obligation.obligation_text,
                contract_id=contract_id,
                top_k=3,
            )

            # -------------------------------------------------
            # Verify against retrieved evidence
            # -------------------------------------------------

            best_source_chunk_id = source_chunk_id
            best_source_chunk_index = chunk_index
            best_source_text = chunk

            verification = None

            for candidate in similar_chunks:

                candidate_result = verify_with_nvidia(
                    obligation_text=(
                        obligation.obligation_text
                    ),
                    source_text=candidate["content"],
                )

                if (
                    verification is None
                    or candidate_result["grounding_score"]
                    > verification["grounding_score"]
                ):
                    verification = candidate_result

                    best_source_chunk_id = candidate["id"]
                    best_source_chunk_index = (
                        candidate["chunk_index"]
                    )
                    best_source_text = candidate["content"]

            # -------------------------------------------------
            # Safety fallback
            # -------------------------------------------------

            if verification is None:

                verification = verify_with_nvidia(
                    obligation_text=(
                        obligation.obligation_text
                    ),
                    source_text=chunk,
                )

            # -------------------------------------------------
            # Determine verification status
            # -------------------------------------------------

            verification_status = (
                "VERIFIED"
                if verification["verified"]
                else "NOT_VERIFIED"
            )

            # -------------------------------------------------
            # Calculate risk
            # -------------------------------------------------

            risk = evaluate_obligation(
                deadline_date,
                reference_date,
                verification_status,
            )

            # -------------------------------------------------
            # Save obligation
            # -------------------------------------------------

            obligation_id = insert_obligation(
                contract_id=contract_id,
                party_responsible=(
                    obligation.party_responsible
                ),
                obligation_text=(
                    obligation.obligation_text
                ),
                deadline=obligation.deadline,
                clause_reference=(
                    obligation.clause_reference
                ),
                verification_status=(
                    verification_status
                ),
                grounding_score=(
                    verification["grounding_score"]
                ),
                risk_tier=risk["risk_tier"],
                days_until_deadline=(
                    risk["days_until_deadline"]
                ),
                source_chunk_id=(
                    best_source_chunk_id
                ),
            )

            # -------------------------------------------------
            # API result
            # -------------------------------------------------

            results.append(
                {
                    "id": obligation_id,
                    "contract_id": contract_id,
                    "party_responsible": (
                        obligation.party_responsible
                    ),
                    "obligation_text": (
                        obligation.obligation_text
                    ),
                    "deadline": (
                        obligation.deadline
                    ),
                    "parsed_deadline": (
                        deadline_date
                    ),
                    "clause_reference": (
                        obligation.clause_reference
                    ),
                    "source_chunk_id": (
                        best_source_chunk_id
                    ),
                    "source_chunk_index": (
                        best_source_chunk_index
                    ),
                    "source_text": (
                        verification.get(
                            "source_text",
                            best_source_text,
                        )
                    ),
                    "verification_status": (
                        verification_status
                    ),
                    "grounding_score": (
                        verification[
                            "grounding_score"
                        ]
                    ),
                    "verification_reason": (
                        verification.get(
                            "reason",
                            "",
                        )
                    ),
                    "days_until_deadline": (
                        risk[
                            "days_until_deadline"
                        ]
                    ),
                    "risk_tier": (
                        risk["risk_tier"]
                    ),
                }
            )

    return results