from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_client
from api.main import app


@pytest.fixture
def mongodb_client():
    yield MagicMock()


@pytest.fixture
def client(mongodb_client):
    def get_mock_client():
        yield mongodb_client

    app.dependency_overrides[get_client] = get_mock_client

    yield TestClient(app)
