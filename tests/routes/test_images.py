from datetime import datetime
from itertools import chain, repeat
from unittest.mock import AsyncMock, MagicMock

import pytest
from gridfs.errors import NoFile
from motor.motor_gridfs import AgnosticGridOut


class TestImages:
    @pytest.fixture
    def image_file(self):
        grid_out = MagicMock(AgnosticGridOut)
        grid_out.read = AsyncMock(side_effect=chain([b"abc"], repeat(b"")))
        grid_out.upload_date = datetime.now()
        grid_out.content_type = "image/png"
        grid_out.length = 3
        yield grid_out

    def test_get_image_found(self, client, mongodb_fs, image_file):
        mongodb_fs.open_download_stream = AsyncMock(return_value=image_file)

        response = client.get("/images/aaaaaaaaaaaaaaaaaaaaaaaa/")
        assert response.status_code == 200
        assert response.content == b"abc"

    def test_get_image_not_found(self, client, mongodb_fs, image_file):
        mongodb_fs.open_download_stream = AsyncMock(side_effect=NoFile)

        response = client.get("/images/aaaaaaaaaaaaaaaaaaaaaaaa/")
        mongodb_fs.open_download_stream.assert_called_once()
        assert response.status_code == 404
