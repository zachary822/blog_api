from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from motor.motor_gridfs import AgnosticGridOut


class TestImages:
    def test_get_image(self, client, mongodb_fs):
        grid_out = MagicMock(AgnosticGridOut)
        grid_out.read = AsyncMock(side_effect=[b"abc", b""])
        grid_out.upload_date = datetime.now()
        grid_out.content_type = "image/png"
        grid_out.length = 3

        mongodb_fs.open_download_stream = AsyncMock(return_value=grid_out)

        response = client.get("/images/aaaaaaaaaaaaaaaaaaaaaaaa/")
        assert response.status_code == 200
        assert response.content == b"abc"
