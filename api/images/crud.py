from typing import AsyncIterator

import pendulum
from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorGridFSBucket,
    AsyncIOMotorGridOut,
)

from api.types import ObjectId
from api.utils import to_rfc7231_format


def get_image(
    fs: AsyncIOMotorGridFSBucket,
    session: AsyncIOMotorClientSession,
    object_id: ObjectId,
) -> AsyncIOMotorGridOut:
    return fs.open_download_stream(object_id, session=session)


def get_image_headers(out: AsyncIOMotorGridOut):
    last_modified = pendulum.instance(out.upload_date)
    headers = {
        "Content-Length": str(out.length),
        "Last-Modified": to_rfc7231_format(last_modified),
        "Cache-Control": "max-age=604800, must-revalidate",
    }

    try:
        headers["ETag"] = f'"{out.metadata["md5"]}"'
    except KeyError:
        pass

    return headers


async def grid_iter(out: AsyncIOMotorGridOut, chunk_size: int = 4096) -> AsyncIterator[bytes]:
    while content := await out.read(chunk_size):
        yield content
