from agents.verification_agent import (
    cosine_similarity,
    verify_obligation,
)


def test_cosine_similarity_identical_vectors():
    vector = [1.0, 2.0, 3.0]

    score = cosine_similarity(vector, vector)

    assert abs(score - 1.0) < 0.0001


def test_verify_matching_obligation():
    obligation = (
        "The Supplier shall submit a monthly progress report "
        "within ten business days after the end of each month."
    )

    source = (
        "The Supplier shall submit a monthly progress report "
        "within ten business days after the end of each month."
    )

    result = verify_obligation(
        obligation_text=obligation,
        source_text=source,
    )

    assert result["verification_status"] == "VERIFIED"
    assert result["grounding_score"] >= 0.70


def test_verify_unrelated_text():
    obligation = (
        "The Supplier shall submit a monthly progress report."
    )

    source = (
        "The Customer may terminate this agreement "
        "upon thirty days written notice."
    )

    result = verify_obligation(
        obligation_text=obligation,
        source_text=source,
    )

    assert result["verification_status"] == "NOT_VERIFIED"
    assert result["grounding_score"] < 0.70