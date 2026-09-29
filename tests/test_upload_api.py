import io

from backend.app import app


def test_upload_without_file():
    client = app.test_client()

    response = client.post(
        "/contracts/upload"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "No file provided"


def test_upload_unsupported_file():
    client = app.test_client()

    response = client.post(
        "/contracts/upload",
        data={
            "file": (
                io.BytesIO(b"fake image"),
                "contract.txt",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "Unsupported file type" in data["error"]