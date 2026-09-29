from agents.extraction_agent import extract_obligations


def test_extract_obligations():
    chunk = """
    The Supplier shall submit a monthly progress report
    within ten business days after the end of each month.
    """

    obligations = extract_obligations(chunk)

    assert isinstance(obligations, list)
    assert len(obligations) > 0

    obligation = obligations[0]

    assert "party_responsible" in obligation
    assert "obligation_text" in obligation
    assert "deadline" in obligation
    assert "clause_reference" in obligation
    