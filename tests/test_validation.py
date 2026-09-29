import pytest

from agents.validation import (
    Obligation,
    validate_obligation,
    validate_obligations,
)


def test_validate_obligation():
    data = {
        "party_responsible": "Supplier",
        "obligation_text": "Submit a monthly progress report",
        "deadline": "within ten business days after the end of each month",
        "clause_reference": "4.2",
    }

    obligation = validate_obligation(data)

    assert isinstance(obligation, Obligation)
    assert obligation.party_responsible == "Supplier"
    assert obligation.obligation_text == (
        "Submit a monthly progress report"
    )
    assert obligation.deadline == (
        "within ten business days after the end of each month"
    )
    assert obligation.clause_reference == "4.2"


def test_optional_fields_can_be_missing():
    data = {
        "obligation_text": "Maintain adequate insurance coverage"
    }

    obligation = validate_obligation(data)

    assert obligation.obligation_text == (
        "Maintain adequate insurance coverage"
    )
    assert obligation.party_responsible is None
    assert obligation.deadline is None
    assert obligation.clause_reference is None


def test_invalid_obligation_without_text():
    data = {
        "party_responsible": "Supplier",
        "deadline": "30 days",
        "clause_reference": "4.2",
    }

    with pytest.raises(ValueError):
        validate_obligation(data)


def test_validate_multiple_obligations():
    data = [
        {
            "party_responsible": "Supplier",
            "obligation_text": "Submit monthly reports",
            "deadline": "within 10 days",
            "clause_reference": "4.2",
        },
        {
            "party_responsible": "Customer",
            "obligation_text": "Pay the invoice",
            "deadline": "within 30 days",
            "clause_reference": "5.1",
        },
    ]

    obligations = validate_obligations(data)

    assert len(obligations) == 2
    assert isinstance(obligations[0], Obligation)
    assert isinstance(obligations[1], Obligation)