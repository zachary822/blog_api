from datetime import datetime
from itertools import chain, repeat
from unittest.mock import AsyncMock, MagicMock

import pytest
from gridfs.errors import NoFile
from motor.motor_asyncio import AsyncIOMotorGridOut


class TestImages:
    @pytest.fixture
    def image_file(self):
        def wrapper(data: bytes):
            grid_out = MagicMock(AsyncIOMotorGridOut)
            grid_out.read = AsyncMock(side_effect=chain([data], repeat(b"")))
            grid_out.upload_date = datetime.now()
            grid_out.content_type = "image/png"
            grid_out.length = 3
            return grid_out

        return wrapper

    def test_get_image_found(self, client, mongodb_fs, image_file):
        mongodb_fs.open_download_stream = AsyncMock(return_value=image_file(b"abc"))

        response = client.get("/images/aaaaaaaaaaaaaaaaaaaaaaaa/")
        assert response.status_code == 200
        assert response.content == b"abc"

    def test_get_image_not_found(self, client, mongodb_fs):
        mongodb_fs.open_download_stream = AsyncMock(side_effect=NoFile)

        response = client.get("/images/aaaaaaaaaaaaaaaaaaaaaaaa/")
        mongodb_fs.open_download_stream.assert_called_once()
        assert response.status_code == 404
