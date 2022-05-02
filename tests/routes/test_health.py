from unittest.mock import AsyncMock


def test_health(client, mongodb_client):
    mongodb_client.server_info = AsyncMock(return_value={"version": "0.0.0"})

    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mongo_version": "0.0.0"}
