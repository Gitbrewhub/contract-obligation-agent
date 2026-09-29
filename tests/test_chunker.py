from ingestion.chunker import chunk_text


def test_chunk_text():
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 1000 for chunk in chunks)


def test_chunk_overlap():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunk_text(
        text,
        chunk_size=10,
        overlap=3
    )

    assert chunks[0][-3:] == chunks[1][:3]


def test_empty_text():
    assert chunk_text("") == []