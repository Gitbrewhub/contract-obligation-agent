from datetime import datetime
from pathlib import Path

from agents.extraction_agent import extract_obligations
from agents.risk_engine import evaluate_obligation
from agents.validation import validate_obligations
from agents.verification_agent import verify_obligation

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

from graph.state import ContractState


# =========================================================
# INGESTION NODE
# =========================================================

def ingest_node(
    state: ContractState,
) -> ContractState:
    """
    LangGraph node responsible for:

    1. Loading the contract
    2. Extracting text
    3. Splitting text into chunks
    4. Creating the contract record
    5. Generating embeddings
    6. Storing document chunks
    """

    file_path = state[
        "file_path"
    ]

    path = Path(
        file_path
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Contract file not found: {file_path}"
        )

    # -----------------------------------------------------
    # Extract contract text
    # -----------------------------------------------------

    contract_text = extract_contract_text(
        str(path)
    )

    if not contract_text.strip():
        raise ValueError(
            "Contract contains no extractable text"
        )

    # -----------------------------------------------------
    # Split contract into chunks
    # -----------------------------------------------------

    chunks = chunk_text(
        contract_text
    )

    if not chunks:
        raise ValueError(
            "No chunks were generated"
        )

    # -----------------------------------------------------
    # Create contract database record
    # -----------------------------------------------------

    contract_id = create_contract(
        path.name
    )

    # -----------------------------------------------------
    # Generate embeddings and store chunks
    # -----------------------------------------------------

    for chunk_index, chunk in enumerate(
        chunks
    ):

        embedding = generate_embedding(
            chunk
        )

        insert_document_chunk(
            contract_id=contract_id,
            chunk_index=chunk_index,
            content=chunk,
            embedding=embedding,
        )

    # -----------------------------------------------------
    # Return updated LangGraph state
    # -----------------------------------------------------

    return {
        **state,
        "contract_id": contract_id,
        "contract_text": contract_text,
        "chunks": chunks,
    }


# =========================================================
# EXTRACTION NODE
# =========================================================

def extraction_node(
    state: ContractState,
) -> ContractState:
    """
    Extract contractual obligations from every
    contract chunk using the NVIDIA extraction agent.
    """

    chunks = state[
        "chunks"
    ]

    extracted_obligations = []

    # -----------------------------------------------------
    # Extract obligations from every chunk
    # -----------------------------------------------------

    for chunk in chunks:

        obligations = extract_obligations(
            chunk
        )

        extracted_obligations.extend(
            obligations
        )

    # -----------------------------------------------------
    # Return extracted obligations
    # -----------------------------------------------------

    return {
        **state,
        "extracted_obligations": (
            extracted_obligations
        ),
    }


# =========================================================
# VALIDATION NODE
# =========================================================

def validation_node(
    state: ContractState,
) -> ContractState:
    """
    Validate extracted obligations using Pydantic.
    """

    extracted = state[
        "extracted_obligations"
    ]

    # -----------------------------------------------------
    # Validate all extracted obligations
    # -----------------------------------------------------

    validated = validate_obligations(
        extracted
    )

    # -----------------------------------------------------
    # Convert Pydantic models to dictionaries
    # -----------------------------------------------------

    validated_dicts = [
        obligation.model_dump()
        for obligation in validated
    ]

    # -----------------------------------------------------
    # Return validated obligations
    # -----------------------------------------------------

    return {
        **state,
        "validated_obligations": (
            validated_dicts
        ),
    }


# =========================================================
# VERIFICATION NODE
# =========================================================

def verification_node(
    state: ContractState,
) -> ContractState:
    """
    Verify each validated obligation against the
    most relevant source chunks.

    Verification uses semantic similarity rather than
    another NVIDIA generation call.

    This avoids repeated JSON-generation failures and
    significantly reduces NVIDIA API calls.
    """

    contract_id = state[
        "contract_id"
    ]

    chunks = state[
        "chunks"
    ]

    validated = state[
        "validated_obligations"
    ]

    processed_obligations = []

    # -----------------------------------------------------
    # Process every validated obligation
    # -----------------------------------------------------

    for obligation in validated:

        obligation_text = obligation[
            "obligation_text"
        ]

        # -------------------------------------------------
        # Retrieve the most semantically relevant chunks
        # -------------------------------------------------

        similar_chunks = search_similar_chunks(
            query=obligation_text,
            contract_id=contract_id,
            top_k=3,
        )

        # -------------------------------------------------
        # Fallback if semantic search returns nothing
        # -------------------------------------------------

        if not similar_chunks:

            similar_chunks = [
                {
                    "id": None,
                    "chunk_index": None,
                    "content": chunks[0],
                }
            ]

        # -------------------------------------------------
        # Find the strongest supporting source chunk
        # -------------------------------------------------

        best_verification = None
        best_chunk = None

        for candidate in similar_chunks:

            verification = verify_obligation(
                obligation_text=obligation_text,
                source_text=candidate[
                    "content"
                ],
            )

            # ---------------------------------------------
            # Keep the candidate with the highest
            # grounding score
            # ---------------------------------------------

            if (
                best_verification is None
                or verification[
                    "grounding_score"
                ]
                > best_verification[
                    "grounding_score"
                ]
            ):

                best_verification = (
                    verification
                )

                best_chunk = candidate

        # -------------------------------------------------
        # Safety check
        # -------------------------------------------------

        if (
            best_verification is None
            or best_chunk is None
        ):
            raise ValueError(
                "Unable to verify extracted obligation"
            )

        # -------------------------------------------------
        # Convert semantic verification result into
        # application-level verification status
        # -------------------------------------------------

        verification_status = (
            "VERIFIED"
            if best_verification[
                "verified"
            ]
            else "NOT_VERIFIED"
        )

        # -------------------------------------------------
        # Store complete processed obligation
        # -------------------------------------------------

        processed_obligations.append(
            {
                **obligation,

                "verification_status": (
                    verification_status
                ),

                "grounding_score": (
                    best_verification[
                        "grounding_score"
                    ]
                ),

                "source_chunk_id": (
                    best_chunk[
                        "id"
                    ]
                ),

                "source_chunk_index": (
                    best_chunk[
                        "chunk_index"
                    ]
                ),

                "source_text": (
                    best_verification.get(
                        "source_text",
                        best_chunk[
                            "content"
                        ],
                    )
                ),

                "verification_reason": (
                    best_verification.get(
                        "reason",
                        "",
                    )
                ),
            }
        )

    # -----------------------------------------------------
    # Return verified obligations
    # -----------------------------------------------------

    return {
        **state,
        "processed_obligations": (
            processed_obligations
        ),
    }


# =========================================================
# RISK ANALYSIS NODE
# =========================================================

def risk_node(
    state: ContractState,
) -> ContractState:
    """
    Calculate risk information for every verified
    contractual obligation.

    Risk analysis combines:

    1. Deadline proximity
    2. Verification status
    3. Clause-risk signals
    4. Risk reasons

    The risk engine receives the actual obligation text,
    allowing it to detect clause-level risk patterns.
    """

    reference_date = state.get(
        "reference_date"
    )

    if reference_date is None:
        reference_date = datetime.now()

    processed = state[
        "processed_obligations"
    ]

    final_results = []

    # -----------------------------------------------------
    # Analyze every processed obligation
    # -----------------------------------------------------

    for obligation in processed:

        # -------------------------------------------------
        # Parse contractual deadline
        # -------------------------------------------------

        deadline_date = parse_deadline(
            obligation.get(
                "deadline"
            )
        )

        # -------------------------------------------------
        # Evaluate deadline + verification +
        # clause-level risk
        # -------------------------------------------------

        risk = evaluate_obligation(
            deadline_date=deadline_date,
            reference_date=reference_date,
            verification_status=(
                obligation[
                    "verification_status"
                ]
            ),
            obligation_text=(
                obligation[
                    "obligation_text"
                ]
            ),
        )

        # -------------------------------------------------
        # Build final obligation result
        # -------------------------------------------------

        result = {
            **obligation,

            "parsed_deadline": (
                deadline_date
            ),

            "days_until_deadline": (
                risk[
                    "days_until_deadline"
                ]
            ),

            "risk_tier": (
                risk[
                    "risk_tier"
                ]
            ),

            "clause_risks": (
                risk.get(
                    "clause_risks",
                    []
                )
            ),

            "risk_reasons": (
                risk.get(
                    "risk_reasons",
                    []
                )
            ),
        }

        # -------------------------------------------------
        # Store obligation in PostgreSQL
        # -------------------------------------------------

        obligation_id = insert_obligation(
            contract_id=state[
                "contract_id"
            ],

            party_responsible=(
                obligation.get(
                    "party_responsible"
                )
            ),

            obligation_text=(
                obligation[
                    "obligation_text"
                ]
            ),

            deadline=(
                obligation.get(
                    "deadline"
                )
            ),

            clause_reference=(
                obligation.get(
                    "clause_reference"
                )
            ),

            verification_status=(
                obligation[
                    "verification_status"
                ]
            ),

            grounding_score=(
                obligation[
                    "grounding_score"
                ]
            ),

            risk_tier=(
                risk[
                    "risk_tier"
                ]
            ),

            days_until_deadline=(
                risk[
                    "days_until_deadline"
                ]
            ),

            source_chunk_id=(
                obligation.get(
                    "source_chunk_id"
                )
            ),
        )

        # -------------------------------------------------
        # Add database ID to final result
        # -------------------------------------------------

        result[
            "id"
        ] = obligation_id

        final_results.append(
            result
        )

    # -----------------------------------------------------
    # Return final LangGraph state
    # -----------------------------------------------------

    return {
        **state,
        "results": final_results,
    }