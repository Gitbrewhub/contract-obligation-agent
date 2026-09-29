from backend.app import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["service"] == "contract-obligation-agent"


def test_contract_obligations_endpoint():
    client = app.test_client()

    response = client.get(
        "/contracts/1/obligations"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["contract_id"] == 1
    assert "count" in data
    assert "obligations" in data
    assert isinstance(data["obligations"], list)