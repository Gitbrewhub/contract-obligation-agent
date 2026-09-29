from ingestion.embedder import generate_embedding


def test_generate_embedding():
    text = "The supplier shall submit the monthly report."

    embedding = generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert all(isinstance(value, float) for value in embedding)