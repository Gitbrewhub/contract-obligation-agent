from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class Obligation(BaseModel):
    """
    Structured representation of a contractual obligation.
    """

    model_config = ConfigDict(extra="ignore")

    party_responsible: Optional[str] = None
    obligation_text: str
    deadline: Optional[str] = None
    clause_reference: Optional[str] = None


def validate_obligation(data: dict) -> Obligation:
    """
    Validate a single extracted obligation.

    Args:
        data: Raw obligation dictionary returned by the LLM.

    Returns:
        A validated Obligation object.

    Raises:
        ValueError: If the obligation does not satisfy the schema.
    """

    try:
        return Obligation.model_validate(data)

    except ValidationError as exc:
        raise ValueError(
            f"Invalid obligation data: {exc}"
        ) from exc


def validate_obligations(data: list[dict]) -> list[Obligation]:
    """
    Validate a list of extracted obligations.

    Args:
        data: List of raw obligation dictionaries.

    Returns:
        List of validated Obligation objects.

    Raises:
        ValueError: If the input is not a list or contains
                    invalid obligation data.
    """

    if not isinstance(data, list):
        raise ValueError("Obligations must be provided as a list")

    validated_obligations = []

    for item in data:
        validated_obligations.append(
            validate_obligation(item)
        )

    return validated_obligations