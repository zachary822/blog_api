from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_client, get_fs, get_session
from api.main import app


@pytest.fixture
def mongodb_client():
    yield MagicMock()


@pytest.fixture
def mongodb_session():
    yield MagicMock()


@pytest.fixture
def mongodb_fs():
    yield MagicMock()


@pytest.fixture
def client(mongodb_client, mongodb_fs, mongodb_session):
    async def get_mock_client():
        yield mongodb_client

    async def get_mock_session():
        yield mongodb_session

    async def get_mock_fs():
        yield mongodb_fs

    with patch.dict(
        app.dependency_overrides,
        {
            get_client: get_mock_client,
            get_fs: get_mock_fs,
            get_session: get_mock_session,
        },
    ):
        yield TestClient(app)
