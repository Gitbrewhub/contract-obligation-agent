from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    extraction_node,
    ingest_node,
    risk_node,
    validation_node,
    verification_node,
)

from graph.state import ContractState


def build_contract_graph():
    """
    Build the Contract Obligation Tracking LangGraph.

    Flow:

    START
      ↓
    Ingestion
      ↓
    Extraction
      ↓
    Validation
      ↓
    Verification
      ↓
    Risk Analysis
      ↓
    END
    """

    graph = StateGraph(
        ContractState
    )

    # Register nodes.
    graph.add_node(
        "ingestion",
        ingest_node,
    )

    graph.add_node(
        "extraction",
        extraction_node,
    )

    graph.add_node(
        "validation",
        validation_node,
    )

    graph.add_node(
        "verification",
        verification_node,
    )

    graph.add_node(
        "risk",
        risk_node,
    )

    # Define execution order.
    graph.add_edge(
        START,
        "ingestion",
    )

    graph.add_edge(
        "ingestion",
        "extraction",
    )

    graph.add_edge(
        "extraction",
        "validation",
    )

    graph.add_edge(
        "validation",
        "verification",
    )

    graph.add_edge(
        "verification",
        "risk",
    )

    graph.add_edge(
        "risk",
        END,
    )

    return graph.compile()