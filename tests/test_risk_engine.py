from datetime import datetime

from agents.risk_engine import (
    calculate_days_until_deadline,
    calculate_risk_tier,
    evaluate_obligation,
)


def test_days_until_deadline():
    reference_date = datetime(2026, 9, 16)
    deadline_date = datetime(2026, 9, 30)

    days = calculate_days_until_deadline(
        deadline_date,
        reference_date,
    )

    assert days == 14


def test_overdue_deadline():
    reference_date = datetime(2026, 9, 16)
    deadline_date = datetime(2026, 9, 10)

    days = calculate_days_until_deadline(
        deadline_date,
        reference_date,
    )

    assert days == -6


def test_no_deadline():
    result = calculate_days_until_deadline(
        None,
        datetime(2026, 9, 16),
    )

    assert result is None


def test_high_risk():
    assert calculate_risk_tier(5, "VERIFIED") == "HIGH"


def test_medium_risk():
    assert calculate_risk_tier(20, "VERIFIED") == "MEDIUM"


def test_low_risk():
    assert calculate_risk_tier(60, "VERIFIED") == "LOW"


def test_no_deadline_risk():
    assert calculate_risk_tier(None, "VERIFIED") == "NO_DEADLINE"


def test_unverified_risk():
    assert calculate_risk_tier(5, "NOT_VERIFIED") == "REVIEW"


def test_complete_evaluation():
    reference_date = datetime(2026, 9, 16)
    deadline_date = datetime(2026, 9, 30)

    result = evaluate_obligation(
        deadline_date=deadline_date,
        reference_date=reference_date,
        verification_status="VERIFIED",
    )

    assert result["days_until_deadline"] == 14
    assert result["risk_tier"] == "MEDIUM"