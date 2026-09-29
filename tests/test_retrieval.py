from ingestion.pipeline import ingest_contract
from database.retrieval import search_similar_chunks


def test_search_similar_chunks():
    contract_id = ingest_contract(
        "contracts/uploads/01_Software_Development_Agreement.docx"
    )

    results = search_similar_chunks(
        query="What are the obligations of the supplier?",
        contract_id=contract_id,
        top_k=3,
    )

    assert len(results) > 0
    assert len(results) <= 3

    for result in results:
        assert "content" in result
        assert "similarity" in result
        assert 0 <= result["similarity"] <= 1