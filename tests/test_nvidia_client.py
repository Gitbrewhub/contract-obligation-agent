from agents.nvidia_client import ask_nvidia


def test_nvidia_connection():
    response = ask_nvidia(
        "Reply with exactly: NVIDIA connection successful."
    )

    assert response is not None
    assert len(response.strip()) > 0