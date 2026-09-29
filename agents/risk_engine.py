import re
from typing import Optional


HIGH_RISK_PATTERNS = {
    "unlimited_liability": [
        r"unlimited liability",
        r"uncapped liability",
        r"without limitation",
        r"without any limitation",
    ],
    "indemnification": [
        r"indemnif",
        r"hold harmless",
    ],
    "penalties": [
        r"penalt",
        r"liquidated damages",
        r"damages",
    ],
    "termination": [
        r"terminate",
        r"termination",
        r"terminate this agreement",
    ],
}


MEDIUM_RISK_PATTERNS = {
    "automatic_renewal": [
        r"automatic renewal",
        r"automatically renew",
        r"auto-renew",
        r"renewal",
    ],
    "audit_rights": [
        r"audit",
        r"inspection rights",
        r"access to records",
    ],
    "insurance": [
        r"insurance",
        r"insured",
        r"coverage",
    ],
    "confidentiality": [
        r"confidential",
        r"confidentiality",
        r"non-disclosure",
    ],
}


def calculate_days_until_deadline(
    deadline_date,
    reference_date,
) -> Optional[int]:

    if deadline_date is None:
        return None

    return (
        deadline_date.date()
        - reference_date.date()
    ).days


def detect_clause_risks(
    obligation_text: str,
) -> list[dict]:
    """
    Detect contract-risk signals directly from the
    obligation text.

    This is a deterministic safety layer.
    It does not claim legal advice or legal conclusions.
    """

    text = (
        obligation_text
        or ""
    ).lower()

    risks = []

    for category, patterns in HIGH_RISK_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):

                risks.append(
                    {
                        "category": category,
                        "severity": "HIGH",
                        "matched_pattern": pattern,
                    }
                )

                break

    for category, patterns in MEDIUM_RISK_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):

                risks.append(
                    {
                        "category": category,
                        "severity": "MEDIUM",
                        "matched_pattern": pattern,
                    }
                )

                break

    return risks


def calculate_risk_tier(
    days_until_deadline: Optional[int],
    verification_status: str = "PENDING",
    clause_risks: Optional[list[dict]] = None,
) -> str:
    """
    Combine deadline, verification and clause-risk signals.
    """

    clause_risks = clause_risks or []

    if verification_status == "NOT_VERIFIED":
        return "REVIEW"

    has_high_clause_risk = any(
        risk["severity"] == "HIGH"
        for risk in clause_risks
    )

    if has_high_clause_risk:
        return "HIGH"

    if days_until_deadline is not None:

        if days_until_deadline <= 7:
            return "HIGH"

        if days_until_deadline <= 30:
            return "MEDIUM"

        if days_until_deadline > 30:
            return "LOW"

    if any(
        risk["severity"] == "MEDIUM"
        for risk in clause_risks
    ):
        return "MEDIUM"

    if days_until_deadline is None:
        return "NO_DEADLINE"

    return "LOW"


def evaluate_obligation(
    deadline_date,
    reference_date,
    verification_status: str = "PENDING",
    obligation_text: str = "",
) -> dict:

    days_until_deadline = (
        calculate_days_until_deadline(
            deadline_date,
            reference_date,
        )
    )

    clause_risks = detect_clause_risks(
        obligation_text
    )

    risk_tier = calculate_risk_tier(
        days_until_deadline,
        verification_status,
        clause_risks,
    )

    risk_reasons = []

    if days_until_deadline is not None:

        if days_until_deadline < 0:
            risk_reasons.append(
                "Deadline has passed."
            )

        elif days_until_deadline <= 7:
            risk_reasons.append(
                "Deadline is within 7 days."
            )

        elif days_until_deadline <= 30:
            risk_reasons.append(
                "Deadline is within 30 days."
            )

    for risk in clause_risks:

        risk_reasons.append(
            risk["category"].replace(
                "_",
                " ",
            ).title()
        )

    if verification_status == "NOT_VERIFIED":
        risk_reasons.append(
            "Source verification is insufficient."
        )

    return {
        "days_until_deadline": days_until_deadline,
        "risk_tier": risk_tier,
        "clause_risks": clause_risks,
        "risk_reasons": risk_reasons,
    }