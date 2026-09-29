from datetime import datetime

from graph.workflow import build_contract_graph


def test_contract_graph_structure():
    """
    Verify that the LangGraph workflow is compiled
    and contains all expected nodes.
    """

    graph = build_contract_graph()

    node_names = set(
        graph.nodes.keys()
    )

    expected_nodes = {
        "ingestion",
        "extraction",
        "validation",
        "verification",
        "risk",
    }

    assert expected_nodes.issubset(
        node_names
    )


def test_contract_graph_execution():
    """
    Execute the complete LangGraph workflow against
    the sample contract.

    This is an integration test and will call NVIDIA NIM.
    """

    graph = build_contract_graph()

    result = graph.invoke(
        {
            "file_path": (
                "contracts/uploads/"
                "01_Software_Development_Agreement.docx"
            ),
            "reference_date": datetime(
                2026,
                9,
                16,
            ),
        }
    )

    assert result["contract_id"] is not None

    assert "results" in result

    assert isinstance(
        result["results"],
        list,
    )

    assert len(
        result["results"]
    ) > 0

    first_result = result[
        "results"
    ][0]

    assert "obligation_text" in first_result

    assert "verification_status" in first_result

    assert "grounding_score" in first_result

    assert "risk_tier" in first_result