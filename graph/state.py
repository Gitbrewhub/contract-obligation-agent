from typing import Any, TypedDict


class ContractState(TypedDict, total=False):
    """
    Shared state passed between LangGraph nodes.

    Each node reads the information it needs from this state
    and adds its results back into the state.
    """

    # Input
    file_path: str
    reference_date: Any

    # Ingestion
    contract_id: int
    contract_text: str
    chunks: list[str]

    # Extraction
    extracted_obligations: list[dict]

    # Validation
    validated_obligations: list[dict]

    # Verification + risk
    processed_obligations: list[dict]

    # Final result
    results: list[dict]

    # Error handling
    error: str | None
    