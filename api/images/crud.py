from typing import AsyncIterator

import pendulum
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from motor.motor_gridfs import AgnosticGridOut

from api.types import ObjectId
from api.utils import to_rfc7231_format


def get_image(fs: AsyncIOMotorGridFSBucket, object_id: ObjectId) -> AgnosticGridOut:
    return fs.open_download_stream(object_id)


def get_image_headers(out: AgnosticGridOut):
    last_modified = pendulum.instance(out.upload_date)
    headers = {
        "Content-Length": str(out.length),
        "Last-Modified": to_rfc7231_format(last_modified),
    }

    try:
        headers["ETag"] = f'"{out.metadata["md5"]}"'
    except KeyError:
        pass

    return headers


async def grid_iter(
    out: AgnosticGridOut, chunk_size: int = 4096
) -> AsyncIterator[bytes]:
    while True:
        content = await out.read(chunk_size)
        if not content:
            break
        yield content
